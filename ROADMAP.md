# Roadmap

Adaptive Orchestrator is a public beta. The roadmap prioritizes correctness, portability, and observability over adding more agents.

## Near term

- validate installation and skill discovery across multiple Claude Code environments
- collect examples of T0-T3 classification quality
- refine FAST/AUTO/STRICT behavior from real usage
- improve compatibility diagnostics for restricted model allowlists
- expand validation around unsupported frontmatter/tool combinations
- document more real task examples and expected orchestration traces

## Candidate improvements

- optional machine-readable orchestration summary for CI/log analysis
- lightweight telemetry hooks that remain local unless users explicitly integrate them
- configurable per-project policy overrides without mutating the plugin core
- additional specialist reviewers only where there is a clear, general-purpose use case
- richer regression fixtures for plugin manifests and agent contracts
- release automation once the beta stabilizes

## Non-goals

The project does not aim to:

- maximize agent count
- hard-code model version numbers
- replace project-specific CLAUDE.md rules
- replace qualified security, legal, financial, medical, or other professional review where required
- silently auto-approve unresolved critical findings
- become a general collection of unrelated prompts

## Stability target

A future stable release should demonstrate:

- reliable plugin installation
- predictable model fallback
- bounded cost/turn behavior
- independent reviewer enforcement
- worktree isolation behaving as intended
- validation passing across supported manifest changes
- documented results from representative low-, medium-, and high-risk engineering tasks
