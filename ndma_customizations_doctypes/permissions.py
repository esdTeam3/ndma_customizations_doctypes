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


# --- Department Manager -----------------------------------------------------
# Scopes the doctypes behind the Manager - NDMA workspace's manager-approval
# cards (Leave Application, Leave Adjustment, Time Off Request x2, Leave
# Resumption, Transportation Request) to the manager's own Employee.department.
# Resolved fresh from the Employee record on every call — reassign the
# manager's department and their access changes immediately, with no
# per-department config anywhere.
#
# Each entry's "exempt_roles" are the roles that already have their own,
# broader access logic for that doctype (System Manager always; HR Manager /
# HR User on Leave Application; Leave Approver / Manager - NDMA / Professional
# Assistant - NDMA on Leave Resumption) — Department Manager scoping must not
# additionally narrow them if a user happens to hold both roles.
DEPARTMENT_MANAGER_ROLE = "Department Manager"

# DGM (Admin) - NDMA and DGM (Operations) - NDMA are org-wide Leave Application
# approvers (see the Leave Application Workflow's "Pending DGM Approval" /
# "Submitted" transitions) and are meant to see every department's records
# across the Manager - NDMA workspace, not just their own - exempt everywhere,
# same as System Manager, in case either role is ever also assigned Department
# Manager.
_DGM_ROLES = {"DGM (Admin) - NDMA", "DGM (Operations) - NDMA"}

DEPARTMENT_SCOPED_DOCTYPES = {
	"Leave Application": {
		"field": "department",
		"exempt_roles": {"System Manager", "HR Manager", "HR User"} | _DGM_ROLES,
	},
	"Leave Resumption": {
		"field": "department",
		"exempt_roles": {
			"System Manager",
			"HR Manager",
			"HR User",
			"Leave Approver",
			"Manager - NDMA",
			"Professional Assistant - NDMA",
		}
		| _DGM_ROLES,
	},
	"Employee Time Off Request": {
		"field": "department",
		"exempt_roles": {"System Manager"} | _DGM_ROLES,
	},
	"Transportation Request": {
		"field": "department_tr",
		"exempt_roles": {"System Manager"} | _DGM_ROLES,
	},
}


def _department_manager_scope(doctype, user):
	"""Return (field, manager_department) if Department Manager scoping applies
	to this doctype/user, else None — meaning this hook has no opinion and
	other permission hooks / DocPerms decide as usual."""
	config = DEPARTMENT_SCOPED_DOCTYPES.get(doctype)
	if not config:
		return None

	roles = set(frappe.get_roles(user))
	if DEPARTMENT_MANAGER_ROLE not in roles or (config["exempt_roles"] & roles):
		return None

	return config["field"], frappe.db.get_value("Employee", {"user_id": user}, "department")


def get_permission_query_conditions(user=None, doctype=None):
	"""List-view scoping for Department Manager.

	frappe.model.db_query.DatabaseQuery AND-combines the results of every
	app's permission_query_conditions hook for a doctype, dropping empty
	results — so returning "" here simply adds no restriction, it never
	widens access granted elsewhere.
	"""
	if not user:
		user = frappe.session.user

	scope = _department_manager_scope(doctype, user)
	if not scope:
		return ""

	field, dept = scope
	if not dept:
		return "1=0"
	return f"`tab{doctype}`.{field} = {frappe.db.escape(dept)}"


def department_manager_has_permission(doc, ptype, user, debug=False):
	"""Document-level counterpart of get_permission_query_conditions, so the
	department restriction can't be bypassed by opening a record directly.

	frappe.permissions.has_controller_permissions checks every app's
	has_permission hook for the doctype, most-recently-loaded app first, and
	stops at the first answer that isn't None. Returning None here means this
	hook has no opinion for this doc/user, deferring to other apps' hooks (and
	ultimately to DocPerms) — a controller hook can only deny, never grant.
	"""
	scope = _department_manager_scope(doc.doctype, user)
	if not scope:
		return None

	field, dept = scope
	return bool(dept) and doc.get(field) == dept
