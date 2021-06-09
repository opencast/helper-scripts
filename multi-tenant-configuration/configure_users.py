# import yaml
# import json
# from args.args_parser import get_args_parser
# from args.args_error import args_error
from rest_requests.request import get_request, post_request
from rest_requests.request_error import RequestError
# from input_output.input import get_yes_no_answer
from user_interaction import check_or_ask_for_permission
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

    # Check and configure System User Accounts & External API User Accounts:
    # For all organizations:
    for organization in ENV_CONFIG['opencast_organizations']:
        if organization['id'] == tenant_id:                         # ToDo or 'all' ?
            for user in organization['external_api_accounts']:
                # For all Users                                     # ToDo System & External API ?
                # check and configure user
                check_user(user=user, tenant_id=tenant_id)


def check_user(user, tenant_id):
    log(f"Check user {user['name']} on tenant {tenant_id}.")

    # Check if user exists
    existing_user = get_user(username=user['username'], tenant_id=tenant_id)
    if not existing_user:
        # create user if it does not exist on tenant (Ask for permission)
        action_allowed = check_or_ask_for_permission(
            target_type='user',
            action='create',
            target_name=user['name'],
            tenant_id=tenant_id
        )
        if action_allowed:
            create_user(account=user, tenant_id=tenant_id)
    else:
        print('User already exist.')
        # ToDo checks

        # Check if Account has External API access. (/api/info/me & /api/info/me/roles)
        check_api_access(user=user, tenant_id=tenant_id)

        # Check if Roles (from API request?) match roles in the configuration file.

        # If no External API access or roles do not match:
        # Update account (Asks for permission)


def get_roles_as_json_array(account):
    roles = [{'name': role, 'type': 'INTERNAL'} for role in account['roles']]

    return roles


def create_user(account, tenant_id):
    """ sends a POST request to the admin UI to create a User

    :param account:         dict    user account to be created      (e.g. {'username': 'Peter', 'password': '123'}
    :param tenant_id:       String
    :return:
    """
    log(f"Create user {account['username']}")

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
        elif err.get_status_code() == "403":
            print("Forbidden, not enough permissions to create a user with a admin role.")
        return False
    except Exception as e:
        print("User could not be created: {}".format(str(e)))
        return False

    return response


def check_api_access(user, tenant_id):
    # ToDo

    tenant_url = CONFIG.tenant_urls[tenant_id]
    url = '{}/api/info/me/'.format(tenant_url)
    data = {
        'tenant_id': tenant_id,
        'username': user['username'],
        'password': user['password']
    }

    try:
        response = get_request(url, DIGEST_LOGIN, '/api/info/me', data=data)
        print(response.json())
    except Exception as e:
        print(e)

    return


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
