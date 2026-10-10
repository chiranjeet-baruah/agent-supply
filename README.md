# AgentSupply

Choose a skill in the [catalog](CATALOG.md), read its instructions, then install it with Codex or Claude Code. AgentSupply currently has two engineering skills. Each contains instructions, with no bundled scripts or MCP server.

## Install through a marketplace

Choose a skill from the [catalog](CATALOG.md). Add this repository as a marketplace, then install it.

**Codex CLI:**

```sh
codex plugin marketplace add chiranjeet-baruah/agent-supply
codex plugin add go-code-review@agent-supply
```

**Claude Code:**

```sh
claude plugin marketplace add chiranjeet-baruah/agent-supply
claude plugin install go-code-review@agent-supply
```

To install the other skill, replace `go-code-review` with `postgres-query-review`.

When this repository is open in the ChatGPT desktop app, **AgentSupply** can also appear in its Plugins Directory. Adding this repository does not list it in OpenAI's or Anthropic's public plugin directories.

Claude Code leaves auto-update off for a new marketplace. To receive later skill versions, enable auto-update for **agent-supply** in `/plugin`. You can also update manually with `claude plugin marketplace update agent-supply` and `claude plugin update go-code-review@agent-supply`. See [Claude's hosting guide](https://code.claude.com/docs/en/plugins/host-marketplace) and [OpenAI's plugin packaging guide](https://developers.openai.com/plugins/build/plugins) for client behavior.

## Install a skill manually

1. Open a skill in the [catalog](CATALOG.md). Read its `SKILL.md` and license.
2. Copy the full `skills/<name>/` folder to the skill location documented by your agent. Keep the folder name and `SKILL.md`.
3. Refresh or restart the agent if its instructions require it. Try a task that matches the skill's description.

The [Agent Skills specification](https://agentskills.io/specification) defines the skill format. Claude Code's marketplace manifest has been validated locally. CI checks that both marketplace packages match the reviewed skills. Skill behavior has not been evaluated across products or models.

## Check a contribution

From the project root, run these commands in order. The first two regenerate the catalog and marketplace packages; the remaining three check the generated files and run tests.

```sh
python3 tooling/validate.py --write-catalog
python3 -m tooling.package_plugins --write
python3 tooling/validate.py
python3 -m tooling.package_plugins
python3 -m unittest discover -s tests
```

The validators check [`registry/catalog.json`](registry/catalog.json), skill metadata, file layout, symlinks, catalog freshness, and whether marketplace packages match the reviewed skill files byte for byte. They need Python 3.10 or newer and no third-party packages.

CI scans every skill with [NVIDIA SkillSpector](https://github.com/NVIDIA/skillspector). Its `skillspector` job uses Python 3.12 and a pinned upstream revision. Findings or incomplete coverage fail the scan. Both `validate` and `skillspector` must pass before merge. The exact commands are in [the workflow](.github/workflows/validate.yml).

These checks read skill files without running them. They do not prove that a skill is safe or works in a particular agent.

Dependabot proposes weekly updates to CI's GitHub Actions and locked Python packages. The `skillspector` job audits those packages for known vulnerabilities before installation. Dependency update PRs need the same checks and review as other changes. See the [maintainer checklist](docs/MAINTAINER_SETUP.md) for coverage and limits.

## Releases

After both checks pass on `main`, CI publishes the next patch version as a [GitHub release](https://github.com/chiranjeet-baruah/agent-supply/releases). Each release points to the checked commit and uses generated notes. See the [maintainer checklist](docs/MAINTAINER_SETUP.md) for recovery steps.

## Contribute or report an issue

Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing a skill. Current submissions must be original, instruction-only skills with optional Markdown references. A maintainer reviews the purpose, source, behavior, and risks.

Report vulnerabilities through [SECURITY.md](SECURITY.md). [GOVERNANCE.md](GOVERNANCE.md) explains publication decisions.

## License

Original AgentSupply content and tooling use the [Apache License 2.0](LICENSE). A future third-party listing would keep its own license and attribution; appearing in the catalog would not relicense it.
