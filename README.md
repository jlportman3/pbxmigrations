# PBX Migration Agent

This project provides an intelligent agent (`pbx_agent.py`) designed to assist in the migration of Asterisk/FreePBX systems from older versions to newer ones. It automates the collection, comparison, and transfer of critical PBX data, including configuration files, database entries, sound files, and voicemails.

## Features

*   **Data Fetching (`fetch-all`)**:
    *   Collects `/etc/asterisk` configurations, MySQL database dumps, Asterisk sound files (`/var/lib/asterisk/sounds`), and voicemail data (`/var/spool/asterisk/voicemail`) from both old and new PBX servers.
    *   Stores fetched data locally in `data/old_system` and `data/new_system` directories.

*   **Configuration and Data Comparison (`compare`)**:
    *   Analyzes differences in `/etc/asterisk` files and MySQL database entries between the old and new systems.
    *   Generates a concise, migration-focused report (`comparison_report.txt`) highlighting what needs to be migrated. The report provides counts for large sets of differences and lists individual items for smaller sets.

*   **Automated Migration (`migrate`)**:
    *   Pushes the identified missing or differing data (configurations, sound files, voicemails, and database content) from the local `old_system` data to the new PBX server.

## Usage

### Prerequisites

*   Python 3 installed on your local machine.
*   SSH access to both your old and new PBX servers with key-based authentication configured for the `SSH_USER` specified in `pbx_agent.py`.
*   `rsync` installed on both local and remote servers.
*   MySQL/MariaDB server running on both PBX systems, with `mysqldump` and `mysql` client utilities available.
*   The `SSH_USER` must have read permissions for `/etc/asterisk`, `/var/lib/asterisk/sounds`, and `/var/spool/asterisk/voicemail` on the old server, and write permissions for target directories on the new server. MySQL users must have appropriate database privileges.

### Configuration

Edit the `pbx_agent.py` file to set your SSH connection details and MySQL credentials:

```python
# SSH Connection Details
OLD_SYSTEM_HOST = "pbx.alamobb.net"
NEW_SYSTEM_HOST = "newpbx.alamobb.net"
SSH_USER = "baron"
# ... other SSH options ...

# MySQL Credentials
MYSQL_USER_OLD = "root"
MYSQL_PASS_OLD = "mxyzptlk"
MYSQL_USER_NEW = "freepbxuser"
MYSQL_PASS_NEW = "kWqTywBNmsDK"
MYSQL_DB = "asterisk"
```

**Security Note**: Passing MySQL passwords directly in the script or on the command line is a security risk. For production environments, consider using `.my.cnf` files or environment variables for credentials.

### Running the Agent

Navigate to the project directory in your terminal.

1.  **Fetch all data from both systems**:
    This step collects all necessary configurations, database dumps, sound files, and voicemails.
    ```bash
    python3 pbx_agent.py fetch-all
    ```

2.  **Generate a comparison report**:
    This will create `comparison_report.txt` detailing the differences and what needs to be migrated.
    ```bash
    python3 pbx_agent.py compare
    ```
    Review `comparison_report.txt` to understand the proposed migration plan.

3.  **Migrate data to the new system**:
    **WARNING**: This action will push data from the old system to the new system. Ensure you have backups and understand the implications before proceeding.
    ```bash
    python3 pbx_agent.py migrate
    ```

## Development Notes

*   The `_parse_sql_dump` function is a basic key-value parser. For complex SQL structures, it might not capture all nuances.
*   The `compare_configs.py` script is a standalone comparison tool, but its core logic for directory and database comparison has been integrated and enhanced within `pbx_agent.py`.
