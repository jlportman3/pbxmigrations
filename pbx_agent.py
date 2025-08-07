#!/usr/bin/env python3
"""
An intelligent agent for comparing and migrating Asterisk PBX systems.
"""

import argparse
import subprocess
from pathlib import Path
from typing import Iterable, Tuple

# --- Configuration ---

# SSH Connection Details
OLD_SYSTEM_HOST = "pbx.alamobb.net"
NEW_SYSTEM_HOST = "newpbx.alamobb.net"
SSH_USER = "baron"
SSH_COMMON_OPTS = ["-o", "StrictHostKeyChecking=no"]
SSH_OLD_SERVER_OPTS = ["-o", "HostKeyAlgorithms=+ssh-rsa", "-o", "PubkeyAcceptedKeyTypes=+ssh-rsa"]

# MySQL Credentials
MYSQL_USER_OLD = "root"
MYSQL_PASS_OLD = "mxyzptlk"
MYSQL_USER_NEW = "freepbxuser"
MYSQL_PASS_NEW = "kWqTywBNmsDK"
MYSQL_DB = "asterisk"

# Data Storage Paths
DATA_DIR = Path("data")
OLD_SYSTEM_DATA_DIR = DATA_DIR / "old_system"
NEW_SYSTEM_DATA_DIR = DATA_DIR / "new_system"

# --- Core Functions ---

def run_remote_command(host: str, command: str, is_old_server: bool = False):
    """Executes a command on a remote server via SSH."""
    ssh_opts = SSH_COMMON_OPTS
    if is_old_server:
        ssh_opts += SSH_OLD_SERVER_OPTS
    
    full_command = ["ssh"] + ssh_opts + [f"{SSH_USER}@{host}", command]
    print(f"Running on {host}: {' '.join(full_command)}")
    
    try:
        result = subprocess.run(full_command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command on {host}:")
        print(e.stderr)
        raise

def fetch_etc_asterisk(host: str, local_dir: Path, is_old_server: bool = False):
    """Fetches the /etc/asterisk directory from a remote server."""
    print(f"Fetching /etc/asterisk from {host}...")
    local_dir.mkdir(parents=True, exist_ok=True)
    
    ssh_opts = SSH_COMMON_OPTS
    if is_old_server:
        ssh_opts += SSH_OLD_SERVER_OPTS
        
    rsync_command = [
        "rsync",
        "-avz",
        "-e", f"ssh {' '.join(ssh_opts)}",
        f"{SSH_USER}@{host}:/etc/asterisk/",
        str(local_dir / "asterisk")
    ]
    if host == NEW_SYSTEM_HOST:
        rsync_command.insert(2, "--exclude=keys") # Insert after -avz
    
    print(f"Running: {' '.join(rsync_command)}")
    try:
        subprocess.run(rsync_command, check=True)
        print("Fetch successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error fetching /etc/asterisk from {host}: {e}")
        raise

def fetch_mysql_dump(host: str, local_dir: Path, is_old_server: bool = False):
    """Fetches a MySQL dump from the remote server."""
    print(f"Fetching MySQL dump from {host}...")
    local_dir.mkdir(parents=True, exist_ok=True)
    dump_file = local_dir / "asterisk_dump.sql"
    
    mysql_user = MYSQL_USER_OLD
    mysql_pass = MYSQL_PASS_OLD
    if host == NEW_SYSTEM_HOST:
        mysql_user = MYSQL_USER_NEW
        mysql_pass = MYSQL_PASS_NEW

    # Note: Password is sent on the command line. This is a security risk on a shared system.
    # Acceptable for this controlled environment, but should be improved for a general tool.
    command = f"mysqldump -u {mysql_user} -p'{mysql_pass}' {MYSQL_DB}"
    
    try:
        dump_content = run_remote_command(host, command, is_old_server)
        with open(dump_file, "w") as f:
            f.write(dump_content)
        print("MySQL dump successful.")
    except Exception as e:
        print(f"Error fetching MySQL dump from {host}: {e}")
        raise

# --- Main Execution ---

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

def _parse_sql_dump(path: Path) -> dict[str, str]:
    """Parse a simplified SQL dump into a dictionary (key-value pairs)."""
    result: dict[str, str] = {}
    with open(path) as fh:
        for line in fh:
            # This is a very basic parser. It assumes lines are in a simple KEY=VALUE format
            # or can be simplified to such. For complex SQL, a proper SQL parser would be needed.
            if '=' in line:
                key, value = line.split('=', 1)
                result[key.strip()] = value.strip()
            elif ':' in line: # For ASTDB like entries
                key, value = line.split(':', 1)
                result[key.strip()] = value.strip()
    return result

def _compare_sql_dumps(old_db: dict[str, str], new_db: dict[str, str]) -> Tuple[Iterable[str], dict[str, Tuple[str, str]]]:
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

def main():
    parser = argparse.ArgumentParser(description="PBX Migration Agent")
    parser.add_argument("action", choices=["fetch-all", "compare"], help="Action to perform")
    args = parser.parse_args()

    if args.action == "fetch-all":
        print("--- Starting data fetch from OLD system ---")
        fetch_etc_asterisk(OLD_SYSTEM_HOST, OLD_SYSTEM_DATA_DIR, is_old_server=True)
        fetch_mysql_dump(OLD_SYSTEM_HOST, OLD_SYSTEM_DATA_DIR, is_old_server=True)
        
        print("\n--- Starting data fetch from NEW system ---")
        fetch_etc_asterisk(NEW_SYSTEM_HOST, NEW_SYSTEM_DATA_DIR)
        fetch_mysql_dump(NEW_SYSTEM_HOST, NEW_SYSTEM_DATA_DIR)
        
        print("\nData fetch complete.")

    elif args.action == "compare":
        print("--- Comparing /etc/asterisk directories ---")
        old_etc_dir = OLD_SYSTEM_DATA_DIR / "asterisk"
        new_etc_dir = NEW_SYSTEM_DATA_DIR / "asterisk"
        
        missing_new, missing_old = _compare_dirs(old_etc_dir, new_etc_dir)

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

        print("\n--- Comparing MySQL Databases ---")
        old_db_path = OLD_SYSTEM_DATA_DIR / "asterisk_dump.sql"
        new_db_path = NEW_SYSTEM_DATA_DIR / "asterisk_dump.sql"

        old_db = _parse_sql_dump(old_db_path)
        new_db = _parse_sql_dump(new_db_path)

        missing_keys, changed = _compare_sql_dumps(old_db, new_db)

        if missing_keys:
            print("\nDatabase entries missing in new system:")
            for key in missing_keys:
                print(f"  {key} : {old_db[key]}")
        if changed:
            print("\nDatabase entries with different values:")
            for key, (old_val, new_val) in sorted(changed.items()):
                print(f"  {key}\n    old: {old_val}\n    new: {new_val}")
        if not missing_keys and not changed:
            print("\nDatabase entries are identical")

if __name__ == "__main__":
    main()
