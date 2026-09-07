## Summary

Describe the change and the problem it solves.

## Why this belongs in the plugin

Explain why the behavior is general-purpose rather than project-specific.

## Affected components

- [ ] plugin/marketplace metadata
- [ ] orchestrator skill
- [ ] review/audit skills
- [ ] agents
- [ ] validation/CI
- [ ] documentation

## Verification

List the checks you ran and their results.

- [ ] `python scripts/validate.py`
- [ ] `claude plugin validate .` (when Claude CLI is available)
- [ ] relevant manual Claude Code behavior checked

## Safety and compatibility

- [ ] model aliases remain future-oriented; no dated model IDs added
- [ ] reviewer/explorer write restrictions remain intact
- [ ] agent turn/effort budgets remain bounded
- [ ] no critical review gate was weakened
- [ ] installation path and marketplace metadata remain valid

## Remaining risks

List genuine unresolved risks or write `None`.
