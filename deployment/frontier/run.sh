#!/bin/sh

cd /usr/local/packages/frontier
export PYTHONPATH=`pwd`:${PYTHONPATH}
python -O atrax/frontier/frontier_service.py -d $@
