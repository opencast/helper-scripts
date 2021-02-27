import yaml
from args.args_parser import get_args_parser
from args.args_error import args_error
from rest_requests.request import get_request, post_request


def parse_args():
    """
    Parse the arguments and check them for correctness

    :return:
    :rtype:
    """
    parser, optional_args, required_args = get_args_parser()

    # change to required_args ?
    required_args.add_argument("-e", "--environment", type=str, nargs='+', help="the environment (either 'staging' or 'production')")
    optional_args.add_argument("-t", "--tenantid", type=str, nargs='+', help="target tenant id")

    args = parser.parse_args()

    if not args.environment:
        args_error(parser, "You have to provide an environment. Either 'staging' or 'production'")
    if not args.environment[0] in ('staging', 'production'):
        args_error(parser, "The environment has to be either 'staging' or 'production'")
    if len(args.environment) > 1:
        args_error(parser, "You can only provide one environment. Either 'staging' or 'production'")

    if not args.tenantid:
        args.tenantid = ['']

    return args.environment[0], args.tenantid[0]


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


def parse_config(config, env_config):

    tenant_ids = [tenant['id'] for tenant in env_config['opencast_organizations']]
    if not (hasattr(config,'tenant_urls') and config.tenant_urls):
        config.tenant_urls = {}
        for tenant_id in tenant_ids:
            config.tenant_urls[tenant_id] = config.tenant_url_pattern.format(tenant_id)

    return True


def get_roles_as_Json_array(account):
    roles = [{'name': role, 'type': 'INTERNAL'} for role in account['roles']]

    return roles

def create_user(account, digest_login, base_url):
    """ sends a POST request to the admin UI to create a User

    :param tenantid:        str     tenant id to form correct url   (e.g. 'tenant1')
    :param account:         dict    user account to be created      (e.g. {'username': 'Peter', 'password': '123'}
    :param digest_login:    digest login
    :param base_url:        base url
    :return:
    """
    url = '{}/admin-ng/users/'.format(base_url)
    data = {
        'username': account['username'],
        'password': account['password'],
        'name': account['name'],
        'email': account['email'],
        'roles': str(get_roles_as_Json_array(account))
    }
    # ToDo error handling
    response = post_request(url, digest_login, '/admin-ng/users/', data=data)

    return response
