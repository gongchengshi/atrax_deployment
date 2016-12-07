import sys
from atrax.management.aws_env.crawl_job_controller import CrawlJobController

job_name = sys.argv[1]
job = CrawlJobController(job_name)
job.destroy()
