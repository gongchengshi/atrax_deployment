import sys
import time
from atrax.management.aws_env.crawl_job_controller import CrawlJobController

job_name = sys.argv[1]

job = CrawlJobController(job_name)

print "Pausing..."
job.pause()
print "Paused"
time.sleep(3)
print "Starting..."
job.start()
