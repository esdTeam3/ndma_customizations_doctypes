# HR Operations Workspace Training Guide

## Purpose
This guide walks trainers through every Number Card in the HR Operations workspace and shows the user-to-user handoffs needed to move records through the full lifecycle.

Scope covers cards under:
- Leave Application
- Time Off Request
- Resumption
- Contract Renewal
- Job Letter

## Training Users (Current Site)
Use these users for role switching:

| Role | Training User |
|---|---|
| Employee - NDMA | test.employee@ndma.gy |
| Manager - NDMA | test.manager@ndma.gy |
| HR User | test.hruser@ndma.gy |
| HR Manager | test.hrmanager@ndma.gy |
| Department Manager | test.deptmanager@ndma.gy |
| General Manager | test.gm@ndma.gy |
| DGM (Operations) - NDMA | test.dgmops@ndma.gy |

## General Training Rules
1. Start every scenario by creating a fresh record.
2. Save before checking workflow actions.
3. After each workflow action, refresh HR Operations and validate card count movement.
4. Use impersonation or logout/login to switch users.
5. Keep all training records in Human Resources department when card filter requires it.

---

## A. Leave Application Cards

### A1. Submitted
Card filter: Leave Application.workflow_state = Submitted and department = Human Resources

Steps:
1. Login as test.employee@ndma.gy.
2. Create Leave Application with department Human Resources.
3. Submit from Draft.
4. Validate card Submitted increments by 1.
5. Keep record in Submitted for next card walkthroughs.

### A2. Pending HR Approval
Card filter: Leave Application.workflow_state = Pending HR Approval

Steps:
1. Start with a record in Submitted.
2. Switch to test.manager@ndma.gy.
3. Open the same Leave Application.
4. Use workflow action Verify.
5. Validate card movement: Submitted down, Pending HR Approval up.

### A3. Pending HR Manager Approval
Card filter: Leave Application.workflow_state = Pending HR Manager Approval

Steps:
1. Start with a record in Pending HR Approval.
2. Switch to test.hruser@ndma.gy.
3. Open record.
4. Use workflow action Accept.
5. Validate card movement: Pending HR Approval down, Pending HR Manager Approval up.

### A4. Pending HR Verification
Card filter: Leave Application.workflow_state = Pending HR Verification

Steps (special path):
1. Login as test.gm@ndma.gy.
2. Create a new Leave Application (or open Draft created for GM route).
3. Submit using GM route that leads to Pending HR Verification.
4. Validate Pending HR Verification card increments.
5. Switch to test.hrmanager@ndma.gy and approve to complete this branch.

### A5. Pending Leave Adjustment Approval
Card filter: Leave Application.workflow_state = Pending Leave Adjustment Approval and department = Human Resources

Steps:
1. Start with a Leave Application already in Approved.
2. Switch to test.employee@ndma.gy.
3. Click workflow action Adjust Leave.
4. From Draft Adjustment, click Submit Adjustment.
5. Validate Pending Leave Adjustment Approval increments.

### A6. Pending Leave Adjustment HR Review
Card filter: Leave Application.workflow_state = Pending Leave Adjustment HR Review

Steps:
1. Start with record in Pending Leave Adjustment Approval.
2. Switch to test.manager@ndma.gy.
3. Click Accept Adjustment.
4. Validate card movement to Pending Leave Adjustment HR Review.

### A7. Leave Adjustment Approved
Card filter: Leave Application.workflow_state = Leave Adjustment Approved

Steps:
1. Start with record in Pending Leave Adjustment HR Review.
2. Switch to test.hrmanager@ndma.gy.
3. Click Approve Adjustment.
4. Validate Leave Adjustment Approved increments.
5. Optional closure: click Update Leave Dates to return to Approved.

---

## B. Time Off Request Cards

### B1. Time Off Request - Submitted
Card filter: Time Off.status = Pending Manager

Steps:
1. Login as test.employee@ndma.gy.
2. Create Time Off request.
3. Click Submit.
4. Validate Time Off Request - Submitted increments.

### B2. Time Off Request - Pending HR Approval
Card filter: Time Off.status = Pending HR Approval

Steps:
1. Start with Time Off in Pending Manager.
2. Switch to test.manager@ndma.gy.
3. Click Approve.
4. Validate card movement to Time Off Request - Pending HR Approval.
5. Switch to test.hruser@ndma.gy or test.hrmanager@ndma.gy and Approve to complete lifecycle.

---

## C. Resumption Cards

### C1. Resumption - Submitted
Card filter: Leave Resumption.workflow_state = Submitted and department = Human Resources

Steps:
1. Login as test.employee@ndma.gy.
2. Create Leave Resumption record for Human Resources.
3. Submit.
4. Validate Resumption - Submitted increments.

### C2. Resumption - Endorsed
Card filter: Leave Resumption.workflow_state = Endorsed

Steps:
1. Start with record in Submitted.
2. Switch to test.manager@ndma.gy.
3. Click Endorse.
4. Validate Resumption - Endorsed increments.

### C3. Resumption - Accepted
Card filter: Leave Resumption.workflow_state = Accepted

Steps:
1. Start with record in Endorsed.
2. Switch to test.hrmanager@ndma.gy.
3. Click Accept.
4. Validate Resumption - Accepted increments.

---

## D. Contract Renewal Cards

### D1. Contract Renewal Pending HR Review
Card filter: Contract Renewal.status = Pending HR Review

Steps:
1. Login as test.employee@ndma.gy.
2. Create Contract Renewal record and Submit.
3. Switch to test.manager@ndma.gy and click Recommend.
4. Validate Contract Renewal Pending HR Review increments.

### D2. Contract Renewal Pending HR Processing
Card filter: Contract Renewal.status = Pending HR Processing

Steps:
1. Start with record in Pending HR Review.
2. Switch to test.hruser@ndma.gy (or HR Manager).
3. Click Forward to GM.
4. Switch to test.gm@ndma.gy and click Endorse.
5. Validate Contract Renewal Pending HR Processing increments.
6. Continue lifecycle: HR Send to GM -> GM Approve.

---

## E. Job Letter Card

### E1. Job Letter Pending HR
Card filter: Job Letter.status = Pending HR

Steps:
1. Login as test.employee@ndma.gy.
2. Create Job Letter request and Submit.
3. Switch to test.manager@ndma.gy (or Department Manager).
4. Click Approve.
5. Validate Job Letter Pending HR increments.
6. Switch to test.hruser@ndma.gy (or HR Manager) and click Issue Letter to complete.

---

## Fast Validation Checklist (After Each Scenario)
1. Source card count decreases after transition.
2. Target card count increases after transition.
3. Workflow state/status equals the card filter state.
4. Next role can see the expected workflow action.

## Troubleshooting
1. If action button is missing: save record, refresh, re-open, confirm user role.
2. If status value error appears: check workflow state spelling/casing against card filter.
3. If permission denied appears: verify DocPerm plus workflow transition allowed role.
4. If card count does not move: clear cache and refresh workspace.
