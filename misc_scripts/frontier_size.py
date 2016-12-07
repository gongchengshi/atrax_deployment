import sys
from aws import USWest2 as AwsConnections
from aws.sqs import count_messages

job_name = sys.argv[1]

print count_messages(AwsConnections.sqs(), job_name)
