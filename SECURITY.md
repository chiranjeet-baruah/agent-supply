# Security policy

Report a vulnerability through [GitHub private vulnerability reporting](https://github.com/chiranjeet-baruah/agent-supply/security/advisories/new). If that option is unavailable, open a public issue asking for a private contact channel. Keep exploit details, secrets, and affected user data out of the public issue.

Include the affected skill and version, impact, reproduction steps, and a safe way to contact you. Maintainers triage reports as capacity permits; there is no response-time guarantee.

## Before installing a skill

Read its instructions and give your agent only the permissions it needs. A skill can influence tool use, data access, and code execution in the host agent.

## What the checks cover

The repository validator checks file layout and metadata. CI also runs SkillSpector's static security scan on every skill. Neither check runs a skill, catches every malicious instruction, or tests behavior in every agent. The current catalog contains no executable scripts or bundled MCP servers. Maintainers may amend or remove a skill if a material risk is found.
