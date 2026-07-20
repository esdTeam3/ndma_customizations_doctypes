frappe.pages['approvals-cockpit'].on_page_load = function(wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Approvals',
        single_column: true
    });

    $(page.body).css({
        background: 'linear-gradient(180deg, rgba(255,255,255,0.55) 0%, rgba(255,255,255,0.2) 100%)',
        borderRadius: '14px',
        padding: '8px 0 18px'
    });

    const roles = frappe.user_roles;
    const is_manager = roles.includes('Manager - NDMA') || roles.includes('Department Manager');
    const is_executive = roles.some(r => ['DGM (Admin) - NDMA', 'DGM (Operations) - NDMA',
                                            'General Manager', 'Director - NDMA'].includes(r));

    let html = `
        <div style="padding: 10px 15px 15px; max-width: 900px;">
            <p style="color: var(--text-muted); margin-top:-8px; margin-bottom: 10px;">
                Merges My Team &ndash; Approvals + Executive Approvals
            </p>
            <div style="display:inline-block; margin-bottom:18px; font-size:13px; color: var(--text-muted);">
                <span style="display:inline-block; padding:6px 10px; border:1px solid rgba(153, 125, 51, 0.28); border-radius:999px; background: rgba(255, 247, 230, 0.55);">
                    Restricted to: Manager - NDMA · Department Manager · DGM · GM · Director - NDMA
                </span>
            </div>

            <h4>Your Shortcuts</h4>
            <div id="shortcut-row" style="display:flex; gap:15px; margin-bottom:25px; flex-wrap:wrap;"></div>

            <h4>Reports &amp; Masters</h4>
            <div style="display:flex; gap:20px; flex-wrap:wrap;">
                ${is_manager ? render_card('My team', 'For role: Manager - NDMA / Department Manager', [
                    'Time Off', 'Leave Application', 'Leave Resumption', 'Job Letter',
                    'Performance Evaluation', 'Contract Renewal',
                    'Transportation Request', 'Material Request'
                ]) : ''}
                ${is_executive ? render_card('Executive tier', 'For role: DGM / GM / Director - NDMA', [
                    'Leave Application', 'Material Request', 'Payment Entry',
                    'Purchase Order', 'Vehicle Incident Report', 'Contract Renewal'
                ]) : ''}
            </div>
            ${(!is_manager && !is_executive) ? '<p>You do not have a role assigned to view any approvals here.</p>' : ''}
        </div>
    `;
    $(page.body).html(html);
    load_shortcut_counts(is_manager, is_executive);

    function render_card(title, role_tag, doctypes) {
        const allowed_doctypes = doctypes.filter((dt) => frappe.model.can_read(dt));

        if (!allowed_doctypes.length) {
            return '';
        }

        let links = allowed_doctypes.map(dt =>
            `<div style="padding:5px 0; cursor:pointer; color:var(--text-color); opacity:0.96;"
                  onclick="frappe.set_route('List', '${dt}')">• ${dt}</div>`
        ).join('');
        return `<div style="border:1px solid rgba(0, 0, 0, 0.08); background: rgba(255, 255, 255, 0.68); backdrop-filter: blur(8px); border-radius:12px;
                            padding:15px; flex:1; min-width:260px; box-shadow: 0 4px 18px rgba(0, 0, 0, 0.04);">
                    <strong>${title}</strong><br>
                    <span style="background:#eef0ff; color:#5c5cff; font-size:12px;
                                 padding:2px 8px; border-radius:10px; display:inline-block; margin:6px 0;">
                        ${role_tag}
                    </span>
                    <div style="margin-top:8px;">${links}</div>
                </div>`;
    }

    function load_shortcut_counts(is_manager, is_executive) {
    const shortcuts = [];
    if (is_manager) {
        if (frappe.model.can_read('Time Off')) {
            shortcuts.push({ label: 'Pending (my team)', doctype: 'Time Off', filter: { status: ['like', '%Pending%'] } });
            shortcuts.push({ label: 'Approved this week', doctype: 'Time Off', filter: { status: 'Approved' } });
        }
    }
    if (is_executive) {
        if (frappe.model.can_read('Vehicle Incident Report')) {
            shortcuts.push({ label: 'Pending (executive)', doctype: 'Vehicle Incident Report', filter: { status: ['like', '%Pending%'] } });
        }
    }

    let row = $('#shortcut-row');
    shortcuts.forEach(s => {
        frappe.db.count(s.doctype, { filters: s.filter })
            .then(count => {
                row.append(`
                    <div style="border:1px solid var(--border-color); border-radius:8px;
                                padding:12px 18px; min-width:150px;">
                        <div style="font-size:13px; color:var(--text-muted);">${s.label}</div>
                        <div style="font-size:22px; font-weight:600;">${count}</div>
                    </div>
                `);
            })
            .catch(() => { /* silently skip — role has no permission on this doctype */ });
    });
}}