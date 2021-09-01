import os
import sys
sys.path.append(os.path.join(os.path.abspath('..'), "lib"))

from args.digest_login import DigestLogin
from input_output.logger import Logger
from input_output.yaml_utils import read_yaml_file
from rest_requests.basic_requests import get_tenants
from parse_arguments import parse_args
from configure_users import check_external_api_accounts, check_system_accounts, set_config_users
from configure_groups import check_groups, set_config_groups
from configure_capture_accounts import check_capture_accounts, set_config_capture_accounts
import config


def main():

    ###   Parse args and config   ###
    digest_login = DigestLogin(user=config.digest_user, password=config.digest_pw)
    environment, tenant_to_check, check, verbose = parse_args()
    logger = Logger(verbose)
    # parse script config
    config.tenant_ids = get_tenants(config.server_url, digest_login)
    for ignored_tenant in config.ignored_tenants:
        config.tenant_ids.remove(ignored_tenant)
    if not hasattr(config, 'tenant_urls'):
        config.tenant_urls = {}
    for tenant_id in config.tenant_ids:
        if not tenant_id in config.tenant_urls:
            config.tenant_urls[tenant_id] = config.tenant_url_pattern.format(tenant_id)
    # read and parse organization config
    org_conf = read_yaml_file(config.org_config_path.format(environment))
    opencast_organizations = {}
    for organization in org_conf['opencast_organizations']:
        opencast_organizations[organization['id']] = organization
    # read group config
    group_config = read_yaml_file(config.group_config_path)
    # import config to scripts
    set_config_users(digest_login, org_conf, config, logger)
    set_config_groups(digest_login, group_config, config, logger)
    set_config_capture_accounts(org_conf, config, logger)

    # if tenant is not given, we perform the checks for all tenants
    tenants_to_check = [tenant_to_check] if tenant_to_check else config.tenant_ids

    ###   Start checks   ###
    for tenant_id in tenants_to_check:
        if check == 'users' or check == 'all':
            check_system_accounts(opencast_organizations['All Tenants']['switchcast_system_accounts'], tenant_id)
            check_external_api_accounts(opencast_organizations[tenant_id])
        if check == 'groups' or check == 'all':
            check_groups(tenant_id)
        if check == 'capture' or check == 'all':
            check_capture_accounts(opencast_organizations[tenant_id])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborting process.")
        sys.exit(0)
