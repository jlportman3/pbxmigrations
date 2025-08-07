# PBX Migration Utilities

This repository holds configuration snapshots from an old and a new
FreePBX/Asterisk installation and provides tools to help verify that the
new system replicates everything from the old one.

## compare_configs.py

`compare_configs.py` compares the configuration file sets and ASTDB
entries between two systems. It expects tarballs of `/etc/asterisk` and
text dumps of the Asterisk database (`database show` output).

### Usage

```bash
python3 compare_configs.py \
    --old-etc asterisk.old.tgz \
    --new-etc asterisk.new.tgz \
    --old-db database.old.txt \
    --new-db database.new.txt
```

The script prints files or ASTDB keys present on the old system but
missing on the new one, and highlights differing values.
