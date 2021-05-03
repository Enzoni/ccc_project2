#!/bin/bash

pip3 install -r config/requirements.txt 


echo "Running harvester"

nohup python3 btc_crawl.py -a=8 -c=Sydney     -d=btc_1 >> output_s.txt 2>&1 &
nohup python3 btc_crawl.py -a=8 -c=Melbourne  -d=btc_2 >> output_m.txt 2>&1 &
nohup python3 btc_crawl.py -a=4 -c=Brisbane   -d=btc_3 >> output_b.txt 2>&1 &
nohup python3 btc_crawl.py -a=4 -c=Perth      -d=btc_4 >> output_p.txt 2>&1 &
nohup python3 btc_crawl.py -a=3 -c=Gold_Coast -d=btc_5 >> output_g.txt 2>&1 &
nohup python3 btc_crawl.py -a=3 -c=Newcastle  -d=btc_6 >> output_n.txt 2>&1 &
