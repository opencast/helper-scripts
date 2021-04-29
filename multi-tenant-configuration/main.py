import os
import sys
sys.path.append(os.path.join(os.path.abspath('..'), "lib"))

# import io
# import yaml
# from args.args_parser import get_args_parser
# from args.args_error import args_error
# from rest_requests.request_error import RequestError
# from input_output.input import get_yes_no_answer
from args.digest_login import DigestLogin
from parsing_configurations import parse_args, read_yaml_file, parse_config
from configure_users import check_users
from configure_groups import check_groups
# from rest_requests.request import get_request, post_request
# from rest_requests.request_error import RequestError
import config


VERBOSE_FLAG = True

def main():

    ###   Parse args and config   ###
    environment, tenant_id, check = parse_args()                                    # parse args
    env_conf = read_yaml_file(config.env_path.format(environment))                  # read environment config file
    script_config = parse_config(config, env_conf)                                  # parse config.py
    group_config = read_yaml_file(config.group_path)                                # read group config file
    # ToDo Think about whether we should exclude Digest Login credentials from config.py file
    digest_login = DigestLogin(user=config.digest_user, password=config.digest_pw)  # create Digest Login

    ###   Start checks   ###
    if check == 'all':
        check_users(tenant_id=tenant_id, digest_login=digest_login, env_conf=env_conf, config=script_config)
        check_groups(tenant_id=tenant_id, digest_login=digest_login, group_config=group_config, config=script_config)
    elif check == 'users':
        check_users(tenant_id=tenant_id, digest_login=digest_login, env_conf=env_conf, config=script_config)
    elif check == 'groups':
        check_groups(tenant_id=tenant_id, digest_login=digest_login, group_config=group_config, config=script_config)


# def check_users(tenant_id, digest_login, env_conf):
#     print('Log: start checking users for tenant ', tenant_id)
#
#     external_api_accounts = {}
#     for tenant in env_conf['opencast_organizations']:
#         id = tenant['id']
#         if id != "dummy":
#             external_api_accounts[id] = tenant['external_api_accounts']
#
#     if not tenant_id:
#         for_all_tenants = get_yes_no_answer("Create User for all tenants?")
#         if not for_all_tenants:
#             __abort_script("Okay, not doing anything.")
#         else:
#             # create user account for all tenants
#             for tenant_id in config.tenant_ids:
#                 for account in external_api_accounts[tenant_id]:
#                     response = create_user(account, digest_login, config.tenant_urls[tenant_id])
#     else:
#         # create user accounts on the specified tenant
#         for account in external_api_accounts[tenant_id]:
#             response = create_user(account, digest_login, config.tenant_urls[tenant_id])


# def check_groups(tenant_id, digest_login, group_config):
#
#     tenant_url = config.tenant_urls[tenant_id]
#     # For all Groups:
#     for group in group_config['groups']:
#         if not tenant_id:
#             tenant_id = group['tenants']
#         group['identifier'] = generate_group_identifier(group, tenant_id)
#         # Check group
#         if group['tenants'] == 'all' or group['tenants'] == tenant_id:
#             check_group(tenant_url=tenant_url, digest_login=digest_login, group=group, tenant_id=tenant_id)


# def check_if_group_exists(tenant_url, digest_login, group, tenant_id):
#     # ToDo log
#     url = '{}/api/groups/{}'.format(tenant_url, group['identifier'])
#     try:
#         response = get_request(url, digest_login, '/api/groups/')
#         return response.json()
#     except RequestError as err:
#         if err.get_status_code() == "404":
#             print('Group was not found: ', err)
#             return False
#         else:
#             raise Exception
#     except Exception as e:
#         print("ERROR: {}".format(str(e)))
#         return False

#
# def check_group(tenant_url, digest_login, group, tenant_id):
#     # ToDo log
#     print(f"Checking group {group['name']} with id {group['identifier']}")
#
#     # Check if group exists.
#     existing_group = check_if_group_exists(tenant_url, digest_login, group, tenant_id)
#     if not existing_group:
#         # Create group if it does not exist. Ask for permission
#         answer = get_yes_no_answer(f"group {group['name']} does not exist. Create group?")
#         if answer:
#             existing_group = create_group(group=group, digest_login=digest_login, tenant_url=tenant_url, tenant_id=tenant_id)
#     elif existing_group:
#         # Check if group name and description match the name and description provided in the configuration.
#         print('check names:')
#         if group['name'] == existing_group['name']:
#             print('names are equal')
#         # Update them if they do not match. (Asks for permission)
#         # Check if group members exist.
#         # Create missing group members. (Asks for permission)
#         # Check if group roles match the group roles provided in the configuration.
#         # Update group roles if they do not match.(Asks for permission)
#         # Check if group members match the group members provided in the configuration. Add or remove members accordingly.
#         # Check external API accounts of members. Add missing API accounts.
#         # Check group type. If group is closed, remove unexpected members.
#         # Update group members. (Asks for permission)


# def create_group(group, digest_login, tenant_url, tenant_id):
#     # ToDo log
#     print('Try to create Group!')
#     url = '{}/api/groups/'.format(tenant_url)
#
#     # ToDo is this logic correct?
#     # should be checked if the member exists?
#     members = [member['uid'] for member in group['members']
#                if member['tenants'] == 'all' or member['tenants'] == tenant_id]
#     members = ",".join(members)
#     # print("members: ", members)
#
#     # ToDo check group config file if 'add' and 'remove' are needed
#     roles = []
#     for permission in group['permissions']:
#         if permission['tenants'] == 'all' or permission['tenants'] == tenant_id:
#             for role in permission['roles']:
#                 roles.append(role)
#     roles = ','.join(roles)
#     # print("roles: ", roles)
#
#     data = {
#         'name': group['name'],
#         'description': group['description'],
#         'roles': roles,
#         'members': members,
#     }
#     try:
#         response = post_request(url, digest_login, '/api/groups/', data=data)
#         print("created group {}".format(group['name']))
#     except RequestError as err:
#         if err.get_status_code() == "400":
#             print("Conflict: group with name {} could not be created.".format(group['name']))
#         elif err.get_status_code() == "409":
#             print("Failed to create group: ", err)
#         else:
#             print(err)
#         return False
#     except Exception as e:
#         print("Group could not be created: {}".format(str(e)))
#         return False
#
#     return response


def log(message):
    if(VERBOSE_FLAG):
        print(message)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborting process.")
        sys.exit(0)
