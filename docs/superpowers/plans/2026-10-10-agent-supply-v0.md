# AgentSupply v0 Implementation Plan

This completed plan records the v0.1.0 launch. For current checks and release steps, see [the maintainer checklist](../../MAINTAINER_SETUP.md).

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Native execution was used for this small, tightly coupled initial repository.

**Goal:** Publish a usable, validated first-party skills catalog on GitHub.

**Architecture:** JSON is the listing source of truth; skill folders contain portable instructions; a Python standard library tool validates both and renders the Markdown catalog. CI runs the same checks without executing skills.

**Tech Stack:** Markdown, JSON, Python 3.10+, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-10-10-agent-supply-v0-design.md`

## Global constraints

- First-party, instruction-only skills in v0.
- No runtime or third-party Python dependencies.
- Structural validation must not be described as a security certification.
- No unverified cross-harness compatibility claims.

## Review focus

- Duplicate or malformed registry IDs: reject with a clear error.
- Path traversal and symlinks: reject before reading outside the repository.
- Registry/frontmatter mismatch: reject with the affected path.
- Unlisted skill directories: reject so a skill cannot bypass catalog review.
- Stale generated catalog: fail CI and offer a repair command.

## Tasks

### 1. Publish the two pilot skills and registry

- [x] Add `skills/go-code-review/SKILL.md` and `skills/postgres-query-review/SKILL.md` with valid metadata, useful workflows, and explicit limitations.
- [x] Add `registry/catalog.json` with stable IDs, paths, versions, summaries, categories, and license.
- [x] Check each instruction for unsupported claims and unintended write or execution authority.

### 2. Validate and render the catalog

- [x] Add `tooling/validate.py` with `validate_repository(root) -> list[str]` and `render_catalog(entries) -> str`.
- [x] Add unit tests for the five review-focus failure modes and a valid fixture.
- [x] Generate `CATALOG.md` and run validation and tests locally.

### 3. Document and wire the repository

- [x] Expand `README.md` with scope, discovery, installation, and validation instructions.
- [x] Add contribution, security, and governance policies, a focused `.gitignore`, and GitHub templates.
- [x] Add a least-privilege CI workflow pinned to an immutable checkout commit.
- [x] Run the full checks, inspect the diff, and report what remains for GitHub repository settings.
