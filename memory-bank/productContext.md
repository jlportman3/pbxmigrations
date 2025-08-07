# Product Context: Asterisk/FreePBX Migration Tool

## Why this project exists
Many organizations face challenges migrating their legacy Asterisk/FreePBX systems to newer versions due to the complexity of configuration files, database schemas, and media files. Manual migration is error-prone, time-consuming, and often leads to data inconsistencies or service disruptions. This tool aims to streamline and automate this process.

## Problems it solves
*   **Reduces Manual Effort**: Automates the collection and comparison of configuration and data, significantly cutting down on manual intervention.
*   **Minimizes Downtime**: Provides a structured approach to migration, allowing for pre-migration analysis and a more predictable transfer process.
*   **Ensures Data Integrity**: Helps identify discrepancies between old and new systems, ensuring that critical configurations and data are not lost during migration.
*   **Supports Different Data Types**: Handles not just configuration files but also database entries, sound files, and voicemails, which are often overlooked in simpler migration scripts.

## How it should work
The tool operates in distinct phases:
1.  **Fetch**: Connects to both old and new PBX servers via SSH/rsync/mysqldump to collect all relevant data locally.
2.  **Compare**: Analyzes the fetched data to identify differences in configuration files and database entries. This comparison generates a human-readable report highlighting what needs to be migrated.
3.  **Migrate**: Pushes the identified missing or differing data from the old system's local copy to the new PBX server.

## User experience goals
The tool should be:
*   **Easy to use**: Command-line interface with clear actions (`fetch-all`, `compare`, `migrate`).
*   **Informative**: Provides clear feedback during operations and generates concise, actionable comparison reports.
*   **Reliable**: Performs data transfers securely and accurately, minimizing risks during migration.
