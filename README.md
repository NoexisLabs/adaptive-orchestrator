# Adaptive Orchestrator for Claude Code

A reusable Claude Code plugin for **risk-aware multi-agent engineering**.

It adds a lightweight-to-rigorous orchestration system that scales with task complexity instead of invoking a large agent hierarchy for every change.

## What it adds

- Complexity tiers: T0 trivial, T1 standard, T2 complex, T3 critical/specialist
- Capability-based model routing with graceful fallbacks
- Independent Advisor review
- Domain Logic Auditor for specialized high-consequence logic
- Security Auditor
- Backend, frontend, test, and repository-explorer agents
- Evidence-based completion gates
- Retry budgets and root-cause re-planning
- Independent author/reviewer separation
- Worktree/branch isolation guidance for concurrent writers

## Why

The objective is not "more agents." The objective is **better engineering control**:

- cheap/fast models for mechanical discovery
- strong coding models for implementation
- stronger independent reasoning models for judgment and audit
- explicit evidence before completion
- escalation only when complexity warrants it
- no hard dependency on one specific model family

## Installation from GitHub

```text
/plugin marketplace add NoexisLabs/adaptive-orchestrator
/plugin install adaptive-orchestrator@adaptive-orchestrator-marketplace
```

Claude Code installs plugins at **user scope by default**, making the plugin available across your projects. You can also choose project or local scope from `/plugin`.

## Usage

The skill is discoverable as:

```text
/adaptive-orchestrator:orchestrate
```

Claude may also invoke the skill automatically when its description matches the task.

For a complex request, you can explicitly say:

```text
Use the adaptive orchestrator workflow for this task.
```

## Architecture

```text
                         ORCHESTRATOR
                              |
                        ADVISOR CHALLENGE
                              |
                       REVISED WORK GRAPH
                              |
                +-------------+-------------+
                |             |             |
             BACKEND       FRONTEND       TESTING
                |             |             |
                +-------------+-------------+
                              |
                    SPECIALIST REVIEWERS
                     /                 \
              SECURITY               DOMAIN
                     \                 /
                      +-------+-------+
                              |
                        FINAL REVIEW
                              |
                      COMPLETION GATE
```

The actual path depends on risk. A typo does **not** run the full graph.

## Capability-based model routing

Model names are treated as preferences, not hard dependencies. The plugin first uses what is actually available in the user's Claude Code environment.

| Role | Preferred routing |
|---|---|
| Orchestrator | Fable → Opus → Sonnet → inherit |
| Advisor / Final Reviewer | Opus → Fable → Sonnet → inherit |
| Domain Logic Auditor | Fable → Opus → Sonnet → inherit |
| Security Auditor | Opus → Fable → Sonnet → inherit |
| Backend / Frontend / Test | Sonnet → strongest suitable coding model → inherit |
| Repository Explorer | Haiku → cheapest/fastest suitable model → inherit |

This makes the plugin portable across accounts, organizations, API providers, and future model lineups. If a preferred model is unavailable, orchestration continues with the strongest suitable available fallback rather than failing.

Where Claude Code agent manifests require concrete selectors, agents use supported selectors or `inherit`; the orchestration skill contains the role-level fallback policy.

## Evidence gates

An agent saying "done" is not evidence. Depending on the task, completion should be supported by tests, builds, type/lint checks, targeted reproduction, schema/contract validation, output inspection, and final diff review.

## Retry policy

Per work unit, prefer:

1. one normal implementation attempt
2. one evidence-driven correction attempt
3. if still failing, return to orchestration for root-cause re-planning or capability escalation

Repeatedly applying variants of the same failed hypothesis is explicitly discouraged.

## Worktree isolation

For parallel writing agents, prefer isolated Git worktrees or equivalent branches where supported. Do not let independent agents concurrently edit overlapping files without a merge plan.

## Scope and persistence

Plugins installed at user scope are available across projects. Project-specific architecture, commands, domain rules, and coding conventions should stay in each project's own configuration; this plugin supplies the general engineering operating model.

## License

MIT
