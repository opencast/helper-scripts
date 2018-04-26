""" This module parses the arguments for the script and checks them for errors."""

import argparse
import getpass
from collections import namedtuple

DigestLogin = namedtuple('DigestLogin', ['user', 'password'])

def _usage(parser):
    """
    Print usage of script in case of error during args parsing and quit the script.

    :param parser:
    :type parser: argparse.ArgumentParser
    """

    parser.print_usage()
    parser.exit()

def parse_args():
    """
    Parse the arguments and read in the digest password.
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("-o","--opencast", type=str, help="url of running opencast instance", required=True)
    parser.add_argument('-s', "--https", action='store_true', help="enables https")

    parser.add_argument("-u", "--user", type=str, help="digest user", required=True)
    parser.add_argument("-p", "--password", type=str, help="digest password", required=False)

    parser.add_argument("-b","--backup", type=str, help="path to backup", required=True)
    parser.add_argument("-m", "--media-packages", type=str, nargs='+', help="list of media package ids to be restored", required=False)
    parser.add_argument("-t","--tenant", type=str, help="tenant id", required=False)
    parser.add_argument('-w', "--workflow-id", type=str, help="id for workflow on ingest", required = False)
    parser.add_argument('-l', "--lastversion", action='store_true', help="always recover last version of mediapackage")

    args = parser.parse_args()

    if not (args.opencast and args.user and args.backup):
        _usage(parser)

    if not args.password:

        digest_pw = getpass.getpass('No password provided, enter digest password:')
        while not digest_pw:
            digest_pw = getpass.getpass('Password cannot be empty, please try again:')
    else:
        digest_pw = args.password

    digest_login = DigestLogin(user= args.user, password = digest_pw)

    return args.opencast, args.https, digest_login , args.backup, args.media_packages, args.tenant, args.workflow_id, \
           args.lastversion