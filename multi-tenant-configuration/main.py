import os
import sys
import yaml

sys.path.append(os.path.join(os.path.abspath('..'), "lib"))

# import datetime
import config
import io
# from collections import defaultdict
from rest_requests.request_error import RequestError
from args.digest_login import DigestLogin
from rest_requests.request import get_request, post_request
# from pathlib import Path


# ToDo
# add logger
# add interaction question
# add parameter to python command

def main():
    """
    configure Groups and Users
    """

    digest_login = DigestLogin(user=config.digest_user, password=config.digest_pw)
    # read config file
    opencast_organizations = read_configuration_file(config.env_path)['opencast_organizations']
    tenants = [tenant['id'] for tenant in opencast_organizations]
    external_api_accounts = opencast_organizations[1]['external_api_accounts']

    # create users for tenant 1
    for account in external_api_accounts:
        tenant = tenants[1]
        create_user(tenant, account, digest_login)


def read_configuration_file(path):
    with open(path, 'r') as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)

    return conf

# # example get request
# response = get_request("http://tenant1:8080/users/users.json", digest_login, "users/users.json")
# json_content = get_json_content(response)
# print(response)

def get_roles_as_Json_array(account):
    roles = [{'name': role, 'type': 'INTERNAL'} for role in account['roles']]

    return roles

def create_user(tenantid, account, digest_login):
    """ sends a POST request to the admin UI to create a User

    :param tenantid:    str     tenant id to form correct url   (e.g. 'tenant1')
    :param account:     dict    user account to be created      (e.g. {'username': 'Peter', 'password': '123'}
    :param digest_login: digest login
    :return:
    """
    url = '{}/admin-ng/users/'.format(config.url_pattern.format(tenantid))
    data = {
        'username': account['username'],
        'password': account['password'],
        'name': account['name'],
        'email': account['email'],
        'roles': str(get_roles_as_Json_array(account))
    }
    # ToDo error handling
    response = post_request(url, digest_login, '/admin-ng/users/', data=data)

    return response


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborting process.")
        sys.exit(0)