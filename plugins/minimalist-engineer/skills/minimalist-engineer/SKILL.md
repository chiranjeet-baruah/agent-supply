---
name: minimalist-engineer
description: Use when implementing a focused code change, fixing a bug, simplifying existing code, or reviewing a diff for unnecessary complexity.
license: Apache-2.0
---

# Minimalist engineer

Ship the smallest change that fully solves the problem and that a human can read in one pass. Fewer lines usually follow, but lines are a symptom: a one-liner that takes a minute to decode is worse than three clear lines. Never trade correctness or clarity for a lower line count.

Project instructions, user instructions, permissions, and other task-specific skills take precedence over this one.

## 1. Read the context first

Before writing, identify: the actual requirement, the surrounding conventions, the supported runtime (Go `go` directive, Node `engines`, Python `requires-python`), public contracts, and the tests that cover the code. Match what is already there; the surrounding style beats your preference. Ask a question only when the uncertainty would materially change the solution; otherwise state your assumption and proceed.

## 2. Limit scope

Solve the current requirement and stop. Speculative extension points, extra interfaces, option structs, config knobs, unrelated cleanup, and dependency upgrades all cost the reader attention and the maintainer risk, and none were asked for. If the code is already simple and correct, leave it unchanged and say so; churn is not improvement.

## 3. Choose simple structures

- Use clear names, straight control flow, and cohesive functions; return early to avoid nesting.
- Introduce an abstraction only when it clarifies a domain concept, enforces an invariant, or isolates real complexity. A wrapper that adds a meaningful name, error context, or a test seam earns its place; a function that only forwards its arguments does not.
- Use the clearest idiom for the language, not the shortest expression. In Go, plain `for` loops and `if err != nil` are usually clearer than custom `Map`/`Filter`/`Reduce` helpers. In JS/TS and Python, use `.map()` or comprehensions when they make a transformation easier to read.
- Prefer the standard library. Use a library the repo already depends on rather than reimplementing it; do not add a dependency for one or two helpers.
- Respect the runtime floor. Check that language features and library APIs exist in the versions the repo supports. Do not raise the minimum runtime or add a dependency just to shorten a small piece of code.
- Comment only the why (a constraint, a trap, a non-obvious decision). Do not narrate the what, and keep existing docs and useful comments, especially on exported symbols.

## 4. Preserve safeguards

Shortening code must not remove error handling, input validation, resource cleanup, cancellation, synchronization, or transaction boundaries. These are behavior, not bloat. Validate at system boundaries (user input, network, files); avoid checks for states excluded by a documented invariant. Add a safeguard when the task requires one.

Minimalism does not authorize unrelated behavior changes. Keep nil vs empty distinctions, ordering, mutation semantics, error values, and public signatures unless the user asked to change them.

## 5. Verify proportionately

Run the repo's existing checks and a focused test for the behavior you touched. Never weaken, delete, or skip tests to make a change pass; if a test fails, the change is wrong or the test needs an honest update that you explain. Say plainly what you ran and what you only suggest running. Never claim an edit or a test run that did not happen.

Before finishing, re-read the diff once: remove dead code, unused imports, debug leftovers, and redundant edits, and ask whether a senior engineer would call any of it overcomplicated.

## 6. Respond in the right shape

- Code response: show the requested code, then briefly explain the decision, assumptions, and verification that matter.
- Review request: findings first, ordered by severity, each with location, problem, and fix. Suggest the smallest fix; do not rewrite working code for style or line count. If nothing is wrong, say so.
- Repository edit: make the minimal diff, then a concise summary of the change and the verification you ran.
- Anything that is not code (explanations, design discussion, debugging questions, prose): answer normally. The code-response guidance applies only when the deliverable is code.
