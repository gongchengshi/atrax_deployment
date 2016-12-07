#!/bin/bash

apt-get update

# Python
apt-get install -y python2
apt-get install -y python-dev
#apt-get install -y python-pip # this doesn't work on Trusy Tahr
wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
python get-pip.py

pip install -U awscli

# Create a memory swap space the size of physical memory
total_ram=`cat /proc/meminfo | grep MemTotal | awk '{ print $2 }'`K

fallocate -l ${total_ram} /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo "/swapfile   none    swap    sw    0   0" >> /etc/fstab

sysctl vm.swappiness=10
echo `sysctl vm.swappiness` >> /etc/sysctl.conf

sysctl vm.vfs_cache_pressure=50
echo `sysctl vm.vfs_cache_pressure` >> /proc/sys/vm/vfs_cache_pressure

# Redis needs this
sysctl vm.overcommit_memory=1
echo `sysctl vm.overcommit_memory` >> /etc/sysctl.conf

# CloudWatch Logs Agent
wget https://s3.amazonaws.com/aws-cloudwatch/downloads/latest/awslogs-agent-setup.py
chmod +x ./awslogs-agent-setup.py
./awslogs-agent-setup.py -n -r us-west-2 -c s3://atrax-configuration-management/cloudwatch_logs.config
