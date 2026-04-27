#!/usr/bin/env python3
"""Bump blender_manifest.toml and __init__.py version; optional git commit, tag, push."""

import argparse
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "blender_manifest.toml"
INIT_PATH = ROOT / "__init__.py"


def read_manifest_version() -> tuple[int, int, int]:
	text = MANIFEST_PATH.read_text(encoding="utf-8")
	m = re.search(r'^version\s*=\s*"(\d+)\.(\d+)\.(\d+)"', text, re.MULTILINE)
	if not m:
		print("release_bump: read_manifest_version: could not parse version from blender_manifest.toml")
		sys.exit(1)
	return int(m.group(1)), int(m.group(2)), int(m.group(3))


def write_manifest_version(version: tuple[int, int, int]) -> None:
	text = MANIFEST_PATH.read_text(encoding="utf-8")
	new_line = f'version = "{version[0]}.{version[1]}.{version[2]}"'
	text_new = re.sub(
		r'^version\s*=\s*"[^"]+"',
		new_line,
		text,
		count=1,
		flags=re.MULTILINE,
	)
	MANIFEST_PATH.write_text(text_new, encoding="utf-8")


def write_init_version(version: tuple[int, int, int]) -> None:
	text = INIT_PATH.read_text(encoding="utf-8")
	replacement = f'"version"    : ({version[0]}, {version[1]}, {version[2]}),'
	text_new = re.sub(
		r'"version"\s*:\s*\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)',
		replacement,
		text,
		count=1,
	)
	INIT_PATH.write_text(text_new, encoding="utf-8")


def bump_from_kind(v: tuple[int, int, int], kind: str) -> tuple[int, int, int]:
	major, minor, patch = v
	if kind == "patch":
		return major, minor, patch + 1
	if kind == "minor":
		return major, minor + 1, 0
	if kind == "major":
		return major + 1, 0, 0
	raise ValueError(kind)


def run_git(args: list[str]) -> None:
	print(f"release_bump: run_git: git {' '.join(args)}")
	subprocess.run(["git", *args], cwd=ROOT, check=True)


def main() -> None:
	parser = argparse.ArgumentParser(
		description="Bump Asset Exporter version in blender_manifest.toml and __init__.py",
	)
	parser.add_argument(
		"bump",
		help="patch, minor, major — or an explicit version like 1.2.3",
	)
	parser.add_argument(
		"--commit",
		action="store_true",
		help="Stage version files and create a git commit",
	)
	parser.add_argument(
		"--tag",
		action="store_true",
		help="Create a git tag at the new version (requires --commit)",
	)
	parser.add_argument(
		"--push",
		action="store_true",
		help="Push current branch and the new tag to origin",
	)
	args = parser.parse_args()

	current = read_manifest_version()
	arg = args.bump.strip().lower()

	if re.fullmatch(r"\d+\.\d+\.\d+", arg):
		parts = arg.split(".")
		new_version = (int(parts[0]), int(parts[1]), int(parts[2]))
	elif arg in ("patch", "minor", "major"):
		new_version = bump_from_kind(current, arg)
	else:
		print("release_bump: main: bump must be patch, minor, major, or x.y.z")
		sys.exit(2)

	new_str = f"{new_version[0]}.{new_version[1]}.{new_version[2]}"
	cur_str = f"{current[0]}.{current[1]}.{current[2]}"
	print(f"release_bump: main: {cur_str} -> {new_str}")

	write_manifest_version(new_version)
	write_init_version(new_version)

	if args.tag and not args.commit:
		print("release_bump: main: --tag requires --commit")
		sys.exit(1)

	if args.commit:
		run_git(["add", "blender_manifest.toml", "__init__.py"])
		run_git(["commit", "-m", f"chore: release {new_str}"])

	if args.tag:
		run_git(["tag", new_str])

	if args.push:
		run_git(["push", "origin", "HEAD"])
		if args.tag:
			run_git(["push", "origin", new_str])

	print(f"release_bump: main: done; version is now {new_str}")


if __name__ == "__main__":
	main()
