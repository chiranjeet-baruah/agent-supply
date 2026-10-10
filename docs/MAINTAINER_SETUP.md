# Maintainer checklist

Read every changed skill before merging. The repository ruleset requires `validate` and `skillspector` to pass; neither check replaces a human review.

## Marketplace packages

`skills/` and `registry/catalog.json` supply the two marketplace manifests and the installable packages under `plugins/`. After changing a skill or its listing, run:

```sh
python3 tooling/validate.py --write-catalog
python3 -m tooling.package_plugins --write
python3 -m tooling.package_plugins
```

The required `validate` job checks that packaged skills match their reviewed sources and that generated locations have no extra files. Run `claude plugin validate .` locally to check Claude's marketplace schema.

Package versions come from each skill's registry version, separately from the repository release tag. Raise the affected skill's version whenever its packaged content changes. Claude Code keeps a cached copy when the plugin version stays the same. Auto-update is off by default for a new Claude marketplace. Test an installation in each client before claiming runtime compatibility.

Host the marketplace in Git. Claude Code clones the repository to resolve its relative plugin paths. Adding only the raw `marketplace.json` URL leaves those paths unavailable. See [Claude's hosting guide](https://code.claude.com/docs/en/plugins/host-marketplace).

## Review a pull request

1. Read changed instructions and references. Check the skill's source, license, authority, and likely failure modes.
2. Confirm the `validate` and `skillspector` status checks pass on the current pull request commit. Review any scanner finding before changing the skill or the scan policy.
3. Merge through the pull request. GitHub deletes the merged branch automatically. No second-person approval is required while there is only one active maintainer.

## Releases

Every push to `main` runs both checks again. If they pass, CI creates the next patch tag and a GitHub release at that commit. Release notes are generated from the previous release. For example, the first automated release after `v0.1.0` is `v0.1.1`.

After merging, check the release job and published tag. If the job fails, inspect its log, fix the cause, and rerun it. A rerun skips a commit that already has a release. Create a new minor or major version deliberately; later merges continue with patch versions from it.

The v0.1.0 release is complete. The [original design](superpowers/specs/2026-10-10-agent-supply-v0-design.md) and [implementation plan](superpowers/plans/2026-10-10-agent-supply-v0.md) record that work.

## Dependency updates

Dependabot checks GitHub Actions and the locked CI Python environment weekly. Review its PRs and run the existing checks before merging. Each merge publishes a patch release. Dependabot alerts and security update PRs are enabled in repository settings. Do not auto-merge dependency updates.

SkillSpector is installed from a reviewed upstream commit recorded in `pyproject.toml`. `uv.lock` fixes Python dependency versions and artifact hashes. The required `skillspector` job audits the lock before installing it and runs every Monday, so a new advisory can fail a scheduled run.

Dependabot updates registry packages, but not SkillSpector's Git commit. To update that commit, check upstream releases and advisories, edit `pyproject.toml`, regenerate `uv.lock` with `uv lock`, and submit a PR that passes both checks.

The setup-uv Action is tracked by Dependabot; its `version` input pins the uv binary separately. Review new uv releases and update that input through a checked PR. Keep the binary pinned so CI does not change between reviews.

## Repository settings

Checked on 2026-10-10: `chiranjeet-baruah/agent-supply` is public. The active `Protect main` ruleset requires a pull request and both status checks, uses strict checks, and blocks force pushes and deletion.

Automatic deletion of merged branches, secret scanning, push protection, Dependabot alerts and security updates, and private vulnerability reporting were enabled at that check. Verify these settings in GitHub; a local clone cannot show their current state.

Static scans do not establish that a skill is safe or works with every agent.

GitHub reference: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository
