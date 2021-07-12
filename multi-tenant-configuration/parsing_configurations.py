import yaml
import json
from args.args_parser import get_args_parser
from args.args_error import args_error
from rest_requests.basic_requests import get_tenants


VERBOSE_FLAG = True


def parse_args():
    """
    Parse the arguments and check them for correctness

    :return:
    :rtype:
    """
    parser, optional_args, required_args = get_args_parser()

    required_args.add_argument("-e", "--environment", type=str, nargs='+',
                               help="the environment (either 'staging' or 'production')")
    optional_args.add_argument("-t", "--tenantid", type=str, nargs='+', help="target tenant id")
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

    if not args.tenantid:
        args.tenantid = ['']

    if not args.check:
        args.check = ['all']
    elif args.check[0] not in ['users', 'groups', 'cast', 'capture']:
        args_error(parser, "The check should be 'users', 'groups', 'cast' or 'capture'")

    global VERBOSE_FLAG
    if args.verbose and args.verbose[0] == "True":
        VERBOSE_FLAG = True
    else:
        VERBOSE_FLAG = False

    return args.environment[0], args.tenantid[0], args.check[0]


def read_yaml_file(path):
    """
    reads a .yaml file and returns a dictionary
    :param path: path to the yaml file
    :return: returns a dictionary
    """
    # ToDo error handling if path or file does not exist
    # FileNotFoundError:
    with open(path, 'r') as f:
        content = yaml.load(f, Loader=yaml.FullLoader)

    return content


def parse_config(config, env_config, digest_login):
    # ToDo Check if all mandatory configurations are given

    # ToDo should mh_default_org be removed from tenant_ids?
    config.tenant_ids = get_tenants(config.base_url, digest_login)
    config.tenant_ids.remove('mh_default_org')

    if not (hasattr(config, 'tenant_urls') and config.tenant_urls):
        config.tenant_urls = {}
        for tenant_id in config.tenant_ids:
            config.tenant_urls[tenant_id] = config.tenant_url_pattern.format(tenant_id)

    return config


def create_group_config_file_from_json_file(json_file_path, yaml_file_path='test.yaml'):
    """
    This function can be used to transform a json file to a yaml file.
    requires import json and import yaml
    :param json_file_path: path to json file
    :param yaml_file_path: path to yaml file (will be created if it does not exist)
    :return:
    """

    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
    with open(yaml_file_path, 'w') as file:
        yaml.dump(json_data, file, sort_keys=False)

    return True


def log(*args):
    if VERBOSE_FLAG:
        print(*args)


def __abort_script(message):
    print(message)
    sys.exit()
