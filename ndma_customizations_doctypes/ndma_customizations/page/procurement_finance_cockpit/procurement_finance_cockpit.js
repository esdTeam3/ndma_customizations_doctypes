frappe.pages['procurement-finance-cockpit'].on_page_load = function(wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Procurement & Finance',
        single_column: true
    });

    const roles = frappe.user_roles;
    const is_procurement = roles.some(r => [
        'Procurement Manager - NDMA', 'Procurement Officer', 'Procurement Assistant',
        'Professional Assistant - NDMA', 'PR Verifier', 'Purchase User',
        'Purchase Manager', 'Purchase Master Manager', 'Stock Manager', 'Stock User'
    ].includes(r));
    const is_accounts = roles.some(r => [
        'Accounts Manager', 'Accounts User', 'Examination Officer - NDMA'
    ].includes(r));

    let html = `
        <div style="padding: 15px; max-width: 900px;">
            <p style="color: var(--text-muted); margin-top:-8px;">
                Merges Procurement + Accounts into one procure-to-pay view
            </p>
            <div style="background:#fff7e6; border:1px solid #ffe0a3; border-radius:6px;
                        padding:8px 12px; display:inline-block; margin-bottom:20px; font-size:13px;">
                🔒 Restricted to: Procurement roles · Accounts roles
            </div>

            <h4>Your Shortcuts</h4>
            <div id="shortcut-row" style="display:flex; gap:15px; margin-bottom:25px; flex-wrap:wrap;"></div>

            <h4>Reports &amp; Masters</h4>
            <div style="display:flex; gap:20px; flex-wrap:wrap;">
                ${is_procurement ? render_card('Procurement &amp; stores', 'For role: Procurement / Purchase / Stock', [
                    'Material Request', 'Purchase Order', 'Purchase Receipt'
                ]) : ''}
                ${is_accounts ? render_card('Accounts', 'For role: Accounts / Examination Officer', [
                    'Payment Entry', 'Payroll Entry'
                ]) : ''}
            </div>
            ${(!is_procurement && !is_accounts) ? '<p>You do not have a role assigned to view anything here.</p>' : ''}
        </div>
    `;
    $(page.body).html(html);
    load_shortcut_counts(is_procurement, is_accounts);

    function render_card(title, role_tag, doctypes) {
        let links = doctypes.map(dt =>
            `<div style="padding:5px 0; cursor:pointer; color:var(--text-color);"
                  onclick="frappe.set_route('List', '${dt}')">• ${dt}</div>`
        ).join('');
        return `<div style="border:1px solid var(--border-color); border-radius:8px;
                            padding:15px; flex:1; min-width:260px;">
                    <strong>${title}</strong><br>
                    <span style="background:#eef0ff; color:#5c5cff; font-size:12px;
                                 padding:2px 8px; border-radius:10px; display:inline-block; margin:6px 0;">
                        ${role_tag}
                    </span>
                    <div style="margin-top:8px;">${links}</div>
                </div>`;
    }

function load_shortcut_counts(is_procurement, is_accounts) {
    const shortcuts = [];
    if (is_procurement) shortcuts.push({ label: 'Pending Material Requests', doctype: 'Material Request', filter: { status: ['like', '%Pending%'] } });
    if (is_procurement) shortcuts.push({ label: 'Open Purchase Orders', doctype: 'Purchase Order', filter: { status: ['!=', 'Completed'] } });
    if (is_accounts) shortcuts.push({ label: 'Pending Payments', doctype: 'Payment Entry', filter: { docstatus: 0 } });

    let row = $('#shortcut-row');
    row.empty();

    shortcuts.forEach((s, i) => {
        frappe.db.count(s.doctype, { filters: s.filter })
            .then(count => {
                const tile_id = `shortcut-tile-${i}`;
                row.append(`
                    <div class="shortcut-tile" id="${tile_id}"
                         data-doctype="${s.doctype}"
                         style="border:1px solid var(--border-color); border-radius:8px;
                                padding:12px 18px; min-width:150px; cursor:pointer;">
                        <div style="font-size:13px; color:var(--text-muted);">${s.label}</div>
                        <div style="font-size:22px; font-weight:600;">${count}</div>
                    </div>
                `);
                $(`#${tile_id}`).data('filter', s.filter);
            })
            .catch((err) => {
                console.error('Shortcut count failed for', s.doctype, err);
            });
    });
}

// Delegated handler — bound once, works for tiles added now or later
$(document).off('click', '#shortcut-row .shortcut-tile')
   .on('click', '#shortcut-row .shortcut-tile', function() {
            frappe.route_options = $(this).data('filter');
            frappe.set_route('List', $(this).data('doctype'));
        });
};