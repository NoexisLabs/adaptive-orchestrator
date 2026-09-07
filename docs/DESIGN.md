# Design Notes

## Principles

1. Scale orchestration to risk.
2. Keep implementation agents narrowly scoped.
3. Separate authorship from primary review.
4. Treat verification evidence as the completion criterion.
5. Escalate models when reasoning difficulty warrants it.
6. Re-plan after repeated failures rather than looping.
7. Isolate concurrent writers.
8. Keep domain-specific project rules outside the reusable plugin.

## Complexity routing

### T0
Direct edit and targeted verification.

### T1
Normal implementation agent plus verification.

### T2
Orchestrator, independent advisor, implementation agents, verification, final review.

### T3
T2 plus security and/or domain specialist pre/post gates.

## Model portability

Claude Code's documented subagent model field supports aliases including `opus`, `sonnet`, `haiku`, and `inherit`. Because this plugin is intended to remain future-proof and Fable-class alias support may differ by Claude Code release, Fable-preferred agents use `inherit` in their manifests and carry an explicit class preference in their instructions. The runtime/orchestrating session should use the strongest available Fable-class model when desired.
