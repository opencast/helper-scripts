from args.args_parser import get_args_parser
from args.args_error import args_error


def parse_args():
    """
    Parse the arguments and check them for correctness

    :return: target_url and number of events to be created if given
    :rtype: str, int
    """
    parser, optional_args, required_args = get_args_parser()

    optional_args.add_argument("-t", "--target_url", type=str, nargs='+', help="URL of target system")
    optional_args.add_argument("-n", "--number", type=int, nargs='+', help="number of events")

    args = parser.parse_args()

    if not args.target_url:
        args.target_url = [None]
    if not args.number:
        args.number = [None]
    elif args.number[0] > 1000:
        args_error(parser, "to many events ...")

    return args.target_url[0], args.number[0]
