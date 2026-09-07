# Design Notes

## Principles

1. Scale orchestration to risk.
2. Optimize correctness per unit of compute, not agent count.
3. Keep implementation agents narrowly scoped.
4. Separate authorship from primary review.
5. Treat verification evidence as the completion criterion.
6. Use model-family aliases as preferences and rely on Claude Code's native availability substitution/fallback.
7. Bound agent turns, retries, total agents, and concurrency.
8. Re-plan after repeated failures rather than looping.
9. Isolate concurrent writers with worktrees only when their work is genuinely independent.
10. Keep project-specific domain rules outside the reusable plugin.

## Operating modes

### FAST
Minimize agents and verification breadth while retaining mandatory T3 specialist/evidence gates.

### AUTO
Default adaptive behavior.

### STRICT
Require stronger author/reviewer separation, pre-review/final review for substantial work, relevant specialist gates, and broader regression evidence.

## Complexity routing

### T0
Direct edit and targeted verification. No subagents by default.

### T1
Normal implementation plus verification. Independent review only when risk warrants it.

### T2
Orchestrator, independent advisor, implementation agents, verification, independent final review.

### T3
T2 plus relevant security and/or domain specialist pre/post gates and final completion gate.

## Model portability

Current Claude Code subagent frontmatter supports the family aliases `fable`, `opus`, `sonnet`, `haiku`, plus full model IDs and `inherit`.

Adaptive Orchestrator deliberately uses family aliases rather than dated model IDs:

- Orchestrator: `fable`
- Advisor: `opus`
- Domain Logic Auditor: `fable`
- Security Auditor: `opus`
- Backend/Frontend/Test/Isolated Implementer: `sonnet`
- Repository Explorer: `haiku`

Claude Code checks these against the user's `availableModels` policy. When a requested family alias is blocked, it can substitute an allowed version of the family; when no compatible family version is available, it falls back to the inherited session model. This makes the plugin portable without collapsing all agents to `inherit`.

## Capability boundaries

Reviewers and explorers are technically read-only through their `tools` allowlist:

```text
Read, Grep, Glob
```

This applies to:

- advisor
- security-auditor
- domain-logic-auditor
- repository-explorer

Implementation agents retain write capability. The isolated implementer adds `isolation: worktree` for safe parallel writes.

## Bounded execution

Agents carry explicit `maxTurns` and `effort` values. The orchestrator also applies request-level budgets:

- T0: 0 subagents
- T1: up to 2
- T2: up to 4
- T3: up to 6
- default concurrent maximum: 3

Per work unit, the default retry policy is one normal attempt plus one evidence-driven correction. A second meaningful failure returns control to the orchestrator for root-cause re-planning.

## Worktree policy

One writer uses the normal project tree. Multiple genuinely independent writers may use the `isolated-implementer` agent, which runs with `isolation: worktree`. Work that overlaps the same files or depends on the same mutable state should be serialized instead.

## Confidence and evidence

Confidence is a routing signal, not proof:

- high confidence: continue only if evidence passes
- medium confidence: add targeted inspection or independent review
- low confidence: re-investigate before implementation
- material reviewer disagreement: reconcile from repository evidence and escalate reasoning if needed

Tests, runtime behavior, schema/contract checks, and final diff inspection take precedence over confidence statements.

## User-facing workflows

The plugin exposes:

- `/adaptive-orchestrator:orchestrate` — implementation workflow with FAST/AUTO/STRICT modes
- `/adaptive-orchestrator:review` — read-only review of existing code/diffs/branches/PRs
- `/adaptive-orchestrator:audit` — deep read-only architecture/security/domain/reliability audit

See `PROTOCOL.md` for task packets, budgets, retry rules, and evidence gates.
