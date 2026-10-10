# Contributing

AgentSupply v0 is a small, manually curated catalog. Propose a skill with an issue before writing a large submission. Explain the task it solves, intended users, why an existing skill is insufficient, expected inputs and outputs, and any permissions it would need.

## Current submission profile

- One purpose per skill in `skills/<name>/SKILL.md`, with a lowercase, hyphenated directory name matching the frontmatter `name`.
- Plain, single-line `name`, `description`, and `license` frontmatter fields. Use an unquoted description that says what the skill does and when to use it; quote syntax and YAML block scalars are outside the current validator profile.
- `license: Apache-2.0` for original first-party content. Include only work you have rights to contribute. Do not copy third-party prompts or documentation without permission and attribution.
- Optional Markdown files directly under `references/`. The current validator rejects scripts, binaries, symlinks, nested resource folders, and external artifact sources. Propose richer formats as a separate design change.
- No credentials, personal data, undisclosed network destinations, hidden tool instructions, or claims of cross-agent compatibility without test evidence.

Add a matching record to `registry/catalog.json`. Keep the ID and path stable. Increase the version when changing published skill behavior; explain meaningful changes in the pull request.

Run:

```sh
python3 tooling/validate.py --write-catalog
python3 tooling/validate.py
python3 -m unittest discover -s tests
```

## Review

CI checks structure only. A maintainer reviews the instructions, intended authority, provenance, license, references, and likely failure modes. Reviewers may request task examples or evaluation evidence. A merged skill is a curated listing, not a safety guarantee. See [GOVERNANCE.md](GOVERNANCE.md) for publication decisions.
