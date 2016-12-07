#!/usr/bin/python

import sys
from atrax.management.aws_env.crawl_job_controller import CrawlJobController
from atrax.management.crawl_job_state import CrawlJobState

job_name = sys.argv[1]
job = CrawlJobController(job_name)
job.state.set(CrawlJobState.STOPPED)
job.start()
