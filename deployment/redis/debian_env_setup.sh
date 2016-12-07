#!/bin/sh

apt-get install make -y

cd /usr/local/packages/redis

# Redis Server
rm -rf redis-2.8.17
rm -rf redis_server
tar -xf redis-2.8.17.tar.gz
cd redis-2.8.17
make
cd ..
mv redis-2.8.17 redis_server
