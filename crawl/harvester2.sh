#!/bin/bash

pip3 install -r config/requirements.txt 


echo "Running harvester"

nohup python3 btc_crawl.py -a=5 -s=Brisbane   -d=btc_b >> output_b.txt 2>&1 &
nohup python3 btc_crawl.py -a=5 -s=Perth      -d=btc_p >> output_p.txt 2>&1 &


