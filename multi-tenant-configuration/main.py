import os
import sys
sys.path.append(os.path.join(os.path.abspath('..'), "lib"))

from args.digest_login import DigestLogin
from input_output.logger import Logger
from input_output.yaml_utils import read_yaml_file
from rest_requests.basic_requests import get_tenants
from parse_arguments import parse_args
from configure_users import check_users, set_config_users
from configure_groups import check_groups, set_config_groups
from configure_capture_accounts import check_capture_accounts, set_config_capture_accounts
import config


def main():

    ###   Parse args and config   ###
    digest_login = DigestLogin(user=config.digest_user, password=config.digest_pw)
    environment, tenant_id, check, verbose = parse_args()
    logger = Logger(verbose)
    # read and parse organization config
    org_conf = read_yaml_file(config.org_config_path.format(environment))
    config.tenant_ids = get_tenants(config.server_url, digest_login)
    config.tenant_ids.remove('mh_default_org')
    if not hasattr(config, 'tenant_urls'):
        config.tenant_urls = {}
    for tenant_id in config.tenant_ids:
        if not tenant_id in config.tenant_urls:
            config.tenant_urls[tenant_id] = config.tenant_url_pattern.format(tenant_id)
    # read group config
    group_config = read_yaml_file(config.group_config_path)
    # import config to scripts
    set_config_users(digest_login, org_conf, config, logger)
    set_config_groups(digest_login, group_config, config, logger)
    set_config_capture_accounts(org_conf, config, logger)

    # if tenant is not given, we perform the checks for all tenants
    tenants_to_check = [tenant_id] if tenant_id else config.tenant_ids

    ###   Start checks   ###
    for tenant_id in tenants_to_check:
        if check == 'all':
            check_users(tenant_id)
            check_groups(tenant_id)
            check_capture_accounts(tenant_id)
        elif check == 'users':
            check_users(tenant_id)
        elif check == 'groups':
            check_groups(tenant_id)
        elif check == 'capture':
            check_capture_accounts(tenant_id)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborting process.")
        sys.exit(0)
