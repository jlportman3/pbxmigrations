#!/usr/bin/env python3
"""Compare FreePBX/Asterisk configuration between old and new systems.

This helper script compares:

* Extracted contents of two tarballs containing `/etc/asterisk` from the
  old and new servers.
* ASTDB dump files created with `database show` from the Asterisk CLI.

The script reports configuration files missing between systems and
differences in ASTDB key/value pairs so you can ensure the new system
contains everything from the old one.
"""

from __future__ import annotations

import argparse
import tarfile
import tempfile
from pathlib import Path
from typing import Dict, Iterable, Tuple


def _extract_tar(path: str) -> Path:
    """Extract a tar.gz file to a temporary directory and return its path."""
    tmpdir = tempfile.mkdtemp(prefix="pbxmigrations_")
    with tarfile.open(path, "r:gz") as tar:
        tar.extractall(tmpdir)
    return Path(tmpdir)


def _list_files(root: Path) -> Iterable[Path]:
    """Yield relative file paths under *root* (files only)."""
    for p in root.rglob("*"):
        if p.is_file():
            yield p.relative_to(root)


def _compare_dirs(old_dir: Path, new_dir: Path) -> Tuple[Iterable[Path], Iterable[Path]]:
    """Return files missing in the new and in the old directories."""
    old_files = set(_list_files(old_dir))
    new_files = set(_list_files(new_dir))
    missing_in_new = sorted(old_files - new_files)
    missing_in_old = sorted(new_files - old_files)
    return missing_in_new, missing_in_old


def _parse_astdb(path: str) -> Dict[str, str]:
    """Parse an ASTDB dump created with `database show` into a dict."""
    result: Dict[str, str] = {}
    with open(path) as fh:
        for line in fh:
            if ":" not in line:
                continue
            key, value = line.rstrip().split(":", 1)
            result[key.strip()] = value.strip()
    return result


def _compare_astdb(old_db: Dict[str, str], new_db: Dict[str, str]) -> Tuple[Iterable[str], Dict[str, Tuple[str, str]]]:
    """Return keys missing in new DB and keys with differing values."""
    old_keys = set(old_db)
    new_keys = set(new_db)
    missing_keys = sorted(old_keys - new_keys)
    changed = {
        key: (old_db[key], new_db[key])
        for key in old_keys & new_keys
        if old_db[key] != new_db[key]
    }
    return missing_keys, changed


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare FreePBX configs and ASTDB dumps")
    parser.add_argument("--old-etc", required=True, help="Tarball of old /etc/asterisk")
    parser.add_argument("--new-etc", required=True, help="Tarball of new /etc/asterisk")
    parser.add_argument("--old-db", required=True, help="ASTDB dump from old system")
    parser.add_argument("--new-db", required=True, help="ASTDB dump from new system")
    args = parser.parse_args()

    old_dir = _extract_tar(args.old_etc)
    new_dir = _extract_tar(args.new_etc)
    missing_new, missing_old = _compare_dirs(old_dir, new_dir)

    if missing_new:
        print("Files present in old system but missing in new:")
        for p in missing_new:
            print(f"  {p}")
    if missing_old:
        print("Files present in new system but missing in old:")
        for p in missing_old:
            print(f"  {p}")
    if not missing_new and not missing_old:
        print("Configuration file sets are identical")

    old_db = _parse_astdb(args.old_db)
    new_db = _parse_astdb(args.new_db)
    missing_keys, changed = _compare_astdb(old_db, new_db)

    if missing_keys:
        print("\nASTDB entries missing in new system:")
        for key in missing_keys:
            print(f"  {key} : {old_db[key]}")
    if changed:
        print("\nASTDB entries with different values:")
        for key, (old_val, new_val) in sorted(changed.items()):
            print(f"  {key}\n    old: {old_val}\n    new: {new_val}")
    if not missing_keys and not changed:
        print("\nASTDB entries are identical")


if __name__ == "__main__":
    main()
