# Maintainer setup for the first GitHub release

The working tree is release-ready only after the following remote checks are completed. Repository visibility and security settings cannot be inferred from the local Git remote.

1. Publish the reviewed changes to `chiranjeet-baruah/agent-supply` through a pull request. Confirm the repository description matches the current README and that visibility is **Public** if the open catalog is intended to be discoverable.
2. Confirm the `Validate catalog` workflow passes on the pull request. The status check job is named `validate`.
3. Add a rule for `main` that requires a pull request and the `validate` status check, and blocks force pushes and deletion. GitHub requires a status check to have run before selecting it as required. Do not require a second person's approval while there is only one active maintainer.
4. Enable private vulnerability reporting and secret scanning where the repository's GitHub settings offer them. Check that the private reporting link in `SECURITY.md` works.
5. After merging and rechecking the catalog on `main`, create the `v0.1.0` release from that commit with notes based on `CHANGELOG.md`.

The ruleset is a governance control. CI is a structural check. Neither establishes that the skills are safe or compatible with every agent.

GitHub reference: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository
