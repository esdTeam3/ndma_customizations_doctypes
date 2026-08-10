import frappe
from frappe.permissions import add_permission, update_permission_property

ROLE = "Payroll User - NDMA"

# doctype -> is_submittable (controls whether "submit" is granted)
ALLOWED_DOCTYPES = {
	"Salary Slip": True,
	"Payroll Entry": True,
	"Salary Structure": True,
	"Salary Structure Assignment": True,
	"Additional Salary": True,
	"Employee Incentive": True,
	"Retention Bonus": True,
	"Payroll Period": False,
}

# Read-only doctypes: viewable but not editable by this role. Account, Bank Account,
# and Cost Center are required to pick existing values in Payroll Entry's
# Payroll Payable Account / Bank Account / Cost Center fields - without at least
# read here, Payroll Entry can't be created at all (Account and Cost Center are
# mandatory fields on that doctype).
READ_ONLY_DOCTYPES = (
	"Bank",
	"Account",
	"Bank Account",
	"Cost Center",
)

ALLOWED_REPORTS = (
	"NIS",
	"GRA",
	"GRA with refund",
	"Earnings and Deductions",
	"Salary Analysis NDMA",
	"Salary Register",
	"Provident Fund Deductions",
	"Professional Tax Deductions",
	"Income Tax Deductions",
)

# Workspaces that must stay hidden from Payroll User - NDMA in the sidebar/navigation
# tree. Populated with the roles that already have real read access to that
# workspace's own doctypes, so restricting it doesn't change behavior for anyone
# who currently has legitimate access - it only excludes the new role.
RESTRICTED_WORKSPACE_ROLES = {
	"Tax & Benefits": ["Employee", "HR Manager", "HR User", "System Manager"],
}


def execute():
	if not frappe.db.exists("Role", ROLE):
		frappe.get_doc({"doctype": "Role", "role_name": ROLE, "desk_access": 1}).insert(
			ignore_permissions=True
		)

	for doctype, is_submittable in ALLOWED_DOCTYPES.items():
		if not frappe.db.exists("DocType", doctype):
			continue

		add_permission(doctype, ROLE, permlevel=0, ptype="read")

		permission_values = {"read": 1, "write": 1, "create": 1}
		if is_submittable:
			permission_values["submit"] = 1

		for ptype, value in permission_values.items():
			update_permission_property(doctype, ROLE, 0, ptype, value=value, validate=False)

		frappe.clear_cache(doctype=doctype)

	for doctype in READ_ONLY_DOCTYPES:
		if not frappe.db.exists("DocType", doctype):
			continue

		add_permission(doctype, ROLE, permlevel=0, ptype="read")
		update_permission_property(doctype, ROLE, 0, "read", value=1, validate=False)
		frappe.clear_cache(doctype=doctype)

	if frappe.db.exists("Workspace", "Payroll") and not frappe.db.exists(
		"Workspace Link", {"parent": "Payroll", "link_to": "Bank", "link_type": "DocType"}
	):
		payroll_workspace = frappe.get_doc("Workspace", "Payroll")
		payroll_workspace.append(
			"links",
			{
				"label": "Bank",
				"type": "Link",
				"link_type": "DocType",
				"link_to": "Bank",
				"onboard": 0,
			},
		)
		payroll_workspace.save(ignore_permissions=True)

	for report in ALLOWED_REPORTS:
		if not frappe.db.exists("Report", report):
			continue

		report_doc = frappe.get_doc("Report", report)
		if any(r.role == ROLE for r in report_doc.roles):
			continue

		report_doc.append("roles", {"role": ROLE})
		report_doc.save(ignore_permissions=True)

	for workspace, allowed_roles in RESTRICTED_WORKSPACE_ROLES.items():
		if not frappe.db.exists("Workspace", workspace):
			continue

		workspace_doc = frappe.get_doc("Workspace", workspace)
		existing_roles = {r.role for r in workspace_doc.roles}
		missing_roles = [role for role in allowed_roles if role not in existing_roles]
		if not missing_roles:
			continue

		for role in missing_roles:
			workspace_doc.append("roles", {"role": role})
		workspace_doc.save(ignore_permissions=True)

	frappe.clear_cache()
