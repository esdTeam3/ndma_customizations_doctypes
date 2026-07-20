import frappe


def execute():
    workflow_name = frappe.db.get_value("Workflow", {"document_type": "USIM", "is_active": 1}, "name")
    if not workflow_name:
        return

    transition_name = frappe.db.get_value(
        "Workflow Transition",
        {
            "parent": workflow_name,
            "state": "Draft",
            "action": "Submit",
            "allowed": "USIM Requester",
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

    frappe.clear_cache(doctype="USIM")
