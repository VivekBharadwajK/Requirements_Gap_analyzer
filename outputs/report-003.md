# Requirements Gap Analysis Report

**Generated:** 2026-06-12T19:13:27.308295

## Summary

| Metric | Count |
|--------|-------|
| Requirements Extracted | 6 |
| Solutions Identified | 8 |
| **Gaps Found** | **6** |

### Gaps by Severity

- **HIGH**: 3
- **MEDIUM**: 3

### Gaps by Type

- Ambiguity: 1
- Implicit Assumption: 1
- Scope Mismatch: 2
- Unaddressed: 2

---

## Gaps

### GAP-001 🔴 [UNADDRESSED]

**Description:** EU data residency is not explicitly covered by the solution, which assumes EU data can be stored in US and APAC.

**Requirements:** REQ-004

**Suggested Action:** Clarify with engineering team: What specific measures will be taken to ensure GDPR compliance for EU deployments?

---

### GAP-002 🟡 [UNADDRESSED]

**Description:** The solution does not explicitly cover the requirement for a fully responsive web portal, only mentions it as a constraint.

**Requirements:** REQ-005

**Suggested Action:** Ask engineering team to confirm: Will the web portal be fully responsive and meet the 'no native app needed' requirement?

---

### GAP-003 🔴 [SCOPE MISMATCH]

**Description:** The solution's scope for the web portal does not match the requirement's expected scale, as it only covers 10,000 concurrent users.

**Requirements:** REQ-001
**Solutions:** SOL-007

**Suggested Action:** Clarify with engineering team: How will the solution handle peak concurrent usage of up to 2 million users?

---

### GAP-004 🔴 [SCOPE MISMATCH]

**Description:** The solution's scope for infrastructure deployment does not match the requirement's expected scale, as it only covers a single region.

**Requirements:** REQ-001
**Solutions:** SOL-008

**Suggested Action:** Clarify with engineering team: How will the solution handle deployments across multiple regions?

---

### GAP-005 🟡 [IMPLICIT ASSUMPTION]

**Description:** The solution assumes that 99.5% uptime is realistic for an initial launch, which may not align with the requirement's expected 99.9% uptime.

**Requirements:** REQ-002
**Solutions:** SOL-003

**Suggested Action:** Ask engineering team to confirm: Is the assumed uptime realistic and how will it be achieved?

---

### GAP-006 🟡 [AMBIGUITY]

**Description:** The requirement's constraint for scheduled maintenance windows is not explicitly covered by the solution.

**Requirements:** REQ-003
**Solutions:** SOL-003

**Suggested Action:** Clarify with engineering team: What specific measures will be taken to ensure compliance with this requirement?

---

## Extracted Requirements

### REQ-001 — Expected scale: 50,000 enterprise accounts with 5-200 users per account, total users up to 2 million, peak concurrent usage of 10,000 users
- **Priority:** must-have
- **Raised by:** James (Client)
- **Source:** BT-003.txt
- **Constraints:** User growth rate: 30% year-over-year

### REQ-002 — Page loads under 2 seconds, API responses under 500ms
- **Priority:** must-have
- **Raised by:** James (Client)
- **Source:** BT-003.txt
- **Constraints:** Performance expectations: page load time < 2s, API response time < 500ms

### REQ-003 — 99.9% uptime minimum, scheduled maintenance windows outside business hours
- **Priority:** must-have
- **Raised by:** James (Client)
- **Source:** BT-003.txt
- **Constraints:** Availability: 99.9% uptime, scheduled maintenance during non-business hours

### REQ-004 — EU data stays in EU, US and APAC can be wherever makes sense for latency
- **Priority:** must-have
- **Raised by:** James (Client)
- **Source:** BT-003.txt
- **Constraints:** Data residency: EU data only, US and APAC data storage flexible

### REQ-005 — Web portal must be fully responsive, native app not required for v1
- **Priority:** must-have
- **Raised by:** James (Client)
- **Source:** BT-003.txt
- **Constraints:** Mobile experience: web portal responsive, no native app needed

### REQ-006 — Admins need a dashboard showing ticket volume, resolution times, SLA compliance rates in real-time or near-real-time
- **Priority:** must-have
- **Raised by:** James (Client)
- **Source:** BT-003.txt
- **Constraints:** Reporting and analytics: real-time or near-real-time reporting needed

## Extracted Solutions

### SOL-001 — Deploy on AWS, single region to start — eu-west-1 since most users are in Europe.
- **Technologies:** AWS, ECS Fargate
- **Assumptions:** Should be fine with properly indexed queries
- **Source:** ET-003.txt

### SOL-002 — Use Redis for session data and frequently accessed stuff like account profiles.
- **Technologies:** Redis
- **Assumptions:** Should keep response times snappy
- **Source:** ET-003.txt

### SOL-003 — Set up CloudWatch dashboards and PagerDuty alerts for downtime.
- **Technologies:** CloudWatch, PagerDuty
- **Assumptions:** 99.5% uptime is realistic for an initial launch
- **Source:** ET-003.txt

### SOL-004 — Use Next.js for the main pages to help with initial load.
- **Technologies:** Next.js
- **Assumptions:** Static assets can come from S3 directly. Let's not over-engineer
- **Source:** ET-003.txt

### SOL-005 — Use a single Postgres instance with a read replica.
- **Technologies:** Postgres, RDS Postgres
- **Assumptions:** We can shard later if needed but I don't think we'll hit those limits for a while
- **Source:** ET-003.txt

### SOL-006 — Use S3 directly for static assets.
- **Technologies:** S3
- **Assumptions:** Probably not for v1. Let's not over-engineer
- **Source:** ET-003.txt

### SOL-007 — Use CDN for the web portal.
- **Technologies:** CDN
- **Assumptions:** Web portal must be fully responsive, native app not required for v1
- **Source:** ET-003.txt

### SOL-008 — Use Terraform to set up the infrastructure.
- **Technologies:** Terraform
- **Assumptions:** Let me knock out the Terraform configs this sprint
- **Source:** ET-003.txt
