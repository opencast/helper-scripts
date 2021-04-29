import yaml
import json
from args.args_parser import get_args_parser
from args.args_error import args_error
from rest_requests.request import get_request, post_request
from rest_requests.request_error import RequestError


def parse_args():
    """
    Parse the arguments and check them for correctness

    :return:
    :rtype:
    """
    parser, optional_args, required_args = get_args_parser()

    # ToDo change optional to required_args ?
    required_args.add_argument("-e", "--environment", type=str, nargs='+',
                               help="the environment (either 'staging' or 'production')")
    optional_args.add_argument("-t", "--tenantid", type=str, nargs='+', help="target tenant id")
    optional_args.add_argument("-c", "--check", type=str, nargs='+',
                               help="checks to be performed ('users', 'groups', 'cast' or 'capture') (default: all)")

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


def parse_config(config, env_config):

    # ToDo check if "dummy" is really how it should be in the organizations file
    config.tenant_ids = [tenant['id'] for tenant in env_config['opencast_organizations'] if tenant['id'] != "dummy"]
    # ToDo suche get all tenant funktion
    if not (hasattr(config,'tenant_urls') and config.tenant_urls):
        config.tenant_urls = {}
        for tenant_id in config.tenant_ids:
            config.tenant_urls[tenant_id] = config.tenant_url_pattern.format(tenant_id)

    return config


# def get_roles_as_Json_array(account):
#     roles = [{'name': role, 'type': 'INTERNAL'} for role in account['roles']]
#
#     return roles


# def generate_group_identifier(group, tenant_id):
#     # ToDo move this to parse group config file
#     # ToDo check if the generated identifiers are correct! (the same as in the ruby script)
#     # return f"{tenant_id}_{group['name'].replace(' ', '_')}".lower()
#     return group['name'].replace(' ', '_').lower()

#
# def create_user(account, digest_login, tenant_url):
#     """ sends a POST request to the admin UI to create a User
#
#     :param account:         dict    user account to be created      (e.g. {'username': 'Peter', 'password': '123'}
#     :param digest_login:    digest login
#     :param tenant_url:        tenant url
#     :return:
#     """
#     url = '{}/admin-ng/users/'.format(tenant_url)
#     data = {
#         'username': account['username'],
#         'password': account['password'],
#         'name': account['name'],
#         'email': account['email'],
#         'roles': str(get_roles_as_Json_array(account))
#     }
#     try:
#         response = post_request(url, digest_login, '/admin-ng/users/', data=data)
#         print("created user {}".format(account['username']))
#     except RequestError as err:
#         if err.get_status_code() == "409":
#             print("Conflict, a user with username {} already exist.".format(account['username']))
#         if err.get_status_code() == "403":
#             print("Forbidden, not enough permissions to create a user with a admin role.")
#         return False
#     except Exception as e:
#         print("User could not be created: {}".format(str(e)))
#         return False
#
#     return response


# def get_groups_from_tenant(tenant_url, digest_login):
#
#     url = '{}/api/groups/'.format(tenant_url)
#     try:
#         response = get_request(url, digest_login, '/api/groups/')
#     except RequestError as err:
#         print('RequestError:')
#         print(err)
#         return False
#     except Exception as e:
#         print("Groups could not be retrieved from {}. ".format(tenant_url))
#         print("Error: {}".format(str(e)))
#         return False
#
#     return response.json()


def create_group_config_file_from_json_file(json_file_path, yaml_file_path='test.yaml'):
    """
    This function can be used to transform a json file to a yaml file.
    requires import json and import yaml
    :param json_file_path: path to json file
    :param yaml_file_path: path to yaml file (will be created if it does not exist)
    :return:
    """

    with open(json_file_path, 'r') as json_file:
        jsonData = json.load(json_file)
    with open(yaml_file_path, 'w') as file:
        yaml.dump(jsonData, file, sort_keys=False)

    return True


def __abort_script(message):
    print(message)
    sys.exit()
