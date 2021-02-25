import yaml

from args.args_parser import get_args_parser
from args.args_error import args_error


def parse_args():
    """
    Parse the arguments and check them for correctness

    :return: list of event ids, list of series ids (one of them will be None)
    :rtype: list, list
    """
    parser, optional_args, required_args = get_args_parser()

    # change to required_args ?
    required_args.add_argument("-e", "--environment", type=str, nargs='+', help="the environment (either 'staging' or 'production')")
    optional_args.add_argument("-t", "--tenantid", type=str, nargs='+', help="target tenant id")

    args = parser.parse_args()

    if not args.environment:
        args_error(parser, "You have to provide an environment")

    return args.environment, args.tenantid


def read_configuration_file(path):
    with open(path, 'r') as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)

    return conf
