from aws import USWest2 as AwsConnections

sqs = AwsConnections.sqs()

all_queues = sqs.get_all_queues()

for queue in all_queues:
    msg = queue.read(wait_time_seconds=0)
    if msg is None:
        queue.delete()
