import os

from args.args_error import args_error
from args.args_parser import get_args_parser
from args.digest_login import read_digest_password, DigestLogin


def parse_args():
    """
    Parse the arguments, check them for correctness, read in the digest password if necessary, and return everything.

    :return: Opencast URL, list of paths to directories with distribution artefacts, whether to use https,
             chosen tenants, excluded tenants, digest user and password, whether to print progress statements,
            whether to print progress bars
    :rtype: str, list, bool, list, list, DigestLogin, bool, bool
    """

    parser, optional_args, required_args = get_args_parser()

    required_args.add_argument("-o", "--opencast", type=str, help="url of the opencast instance", required=True)
    required_args.add_argument("-d", "--distribution-dirs", type=str, nargs='+',
                               help="list of distribution directories to check", required=True)
    optional_args.add_argument("-c", "--chosen-tenants", type=str, nargs='+', help="list of tenants to check")
    optional_args.add_argument("-e", "--excluded-tenants", type=str, nargs='+', help="list of tenants to be excluded")
    required_args.add_argument("-u", "--user", type=str, help="digest user", required=True)
    optional_args.add_argument("-p", "--password", type=str, help="digest password")
    optional_args.add_argument('-s', "--silent", action='store_true', help="disables progress output")
    optional_args.add_argument('-l', "--https", action='store_true', help="enables https")
    optional_args.add_argument('-n', "--no-fancy-output", action='store_true',
                               help="disables fancy output including the progress bars")

    args = parser.parse_args()

    if not args.opencast and args.user and args.distribution_dirs:
        args_error(parser)

    if args.excluded_tenants and args.chosen_tenants:
        args_error(parser, "The options --chosen-tenants and --excluded-tenants can't both be defined.")

    if args.silent and args.no_fancy_output:
        args_error(parser, "The options --silent and --no-fancy-output can't both be defined.")

    for dir_path in args.distribution_dirs:
        distribution_dir = os.path.abspath(dir_path)
        if not os.path.isdir(distribution_dir):
            args_error(parser, "One directory for distribution artefacts does not exist.")

    if not args.password:
        digest_pw = read_digest_password()
    else:
        digest_pw = args.password

    return args.opencast, args.distribution_dirs, args.https, args.chosen_tenants, args.excluded_tenants, \
        DigestLogin(user=args.user, password=digest_pw), args.silent, args.no_fancy_output
