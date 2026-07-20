frappe.ui.form.on("Time Off", {
    refresh(frm) {
        if (!should_show_confirm(frm)) {
            return;
        }

        frappe
            .xcall("frappe.model.workflow.get_transitions", { doc: frm.doc })
            .then((transitions) => {
                const can_submit = (transitions || []).some((transition) => transition.action === "Submit");
                if (!can_submit) {
                    return;
                }

                const show_submit_button = () => {
                    const button = frm.page.add_inner_button(
                        __("Submit"),
                        () => apply_submit_transition(frm),
                        null,
                        "primary"
                    );
                    if (button) {
                        button.removeClass("btn-default").addClass("btn-primary");
                    }
                };

                show_submit_button();
                setTimeout(show_submit_button, 300);
                setTimeout(show_submit_button, 1200);
            })
            .catch(() => {
                // Keep the default form actions when transitions cannot be fetched.
            });
    },
});

function should_show_confirm(frm) {
    return (
        !frm.is_new() &&
        frm.doc.docstatus === 0 &&
        frm.doc.status === "Draft" &&
        frm.doc.owner === frappe.session.user &&
        (
            frappe.user.has_role("Employee - NDMA") ||
            frappe.user.has_role("Manager - NDMA") ||
            frappe.user.has_role("Manager Tier - NDMA")
        )
    );
}

function apply_submit_transition(frm) {
    frappe.dom.freeze(__("Submitting Time Off..."));

    frappe
        .xcall("frappe.model.workflow.apply_workflow", {
            doc: frm.doc,
            action: "Submit",
        })
        .then((doc) => {
            if (doc) {
                frappe.model.sync(doc);
            }
            frm.reload_doc();
        })
        .finally(() => {
            frappe.dom.unfreeze();
        });
}
