import frappe


WORKSPACE_CONTENT = (
	'[{"id":"pbdk6E-KA_","type":"header","data":{"text":"<span class=\\"h1\\">My Requests</span>","col":12}},'
	'{"id":"myReqDash001","type":"custom_block","data":{"custom_block_name":"My Requests - Custom Styles","col":12}}]'
)


def execute():
	leave_pending = frappe.db.count("Leave Application", {"workflow_state": ["like", "Pending%"]})
	time_off_pending = frappe.db.count("Time Off", {"status": ["in", ["Pending Manager", "Pending HR Approval"]]})
	transport_pending = frappe.db.count("Transportation Request", {"workflow_state": ["like", "Pending%"]})
	issue_open = frappe.db.count(
		"Issue", {"status": ["in", ["Open", "Submitted", "In Progress", "On Hold"]]}
	)

	html = """
<div style="padding: 2px 0 10px; max-width: 980px;">
	<p style="color: var(--text-muted); margin: 0 0 6px;">Self-service · all departments</p>

	<h4 style="margin: 10px 0 12px; font-size: 13px; letter-spacing: 0.04em; text-transform: uppercase; color: var(--text-muted);">Your Shortcuts</h4>
	<div style="display: grid; grid-template-columns: repeat(2, minmax(240px, 1fr)); gap: 12px; margin-bottom: 20px;">
		<div onclick="frappe.route_options={workflow_state:['like','Pending%']}; frappe.set_route('List', 'Leave Application');" style="padding: 14px 16px; border: 1px solid rgba(0,0,0,0.08); border-radius: 12px; background: rgba(255,255,255,0.6); cursor: pointer;">
			<div style="display:flex; justify-content:space-between; align-items:center; gap:10px; margin-bottom:4px;">
				<strong>Leave Application</strong>
				<span style="padding: 3px 9px; border-radius: 999px; background: rgba(253, 234, 196, 0.9); color: #b96b00; font-size: 12px; white-space: nowrap;"><span class="myreq-count" data-myreq="leave">__LEAVE_PENDING__</span> pending</span>
			</div>
			<div style="color: var(--text-muted); font-size: 13px;">Open list →</div>
		</div>

		<div onclick="frappe.route_options={status:['in',['Pending Manager','Pending HR Approval']]}; frappe.set_route('List', 'Time Off');" style="padding: 14px 16px; border: 1px solid rgba(0,0,0,0.08); border-radius: 12px; background: rgba(255,255,255,0.6); cursor: pointer;">
			<div style="display:flex; justify-content:space-between; align-items:center; gap:10px; margin-bottom:4px;">
				<strong>Time Off</strong>
				<span style="padding: 3px 9px; border-radius: 999px; background: rgba(232, 232, 232, 0.95); color: #666; font-size: 12px; white-space: nowrap;"><span class="myreq-count" data-myreq="timeoff">__TIME_OFF_PENDING__</span> pending</span>
			</div>
			<div style="color: var(--text-muted); font-size: 13px;">Open list →</div>
		</div>

		<div onclick="frappe.route_options={workflow_state:['like','Pending%']}; frappe.set_route('List', 'Transportation Request');" style="padding: 14px 16px; border: 1px solid rgba(0,0,0,0.08); border-radius: 12px; background: rgba(255,255,255,0.6); cursor: pointer;">
			<div style="display:flex; justify-content:space-between; align-items:center; gap:10px; margin-bottom:4px;">
				<strong>Transportation Request</strong>
				<span style="padding: 3px 9px; border-radius: 999px; background: rgba(232, 232, 232, 0.95); color: #666; font-size: 12px; white-space: nowrap;"><span class="myreq-count" data-myreq="transport">__TRANSPORT_PENDING__</span> pending</span>
			</div>
			<div style="color: var(--text-muted); font-size: 13px;">Open list →</div>
		</div>

		<div onclick="frappe.route_options={status:['in',['Open','Submitted','In Progress','On Hold']]}; frappe.set_route('List', 'Issue');" style="padding: 14px 16px; border: 1px solid rgba(0,0,0,0.08); border-radius: 12px; background: rgba(255,255,255,0.6); cursor: pointer;">
			<div style="display:flex; justify-content:space-between; align-items:center; gap:10px; margin-bottom:4px;">
				<strong>Issue</strong>
				<span style="padding: 3px 9px; border-radius: 999px; background: rgba(255, 229, 232, 0.95); color: #c7475b; font-size: 12px; white-space: nowrap;"><span class="myreq-count" data-myreq="issue">__ISSUE_OPEN__</span> open</span>
			</div>
			<div style="color: var(--text-muted); font-size: 13px;">Open list →</div>
		</div>
	</div>

	<h4 style="margin: 10px 0 12px; font-size: 13px; letter-spacing: 0.04em; text-transform: uppercase; color: var(--text-muted);">Reports &amp; Masters</h4>
	<div style="display: grid; grid-template-columns: repeat(2, minmax(240px, 1fr)); gap: 12px;">
		<div style="padding: 14px 16px; border: 1px solid rgba(0,0,0,0.08); border-radius: 12px; background: rgba(255,255,255,0.6);">
			<strong>Leave &amp; time</strong>
			<div style="margin-top: 10px; color: var(--text-color); opacity: 0.95;">
				<div onclick="frappe.set_route('List', 'Leave Application');" style="padding: 4px 0; cursor: pointer;">• Leave Application</div>
				<div onclick="frappe.set_route('List', 'Time Off');" style="padding: 4px 0; cursor: pointer;">• Time Off</div>
				<div onclick="frappe.set_route('List', 'Leave Resumption');" style="padding: 4px 0; cursor: pointer;">• Leave Resumption</div>
			</div>
		</div>

		<div style="padding: 14px 16px; border: 1px solid rgba(0,0,0,0.08); border-radius: 12px; background: rgba(255,255,255,0.6);">
			<strong>My employment</strong>
			<div style="margin-top: 10px; color: var(--text-color); opacity: 0.95;">
				<div onclick="frappe.set_route('List', 'Contract Renewal');" style="padding: 4px 0; cursor: pointer;">• Contract Renewal</div>
				<div onclick="frappe.set_route('List', 'Job Letter');" style="padding: 4px 0; cursor: pointer;">• Job Letter</div>
				<div onclick="frappe.set_route('List', 'Employee Profile Update');" style="padding: 4px 0; cursor: pointer;">• Employee Profile Update</div>
				<div onclick="frappe.set_route('List', 'Performance Evaluation');" style="padding: 4px 0; cursor: pointer;">• Performance Evaluation</div>
			</div>
		</div>

		<div style="padding: 14px 16px; border: 1px solid rgba(0,0,0,0.08); border-radius: 12px; background: rgba(255,255,255,0.6); grid-column: 1 / span 1;">
			<strong>Requests</strong>
			<div style="margin-top: 10px; color: var(--text-color); opacity: 0.95;">
				<div onclick="frappe.set_route('List', 'Transportation Request');" style="padding: 4px 0; cursor: pointer;">• Transportation Request</div>
				<div onclick="frappe.set_route('List', 'Training Feedback');" style="padding: 4px 0; cursor: pointer;">• Training Feedback</div>
				<div onclick="frappe.set_route('List', 'Issue');" style="padding: 4px 0; cursor: pointer;">• Issue</div>
			</div>
		</div>
	</div>
</div>
"""
	html = _replace_counts(html, leave_pending, time_off_pending, transport_pending, issue_open)

	script = """
// Custom HTML Block runs inside a shadow DOM; `root_element` (the shadowRoot) is
// provided by frappe.create_shadow_element. Query counts within it, not document.
(function () {
	var root = (typeof root_element !== 'undefined' && root_element) ? root_element : document;

	function set_count(key, value) {
		root.querySelectorAll('.myreq-count[data-myreq="' + key + '"]').forEach(function (el) {
			el.textContent = value;
		});
	}

	if (!root.querySelectorAll('.myreq-count').length) return;

	frappe.db.count('Leave Application', { filters: { workflow_state: ['like', 'Pending%'] } })
		.then(function (v) { set_count('leave', v); });
	frappe.db.count('Time Off', { filters: { status: ['in', ['Pending Manager', 'Pending HR Approval']] } })
		.then(function (v) { set_count('timeoff', v); });
	frappe.db.count('Transportation Request', { filters: { workflow_state: ['like', 'Pending%'] } })
		.then(function (v) { set_count('transport', v); });
	frappe.db.count('Issue', { filters: { status: ['in', ['Open', 'Submitted', 'In Progress', 'On Hold']] } })
		.then(function (v) { set_count('issue', v); });
})();
"""

	if frappe.db.exists("Custom HTML Block", "My Requests - Custom Styles"):
		frappe.db.set_value("Custom HTML Block", "My Requests - Custom Styles", "html", html, update_modified=False)
		frappe.db.set_value("Custom HTML Block", "My Requests - Custom Styles", "script", script, update_modified=False)


	if frappe.db.exists("Workspace", "My Requests"):
		frappe.db.set_value("Workspace", "My Requests", "content", WORKSPACE_CONTENT, update_modified=False)

	frappe.clear_cache(doctype="Workspace")


def _replace_counts(html, leave_pending, time_off_pending, transport_pending, issue_open):
	html = html.replace("__LEAVE_PENDING__", str(leave_pending))
	html = html.replace("__TIME_OFF_PENDING__", str(time_off_pending))
	html = html.replace("__TRANSPORT_PENDING__", str(transport_pending))
	html = html.replace("__ISSUE_OPEN__", str(issue_open))
	return html