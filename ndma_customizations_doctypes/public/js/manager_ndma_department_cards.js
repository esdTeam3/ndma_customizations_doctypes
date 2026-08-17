frappe.provide("frappe.widget");

const NDMA_DEPARTMENT_CARDS = new Set([
	"Leave Application – Submitted",
	"Leave Adjustment – Manager Approval",
	"Time Off Request – Manager Approval",
	"Time Off Request – Return Endorsement",
	"Leave Resumption – Submitted",
	"Transportation Request – Manager Approval",
]);

function patch_number_card_widget_department_picker() {
	const NumberCardWidget =
		frappe.widget.widget_factory && frappe.widget.widget_factory.number_card;
	if (!NumberCardWidget || NumberCardWidget.prototype.__ndma_department_picker_patched) {
		return;
	}

	const original_set_route = NumberCardWidget.prototype.set_route;

	NumberCardWidget.prototype.set_route = function () {
		const card_name = this.card_doc && this.card_doc.name;
		if (this.card_doc.type !== "Document Type" || !NDMA_DEPARTMENT_CARDS.has(card_name)) {
			return original_set_route.call(this);
		}

		show_department_picker(this);
	};

	NumberCardWidget.prototype.__ndma_department_picker_patched = true;
}

function show_department_picker(widget) {
	frappe
		.call({
			method: "ndma_customizations_doctypes.api.department_cards.get_departments_for_card",
			args: { number_card: widget.card_doc.name },
			freeze: true,
		})
		.then(({ message }) => {
			if (!message) return;

			const { department_field, departments, allow_all } = message;

			if (!departments.length) {
				frappe.msgprint(__("No department is assigned to you. Please contact HR."));
				return;
			}

			if (departments.length === 1 && !allow_all) {
				route_to_department(widget, department_field, departments[0].name);
				return;
			}

			render_department_dialog(widget, department_field, departments, allow_all);
		});
}

function render_department_dialog(widget, department_field, departments, allow_all) {
	const dialog = new frappe.ui.Dialog({
		title: __("Select Department"),
		fields: [{ fieldtype: "HTML", fieldname: "department_cards" }],
	});

	const all_card_html = allow_all
		? `<div class="ndma-department-card" data-all="1"
				style="cursor:pointer;padding:12px 16px;border:1px solid var(--border-color);
				border-radius:var(--border-radius-md);font-weight:bold;">
				${__("All Departments")}
			</div>`
		: "";

	const cards_html = departments
		.map(
			(dept) => `
			<div class="ndma-department-card" data-department="${frappe.utils.escape_html(dept.name)}"
				style="cursor:pointer;padding:12px 16px;border:1px solid var(--border-color);
				border-radius:var(--border-radius-md);">
				${frappe.utils.escape_html(dept.department_name || dept.name)}
			</div>`
		)
		.join("");

	dialog.fields_dict.department_cards.$wrapper.html(
		`<div class="ndma-department-card-list"
			style="display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px;">
			${all_card_html}${cards_html}
		</div>`
	);

	dialog.$wrapper.find(".ndma-department-card").on("click", (event) => {
		const department = event.currentTarget.dataset.all
			? null
			: event.currentTarget.dataset.department;
		dialog.hide();
		route_to_department(widget, department_field, department);
	});

	dialog.show();
}

function route_to_department(widget, department_field, department) {
	const filters = widget.get_filters();
	const route = frappe.utils.generate_route({
		name: widget.card_doc.document_type,
		type: "doctype",
	});

	frappe.route_options = filters.reduce((acc, filter) => {
		return Object.assign(acc, { [`${filter[0]}.${filter[1]}`]: [filter[2], filter[3]] });
	}, {});
	if (department) {
		frappe.route_options[`${widget.card_doc.document_type}.${department_field}`] = [
			"=",
			department,
		];
	}

	frappe.set_route(route);
}

patch_number_card_widget_department_picker();
setTimeout(patch_number_card_widget_department_picker, 0);
setTimeout(patch_number_card_widget_department_picker, 300);
