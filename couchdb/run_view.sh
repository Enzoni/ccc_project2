#!/bin/sh

pip3 install couchdb

nohup python3 setup_db.py >> output.txt 2>&1
