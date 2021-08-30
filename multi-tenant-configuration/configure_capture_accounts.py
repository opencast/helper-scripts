from rest_requests.request import get_request
from rest_requests.request_error import RequestError
from args.basic_login import BasicLogin
from input_output.logger import Logger


CONFIG = None
ENV_CONFIG = None


def set_config_capture_accounts(env_conf: dict, config: dict, logger: Logger):
    """
    Sets/imports the global config variables.
    must be called before any checks can be performed.
    :param env_conf: The environment configuration which specifies the user and system accounts
    :type env_conf: dict
    :param config: The script configuration
    :type config: dict
    :param logger: A Logger instance
    :type logger: Logger
    """

    global ENV_CONFIG
    global CONFIG
    global log
    ENV_CONFIG = env_conf
    CONFIG = config
    log = logger.log


def check_capture_accounts(tenant_id: str):
    """
    Performs the checks for each capture agent on the specified tenant
    :param tenant_id: The target tenant
    :type tenant_id: str
    """
    log('\nStart checking Capture Agent Accounts for tenant: ', tenant_id)

    # Check and configure Capture Agent Accounts:
    for organization in ENV_CONFIG['opencast_organizations']:
        # check switchcast system accounts
        if organization['id'] == tenant_id:
            for capture_agent_account in organization['capture_agent_accounts']:
                __check_capture_agent_account(capture_agent_account, tenant_id)


def __check_capture_agent_account(account: dict, tenant_id: str) -> bool:
    """
    Performs checks for the specified Capture Agent Account:
    - checks if username and password exists
    - checks if account has API access (and if password matches)
    Checks if the capture agent defined in the config has access to the service registry
    with the username and password defined in the config, and sends a get request to '/services/available.json'
    to find the ingest service. If check fails, prints a warning.

    :param account: The Capture Agent Account to be checked
    :type account: dict
    :param tenant_id: The target tenant
    :type tenant_id: str
    :return: bool
    """
    log(f"Checking Capture Agent Account {account['username']} on tenant {tenant_id}.")

    # check username and password
    if not account['username']:
        print('ERROR: No Capture Agent Account has been configured')
        return False
    if not account['password']:
        print(f"ERROR: No password configured for Capture Agent User {account['username']}")
        return False

    # Check if account has api access
    url = f'{CONFIG.tenant_urls[tenant_id]}/services/available.json?serviceType=org.opencastproject.ingest'
    login = BasicLogin(user=account['username'], password=account['password'])
    try:
        response = get_request(url, login, '/services/available.json', use_digest=False)
    except RequestError:
        print(f"WARNING: Capture Agent {account['username']} has no access.")
        return False
    except Exception as e:
        print('ERROR: Failed to check for API access.')
        print(str(e))
        return False

    if 'services' in response.json().keys():
        return True
    else:
        return False
