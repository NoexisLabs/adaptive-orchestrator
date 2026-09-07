# Security Policy

Adaptive Orchestrator influences how Claude Code delegates, reviews, and verifies engineering work. Security reports that could cause unsafe repository modification, privilege-boundary bypass, reviewer write access, secret exposure, or misleading completion should be treated carefully.

## Supported versions

Security fixes are applied to the latest version on `main`. Older versions may not receive backports during the public beta.

## Reporting a vulnerability

Please do **not** publish a detailed exploit or sensitive proof of concept in a public issue.

Use GitHub's private vulnerability reporting / security advisory mechanism for this repository when available. Include:

- affected file or agent/skill
- expected security boundary
- observed behavior
- reproduction steps
- likely impact
- suggested mitigation, if known

If private reporting is not available, open a minimal public issue requesting a private security contact without including exploit details.

## Security boundaries

The plugin is designed to preserve these principles:

- reviewers and explorers should not have normal write tools
- CRITICAL findings block completion
- HIGH findings normally block completion unless disproven, mitigated, impossible, or explicitly accepted
- security-sensitive T3 work requires specialist review
- secrets and credentials must not be introduced into prompts, logs, committed files, or debugging artifacts
- evidence and repository state outrank agent confidence

## Scope

Reports are especially relevant when they involve:

- authentication or authorization bypass in the orchestration policy
- unintended reviewer write capability
- unsafe tool permissions
- worktree or branch isolation failures caused by plugin configuration
- secret leakage
- model-routing behavior that silently removes required security review
- validation gaps that permit malformed or unsafe plugin manifests

The plugin cannot guarantee the security of the user's codebase, Claude Code runtime, third-party tools, external MCP servers, or the models themselves.
