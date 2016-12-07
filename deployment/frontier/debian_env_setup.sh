#!/bin/sh

# Boto
pip install -U boto

# ZeroMQ
apt-get install libzmq3 -y
apt-get install libzmq-dev -y
pip install -U pyzmq

# Redis Client
apt-get install libhiredis-dev -y
pip install -U redis
pip install -U hiredis
pip install -U cython

# PyreBloom
wget -O pyrebloom.zip https://github.com/seomoz/pyreBloom/archive/master.zip
apt-get install unzip -y
unzip -u pyrebloom.zip
pip install -U setuptools
cd pyreBloom-master
python setup.py install

# Misc
pip install -U jinja2
pip install -U argparse
pip install -U waiting

# Fetcher

# libxml2
apt-get install -y libxml2-dev
apt-get install -y libxslt-dev
apt-get install -y zlib1g-dev
pip install -U lxml

# Misc
pip install -U urllib3
pip install -U beautifulsoup4
pip install -U dnspython
pip install -U requests
pip install -U urlnorm
pip install -U tinycss
pip install -U robotexclusionrulesparser
pip install -U tldextract
pip install -U python-dateutil
pip install -U reppy
pip install -U nilsimsa
pip install -U xxhash
pip install -U pybst
