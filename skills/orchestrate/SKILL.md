---
name: orchestrate
description: Coordinate engineering tasks using risk-aware multi-agent orchestration, native Claude Code model routing, independent review, evidence gates, specialist audits, bounded retries, and worktree isolation. Use automatically for complex, cross-cutting, security-sensitive, domain-critical, or high-risk work; keep trivial work lightweight.
argument-hint: "[fast|auto|strict] <task>"
---

# Adaptive Orchestrator

Operate like a senior engineering organization, not a single undifferentiated coding agent.

User input: $ARGUMENTS

## 1. Select operating mode

If the first argument is FAST, AUTO, or STRICT, use it case-insensitively and treat the remaining arguments as the task. Otherwise default to AUTO.

### FAST
Optimize for speed and cost while preserving essential verification.
- T0: direct execution + targeted verification
- T1: implementation + verification
- T2: orchestrator + implementation + verification; add advisor only when uncertainty/risk is material
- T3: required specialist reviewer + implementation + verification
- Prefer fewer agents and narrower test scope

### AUTO
Default risk-aware behavior. Scale orchestration to complexity and evidence.

### STRICT
Maximize independent verification.
- Advisor pre-review for T2/T3
- Author and primary reviewer must differ where practical
- Required specialist reviews for relevant T3 domains
- Independent final review for substantial changes
- Broader regression evidence and final diff inspection

Mode never weakens mandatory safety, security, or evidence gates for T3 work.

## 2. Use native model routing and fallback

Use model-family aliases declared by the plugin agents. They are preferences, not hard dependencies.

Preferred assignments:
- orchestrator: Fable
- advisor/final independent reviewer: Opus
- domain-logic auditor: Fable
- security auditor: Opus
- implementation/test agents: Sonnet
- repository explorer: Haiku

Claude Code checks aliases against the user's `availableModels` policy. If a family is blocked or unavailable, Claude Code may substitute an allowed model from that family or fall back to the inherited session model. Continue the workflow when this occurs. Do not fail merely because a preferred family is unavailable, and do not pin dated model IDs.

## 3. Classify complexity and risk

### T0 — Trivial
One-line fix, typo, obvious local configuration change, simple lookup.
Flow: `direct execution -> targeted verification`

### T1 — Standard
Well-defined feature or bug within a narrow component.
Flow: `implementation -> verification`, with independent review only when risk warrants it.

### T2 — Complex
Cross-module work, unclear root cause, migrations, concurrency, broad refactors, meaningful architecture/performance changes.
Flow in AUTO: `orchestrator -> advisor -> revised plan -> workers -> verification -> independent final review`

### T3 — Critical / specialist
Authentication, authorization, payments, sensitive data, destructive migrations, privileged operations, compliance-sensitive behavior, critical domain calculations, highly consequential production changes.
Flow in AUTO/STRICT: `orchestrator -> relevant specialist pre-review -> advisor -> workers -> verification -> specialist post-review -> independent final review -> completion gate`

## 4. Set an orchestration budget before dispatch

Default maximum total subagents per request:
- T0: 0
- T1: 2
- T2: 4
- T3: 6

Default maximum concurrent subagents: 3.

FAST should reduce the budget where possible. STRICT may use the full budget but must not spawn agents merely to create activity. Exceed these defaults only when the task structure clearly justifies it; record why.

The optimization target is correctness per unit of compute, not agent count.

## 5. Orchestrator contract

Before significant edits establish:
- OBJECTIVE
- CURRENT_STATE backed by repository evidence
- CONSTRAINTS
- FILES_SYSTEMS_AFFECTED
- DEPENDENCIES
- PROPOSED_PLAN
- RISKS
- VERIFICATION_METHOD
- MODE
- COMPLEXITY_TIER
- AGENT_BUDGET

Do not speculate about code that can be inspected. Protect orchestrator context by delegating large mechanical searches and requesting concise evidence-backed returns.

## 6. Delegated task packet

Every worker receives a bounded packet:

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

Isolated worktree workers additionally return `MERGE_NOTES`.

## 7. Advisor gate

For T2/T3 in AUTO/STRICT, challenge the plan before implementation. Provide the original objective, discovered architecture, constraints, evidence, and proposed plan.

Review for unsupported assumptions, hidden dependencies, unnecessary complexity, security/authorization, data integrity, migrations/backward compatibility, concurrency, performance, observability, failure modes, testing gaps, simpler alternatives, and symptom fixes that miss root causes.

Findings: CRITICAL, HIGH, MEDIUM, LOW, OPTIONAL. A bare "approved" is not sufficient; soundness must be explained.

## 8. Specialist gates

### Domain logic auditor
Use when correctness depends on specialized business, scientific, financial, operational, legal-rule, analytics, optimization, or other nontrivial domain logic. Independently reconstruct intended logic and check units, directionality, transformations, missing values, edge conditions, time semantics, precision, invariants, and user-visible outputs.

### Security auditor
Use for material changes involving authentication, authorization, permissions, sessions, secrets, payments, tenant isolation, user data, uploads, external APIs, administrative functionality, or privileged operations. Review both intended design and resulting implementation evidence/diff.

Specialist reviewers are read-only by design. Provide them the diff/evidence they need instead of asking them to repair their own findings.

## 9. Evidence-first rule

Never invent APIs, routes, schemas, columns, environment variables, dependencies, tests, infrastructure, or domain rules.

Evidence priority:
1. executable implementation
2. schemas/migrations
3. configuration
4. tests
5. project documentation
6. comments

Documentation is not authoritative when implementation contradicts it.

## 10. Root cause and retry budget

For bugs:
`trace/reproduce -> root cause -> blast radius -> smallest robust fix -> tests -> regression check`

Per work unit:
1. one normal implementation attempt
2. one evidence-driven correction attempt
3. after a second meaningful failure, stop and return to the orchestrator for root-cause re-planning or reasoning escalation

Do not keep retrying variants of the same failed hypothesis.

## 11. Work isolation and parallelism

Parallelize only independent work.
- ONE WRITER: use the normal implementation agent in the current tree
- MULTIPLE INDEPENDENT WRITERS: use `isolated-implementer` or equivalent worktree isolation
- OVERLAPPING FILES: do not parallelize; serialize or create an explicit merge plan

Do not use worktree isolation as a substitute for dependency analysis.

## 12. Confidence-based escalation

Confidence is advisory and never overrides evidence.

After investigation or a failed verification, estimate confidence in the current hypothesis:
- HIGH (roughly >=90%): proceed only if evidence gates pass
- MEDIUM (roughly 70-89%): add targeted inspection or an independent reviewer before committing to a broad change
- LOW (<70%): re-investigate before implementation; do not compensate with repeated random patches

Material disagreement between independent agents is itself an escalation signal. Reconcile from repository evidence; if still unresolved, use the strongest available reasoning capability justified by the task.

## 13. Evidence gates

An agent saying "done" is not evidence. A work unit passes only when acceptance criteria are supported by appropriate evidence such as:
- targeted tests
- broader regression tests when justified
- build/type/lint results
- reproduction no longer failing
- inspected runtime/output behavior
- schema/contract/invariant validation
- final diff review

For substantial work, the orchestrator must inspect the actual resulting diff.

## 14. Independent-review principle

Whenever practical:
`AUTHOR != PRIMARY_REVIEWER`

Prefer separation of both role and model family when available. Reviewers must not modify the repository during their review role.

## 15. Finding gate

Unresolved CRITICAL findings block completion.

Unresolved HIGH findings normally block completion unless evidence demonstrates the finding is invalid, mitigated, impossible, or the user explicitly accepts the risk. Record the rationale.

## 16. Change discipline

Do not perform unrelated refactors, redesign working UI unless asked, silently remove functionality, weaken security for convenience, introduce dependencies without justification, leave debug artifacts/secrets, or break compatibility unnecessarily.

## 17. Final response

For substantial work summarize:

### Result
What changed and whether the objective is met.

### Key decisions
Important choices and why.

### Review findings
Material advisor/specialist findings and disposition.

### Changes
Main components/files changed.

### Verification
Tests/checks and outcomes.

### Remaining risks
Only genuine unresolved risks.

Do not dump internal agent transcripts or every shell command.
