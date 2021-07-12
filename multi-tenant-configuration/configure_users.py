from rest_requests.request import get_request, post_request, put_request
from rest_requests.request_error import RequestError
from input_output.input import get_yes_no_answer
from user_interaction import check_or_ask_for_permission
from parsing_configurations import __abort_script, log


CONFIG = None
ENV_CONFIG = None
DIGEST_LOGIN = None


def set_config_users(digest_login, env_conf, config):

    global DIGEST_LOGIN
    global ENV_CONFIG
    global CONFIG
    DIGEST_LOGIN = digest_login
    ENV_CONFIG = env_conf
    CONFIG = config

    return


def check_users(tenant_id):
    log('\nStart checking users for tenant: ', tenant_id)

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
        # Check if Account has External API access. (/api/info/me)
        check_api_access(user=user, tenant_id=tenant_id)
        # Check if Roles match roles in the configuration file. (/api/info/me/roles)
        check_user_roles(user=user, tenant_id=tenant_id)
        # If no External API access or roles do not match:
        # Update account (Asks for permission)


def __get_roles_as_json_array(account, as_string=False):
    roles = [{'name': role, 'type': 'INTERNAL'} for role in account['roles']]
    if as_string:
        roles = [str(role) for role in roles]
        roles = '[' + ','.join(roles) + ']'

    return roles


def create_user(account, tenant_id):
    """ sends a POST request to the admin UI to create a User

    :param account:         dict    user account to be created      (e.g. {'username': 'Peter', 'password': '123'}
    :param tenant_id:       String
    :return:
    """
    log(f"Create user {account['username']}")

    url = f'{CONFIG.tenant_urls[tenant_id]}/admin-ng/users/'
    data = {
        'username': account['username'],
        'password': account['password'],
        'name':     account['name'],
        'email':    account['email'],
        'roles':    __get_roles_as_json_array(account, as_string=True)
    }

    try:
        response = post_request(url, DIGEST_LOGIN, '/admin-ng/users/', data=data)
    except RequestError as err:
        if err.get_status_code() == "409":
            print(f"Conflict, a user with username {account['username']} already exist.")
        elif err.get_status_code() == "403":
            print("Forbidden, not enough permissions to create a user with a admin role.")
        return False
    except Exception as e:
        print("User could not be created: ", str(e))
        return False

    return response


def update_user(tenant_id, user_id=None, user=None, name=None, email=None, roles=None):
    log(f"Try to update user ... ")

    if not user_id and not user:
        log("Cannot update user without a specified name.")
        return False

    if user:
        if not user_id:
            user_id = user['username']
        if not name:
            name = user['name']
        if not email:
            email = user['email']
        if not roles:
            roles = user['roles']

    if not isinstance(roles, list):
        roles = [roles]
    # roles = [str({'name': role, 'type': 'INTERNAL'}) for role in roles]
    roles = __get_roles_as_json_array(account={'roles': roles}, as_string=True)

    print(roles)

    url = f'{CONFIG.tenant_urls[tenant_id]}/admin-ng/users/{user_id}.json'
    data = {
        'name': name,
        'email': email,
        'roles': roles
    }

    try:
        response = put_request(url, DIGEST_LOGIN, '/api/groups/{username}.json', data=data)
    except RequestError as err:
        if err.get_status_code() == "400": # ToDo: check if this is actually 404
            print(f"Bad Request: Invalid data provided.")
        print("RequestError: ", err)
        return False
    except Exception as e:
        print(f"User with name {name} could not be updated. \n", "Exception: ", str(e))
        return False

    log(f"Updated user {name}.")

    return response


def check_api_access(user, tenant_id):
    log(f"Check API access for user {user['username']}")

    if not get_user_info(user=user, tenant_id=tenant_id):
        # ToDo ask for permission to solve the problem
        print('User has no API Access')


def check_user_roles(user, tenant_id):
    log(f"Check user roles of user {user['username']}")

    existing_user_roles = get_user_roles(user, tenant_id)
    user_roles = user['roles']

    print('system roles: ', existing_user_roles)
    print('config roles: ', user_roles)

    roles = existing_user_roles.copy()
    missing_roles = [role for role in user_roles if role not in existing_user_roles]
    additional_roles = [role for role in existing_user_roles if role not in user_roles]

    if user_roles == existing_user_roles:
        log('User roles match.')
    else:
        if missing_roles:
            print("Missing roles: ", missing_roles)
            action_allowed = check_or_ask_for_permission(
                target_type='user',
                action='add missing user roles',
                target_name=user['name'],
                tenant_id=tenant_id,
                option_i=True
            )
            if action_allowed == 'i':
                for role in missing_roles:
                    action_allowed = get_yes_no_answer(f"Add role {role} to user {user['name']}?")
                    if action_allowed:
                        roles.append(role)
            elif action_allowed:
                for role in missing_roles:
                    roles.append(role)

        if additional_roles:
            print("Additional roles: ", additional_roles)
            action_allowed = check_or_ask_for_permission(
                target_type='user',
                action='remove additional user roles',
                target_name=user['name'],
                tenant_id=tenant_id,
                option_i=True
            )
            if action_allowed == 'i':
                for role in additional_roles:
                    action_allowed = get_yes_no_answer(f"Remove role {role} from user {user['name']}?")
                    if action_allowed:
                        roles.remove(role)
            elif action_allowed:
                for role in additional_roles:
                    roles.remove(role)

        if roles != existing_user_roles:
            # roles = ",".join(roles)
            print(roles)
            update_user(tenant_id=tenant_id, user=user, roles=roles)

        return


def get_user_info(user, tenant_id):

    url = f'{CONFIG.tenant_urls[tenant_id]}/api/info/me'
    headers = {
        'X-RUN-AS-USER': user['username']
    }

    try:
        response = get_request(url, DIGEST_LOGIN, '/api/info/me', headers=headers)
    except Exception as e:
        print(e)
        return False

    return response.json()


def get_user_roles(user, tenant_id):
    # ToDo check if the 'effective roles' should be excluded here
    # -> switch to /admin-ng/users/{username}.json

    url = f'{CONFIG.tenant_urls[tenant_id]}/api/info/me/roles'
    headers = {
        'X-RUN-AS-USER': user['username']
    }

    try:
        response = get_request(url, DIGEST_LOGIN, '/api/info/me/roles', headers=headers)
    except Exception as e:
        print(e)
        return False

    return response.json()



def get_user(username, tenant_id):
    """ sends a GET request to the admin UI to get a User

    :param username:        String
    :param tenant_id:       String
    :return:
    """

    url = f'{CONFIG.tenant_urls[tenant_id]}/admin-ng/users/{username}.json'

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
