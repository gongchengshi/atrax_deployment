#!/bin/sh

cd /usr/local/packages/fetcher
num_procs=2

export PYTHONPATH=`pwd`:${PYTHONPATH}
python -O atrax/fetcher/fetcher_service.py -d -c ${num_procs} --env aws $@
