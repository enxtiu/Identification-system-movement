#!/bin/bash
DATE=$(date +"%Y-%m-%d_%H-%M")
pg_dump -U admin -d tracking -f /backups/db_backup_$DATE.sql
echo "Backup created: db_backup_$DATE.sql"