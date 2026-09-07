# Orchestration Protocol

This document defines the coordination contract used by Adaptive Orchestrator.

## Operating modes

### FAST
Minimize agent count and cost. Preserve mandatory T3 specialist and evidence gates.

### AUTO
Default risk-aware routing.

### STRICT
Use independent pre-review and final review for substantial work, plus relevant specialist gates and broader verification.

## Complexity tiers

| Tier | Typical work | Default max subagents |
|---|---|---:|
| T0 | trivial/local | 0 |
| T1 | narrow feature or bug | 2 |
| T2 | cross-cutting/architectural | 4 |
| T3 | critical/security/domain-sensitive | 6 |

Default maximum concurrency is 3.

## Preferred model aliases

| Role | Alias | Effort | Max turns |
|---|---|---|---:|
| Orchestrator | `fable` | high | 40 |
| Advisor | `opus` | high | 15 |
| Domain Logic Auditor | `fable` | high | 18 |
| Security Auditor | `opus` | high | 18 |
| Backend Engineer | `sonnet` | medium | 30 |
| Frontend Engineer | `sonnet` | medium | 30 |
| Test Engineer | `sonnet` | medium | 20 |
| Repository Explorer | `haiku` | low | 10 |
| Isolated Implementer | `sonnet` | medium | 30 |

These are preferences. Claude Code checks aliases against `availableModels` and can substitute an allowed model or inherit the session model.

## Task packet

Every delegated worker should receive:

```text
TASK_ID
OBJECTIVE
CONTEXT
FILES_ALLOWED
FILES_FORBIDDEN
DEPENDENCIES
CONSTRAINTS
ACCEPTANCE_CRITERIA
VERIFICATION
RETURN_FORMAT
```

Implementation workers return:

```text
STATUS
FILES_CHANGED
SUMMARY
EVIDENCE
TEST_RESULTS
ASSUMPTIONS
OPEN_RISKS
```

Worktree-isolated workers also return:

```text
MERGE_NOTES
```

## Retry policy

Per work unit:

1. One normal implementation attempt.
2. One evidence-driven correction attempt.
3. After a second meaningful failure, stop and return to orchestration for root-cause re-planning or justified reasoning escalation.

Repeated variants of the same failed hypothesis are not a retry strategy.

## Confidence escalation

Confidence never overrides evidence.

- HIGH (~90%+): proceed only if evidence gates pass.
- MEDIUM (~70-89%): add targeted inspection or independent review.
- LOW (<70%): re-investigate before implementation.
- Material disagreement between independent agents: reconcile from repository evidence and escalate reasoning if still unresolved.

## Parallel writers

- One writer: normal implementation agent in the current tree.
- Multiple independent writers: `isolated-implementer` with `isolation: worktree`.
- Overlapping files: serialize the work or establish an explicit merge plan.

## Evidence gate

A completion claim is not evidence. Use the checks appropriate to the change: targeted tests, regression tests, build/type/lint, reproduction, runtime/output inspection, schema validation, contracts/invariants, and final diff review.

## Review independence

Whenever practical:

```text
AUTHOR != PRIMARY_REVIEWER
```

Advisor, security auditor, domain auditor, and repository explorer are read-only plugin agents.
