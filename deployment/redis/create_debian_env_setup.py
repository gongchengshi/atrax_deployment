#! /usr/bin/python2

import StringIO
from jinja2 import Environment, FileSystemLoader
import os

import base64


abs_path = os.path.dirname(os.path.realpath(__file__))
env = Environment(loader=FileSystemLoader(abs_path))
template = env.get_template('debian_env_setup.sh.jinja2')
with open(os.path.join(abs_path, 'redis.conf'), 'r') as redis_config_file:
    output = StringIO.StringIO()
    base64.encode(redis_config_file, output)
    script = template.render(redis_config=output.getvalue())
    output.close()

DIR = 'atrax_deployment/deployment/redis/'
with open(DIR + 'debian_env_setup.sh', 'w') as env_setup_file:
    env_setup_file.write(script)
