from rest_requests.request import get_request, post_request, put_request
from rest_requests.request_error import RequestError
from configure_users import get_user
from input_output.input import get_yes_no_answer
from user_interaction import check_or_ask_for_permission
from parsing_configurations import log


CONFIG = None
GROUP_CONFIG = None
DIGEST_LOGIN = None


def set_config_groups(digest_login, group_config, config):

    global DIGEST_LOGIN
    global GROUP_CONFIG
    global CONFIG
    DIGEST_LOGIN = digest_login
    GROUP_CONFIG = group_config
    CONFIG = config

    return


def check_groups(tenant_id):
    log('\nStart checking groups for tenant: ', tenant_id)

    # For all Groups:
    for group in GROUP_CONFIG['groups']:
        # Check group
        if group['tenants'] == 'all' or group['tenants'] == tenant_id:
            group['identifier'] = generate_group_identifier(group, tenant_id)
            check_group(group=group, tenant_id=tenant_id)


def check_group(group, tenant_id):
    log(f"\nCheck group {group['name']} with id {group['identifier']}")

    # Check if group exists.
    existing_group = check_if_group_exists(group, tenant_id)
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
        check_group_description(group=group, existing_group=existing_group, tenant_id=tenant_id)
        # Check if group members exist.
        # Check if group members match the group members provided in the configuration.
        # Add or remove members accordingly.
        check_group_members(group=group, existing_group=existing_group, tenant_id=tenant_id)
        # Check if group roles match the group roles provided in the configuration.
        # Update group roles if they do not match.(Asks for permission)
        check_group_roles(group=group, existing_group=existing_group, tenant_id=tenant_id)

        # Check external API accounts of members. Add missing API accounts.
        # Check group type. If group is closed, remove unexpected members.
        # Update group members. (Asks for permission)


def check_if_group_exists(group, tenant_id):
    log(f"check if group {group['name']} exists.")

    url = f"{CONFIG.tenant_urls[tenant_id]}/api/groups/{group['identifier']}"
    try:
        response = get_request(url, DIGEST_LOGIN, '/api/groups/')
        return response.json()
    except RequestError as err:
        if err.get_status_code() == "404":
            return False
        else:
            raise Exception
    except Exception as e:
        print("ERROR: ", str(e))
        return False


def check_group_description(group, existing_group, tenant_id):
    log(f"check names and description for group {group['name']}.")
    # ToDo: does it really makes sense to check for the name?
    #  This seems to be already done when checking for the existence of the group.
    if group['name'] != existing_group['name']:
        print("WARNING: Group names do not match. ")
        return
    if group_description_template(group['description'], tenant_id) == existing_group['description']:
        log('Group descriptions match.')
    else:
        action_allowed = check_or_ask_for_permission(
            target_type='group',
            action='update the description',
            target_name=group['name'],
            tenant_id=tenant_id
        )
        if action_allowed:
            update_group(
                tenant_id=tenant_id,
                description=group['description'],
                name=group['name']
            )

    return


def check_group_members(group, existing_group, tenant_id):
    log(f"Check members for group {group['name']}.")

    group_members = extract_members_from_group(group=group, tenant_id=tenant_id)
    existing_group_members = sorted(filter(None, existing_group['members'].split(",")))

    log("Config group members: ", group_members)
    log("Existing group members: ", existing_group_members)

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
            update_group(tenant_id=tenant_id, group=group, members=members)

    return


def check_group_roles(group, existing_group, tenant_id):
    log(f"Check roles for group {group['name']}.")

    group_roles = extract_roles_from_group(group=group, tenant_id=tenant_id).split(",")
    existing_group_roles = sorted(existing_group['roles'].split(","))

    log("Config group roles: ", group_roles)
    log("Existing group roles: ", existing_group_roles)

    roles = existing_group_roles.copy()
    missing_roles = [role for role in group_roles if role not in existing_group_roles]
    additional_roles = [role for role in existing_group_roles if role not in group_roles]

    if group_roles == existing_group_roles:
        log('Group roles match.')
    else:
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
            update_group(tenant_id=tenant_id, group=group, roles=roles)

        return


def generate_group_identifier(group, tenant_id):
    # ToDo check if the generated identifiers are correct! (the same as in the ruby script)
    # return f"{tenant_id}_{group['name'].replace(' ', '_')}".lower()
    return group['name'].replace(' ', '_').lower()


def get_groups_from_tenant(tenant_id):

    url = f'{CONFIG.tenant_urls[tenant_id]}/api/groups/'
    try:
        response = get_request(url, DIGEST_LOGIN, '/api/groups/')
    except RequestError as err:
        print('RequestError: ', err)
        return False
    except Exception as e:
        print("Groups could not be retrieved. \n", "Error: ", str(e))
        return False

    return response.json()


def extract_roles_from_group(group, tenant_id):
    """

    :param group:
    :param tenant_id:
    :return: sorted comma separated list of roles (e.g. "ROLE_ADMIN,ROLE_SUDO")
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
    roles = ','.join(sorted(roles))
    return roles


def extract_members_from_group(group, tenant_id, as_string=False):
    """
    Does not check if member exists on tenant
    :param group:
    :param tenant_id:
    :param as_string:
    :return: Comma separated string of members (e.g. "guy1,guy2") or list of members.
    """
    members = [member['uid'] for member in group['members'] if member['tenants'] in ['all', tenant_id]]
    if as_string:
        members = ",".join(sorted(members))

    return members


def group_description_template(description, tenant_id):
    # ToDo check for a better way to insert into template
    description = description.replace("${name}", tenant_id)

    return description


def update_group(tenant_id, group=None, name=None, description=None, roles=None, members=None):
    log(f"Try to update group ... ")

    if not name and not group:
        log("Cannot update group without a specified name.")
        return False

    if group:
        group_id = group['identifier']
        if not name:
            name = group['name']
        if not members:
            members = extract_members_from_group(group, tenant_id, as_string=True)
        if not roles:
            roles = extract_roles_from_group(group, tenant_id)
        if not description:
            description = group_description_template(group['description'], tenant_id)
    else:
        group_id = generate_group_identifier(group={'name': name}, tenant_id=tenant_id)
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


def create_group(group, tenant_id):
    log(f"trying to create group {group['name']}. ")

    url = f'{CONFIG.tenant_urls[tenant_id]}/api/groups/'

    # extract members and roles
    members = extract_members_from_group(group, tenant_id)
    # check if member exist on tenant
    for member in members:
        if not get_user(username=member, tenant_id=tenant_id):
            print(f"Member {member} does not exist.")
            members.remove(member)
    members = ",".join(members)
    roles = extract_roles_from_group(group, tenant_id)
    description = group_description_template(group['description'], tenant_id)
    data = {
        'name': group['name'],
        'description': description,
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
