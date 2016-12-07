import sys
from aws import USWest2 as AwsConnections
from aws.sdb import count
from atrax.common.crawl_job import CrawlJobGlossary

job_name = sys.argv[1]

crawled_urls = AwsConnections.sdb().lookup(CrawlJobGlossary(job_name).crawled_urls_table_name)

if not crawled_urls:
    exit()

num = count(crawled_urls)

print num
