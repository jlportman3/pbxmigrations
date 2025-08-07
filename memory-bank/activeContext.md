# Active Context: Asterisk/FreePBX Migration Tool Development

## Current work focus
The primary focus has been on developing and refining the core functionalities of the `pbx_agent.py` script, specifically:
*   **Data Fetching**: Implementing robust methods to pull `/etc/asterisk` configurations, MySQL dumps, sound files, and voicemails from both old and new PBX systems.
*   **Data Comparison**: Enhancing the comparison logic to identify differences in configuration files and database entries.
*   **Migration Logic**: Developing functions to push identified data from the old system to the new one.
*   **Reporting**: Improving the clarity and conciseness of the comparison report.

## Recent changes
*   **`pbx_agent.py`**:
    *   Added `SOUND_FILES_PATH` and `VOICEMAIL_PATH` constants.
    *   Replaced `fetch_etc_asterisk` with a more generic `fetch_directory` function to handle various directory fetches (configs, sounds, voicemails).
    *   Updated `fetch-all` action to use `fetch_directory` for all relevant paths.
    *   Added `push_directory` and `push_mysql_dump` functions for migration.
    *   Introduced a new `migrate` action to orchestrate the pushing of data from old to new.
    *   Refactored comparison logic into `generate_comparison_report` function.
    *   Improved `compare` action output to be terse and migration-focused, listing counts for large differences and explicit migration instructions.

## Next steps
*   **Testing**: Thoroughly test all `fetch-all`, `compare`, and `migrate` actions in various scenarios.
*   **Error Handling**: Enhance error handling and logging for more robust operations.
*   **User Feedback Integration**: Continue refining the comparison report based on user feedback to ensure it meets their needs for clarity and actionability.
*   **Documentation**: Ensure all functionalities are well-documented within the code and in the `README.md`.

## Active decisions and considerations
*   The `_parse_sql_dump` function is currently a basic key-value parser. For more complex SQL dumps, a more sophisticated parser might be needed to avoid "gobbledygook" in the report if the current terse output is still insufficient.
*   The `migrate` action performs a direct push/import. Consideration for more granular control over migration (e.g., selective table import, merging config files) might be needed in the future.
*   SSH authentication relies on `SSH_USER` and assumes key-based authentication is set up. Password handling for MySQL is currently in the command line, which is noted as a security risk for shared systems.
