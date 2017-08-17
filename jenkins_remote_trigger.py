from __future__ import print_function
import argparse
from jenkinsapi.jenkins import Jenkins

__version__ = '0.1.0'


def main():
    """ parse command line options and run commands.
    """
    parser = argparse.ArgumentParser(
        description='A Jenkins job trigger.')

    parser.add_argument(
        '-V', '--version', dest='version', action='store_true',
        help="show version")
    parser.add_argument(
        '--host', help="Specify Jenkins host")
    parser.add_argument(
        '--username', help="Specify Jenkins auth username")
    parser.add_argument(
        '--password', help="Specify Jenkins auth password")
    parser.add_argument(
        '--job-name', help="Specify Jenkins job name to be triggered")
    parser.add_argument(
        '--mail-recepients', help="Specify mail recepients.")

    args = parser.parse_args()

    if args.version:
        print(__version__)
        exit(0)

    if not (args.host and args.username and args.password):
        print("Remote Jenkins auth info missing.")
        exit(1)

    if not args.job_name:
        print("Remote Jenkins job name not specified.")
        exit(1)

    return trigger(args)

def trigger(args):
    """ trigger remote Jenkins to build job.
    """
    jenkins_client = Jenkins(
        args.host,
        username=args.username,
        password=args.password
    )
    print("===== Start to initialize remote Jenkins job {}.".format(args.job_name))
    params = {
        "MAIL_RECEPIENTS": args.mail_recepients
    }
    job = jenkins_client[args.job_name]
    queue_item = job.invoke(build_params=params)

    print("===== Remote Jenkins job invoked, block until build complete.")
    queue_item.block_until_complete()

    build = queue_item.get_build()
    build_status = build.get_status()
    build_number = build.get_number()
    print("===== Remote Jenkins job #{} finished, build status: {}.".format(
        build_number, build_status))

    return 0 if build_status == "SUCCESS" else 1


if __name__ == '__main__':
    main()
