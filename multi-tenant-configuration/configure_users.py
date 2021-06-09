# import yaml
# import json
# from args.args_parser import get_args_parser
# from args.args_error import args_error
from rest_requests.request import get_request, post_request
from rest_requests.request_error import RequestError
from input_output.input import get_yes_no_answer
from parsing_configurations import __abort_script, log


CONFIG = None
ENV_CONFIG = None
DIGEST_LOGIN = None


def check_users(tenant_id, digest_login, env_conf, config):
    log('\nStart checking users for tenant: ', tenant_id)

    global DIGEST_LOGIN
    global ENV_CONFIG
    global CONFIG
    DIGEST_LOGIN = digest_login
    ENV_CONFIG = env_conf
    CONFIG = config

    external_api_accounts = {}
    for tenant in ENV_CONFIG['opencast_organizations']:
        id = tenant['id']
        # ToDo check if this is necessary
        if id != "dummy":
            external_api_accounts[id] = tenant['external_api_accounts']

    if not tenant_id:
        for_all_tenants = get_yes_no_answer("Create User for all tenants?")
        if not for_all_tenants:
            __abort_script("Okay, not doing anything.")
        else:
            # create user account for all tenants
            for tenant_id in CONFIG.tenant_ids:
                for account in external_api_accounts[tenant_id]:
                    create_user(account, tenant_id)
    else:
        # create user accounts on the specified tenant
        for account in external_api_accounts[tenant_id]:
            create_user(account, tenant_id)


def get_roles_as_json_array(account):
    roles = [{'name': role, 'type': 'INTERNAL'} for role in account['roles']]

    return roles


def create_user(account, tenant_id):
    """ sends a POST request to the admin UI to create a User

    :param account:         dict    user account to be created      (e.g. {'username': 'Peter', 'password': '123'}
    :param tenant_id:       String
    :return:
    """
    log(f"create user {account['username']}")

    tenant_url = CONFIG.tenant_urls[tenant_id]
    url = '{}/admin-ng/users/'.format(tenant_url)
    data = {
        'username': account['username'],
        'password': account['password'],
        'name':     account['name'],
        'email':    account['email'],
        'roles':    str(get_roles_as_json_array(account))
    }

    try:
        response = post_request(url, DIGEST_LOGIN, '/admin-ng/users/', data=data)
    except RequestError as err:
        if err.get_status_code() == "409":
            print("Conflict, a user with username {} already exist.".format(account['username']))
        if err.get_status_code() == "403":
            print("Forbidden, not enough permissions to create a user with a admin role.")
        return False
    except Exception as e:
        print("User could not be created: {}".format(str(e)))
        return False

    return response


def get_user(username, tenant_id):
    """ sends a GET request to the admin UI to get a User

    :param username:        String
    :param tenant_id:       String
    :return:
    """

    tenant_url = CONFIG.tenant_urls[tenant_id]
    url = f'{tenant_url}/admin-ng/users/{username}.json'

    try:
        response = get_request(url, DIGEST_LOGIN, '/admin-ng/users/{username}.json')
    except RequestError as err:
        if err.get_status_code() == "404":
            return False
        else:
            print(err)
            return False
    except Exception as e:
        print(e)
        return False

    return response
