# System Patterns: Asterisk/FreePBX Migration Tool

## System architecture
The migration tool operates as a client-side Python script (`pbx_agent.py`) that interacts with remote Asterisk/FreePBX servers via SSH. It leverages standard Linux utilities like `rsync` and `mysqldump` for data transfer and `mysql` for database import.

```mermaid
graph TD
    A[Local Machine] -->|SSH/rsync/mysqldump| B[Old PBX Server]
    A[Local Machine] -->|SSH/rsync/mysqldump/mysql| C[New PBX Server]
    B --> D[Local Data Storage (old_system)]
    C --> E[Local Data Storage (new_system)]
    D --> F[Comparison Logic]
    E --> F
    F --> G[Comparison Report]
    D --> H[Migration Logic]
    H --> C
```

## Key technical decisions
*   **SSH for Remote Access**: Secure and widely available for remote command execution and file transfer.
*   **Rsync for Directory Synchronization**: Efficiently transfers and synchronizes directories, handling incremental updates and permissions.
*   **Mysqldump for Database Export**: Standard tool for creating database backups.
*   **Python for Orchestration**: Provides a flexible and readable scripting environment to orchestrate the various system commands and manage data flow.
*   **Local Data Staging**: All data is first pulled to the local machine before comparison or pushing to the new system. This provides a safe intermediate state and allows for offline analysis.

## Design patterns in use
*   **Command Pattern**: The `main` function dispatches actions (`fetch-all`, `compare`, `migrate`) based on command-line arguments.
*   **Facade Pattern**: The `pbx_agent.py` script acts as a facade, simplifying complex `ssh`, `rsync`, and `mysqldump` commands into higher-level Python functions.

## Component relationships
*   `pbx_agent.py`: The main script, orchestrating all operations.
*   `compare_configs.py`: A helper script (though currently its logic is largely duplicated/integrated into `pbx_agent.py`'s comparison functions) for comparing configuration files and ASTDB dumps. This could be refactored to be called directly by `pbx_agent.py` if its functionality becomes more distinct or complex.
*   `data/`: Local directory for storing fetched data from old and new systems.
