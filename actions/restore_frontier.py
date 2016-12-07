import sys
from atrax.management.aws_env.frontier_controller import FrontierController

job_name = sys.argv[1]

frontier_controller = FrontierController(job_name)
frontier_controller.restore()
