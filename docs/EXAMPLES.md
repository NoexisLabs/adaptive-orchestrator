# Usage Examples

These examples show intended orchestration behavior, not guaranteed exact agent transcripts. The orchestrator should adapt to repository evidence and user constraints.

## T0 — trivial fix

Request:

```text
/adaptive-orchestrator:orchestrate auto Fix the typo in the API error message and verify it
```

Expected behavior:

```text
classify T0
→ direct edit
→ targeted verification
→ done
```

No subagent should be spawned merely because the plugin supports multi-agent work.

## T1 — narrow bug

Request:

```text
/adaptive-orchestrator:orchestrate auto Fix the null dereference in the invoice formatter and add regression coverage
```

Expected behavior:

```text
classify T1
→ inspect relevant path
→ one implementation worker
→ targeted test engineer or direct verification
→ evidence gate
```

## T2 — cross-cutting change

Request:

```text
/adaptive-orchestrator:orchestrate auto Replace the cache invalidation strategy across API and worker processes without changing public behavior
```

Expected behavior:

```text
classify T2
→ orchestrator builds plan
→ independent advisor challenges assumptions
→ revised work graph
→ one or more independent implementation workers
→ worktree isolation when parallel writers are safe
→ verification
→ independent final review
→ evidence gate
```

## T3 — security-sensitive change

Request:

```text
/adaptive-orchestrator:orchestrate strict Refactor tenant authorization so every object-level read and write enforces tenant isolation
```

Expected behavior:

```text
classify T3
→ orchestrator
→ security pre-review
→ independent advisor
→ implementation
→ tests including negative authorization cases
→ security post-review
→ independent final review
→ no unresolved CRITICAL/HIGH findings
→ completion gate
```

## Domain-critical logic

Request:

```text
/adaptive-orchestrator:orchestrate strict Rewrite the tax calculation engine while preserving all documented rounding and threshold rules
```

Expected behavior includes an independent Domain Logic Auditor that reconstructs rules from evidence and checks units, thresholds, time semantics, precision, missing values, boundaries, and outputs.

## Read-only review

Request:

```text
/adaptive-orchestrator:review Review the current diff for architectural regressions, unsafe assumptions, and missing tests
```

Expected behavior:

- inspect only
- no code edits
- evidence-backed findings
- severity classification
- recommended changes

## Deep audit

Request:

```text
/adaptive-orchestrator:audit Audit authentication, authorization, secrets handling, data integrity, and test coverage
```

Expected behavior:

- map relevant architecture and data flow
- invoke specialist reviewers where justified
- produce findings with evidence and impact
- do not implement remediation

## FAST vs AUTO vs STRICT

The same request can produce a different orchestration envelope depending on mode.

### FAST

Prefer the minimum useful number of agents and checks. Do not skip mandatory T3 specialist gates.

### AUTO

Default. Balance assurance, cost, and speed based on observed risk.

### STRICT

Increase independent challenge and verification. Appropriate when consequences are high or when the user explicitly values assurance over cost.

## Failure and retry example

If an implementation attempt fails verification:

```text
attempt 1
→ evidence shows failure
→ one evidence-driven correction attempt
→ failure persists
→ stop repeating the same hypothesis
→ return to orchestrator
→ re-investigate root cause / dependencies
→ escalate model or effort only if justified
```

## Parallelism example

Safe:

```text
worker A: backend files
worker B: independent frontend files
→ worktree isolation
→ explicit integration plan
```

Unsafe:

```text
worker A: auth/service.py
worker B: auth/service.py
→ do not parallelize without a deliberate merge strategy
```
