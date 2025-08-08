# Migration Review Notes: Old `/etc/asterisk` Files Missing on New Server

This document records the review and migration decision for each configuration file found in the old system but missing in the new system.

---

## Not to be Copied (Obsolete, Deprecated, or Not Needed)

- ais.conf — Sample for experimental res_ais, not needed.
- app_mysql.conf — For deprecated app_mysql, not needed unless legacy dialplan uses MYSQL().
- asterisk.conf.bak — Backup file, not needed.
- ccss_general_additional.conf — Likely auto-generated, not needed.
- ccss_general_custom.conf — Likely auto-generated, not needed.
- cdr_custom.conf — Legacy CDR config, not needed if using CDR_ADAPTIVE_ODBC or new CDR modules.
- cdr_mysql.conf — Deprecated, not needed.
- cdr_mysql.conf.bak — Backup, not needed.
- cdr_sqlite3_custom.conf — Not needed unless using SQLite3 CDR backend.
- cdr_syslog.conf — Not needed unless using syslog for CDR.
- cel_custom.conf — Not needed unless using custom CEL backend.
- cel_sqlite3_custom.conf — Not needed unless using SQLite3 CEL backend.
- chan_dahdi.conf.template — Template, not needed.
- chan_ooh323.conf — Old H.323 channel driver, not needed.
- confbridge.conf.save — Backup, not needed.
- extensions.conf.0 — Backup, not needed.
- extensions_custom.conf.sample — Sample, not needed.
- freepbx_featurecodes.conf.template — Template, not needed.
- freepbx_menu.conf.template — Template, not needed.
- gtalk.conf — Deprecated, not needed.
- h323.conf — Deprecated, not needed.
- iax.conf.0 — Backup, not needed.
- jabber.conf — Deprecated, not needed.
- jingle.conf — Deprecated, not needed.
- logger.conf.save — Backup, not needed.
- manager.conf.2.7.0.bak — Backup, not needed.
- manager.conf.2.8.0.bak — Backup, not needed.
- misdn.conf — Deprecated, not needed.
- modem.conf — Deprecated, not needed.
- muted.conf — Not needed.
- oss.conf — Not needed.
- pbxid — Not needed.
- phone.conf — Not needed.
- res_config_sqlite.conf — Not needed unless using SQLite3 for config.
- res_digium_phone_additional.conf — Not needed unless using Digium phones.
- res_digium_phone_applications.conf — Not needed unless using Digium phones.
- res_digium_phone_devices.conf — Not needed unless using Digium phones.
- res_digium_phone_firmware.conf — Not needed unless using Digium phones.
- rpt.conf — Not needed unless using app_rpt.
- sip.conf.bak — Backup, not needed.
- sip_general_custom.conf.save — Backup, not needed.
- sip_notify.conf.bak — Backup, not needed.
- sip_notify_endpointman.conf — Not needed unless using endpoint manager.
- swift.conf — Not needed unless using Swift TTS.
- t1 — Not needed.
- t2 — Not needed.
- usbradio.conf — Not needed unless using usbradio.
- version — Not needed.
- vm_email.inc.bak — Backup, not needed.
- vpb.conf — Not needed.
- zapata.conf.template — Template, not needed.

### Files in backup subdirectory:
- backup/ccss.conf.bk.1742413583 — Backup, not needed.
- backup/cel.conf.bk.1476716045 — Backup, not needed.
- backup/cel_odbc.conf.bk.1476716045 — Backup, not needed.
- backup/http.conf.bk.1476715994 — Backup, not needed.
- backup/udptl.conf.bk.1476715994 — Backup, not needed.

---

## [Action Required] — Review individually for possible migration

- confbridge.conf.save — If you have custom ConfBridge settings, review and merge as needed.
- muted.conf — If you use custom mute/unmute features, review.
- parking_additional.inc — If you use custom parking lot settings, review.
- vm_email.inc — If you use custom voicemail email templates, review.
- vm_general.inc — If you use custom voicemail general settings, review.

---

**Summary:**  
- All files above have been reviewed.  
- Only files with custom dialplan logic, voicemail, parking, or other user-specific configuration should be considered for migration.  
- All others are obsolete, deprecated, or not needed for a modern FreePBX/Asterisk deployment.

**This document serves as the migration record for config file review.**
