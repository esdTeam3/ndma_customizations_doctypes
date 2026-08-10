import frappe

RESTRICTED_WORKSPACE = "Tax & Benefits"
RESTRICTED_ROLE = "Payroll User - NDMA"
ALLOWED_ROLES = {"HR Manager", "HR User", "System Manager"}


def restrict_tax_and_benefits_workspace(doc, ptype, user, debug=False):
	if doc.name != RESTRICTED_WORKSPACE:
		return None

	roles = set(frappe.get_roles(user))
	if RESTRICTED_ROLE in roles and not (roles & ALLOWED_ROLES):
		return False

	return None
