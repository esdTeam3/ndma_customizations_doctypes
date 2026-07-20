frappe.provide("frappe.ui.form");

function patch_issue_quick_entry_redirect() {
	const quick_entry = frappe.ui?.form?.QuickEntryForm;
	if (!quick_entry || quick_entry.__ndma_issue_redirect_patched) {
		return;
	}

	const original_open_form_if_not_list = quick_entry.prototype.open_form_if_not_list;

	quick_entry.prototype.open_form_if_not_list = function () {
		const doc = this.dialog && this.dialog.doc;
		if (doc && doc.doctype === "Issue" && doc.name) {
			return frappe.set_route("Form", doc.doctype, doc.name);
		}

		if (original_open_form_if_not_list) {
			return original_open_form_if_not_list.call(this);
		}
	};

	quick_entry.__ndma_issue_redirect_patched = true;
}

function patch_issue_make_quick_entry() {
	const make_quick_entry = frappe.ui?.form?.make_quick_entry;
	if (!make_quick_entry || make_quick_entry.__ndma_issue_redirect_patched) {
		return;
	}

	frappe.ui.form.make_quick_entry = function (doctype, after_insert, init_callback, doc, force) {
		if (doctype !== "Issue") {
			return make_quick_entry.call(this, doctype, after_insert, init_callback, doc, force);
		}

		const wrapped_after_insert = (created_doc) => {
			if (after_insert) {
				after_insert(created_doc);
			}

			const target = created_doc || doc;
			if (target && target.name) {
				frappe.set_route("Form", "Issue", target.name);
			}
		};

		return make_quick_entry.call(this, doctype, wrapped_after_insert, init_callback, doc, force);
	};

	frappe.ui.form.make_quick_entry.__ndma_issue_redirect_patched = true;
}

patch_issue_quick_entry_redirect();
patch_issue_make_quick_entry();
setTimeout(patch_issue_quick_entry_redirect, 0);
setTimeout(patch_issue_quick_entry_redirect, 300);
setTimeout(patch_issue_make_quick_entry, 0);
setTimeout(patch_issue_make_quick_entry, 300);
