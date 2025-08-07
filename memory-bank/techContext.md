# Technical Context: Asterisk/FreePBX Migration Tool

## Technologies used
*   **Python 3**: The primary programming language for the `pbx_agent.py` script.
*   **SSH**: Used for secure remote command execution and file transfer.
*   **Rsync**: A fast, versatile, remote (and local) file-copying tool. Used for synchronizing directories like `/etc/asterisk`, `/var/lib/asterisk/sounds`, and `/var/spool/asterisk/voicemail`.
*   **MySQL/MariaDB**: The database system used by FreePBX. `mysqldump` is used for exporting data, and the `mysql` client is used for importing.
*   **Asterisk**: The open-source telephony platform whose configurations and data are being migrated.
*   **FreePBX**: The web-based graphical user interface that controls and manages Asterisk.

## Development setup
*   **Local Development Environment**: A machine with Python 3 installed and SSH access to both the old and new PBX servers.
*   **SSH Keys**: Assumes SSH key-based authentication is set up for the `SSH_USER` on both remote servers to avoid password prompts.
*   **Permissions**: The `SSH_USER` on the remote servers must have sufficient read permissions for `/etc/asterisk`, `/var/lib/asterisk/sounds`, and `/var/spool/asterisk/voicemail`, and write permissions for the target directories on the new server. For MySQL operations, the configured `MYSQL_USER` must have appropriate database privileges.

## Technical constraints
*   **SSH Access**: Requires SSH access to both old and new PBX servers.
*   **Rsync Availability**: `rsync` must be installed on both the local machine and the remote PBX servers.
*   **MySQL Client/Server**: MySQL/MariaDB server must be running on both PBX systems, and the `mysqldump` and `mysql` client utilities must be available.
*   **Python Version**: Developed and tested with Python 3.
*   **Security**: Current implementation sends MySQL passwords on the command line during `mysqldump` and `mysql` import, which is a security risk in shared environments. This should be addressed for production use (e.g., using `.my.cnf` files or environment variables).

## Dependencies
The script primarily relies on standard Python libraries (`argparse`, `subprocess`, `pathlib`, `typing`) and external system commands (`ssh`, `rsync`, `mysqldump`, `mysql`). No external Python packages are required beyond the standard library.
