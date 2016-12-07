#!/usr/bin/python2
import argparse
import subprocess
import sys
from datetime import datetime


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('module', type=str)
    args = parser.parse_args()

    package_command_format = 'atrax_deployment/deployment/%s/package.sh'
    modules = ['fetcher', 'frontier', 'redis', 'controller']

    if args.module in modules:
        print subprocess.check_output(package_command_format % args.module)
    elif args.module == 'all':
        for module in modules:
            print subprocess.check_output(package_command_format % module)
    else:
        print 'Unknown module name: %s' % args.module
        return 1

    sync_command = 'aws s3 sync "atrax_deployment/output" "s3://atrax-configuration-management/packages"'
    print subprocess.check_output(sync_command, shell=True)

    print "Finished: %s" % datetime.now()

    return 0

if __name__ == "__main__":
    sys.exit(main())
