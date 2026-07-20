import frappe
from frappe.permissions import add_permission, update_permission_property


def execute():
	doctype_name = "Issue"
	role = "Employee - NDMA"
	status_options = "\nOpen\nSubmitted\nOn Hold\nIn Progress\nResolved\nRejected"

	status_field_name = frappe.db.get_value("DocField", {"parent": doctype_name, "fieldname": "status"}, "name")
	if status_field_name:
		frappe.db.set_value(
			"DocField",
			status_field_name,
			"options",
			status_options,
			update_modified=False,
		)

	if not frappe.db.exists("Role", role):
		return

	# Grant read on linked doctypes used by Issue link fields (e.g. Location -> Branch).
	# Branch uses Custom DocPerm which overrides standard DocPerm, so the role must be added explicitly.
	for linked_doctype in ("Branch",):
		add_permission(linked_doctype, role, permlevel=0, ptype="read")
		update_permission_property(
			linked_doctype,
			role,
			0,
			"read",
			value=1,
			validate=False,
		)

	# Ensure custom permissions exist and grant requester permissions.
	add_permission(doctype_name, role, permlevel=0, ptype="read")

	permission_values = {
		"read": 1,
		"write": 1,
		"create": 1,
		"submit": 1,
		"cancel": 0,
	}

	for ptype, value in permission_values.items():
		update_permission_property(
			doctype_name,
			role,
			0,
			ptype,
			value=value,
			validate=False,
		)

	workflow_name = frappe.db.get_value(
		"Workflow",
		{"document_type": doctype_name, "is_active": 1},
		"name",
	)
	if not workflow_name:
		frappe.clear_cache(doctype=doctype_name)
		return

	transition_name = frappe.db.get_value(
		"Workflow Transition",
		{
			"parent": workflow_name,
			"state": "Draft",
			"action": "Submit",
			"allowed": role,
		},
		"name",
	)

	if not transition_name:
		employee_transition_name = frappe.db.get_value(
			"Workflow Transition",
			{
				"parent": workflow_name,
				"state": "Draft",
				"action": "Submit",
				"allowed": "Employee",
			},
			"name",
		)

		if employee_transition_name:
			frappe.db.set_value(
				"Workflow Transition",
				employee_transition_name,
				"allowed",
				role,
				update_modified=False,
			)
			transition_name = employee_transition_name

	if transition_name:
		frappe.db.set_value(
			"Workflow Transition",
			transition_name,
			"allow_self_approval",
			1,
			update_modified=False,
		)

	admin_transition_name = frappe.db.get_value(
		"Workflow Transition",
		{
			"parent": workflow_name,
			"state": "Draft",
			"action": "Submit",
			"allowed": "Administrator",
		},
		"name",
	)

	if not admin_transition_name:
		frappe.get_doc(
			{
				"doctype": "Workflow Transition",
				"parent": workflow_name,
				"parenttype": "Workflow",
				"parentfield": "transitions",
				"state": "Draft",
				"action": "Submit",
				"next_state": "Submitted",
				"allowed": "Administrator",
				"allow_self_approval": 1,
			}
		).insert(ignore_permissions=True)
	else:
		frappe.db.set_value(
			"Workflow Transition",
			admin_transition_name,
			"allow_self_approval",
			1,
			update_modified=False,
		)

	# Allow Employee - NDMA to edit the Draft state (workflow locks form otherwise).
	# Frappe supports multiple Workflow Document State rows per state, one per allow_edit role.
	draft_status = frappe.db.get_value(
		"Workflow Document State",
		{"parent": workflow_name, "state": "Draft"},
		"doc_status",
	)

	for edit_role in ("Employee - NDMA", "Administrator"):
		existing_draft_state = frappe.db.get_value(
			"Workflow Document State",
			{"parent": workflow_name, "state": "Draft", "allow_edit": edit_role},
			"name",
		)
		if not existing_draft_state:
			frappe.get_doc(
				{
					"doctype": "Workflow Document State",
					"parent": workflow_name,
					"parenttype": "Workflow",
					"parentfield": "states",
					"state": "Draft",
					"doc_status": draft_status or "0",
					"allow_edit": edit_role,
					"update_field": "status",
					"update_value": "Open",
				}
			).insert(ignore_permissions=True)

	# Keep Issue.status aligned with workflow state to avoid submit validation errors.
	state_status_map = {
		"Draft": "Open",
		"Submitted": "Submitted",
		"In Progress": "In Progress",
		"On Hold": "On Hold",
		"Resolved": "Resolved",
		"Rejected": "Rejected",
	}

	for state, status in state_status_map.items():
		frappe.db.sql(
			"""
			UPDATE `tabWorkflow Document State`
			SET update_field='status', update_value=%s
			WHERE parent=%s AND state=%s
			""",
			(status, workflow_name, state),
		)

	# Normalize existing issues where workflow/docstatus no longer matches status value.
	frappe.db.sql(
		"""
		UPDATE `tabIssue`
		SET status='Open'
		WHERE docstatus=0 AND (status IS NULL OR status='')
		"""
	)
	frappe.db.sql(
		"""
		UPDATE `tabIssue`
		SET status='Submitted'
		WHERE docstatus=1 AND workflow_state='Submitted' AND status='Open'
		"""
	)
	frappe.db.sql(
		"""
		UPDATE `tabIssue`
		SET status='In Progress'
		WHERE docstatus=1 AND workflow_state='In Progress' AND status='Open'
		"""
	)
	frappe.db.sql(
		"""
		UPDATE `tabIssue`
		SET status='On Hold'
		WHERE docstatus=1 AND workflow_state='On Hold' AND status='Open'
		"""
	)
	frappe.db.sql(
		"""
		UPDATE `tabIssue`
		SET status='Resolved'
		WHERE docstatus=1 AND workflow_state='Resolved' AND status='Open'
		"""
	)
	frappe.db.sql(
		"""
		UPDATE `tabIssue`
		SET status='Rejected'
		WHERE docstatus=2 AND workflow_state='Rejected' AND status='Open'
		"""
	)

	frappe.clear_cache(doctype=doctype_name)