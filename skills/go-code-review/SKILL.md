---
name: go-code-review
description: Reviews Go changes for correctness, concurrency, reliability, API compatibility, and test gaps. Use when reviewing a Go pull request, patch, or implementation.
license: Apache-2.0
---

# Go code review

Review the supplied Go change as a maintainer responsible for production behavior.

## Workflow

1. Establish the intended behavior, affected callers, Go version, and operational context from the request and repository. State material assumptions when these are unavailable.
2. Read the changed code and enough surrounding code to trace inputs, outputs, errors, and ownership. Inspect relevant tests and callers. Do not infer behavior from a diff alone when the surrounding contract matters.
3. Prioritize concrete defects: incorrect results, data races, deadlocks, goroutine leaks, cancellation failures, unbounded work, broken error handling, resource leaks, compatibility breaks, and missing tests for risky paths.
4. Check whether the code handles partial failures and retries safely. For concurrent code, identify the shared state, synchronization, and shutdown path. For APIs, inspect callers and compatibility expectations.
5. Run focused tests or static checks when the environment and task permit them. Report the exact command and result. If a check was not run, say so.
6. Return findings ordered by severity. For each finding, give the file and line, the failing scenario, why the code causes it, and a practical fix. Distinguish a confirmed defect from a plausible risk that needs a reproducer.

## Review bar

- Do not invent a race, benchmark result, test failure, or production impact.
- Do not request broad refactoring when a smaller correction solves the problem.
- Treat style comments as optional unless they obscure correctness or maintenance.
- Do not modify code unless the user asks for a fix.
- If no concrete defect is found, say so and name the most important unverified risk or test gap.

## Output

Start with specific findings. Then give a short verification note and any remaining assumptions. Cite repository paths and line numbers where available.
