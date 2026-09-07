# Quickstart

## 1. Install the marketplace

In Claude Code:

```text
/plugin marketplace add NoexisLabs/adaptive-orchestrator
```

## 2. Install the plugin

```text
/plugin install adaptive-orchestrator@adaptive-orchestrator-marketplace
```

Install at user scope if you want the plugin available across projects.

## 3. Start with AUTO

```text
/adaptive-orchestrator:orchestrate auto Fix the failing API pagination and add regression coverage
```

`AUTO` is the default and is appropriate for most engineering work.

## Choose a mode

### FAST

Use when the task is narrow, low-risk, and speed matters.

```text
/adaptive-orchestrator:orchestrate fast Add a null guard to this parser and verify the existing tests
```

FAST does not disable mandatory safety gates for critical work.

### AUTO

Use for normal day-to-day work.

```text
/adaptive-orchestrator:orchestrate auto Investigate and fix the intermittent cache invalidation bug
```

The orchestrator decides how many agents and review gates are justified.

### STRICT

Use for authentication, payments, migrations, production-critical refactors, or when you explicitly want stronger independent challenge.

```text
/adaptive-orchestrator:orchestrate strict Refactor tenant authorization without changing public API behavior
```

## Review without editing

```text
/adaptive-orchestrator:review Review the current diff for regressions and architectural issues
```

The review workflow is read-only.

## Deep audit

```text
/adaptive-orchestrator:audit Audit authentication, authorization, tenant isolation, and related tests
```

The audit workflow is also read-only and produces findings rather than remediation edits.

## What to expect

Adaptive Orchestrator first classifies the task from T0 to T3. It then selects an appropriate workflow, model family, effort level, and bounded agent budget.

The key rule is that completion requires evidence. A worker saying that a task is complete is not enough.

Typical evidence includes:

- tests
- build/type/lint output
- targeted reproduction
- schema or contract checks
- runtime/output inspection
- independent diff review

## If a preferred model is unavailable

The plugin uses Claude Code model-family aliases. Model assignments are preferences. Claude Code can fall back according to the models available to the user/environment, so lack of access to one preferred family should not prevent the workflow from running.

## Updating

Use Claude Code's plugin management commands/UI to refresh the marketplace and update the installed plugin when a newer version is available.

## Troubleshooting

If installation or discovery fails:

1. Confirm the marketplace was added with the exact repository name.
2. Confirm the plugin name is `adaptive-orchestrator`.
3. Run `claude plugin validate .` from a local clone if the Claude CLI is available.
4. Check the repository's GitHub Actions validation status.
5. Open a bug report with the Claude Code version, environment, installation command, observed output, and expected behavior.
