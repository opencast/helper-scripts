""" This module parses the arguments for the script and checks them for errors."""

import argparse
import getpass
import os
from collections import namedtuple

import sys

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
    parser.add_argument("-t", "--tenants", type=str, nargs='+', help="list of tenants to check", required=False)
    parser.add_argument("-e", "--exclude-tenants", type=str, nargs='+', help="list of tenants to be excluded", required=False)
    parser.add_argument("-u", "--user", type=str, help="digest user", required=True)
    parser.add_argument("-p", "--password", type=str, help="digest password", required=False)
    parser.add_argument("-c", "--check", type=str, help="checks to perform", required=False,
                        choices = [Checks.DC, Checks.ACL, Checks.DC_ACL, Checks.OAIPMH, Checks.ALL], default=Checks.ALL)
    parser.add_argument('-s', "--silent", action='store_true', help="disables progress output")
    parser.add_argument('-l', "--https", action='store_true', help="enables https")
    parser.add_argument('-n', "--no-fancy-output", action='store_true', help="disables fancy output including the progress bars")
    parser.add_argument('-r', "--no-series-error", action='store_true', help="enables treating events without series as malformed")
    parser.add_argument('-d', "--results-dir", type = str, help="directory where results should be stored")


    args = parser.parse_args()

    if not args.opencast and args.user:
        _usage(parser)

    if args.exclude_tenants and args.tenants:
        print("The options --tenants and --exclude-tenants can't both be defined.", file=sys.stderr)
        _usage(parser)

    if args.silent and args.no_fancy_output:
        print("The options --silent and --no-fancy-output can't both be defined.", file=sys.stderr)
        _usage(parser)

    if not args.password:

        digest_pw = getpass.getpass('No password provided, enter digest password:')
        while not digest_pw:
            digest_pw = getpass.getpass('Password cannot be empty, please try again:')
    else:
        digest_pw = args.password


    if args.results_dir:
        results_dir = os.path.abspath(args.results_dir)
        if not os.path.isdir(results_dir):
            print("Directory for results does not exist", file=sys.stderr)
            _usage(parser)
    else:
        results_dir = os.getcwd()


    return args.opencast, args.tenants, args.exclude_tenants, args.https, DigestLogin(user= args.user, password = digest_pw), \
           args.silent, args.no_fancy_output, args.no_series_error, args.check, results_dir