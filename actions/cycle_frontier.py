import sys
from aws import USWest2 as AwsConnections
from aws.sqs import cycle_queue

crawl_job_name = sys.argv[1]

queue_name = None
if len(sys.argv) > 2:
    queue_name = sys.argv[2]

sqs = AwsConnections.sqs()

if queue_name is None:
    for queue in sqs.get_all_queues(crawl_job_name):
        print "Cycling " + queue.name
        cycle_queue(sqs, queue)
else:
    queue = sqs.lookup(queue_name)
    if not queue:
        print "No queue named " + queue_name
        exit(1)
    print "Cycling " + queue.name
    cycle_queue(sqs, queue)
