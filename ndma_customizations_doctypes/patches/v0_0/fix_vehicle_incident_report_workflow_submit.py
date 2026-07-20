import frappe


def execute():
    doctype_name = "Vehicle Incident Report"

    status_field = frappe.db.get_value("DocField", {"parent": doctype_name, "fieldname": "status"}, "name")
    if status_field:
        frappe.db.set_value("DocField", status_field, "allow_on_submit", 1, update_modified=False)

    # Ensure role permissions support workflow actions on submitted records.
    for role in ("Fleet Manager", "DGM (Operations) - NDMA"):
        perm_name = frappe.db.get_value("DocPerm", {"parent": doctype_name, "role": role}, "name")
        if perm_name:
            frappe.db.set_value("DocPerm", perm_name, "submit", 1, update_modified=False)
            frappe.db.set_value("DocPerm", perm_name, "cancel", 1, update_modified=False)

    workflow_name = frappe.db.get_value(
        "Workflow",
        {"document_type": doctype_name, "is_active": 1},
        "name",
    )

    # If no active workflow exists for this doctype, nothing to enforce.
    if not workflow_name:
        return

    legacy_state = "Pending verification"
    canonical_state = "Pending Verification"

    # Normalize legacy workflow state casing to match DocType status options.
    frappe.db.sql(
        """
        UPDATE `tabWorkflow Document State`
        SET state=%s
        WHERE parent=%s AND state=%s
        """,
        (canonical_state, workflow_name, legacy_state),
    )
    frappe.db.sql(
        """
        UPDATE `tabWorkflow Transition`
        SET state=%s
        WHERE parent=%s AND state=%s
        """,
        (canonical_state, workflow_name, legacy_state),
    )
    frappe.db.sql(
        """
        UPDATE `tabWorkflow Transition`
        SET next_state=%s
        WHERE parent=%s AND next_state=%s
        """,
        (canonical_state, workflow_name, legacy_state),
    )

    transition_name = frappe.db.get_value(
        "Workflow Transition",
        {
            "parent": workflow_name,
            "state": "Draft",
            "action": "Submit",
            "allowed": "Employee - NDMA",
        },
        "name",
    )
    if transition_name:
        frappe.db.set_value(
            "Workflow Transition",
            transition_name,
            "allow_self_approval",
            1,
            update_modified=False,
        )

    state_docstatus_map = {
        "Draft": "0",
        "Pending Verification": "1",
        "Pending DGM": "1",
        "Closed": "1",
        "Rejected": "2",
    }

    for state, doc_status in state_docstatus_map.items():
        state_row = frappe.db.get_value(
            "Workflow Document State",
            {"parent": workflow_name, "state": state},
            "name",
        )
        if state_row:
            frappe.db.set_value(
                "Workflow Document State",
                state_row,
                "doc_status",
                doc_status,
                update_modified=False,
            )

    # Normalize legacy values already stored in documents.
    frappe.db.sql(
        """
        UPDATE `tabVehicle Incident Report`
        SET status=%s
        WHERE status=%s
        """,
        (canonical_state, legacy_state),
    )

    frappe.clear_cache(doctype=doctype_name)
