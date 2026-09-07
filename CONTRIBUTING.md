# Contributing

Contributions are welcome. Adaptive Orchestrator is intentionally small, declarative, and conservative about new complexity.

## Before opening a change

1. Check existing issues and documentation.
2. Keep the plugin general-purpose; project-specific rules should not be added to the reusable core.
3. Prefer model-family aliases over dated model IDs.
4. Preserve reviewer independence and evidence-gated completion.
5. Avoid adding dependencies unless they materially improve validation or portability.

## Development workflow

Fork or branch the repository, make a focused change, then run:

```bash
python scripts/validate.py
```

If Claude Code CLI is installed, also run:

```bash
claude plugin validate .
```

GitHub Actions runs the repository validator automatically on pushes to `main` and on pull requests.

## Pull request expectations

A useful pull request should include:

- the problem being solved
- why the change belongs in the general-purpose plugin
- affected agents/skills/docs
- verification performed
- compatibility or model-routing implications
- any new risk introduced

Keep unrelated refactors out of the same pull request.

## Agent changes

When modifying an agent:

- keep the `name` and `description` explicit
- use only supported model aliases
- set an intentional `effort` level
- set a bounded `maxTurns`
- preserve read-only restrictions for reviewer/explorer roles
- do not weaken independent-review boundaries without strong justification

## Skill changes

Skills should remain evidence-first and should not claim support for behavior that Claude Code cannot actually enforce.

New user-facing skills should have a narrow, clearly distinct purpose.

## Security issues

Do not open public issues for vulnerabilities that could meaningfully weaken users' repositories or Claude Code execution boundaries. Follow `SECURITY.md` instead.
