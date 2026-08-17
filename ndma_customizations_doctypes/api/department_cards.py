import frappe
from frappe import _

from ndma_customizations_doctypes.permissions import (
	_DGM_ROLES,
	DEPARTMENT_MANAGER_ROLE,
	DEPARTMENT_SCOPED_DOCTYPES,
)

# permissions.py's exempt_roles (HR Manager, Manager - NDMA, Leave Approver, ...)
# describe who should NOT be data-restricted to their own department - that's a
# backend access decision this module doesn't touch. This picker is stricter on
# purpose: anyone with Department Manager, other than a genuinely unrestricted
# role, is offered only their own department card here, even if an exempt role
# would let them read every department's records once they reach the list view.
# The list view's actual permissions are unchanged either way - selecting a
# department here only sets a default filter, not a restriction.
UNRESTRICTED_ROLES = {"System Manager"} | _DGM_ROLES


@frappe.whitelist()
def get_departments_for_card(number_card):
	"""Departments to offer as cards before routing a Manager - NDMA number
	card to its filtered list."""
	card = frappe.get_cached_doc("Number Card", number_card)
	config = DEPARTMENT_SCOPED_DOCTYPES.get(card.document_type)
	if not config:
		frappe.throw(_("No department field configured for {0}").format(card.document_type))

	field = config["field"]
	user = frappe.session.user
	roles = set(frappe.get_roles(user))

	if DEPARTMENT_MANAGER_ROLE in roles and not (UNRESTRICTED_ROLES & roles):
		department = frappe.db.get_value("Employee", {"user_id": user}, "department")
		if not department:
			return {"department_field": field, "departments": [], "allow_all": False}

		department_name = frappe.db.get_value("Department", department, "department_name") or department
		return {
			"department_field": field,
			"departments": [{"name": department, "department_name": department_name}],
			"allow_all": False,
		}

	# Admin/unrestricted user - offer every active, selectable department, plus
	# the option to skip the department filter entirely. Runs regardless of the
	# caller's own Department read permission, same as permissions.py already
	# resolves Employee.department directly.
	departments = frappe.get_all(
		"Department",
		filters={"disabled": 0, "is_group": 0},
		fields=["name", "department_name"],
		order_by="department_name",
		ignore_permissions=True,
	)
	return {"department_field": field, "departments": departments, "allow_all": True}
