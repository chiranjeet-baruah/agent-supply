# Maintainer checklist

Review each pull request before merging. The repository ruleset requires both `validate` and `skillspector` to pass, but CI does not replace reading the changed skill.

## Review a pull request

1. Read changed instructions and references. Check the skill's source, license, authority, and likely failure modes.
2. Confirm the `validate` and `skillspector` status checks pass on the current pull request commit. Review any scanner finding before changing the skill or the scan policy.
3. Merge through the pull request. GitHub deletes the merged branch automatically. No second-person approval is required while there is only one active maintainer.

## Releases

Every push to `main` runs both checks again. After they pass, CI creates the next patch tag and a GitHub release at that commit. The release notes are generated from the previous release. For example, the first automated release after `v0.1.0` is `v0.1.1`.

Check the release job and the published tag after merging. If the job fails, inspect its log and rerun it after fixing the cause. A rerun skips a commit that already has a release. A new minor or major version needs a deliberate release with that version; later merges continue with patch versions from it.

The v0.1.0 release is complete. The [original design](superpowers/specs/2026-10-10-agent-supply-v0-design.md) and [implementation plan](superpowers/plans/2026-10-10-agent-supply-v0.md) record that work.

## Dependency updates

Dependabot checks GitHub Actions and the locked CI Python environment weekly. Review its PRs and let the existing checks run before merging; each merge publishes a patch release. Dependabot alerts and security update PRs are enabled in repository settings. Do not auto-merge dependency updates.

SkillSpector is installed from a reviewed upstream commit recorded in `pyproject.toml`. `uv.lock` fixes its Python dependency versions and artifact hashes, and the required `skillspector` job audits the lock before installing it. This job also runs every Monday so new advisories can fail a run even without a pull request. Dependabot updates the registry packages. It does not update SkillSpector's Git commit: check upstream releases and advisories, change the commit in `pyproject.toml`, regenerate `uv.lock` with `uv lock`, and use a PR that passes both checks.

## Repository settings

Checked on 2026-10-10: `chiranjeet-baruah/agent-supply` is public. The active `Protect main` ruleset requires a pull request and both status checks, uses strict checks, and blocks force pushes and deletion. Automatic deletion of merged branches, secret scanning, push protection, Dependabot alerts and security updates, and private vulnerability reporting are enabled. A local clone cannot verify live GitHub settings.

Static scans do not establish that a skill is safe or works with every agent.

GitHub reference: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository
