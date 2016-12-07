import sys

job_name = sys.argv[1]
prefix = sys.argv[2] if len(sys.argv) > 2 else None

if prefix is None:
    from atrax.management.aws_env.frontier_controller import FrontierController
    frontier_controller = FrontierController(job_name)
    frontier_controller.persist()
else:
    from aws import USWest2 as AwsConnections
    import aws.sqs
    from atrax.common.crawl_job import CrawlJob
    crawl_job = CrawlJob(job_name)
    aws.sqs.persist_to_s3(AwsConnections.sqs(), prefix, crawl_job.persisted_frontier_bucket)
