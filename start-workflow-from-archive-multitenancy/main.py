import os
import sys
import io
import config

sys.path.append(os.path.join(os.path.abspath('..'), "lib"))

from args.digest_login import DigestLogin
from args.args_error import args_error
from args.args_parser import get_args_parser
from rest_requests.request_error import RequestError
from rest_requests.workflow_requests import start_task


def parse_args():
    """
    Parse the arguments and check them for correctness

    :return: workflow definition, directory path
    :rtype: str, str
    """
    parser, optional_args, required_args = get_args_parser()
    required_args.add_argument("-w", "--workflow", type=str, help="The workflow to start")
    required_args.add_argument("-d", "--dir", type=str, help="The path to the directory containing the event id files")
    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        args_error(parser, "Provided directory doesn't exist!")

    return args.workflow, args.dir


def main():
    digest_login = DigestLogin(user=config.digest_user, password=config.digest_pw)
    workflow_definition, directory = parse_args()

    dir_name, sub_dirs, files = next(os.walk(directory))
    for file in files:
        tenant = os.path.splitext(file)[0]
        server_url = config.url_pattern.format(tenant)
        file_path = os.path.join(directory, file)
        print("Starting with tenant {}".format(tenant))

        with io.open(file_path, 'r', newline='\n', encoding='utf8') as f:
            for event_id in f:
                event_id = event_id.rstrip('\n')
                try:
                    start_task(server_url, digest_login, workflow_definition, event_id)
                    print("Workflow started for event {}.".format(event_id))
                except RequestError as e:
                    print("Workflow couldn't be started for event: {} {}".format(event_id, e.error))


if __name__ == '__main__':
    main()
