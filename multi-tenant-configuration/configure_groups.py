import yaml
import json
from args.args_parser import get_args_parser
from args.args_error import args_error
from rest_requests.request import get_request, post_request
from rest_requests.request_error import RequestError
from input_output.input import get_yes_no_answer
from parsing_configurations import log

def check_groups(tenant_id, digest_login, group_config, config):

    tenant_url = config.tenant_urls[tenant_id]
    # For all Groups:
    for group in group_config['groups']:
        if not tenant_id:
            tenant_id = group['tenants']
        group['identifier'] = generate_group_identifier(group, tenant_id)
        # Check group
        if group['tenants'] == 'all' or group['tenants'] == tenant_id:
            check_group(tenant_url=tenant_url, digest_login=digest_login, group=group, tenant_id=tenant_id)


def check_if_group_exists(tenant_url, digest_login, group, tenant_id):
    # ToDo log
    url = '{}/api/groups/{}'.format(tenant_url, group['identifier'])
    try:
        response = get_request(url, digest_login, '/api/groups/')
        return response.json()
    except RequestError as err:
        if err.get_status_code() == "404":
            print('Group was not found: ', err)
            return False
        else:
            raise Exception
    except Exception as e:
        print("ERROR: {}".format(str(e)))
        return False


def check_group(tenant_url, digest_login, group, tenant_id):
    log(f"Check group {group['name']} with id {group['identifier']}")

    # Check if group exists.
    existing_group = check_if_group_exists(tenant_url, digest_login, group, tenant_id)
    if not existing_group:
        # Create group if it does not exist. Ask for permission
        answer = get_yes_no_answer(f"group {group['name']} does not exist. Create group?")
        if answer:
            existing_group = create_group(group=group, digest_login=digest_login, tenant_url=tenant_url, tenant_id=tenant_id)
    elif existing_group:
        # Check if group name and description match the name and description provided in the configuration.
        log('check names for group')
        if group['name'] == existing_group['name']:
            log('names are equal')
        # Update them if they do not match. (Asks for permission)
        # Check if group members exist.
        # Create missing group members. (Asks for permission)
        # Check if group roles match the group roles provided in the configuration.
        # Update group roles if they do not match.(Asks for permission)
        # Check if group members match the group members provided in the configuration. Add or remove members accordingly.
        # Check external API accounts of members. Add missing API accounts.
        # Check group type. If group is closed, remove unexpected members.
        # Update group members. (Asks for permission)


def generate_group_identifier(group, tenant_id):
    # ToDo move this to parse group config file
    # ToDo check if the generated identifiers are correct! (the same as in the ruby script)
    # return f"{tenant_id}_{group['name'].replace(' ', '_')}".lower()
    return group['name'].replace(' ', '_').lower()


def get_groups_from_tenant(tenant_url, digest_login):

    url = '{}/api/groups/'.format(tenant_url)
    try:
        response = get_request(url, digest_login, '/api/groups/')
    except RequestError as err:
        print('RequestError:')
        print(err)
        return False
    except Exception as e:
        print("Groups could not be retrieved from {}. ".format(tenant_url))
        print("Error: {}".format(str(e)))
        return False

    return response.json()


def create_group(group, digest_login, tenant_url, tenant_id):
    # ToDo log
    print('Try to create Group!')
    url = '{}/api/groups/'.format(tenant_url)

    # ToDo is this logic correct?
    # should be checked if the member exists?
    members = [member['uid'] for member in group['members']
               if member['tenants'] == 'all' or member['tenants'] == tenant_id]
    members = ",".join(members)
    # print("members: ", members)

    # ToDo check group config file if 'add' and 'remove' are needed
    roles = []
    for permission in group['permissions']:
        if permission['tenants'] == 'all' or permission['tenants'] == tenant_id:
            for role in permission['roles']:
                roles.append(role)
    roles = ','.join(roles)
    # print("roles: ", roles)

    data = {
        'name': group['name'],
        'description': group['description'],
        'roles': roles,
        'members': members,
    }
    try:
        response = post_request(url, digest_login, '/api/groups/', data=data)
        print("created group {}".format(group['name']))
    except RequestError as err:
        if err.get_status_code() == "400":
            print("Conflict: group with name {} could not be created.".format(group['name']))
        elif err.get_status_code() == "409":
            print("Failed to create group: ", err)
        else:
            print(err)
        return False
    except Exception as e:
        print("Group could not be created: {}".format(str(e)))
        return False

    return response
