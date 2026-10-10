# Security policy

Report a vulnerability through [GitHub private vulnerability reporting](https://github.com/chiranjeet-baruah/agent-supply/security/advisories/new). If that option is unavailable, open a public issue asking for a private contact channel. Keep exploit details, secrets, and affected user data out of the public issue.

Include the affected skill and version, impact, reproduction steps, and a safe way to contact you. Maintainers triage reports as capacity permits; there is no response-time guarantee.

## Before installing a skill

Read its instructions and give your agent only the permissions it needs. A skill can influence tool use, data access, and code execution in the host agent.

## What the checks cover

The repository validator checks file layout and metadata. CI verifies that the Codex and Claude marketplace packages contain the same skill files as the reviewed source, with no extra package files. CI also runs SkillSpector's static security scan on every skill and audits its locked Python dependencies for known vulnerabilities. These checks do not run a skill, catch every malicious instruction, or test behavior in every agent. Dependency audits cannot detect undisclosed vulnerabilities or prove package safety. The current catalog contains no executable scripts or bundled MCP servers. Maintainers may amend or remove a skill if a material risk is found.
