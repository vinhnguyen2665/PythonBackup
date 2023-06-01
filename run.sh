#!/bin/sh
echo "Start Backup Service"
#source /opt/database_backup/DatabaseBackup/bin/activate
#python --version
touch log.pid
source env/bin/activate
python3 ./main.py >>./log.pid
ps aux | grep main.py
echo "Start OCR Success"
