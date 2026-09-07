# Adaptive Orchestrator for Claude Code

A reusable Claude Code plugin for **risk-aware multi-agent engineering**.

Adaptive Orchestrator scales from direct execution to independent multi-agent review depending on task complexity and risk. It combines model-family routing, bounded agent budgets, read-only reviewers, evidence gates, retry limits, specialist audits, and worktree isolation.

## What it adds

- Complexity tiers: T0 trivial, T1 standard, T2 complex, T3 critical/specialist
- Operating modes: **FAST / AUTO / STRICT**
- Native Claude Code model-family routing with availability fallback
- Independent Advisor review
- Domain Logic Auditor for specialized high-consequence logic
- Security Auditor
- Backend, frontend, test, repository-explorer, and isolated worktree implementation agents
- Explicit `maxTurns` and `effort` budgets
- Request-level agent/concurrency budgets
- Evidence-based completion gates
- Two-attempt retry budget and root-cause re-planning
- Confidence-based escalation
- Independent author/reviewer separation
- Dedicated read-only `review` and `audit` skills
- Worktree isolation for parallel independent writers

## Why

The objective is not "more agents." The objective is **better engineering control**:

- cheaper models for mechanical discovery
- coding-focused models for implementation
- stronger independent models for judgment and audit
- explicit evidence before completion
- bounded retries and agent count
- escalation only when uncertainty or consequence warrants it

The optimization target is **correctness per unit of compute**, not maximum agent activity.

## Installation from GitHub

```text
/plugin marketplace add NoexisLabs/adaptive-orchestrator
/plugin install adaptive-orchestrator@adaptive-orchestrator-marketplace
```

Plugins installed at user scope are available across projects. Project-specific architecture, commands, domain rules, and coding conventions should remain in each project's own configuration.

## User-facing skills

### Orchestrate

```text
/adaptive-orchestrator:orchestrate [fast|auto|strict] <task>
```

Examples:

```text
/adaptive-orchestrator:orchestrate auto Fix the authentication regression
/adaptive-orchestrator:orchestrate strict Refactor the payment authorization flow
/adaptive-orchestrator:orchestrate fast Add the missing null guard and verify it
```

If no mode is supplied, `AUTO` is used.

### Review

```text
/adaptive-orchestrator:review <target or objective>
```

Read-only review of an existing implementation, diff, branch, or PR. It does not implement fixes.

### Audit

```text
/adaptive-orchestrator:audit <scope or objective>
```

Deep read-only architecture, security, domain-logic, data-integrity, reliability, and verification audit. Remediation can then be handed to `orchestrate`.

## Operating modes

| Mode | Goal | Typical behavior |
|---|---|---|
| FAST | Speed / lower cost | minimal agents, targeted verification, mandatory T3 gates retained |
| AUTO | Balanced default | risk-aware routing and independent review where justified |
| STRICT | Maximum assurance | pre-review, stronger author/reviewer separation, specialist gates, broader verification |

## Complexity tiers and default budgets

| Tier | Typical work | Default max subagents |
|---|---|---:|
| T0 | trivial/local | 0 |
| T1 | narrow feature or bug | 2 |
| T2 | cross-cutting/architectural | 4 |
| T3 | critical/security/domain-sensitive | 6 |

Default maximum concurrent subagents: **3**.

## Model routing

The plugin uses Claude Code's model-family aliases rather than dated model IDs:

| Role | Preferred alias | Effort | Max turns |
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

These are **preferences, not hard dependencies**. Claude Code checks requested aliases against the user's `availableModels` allowlist. When an alias is not permitted, Claude Code can substitute an allowed model from that family or fall back to the inherited session model. The plugin therefore retains useful routing without requiring every user to have Fable, Opus, Sonnet, and Haiku access.

## Reviewer independence

The Advisor, Security Auditor, Domain Logic Auditor, and Repository Explorer are technically restricted to:

```text
Read, Grep, Glob
```

They cannot use normal file-writing tools. This reinforces:

```text
AUTHOR != PRIMARY_REVIEWER
```

Implementation agents retain write access.

## Worktree isolation

Adaptive Orchestrator applies this rule:

```text
ONE WRITER
→ normal implementation agent in the current tree

MULTIPLE INDEPENDENT WRITERS
→ isolated-implementer with isolation: worktree

OVERLAPPING FILES
→ serialize or create an explicit merge plan
```

Worktree isolation is not used as a substitute for dependency analysis.

## Retry and escalation policy

Per work unit:

1. one normal implementation attempt
2. one evidence-driven correction attempt
3. after a second meaningful failure, stop and return to orchestration for root-cause re-planning or justified model/effort escalation

Confidence is advisory:

- high (~90%+): proceed only if evidence gates pass
- medium (~70-89%): add targeted inspection or independent review
- low (<70%): re-investigate before implementation
- material disagreement between independent agents: reconcile from repository evidence and escalate if necessary

Tests and observable evidence always override confidence claims.

## Task packets

Every delegated worker receives a bounded packet:

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

See [`docs/PROTOCOL.md`](docs/PROTOCOL.md) for the full coordination contract.

## Evidence gates

An agent saying "done" is not evidence. Depending on the task, completion should be supported by:

- targeted tests
- broader regression checks when justified
- build/type/lint results
- reproduction no longer failing
- inspected runtime/output behavior
- schema validation
- contract/invariant checks
- final diff review

CRITICAL findings block completion. HIGH findings normally block completion unless disproven, mitigated, impossible, or explicitly accepted by the user.

## Architecture

```text
                   USER REQUEST
                        │
                  MODE SELECTION
              FAST / AUTO / STRICT
                        │
                  RISK CLASSIFIER
                  T0 / T1 / T2 / T3
                        │
                   ORCHESTRATOR
                        │
               ┌────────┴────────┐
               │                 │
          EXPLORATION        ADVISOR
               │                 │
               └────────┬────────┘
                        │
                    WORK GRAPH
                        │
           ┌────────────┼────────────┐
           │            │            │
        BACKEND      FRONTEND     ISOLATED
           │            │          WORKTREE
           └────────────┼────────────┘
                        │
                    VERIFY
                        │
              ┌─────────┴─────────┐
              │                   │
          SECURITY             DOMAIN
          if relevant          if relevant
              │                   │
              └─────────┬─────────┘
                        │
              INDEPENDENT REVIEW
                        │
                  EVIDENCE GATE
                        │
                       DONE
```

A typo does **not** run the full graph.

## Validation

The repository includes CI that checks plugin/marketplace version consistency, JSON, agent/skill frontmatter, valid model aliases, required agents/skills, reviewer read-only restrictions, README install commands, and accidental dated model IDs.

When the Claude CLI is available, you can also run:

```bash
claude plugin validate .
```

## Design notes

- [`docs/DESIGN.md`](docs/DESIGN.md)
- [`docs/PROTOCOL.md`](docs/PROTOCOL.md)

## License

MIT
