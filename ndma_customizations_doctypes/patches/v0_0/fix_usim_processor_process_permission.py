import frappe


def execute():
    doctype_name = "USIM"

    # Ensure processor role can edit USIM records in runtime permissions.
    perm_name = frappe.db.get_value("DocPerm", {"parent": doctype_name, "role": "USIM Processor"}, "name")
    if perm_name:
        frappe.db.set_value("DocPerm", perm_name, "read", 1, update_modified=False)
        frappe.db.set_value("DocPerm", perm_name, "write", 1, update_modified=False)

    workflow_name = frappe.db.get_value(
        "Workflow", {"document_type": doctype_name, "is_active": 1}, "name"
    )
    if not workflow_name:
        frappe.clear_cache(doctype=doctype_name)
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

    # Normalize already-saved document statuses.
    frappe.db.sql(
        """
        UPDATE `tabUSIM`
        SET status=%s
        WHERE status=%s
        """,
        (canonical_state, legacy_state),
    )

    # Keep expected workflow role mapping intact.
    state_row = frappe.db.get_value(
        "Workflow Document State",
        {"parent": workflow_name, "state": canonical_state},
        "name",
    )
    if state_row:
        frappe.db.set_value(
            "Workflow Document State",
            state_row,
            "allow_edit",
            "USIM Burn Verifier",
            update_modified=False,
        )

    process_transition = frappe.db.get_value(
        "Workflow Transition",
        {
            "parent": workflow_name,
            "state": "Pending Processing",
            "action": "Process",
        },
        "name",
    )
    if process_transition:
        frappe.db.set_value(
            "Workflow Transition",
            process_transition,
            "allowed",
            "USIM Processor",
            update_modified=False,
        )

    frappe.clear_cache(doctype=doctype_name)
