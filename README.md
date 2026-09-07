# Adaptive Orchestrator for Claude Code

A reusable Claude Code plugin for **risk-aware multi-agent engineering**.

It adds a lightweight-to-rigorous orchestration system that scales with task complexity instead of invoking a large agent hierarchy for every change.

## What it adds

- Complexity tiers: T0 trivial, T1 standard, T2 complex, T3 critical/specialist
- Model-class routing: Fable / Opus / Sonnet / Haiku by role
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

- cheap models for mechanical discovery
- normal coding models for implementation
- stronger independent models for judgment and audit
- explicit evidence before completion
- escalation only when complexity warrants it

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

## Model classes

The policy is deliberately future-oriented:

| Role | Preferred class |
|---|---|
| Orchestrator | Fable |
| Advisor | Opus |
| Domain Logic Auditor | Fable |
| Security Auditor | Opus |
| Backend / Frontend / Test | Sonnet |
| Repository Explorer | Haiku |

Claude Code agent manifests currently accept model selectors such as `opus`, `sonnet`, `haiku`, or `inherit`. Where a Fable alias is not available in the agent manifest schema, this plugin uses `inherit` and instructs the orchestrator/domain auditor to prefer Fable when the runtime can select it. This avoids pinning dated model IDs.

## Evidence gates

An agent saying "done" is not evidence. Depending on the task, completion should be supported by tests, builds, type/lint checks, targeted reproduction, schema/contract validation, output inspection, and final diff review.

## Retry policy

Per work unit, prefer:

1. one normal implementation attempt
2. one evidence-driven correction attempt
3. if still failing, return to orchestration for root-cause re-planning or model escalation

Repeatedly applying variants of the same failed hypothesis is explicitly discouraged.

## Worktree isolation

For parallel writing agents, prefer isolated Git worktrees or equivalent branches where supported. Do not let independent agents concurrently edit overlapping files without a merge plan.

## Scope and persistence

Plugins installed at user scope are available across projects. Project-specific architecture, commands, domain rules, and coding conventions should stay in each project's own configuration; this plugin supplies the general engineering operating model.

## License

MIT
