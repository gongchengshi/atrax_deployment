#!/bin/bash

src_dir=atrax_deployment/deployment/redis
out_dir=atrax_deployment/output/redis
mkdir -p ${out_dir}

tar -cf ${out_dir}/redis.tar -C ${src_dir} run.sh redis.conf

rsync -t ${src_dir}/redis-2.8.17.tar.gz ${out_dir}/
rsync -t ${src_dir}/debian_env_setup.sh ${out_dir}/
