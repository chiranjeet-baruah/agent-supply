#!/usr/bin/env python3
"""Validate AgentSupply's narrow v0 skill profile and render its catalog."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ENTRY_FIELDS = {"id", "title", "summary", "category", "path", "version", "license"}
FRONTMATTER_FIELDS = {"name", "description", "license"}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_RE = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _read_registry(root: Path) -> tuple[list[dict[str, str]], list[str]]:
    path = root / "registry" / "catalog.json"
    if path.parent.is_symlink() or path.is_symlink():
        return [], ["registry/catalog.json: symlinks are not allowed"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        return [], [f"registry/catalog.json: {exc}"]

    if not isinstance(data, dict) or set(data) != {"schema_version", "entries"}:
        return [], ["registry/catalog.json: expected only schema_version and entries"]
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        return [], ["registry/catalog.json: schema_version must be 1"]
    if not isinstance(data["entries"], list) or not data["entries"]:
        return [], ["registry/catalog.json: entries must be a nonempty array"]

    entries: list[dict[str, str]] = []
    errors: list[str] = []
    seen: set[str] = set()
    for index, entry in enumerate(data["entries"]):
        where = f"registry/catalog.json: entries[{index}]"
        if not isinstance(entry, dict) or set(entry) != ENTRY_FIELDS:
            errors.append(f"{where}: expected fields {', '.join(sorted(ENTRY_FIELDS))}")
            continue
        if any(not isinstance(value, str) or not value.strip() or any(ord(char) < 32 for char in value)
               for value in entry.values()):
            errors.append(f"{where}: all fields must be nonempty, single-line strings")
            continue
        skill_id = entry["id"]
        if len(skill_id) > 64 or not NAME_RE.fullmatch(skill_id):
            errors.append(f"{where}: invalid id {skill_id!r}")
            continue
        if skill_id in seen:
            errors.append(f"{where}: duplicate id {skill_id}")
            continue
        seen.add(skill_id)
        if entry["path"] != f"skills/{skill_id}":
            errors.append(f"{where}: path must be skills/{skill_id}")
            continue
        if not VERSION_RE.fullmatch(entry["version"]):
            errors.append(f"{where}: version must be MAJOR.MINOR.PATCH")
            continue
        if entry["license"] != "Apache-2.0":
            errors.append(f"{where}: v0 accepts only first-party Apache-2.0 skills")
            continue
        if len(entry["title"]) > 80 or len(entry["summary"]) > 240:
            errors.append(f"{where}: title or summary exceeds the v0 length limit")
            continue
        entries.append(entry)
    return entries, errors


def _read_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    label = str(path)
    if path.is_symlink():
        return {}, [f"{label}: symlinks are not allowed"]
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return {}, [f"{label}: {exc}"]
    lines = content.splitlines()
    if not lines or lines[0] != "---":
        return {}, [f"{label}: expected YAML frontmatter starting with ---"]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, [f"{label}: missing closing --- in frontmatter"]
    if not any(line.strip() for line in lines[end + 1 :]):
        return {}, [f"{label}: skill instructions are empty"]

    fields: dict[str, str] = {}
    errors: list[str] = []
    for line in lines[1:end]:
        key, separator, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if not separator or key not in FRONTMATTER_FIELDS or not value:
            errors.append(f"{label}: v0 frontmatter requires one-line name, description, and license fields")
        elif key in fields:
            errors.append(f"{label}: duplicate frontmatter field {key}")
        else:
            fields[key] = value
    if set(fields) != FRONTMATTER_FIELDS:
        errors.append(f"{label}: expected name, description, and license fields")
    if "name" in fields and (len(fields["name"]) > 64 or not NAME_RE.fullmatch(fields["name"])):
        errors.append(f"{label}: invalid skill name")
    if "description" in fields:
        description = fields["description"]
        if len(description) > 1024:
            errors.append(f"{label}: description exceeds 1024 characters")
        if (not description[0].isalpha() or not any(char.isspace() for char in description)
                or ": " in description or " #" in description or "\t" in description):
            errors.append(f"{label}: v0 description must be an unquoted plain-text YAML scalar")
    return fields, errors


def _validate_skill(root: Path, entry: dict[str, str]) -> list[str]:
    skill_id = entry["id"]
    directory = root / "skills" / skill_id
    label = f"skills/{skill_id}"
    errors: list[str] = []
    if directory.is_symlink() or not directory.is_dir():
        return [f"{label}: expected a real directory"]
    for item in directory.iterdir():
        relative = f"{label}/{item.name}"
        if item.is_symlink():
            errors.append(f"{relative}: symlinks are not allowed")
        elif item.name == "SKILL.md" and item.is_file():
            pass
        elif item.name == "references" and item.is_dir():
            for reference in item.iterdir():
                if reference.is_symlink() or not reference.is_file() or reference.suffix != ".md":
                    errors.append(f"{relative}/{reference.name}: only regular Markdown files are allowed")
        else:
            errors.append(f"{relative}: v0 allows only SKILL.md and references/*.md")

    frontmatter, metadata_errors = _read_frontmatter(directory / "SKILL.md")
    errors.extend(message.replace(str(root) + "/", "") for message in metadata_errors)
    if frontmatter.get("name") != skill_id:
        errors.append(f"{label}/SKILL.md: name must match registry id and directory")
    if frontmatter.get("license") != entry["license"]:
        errors.append(f"{label}/SKILL.md: license must match registry")
    return errors


def render_catalog(entries: list[dict[str, str]]) -> str:
    """Render a deterministic GitHub-readable catalog from validated entries."""
    def cell(value: str) -> str:
        for char, replacement in (
            ("&", "&amp;"), ("<", "&lt;"), (">", "&gt;"),
            ("[", "&#91;"), ("]", "&#93;"), ("|", "&#124;"),
            ("`", "&#96;"), ("\\", "&#92;"),
        ):
            value = value.replace(char, replacement)
        return value

    lines = [
        "# Skills catalog",
        "",
        "<!-- Generated by python3 tooling/validate.py --write-catalog. Do not edit by hand. -->",
        "",
        "These first-party skills contain instructions only. CI checks file structure and scans each skill for security patterns. Passing those checks does not prove safety or compatibility with a particular agent.",
        "",
        "| Skill | Category | Purpose | Version |",
        "| --- | --- | --- | --- |",
    ]
    for entry in sorted(entries, key=lambda item: item["id"]):
        link = f"[{cell(entry['title'])}]({entry['path']}/SKILL.md)"
        lines.append(f"| {link} | {cell(entry['category'])} | {cell(entry['summary'])} | {entry['version']} |")
    lines.extend(["", "See [README.md](README.md) for installation guidance and [CONTRIBUTING.md](CONTRIBUTING.md) for the review policy.", ""])
    return "\n".join(lines)


def _validate_repository(root: Path, check_catalog: bool) -> tuple[list[dict[str, str]], list[str]]:
    entries, errors = _read_registry(root)
    skills_dir = root / "skills"
    if skills_dir.is_symlink() or not skills_dir.is_dir():
        errors.append("skills: expected a real directory")
        return entries, errors

    listed = {entry["id"] for entry in entries}
    for item in skills_dir.iterdir():
        if item.name not in listed:
            errors.append(f"skills/{item.name}: unlisted skill or unexpected file")
    for entry in entries:
        errors.extend(_validate_skill(root, entry))

    if check_catalog and not errors:
        catalog = root / "CATALOG.md"
        if catalog.is_symlink():
            errors.append("CATALOG.md: symlinks are not allowed")
        else:
            try:
                actual = catalog.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                errors.append(f"CATALOG.md: {exc}")
            else:
                if actual != render_catalog(entries):
                    errors.append("CATALOG.md: stale; run python3 tooling/validate.py --write-catalog")
    return entries, errors


def validate_repository(root: Path) -> list[str]:
    """Return all structural and catalog errors without executing skill content."""
    return _validate_repository(root, check_catalog=True)[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--write-catalog", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    entries, errors = _validate_repository(root, check_catalog=not args.write_catalog)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    if args.write_catalog:
        catalog = root / "CATALOG.md"
        if catalog.is_symlink():
            print("CATALOG.md: symlinks are not allowed", file=sys.stderr)
            return 1
        catalog.write_text(render_catalog(entries), encoding="utf-8")
        print("Wrote CATALOG.md")
    else:
        print(f"Validated {len(entries)} skills and CATALOG.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
