import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

# Department Manager scoping (see ndma_customizations_doctypes.permissions) was being
# silently overridden on two fronts:
#
# 1. Leave Application had a duplicate, unrestricted (if_owner=0) Custom DocPerm row
#    for the Employee / Employee - NDMA roles alongside the intended if_owner=1 row.
#    Frappe's role-permission merge lets the unrestricted row win, so plain employees
#    could read every Leave Application regardless of department. We only remove the
#    unrestricted duplicate, and only when the if_owner=1 row it duplicates is still
#    present — never leaving a role with no read grant at all.
#
# 2. ERPNext auto-creates an "Employee = self, apply_to_all_doctypes" User Permission
#    the first time an Employee's user_id is linked. That restriction stacks (AND) on
#    top of our department-scoped list/permission conditions, collapsing a manager's
#    visible set down to only their own personally-filed records. Marking the
#    Employee-link field on each department-scoped doctype as ignore_user_permissions
#    makes our own permissions.py hooks the sole authority there, same as
#    Transportation Request already is by having no Employee-link field at all.

REDUNDANT_DOCPERM_ROLES = ("Employee", "Employee - NDMA")

IGNORE_USER_PERMISSIONS_FIELDS = (
	("Leave Application", "employee"),
	("Leave Resumption", "employee_id"),
	("Employee Time Off Request", "employee"),
)


def execute():
	remove_redundant_leave_application_docperms()
	apply_ignore_user_permissions()


def remove_redundant_leave_application_docperms():
	doctype = "Leave Application"

	for role in REDUNDANT_DOCPERM_ROLES:
		owner_restricted_exists = frappe.db.exists(
			"Custom DocPerm", {"parent": doctype, "role": role, "if_owner": 1}
		)
		if not owner_restricted_exists:
			frappe.logger().warning(
				f"[fix_department_manager_visibility] Skipping {doctype}/{role}: "
				"no if_owner=1 DocPerm row found to fall back to, leaving as-is."
			)
			continue

		unrestricted_rows = frappe.get_all(
			"Custom DocPerm",
			filters={"parent": doctype, "role": role, "if_owner": 0},
			pluck="name",
		)
		for row_name in unrestricted_rows:
			frappe.delete_doc("Custom DocPerm", row_name, ignore_permissions=True)

	frappe.clear_cache(doctype=doctype)


def apply_ignore_user_permissions():
	for doctype, fieldname in IGNORE_USER_PERMISSIONS_FIELDS:
		meta = frappe.get_meta(doctype)
		field = meta.get_field(fieldname)
		if not field or field.fieldtype != "Link" or field.options != "Employee":
			frappe.logger().warning(
				f"[fix_department_manager_visibility] Skipping {doctype}.{fieldname}: "
				"field not found or not a Link to Employee as expected."
			)
			continue

		# make_property_setter deletes any existing Property Setter for this
		# doctype/field/property before inserting, so this is safe to re-run and
		# self-corrects a Property Setter left with the wrong value.
		make_property_setter(doctype, fieldname, "ignore_user_permissions", 1, "Check")
		frappe.clear_cache(doctype=doctype)
