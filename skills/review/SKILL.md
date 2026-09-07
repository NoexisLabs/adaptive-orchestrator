---
name: review
description: Independently review an existing implementation, branch, diff, or pull request for correctness, regressions, architecture, security, domain logic, and verification gaps without implementing fixes.
argument-hint: "[target or review objective]"
model: opus
effort: high
disallowed-tools: Edit, Write, NotebookEdit
---

# Adaptive Review

Review target: $ARGUMENTS

This is a review-only workflow. Do not implement fixes. Shell commands, if used, must be read-only inspection commands.

1. Establish the original objective or infer it from the target and repository evidence. State uncertainty rather than inventing intent.
2. Inspect the actual changed implementation, relevant surrounding code, contracts, tests, configuration, and migration/schema effects.
3. Use the read-only `advisor` as the primary independent reviewer for substantial changes.
4. Invoke `security-auditor` when authentication, authorization, secrets, payments, tenant isolation, privileged operations, external inputs, or sensitive data are affected.
5. Invoke `domain-logic-auditor` when correctness depends on specialized calculations, business/scientific/operational rules, time semantics, units, thresholds, transformations, or invariants.
6. Check for accidental scope creep, compatibility breaks, performance/concurrency regressions, missing observability, weak failure handling, test gaps, debug artifacts, secret leakage, and architecture drift.
7. Findings use CRITICAL, HIGH, MEDIUM, LOW, INFORMATIONAL/OPTIONAL as appropriate. Support each material finding with repository evidence.
8. Do not let reviewer confidence override failing evidence. If the evidence is insufficient, say what must be inspected or tested next.

Return:

### Review result
Overall disposition: PASS, PASS WITH FINDINGS, or BLOCKED.

### Findings
For each material issue: SEVERITY, COMPONENT, EVIDENCE, IMPACT, RECOMMENDED CHANGE, VERIFICATION REQUIRED.

### Verification gaps
Checks that are missing or inconclusive.

### Residual risk
Only unresolved risks supported by evidence.
