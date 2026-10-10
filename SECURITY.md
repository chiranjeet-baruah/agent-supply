# Security policy

Agent instructions can influence tool use, data access, and code execution in the host agent. Treat every skill as code-like supply-chain input: inspect it before installation and use the least privileges your harness supports.

## Reporting a vulnerability

Use [GitHub private vulnerability reporting](https://github.com/chiranjeet-baruah/agent-supply/security/advisories/new) if available. If that option is unavailable, open a public issue requesting a private contact channel **without** exploit details, secrets, or affected user data.

Include the affected skill and version, impact, reproduction steps, and a safe way to contact you. Maintainers will acknowledge and triage reports as capacity permits; no response-time guarantee is implied.

## Scope of checks

The automated validator enforces a narrow file layout and metadata consistency. It does not detect every malicious instruction, verify behavioral safety, or test all harnesses. The current catalog contains no executable scripts or bundled MCP servers. Maintainers may remove or amend a listing if a material risk is found.
