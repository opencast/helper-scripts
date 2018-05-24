import argparse
import os

from shared.args.args_error import args_error
from shared.args.digest_login import read_digest_password, DigestLogin


def parse_args():
    """
    Parse the arguments, check them for correctness, read in the digest password if necessary, and return everything.

    :rtype: str, bool, list, list, DigestLogin, int, int, bool, str
    :return: opencast url, whether to use https, chosen tenants, excluded tenants, the digest user and password,
    the waiting period between batches and the amount of workflows in a batch, whether to print progress statements, and
    the results directory
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--opencast", type=str, help="url of the opencast instance", required=True)
    parser.add_argument("-c", "--chosen-tenants", type=str, nargs='+', help="list of tenants to check", required=False)
    parser.add_argument("-e", "--excluded-tenants", type=str, nargs='+', help="list of tenants to be excluded",
                        required=False)
    parser.add_argument("-u", "--user", type=str, help="digest user", required=True)
    parser.add_argument("-p", "--password", type=str, help="digest password", required=False)
    parser.add_argument('-s', "--silent", action='store_true', help="disables progress output")
    parser.add_argument('-l', "--https", action='store_true', help="enables https")
    parser.add_argument('-n', "--no-fancy-output", action='store_true',
                        help="disables fancy output including the progress bars")
    parser.add_argument('-d', "--results-dir", type=str, help="directory where results should be stored")
    parser.add_argument('-w', "--waiting-period", type=int, help="time in seconds between the starting of workflows of "
                                                                 "two batches", default=60)
    parser.add_argument('-b', "--batch-size", type=int, help="amount of workflows that should be started right away",
                        default=100)

    args = parser.parse_args()

    if not args.opencast and args.user:
        args_error(parser)

    if args.excluded_tenants and args.chosen_tenants:
        args_error(parser, "The options --chosen-tenants and --excluded-tenants can't both be defined.")

    if args.silent and args.no_fancy_output:
        args_error(parser, "The options --silent and --no-fancy-output can't both be defined.")

    if args.batch_size <= 0:
        args_error(parser, "The batch size can't be <= 0.")

    if args.waiting_period < 0:
        args_error(parser, "The waiting period can't be negative.")

    if args.results_dir:
        results_dir = os.path.abspath(args.results_dir)
        if not os.path.isdir(results_dir):
            args_error(parser, "Directory for results does not exist")
    else:
        results_dir = os.getcwd()

    if not args.password:
        digest_pw = read_digest_password()
    else:
        digest_pw = args.password

    return args.opencast, args.https, args.chosen_tenants, args.excluded_tenants, \
        DigestLogin(user=args.user, password=digest_pw), args.waiting_period, args.batch_size, args.silent, \
        args.no_fancy_output, results_dir
