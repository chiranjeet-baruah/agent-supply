# Maintainer release process

As checked on 2026-10-10, `chiranjeet-baruah/agent-supply` is public. Its `Protect main` ruleset requires a pull request and the `validate` status check, and blocks force pushes and deletion. Secret scanning, push protection, dependency alerts, and private vulnerability reporting are enabled. Check these live settings again before later releases; a local clone cannot prove their current state.

For the first release:

1. Review the open pull request and confirm its `Validate catalog` workflow passes. The status check job is named `validate`.
2. Merge through the pull request. No second-person approval is required while there is only one active maintainer.
3. Recheck the catalog on `main`, then create the `v0.1.0` release from that commit with notes based on `CHANGELOG.md`.

For later releases, verify that the security reporting link in `SECURITY.md` remains available and that any new compatibility claims have actual test evidence. The ruleset is a governance control; CI is a structural check. Neither establishes that the skills are safe or compatible with every agent.

GitHub reference: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository
