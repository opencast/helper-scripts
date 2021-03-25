import os
import sys
sys.path.append(os.path.join(os.path.abspath('..'), "lib"))

# import io
# import yaml
# from args.args_parser import get_args_parser
# from args.args_error import args_error
# from rest_requests.request_error import RequestError
from input_output.input import get_yes_no_answer
from args.digest_login import DigestLogin
from utils import parse_args, read_yaml_file, parse_config, create_user
import config


# ToDo
# add logger
# add interaction question

def main():
    """
    configure Groups and Users
    """

    # parse args
    environment, tenant_id = parse_args()
    # read environment config file
    env_conf = read_yaml_file(config.env_path.format(environment))
    # parse config.py
    parse_config(config, env_conf)
    # create Digest Login
    digest_login = DigestLogin(user=config.digest_user, password=config.digest_pw)

    start_process = get_yes_no_answer("Create User?")
    if not start_process:
        __abort_script("Okay, not doing anything.")

    external_api_accounts = env_conf['opencast_organizations'][1]['external_api_accounts']

    if not tenant_id:
        for_all_tenants = get_yes_no_answer("Create User for all tenants?")
        if for_all_tenants:
            # create user account on all tenants
            for tenant_url in config.tenant_urls:
                for account in external_api_accounts:
                    response = create_user(account, digest_login, tenant_url)
                    # json_content = get_json_content(response)
                    print(response)
    else:
        # create user accounts on the specified tenant
        for account in external_api_accounts:
            tenant_url = config.tenant_urls[tenant_id]
            response = create_user(account, digest_login, tenant_url)
            if response:
                print("created user {}".format(account['username']))

def __abort_script(message):
    print(message)
    sys.exit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborting process.")
        sys.exit(0)
