# Step-by-Step Plan for Safe Asterisk/FreePBX Migration (Incremental/Selective Approach)

> **Context:**  
> The new server is already up, configured, and about 99% complete.  
> The goal is to bring over only what is truly missing or essential from the old system, without overwriting or restoring the entire database or configuration.  
> **Restoring a full backup from the old system onto the new system is NOT safe and will cause major issues.**  
> All database differences must be carefully reviewed and handled individually.

---

## 1. Snapshot the New Server (Linode VM)

- **Log in to your Linode dashboard.**
- Take a full snapshot of the new PBX VM before making any changes.
- This snapshot provides a rollback point in case of any migration issues.

---

## 2. Review the Migration Report

- Open `comparison_report.txt` for a summary of:
    - Files present in the old `/etc/asterisk` but missing in the new.
    - Files present in the new `/etc/asterisk` but not in the old (review for possible cleanup).
    - Database entries present in the old system but missing in the new.
    - Database entries with different values.

---

## 3. Configuration Files: Selective Copy

- **Do NOT overwrite the entire `/etc/asterisk` directory.**
- For each file listed as missing in the new system:
    - Review its content and relevance.
    - If it is a custom dialplan, context, or other essential config, copy it to the new system.
    - If it is obsolete or replaced by new features, skip it.
    - Use `diff` to compare file contents before copying.
    - Example:
      ```bash
      diff data/old_system/asterisk/extensions_custom.conf /etc/asterisk/extensions_custom.conf
      # If needed:
      scp data/old_system/asterisk/extensions_custom.conf [user]@[new_server]:/etc/asterisk/
      ```
- For files present in the new system but not in the old:
    - Review for possible cleanup, but **do not delete unless you are certain** they are not needed.

---

## 4. Database Entries: Manual, Careful Handling

- **Do NOT restore the old database dump onto the new system.**
- For each missing or differing entry:
    - Identify what the entry represents (e.g., extension, trunk, route, voicemail box, custom table).
    - If it is a user-facing feature (extension, voicemail, etc.), consider recreating it via the FreePBX GUI for proper schema compatibility.
    - For custom or advanced features, manually craft SQL `INSERT` or `UPDATE` statements as needed, but only after confirming compatibility with the new schema.
    - Always back up the current database before making any manual changes.
    - Example workflow:
      1. Use `mysql` CLI or FreePBX GUI to inspect the current state.
      2. For each missing entry, decide if it should be added, and if so, add it using the GUI or a carefully crafted SQL statement.
      3. For differing entries, review both old and new values, and update only if necessary and safe.

---

## 5. Sound Files and Voicemails

- If there are custom sound files or voicemails missing on the new system:
    - Use `rsync` to copy only the missing files.
    - Do not overwrite existing files unless you are certain they are outdated or incorrect.
    - Example:
      ```bash
      rsync -avz --ignore-existing data/old_system/sounds/ [user]@[new_server]:/var/lib/asterisk/sounds/
      rsync -avz --ignore-existing data/old_system/voicemail/ [user]@[new_server]:/var/spool/asterisk/voicemail/
      ```

---

## 6. Restart and Validate

- After making changes, restart Asterisk/FreePBX services:
    ```bash
    systemctl restart asterisk
    systemctl restart freepbx
    ```
- Validate:
    - Test all extensions, trunks, voicemails, and custom features.
    - Check logs for errors or warnings.
    - Confirm that the system is stable and all intended features are working.

---

## 7. Document All Changes

- Keep a log of every file copied, database entry added/modified, and any other manual intervention.
- This will help with troubleshooting and future audits.

---

**Summary:**  
- Take a Linode snapshot before any changes.
- Review and selectively copy only essential missing config files.
- Handle database differences one entry at a time, using the GUI or carefully crafted SQL, never a full restore.
- Sync only missing sound files/voicemails.
- Restart and validate.
- Document every change.

This incremental, selective approach ensures the new system remains stable and avoids the risks of overwriting or restoring incompatible data.
