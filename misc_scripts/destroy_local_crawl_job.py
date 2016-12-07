import os
import redis
import sys
from atrax.common.constants import LOCALHOST_IP, DEFAULT_REDIS_PORT
from atrax.management.local_env.crawl_job_controller import LocalCrawlJobController
from aws import USWest2 as AwsConnections
import shutil

job_name = sys.argv[1]


def reset_seen_urls():
    print "resetting seen urls"
    host=LOCALHOST_IP
    port=DEFAULT_REDIS_PORT
    redis_conn = redis.Redis(host, port)
    redis_conn.flushall()


def delete_local_config_dir():
    crawl_job_dir = os.path.join('/usr/local/crawl_jobs/', job_name)
    if os.path.exists(crawl_job_dir):
        shutil.rmtree(crawl_job_dir)


def reset_frontier():
    print "resetting frontier"
    for queue in AwsConnections.sqs().get_all_queues(job_name):
        queue.delete()

    delete_local_config_dir()
    reset_seen_urls()


def reset_all():
    print "resetting all"
    job = LocalCrawlJobController(job_name)
    job.destroy()
    reset_frontier()


reset_all()
