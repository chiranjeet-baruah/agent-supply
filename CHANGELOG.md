# Changelog

For releases after `v0.1.0`, see [GitHub Releases](https://github.com/chiranjeet-baruah/agent-supply/releases). CI generates release notes for every merge to `main`.

## Changes since 0.1.0

- Added the Minimalist Engineer skill for focused code changes and simplicity reviews.
- Added installable Codex and Claude Code repository marketplaces, with CI checks that packaged skills match their reviewed sources.
- Required SkillSpector static scans and the existing validator to pass before merging to `main`.
- Updated the contributor, security, and maintainer documentation to reflect the current workflow.
- Added automatic patch releases after both checks pass on `main`.
- Added weekly Dependabot updates for CI dependencies, locked SkillSpector's Python packages, audited them in CI, and updated the pinned checkout action.

## 0.1.0

- Added Go code review and PostgreSQL query review skills.
- Added a registry-backed catalog, structural validator, and CI checks.
- Added contribution, governance, and security reporting guidance.
