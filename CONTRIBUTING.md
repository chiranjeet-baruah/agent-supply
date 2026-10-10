# Contributing

Before writing a large submission, open a [skill proposal issue](.github/ISSUE_TEMPLATE/skill-proposal.md). Include the task, intended users, inputs and outputs, needed permissions, and why an existing skill does not cover it.

## Add a skill

1. Put one purpose in `skills/<name>/SKILL.md`. Use a lowercase, hyphenated folder name that matches its frontmatter `name`.
2. Add plain, single-line `name`, `description`, and `license` fields. Write an unquoted description that says what the skill does and when to use it. The validator rejects quoted values and YAML block scalars.
3. Add optional Markdown references directly under `references/`. The current profile does not accept scripts, binaries, symlinks, nested folders, or external artifact sources.
4. Add a record to `registry/catalog.json`. Keep existing IDs and paths stable. Raise a published skill's version when its packaged content changes, and explain the change in the pull request.
5. Regenerate `CATALOG.md` and the Codex and Claude marketplace packages. The files under `plugins/` are generated copies; edit the skill under `skills/` instead.

Use `license: Apache-2.0` for original first-party work. Share only material you have rights to use; third-party prompts or documentation need permission and attribution. Keep credentials, personal data, hidden tool instructions, and undisclosed network destinations out of submissions. Provide test evidence for agent compatibility claims.

## Run the checks

```sh
python3 tooling/validate.py --write-catalog
python3 -m tooling.package_plugins --write
python3 tooling/validate.py
python3 -m tooling.package_plugins
python3 -m unittest discover -s tests
```

CI runs a static SkillSpector scan on every skill. A finding, an incomplete scan, or coverage below 100% blocks the pull request. With `skillspector` installed, check one skill locally with:

```sh
skillspector scan skills/go-code-review --no-llm --fail-on-findings --fail-on-incomplete --min-coverage 100
```

The [CI workflow](.github/workflows/validate.yml) pins the scanner revision. There is no suppression baseline; findings must be reviewed and resolved before merge.

## Review and merge

A maintainer reads the instructions and references, checks the source and license, and considers likely failure modes. They may ask for task examples or evaluation evidence. Passing CI does not guarantee safety or compatibility. See [GOVERNANCE.md](GOVERNANCE.md) for publication decisions.
