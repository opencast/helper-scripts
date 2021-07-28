from rest_requests.request import get_request, post_request, put_request
from rest_requests.request_error import RequestError
from args.digest_login import DigestLogin
from configure_users import get_user
from input_output.input import get_yes_no_answer
from user_interaction import check_or_ask_for_permission
from parsing_configurations import log


CONFIG = None
GROUP_CONFIG = None
DIGEST_LOGIN = None


def set_config_groups(digest_login: DigestLogin, group_config: dict, config: dict):
    """
    Sets/imports the global config variables.
    Must be called before any checks can be performed.
    :param digest_login: The digest login to be used
    :type digest_login: DigestLogin
    :param group_config: The group configuration which specifies the groups on each tenant
    :type group_config: dict
    :param config: The script configuration
    :type config: dict
    """

    global DIGEST_LOGIN
    global GROUP_CONFIG
    global CONFIG
    DIGEST_LOGIN = digest_login
    GROUP_CONFIG = group_config
    CONFIG = config


def check_groups(tenant_id: str):
    """
    Performs the checks for each group on the specified tenant
    :param tenant_id: The target tenant
    :type tenant_id: str
    """
    log('\nStart checking groups for tenant: ', tenant_id)

    # For all Groups:
    for group in GROUP_CONFIG['groups']:
        # Check group
        if group['tenants'] == 'all' or group['tenants'] == tenant_id:
            group['identifier'] = __generate_group_identifier(group, tenant_id)
            __check_group(group=group, tenant_id=tenant_id)


def __check_group(group: dict, tenant_id: str):
    """
    Performs all checks for the specified group:
    - checks if group exists
    - checks if group description matches
    - checks if group members match
    - checks if group roles match
    - ToDo Check API access of all group members
    - ToDo Check group type
    :param group: The group to be checked
    :type group: dict
    :param tenant_id: The target tenant
    :type tenant_id: str
    """
    log(f"\nCheck group {group['name']} with id {group['identifier']}")

    # Check if group exists.
    existing_group = get_group(group, tenant_id)
    if not existing_group:
        # Create group if it does not exist.
        # Ask for permission
        action_allowed = check_or_ask_for_permission(
            target_type='group',
            action='create',
            target_name=group['name'],
            tenant_id=tenant_id
        )
        if action_allowed:
            create_group(group=group, tenant_id=tenant_id)
    else:
        # Check if group name and description match the name and description provided in the configuration.
        # Update them if they do not match. (Asks for permission)
        __check_group_description(group=group, existing_group=existing_group, tenant_id=tenant_id)
        # Check if group members exist.
        # Check if group members match the group members provided in the configuration.
        # Add or remove members accordingly.
        __check_group_members(group=group, existing_group=existing_group, tenant_id=tenant_id)
        # Check if group roles match the group roles provided in the configuration.
        # Update group roles if they do not match. (Asks for permission)
        __check_group_roles(group=group, existing_group=existing_group, tenant_id=tenant_id)
        # ToDo
        # Check external API accounts of members. Add missing API accounts.
        # ToDo should this actually be done? We already ask if members should be removed in the member check.
        # Check group type. If group is closed, remove unexpected members.
        # Check for invalid group type
        # Update group members. (Asks for permission)


def __check_group_description(group: dict, existing_group: dict, tenant_id: str):
    """
    Checks if the group description matches.
    Ask for permission to update the group if necessary.
    :param group: The group as specified in the config file
    :type group: dict
    :param existing_group: The existing group as specified on the tenant system
    :type existing_group: dict
    :param tenant_id: The target tenant
    :type tenant_id: str
    """
    log(f"check names and description for group {group['name']}.")

    # ToDo: does it really makes sense to check for the name?
    #  This seems to be already done when checking for the existence of the group.
    if group['name'] != existing_group['name']:
        print("WARNING: Group names do not match. ")
        return
    if __group_description_template(group['description'], tenant_id) == existing_group['description']:
        log('Group descriptions match.')
    else:
        action_allowed = check_or_ask_for_permission(
            target_type='group',
            action='update the description',
            target_name=group['name'],
            tenant_id=tenant_id
        )
        if action_allowed:
            update_group(tenant_id, group)


def __check_group_members(group: dict, existing_group: dict, tenant_id: str):
    """
    Checks if the group member match.
    Asks for permission to either add or remove members accordingly.
    :param group: The group as specified in the configuration file
    :type group: dict
    :param existing_group: The existing group as specified on the tenant system
    :type existing_group: dict
    :param tenant_id: The target tenant
    :type tenant_id: str
    """
    log(f"Check members for group {group['name']}.")

    group_members = __extract_members_from_group(group=group, tenant_id=tenant_id)
    existing_group_members = sorted(filter(None, existing_group['members'].split(",")))
    log("Config group members: ", group_members)

    members = existing_group_members.copy()
    missing_members = [member for member in group_members if member not in existing_group_members]
    for member in missing_members:
        if not get_user(username=member, tenant_id=tenant_id):
            log(f"Member {member} of group {group['name']} not found on tenant {tenant_id}.")
            missing_members.remove(member)
    additional_members = [member for member in existing_group_members if member not in group_members]

    if not missing_members and not additional_members:
        log('Group members match.')
    else:
        print("Existing group members: ", existing_group_members)
        if missing_members:
            print("Missing members: ", missing_members)
            action_allowed = check_or_ask_for_permission(
                target_type='group',
                action='add missing members',
                target_name=group['name'],
                tenant_id=tenant_id,
                option_i=True
            )
            if action_allowed == 'i':
                for member in missing_members:
                    action_allowed = get_yes_no_answer(f"Add member {member} to group {group['name']}?")
                    if action_allowed:
                        members.append(member)
            elif action_allowed:
                for member in missing_members:
                    members.append(member)

        if additional_members:
            print("Additional members: ", additional_members)
            action_allowed = check_or_ask_for_permission(
                target_type='group',
                action='remove additional members',
                target_name=group['name'],
                tenant_id=tenant_id,
                option_i=True
            )
            if action_allowed == 'i':
                for member in additional_members:
                    action_allowed = get_yes_no_answer(f"remove member {member} from group {group['name']}?")
                    if action_allowed:
                        members.remove(member)
            elif action_allowed:
                for member in additional_members:
                    members.remove(member)

        # Update Group if there are any changes
        if members != existing_group_members:
            # members = ",".join(list(dict.fromkeys(members)))
            members = ",".join(members)
            update_group(tenant_id, group, overwrite_members=members)


def __check_group_roles(group: dict, existing_group: dict, tenant_id: str):
    """
    Checks if the group roles match.
    Asks for permission to either add or remove roles accordingly.
    :param group: The group as specified in the configuration file
    :type group: dict
    :param existing_group: The existing group as specified on the tenant system
    :type existing_group: dict
    :param tenant_id: The target tenant
    :type tenant_id: str
    """
    log(f"Check roles for group {group['name']}.")

    group_roles = __extract_roles_from_group(group=group, tenant_id=tenant_id)
    existing_group_roles = sorted(existing_group['roles'].split(","))
    log("Config group roles: ", group_roles)

    roles = existing_group_roles.copy()
    missing_roles = [role for role in group_roles if role not in existing_group_roles]
    additional_roles = [role for role in existing_group_roles if role not in group_roles]

    if group_roles == existing_group_roles:
        log('Group roles match.')
    else:
        print("Existing group roles: ", existing_group_roles)
        if missing_roles:
            print("Missing roles: ", missing_roles)
            action_allowed = check_or_ask_for_permission(
                target_type='group',
                action='add missing group roles',
                target_name=group['name'],
                tenant_id=tenant_id,
                option_i=True
            )
            if action_allowed == 'i':
                for role in missing_roles:
                    action_allowed = get_yes_no_answer(f"Add role {role} to group {group['name']}?")
                    if action_allowed:
                        roles.append(role)
            elif action_allowed:
                for role in missing_roles:
                    roles.append(role)

        if additional_roles:
            print("Additional roles: ", additional_roles)
            action_allowed = check_or_ask_for_permission(
                target_type='group',
                action='remove additional group roles',
                target_name=group['name'],
                tenant_id=tenant_id,
                option_i=True
            )
            if action_allowed == 'i':
                for role in additional_roles:
                    action_allowed = get_yes_no_answer(f"remove role {role} from group {group['name']}?")
                    if action_allowed:
                        roles.remove(role)
            elif action_allowed:
                for role in additional_roles:
                    roles.remove(role)

        if roles != existing_group_roles:
            # roles = ",".join(list(dict.fromkeys(roles)))
            roles = ",".join(roles)
            update_group(tenant_id, group, overwrite_roles=roles)


def get_group(group: dict, tenant_id: str):
    """
    Checks if the group exists on the specified tenant
    :param group: The group as defined in the configuration file
    :type group: dict
    :param tenant_id: The target tenant
    :type tenant_id: str
    :return: The group as specified on the tenant if it exists or False
    """
    log(f"check if group {group['name']} exists.")

    url = f"{CONFIG.tenant_urls[tenant_id]}/api/groups/{group['identifier']}"
    try:
        response = get_request(url, DIGEST_LOGIN, '/api/groups/')
        return response.json()
    except RequestError as err:
        if err.get_status_code() == "404":
            pass
        else:
            raise Exception
    except Exception as e:
        print("ERROR: ", str(e))
    return False


def create_group(group: dict, tenant_id: str):
    """
    Sends a POST request to /api/groups/ to create a new group with the given parameter.
    :param group: The group to be created (usually the one specified in the configuration file)
    :type group: dict
    :param tenant_id: The target tenant
    :type tenant_id: str
    :return: Returns the response if successful or False if the request failed
    """
    log(f"trying to create group {group['name']}. ")

    url = f'{CONFIG.tenant_urls[tenant_id]}/api/groups/'

    # extract members and roles
    members = __extract_members_from_group(group, tenant_id)
    # check if member exist on tenant
    for member in members:
        if not get_user(username=member, tenant_id=tenant_id):
            print(f"Warning: Member {member} does not exist.")
            members.remove(member)
    members = ",".join(members)
    roles = __extract_roles_from_group(group, tenant_id, as_string=True)

    data = {
        'name': group['name'],
        'description': __group_description_template(group['description'], tenant_id),
        'roles': roles,
        'members': members,
    }
    try:
        response = post_request(url, DIGEST_LOGIN, '/api/groups/', data=data)
    except RequestError as err:
        if err.get_status_code() == "400":
            print(f"Bad Request: Group with name {group['name']} could not be created.")
        elif err.get_status_code() == "409":
            print(f"Conflict: Group with name {group['name']} could not be created.\n"
                  f"Potentially, Group with name {group['name']} already exists.")
        print("RequestError: ", err)
        return False
    except Exception as e:
        print(f"Group with name {group['name']} could not be created. \n", "Exception: ", str(e))
        return False

    log(f"created group {group['name']}.\nmembers: {members} \nroles: {roles} ")
    return response


def update_group(tenant_id: str, group: dict,
                 overwrite_name=None, overwrite_description=None, overwrite_roles=None, overwrite_members=None):
    """
    Updates the group on the tenant.
    Either with the parameters defined in the group or with the specific parameters to individually overwrite them.
    :param tenant_id: The target tenant
    :type tenant_id: str
    :param group: The group as specified in the configuration file
    :type group: dict
    :param overwrite_name: Optional name
    :type overwrite_name: str or None
    :param overwrite_description: Optional description
    :type overwrite_description: str or None
    :param overwrite_roles: Optional roles
    :type overwrite_roles: str or None
    :param overwrite_members: Optional members
    :type overwrite_members: str or None
    :return: Returns the response if successful or False if the request failed
    """
    log(f"Trying to update group ... ")

    group_id = group['identifier']
    name = overwrite_name if overwrite_name else group['name']
    description = overwrite_description if overwrite_description else \
        __group_description_template(group['description'], tenant_id)
    roles = overwrite_roles if overwrite_roles else \
        __extract_roles_from_group(group, tenant_id, as_string=True)
    members = overwrite_members if overwrite_members else \
        __extract_members_from_group(group, tenant_id, as_string=True)

    url = f'{CONFIG.tenant_urls[tenant_id]}/api/groups/{group_id}'
    data = {
        'name': name,
        'description': description,
        'roles': roles,
        'members': members,
    }
    try:
        response = put_request(url, DIGEST_LOGIN, '/api/groups/{groupId}', data=data)
    except RequestError as err:
        if err.get_status_code() == "400": # ToDo: check if this is actually 404
            print(f"Bad Request: Group with name {name} does not exist.")
        print("RequestError: ", err)
        return False
    except Exception as e:
        print(f"Group with name {name} could not be updated. \n", "Exception: ", str(e))
        return False

    log(f"Updated group {name}.")
    return response


def __generate_group_identifier(group: dict, tenant_id: str):
    """
    generates the group identifier based on the group name
    :param group: The group as specified in the configuration file
    :type group: dict
    :param tenant_id: The target tenant
    :type tenant_id: str
    :return: The group id: str
    """
    # ToDo check if the generated identifiers are correct! (the same as in the ruby script)
    # return f"{tenant_id}_{group['name'].replace(' ', '_')}".lower()
    return group['name'].replace(' ', '_').lower()


def __group_description_template(description: str, tenant_id: str):
    """
    replaces placeholders for names in the group description
    :param description: The group description with placeholders
    :type description: str
    :param tenant_id: The tenant id to be inserted into the description
    :type tenant_id: str
    :return: group description with the inserted name, str
    """
    # ToDo check for a better way to insert into template
    description = description.replace("${name}", tenant_id)

    return description


def __extract_members_from_group(group: dict, tenant_id: str, as_string=False):
    """
    Parses the group configuration and extracts the tenant specific group members.
    Does not check if a member exists on the tenant.
    :param group: The group as specified in the configuration file
    :type group: dict
    :param tenant_id: The target tenant
    :type tenant_id: str
    :param as_string: Whether the roles should be returned as a string or a list
    :type as_string: bool
    :return: Comma separated string of members (e.g. "guy1,guy2") or list of members.
    """
    members = [member['uid'] for member in group['members'] if member['tenants'] in ['all', tenant_id]]
    if as_string:
        members = ",".join(sorted(members))
    return members


def __extract_roles_from_group(group: dict, tenant_id: str, as_string=False):
    """
    Parses the group configuration and extracts the tenant specific group roles for a specific group.
    :param group: The group as specified in the configuration file
    :type group: dict
    :param tenant_id: The target tenant
    :type tenant_id: str
    :param as_string: Whether the roles should be returned as a string or a list
    :type as_string: bool
    :return: Sorted comma separated list of roles (e.g. "ROLE_ADMIN,ROLE_SUDO" or ['ROLE_ADMIN', 'ROLE_SUDO'] )
    """
    roles = []
    for permission in group['permissions']:
        # add all default roles
        if permission['tenants'] == 'all':
            for role in permission['roles']:
                roles.append(role)
        # add/remove tenant specific roles
        elif permission['tenants'] == tenant_id:
            for role in permission['roles']['add']:
                roles.append(role)
            for role in permission['roles']['remove']:
                if role in roles:
                    roles.remove(role)
    if as_string:
        roles = ','.join(sorted(roles))
    return roles
