# Project Brief: Asterisk/FreePBX Migration Program

## Core Requirements and Goals

The primary goal of this project is to create a robust and intelligent migration program to facilitate the transfer of configurations, data, sound files, and voicemails from an ancient Asterisk/FreePBX version to a new version.

The program aims to:
1.  **Automate Data Collection**: Efficiently fetch critical system data from both old and new PBX servers.
2.  **Provide Comprehensive Comparison**: Identify differences between the old and new system configurations and data, presenting these differences in a human-readable format.
3.  **Enable Controlled Migration**: Facilitate the transfer of identified missing or differing components from the old system to the new system.

## Project Scope

The current scope focuses on:
*   `/etc/asterisk` configuration files.
*   MySQL database dumps (specifically the `asterisk` database).
*   Asterisk sound files (`/var/lib/asterisk/sounds`).
*   Asterisk voicemail data (`/var/spool/asterisk/voicemail`).

Future considerations may include other system components or more granular migration controls.
