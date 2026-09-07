---
name: audit
description: Perform a deep read-only architecture, security, domain-logic, data-integrity, reliability, and verification audit of a codebase or subsystem without implementing fixes.
argument-hint: "[scope or audit objective]"
model: fable
effort: high
disallowed-tools: Edit, Write, NotebookEdit
---

# Adaptive Audit

Audit scope: $ARGUMENTS

This is a deep analysis workflow, not an implementation workflow. Do not modify the repository. Shell commands, if used, must be read-only inspection commands.

## Audit procedure

1. Map the relevant architecture, data flow, trust boundaries, state transitions, persistence, external dependencies, and critical execution paths from repository evidence.
2. Use `repository-explorer` for broad mechanical discovery when useful.
3. Use `advisor` to challenge the architecture and assumptions independently.
4. Use `security-auditor` for security-sensitive surfaces.
5. Use `domain-logic-auditor` when specialized calculations, business/scientific/operational rules, transformations, units, thresholds, time semantics, or invariants are material.
6. Trace high-risk findings to concrete code/config/schema/test evidence. Do not infer vulnerabilities or logic errors solely from naming or documentation.
7. Check correctness, authorization, data isolation, secrets, input handling, error behavior, concurrency, migrations, data integrity, external API failure modes, observability, performance bottlenecks, dependency fragility, testing gaps, and recovery/rollback behavior as applicable.
8. Prioritize root causes and systemic failure modes over cosmetic findings.
9. Classify findings CRITICAL, HIGH, MEDIUM, LOW, INFORMATIONAL. CRITICAL/HIGH findings require a concrete evidence trail and a recommended remediation/verification path.
10. Do not implement fixes during the audit. If the user later asks to remediate, hand the findings to `/adaptive-orchestrator:orchestrate`.

## Output

### Executive summary
Scope, overall risk, and the most consequential findings.

### Architecture and trust boundaries
Evidence-backed map of the relevant system.

### Findings
For each finding: SEVERITY, COMPONENT, EVIDENCE, FAILURE/ATTACK PATH, IMPACT, ROOT CAUSE, RECOMMENDED REMEDIATION, VERIFICATION REQUIRED.

### Verification gaps
Important claims that could not be proven from available evidence.

### Prioritized remediation plan
Order fixes by risk reduction and dependency, without implementing them.
