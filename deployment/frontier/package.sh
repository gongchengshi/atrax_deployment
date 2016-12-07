#!/bin/sh

src_dir=atrax_deployment/deployment/frontier
out_dir=atrax_deployment/output/frontier
mkdir -p ${out_dir}

tar -cf ${out_dir}/frontier.tar --exclude=*.pyc --exclude=*test* \
python_common/*.py python_common/geocoding python_common/web python_common/collections \
aws/*.py aws/ec2 aws/s3 aws/sdb aws/sns aws/sqs aws/cloudwatch \
atrax/__init__.py atrax/metrics_service.py \
atrax/common atrax/management atrax/prior_versions atrax/frontier atrax/fetcher \
atrax_deployment/actions

# Add run.sh to the top level of the tar file
tar -rf ${out_dir}/frontier.tar -C ${src_dir} run.sh

rsync -t ${src_dir}/debian_env_setup.sh ${out_dir}/
