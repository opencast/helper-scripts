from args.args_parser import get_args_parser
from args.args_error import args_error


def parse_args():
    """
    Parse the arguments and check them for correctness

    :return: list of event ids, list of series ids (one of them will be None)
    :rtype: list, list
    """
    parser, optional_args, required_args = get_args_parser()

    optional_args.add_argument("-e", "--events", type=str, nargs='+', help="list of event ids")
    optional_args.add_argument("-s", "--series", type=str, nargs='+', help="list of series ids")

    args = parser.parse_args()

    if args.events and args.series:
        args_error(parser, "You can only provide either events or series, not both")

    if not args.events and not args.series:
        args_error(parser, "You have to provide at least one series or event id")

    return args.events, args.series
