""" This module parses the arguments for the script and checks them for errors."""

import argparse
import os

from check.args.check_settings import Checks
from shared.args.args_error import args_error
from shared.args.digest_login import read_digest_password, DigestLogin


def parse_args():
    """
    Parse the arguments, check them, read in the digest password if necessary, and return everything.

    :rtype: str, list, list, bool, DigestLogin, bool, bool, bool, Checks, str
    :return: opencast url, chosen tenants, excluded tenants, whether to use https, the digest user and password,
             whether to print progress statements and whether to print progress bars, whether events without series are
             considered malformed, which data to check and the results directory
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--opencast", type=str, help="url of the opencast instance", required=True)
    parser.add_argument("-t", "--chosen-tenants", type=str, nargs='+', help="list of tenants to check", required=False)
    parser.add_argument("-e", "--excluded-tenants", type=str, nargs='+', help="list of tenants to be excluded",
                        required=False)
    parser.add_argument("-u", "--user", type=str, help="digest user", required=True)
    parser.add_argument("-p", "--password", type=str, help="digest password", required=False)
    parser.add_argument("-c", "--check", type=str, help="checks to perform", required=False,
                        choices=[Checks.DC, Checks.ACL, Checks.DC_ACL, Checks.OAIPMH, Checks.ALL], default=Checks.ALL)
    parser.add_argument('-s', "--silent", action='store_true', help="disables progress output")
    parser.add_argument('-l', "--https", action='store_true', help="enables https")
    parser.add_argument('-n', "--no-fancy-output", action='store_true',
                        help="disables fancy output including the progress bars")
    parser.add_argument('-r', "--no-series-error", action='store_true',
                        help="enables treating events without series as malformed")
    parser.add_argument('-d', "--results-dir", type=str, help="directory where results should be stored")

    args = parser.parse_args()

    if not args.opencast and args.user:
        args_error(parser)

    if args.excluded_tenants and args.chosen_tenants:
        args_error(parser, "The options --chosen-tenants and --excluded-tenants can't both be defined.")

    if args.silent and args.no_fancy_output:
        args_error(parser, "The options --silent and --no-fancy-output can't both be defined.")

    if not args.password:
        digest_pw = read_digest_password()
    else:
        digest_pw = args.password

    if args.results_dir:
        results_dir = os.path.abspath(args.results_dir)
        if not os.path.isdir(results_dir):
            args_error(parser, "Directory for results does not exist.")
    else:
        results_dir = os.getcwd()

    return args.opencast, args.chosen_tenants, args.excluded_tenants, args.https, \
        DigestLogin(user=args.user, password=digest_pw), args.silent, args.no_fancy_output, args.no_series_error, \
        args.check, results_dir
