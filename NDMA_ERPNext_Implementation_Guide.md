# NDMA Portal — ERPNext Implementation Guide
### Consolidating 10 workspaces into 5, with 5 new custom DocTypes
**Target stack:** ERPNext 15.6.0 · Frappe 15.110.0 · HRMS 15.5.0

---

## 0. Confirmed decisions and remaining defaults

| # | Item | Status |
|---|------|--------|
| 1 | Time Off approval chain | **Confirmed:** Employee → Manager - NDMA → HR (final) |
| 2 | Contract Renewal chain | **Confirmed:** Employee → Manager → HR → GM (endorsement) → HR (processing) → GM (final approval) — a two-pass loop through HR and GM, modeled as 4 distinct approval states in §3 |
| 3 | Job Letter chain | **Confirmed:** Employee → Manager → HR (final, issues letter) |
| 4 | Vehicle Incident Report chain | **Confirmed as originally proposed:** Reporter → Fleet Manager verifies → DGM (Operations) - NDMA signs off |
| 5 | USIM chain | **Confirmed as originally proposed:** Requester → USIM Processor → USIM Burn Verifier → USIM Manager final |
| 6 | Procurement & Finance workspace | **Confirmed: strict split**, same treatment as Approvals — a custom Desk Page, not a shared Workspace. See §5.2. |
| 7 | Old workspaces after migration | **Confirmed: keep, but hidden** as a fallback rather than deleted. See §4.4. |
| 8 | Naming series | Confirmed by you: `HR-TOF-`, `HR-CTR-`, `HR-JBL-`; extended the same pattern to `VIR-` and `USIM-` |

Everything below has been updated to match. The DocType JSON files in the zip now reflect the Contract Renewal and Job Letter chains above.

---

## 1. Create the custom app

All new DocTypes, workflows, and the custom Approvals page live in one bench app so they survive ERPNext/HRMS upgrades cleanly.

```bash
# on the bench server, as the frappe user
cd ~/frappe-bench
bench new-app ndma_customizations
# prompts: App Title "NDMA Customizations", keep short name ndma_customizations

bench --site your-site.local install-app ndma_customizations
```

### 1.1 Register the Module Def

Your `Module_Def.csv` export has no NDMA module yet — `bench new-app` creates one automatically named after the app, but confirm it matches:

```bash
bench --site your-site.local console
```
```python
import frappe
if not frappe.db.exists("Module Def", "NDMA Customizations"):
    frappe.get_doc({
        "doctype": "Module Def",
        "module_name": "NDMA Customizations",
        "app_name": "ndma_customizations",
        "custom": 1
    }).insert()
frappe.db.commit()
```

---

## 2. Install the 5 new DocTypes

I've generated importable DocType JSON files, structured as a real Frappe app folder:

```
ndma_customizations/
└── ndma_customizations/
    └── doctype/
        ├── time_off/time_off.json
        ├── contract_renewal/contract_renewal.json
        ├── job_letter/job_letter.json
        ├── vehicle_incident_report/vehicle_incident_report.json
        └── usim/usim.json
```

### 2.1 Copy the files in

Copy each `doctype/<name>/` folder (json + blank `__init__.py`, both included) into:
```
~/frappe-bench/apps/ndma_customizations/ndma_customizations/doctype/
```

### 2.2 Generate the missing Python controller files

Frappe's JSON defines schema; each DocType still needs a `.py` controller and a JS file. Fastest path — let Frappe scaffold them, then the importer overwrites only the JSON:

```bash
cd ~/frappe-bench
bench --site your-site.local console
```
```python
import frappe
for dt in ["Time Off", "Contract Renewal", "Job Letter",
           "Vehicle Incident Report", "USIM"]:
    if not frappe.db.exists("DocType", dt):
        frappe.get_doc({"doctype": "DocType", "name": dt,
                         "module": "NDMA Customizations", "custom": 0}).insert()
```
Then run `bench migrate` — Frappe will notice the JSON already on disk (from the copy in 2.1) differs and will scaffold the matching `.py`/`.js` stub files for you the first time you open each DocType's "Customize Form" or edit it in the DocType list. In practice the cleaner sequence is:

```bash
bench --site your-site.local migrate
bench build
bench restart
```

Then open each new DocType in the desk (**Setup > DocType**) once, just to confirm the fields render as expected before wiring permissions.

### 2.3 Field notes / things to double-check per DocType

- **Time Off / Contract Renewal**: `manager_approver` / `final_approver` are read-only Link fields I've left for a server script or Workflow action to populate (from `employee.reports_to`) — they won't auto-fill until you add that hook.
- **Vehicle Incident Report**: I used a free-text `vehicle` Data field rather than linking to ERPNext's stock `Vehicle` DocType (Assets module) — if your fleet is already tracked there, switch this to `Link → Vehicle` for real reporting.
- **USIM**: no existing "SIM stock" concept in ERPNext, so this is a fully standalone tracking DocType, not tied to Stock/Serial No. If you want SIMs to actually decrement inventory, that's a bigger Stock Entry integration, out of scope here.

---

## 3. Build the Workflows (state machine per DocType)

Each new DocType needs a **Workflow** record (Setup > Workflow) so the `status` field transitions are actually enforced by role, not just cosmetic. Example for Time Off:

**Setup > Workflow > New**
- Document Type: `Time Off`
- Workflow State Field: `status`
- Is Active: ✓

| State | Doc Status | Allow Edit |
|---|---|---|
| Draft | Draft | Employee - NDMA |
| Pending Manager | Draft | Manager - NDMA |
| Pending HR Approval | Draft | HR User |
| Approved | Draft | HR Manager |
| Rejected | Cancelled | HR Manager |

**Transitions:**

| From | To | Allowed Role | Action label |
|---|---|---|---|
| Draft | Pending Manager | Employee - NDMA | Submit |
| Pending Manager | Pending HR Approval | Manager - NDMA | Approve |
| Pending Manager | Rejected | Manager - NDMA | Reject |
| Pending HR Approval | Approved | HR User | Approve |
| Pending HR Approval | Rejected | HR User | Reject |

Repeat the same pattern for the other 4 DocTypes using the confirmed chains in §0. Two need extra care:

### 3.1 Contract Renewal — the two-pass HR/GM loop

Because the chain is Employee → Manager → HR → GM → HR → GM (final), the same role (HR, then GM) appears twice. Frappe Workflow states must be unique per DocType, so this needs **4 distinct states** rather than reusing "Pending HR" / "Pending GM" twice — already reflected in the DocType's `status` field options:

| State | Allow Edit | Purpose |
|---|---|---|
| Draft | Employee - NDMA | Employee submits |
| Pending Manager | Manager - NDMA | Manager recommends |
| Pending HR Review | HR User | HR reviews, first pass |
| Pending GM Endorsement | General Manager | GM endorses in principle |
| Pending HR Processing | HR User | HR drafts the actual renewal contract |
| Pending GM Final Approval | General Manager | GM signs off, final |
| Approved | — | Terminal state |
| Rejected | — | Terminal state, allowed from any pending state |

Transitions go strictly in that order — GM cannot jump from "Endorsement" straight to "Approved"; it must pass back through "Pending HR Processing" first, matching the confirmed loop.

### 3.2 Job Letter — now a 2-hop chain

Updated to Employee → Manager → HR (final):

| From | To | Allowed Role |
|---|---|---|
| Draft | Pending Manager | Employee - NDMA |
| Pending Manager | Pending HR | Manager - NDMA |
| Pending HR | Completed | HR User |
| any pending state | Rejected | Manager - NDMA / HR User |

> Once these are built once in the UI, export them with `bench export-fixtures --app ndma_customizations` so they live in the app's `fixtures/workflow.json` and travel with future deployments instead of being site-only.

---

## 4. Consolidate the Workspaces (10 → 5)

Your `Workspace.csv` confirms only 5 records are NDMA-custom today (`Manager - NDMA`, `Management`, `HR User Workspace`, `HR Manager Workspace`, `Receptionist`); everything else is stock. The mapping:

| Mockup workspace | Built from | Method |
|---|---|---|
| **My Requests** | New | Build fresh — no existing self-service workspace exists |
| **Approvals** | `Manager - NDMA` + `Management` | Merge, custom Desk Page for role-split (see §5) |
| **HR Operations** | `HR User Workspace` + `HR Manager Workspace` | Merge into one, shared shortcuts |
| **Procurement & Finance** | New | Build as a custom Desk Page (strict split, confirmed) — see §5.2, not a stock Workspace |
| **Facilities & Operations** | `Receptionist` + new | Merge Receptionist in, add Transportation/USIM/FASD content |

### 4.1 General workspace build steps (repeat per workspace)

1. **Desk > Workspace > New** (or edit the existing one to rename/restructure).
2. Set **Title**, **Icon**, **Module** = `NDMA Customizations` for the 3 net-new ones; keep original module for merged ones if you want to preserve existing permission inheritance.
3. **Public** = ✓ so it shows for all users, then use the **Roles** table (bottom of Workspace form) to restrict visibility — this maps directly to your mockup's "Restricted to:" pill.
4. Add **Shortcuts** block → one per mockup shortcut tile (Leave Application, Time Off, etc.), set **Count Filter** so the number badge matches (e.g. `status = Pending HR Approval`).
5. Add **Card/Links** blocks → one card per mockup "Reports & masters" section, with Link rows for each DocType.
6. For merged workspaces, **delete the old Workspace record only after** the new one is live and tested — don't delete `HR User Workspace` / `HR Manager Workspace` until HR Operations is confirmed working, since deleting a Workspace immediately removes it from every user's sidebar.

### 4.2 Role restriction — matches your mockup's role-note pill

Workspace-level role restriction is native in Frappe 15 (Roles table on the Workspace form) — no customization needed for:
- **My Requests** → `Employee - NDMA`
- **HR Operations** → `HR User`, `HR Manager`
- **Facilities & Operations** → Fleet Manager, Facilities Manager/Supervisor, Receptionist, USIM roles

### 4.3 Card-level `for-role` sub-tags

Stock Workspaces do **not** support per-card role filtering — only whole-workspace role restriction. Two workspaces in your mockup need it, and **both now get the strict custom-page treatment**:
- **Approvals** (My team vs Executive tier) — see §5.1
- **Procurement & Finance** (Procurement vs Accounts cards) — confirmed strict split — see §5.2

### 4.4 Keeping the old workspaces — hidden, not deleted

Confirmed: `HR User Workspace`, `HR Manager Workspace`, `Manager - NDMA`, `Management`, and `Receptionist` should be **kept as a fallback**, not deleted, once the 5 new consolidated workspaces are live.

Frappe Workspaces don't have a dedicated "hidden but preserved" flag, so the practical approach is:

1. Open each old Workspace record.
2. Uncheck **Public**.
3. Leave the **Roles**/**For User** table empty (don't assign it to anyone).

This removes it from every user's sidebar immediately, while the record — and all its Shortcuts/Links/Cards configuration — stays intact in the database. If something breaks in one of the new consolidated workspaces, you (as System Manager) can still open the old one directly via its URL (`/app/hr-user-workspace` etc.) or re-check **Public** to instantly restore it for everyone as a rollback.

Don't run any `bench` delete or fixture-removal commands against these 5 records as part of this migration.

---

## 5. Custom Desk Pages for strict role-split (Approvals + Procurement & Finance)

### 5.1 Approvals

Because Approvals mixes `Manager - NDMA / Department Manager` (see "My team" card) with `DGM / GM / Director - NDMA` (see "Executive tier" card) in one workspace, this needs a thin custom Page rather than a stock Workspace.

```bash
cd ~/frappe-bench/apps/ndma_customizations
bench make-page approvals_cockpit
```

`ndma_customizations/ndma_customizations/page/approvals_cockpit/approvals_cockpit.js`:

```javascript
frappe.pages['approvals-cockpit'].on_page_load = function(wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Approvals',
        single_column: true
    });

    const roles = frappe.user_roles;
    const is_manager = roles.includes('Manager - NDMA') || roles.includes('Department Manager');
    const is_executive = roles.some(r => ['DGM (Admin) - NDMA', 'DGM (Operations) - NDMA',
                                            'General Manager', 'Director - NDMA'].includes(r));

    let html = '<div class="approvals-cockpit">';

    if (is_manager) {
        html += render_card('My team', [
            'Time Off', 'Leave Application', 'Leave Resumption',
            'Performance Evaluation', 'Contract Renewal',
            'Transportation Request', 'Material Request'
        ]);
    }
    if (is_executive) {
        html += render_card('Executive tier', [
            'Leave Application', 'Material Request', 'Payment Entry',
            'Purchase Order', 'Vehicle Incident Report'
        ]);
    }
    html += '</div>';
    $(page.body).html(html);

    function render_card(title, doctypes) {
        let links = doctypes.map(dt =>
            `<div class="doc-link" onclick="frappe.set_route('List', '${dt}')">${dt}</div>`
        ).join('');
        return `<div class="link-card"><h3>${title}</h3>${links}</div>`;
    }
};
```

### 5.2 Procurement & Finance (confirmed: strict split)

Same pattern as Approvals — procurement staff should never see Accounts cards, and vice versa, even though both sit under one workspace entry in the sidebar.

```bash
cd ~/frappe-bench/apps/ndma_customizations
bench make-page procurement_finance_cockpit
```

`ndma_customizations/ndma_customizations/page/procurement_finance_cockpit/procurement_finance_cockpit.js`:

```javascript
frappe.pages['procurement-finance-cockpit'].on_page_load = function(wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Procurement & Finance',
        single_column: true
    });

    const roles = frappe.user_roles;
    const is_procurement = roles.some(r => ['Procurement Manager - NDMA', 'Procurement Officer',
                                              'Professional Assistant - NDMA', 'Purchase User',
                                              'PR Verifier'].includes(r));
    const is_accounts = roles.some(r => ['Accounts Manager', 'Accounts User',
                                           'Examination Officer - NDMA'].includes(r));

    let html = '<div class="procurement-finance-cockpit">';

    if (is_procurement) {
        html += render_card('Procurement & stores', [
            'Material Request', 'Purchase Order', 'Purchase Receipt'
        ]);
    }
    if (is_accounts) {
        html += render_card('Accounts', [
            'Payment Entry', 'Payroll Entry'
        ]);
    }
    html += '</div>';
    $(page.body).html(html);

    function render_card(title, doctypes) {
        let links = doctypes.map(dt =>
            `<div class="doc-link" onclick="frappe.set_route('List', '${dt}')">${dt}</div>`
        ).join('');
        return `<div class="link-card"><h3>${title}</h3>${links}</div>`;
    }
};
```

A user holding both a procurement role and an accounts role (e.g. a cross-functional System Manager) will see both cards — that's expected and matches how the Approvals page handles overlap.

### 5.3 Wiring both pages into the sidebar

Add each page to the left nav by giving it a stub Workspace record that links to it via a Shortcut of type "URL" (e.g. pointing to `/app/approvals-cockpit` and `/app/procurement-finance-cockpit`), so both still show in the sidebar like the other 3 native workspaces.

---

## 6. Role permission matrix — build order

Use **Setup > Role Permissions Manager** (or `bench --site your-site.local console` with `frappe.permissions.add_permission`) to wire each new DocType to its roles. The permission blocks are already included in each JSON file's `"permissions"` array, so `bench migrate` will apply them automatically once the DocTypes are installed — you shouldn't need to hand-build these in the UI, just verify them.

Double-check against your `Role.csv`:
- `Fleet Manager` ✓ exists
- `USIM Requester`, `USIM Processor`, `USIM Burn Verifier`, `USIM Manager` ✓ all exist
- `DGM (Operations) - NDMA` ✓ exists — used for Vehicle Incident Report final sign-off
- `General Manager` ✓ exists — used for Contract Renewal's two GM approval stages (endorsement + final)
- `Facilities Manager`, `Facility User`, `FASD Manager`, `FASD Supervisor` ✓ all exist — Vehicle Incident Report and Issue permissions can map straight to these, no gap here.

---

## 7. Deployment sequence

```bash
# 1. Pull the new app code onto the bench (copy files or git push to the app repo)
cd ~/frappe-bench

# 2. Install/refresh the app on the target site
bench --site your-site.local install-app ndma_customizations   # first time only
bench --site your-site.local migrate

# 3. Build workspace/workflow fixtures once configured in UI (see §3, §4)
bench --site your-site.local export-fixtures --app ndma_customizations

# 4. Clear cache and rebuild assets
bench --site your-site.local clear-cache
bench build
bench restart
```

---

## 8. Testing checklist before rollout

- [ ] Create one test record per new DocType as a low-privilege test user (Employee - NDMA) — confirm they can create but not approve
- [ ] Step each workflow through every state as the correct role at each hop; confirm a Manager cannot skip straight to Approved
- [ ] For Contract Renewal specifically: confirm GM cannot jump from "Pending GM Endorsement" straight to "Approved" — it must route back through "Pending HR Processing" first
- [ ] Log in as a user with only `Employee - NDMA` → confirm only **My Requests** shows in the sidebar
- [ ] Log in as a user with `Manager - NDMA` only → confirm **Approvals** shows "My team" card but not "Executive tier"
- [ ] Log in as a user with `DGM (Operations) - NDMA` → confirm "Executive tier" shows, "My team" does not (unless they also hold Manager - NDMA)
- [ ] Log in as a Procurement-only role → confirm **Procurement & Finance** shows only the "Procurement & stores" card, not "Accounts"
- [ ] Log in as an Accounts-only role → confirm the reverse
- [ ] Confirm naming series produce `HR-TOF-2026-00001` style IDs matching the mockup, not `HR-TOF-25-00001` or similar
- [ ] Confirm old workspaces (`HR User Workspace`, `HR Manager Workspace`, `Manager - NDMA`, `Management`, `Receptionist`) are hidden (Public unchecked, no assigned users) rather than deleted, and that a System Manager can still reach them directly if needed
- [ ] Re-run the Role Permissions Manager report for each new DocType to confirm no role is missing read access it needs

---

## 9. Anything still worth double-checking

Everything from the original open items list is now confirmed. The only thing I'd still flag for your review once the build is live:

- Whether a **Director - NDMA** or **DGM (Admin) - NDMA** needs any visibility into Contract Renewal (currently it's Manager → HR → General Manager only, with no Director/DGM Admin step) — worth a quick sanity check against how it's handled today outside the system, in case there's an informal sign-off that should be captured.
