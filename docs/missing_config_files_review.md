# Review: Old `/etc/asterisk` Files Missing on New Server

Below is a list of configuration files and templates present in the old system's `/etc/asterisk` but missing from the new system.  
**Do NOT copy all files blindly.**  
For each file, review its content and relevance. Only copy files that are essential for your current PBX setup.

---

## Files to Review

- ais.conf
- app_mysql.conf
- asterisk.conf.bak
- ccss_general_additional.conf
- ccss_general_custom.conf
- cdr_custom.conf
- cdr_mysql.conf
- cdr_mysql.conf.bak
- cdr_sqlite3_custom.conf
- cdr_syslog.conf
- cel_custom.conf
- cel_sqlite3_custom.conf
- chan_dahdi.conf.template
- chan_ooh323.conf
- confbridge.conf.save
- extensions.conf.0
- extensions_custom.conf.jlp
- extensions_custom.conf.sample
- features.conf.0
- freepbx_featurecodes.conf.template
- freepbx_menu.conf.template
- gtalk.conf
- h323.conf
- iax.conf.0
- jabber.conf
- jingle.conf
- logger.conf.save
- manager.conf.2.7.0.bak
- manager.conf.2.8.0.bak
- misdn.conf
- modem.conf
- muted.conf
- oss.conf
- parking_additional.inc
- pbxid
- phone.conf
- res_config_sqlite.conf
- res_digium_phone_additional.conf
- res_digium_phone_applications.conf
- res_digium_phone_devices.conf
- res_digium_phone_firmware.conf
- rpt.conf
- sip.conf.bak
- sip_general_custom.conf.save
- sip_notify.conf.bak
- sip_notify_endpointman.conf
- swift.conf
- t1
- t2
- usbradio.conf
- version
- vm_email.inc
- vm_email.inc.bak
- vm_general.inc
- vpb.conf
- zapata.conf.template

### Files in backup subdirectory:
- backup/ccss.conf.bk.1742413583
- backup/cel.conf.bk.1476716045
- backup/cel_odbc.conf.bk.1476716045
- backup/http.conf.bk.1476715994
- backup/udptl.conf.bk.1476715994

---

**Instructions:**
- For each file, check if it contains custom dialplan logic, device definitions, or other critical configuration.
- If unsure, compare the file's content with the new system or consult documentation.
- Only copy files that are required for your current PBX features or customizations.
- Document any files you copy or modify for future reference.

---

**Note:**  
Some files may be obsolete, deprecated, or replaced by new configuration practices (e.g., migration from `chan_sip` to `pjsip`).  
Always validate after copying and before reloading Asterisk/FreePBX.
