#!/usr/bin/python2
import time
from os import path


def build_setup_script(modules):
    template_dir = path.join(path.dirname(path.realpath(__file__)), '../deployment')

    with open(path.join(template_dir, 'debian_setup.sh')) as debian_setup_file:
        debian_setup = debian_setup_file.read()

    with open(path.join(template_dir, 'update_module.sh')) as update_module_file:
        update_module = update_module_file.read()

    setup_script = debian_setup + '\n'

    for module in modules:
        setup_script += "MODULE_NAME=%s\n%s\n" % (module, update_module)

    setup_script += "\nshutdown -h now\n"

    return setup_script


import argparse
from atrax.management.aws_env.constants import *
from aws import USWest2 as AwsConnections
from aws.ec2 import wait_for_state, VirtualizationType


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--virt', default=VirtualizationType.HVM,
                        choices=VirtualizationType.__dict__.values(), nargs='?')
    parser.add_argument('-n', '--name', type=str, required=True)
    parser.add_argument('modules', choices=ModuleNames.__dict__.values(), nargs='+')
    args = parser.parse_args()

    if ModuleNames.FRONTIER in args.modules:
        base_image_id = FRONTIER_BASE_IMAGE_ID
    elif ModuleNames.FETCHER in args.modules:
        base_image_id = HVM_FETCHER_BASE_IMAGE_ID if args.virt == VirtualizationType.HVM else PARAVIRTUAL_FETCHER_BASE_IMAGE_ID
    else:
        base_image_id = DEFAULT_BASE_IMAGE_ID

    instance_type = 'm3.medium' if args.virt == VirtualizationType.HVM else 'm1.medium'
    setup_script = build_setup_script(args.modules)

    ec2 = AwsConnections.ec2()
    reservation = ec2.run_instances(image_id=base_image_id, instance_type=instance_type,
                                    key_name=EC2_KEY_PAIR_NAME, security_groups=['InternalSSH'],
                                    instance_initiated_shutdown_behavior='stop',
                                    instance_profile_arn=STANDARD_INSTANCE_ARN, user_data=setup_script)

    instance = reservation.instances[0]

    ec2.create_tags([instance.id], {NAME_TAG_NAME: args.name + ' AMI'})

    wait_for_state(instance, "stopped", timeout_seconds=1200)

    created = str(int(time.time()))
    image_id = ec2.create_image(instance.id, args.name + '-' + created)
    ec2.create_tags([image_id],
                    {
                        NAME_TAG_NAME: args.name,
                        PACKAGES_TAG_NAME: ' '.join(args.modules),
                        CREATED_TAG_NAME: created
                    })


if __name__ == "__main__":
    main()
    # with open('setup_script.sh', 'w') as setup_script_file:
    #     setup_script_file.write(build_setup_script(['frontier', 'redis']))
