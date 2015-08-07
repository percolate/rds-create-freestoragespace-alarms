# rds-create-freestoragespace-alarms

[![Circle CI](https://circleci.com/gh/percolate/rds-create-freestoragespace-alarms.svg?style=svg)](https://circleci.com/gh/percolate/rds-create-freestoragespace-alarms)

Automate the creation of RDS Freestoragespace Alarms.
The `Low-Freestoragespace` lower-bound limit in the script is 20%, but this can be altered.

# Quick Start
```bash
"""rds_create_freestoragespace_alarms

Script used to create a below 20 pct. Low-FreeStorageSpace alarm
in AWS CloudWatch for all RDS instances

Usage:
    rds_create_freestoragespace_alarms [options]
    rds_create_freestoragespace_alarms [-h | --help]

Options:
     --debug   Don't send data to AWS
"""
```

# Install
```bash
$ pip install rds_create_freestoragespace_alarms
```
