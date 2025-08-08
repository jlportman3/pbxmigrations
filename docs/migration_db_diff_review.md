# Migration Review Notes: Old MySQL Database Entries Missing or Differing on New Server

This document records the review and migration decision for each database entry found in the old system but missing or differing in the new system.

---

## Example of Differences (first 20 lines):

```
+-- MySQL dump 10.13  Distrib 5.5.62, for debian-linux-gnu (x86_64)
+-- Server version	5.5.62-0ubuntu0.12.04.1-log
+/*!40101 SET NAMES utf8 */;
+/*!40101 SET character_set_client = utf8 */;
+) ENGINE=MyISAM DEFAULT CHARSET=latin1;
+INSERT INTO `admin` VALUES ('need_reload','false'),('version','2.11.0'),('default_directory','1'),('email','baron@baron.com'),('update_email','90e3a0660313953b1be3358126b116d0'),('directory28_migrated','1'),('ALLOW_SIP_ANON','no');
+/*!40101 SET character_set_client = utf8 */;
+  `username` varchar(255) NOT NULL,
+  `sections` blob NOT NULL,
+) ENGINE=MyISAM DEFAULT CHARSET=latin1;
+INSERT INTO `ampusers` VALUES ('admin','9f893391e3e856d01941117269085a5ed8e200ed','','','','*'),('baron','9f893391e3e856d01941117269085a5ed8e200ed','','','','*');
+/*!40101 SET character_set_client = utf8 */;
+  `return_ivr` tinyint(1) NOT NULL DEFAULT '0',
+  `noanswer` tinyint(1) NOT NULL DEFAULT '0',
+) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
+INSERT INTO `announcement` VALUES (1,'notinservice',4,0,'app-blackhole,hangup,1',0,0,''),(2,'MayBeRecorded',18,0,'ext-queues,1,1',0,0,''),(3,'Pickup',17,0,'app-announcement-2,s,1',0,0,''),(4,'holiday-close',21,0,'ivr-3,s,1',0,0,''),(5,'response_delayed_999',24,0,'from-did-direct,999,1',0,0,''),(6,'response_delayed_main',24,0,'app-announcement-3,s,1',0,0,''),(7,'veteransday',25,0,'ivr-3,s,1',0,0,''),(8,'problems',26,0,'ext-local,vmu100,1',0,0,''),(9,'thanksgiving_closed',27,0,'ivr-3,s,1',0,0,''),(10,'power_out',30,0,'app-blackhole,hangup,1',0,0,'2'),(11,'backlog',31,0,'from-did-direct,999,1',0,0,''),(12,'MayBeRecordedTech',18,0,'timeconditions,3,1',0,0,''),(13,'Pickup2',32,0,'app-announcement-12,s,1',0,0,''),(14,'pingmayberecorded',18,0,'ext-group,611,1',0,0,''),(15,'MayBeRecordedBilling',18,0,'ext-queues,1,1',0,0,'');
+-- Table structure for table `backup`
+DROP TABLE IF EXISTS `backup`;
+/*!40101 SET character_set_client = utf8 */;
+CREATE TABLE `backup` (
```

---

## Review and Action Plan

- **Do NOT restore the old database dump onto the new system.**
- For each `INSERT INTO` or schema difference:
    - Identify what the entry or table represents (e.g., admin user, ampuser, announcement, backup table).
    - If it is a user-facing feature (admin, ampuser, announcement), consider recreating it via the FreePBX GUI for proper schema compatibility.
    - For custom or advanced features, manually craft SQL `INSERT` or `UPDATE` statements as needed, but only after confirming compatibility with the new schema.
    - Always back up the current database before making any manual changes.
    - Document each entry reviewed and the action taken (added, skipped, or handled via GUI).

---

**Instructions:**
- Review each `INSERT INTO` or schema difference line by line.
- For each, decide:
    - Is this entry needed on the new system?
    - Is it safe to add or update, or should it be handled via the GUI?
    - If added/updated, document the SQL used and the result.
    - If skipped, document the reason.

---

**This document serves as the migration record for database entry review.**
