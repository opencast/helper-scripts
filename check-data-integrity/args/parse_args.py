""" This module parses the arguments for the script and checks them for errors."""

import argparse
import getpass
from collections import namedtuple

from args.check_settings import Checks

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
    Parse the arguments and read in the digest password and return those.

    :rtype: str, bool, DigestLogin, bool, Checks
    :return: opencast url, whether to use https, the digest user and password, whether to print progress statements and which data to check
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("-o","--opencast", type=str, help="url of the opencast instance", required=True)
    parser.add_argument("-u", "--user", type=str, help="digest user", required=True)
    parser.add_argument("-p", "--password", type=str, help="digest password", required=False)
    parser.add_argument("-c", "--check", type=str, help="checks to perform", required=False,
                        choices = [Checks.DC, Checks.ACL, Checks.DC_ACL, Checks.OAIPMH, Checks.ALL], default=Checks.ALL)
    parser.add_argument('-s', "--silent", action='store_true', help="disables progress output")
    parser.add_argument('-t', "--https", action='store_true', help="enables https")
    args = parser.parse_args()

    if not (args.opencast and args.user):
        _usage(parser)

    if not args.password:

        digest_pw = getpass.getpass('No password provided, enter digest password:')
        while not digest_pw:
            digest_pw = getpass.getpass('Password cannot be empty, please try again:')
    else:
        digest_pw = args.password

    return args.opencast, args.https, DigestLogin(user= args.user, password = digest_pw), \
           args.silent, args.check