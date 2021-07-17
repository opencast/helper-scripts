from rest_requests.request import get_request, post_request, put_request
from rest_requests.request_error import RequestError
from input_output.input import get_yes_no_answer
from user_interaction import check_or_ask_for_permission
from parsing_configurations import __abort_script, log


CONFIG = None
ENV_CONFIG = None
DIGEST_LOGIN = None

# ToDo should this be moved to the config file?
UNEXPECTED_ROLES = ["ROLE_ADMIN", "ROLE_ADMIN_UI", "ROLE_UI_", "ROLE_CAPTURE_"]


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
    for organization in ENV_CONFIG['opencast_organizations']:
        # check switchcast system accounts
        if organization['id'] == 'dummy':
            log(f'Checking system accounts for tenant {tenant_id} ...')
            for system_account in organization['switchcast_system_accounts']:
                check_user(system_account, tenant_id)
        # check and configure external api accounts
        if organization['id'] == tenant_id:                                     # ToDo or 'all' ?
            log(f'Checking External API accounts for tenant {tenant_id} ...')
            for user in organization['external_api_accounts']:
                check_user(user, tenant_id)


def check_user(user, tenant_id):
    log(f"Checking user {user['name']} on tenant {tenant_id}.")

    # Check if user exists
    existing_user = get_user(username=user['username'], tenant_id=tenant_id)
    if not existing_user:
        # create user if it does not exist on tenant (Ask for permission)
        action_allowed = check_or_ask_for_permission(
            target_type='user',
            action='create',
            target_name=user['username'],
            tenant_id=tenant_id
        )
        if action_allowed:
            create_user(account=user, tenant_id=tenant_id)
    else:
        # Check if password is correct and if the account has External API access.
        __check_api_access(user=user, tenant_id=tenant_id)
        # Check if the user roles match the roles in the configuration file.
        __check_user_roles(user, existing_user, tenant_id)
        # check for unexpected roles in the effective roles.
        __check_effective_user_roles(user, tenant_id)


def __get_roles_as_json_array(account, as_string=False):
    roles = [{'name': role, 'type': 'INTERNAL'} for role in account['roles']]
    if as_string:
        roles = [str(role) for role in roles]
        roles = '[' + ','.join(roles) + ']'

    return roles


def create_user(account, tenant_id):
    """
    sends a POST request to the admin UI to create a User
    uses the /admin-ng/users/ endpoint
    :param account: The user account to be created      (e.g. {'username': 'Peter', 'password': '123'}
    :type account: dict
    :param tenant_id: The target tenant
    :type tenant_id: String
    :return: response
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


def update_user(tenant_id, user, overwrite_name=None, overwrite_email=None, overwrite_roles=None, overwrite_pw=None):
    """
    Updates a user with the parameters provided in the user argument
    if they are not overwritten by the optional parameters.
    :param tenant_id: The target tenant
    :type tenant_id: String
    :param user: The user as defined in the config, including the username used to identify the user on the system
    :param overwrite_name: Optional name to use instead
    :type overwrite_name: String
    :param overwrite_email: Optional email to use instead
    :type overwrite_email: String
    :param overwrite_roles: Optional roles to use instead
    :type overwrite_roles: List
    :param overwrite_pw: Optional password to use instead
    :type overwrite_pw: String
    :return: response
    """
    log(f"Trying to update user ... ")

    name = overwrite_name if overwrite_email else user['name']
    email = overwrite_email if overwrite_email else user['email']
    roles = overwrite_roles if overwrite_roles else user['roles']
    pw = overwrite_pw if overwrite_pw else user['password']
    if not isinstance(roles, list):     # in case only one role is given, make sure roles is a list
        roles = [roles]
    roles = __get_roles_as_json_array(account={'roles': roles}, as_string=True)

    url = f"{CONFIG.tenant_urls[tenant_id]}/admin-ng/users/{user['username']}.json"
    data = {
        'password': pw,
        'name': name,
        'email': email,
        'roles': roles
    }
    try:
        response = put_request(url, DIGEST_LOGIN, '/admin-ng/users/{username}.json', data=data)
    except RequestError as err:
        print("RequestError: ", err)
        if err.get_status_code() == "400":
            print(f"Bad Request: Invalid data provided.")
        return False
    except Exception as e:
        print(f"User with name {name} could not be updated. \n", "Exception: ", str(e))
        return False

    log(f"Updated user {name}.")

    return response


def __check_api_access(user, tenant_id):
    """
    Checks if the user defined in the config has access to the API.
    The check tries to login with the username and password defined in the config,
    and sends a get request to '/api/info/me' .
    If check fails, asks for user permission to update user.
    :param user: The user defined in the config
    :type user: Dict
    :param tenant_id: The target tenant
    :type tenant_id: String
    :return: True
    """
    log(f"Checking API access for user {user['username']}")

    url = f'{CONFIG.tenant_urls[tenant_id]}/api/info/me'
    headers = {}
    login = {
        'user': user['username'],
        'password': user['password']
    }
    try:
        get_request(url, login, '/api/info/me', headers=headers, use_digest=False)
    except RequestError:
        print(f"User {user['username']} has no API Access")
        # ToDo add to group to get API access roles?
        action_allowed = check_or_ask_for_permission(
            target_type='user',
            action='configure user',
            target_name=user['username'],
            tenant_id=tenant_id
        )
        if action_allowed:
            update_user(tenant_id, user=user)
    except Exception as e:
        print('Error: Failed to check for API access.')
        print(str(e))
        return False

    return True


def __check_effective_user_roles(user, tenant_id):
    """
    Checks if the effective user roles of the user contain unexpected roles.
    prints a warning for each unexpected role.
    :param user: User containing the username for whom to retrieve the roles
    :type user: Dict
    :param tenant_id: The ID of the target tenant
    :type tenant_id: String
    :return: True
    """
    log(f"Check effective user roles of user {user['username']}")

    effective_user_roles = get_user_roles(user['username'], tenant_id)
    for role in effective_user_roles:
        for unexpected_role in UNEXPECTED_ROLES:
            if unexpected_role in role:
                print(f"WARNING: Unexpected role found for User {user['username']}: {role}")

    return True


def __check_user_roles(user, existing_user, tenant_id):
    """
    Checks if the INTERNAL user roles match the user roles in the config file.
    If check fails, asks for user permission to update user.
    :param user: The user as defined in the config file
    :type user: Dict
    :param existing_user: The user as defined on the tenant
    :type: Dict
    :param tenant_id: The target tenant
    :type: String
    :return: True
    """
    log(f"Check user roles of user {user['username']}")

    existing_user_roles = extract_internal_user_roles(existing_user)
    user_roles = user['roles']
    log('config roles: ', user_roles)

    roles = existing_user_roles.copy()
    missing_roles = [role for role in user_roles if role not in existing_user_roles]
    additional_roles = [role for role in existing_user_roles if role not in user_roles]

    if user_roles == existing_user_roles:
        log('User roles match.')
    else:
        print("existing user roles: ", existing_user_roles)
        if missing_roles:
            print("Missing roles: ", missing_roles)
            action_allowed = check_or_ask_for_permission(
                target_type='user',
                action='add missing user roles',
                target_name=user['username'],
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
                target_name=user['username'],
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
            update_user(tenant_id, user, overwrite_roles=roles)

    return True


def get_user_roles(user_name, tenant_id):
    """
    returns the effective roles of a user (user roles + group roles).
    Uses DigestLogin.
    :param user_name: The username of the user on the tenant
    :type user_name: String
    :param tenant_id: The traget tenant
    :type tenant_id: String
    :return: The roles as dict
    """
    url = f'{CONFIG.tenant_urls[tenant_id]}/api/info/me/roles'
    headers = {'X-RUN-AS-USER': user_name}
    try:
        response = get_request(url, DIGEST_LOGIN, '/api/info/me/roles', headers=headers)
    except Exception as e:
        print(e)
        return False

    return response.json()


def extract_internal_user_roles(existing_user, as_string=False):
    """
    Extracts the INTERNAL user roles from a user on the tenant.
    :param existing_user: The user as defined on the tenant
    :type existing_user: JSON
    :param as_string: Whether the roles should be returned as a string
    :type as_string: Boolean
    :return: roles, as list or string
    """
    roles = []
    for role in existing_user['roles']:
        # ToDo check if 'INTERNAL' is the right thing to use here
        if role['type'] == 'INTERNAL':
            roles.append(role['name'])
    if as_string:
        roles = ",".join(sorted(roles))

    return roles


def get_user(username, tenant_id):
    """
    Sends a GET request to the admin UI to get a user
    :param username: The username of the user on the tenant
    :type username: String
    :param tenant_id: The target tenant
    :type tenant_id: String
    :return: user as JSON
    """
    url = f'{CONFIG.tenant_urls[tenant_id]}/admin-ng/users/{username}.json'
    try:
        response = get_request(url, DIGEST_LOGIN, '/admin-ng/users/{username}.json')
    except RequestError as err:
        if not err.get_status_code() == "404":
            print(err)
        return False
    except Exception as e:
        print(e)
        return False

    return response.json()
