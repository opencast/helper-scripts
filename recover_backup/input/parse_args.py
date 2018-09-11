""" This module parses the arguments for the recover and checks them for errors."""

import os

from args.args_error import args_error
from args.args_parser import get_args_parser
from args.digest_login import read_digest_password, DigestLogin


def parse_args():
    """
    Parse the arguments, check them for correctness, read in the digest password if necessary, and return everything.

    :return: Opencast URL, Whether to use https, digest user and password, path to backup of archive, list of
    media packages to be recovered, tenant id, workflow_id, whether to use the last version of a media package
    :rtype: str, bool, DigestLogin, str, list, str, str, bool
    """

    parser, optional_args, required_args = get_args_parser()

    required_args.add_argument("-o", "--opencast", type=str, help="url of running opencast instance without protocol",
                               required=True)
    optional_args.add_argument('-s', "--https", action='store_true', help="enables https")

    required_args.add_argument("-u", "--user", type=str, help="digest user", required=True)
    optional_args.add_argument("-p", "--password", type=str, help="digest password")

    required_args.add_argument("-b", "--backup", type=str, help="path to backup", required=True)
    optional_args.add_argument("-m", "--media-packages", type=str, nargs='+', help="list of media package ids to be "
                               "restored", required=False)
    optional_args.add_argument("-t", "--tenant", type=str, help="tenant id")
    optional_args.add_argument('-w', "--workflow-id", type=str, help="id for workflow on ingest")
    optional_args.add_argument('-l', "--lastversion", action='store_true', help="always recover last version of "
                               "media package")

    args = parser.parse_args()

    if not (args.opencast and args.user and args.backup):
        args_error(parser)

    if not os.path.isdir(args.backup):
        args_error(parser, "Backup directory does not exist.")

    if not args.password:

        digest_pw = read_digest_password()
    else:
        digest_pw = args.password

    digest_login = DigestLogin(user=args.user, password=digest_pw)

    return args.opencast, args.https, digest_login, args.backup, args.media_packages, args.tenant, args.workflow_id, \
        args.lastversion
