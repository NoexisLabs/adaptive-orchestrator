# Changelog

## 0.2.0 - 2026-09-07

- Restored explicit Claude Code model-family aliases with native `availableModels` substitution/fallback
- Added FAST / AUTO / STRICT operating modes
- Added per-agent `effort` and `maxTurns` budgets
- Added request-level agent and concurrency budgets
- Made advisor, security auditor, domain auditor, and repository explorer technically read-only
- Added worktree-isolated implementation agent for safe parallel writers
- Added confidence-based escalation and stronger root-cause re-planning rules
- Formalized delegated task packets and worker return contracts
- Added dedicated read-only `review` and `audit` skills
- Added orchestration protocol documentation
- Added repository validation CI and version consistency checks

## 0.1.0 - 2026-09-07

- Initial plugin structure
- Added risk/complexity tiers T0-T3
- Added model-class routing policy
- Added orchestrator, advisor, domain-logic, security, implementation, testing, and exploration agents
- Added evidence gates, retry budget, root-cause re-planning, and independent-review policy
- Added marketplace metadata for GitHub distribution
