# Progress: Asterisk/FreePBX Migration Tool

## What works
*   **Data Fetching**: The `fetch-all` action successfully fetches `/etc/asterisk` configurations, sound files, voicemails, and MySQL dumps from both old and new PBX systems. This includes handling SSH connection options for older servers and excluding specific files (like `keys` from new FreePBX installations).
*   **Data Comparison**: The `compare` action now generates a `comparison_report.txt` file. This report provides a terse, migration-focused summary of differences in `/etc/asterisk` files and MySQL database entries, listing counts for large sets of differences and individual items for smaller sets.
*   **Data Migration**: The `migrate` action is implemented to push `/etc/asterisk` configurations, sound files, voicemails, and MySQL database content from the local `old_system` data to the `new_system` PBX server.

## What's left to build
*   **Comprehensive Testing**: While core functionalities are implemented, thorough testing across various Asterisk/FreePBX versions and configurations is crucial.
*   **Enhanced Error Handling**: More granular error handling and user-friendly messages for network issues, permission problems, or command failures.
*   **Advanced MySQL Parsing**: The current MySQL dump parsing is basic. For complex FreePBX databases, a more intelligent parsing and comparison mechanism might be needed to avoid false positives or "gobbledygook" in the report.
*   **Selective Migration**: Implement options for users to selectively migrate specific configurations or database tables, rather than a full overwrite.
*   **Rollback Mechanism**: Consider adding a rollback feature in case of migration failures.
*   **User Interface**: Potentially develop a more interactive user interface beyond the command line for easier operation.

## Current status
The core `pbx_agent.py` script is functional and provides the essential `fetch`, `compare`, and `migrate` capabilities. The comparison report has been refined based on user feedback to be more concise and migration-centric.

## Known issues
*   **MySQL Password Security**: MySQL passwords are passed on the command line, which is a security concern.
*   **Basic SQL Parsing**: The `_parse_sql_dump` function is simplistic and may not handle all complexities of a FreePBX MySQL dump, potentially leading to less accurate comparison results for the database.
*   **No File Content Diff**: The comparison currently only identifies missing/extra files, not differences within file contents.
