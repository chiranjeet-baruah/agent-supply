# AgentSupply v0 design

## Purpose

AgentSupply is a public, curated GitHub catalog of useful agent extensions. The first release serves developers who want inspectable, portable engineering skills. Success means a visitor can find a skill, inspect its instructions and license, install it using their agent's documented mechanism, and see exactly what the repository has validated.

## Scope and architecture

The first release contains two first-party, instruction-only Agent Skills: `go-code-review` and `postgres-query-review`. Their `SKILL.md` files follow the Agent Skills specification. `registry/catalog.json` is the sole source for listing metadata. `CATALOG.md` is generated from it. There is no application server, package manager, account system, or marketplace ranking.

The registry uses `schema_version: 1` and one entry per skill. Each entry has an ID, title, summary, category, path, version, and license. The initial validator accepts a deliberately narrow authoring profile: `SKILL.md` plus Markdown files in `references/`, plain one-line frontmatter fields (`name`, `description`, `license`), an unquoted plain-text description, and no symlinks, scripts, binaries, or nested resource directories. This is a repository policy, not a claim that the Agent Skills specification forbids richer skills.

The Python standard library validator checks registry shape, unique IDs, safe paths, metadata agreement, permitted files, and generated catalog freshness. GitHub Actions runs validation and unit tests on pull requests and pushes to `main`. It does not execute submitted skill content. Publication requires maintainer review; passing CI means structural checks passed, not that a skill is safe or works on every agent.

## Distribution and compatibility

Users can browse and copy a skill folder into the location documented by their agent harness. The catalog does not claim tested compatibility with any harness or model. A later release can add test evidence per harness and separate artifact types for plugins and MCP servers. No vendor-specific marketplace manifest is generated in v0.

## Review and failure behavior

Invalid or unlisted skills fail validation with actionable file-specific errors. A stale generated catalog fails CI and can be repaired with `python3 tooling/validate.py --write-catalog`. Contributions must declare provenance and redistribution rights. Security reports use GitHub private vulnerability reporting where available; public issues should contain no exploit details.

## Alternatives rejected for v0

- A searchable website would add hosting and synchronization work before catalog quality is established.
- A universal installer would imply compatibility the project has not tested.
- Executable skills and plugins would materially increase the review burden without proving demand.

## References

- Agent Skills specification: https://agentskills.io/specification
- OpenAI plugin packaging: https://developers.openai.com/plugins/build/plugins
