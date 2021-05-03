#!/bin/bash

pip3 install -r config/requirements.txt 


echo "Running harvester"

nohup python3 btc_crawl.py -a=6 -s=Gold_Coast -d=btc_g >> output_g.txt 2>&1 &
nohup python3 btc_crawl.py -a=6 -s=Newcastle  -d=btc_n >> output_n.txt 2>&1 &

