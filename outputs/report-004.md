# Requirements Gap Analysis Report

**Generated:** 2026-06-12T18:49:19.641647

## Summary

| Metric | Count |
|--------|-------|
| Requirements Extracted | 11 |
| Solutions Identified | 11 |
| **Gaps Found** | **6** |

### Gaps by Severity

- **HIGH**: 1
- **LOW**: 1
- **MEDIUM**: 4

### Gaps by Type

- Implicit Assumption: 1
- Scope Mismatch: 3
- Unaddressed: 2

---

## Gaps

### GAP-001 🔴 [UNADDRESSED]

**Description:** GDPR implementation details for EU deployment are missing.

**Requirements:** REQ-008

**Suggested Action:** Provide detailed GDPR compliance mechanism and data handling process for EU deployment.

---

### GAP-002 🟡 [SCOPE MISMATCH]

**Description:** 2-week parallel run scope is different from requirement.

**Requirements:** REQ-006
**Solutions:** SOL-006

**Suggested Action:** Clarify the 2-week parallel run scope to match the requirement.

---

### GAP-003 🟡 [SCOPE MISMATCH]

**Description:** Hard cutover with no downtime is not fully covered by the solution.

**Requirements:** REQ-010
**Solutions:** SOL-010

**Suggested Action:** Expand the hard cutover mechanism to include no downtime.

---

### GAP-004 🟡 [IMPLICIT ASSUMPTION]

**Description:** Assumes zero data loss on migration is feasible without validation.

**Requirements:** REQ-007
**Solutions:** SOL-007

**Suggested Action:** Validate the assumption of zero data loss on migration.

---

### GAP-005 🟡 [SCOPE MISMATCH]

**Description:** Clear data migration process is not fully covered by the solution.

**Requirements:** REQ-011
**Solutions:** SOL-011

**Suggested Action:** Expand the clear data migration mechanism to match the requirement.

---

### GAP-006 🟢 [UNADDRESSED]

**Description:** SSO via Azure AD and Okta is a nice-to-have feature but not fully addressed.

**Requirements:** REQ-009

**Suggested Action:** Consider adding SSO via Azure AD and Okta as a future enhancement.

---

## Extracted Requirements

### REQ-001 — The new system needs to sync with Salesforce for support ticket updates.
- **Priority:** must-have
- **Raised by:** James (Client)
- **Source:** BT-004.txt

### REQ-002 — The new system needs to sync with Zendesk for open tickets.
- **Priority:** must-have
- **Raised by:** James (Client)
- **Source:** BT-004.txt

### REQ-003 — The new system needs to support federated identity via SAML and OIDC.
- **Priority:** must-have
- **Raised by:** James (Client)
- **Source:** BT-004.txt

### REQ-004 — The new system needs to connect with Stripe for billing tier tickets.
- **Priority:** must-have
- **Raised by:** James (Client)
- **Source:** BT-004.txt

### REQ-005 — The new system needs to support password reset for existing users.
- **Priority:** must-have
- **Raised by:** James (Client)
- **Source:** BT-004.txt

### REQ-006 — The new system needs to have a 2-week parallel run with both systems active.
- **Priority:** must-have
- **Raised by:** James (Client)
- **Source:** BT-004.txt
- **Constraints:** 2-week parallel run; max 4 hours of downtime during cutover

### REQ-007 — The new system needs to have zero data loss on migration.
- **Priority:** must-have
- **Raised by:** James (Client)
- **Source:** BT-004.txt

### REQ-008 — The new system needs to be GDPR compliant.
- **Priority:** must-have
- **Raised by:** James (Client)
- **Source:** BT-004.txt
- **Constraints:** data handling; consent; right to erasure

### REQ-009 — The new system needs to support SSO via Azure AD and Okta.
- **Priority:** nice-to-have
- **Raised by:** James (Client)
- **Source:** BT-004.txt

### REQ-010 — The new system needs to have a hard cutover with no downtime.
- **Priority:** unclear
- **Raised by:** James (Client)
- **Source:** BT-004.txt
- **Constraints:** max 4 hours of downtime during cutover

### REQ-011 — The new system needs to have a clear data migration process.
- **Priority:** unclear
- **Raised by:** James (Client)
- **Source:** BT-004.txt

## Extracted Solutions

### SOL-001 — The new system needs to sync with Salesforce for support ticket updates.
- **Technologies:** REST API, Bulk API
- **Assumptions:** Should be fine for the scale
- **Source:** ET-004.txt

### SOL-002 — The new system needs to sync with Zendesk for open tickets.
- **Technologies:** Zendesk API
- **Deferred:** Phase 2
- **Assumptions:** 300K tickets are manageable
- **Source:** ET-004.txt

### SOL-003 — The new system needs to support federated identity via SAML and OIDC.
- **Technologies:** Auth0, SAML, OIDC
- **Assumptions:** Enterprise connections are feasible
- **Source:** ET-004.txt

### SOL-004 — The new system needs to connect with Stripe for billing tier tickets.
- **Technologies:** Stripe API
- **Deferred:** Next Sprint
- **Assumptions:** Billing tier tickets are not critical for MVP
- **Source:** ET-004.txt

### SOL-005 — The new system needs to support password reset for existing users.
- **Technologies:** Password reset mechanism
- **Assumptions:** Existing user passwords are manageable
- **Source:** ET-004.txt

### SOL-006 — The new system needs to have a 2-week parallel run with both systems active.
- **Technologies:** Parallel run mechanism
- **Assumptions:** 2-week parallel run is feasible for confidence
- **Source:** ET-004.txt

### SOL-007 — The new system needs to have zero data loss on migration.
- **Technologies:** Data migration mechanism
- **Assumptions:** Zero data loss is feasible for migration
- **Source:** ET-004.txt

### SOL-008 — The new system needs to be GDPR compliant.
- **Technologies:** GDPR compliance mechanism
- **Assumptions:** GDPR compliance is feasible for data handling
- **Source:** ET-004.txt

### SOL-009 — The new system needs to support SSO via Azure AD and Okta.
- **Technologies:** Azure AD, Okta
- **Deferred:** Next Sprint
- **Assumptions:** SSO is a nice-to-have feature
- **Source:** ET-004.txt

### SOL-010 — The new system needs to have a hard cutover with no downtime.
- **Technologies:** Hard cutover mechanism
- **Deferred:** Unclear
- **Assumptions:** Hard cutover is feasible for max 4 hours of downtime
- **Source:** ET-004.txt

### SOL-011 — The new system needs to have a clear data migration process.
- **Technologies:** Data migration mechanism
- **Deferred:** Unclear
- **Assumptions:** Clear data migration is feasible
- **Source:** ET-004.txt
