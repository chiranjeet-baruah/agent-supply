# Governance

The repository owner maintains AgentSupply. They decide which skills to list, review changes, handle reports, and may remove a skill if its source or behavior is in doubt.

## Before a skill is published

Each skill needs a clear purpose, a known source and license, and files a reviewer can inspect. Compatibility and safety claims need evidence. Changes to a published skill's behavior should raise its registry version and explain the effect in the pull request.

The `main` branch requires a pull request and passing `validate` and `skillspector` checks. A maintainer still reads changed skill instructions. A second reviewer is welcome, but the project does not claim independent security review or require an approval from another person while there is only one active maintainer.

Record decisions and exceptions in the relevant issue or pull request. Raise an appeal in a new issue without publishing private security details.
