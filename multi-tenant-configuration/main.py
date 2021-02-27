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
    # create user accounts on the specified tenant
    for account in external_api_accounts:
        url = config.tenant_urls[tenant_id]
        print(url)
        response = create_user(account, digest_login, url)
        json_content = get_json_content(response)
        print(response)


def __abort_script(message):
    print(message)
    sys.exit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborting process.")
        sys.exit(0)
