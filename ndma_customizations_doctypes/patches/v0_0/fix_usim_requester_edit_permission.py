import frappe


def execute():
    workflow_name = frappe.db.get_value("Workflow", {"document_type": "USIM", "is_active": 1}, "name")
    if workflow_name:
        submit_transition = frappe.db.get_value(
            "Workflow Transition",
            {
                "parent": workflow_name,
                "state": "Draft",
                "action": "Submit",
                "allowed": "USIM Requester",
            },
            "name",
        )
        if submit_transition:
            frappe.db.set_value(
                "Workflow Transition",
                submit_transition,
                "allow_self_approval",
                1,
                update_modified=False,
            )

    perm_name = frappe.db.get_value(
        "DocPerm",
        {"parent": "USIM", "role": "USIM Requester"},
        "name",
    )
    if not perm_name:
        return

    frappe.db.set_value("DocPerm", perm_name, "write", 1, update_modified=False)
    frappe.db.set_value("DocPerm", perm_name, "submit", 1, update_modified=False)
    frappe.clear_cache(doctype="USIM")
