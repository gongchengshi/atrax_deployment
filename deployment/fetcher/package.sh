#!/bin/sh

src_dir=atrax_deployment/deployment/fetcher
out_dir=atrax_deployment/output/fetcher
mkdir -p ${out_dir}

tar -cf ${out_dir}/fetcher.tar --exclude=*.pyc --exclude=*test* \
python_common/*.py python_common/geocoding python_common/web python_common/collections \
aws/*.py aws/ec2 aws/s3 aws/sdb aws/sns aws/sqs aws/cloudwatch \
atrax/__init__.py atrax/common atrax/management atrax/prior_versions atrax/frontier atrax/fetcher

# Add run.sh to the top level of the tar file
tar -rf ${out_dir}/fetcher.tar -C ${src_dir} run.sh

rsync -t ${src_dir}/debian_env_setup.sh ${out_dir}/
