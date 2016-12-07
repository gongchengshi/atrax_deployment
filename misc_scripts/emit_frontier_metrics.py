import sys
import time
from aws import USWest2 as AwsConnections


job_name = sys.argv[1]
namespace = 'atrax/' + job_name

queues = AwsConnections.sqs().get_all_queues(job_name)
cw = AwsConnections.cloudwatch()

# This is only accurate when the number of non-empty queues is decreasing
while True:
    non_emtpy_queues = []
    total_messages = 0
    for queue in queues:
        count = queue.count()
        if count > 0:
            total_messages += count
            non_emtpy_queues.append(queue)
    print "%s:%s" % (len(non_emtpy_queues), total_messages)
    cw.put_metric_data(namespace=namespace,
                       name='frontier_size',
                       unit='Count',
                       value=total_messages)
    cw.put_metric_data(namespace=namespace,
                       name='num_nonempty_queues',
                       unit='Count',
                       value=len(non_emtpy_queues))
    queues = non_emtpy_queues
    time.sleep(10)
