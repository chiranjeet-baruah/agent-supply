#!/usr/bin/env python3
"""Build and check Codex and Claude marketplace packages from the skill catalog."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from tooling.validate import validate_repository


REPOSITORY_URL = "https://github.com/chiranjeet-baruah/agent-supply"


def _json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def _has_symlink_in_tree(root: Path, path: Path) -> bool:
    while path != root:
        if path.is_symlink():
            return True
        path = path.parent
    return False


def expected_files(root: Path) -> dict[Path, bytes]:
    """Return every generated file, keyed by its path relative to the repository."""
    errors = validate_repository(root)
    if errors:
        raise ValueError("\n".join(errors))
    entries = json.loads((root / "registry/catalog.json").read_text(encoding="utf-8"))["entries"]
    files: dict[Path, bytes] = {}
    codex_plugins = []
    claude_plugins = []

    for entry in sorted(entries, key=lambda item: item["id"]):
        skill_id = entry["id"]
        plugin_root = Path("plugins") / skill_id
        skill_root = root / entry["path"]
        for source in sorted(skill_root.rglob("*")):
            if source.is_file():
                files[plugin_root / "skills" / skill_id / source.relative_to(skill_root)] = source.read_bytes()

        metadata = {
            "name": skill_id,
            "version": entry["version"],
            "description": entry["summary"],
            "author": {"name": "AgentSupply"},
            "homepage": REPOSITORY_URL,
            "repository": REPOSITORY_URL,
            "license": entry["license"],
        }
        files[plugin_root / "plugin.json"] = _json_bytes({
            "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            **metadata,
        })
        files[plugin_root / ".claude-plugin/plugin.json"] = _json_bytes(metadata)
        codex_plugins.append({
            "name": skill_id,
            "source": {"source": "local", "path": f"./plugins/{skill_id}"},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": "Productivity",
        })
        claude_plugins.append({
            "name": skill_id,
            "source": f"./plugins/{skill_id}",
            "description": entry["summary"],
        })

    files[Path(".agents/plugins/marketplace.json")] = _json_bytes({
        "name": "agent-supply",
        "interface": {"displayName": "AgentSupply"},
        "plugins": codex_plugins,
    })
    files[Path(".claude-plugin/marketplace.json")] = _json_bytes({
        "name": "agent-supply",
        "description": "Curated engineering skills from AgentSupply",
        "owner": {"name": "AgentSupply"},
        "plugins": claude_plugins,
    })
    return files


def check_files(root: Path, expected: dict[Path, bytes]) -> list[str]:
    """Find stale, missing, or unexpected files in generated locations."""
    errors = []
    for relative, content in expected.items():
        path = root / relative
        if _has_symlink_in_tree(root, path):
            errors.append(f"{relative}: symlinks are not allowed")
        elif not path.is_file():
            errors.append(f"{relative}: missing or not a regular file")
        elif path.read_bytes() != content:
            errors.append(f"{relative}: stale; run python3 -m tooling.package_plugins --write")

    managed = [root / "plugins", root / ".agents/plugins", root / ".claude-plugin"]
    for directory in managed:
        if _has_symlink_in_tree(root, directory):
            errors.append(f"{directory.relative_to(root)}: symlinks are not allowed")
        elif directory.exists():
            for path in directory.rglob("*"):
                relative = path.relative_to(root)
                if path.is_symlink():
                    errors.append(f"{relative}: symlinks are not allowed")
                elif path.is_file() and relative not in expected:
                    errors.append(f"{relative}: unexpected generated file")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--write", action="store_true", help="regenerate marketplace files")
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        expected = expected_files(root)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    if args.write:
        for relative, content in expected.items():
            path = root / relative
            if _has_symlink_in_tree(root, path):
                print(f"{relative}: refusing to write through a symlink", file=sys.stderr)
                return 1
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    errors = check_files(root, expected)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"Validated {len(expected)} marketplace files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
