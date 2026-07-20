frappe.ui.form.on("Contract Renewal", {
    refresh(frm) {
        if (!frappe.user.has_role("Employee - NDMA")) {
            return;
        }

        apply_employee_field_access(frm);
        ensure_submit_action(frm);
    },
});

function is_employee_draft(frm) {
    return (
        frm.doc.docstatus === 0 &&
        (frm.is_new() || frm.doc.status === "Draft") &&
        (frm.is_new() || frm.doc.owner === frappe.session.user)
    );
}

function apply_employee_field_access(frm) {
    const editable_fields = [
        "employee",
        "current_contract_end",
        "proposed_term",
        "proposed_start_date",
        "attach_appraisal",
    ];

    const approval_trail_fields = [
        "manager_recommendation",
        "hr_recommendation",
        "gm_endorsement_notes",
        "hr_processing_notes",
        "gm_final_remarks",
    ];

    const can_edit_request_fields = is_employee_draft(frm);

    const apply_access = () => {
        editable_fields.forEach((fieldname) => {
            if (frm.fields_dict[fieldname]) {
                frm.set_df_property(fieldname, "read_only", can_edit_request_fields ? 0 : 1);
                frm.toggle_enable(fieldname, can_edit_request_fields);
            }
        });

        approval_trail_fields.forEach((fieldname) => {
            if (frm.fields_dict[fieldname]) {
                frm.set_df_property(fieldname, "read_only", 1);
                frm.toggle_enable(fieldname, false);
            }
        });
    };

    apply_access();
    setTimeout(apply_access, 200);
    setTimeout(apply_access, 800);

    frm.refresh_fields([...editable_fields, ...approval_trail_fields]);
}

function ensure_submit_action(frm) {
    if (frm.is_new()) {
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
            // Keep native workflow actions when transitions cannot be fetched.
        });
}

function apply_submit_transition(frm) {
    frappe.dom.freeze(__("Submitting Contract Renewal..."));

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
