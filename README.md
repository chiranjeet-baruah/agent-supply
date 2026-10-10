# AgentSupply

A curated, open-source catalog of AI agent skills. The first release focuses on two inspectable, instruction-only engineering skills. Plugins and MCP servers are possible later additions; this repository does not claim to install or verify them today.

## Browse

See the [skills catalog](CATALOG.md) and read a skill's `SKILL.md` before installing it. Each entry links to its source. The catalog is generated from [`registry/catalog.json`](registry/catalog.json).

## Install a skill

1. Choose a skill in the [catalog](CATALOG.md) and inspect its instructions and license.
2. Copy its entire `skills/<name>/` directory into the skills location documented by your agent harness, preserving the folder name and `SKILL.md`.
3. Restart or refresh the agent if its documentation requires it, then try a task matching the skill description.

The [Agent Skills specification](https://agentskills.io/specification) defines the portable skill format. Harnesses differ in discovery paths and activation behavior. AgentSupply has not yet published harness-specific test results, so installation in one product should not be treated as proof of compatibility in another.

## What validation means

`python3 tooling/validate.py` checks the v0 registry, skill metadata, allowed file layout, symlinks, and whether `CATALOG.md` is current. CI also runs [NVIDIA SkillSpector](https://github.com/NVIDIA/skillspector) static scans on every skill directory. Scans fail on findings or incomplete analysis. These checks read files but do not run skill content. Passing them is **not** a security certification or a behavioral compatibility certification.

To regenerate the catalog after changing [`registry/catalog.json`](registry/catalog.json):

```sh
python3 tooling/validate.py --write-catalog
python3 tooling/validate.py
python3 -m unittest discover -s tests
```

The repository validator requires Python 3.10 or newer and has no third-party dependencies. The separate SkillSpector CI job uses Python 3.12 and a pinned upstream revision; its scan policy is in [the workflow](.github/workflows/validate.yml).

## Contribute and report issues

Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing a skill. The first release accepts only original, instruction-only skills with Markdown references. Maintainers review purpose, provenance, behavior, and risks in addition to CI results.

For a vulnerability, follow [SECURITY.md](SECURITY.md). Governance and publication decisions are described in [GOVERNANCE.md](GOVERNANCE.md).

## License

Original AgentSupply content and tooling are licensed under [Apache License 2.0](LICENSE). Future third-party listings or artifacts must retain their own license and attribution; inclusion in the catalog does not relicense them.
