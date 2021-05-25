#!/bin/sh

# COMP90024 Assignment 2
# Team: 38
# City: Melbourne
# Members:
# Ziran Gu (1038782)
# Jueying Wang (1016724)
# Yifei Zhou(980429)
# Jiakai Ni (988303)
# Ziyue Liu (1036109)


pip3 install couchdb

nohup python3 setup_db.py >> output.txt 2>&1
