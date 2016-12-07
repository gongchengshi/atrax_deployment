import sys
import time
from aws import USWest2 as AwsConnections
from aws.sqs import get_queue_age

job_name = sys.argv[1]
now = time.time()

queues = AwsConnections.sqs().get_all_queues(job_name)

queue_ages = sorted([(queue, int(get_queue_age(queue))) for queue in queues], key=lambda t: t[1], reverse=True)

for queue, age in queue_ages:
    if age == 0:
        break
    days_old = age/60.0/60.0/24.0
    print queue.name, str(days_old)
