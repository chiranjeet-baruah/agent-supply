# AgentSupply

Start with the [skills catalog](CATALOG.md). AgentSupply publishes two engineering skills you can read before installing. Each skill contains instructions, with no bundled scripts or MCP server. The catalog does not install or verify plugins or MCP servers.

## Install a skill

1. Open a skill in the [catalog](CATALOG.md). Read its `SKILL.md` and license.
2. Copy the full `skills/<name>/` folder to the skill location documented by your agent. Keep the folder name and `SKILL.md`.
3. Refresh or restart the agent if its instructions require it. Try a task that matches the skill's description.

The [Agent Skills specification](https://agentskills.io/specification) defines the portable format. AgentSupply has not tested these skills across agent products or models. A working install in one product does not establish compatibility elsewhere.

## Check a contribution

Run the repository checks from the project root:

```sh
python3 tooling/validate.py --write-catalog
python3 tooling/validate.py
python3 -m unittest discover -s tests
```

The validator checks [`registry/catalog.json`](registry/catalog.json), skill metadata and file layout, symlinks, and whether `CATALOG.md` is current. It needs Python 3.10 or newer and no third-party packages.

CI also scans every skill with [NVIDIA SkillSpector](https://github.com/NVIDIA/skillspector). Its `skillspector` job uses Python 3.12 and a pinned upstream revision. Static scans fail on findings or incomplete coverage. Both `validate` and `skillspector` must pass before merge. The exact commands are in [the workflow](.github/workflows/validate.yml).

These checks read skill files without running them. They do not prove that a skill is safe or works in a particular agent.

## Contribute or report an issue

Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing a skill. Current submissions must be original, instruction-only skills with optional Markdown references. A maintainer reviews the purpose, source, behavior, and risks.

Report vulnerabilities through [SECURITY.md](SECURITY.md). [GOVERNANCE.md](GOVERNANCE.md) explains publication decisions.

## License

Original AgentSupply content and tooling use the [Apache License 2.0](LICENSE). A future third-party listing would keep its own license and attribution; appearing in the catalog would not relicense it.
