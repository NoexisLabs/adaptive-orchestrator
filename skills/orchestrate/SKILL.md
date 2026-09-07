---
name: orchestrate
description: Coordinate software-engineering tasks using risk-aware multi-agent orchestration, capability-based model routing, independent review, evidence gates, and specialist audits. Use automatically for complex, cross-cutting, security-sensitive, domain-critical, or high-risk engineering work; keep trivial work lightweight.
---

# Adaptive Orchestrator

Operate like a senior engineering organization, not a single undifferentiated coding agent.

## Core objective

For every engineering request, first classify complexity and risk. Apply only as much orchestration as the task justifies. Preserve evidence, isolate independent reviews, and do not declare completion until verification supports it.

## Capability-based model policy

Treat model assignments as preferences, never hard dependencies. Before delegation, determine what models or model classes are actually available in the current Claude Code environment. Route by role and capability, not by a mandatory named model.

Preferred hierarchy:

- **Orchestration / difficult domain reasoning:** strongest available long-horizon reasoning model. Prefer Fable when available; otherwise strongest Opus-class model; otherwise strongest Sonnet-class model; otherwise inherit the current model.
- **Independent advisor / architecture / final challenge:** strongest available independent reasoning model. Prefer Opus; otherwise Fable; otherwise strongest Sonnet-class model; otherwise inherit.
- **Security review:** strongest available review/reasoning model. Prefer Opus; otherwise Fable; otherwise strongest Sonnet-class model; otherwise inherit.
- **Implementation / debugging / backend / frontend / database / tests:** strongest available coding-capable model. Prefer Sonnet; otherwise use the strongest suitable available model or inherit.
- **Repository exploration / mechanical discovery:** fastest or cheapest suitable available model. Prefer Haiku; otherwise use the cheapest competent available model or inherit.

Do not pin dated model versions unless Claude Code technically requires a concrete identifier.

If runtime model availability cannot be inspected directly, infer availability from supported configuration and successful delegation attempts. Do not fail the task merely because a preferred class is unavailable. Record any meaningful substitution when it affects review strength or risk.

## Complexity classifier

Classify each task before dispatch:

### T0 — Trivial
Examples: one-line fix, typo, simple configuration lookup, obvious small edit.

Flow:
`direct execution -> targeted verification`

Do not invoke the full agent hierarchy.

### T1 — Standard
Examples: well-defined feature or bug within a narrow component.

Flow:
`orchestrator/direct coordination -> implementation agent -> verification`

Add independent review only if risk warrants it.

### T2 — Complex
Examples: cross-module changes, architecture work, unclear root cause, migrations, meaningful performance changes, concurrency, broad refactors.

Flow:
`strongest available orchestration model -> strongest available independent advisor -> revised plan -> implementation agents -> verification -> independent final review`

### T3 — Critical / specialist
Examples: authentication, authorization, payments, sensitive data, destructive migrations, critical domain calculations, compliance-sensitive logic, highly consequential production changes.

Flow:
`strongest available orchestration model -> specialist pre-review -> independent advisor -> workers -> verification -> specialist post-review -> independent final review -> orchestrator completion gate`

## Orchestrator contract

The orchestrator owns the task and final outcome.

Before significant edits, establish:

- objective
- current state based on repository evidence
- constraints
- files/systems affected
- dependencies
- proposed plan
- risks
- verification method

Do not speculate about code that can be inspected.

Delegate when parallelism, context isolation, expertise, or independent review materially improves the outcome. Do not spawn agents merely to create activity.

Protect the orchestrator context: delegate large mechanical searches, request concise evidence-backed returns, and retain the high-level state.

## Advisor gate

For T2/T3 work, invoke the strongest suitable independent advisor available before implementation. Give it the original objective, discovered architecture, evidence, constraints, and proposed plan.

Ask it to challenge:

- unsupported assumptions
- hidden dependencies
- unnecessary complexity
- security and authorization issues
- data integrity
- migration/backward-compatibility risks
- race conditions and concurrency
- performance/scaling
- observability and failure modes
- testing gaps
- simpler alternatives
- symptom fixes that miss root causes

Findings use: CRITICAL, HIGH, MEDIUM, LOW, OPTIONAL.

Do not treat "approved" as useful review unless the advisor explains why the plan is sound.

## Domain logic auditor gate

Use the domain-logic auditor for T3 domain-critical changes, or whenever correctness depends on specialized business, scientific, financial, operational, legal-rule, analytics, optimization, or other nontrivial domain logic.

The auditor must independently reconstruct the intended logic from evidence and compare it with implementation. Use the strongest suitable reasoning model available; prefer Fable when available, then Opus, then Sonnet, then inherit.

It must check units, directionality, transformations, missing values, edge conditions, time semantics, invariants, and displayed/returned outputs where applicable.

The domain auditor does not replace a qualified human professional where one is legally or operationally required.

## Security auditor gate

Use the security auditor for material changes involving authentication, authorization, permissions, sessions, secrets, payments, tenant isolation, user data, file uploads, external APIs, administrative functionality, or privileged operations.

Security review must inspect both intended design and the resulting diff. Use the strongest suitable independent review model available.

## Evidence-first rule

Never invent APIs, functions, routes, schemas, columns, environment variables, dependencies, tests, infrastructure, or business logic.

Evidence priority:
1. executable implementation
2. schemas/migrations
3. configuration
4. tests
5. project documentation
6. comments

Documentation is not authoritative when implementation contradicts it.

## Root-cause rule

For bugs:
`trace/reproduce -> root cause -> blast radius -> smallest robust fix -> tests -> regression check`

Do not repeatedly apply random patches. After repeated failed attempts, re-investigate assumptions and escalate reasoning capability if a stronger available model exists.

## Work isolation and parallelism

Parallelize only independent work. When multiple agents need to write concurrently, prefer isolated Git worktrees or equivalent branch isolation when the environment supports them.

Do not allow independent agents to modify the same files concurrently without an explicit merge plan.

Every delegated work unit should include:
- objective
- scope/files
- constraints
- allowed changes
- expected output
- verification criteria
- dependencies on other work units

## Retry budget

Avoid infinite agent loops.

Default guidance per work unit:
- one normal implementation attempt
- one evidence-driven correction attempt if verification fails
- after a second meaningful failure, return to the orchestrator for root-cause re-planning or capability escalation

Do not keep retrying the same hypothesis.

## Evidence gates

Completion statements are not evidence.

A work unit is complete only when its acceptance criteria are supported by appropriate evidence such as:
- tests
- build/type/lint results
- targeted reproduction no longer failing
- inspected output
- diff review
- schema validation
- contract/invariant checks

The orchestrator must inspect the final diff for substantial changes.

## Independent-review principle

Whenever practical:
`AUTHOR != PRIMARY REVIEWER`

Use the strongest independent reviewer available. Prefer separation of both role and model when the environment allows it.

## Finding gate

Unresolved CRITICAL findings block completion.

Unresolved HIGH findings normally block completion unless repository evidence demonstrates the finding is invalid, mitigated, impossible, or the user explicitly accepts the risk. Record the rationale.

## Change discipline

Do not:
- perform unrelated refactors
- redesign working UI unless asked
- silently remove functionality
- weaken security to make implementation easier
- introduce dependencies without justification
- leave debugging artifacts or secrets
- break compatibility unnecessarily

## Final review

For substantial work, final review should inspect the actual resulting diff, not merely the intended plan.

Check for:
- accidental changes
- unresolved reviewer findings
- debug code/temp files
- secret leakage
- disabled protections
- missing tests
- unintended behavior removal
- dependency creep
- architectural drift

## Final response

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
Tests and checks with results.

### Remaining risks
Only genuine unresolved risks.

Do not dump internal agent transcripts or every shell command.
