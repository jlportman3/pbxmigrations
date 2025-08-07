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
SOUND_FILES_PATH = "/var/lib/asterisk/sounds"
VOICEMAIL_PATH = "/var/spool/asterisk/voicemail"

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

def fetch_directory(host: str, remote_path: str, local_dir: Path, is_old_server: bool = False, exclude_pattern: str = ""):
    """Fetches a directory from a remote server via rsync."""
    print(f"Fetching {remote_path} from {host}...")
    local_dir.mkdir(parents=True, exist_ok=True)
    
    ssh_opts = SSH_COMMON_OPTS
    if is_old_server:
        ssh_opts += SSH_OLD_SERVER_OPTS
        
    rsync_command = [
        "rsync",
        "-avz",
        "-e", f"ssh {' '.join(ssh_opts)}",
        f"{SSH_USER}@{host}:{remote_path}/",
        str(local_dir / Path(remote_path).name) # Use the last part of the remote_path as the local directory name
    ]
    
    if exclude_pattern:
        rsync_command.insert(2, f"--exclude={exclude_pattern}") # Insert after -avz
    
    print(f"Running: {' '.join(rsync_command)}")
    try:
        subprocess.run(rsync_command, check=True)
        print("Fetch successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error fetching {remote_path} from {host}: {e}")
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

def push_directory(host: str, local_path: Path, remote_path: str):
    """Pushes a directory to a remote server via rsync."""
    print(f"Pushing {local_path} to {host}:{remote_path}...")
    
    ssh_opts = SSH_COMMON_OPTS
    # No is_old_server check here, as we are pushing to the new server
        
    rsync_command = [
        "rsync",
        "-avz",
        "-e", f"ssh {' '.join(ssh_opts)}",
        str(local_path) + "/", # Add trailing slash to copy contents
        f"{SSH_USER}@{host}:{remote_path}/"
    ]
    
    print(f"Running: {' '.join(rsync_command)}")
    try:
        subprocess.run(rsync_command, check=True)
        print("Push successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error pushing {local_path} to {host}: {e}")
        raise

def push_mysql_dump(host: str, local_dump_path: Path):
    """Pushes a MySQL dump to the remote server and imports it."""
    print(f"Pushing MySQL dump {local_dump_path} to {host}...")
    
    mysql_user = MYSQL_USER_NEW
    mysql_pass = MYSQL_PASS_NEW

    # Command to import the dump on the remote server
    # Note: Password is sent on the command line. This is a security risk on a shared system.
    remote_import_command = f"mysql -u {mysql_user} -p'{mysql_pass}' {MYSQL_DB}"
    
    # Use ssh to pipe the local dump file to the remote mysql command
    ssh_opts = SSH_COMMON_OPTS
    full_command = ["ssh"] + ssh_opts + [f"{SSH_USER}@{host}", remote_import_command]
    
    print(f"Running: cat {local_dump_path} | {' '.join(full_command)}")
    try:
        with open(local_dump_path, 'rb') as f:
            subprocess.run(full_command, stdin=f, check=True)
        print("MySQL dump import successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error importing MySQL dump on {host}:")
        print(e.stderr)
        raise
    except Exception as e:
        print(f"Error pushing MySQL dump to {host}: {e}")
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

def generate_comparison_report(old_etc_dir: Path, new_etc_dir: Path, old_db_path: Path, new_db_path: Path) -> str:
    report_content = []

    # --- Compare /etc/asterisk directories ---
    etc_report_lines = []
    old_etc_dir = OLD_SYSTEM_DATA_DIR / "asterisk"
    new_etc_dir = NEW_SYSTEM_DATA_DIR / "asterisk"
    
    missing_in_new_etc, missing_in_old_etc = _compare_dirs(old_etc_dir, new_etc_dir)

    etc_diff_found = False
    if missing_in_new_etc:
        etc_diff_found = True
        etc_report_lines.append(f"Files to be COPIED from OLD /etc/asterisk to NEW ({len(missing_in_new_etc)} files):")
        if len(missing_in_new_etc) <= 5: # List if few, otherwise just count
            for p in missing_in_new_etc:
                etc_report_lines.append(f"    - {p}")
        else:
            etc_report_lines.append("    (Too many to list, showing count only)")
    
    if missing_in_old_etc:
        etc_diff_found = True
        etc_report_lines.append(f"Files present in NEW /etc/asterisk but NOT in OLD (review for removal from NEW) ({len(missing_in_old_etc)} files):")
        if len(missing_in_old_etc) <= 5: # List if few, otherwise just count
            for p in missing_in_old_etc:
                etc_report_lines.append(f"    - {p}")
        else:
            etc_report_lines.append("    (Too many to list, showing count only)")
    
    if etc_diff_found:
        report_content.append("--- /etc/asterisk Migration Plan ---")
        report_content.extend(etc_report_lines)
        report_content.append("") # Add a blank line for separation

    # --- Compare MySQL Databases ---
    db_report_lines = []
    old_db_path = OLD_SYSTEM_DATA_DIR / "asterisk_dump.sql"
    new_db_path = NEW_SYSTEM_DATA_DIR / "asterisk_dump.sql"

    old_db = _parse_sql_dump(old_db_path)
    new_db = _parse_sql_dump(new_db_path)

    missing_keys_db, changed_keys_db = _compare_sql_dumps(old_db, new_db)

    db_diff_found = False
    if missing_keys_db:
        db_diff_found = True
        db_report_lines.append(f"Database entries to be ADDED from OLD to NEW ({len(missing_keys_db)} entries):")
        if len(missing_keys_db) <= 5: # List if few, otherwise just count
            for key in missing_keys_db:
                db_report_lines.append(f"    - {key} : {old_db[key]}")
        else:
            db_report_lines.append("    (Too many to list, showing count only)")
    
    if changed_keys_db:
        db_diff_found = True
        db_report_lines.append(f"Database entries to be UPDATED from OLD to NEW ({len(changed_keys_db)} entries):")
        if len(changed_keys_db) <= 5: # List if few, otherwise just count
            for key, (old_val, new_val) in sorted(changed_keys_db.items()):
                db_report_lines.append(f"    - {key}\n      Old: {old_val}\n      New: {new_val}")
        else:
            db_report_lines.append("    (Too many to list, showing count only)")
    
    if db_diff_found:
        report_content.append("--- MySQL Database Migration Plan ---")
        report_content.extend(db_report_lines)
        report_content.append("") # Add a blank line for separation

    if not etc_diff_found and not db_diff_found:
        report_content.append("No significant differences found in /etc/asterisk or MySQL databases.")

    return "\n".join(report_content)


def main():
    parser = argparse.ArgumentParser(description="PBX Migration Agent")
    parser.add_argument("action", choices=["fetch-all", "compare", "migrate"], help="Action to perform")
    args = parser.parse_args()

    if args.action == "fetch-all":
        print("--- Starting data fetch from OLD system ---")
        fetch_directory(OLD_SYSTEM_HOST, "/etc/asterisk", OLD_SYSTEM_DATA_DIR, is_old_server=True)
        fetch_directory(OLD_SYSTEM_HOST, SOUND_FILES_PATH, OLD_SYSTEM_DATA_DIR, is_old_server=True)
        fetch_directory(OLD_SYSTEM_HOST, VOICEMAIL_PATH, OLD_SYSTEM_DATA_DIR, is_old_server=True)
        fetch_mysql_dump(OLD_SYSTEM_HOST, OLD_SYSTEM_DATA_DIR, is_old_server=True)
        
        print("\n--- Starting data fetch from NEW system ---")
        fetch_directory(NEW_SYSTEM_HOST, "/etc/asterisk", NEW_SYSTEM_DATA_DIR, exclude_pattern="keys")
        fetch_directory(NEW_SYSTEM_HOST, SOUND_FILES_PATH, NEW_SYSTEM_DATA_DIR)
        fetch_directory(NEW_SYSTEM_HOST, VOICEMAIL_PATH, NEW_SYSTEM_DATA_DIR)
        fetch_mysql_dump(NEW_SYSTEM_HOST, NEW_SYSTEM_DATA_DIR)
        
        print("\nData fetch complete.")

    elif args.action == "compare":
        old_etc_dir = OLD_SYSTEM_DATA_DIR / "asterisk"
        new_etc_dir = NEW_SYSTEM_DATA_DIR / "asterisk"
        old_db_path = OLD_SYSTEM_DATA_DIR / "asterisk_dump.sql"
        new_db_path = NEW_SYSTEM_DATA_DIR / "asterisk_dump.sql"

        report = generate_comparison_report(old_etc_dir, new_etc_dir, old_db_path, new_db_path)
        
        report_file_path = "comparison_report.txt"
        with open(report_file_path, "w") as f:
            f.write(report)
        print(f"Comparison report generated and saved to {report_file_path}")

    elif args.action == "migrate":
        print("--- Starting migration to NEW system ---")
        
        # Push /etc/asterisk
        old_etc_local_path = OLD_SYSTEM_DATA_DIR / "asterisk"
        push_directory(NEW_SYSTEM_HOST, old_etc_local_path, "/etc/asterisk")

        # Push sound files
        old_sounds_local_path = OLD_SYSTEM_DATA_DIR / Path(SOUND_FILES_PATH).name
        push_directory(NEW_SYSTEM_HOST, old_sounds_local_path, SOUND_FILES_PATH)

        # Push voicemails
        old_voicemail_local_path = OLD_SYSTEM_DATA_DIR / Path(VOICEMAIL_PATH).name
        push_directory(NEW_SYSTEM_HOST, old_voicemail_local_path, VOICEMAIL_PATH)

        # Push MySQL dump
        old_db_local_path = OLD_SYSTEM_DATA_DIR / "asterisk_dump.sql"
        push_mysql_dump(NEW_SYSTEM_HOST, old_db_local_path)
        
        print("\nMigration complete.")

if __name__ == "__main__":
    main()
