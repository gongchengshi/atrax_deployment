import sys

import redis
from aws import USWest2 as AwsConnections
from aws.sqs import cycle_queue
from atrax.common.seen_urls import SeenUrls
from atrax.common.constants import DEFAULT_REDIS_PORT, LOCALHOST_IP
from atrax.frontier.message import unpack_message
from atrax.common.crawl_job import CrawlJob
from atrax.common import domain_from_schemeless_url
from python_common.collections.pickling import pickle_set, unpickle_set


def process_message(m, seen_urls):
    try:
        url_info = unpack_message(m)
    except Exception, ex:
        return False

    url_id_and_key = (url_info.id, url_info.domain)
    if url_id_and_key in seen_urls:
        return False
    else:
        seen_urls.add(*url_id_and_key)
        return True


def print_progress(total_messages, moved_messages):
    sys.stdout.write("\rMoved: %d, Deleted %d" % (moved_messages, total_messages-moved_messages))
    sys.stdout.flush()


def main():
    crawl_job = CrawlJob(sys.argv[1])

    redis_client = redis.Redis(LOCALHOST_IP, DEFAULT_REDIS_PORT)
    keys = redis_client.keys(crawl_job.glossary.seen_urls_key + '*')
    if keys is not None:
        num_deleted = redis_client.delete(*keys)
        print "Deleted %d Keys" % num_deleted

    seen_urls = SeenUrls(crawl_job.glossary.seen_urls_key)

    print "Processing Frontier"

    processed_queues_path = 'processed_queues.set'
    processed_queues = unpickle_set(processed_queues_path)

    try:
        sqs = AwsConnections.sqs()
        for queue in sqs.get_all_queues(crawl_job.name):
            if queue.name in processed_queues:
                print "Already Processed Queue: " + queue.name
                continue
            else:
                print "Processing Queue: " + queue.name

            cycle_queue(sqs, queue,
                        egress_predicate=lambda m: process_message(m, seen_urls),
                        progress_callback=print_progress)

            processed_queues.add(queue.name)
            sys.stdout.write("\n")
    finally:
        pickle_set(processed_queues, processed_queues_path)

    items = None

    try:
        print "Processing Crawled URLs"
        sys.stdout.flush()

        i = 0
        items = crawl_job.crawled_urls.select("select itemName() from `%s`" % crawl_job.crawled_urls.name)
        for item in items:
            seen_urls.add(item.name, domain_from_schemeless_url(item.name))
            i += 1
            sys.stdout.write("\rProcessed %d" % i)
            sys.stdout.flush()

        print "\nProcessing Failed URLs"
        sys.stdout.flush()

        i = 0
        items = crawl_job.failed_urls.select("select itemName() from `%s`" % crawl_job.failed_urls.name)
        for item in items:
            seen_urls.add(item.name, domain_from_schemeless_url(item.name))
            i += 1
            sys.stdout.write("\rProcessed %d" % i)
            sys.stdout.flush()

        print "\nProcessing Redirected URLs"
        sys.stdout.flush()

        i = 0
        items = crawl_job.redirected_urls.select("select itemName() from `%s`" % crawl_job.redirected_urls.name)
        for item in items:
            seen_urls.add(item.name, domain_from_schemeless_url(item.name))
            i += 1
            sys.stdout.write("\rProcessed %d" % i)
            sys.stdout.flush()

        print "\nFinished Rebuilding Seen URLs"
    except Exception:
        # Just in case something bad happens, having the next token will allow skipping to where it left off.
        if items and items.next_token:
            print "\nNext Token:\n" + items.next_token
            with open('next_token', 'w') as next_token_file:
                next_token_file.write(items.next_token)
        raise

if __name__ == "__main__":
    main()
