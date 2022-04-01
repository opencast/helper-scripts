import os
import sys

sys.path.append(os.path.join(os.path.abspath('..'), "lib"))

import config
from args.args_error import args_error
from args.args_parser import get_args_parser
from args.digest_login import DigestLogin
from rest_requests.group_requests import create_group
from rest_requests.request_error import RequestError


def parse_args():
    """
    Parse the arguments and check them for correctness

    :return: amount of groups
    :rtype: int
    """
    parser, optional_args, required_args = get_args_parser()
    optional_args.add_argument("-a", "--amount", type=int, help="amount of groups")
    args = parser.parse_args()

    if args.amount and args.amount <= 0:
        args_error(parser, "Amount has to be positive, non-zero number")

    return args.amount


def main():
    digest_login = DigestLogin(user=config.digest_user, password=config.digest_pw)
    amount = parse_args()

    if not amount:
        amount = 100

    for i in range(1, amount + 1):
        name = str(i)
        try:
            create_group(config.admin_url, digest_login, name)
            print("Created group {}".format(name))
        except RequestError as e:
            print("Group {} couldn't be created: {}", name, e.error)


if __name__ == '__main__':
    main()
