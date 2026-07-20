# My Requests Workspace Training Guide

## Purpose
This runbook trains users on every item shown in the My Requests workspace, including who logs in next at each workflow stage to complete the full lifecycle.

Workspace sections covered:
- Top shortcut row: Issue, Leave Application, Transportation Request, Time Off
- Reports and Masters:
- Leave and time: Leave Application, Time Off, Leave Resumption
- My Employment: Contract Renewal, Job Letter, Employee Profile Update, Performance Evaluation
- Requests: Transportation Request, Training Feedback

## Training User Matrix
Use these users for role-switching:

| Role | Suggested User |
|---|---|
| Employee - NDMA | test.employee@ndma.gy |
| Manager - NDMA | test.manager@ndma.gy |
| Department Manager | test.deptmanager@ndma.gy |
| HR User | test.hruser@ndma.gy |
| HR Manager | test.hrmanager@ndma.gy |
| General Manager | test.gm@ndma.gy |
| DGM (Operations) - NDMA | test.dgmops@ndma.gy |
| Facilities Manager | Administrator (or impersonate dedicated account) |
| Facility User | Administrator (or impersonate dedicated account) |
| Transportation request Approver | Administrator (or impersonate dedicated account) |
| Transportation Request Admin | Administrator (or impersonate dedicated account) |

## Standard Training Rules
1. Create a fresh document for each scenario.
2. Save before checking workflow actions.
3. After each action, refresh list/workspace and verify state changed.
4. Switch user immediately when next role owns the state.
5. Follow happy-path steps first; then optionally test reject/rollback branch.

---

## 1) Issue (Top Shortcut)
Lifecycle: Draft -> Submitted -> In Progress -> Resolved

Steps:
1. Login as test.employee@ndma.gy.
2. Open Issue and create a new record.
3. Click Submit (state becomes Submitted).
4. Switch to Facilities Manager user (Administrator if needed).
5. Click Send to Facility User (state becomes In Progress).
6. Switch to Facility User (Administrator if needed).
7. Click Resolved (state becomes Resolved).

Optional branch:
- In Progress -> On Hold -> In Progress.
- Submitted -> Reject.

---

## 2) Leave Application (Top Shortcut and Leave and time)
Primary lifecycle: Draft -> Submitted -> Pending HR Approval -> Pending HR Manager Approval -> Approved

Steps:
1. Login as test.employee@ndma.gy.
2. Create Leave Application and Submit.
3. Switch to test.manager@ndma.gy.
4. Click Verify (moves to Pending HR Approval).
5. Switch to test.hruser@ndma.gy.
6. Click Accept (moves to Pending HR Manager Approval).
7. Switch to test.hrmanager@ndma.gy.
8. Click Approve (moves to Approved).

Adjustment lifecycle (from Approved):
1. Switch back to employee and click Adjust Leave.
2. From Draft Adjustment click Submit Adjustment.
3. Manager accepts adjustment.
4. HR Manager approves adjustment.

---

## 3) Transportation Request (Top Shortcut and Requests)
Lifecycle: Draft -> Approval pending by Manager -> Approved -> Vehicle Assigned

Steps:
1. Login as test.employee@ndma.gy.
2. Create Transportation Request and Submit.
3. Switch to Transportation request Approver (Administrator if needed).
4. Click Approve (moves to Approved).
5. Switch to Transportation Request Admin (Administrator if needed).
6. Click Approve (moves to Vehicle Assigned).

Optional branches:
- Approver can Reject or Rollback for redraft.
- Employee can re-submit from Re-draft.

---

## 4) Time Off (Top Shortcut and Leave and time)
Lifecycle: Draft -> Pending Manager -> Pending HR Approval -> Approved

Steps:
1. Login as test.employee@ndma.gy.
2. Create Time Off and Submit.
3. Switch to test.manager@ndma.gy (or test.deptmanager@ndma.gy).
4. Click Approve (moves to Pending HR Approval).
5. Switch to test.hruser@ndma.gy (or test.hrmanager@ndma.gy).
6. Click Approve (moves to Approved).

Optional branch:
- Manager or HR can Reject at their stage.

---

## 5) Leave Resumption (Leave and time)
Lifecycle: Draft -> Submitted -> Endorsed -> Accepted

Steps:
1. Login as test.employee@ndma.gy.
2. Create Leave Resumption and Submit.
3. Switch to test.manager@ndma.gy.
4. Click Endorse (moves to Endorsed).
5. Switch to test.hrmanager@ndma.gy.
6. Click Accept (moves to Accepted).

---

## 6) Contract Renewal (My Employment)
Lifecycle: Draft -> Pending Manager -> Pending HR Review -> Pending GM Endorsement -> Pending HR Processing -> Pending GM Final Approval -> Approved

Steps:
1. Login as test.employee@ndma.gy.
2. Create Contract Renewal and Submit.
3. Switch to test.manager@ndma.gy or test.deptmanager@ndma.gy.
4. Click Recommend (moves to Pending HR Review).
5. Switch to test.hruser@ndma.gy (or test.hrmanager@ndma.gy).
6. Click Forward to GM (moves to Pending GM Endorsement).
7. Switch to test.gm@ndma.gy.
8. Click Endorse (moves to Pending HR Processing).
9. Switch to HR User/HR Manager.
10. Click Send to GM (moves to Pending GM Final Approval).
11. Switch to GM and click Approve (moves to Approved).

---

## 7) Job Letter (My Employment)
Lifecycle: Draft -> Pending Manager -> Pending HR -> Completed

Steps:
1. Login as test.employee@ndma.gy.
2. Create Job Letter request and Submit.
3. Switch to test.manager@ndma.gy or test.deptmanager@ndma.gy.
4. Click Approve (moves to Pending HR).
5. Switch to test.hruser@ndma.gy (or test.hrmanager@ndma.gy).
6. Click Issue Letter (moves to Completed).

---

## 8) Employee Profile Update (My Employment)
Lifecycle: Draft -> Submitted -> Approved

Steps:
1. Login as test.employee@ndma.gy.
2. Create Employee Profile Update and Submit.
3. Switch to test.hruser@ndma.gy.
4. Click Approve (moves to Approved).

Optional branch:
- HR User can Rollback for redraft or Cancel.

---

## 9) Performance Evaluation (My Employment)
Primary chain: Draft -> Submitted -> Manager Approved -> HR Manager Approved -> Deputy GM Approved -> GM Approved -> Approved

Steps:
1. Login as test.employee@ndma.gy and Submit draft.
2. Switch to test.manager@ndma.gy and Approve.
3. Switch to test.hrmanager@ndma.gy and Approve.
4. Switch to manager tier (as configured) and Approve to Deputy GM Approved.
5. Switch to test.gm@ndma.gy and Approve to GM Approved.
6. Switch to test.hruser@ndma.gy and Approve to final Approved.

Note:
- This workflow has alternate states (Draft(Manager), Under Review(DGM), Pending HR Manager Approval, Pending GM Approval). Use the same role ownership pattern if you test that branch.

---

## 10) Training Feedback (Requests)
Lifecycle: Draft -> Submitted Feedback -> Reviewed -> Accepted

Steps:
1. Login as test.employee@ndma.gy and Submit.
2. Switch to Manager role user (test.manager@ndma.gy where applicable) and Review.
3. Switch to test.hrmanager@ndma.gy and Accept.

Optional branch:
- Manager or HR Manager can Rollback for redraft.

---

## Validation Checklist for Every Card
1. Record appears in expected list for current state.
2. Next workflow action is visible for current user role.
3. After action, state changes to next expected state.
4. Next role can open and continue workflow.
5. Final state matches lifecycle target for that card.

## Quick Troubleshooting
1. Button missing: save, refresh, re-open, verify role.
2. Permission error: confirm DocPerm + workflow transition allowed role.
3. Wrong status text: check workflow state spelling/casing against doctype select options.
4. Counts not updating: clear cache and reload workspace.
