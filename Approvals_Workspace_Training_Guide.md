# Approvals Workspace Training Guide

## Objective
This guide walks through every card shown in the Approvals workspace and trains users to hand off records across the correct roles until each document reaches its end state.

Cards covered from this workspace:
- Time Off
- Leave Application
- Leave Resumption
- Job Letter
- Performance Evaluation
- Contract Renewal
- Transportation Request
- Material Request
- Payment Entry
- Purchase Order
- Vehicle Incident Report

## Suggested Training Users
Use these users when switching roles during practice:

| Role | Training User |
|---|---|
| Employee - NDMA | test.employee@ndma.gy |
| Manager - NDMA | test.manager@ndma.gy |
| Department Manager | test.deptmanager@ndma.gy |
| HR User | test.hruser@ndma.gy |
| HR Manager | test.hrmanager@ndma.gy |
| General Manager | test.gm@ndma.gy |
| DGM (Operations) - NDMA | test.dgmops@ndma.gy |
| Fleet Manager | test.fleetmgr@ndma.gy |
| DGM (Admin) - NDMA | Administrator |
| PR Verifier | Administrator |
| Professional Assistant - NDMA | Administrator |
| Transportation request Approver | Administrator |
| Transportation Request Admin | Administrator |
| Accounts Manager / Accounts User | Administrator |
| Procurement Officer | Administrator |

## Training Conventions
1. Start each scenario with a new document.
2. Save once before checking workflow actions.
3. After each action, refresh and verify the workflow state.
4. Immediately switch to the next owner role and continue.
5. Follow the happy path first, then test reject/rollback.

---

## 1) Time Off
Happy path state flow:
Draft -> Pending Manager -> Pending HR Approval -> Approved

Steps:
1. Login as test.employee@ndma.gy and create Time Off.
2. Click Submit (state: Pending Manager).
3. Switch to test.manager@ndma.gy (or test.deptmanager@ndma.gy).
4. Click Approve (state: Pending HR Approval).
5. Switch to test.hruser@ndma.gy (or test.hrmanager@ndma.gy).
6. Click Approve (state: Approved).

---

## 2) Leave Application
Recommended happy path:
Draft -> Submitted -> Pending HR Approval -> Pending HR Manager Approval -> Approved

Steps:
1. Login as test.employee@ndma.gy and submit Leave Application.
2. Switch to test.manager@ndma.gy.
3. Click Verify (state: Pending HR Approval).
4. Switch to test.hruser@ndma.gy.
5. Click Accept (state: Pending HR Manager Approval).
6. Switch to test.hrmanager@ndma.gy.
7. Click Approve (state: Approved).

Executive branch practice:
1. Submit from Draft as DGM/Admin pathway (where applicable).
2. Drive state to Pending GM Approval.
3. Switch to test.gm@ndma.gy and click Approve.

Adjustment branch practice:
1. From Approved, employee clicks Adjust Leave.
2. Employee submits adjustment.
3. Manager accepts adjustment.
4. HR Manager approves adjustment.

---

## 3) Leave Resumption
Happy path state flow:
Draft -> Submitted -> Endorsed -> Accepted

Steps:
1. Login as test.employee@ndma.gy and submit Leave Resumption.
2. Switch to test.manager@ndma.gy.
3. Click Endorse (state: Endorsed).
4. Switch to test.hrmanager@ndma.gy.
5. Click Accept (state: Accepted).

Fast-track variation:
- HR Manager can also Accept directly from Submitted.

---

## 4) Job Letter
Happy path state flow:
Draft -> Pending Manager -> Pending HR -> Completed

Steps:
1. Login as test.employee@ndma.gy and submit Job Letter request.
2. Switch to test.manager@ndma.gy (or test.deptmanager@ndma.gy).
3. Click Approve (state: Pending HR).
4. Switch to test.hruser@ndma.gy (or test.hrmanager@ndma.gy).
5. Click Issue Letter (state: Completed).

---

## 5) Performance Evaluation
Primary chain:
Draft -> Submitted -> Manager Approved -> HR Manager Approved -> Deputy GM Approved -> GM Approved -> Approved

Steps:
1. Login as test.employee@ndma.gy and submit evaluation.
2. Switch to test.manager@ndma.gy and click Approve.
3. Switch to test.hrmanager@ndma.gy and click Approve.
4. Switch to manager tier approver and click Approve to move to Deputy GM Approved.
5. Switch to test.gm@ndma.gy and click Approve to move to GM Approved.
6. Switch to test.hruser@ndma.gy and click Approve to final Approved.

Alternate executive chain:
Draft(Manager) -> Under Review(DGM) -> Pending HR Manager Approval -> Pending GM Approval -> Approved

---

## 6) Contract Renewal
Happy path state flow:
Draft -> Pending Manager -> Pending HR Review -> Pending GM Endorsement -> Pending HR Processing -> Pending GM Final Approval -> Approved

Steps:
1. Login as test.employee@ndma.gy and submit Contract Renewal.
2. Switch to test.manager@ndma.gy (or test.deptmanager@ndma.gy).
3. Click Recommend (state: Pending HR Review).
4. Switch to test.hruser@ndma.gy (or test.hrmanager@ndma.gy).
5. Click Forward to GM (state: Pending GM Endorsement).
6. Switch to test.gm@ndma.gy.
7. Click Endorse (state: Pending HR Processing).
8. Switch to HR User/HR Manager.
9. Click Send to GM (state: Pending GM Final Approval).
10. Switch to test.gm@ndma.gy.
11. Click Approve (state: Approved).

---

## 7) Transportation Request
Happy path state flow:
Draft -> Approval pending by Manager -> Approved -> Vehicle Assigned

Steps:
1. Login as test.employee@ndma.gy and submit Transportation Request.
2. Switch to Transportation request Approver (Administrator).
3. Click Approve (state: Approved).
4. Switch to Transportation Request Admin (Administrator).
5. Click Approve (state: Vehicle Assigned).

---

## 8) Material Request
Executive-approval path in your workflow:
Draft -> Drafted PR -> Pending verification -> Pending PR (admin/ops) -> DGM Verified PR (optional) -> Approved PR

Steps:
1. Login as Professional Assistant - NDMA (Administrator) and submit for divisional approval.
2. Switch to test.manager@ndma.gy and click Submit for Approval (state: Pending verification).
3. Switch to PR Verifier (Administrator):
4. Choose Verified as valid (admin) for admin route, or Verified as valid (ops) for ops route.
5. If admin route: switch to DGM (Admin) - NDMA (Administrator) and Approve.
6. If ops route: switch to DGM (Operations) - NDMA (test.dgmops@ndma.gy) and Approve.
7. To test escalation branch, DGM can choose Escalate for Approval to DGM Verified PR.
8. Switch to test.gm@ndma.gy and click Approve (state: Approved PR).

Notes:
- After Approved PR, downstream procurement states continue (bid/evaluation/award/PO/payment).
- Those later stages are mostly non-manager operational roles and can be simulated with Administrator.

---

## 9) Payment Entry
No active custom workflow was detected for Payment Entry in this site.

Training approach:
1. Create Payment Entry as Finance/Accounts user.
2. Save and validate accounting dimensions and references.
3. Submit document through standard submit flow.
4. Confirm GL impact and linked document status updates.
5. Test cancel/amend permissions using an Accounts Manager user.

If you later add a custom Payment Entry workflow, update this section with state/action/role handoffs.

---

## 10) Purchase Order
Happy path state flow:
Draft -> Submitted -> Pending DGM Approval -> Awaiting Contract -> Paid

Steps:
1. Login as Procurement Officer (Administrator) and submit PO.
2. Switch to Accounts Manager (Administrator).
3. Click Submit for DGM Approval (state: Pending DGM Approval).
4. Switch to DGM (Admin) - NDMA (Administrator).
5. Click Approve and Move to Contract (state: Awaiting Contract).
6. Switch to Accounts Manager or Accounts User (Administrator).
7. Click Pay and Complete (state: Paid).

---

## 11) Vehicle Incident Report
Happy path state flow:
Draft -> Pending Verification -> Pending DGM -> Closed

Steps:
1. Login as test.employee@ndma.gy and submit Vehicle Incident Report.
2. Switch to test.fleetmgr@ndma.gy.
3. Click Verify (state: Pending DGM).
4. Switch to test.dgmops@ndma.gy.
5. Click Sign Off (state: Closed).

---

## Cross-Card Validation Checklist
Use this checklist for every card test:
1. Correct card opens the expected doctype list/form.
2. Expected workflow action is visible for current role.
3. Action moves document to the expected next state.
4. Next role can see and continue the record.
5. Final state matches the lifecycle target in this guide.

## Quick Troubleshooting
1. Missing action button: save, reload form, verify role and workflow state.
2. Permission denied: verify DocPerm and workflow transition role both allow action.
3. Wrong state text: check state label spelling/casing in workflow and doctype options.
4. Card count mismatch: reload workspace and clear cache.
