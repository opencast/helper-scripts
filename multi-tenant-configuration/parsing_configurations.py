from args.args_parser import get_args_parser
from args.args_error import args_error


def parse_args():
    """
    Parses the arguments and check them for correctness
    :return: the environment, the tenant_id, the check
    :rtype: triple
    """
    parser, optional_args, required_args = get_args_parser()

    required_args.add_argument("-e", "--environment", type=str, nargs='+',
                               help="the environment (either 'staging' or 'production')")
    optional_args.add_argument("-t", "--tenant-id", type=str, nargs='+', help="target tenant id")
    optional_args.add_argument("-c", "--check", type=str, nargs='+',
                               help="checks to be performed ('users', 'groups', 'cast' or 'capture') (default: all)")
    optional_args.add_argument("-v", "--verbose", type=str, nargs='+', help="enables more logging")

    args = parser.parse_args()

    if not args.environment:
        args_error(parser, "You have to provide an environment. Either 'staging' or 'production'")
    if not args.environment[0] in ('staging', 'production'):
        args_error(parser, "The environment has to be either 'staging' or 'production'")
    if len(args.environment) > 1:
        args_error(parser, "You can only provide one environment. Either 'staging' or 'production'")

    if not args.tenant_id:
        args.tenant_id = ['']

    if not args.check:
        args.check = ['all']
    elif args.check[0] not in ['users', 'groups', 'capture']:
        args_error(parser, "The check should be 'users', 'groups' or 'capture'")

    verbose = True if args.verbose else False

    return args.environment[0], args.tenant_id[0], args.check[0], verbose
