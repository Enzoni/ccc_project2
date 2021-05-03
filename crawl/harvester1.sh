#!/bin/bash

pip3 install -r config/requirements.txt 


echo "Running harvester"

nohup python3 btc_crawl.py -a=4 -s=Sydney     -d=btc_s >> output_s.txt 2>&1 &
nohup python3 btc_crawl.py -a=4 -s=Melbourne  -d=btc_m >> output_m.txt 2>&1 &


