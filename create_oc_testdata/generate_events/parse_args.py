from args.args_parser import get_args_parser
from args.args_error import args_error


MAX_NUMBER_OF_EVENTS = 2000


def parse_args():
    """
    Parse the arguments and check them for correctness

    :return: target_url and number of events to be created if given
    :rtype: str, int
    """
    parser, optional_args, required_args = get_args_parser()

    optional_args.add_argument("-t", "--target_url", type=str, nargs='+', help="URL of target system")
    optional_args.add_argument("-n", "--number", type=int, nargs='+', help="number of events")
    optional_args.add_argument("-f", "--file", type=str, nargs='+', help="path to test file")

    args = parser.parse_args()

    args.target_url = args.target_url if args.target_url else [None]
    args.number = args.number if args.number else [None]
    if args.number[0] and args.number[0] > MAX_NUMBER_OF_EVENTS:
        args_error(parser, "too many events ...")
    args.file = args.file if args.file else [None]

    return args.target_url[0], args.number[0], args.file[0]
