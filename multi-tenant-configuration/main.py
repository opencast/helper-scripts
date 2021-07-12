import os
import sys
sys.path.append(os.path.join(os.path.abspath('..'), "lib"))

from args.digest_login import DigestLogin
from parsing_configurations import parse_args, read_yaml_file, parse_config
from configure_users import check_users
from configure_groups import check_groups
import config


def main():

    ###   Parse args and config   ###
    # ToDo Think about whether we should exclude Digest Login credentials from config.py file
    digest_login = DigestLogin(user=config.digest_user, password=config.digest_pw)  # create Digest Login
    environment, tenant_id, check = parse_args()                                    # parse args
    env_conf = read_yaml_file(config.env_path.format(environment))                  # read environment config file
    script_config = parse_config(config, env_conf, digest_login)                    # parse config.py
    group_config = read_yaml_file(script_config.group_path)                         # read group config file

    # if tenant is not given, we perform the checks for all tenants
    if tenant_id:
        tenants_to_check = [tenant_id]
    else:
        tenants_to_check = script_config.tenant_ids

    ###   Start checks   ###
    for tenant_id in tenants_to_check:
        if check == 'all':
            check_users(tenant_id=tenant_id, digest_login=digest_login, env_conf=env_conf, config=script_config)
            check_groups(tenant_id=tenant_id, digest_login=digest_login, group_config=group_config, config=script_config)
        elif check == 'users':
            check_users(tenant_id=tenant_id, digest_login=digest_login, env_conf=env_conf, config=script_config)
        elif check == 'groups':
            check_groups(tenant_id=tenant_id, digest_login=digest_login, group_config=group_config, config=script_config)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborting process.")
        sys.exit(0)
