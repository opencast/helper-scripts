import yaml
import json
from args.args_parser import get_args_parser
from args.args_error import args_error
from rest_requests.request import get_request, post_request, put_request
from rest_requests.request_error import RequestError
from configure_users import get_user
from input_output.input import get_yes_no_answer, get_configurable_answer
from parsing_configurations import log

def check_groups(tenant_id, digest_login, group_config, config):
    log('\nstart checking groups for tenant: ', tenant_id)

    tenant_url = config.tenant_urls[tenant_id]
    # For all Groups:
    for group in group_config['groups']:
        # check for all tenants if tenant_id is not given
        if not tenant_id:
            tenant_id = group['tenants']
        # Check group
        if group['tenants'] == 'all' or group['tenants'] == tenant_id:
            group['identifier'] = generate_group_identifier(group, tenant_id)
            check_group(tenant_url=tenant_url, digest_login=digest_login, group=group, tenant_id=tenant_id)


def check_if_group_exists(tenant_url, digest_login, group, tenant_id):
    log(f"check if group {group['name']} exists ...")

    url = '{}/api/groups/{}'.format(tenant_url, group['identifier'])
    try:
        response = get_request(url, digest_login, '/api/groups/')
        return response.json()
    except RequestError as err:
        if err.get_status_code() == "404":
            return False
        else:
            raise Exception
    except Exception as e:
        print("ERROR: {}".format(str(e)))
        return False


def check_group(tenant_url, digest_login, group, tenant_id):
    log(f"\nCheck group {group['name']} with id {group['identifier']}")

    # Check if group exists.
    existing_group = check_if_group_exists(tenant_url, digest_login, group, tenant_id)
    if not existing_group:
        # Create group if it does not exist. Ask for permission
        answer = get_yes_no_answer(f"Group {group['name']} does not exist. Create group?")
        if answer:
            create_group(digest_login=digest_login, tenant_url=tenant_url, tenant_id=tenant_id, group=group)
    else:
        # Check if group name and description match the name and description provided in the configuration.
        # Update them if they do not match. (Asks for permission)
        check_group_description(tenant_url=tenant_url, digest_login=digest_login,
                                group=group, existing_group=existing_group, tenant_id=tenant_id)
        # Check if group members exist.
        # Create missing group members. (Asks for permission)
        check_group_members(tenant_url=tenant_url, digest_login=digest_login,
                            group=group, existing_group=existing_group, tenant_id=tenant_id)
        # Check if group roles match the group roles provided in the configuration.
        # Update group roles if they do not match.(Asks for permission)
        check_group_roles(tenant_url=tenant_url, digest_login=digest_login,
                          group=group, existing_group=existing_group, tenant_id=tenant_id)
        # Check if group members match the group members provided in the configuration. Add or remove members accordingly.
        # Check external API accounts of members. Add missing API accounts.
        # Check group type. If group is closed, remove unexpected members.
        # Update group members. (Asks for permission)


def check_group_description(tenant_url, digest_login, group, existing_group, tenant_id):
    log(f"check names and description for group {group['name']}.")
    # ToDo: does it really makes sense to check for the name?
    #  This seems to be already done when checking for the existence of the group.
    if group['name'] != existing_group['name']:
        print("WARNING: Group names do not match. ")
        return
    if group_description_template(group['description'], tenant_id) == existing_group['description']:
        log('Group descriptions match.')
    else:
        answer = get_yes_no_answer(f"Update group description for group {group['name']}?")
        if answer:
            update_group(digest_login=digest_login, tenant_url=tenant_url, tenant_id=tenant_id,
                         description=group['description'], name=group['name'])
    return


def check_group_members(tenant_url, digest_login, group, existing_group, tenant_id):
    log(f"Check members for group {group['name']}.")

    group_members = extract_members_from_group(group=group, tenant_id=tenant_id).split(",")
    existing_group_members = sorted(existing_group['members'].split(","))
    log("Config group members: ", group_members)
    log("Existing group members: ", existing_group_members)

    if group_members == existing_group_members:
        log('Group members match.')
    else:
        members = existing_group_members
        missing_members = [member for member in group_members if member not in existing_group_members]
        # check if missing members exist on the tenant
        for member in missing_members:
            if not get_user(username=member, digest_login=digest_login, tenant_url=tenant_url):
                print(f"Member {member} of group {group['name']} not found on tenant {tenant_id}.")
                missing_members.remove(member)
        additional_members = [member for member in existing_group_members if member not in group_members]
        print("Missing members: ", missing_members)
        print("Additional members: ", additional_members)

        if missing_members or additional_members:
            update_answer = get_configurable_answer(
                options=['y', 'n', 'a', 'r'],
                short_descriptions=["Yes", "No", "Add missing members", "Remove additional members"],
                long_descriptions=["updating group members", "skipping group",
                                   "only adding missing members", "only removing additional members"],
                question=f"Group members for group {group['name']} do not match. Update group?\n"
            )
        if missing_members and update_answer in ['y', 'a']:
            answer = get_configurable_answer(
                options=['y', 'n', 'i'],
                short_descriptions=["Yes, all", "No, none", "individual"],
                long_descriptions=["adding missing members", "skipping missing members", "selecting individually"],
                question=f"Add missing group members from the config file to group {group['name']}?"
            )
            if answer == 'y':
                members += missing_members
            elif answer == 'i':
                for member in missing_members:
                    answer = get_yes_no_answer(f"Add member {member} to group {group['name']}?")
                    if answer:
                        members.append(member)

        if additional_members and additional_members[0] and update_answer in ['y', 'r']:
            answer = get_configurable_answer(
                options=['y', 'n', 'i'],
                short_descriptions=["Yes, all", "No, none", "individual"],
                long_descriptions=["removing all additional members",
                                   "keeping additional members", "selecting individually"],
                question=f"Remove group members which are not in the config file from group {group['name']}?"
            )
            if answer == 'y':
                members -= additional_members
            elif answer == 'i':
                for member in additional_members:
                    answer = get_yes_no_answer(f"remove member {member} from group {group['name']}?")
                    if answer:
                        members.remove(member)

        members = ",".join(list(dict.fromkeys(members)))
        update_group(digest_login=digest_login, tenant_url=tenant_url, tenant_id=tenant_id,
                     members=members, name=group['name'])


def check_group_roles(tenant_url, digest_login, group, existing_group, tenant_id):
    log(f"Check roles for group {group['name']}.")

    group_roles = extract_roles_from_group(group=group, tenant_id=tenant_id).split(",")
    existing_group_roles = sorted(existing_group['roles'].split(","))
    log("Config group roles: ", group_roles)
    log("Existing group roles: ", existing_group_roles)

    if group_roles == existing_group_roles:
        log('Group roles match.')
    else:
        roles = existing_group_roles
        missing_roles = [role for role in group_roles if role not in existing_group_roles]
        additional_roles = [role for role in existing_group_roles if role not in group_roles]
        print("Missing roles: ", missing_roles)
        print("Additional roles: ", additional_roles)

        update_answer = get_configurable_answer(
            options=['y', 'n', 'a', 'r'],
            short_descriptions=["Yes", "No", "Add missing roles", "Remove additional roles"],
            long_descriptions=["updating group roles", "skipping group",
                               "only adding missing roles", "only removing additional roles"],
            question=f"Group roles for group {group['name']} do not match. Update group?\n"
        )
        if missing_roles and update_answer in ['y', 'a']:
            answer = get_configurable_answer(
                options=['y', 'n', 'i'],
                short_descriptions=["Yes, all", "No, none", "individual"],
                long_descriptions=["adding missing roles", "skipping missing roles", "selecting individually"],
                question=f"Add missing group roles from the config file to group {group['name']}?\n"
            )
            if answer == 'y':
                roles += missing_roles
            elif answer == 'i':
                for role in missing_roles:
                    answer = get_yes_no_answer(f"Add role {role} to group {group['name']}?")
                    if answer:
                        roles.append(role)

        if additional_roles and update_answer in ['y', 'r']:
            answer = get_configurable_answer(
                options=['y', 'n', 'i'],
                short_descriptions=["Yes, all", "No, none", "individual"],
                long_descriptions=["removing all additional roles",
                                   "keeping additional roles", "selecting individually"],
                question=f"Remove group roles which are not in the config file from group {group['name']}?"
            )
            if answer == 'y':
                roles -= additional_roles
            elif answer == 'i':
                for role in additional_roles:
                    answer = get_yes_no_answer(f"remove role {role} from group {group['name']}?")
                    if answer:
                        roles.remove(role)

        print("roles: ", roles)
        roles = ",".join(list(dict.fromkeys(roles)))
        update_group(digest_login=digest_login, tenant_url=tenant_url, tenant_id=tenant_id,
                     roles=roles, name=group['name'])


def generate_group_identifier(group, tenant_id):
    # ToDo check if the generated identifiers are correct! (the same as in the ruby script)
    # return f"{tenant_id}_{group['name'].replace(' ', '_')}".lower()
    return group['name'].replace(' ', '_').lower()


def get_groups_from_tenant(tenant_url, digest_login):

    url = '{}/api/groups/'.format(tenant_url)
    try:
        response = get_request(url, digest_login, '/api/groups/')
    except RequestError as err:
        print('RequestError: ', err)
        return False
    except Exception as e:
        print(f"Groups could not be retrieved from {tenant_url}. \n", "Error: ", str(e))
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


def extract_members_from_group(group, tenant_id):
    """
    Does not check if member exists on tenant
    :param group:
    :param tenant_id:
    :return: Comma separated list of members (e.g. "guy1,guy2")
    """
    members = [member['uid'] for member in group['members'] if member['tenants'] in ['all', tenant_id]]
    members = ",".join(sorted(members))

    return members


def group_description_template(description, tenant_id):
    # ToDo check for a better way to insert into template
    description = description.replace("${name}", tenant_id)

    return description


def update_group(digest_login, tenant_url, tenant_id,
                 group=None, name=None, description=None, roles=None, members=None):
    log(f"Try to update group ... ")
    if not name and not group:
        log("Cannot update group without a specified name.")
        return False

    if group:
        group_id = group['identifier']
        if not name:
            name = group['name']
        if not members:
            members = extract_members_from_group(group, tenant_id)
        if not roles:
            roles = extract_roles_from_group(group, tenant_id)
        if not description:
            description = group_description_template(group['description'], tenant_id)
    else:
        group_id = generate_group_identifier(group={'name': name}, tenant_id=tenant_id)
    url = f'{tenant_url}/api/groups/{group_id}'

    data = {
        'name': name,
        'description': description,
        'roles': roles,
        'members': members,
    }
    print('data ', data)
    try:
        response = put_request(url, digest_login, '/api/groups/{groupId}', data=data)
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


def create_group(digest_login, tenant_url, tenant_id, group):
    log(f"Try to create group {group['name']} ... ")

    url = f'{tenant_url}/api/groups/'
    # extract members and roles
    members = extract_members_from_group(group, tenant_id).split(",")
    # check if member exist on tenant
    for member in members:
        if not get_user(username=member, digest_login=digest_login, tenant_url=tenant_url):
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
        response = post_request(url, digest_login, '/api/groups/', data=data)
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
