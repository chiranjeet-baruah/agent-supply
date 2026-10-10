# Maintainer checklist

Review each pull request before merging. The repository ruleset requires both `validate` and `skillspector` to pass, but CI does not replace reading the changed skill.

## Review a pull request

1. Read changed instructions and references. Check the skill's source, license, authority, and likely failure modes.
2. Confirm the `validate` and `skillspector` status checks pass on the current pull request commit. Review any scanner finding before changing the skill or the scan policy.
3. Merge through the pull request. GitHub deletes the merged branch automatically. No second-person approval is required while there is only one active maintainer.

## Publish a release

1. Verify the catalog and checks on `main`. Update `CHANGELOG.md` for the version being released.
2. Check that the private reporting link in `SECURITY.md` works and that any new compatibility claim has test evidence.
3. Create the release from the verified `main` commit. Use the changelog for the release notes.

The v0.1.0 release is complete. The [original design](superpowers/specs/2026-10-10-agent-supply-v0-design.md) and [implementation plan](superpowers/plans/2026-10-10-agent-supply-v0.md) record that work.

## Repository settings

Checked on 2026-10-10: `chiranjeet-baruah/agent-supply` is public. The active `Protect main` ruleset requires a pull request and both status checks, uses strict checks, and blocks force pushes and deletion. Automatic deletion of merged branches, secret scanning, push protection, dependency alerts, and private vulnerability reporting are enabled. Recheck these settings before a release; a local clone cannot verify live GitHub settings.

Static scans do not establish that a skill is safe or works with every agent.

GitHub reference: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository
