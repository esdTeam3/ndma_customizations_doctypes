import frappe


def execute():
	html = """
<div style="padding: 2px 0 10px; max-width: 980px;">
	<p style="color: var(--text-muted); margin: 0 0 6px;">Merges My Team &ndash; Approvals + Executive Approvals</p>

	<h4 style="margin: 10px 0 12px; font-size: 13px; letter-spacing: 0.04em; text-transform: uppercase; color: var(--text-muted);">Your Shortcuts</h4>
	<div style="display: grid; grid-template-columns: repeat(2, minmax(240px, 1fr)); gap: 12px; margin-bottom: 20px;">
		<div onclick="frappe.route_options={status:['like','%Pending%']}; frappe.set_route('List', 'Time Off');" style="padding: 14px 16px; border: 1px solid rgba(0,0,0,0.08); border-radius: 12px; background: rgba(255,255,255,0.6); cursor: pointer;">
			<div style="display:flex; justify-content:space-between; align-items:center; gap:10px; margin-bottom:4px;">
				<strong>Pending (my team)</strong>
				<span style="padding: 3px 9px; border-radius: 999px; background: rgba(253, 234, 196, 0.9); color: #b96b00; font-size: 12px; white-space: nowrap;">0</span>
			</div>
			<div style="color: var(--text-muted); font-size: 13px;">Open list →</div>
		</div>

		<div onclick="frappe.route_options={status:'Approved'}; frappe.set_route('List', 'Time Off');" style="padding: 14px 16px; border: 1px solid rgba(0,0,0,0.08); border-radius: 12px; background: rgba(255,255,255,0.6); cursor: pointer;">
			<div style="display:flex; justify-content:space-between; align-items:center; gap:10px; margin-bottom:4px;">
				<strong>Approved this week</strong>
				<span style="padding: 3px 9px; border-radius: 999px; background: rgba(226, 246, 229, 0.95); color: #2a8a44; font-size: 12px; white-space: nowrap;">1</span>
			</div>
			<div style="color: var(--text-muted); font-size: 13px;">Open list →</div>
		</div>

		<div onclick="frappe.route_options={workflow_state:['like','Pending%']}; frappe.set_route('List', 'Vehicle Incident Report');" style="padding: 14px 16px; border: 1px solid rgba(0,0,0,0.08); border-radius: 12px; background: rgba(255,255,255,0.6); cursor: pointer;">
			<div style="display:flex; justify-content:space-between; align-items:center; gap:10px; margin-bottom:4px;">
				<strong>Pending (executive)</strong>
				<span style="padding: 3px 9px; border-radius: 999px; background: rgba(255, 236, 210, 0.9); color: #c27a13; font-size: 12px; white-space: nowrap;">0</span>
			</div>
			<div style="color: var(--text-muted); font-size: 13px;">Open list →</div>
		</div>
	</div>

	<h4 style="margin: 10px 0 12px; font-size: 13px; letter-spacing: 0.04em; text-transform: uppercase; color: var(--text-muted);">Reports &amp; Masters</h4>
	<div style="display: grid; grid-template-columns: repeat(2, minmax(240px, 1fr)); gap: 12px;">
		<div style="padding: 14px 16px; border: 1px solid rgba(0,0,0,0.08); border-radius: 12px; background: rgba(255,255,255,0.6);">
			<strong>My team</strong>
			<div style="margin-top: 10px; color: var(--text-color); opacity: 0.95;">
				<div onclick="frappe.set_route('List', 'Time Off');" style="padding: 4px 0; cursor: pointer;">• Time Off</div>
				<div onclick="frappe.set_route('List', 'Leave Application');" style="padding: 4px 0; cursor: pointer;">• Leave Application</div>
				<div onclick="frappe.set_route('List', 'Leave Resumption');" style="padding: 4px 0; cursor: pointer;">• Leave Resumption</div>
				<div onclick="frappe.set_route('List', 'Job Letter');" style="padding: 4px 0; cursor: pointer;">• Job Letter</div>
				<div onclick="frappe.set_route('List', 'Performance Evaluation');" style="padding: 4px 0; cursor: pointer;">• Performance Evaluation</div>
				<div onclick="frappe.set_route('List', 'Contract Renewal');" style="padding: 4px 0; cursor: pointer;">• Contract Renewal</div>
				<div onclick="frappe.set_route('List', 'Transportation Request');" style="padding: 4px 0; cursor: pointer;">• Transportation Request</div>
				<div onclick="frappe.set_route('List', 'Material Request');" style="padding: 4px 0; cursor: pointer;">• Material Request</div>
			</div>
		</div>

		<div style="padding: 14px 16px; border: 1px solid rgba(0,0,0,0.08); border-radius: 12px; background: rgba(255,255,255,0.6);">
			<strong>Executive tier</strong>
			<div style="margin-top: 10px; color: var(--text-color); opacity: 0.95;">
				<div onclick="frappe.set_route('List', 'Leave Application');" style="padding: 4px 0; cursor: pointer;">• Leave Application</div>
				<div onclick="frappe.set_route('List', 'Material Request');" style="padding: 4px 0; cursor: pointer;">• Material Request</div>
				<div onclick="frappe.set_route('List', 'Payment Entry');" style="padding: 4px 0; cursor: pointer;">• Payment Entry</div>
				<div onclick="frappe.set_route('List', 'Purchase Order');" style="padding: 4px 0; cursor: pointer;">• Purchase Order</div>
				<div onclick="frappe.set_route('List', 'Vehicle Incident Report');" style="padding: 4px 0; cursor: pointer;">• Vehicle Incident Report</div>
				<div onclick="frappe.set_route('List', 'Contract Renewal');" style="padding: 4px 0; cursor: pointer;">• Contract Renewal</div>
			</div>
		</div>
	</div>
</div>
</div>
"""

	if frappe.db.exists("Custom HTML Block", "Approvals Redirect"):
		frappe.db.set_value("Custom HTML Block", "Approvals Redirect", "html", html, update_modified=False)
		frappe.clear_cache(doctype="Workspace")
