import frappe


def execute():
    # Keep My Requests shortcut label/link as Issue.
    shortcut_rows = frappe.get_all(
        "Workspace Shortcut",
        filters={"parent": "My Requests", "link_to": "Issue"},
        fields=["name", "label"],
    )
    for row in shortcut_rows:
        if row.label != "Issue":
            frappe.db.set_value("Workspace Shortcut", row.name, "label", "Issue", update_modified=False)

    # Ensure content block references the Issue shortcut name.
    content = frappe.db.get_value("Workspace", "My Requests", "content") or ""
    if "Facility Request" in content:
        frappe.db.set_value(
            "Workspace",
            "My Requests",
            "content",
            content.replace("Facility Request", "Issue"),
            update_modified=False,
        )

    # Override translation that renames Issue -> Facility Request.
    translation_rows = frappe.get_all(
        "Translation",
        filters={"language": "en", "source_text": "Issue"},
        fields=["name", "translated_text"],
    )
    for row in translation_rows:
        if row.translated_text != "Issue":
            frappe.db.set_value("Translation", row.name, "translated_text", "Issue", update_modified=False)

    frappe.clear_cache(doctype="Workspace")
