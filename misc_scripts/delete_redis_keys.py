import redis
import sys
from atrax.common.constants import DEFAULT_REDIS_PORT, LOCALHOST_IP
from atrax.common.crawl_job import CrawlJobGlossary

crawl_job_name = sys.argv[1]
glossary = CrawlJobGlossary(crawl_job_name)

redis_client = redis.Redis(LOCALHOST_IP, DEFAULT_REDIS_PORT)
keys = redis_client.keys(glossary.seen_urls_key + '*')
split_point = len(glossary.seen_urls_key)
if keys is not None:
    to_delete = []
    for key in keys:
        remaining_key = key[split_point:]
        # Todo: To make this more general purpose, take the patterns from the crawl_job.scope file
        if "siemens" not in remaining_key:
            to_delete.append(key)

    for key in to_delete:
        print "Deleting %s" % key

    num_deleted = redis_client.delete(*to_delete)
    print "Deleted %d Keys" % num_deleted
