import re


permissions = {
    'user': {},
    'group': {}
}
ANSWER_PATTERN = r"^[yn]$|^[yn][ta][ta]$"
HELP_OPTION = 'h'


def check_or_ask_for_permission(target_type, action, target_name, tenant_id, option_i=False) -> bool:
    """
    Check if a permission for the action was already given or asks for permission.

    :param target_type: The target for the action (either 'user' or 'group')
    :type target_type: str
    :param action: The action to be performed
    :type action: str
    :param target_name: The group or user name
    :type target_name: str
    :param tenant_id: The target tenant
    :type tenant_id: str
    :param option_i: Whether the user has the option to perform the action iteratively.
    :type option_i: bool
    :return: bool, whether the action should be performed.
    """

    # check if permission is already defined
    permission = get_permission(target_type, action, target_name, tenant_id)
    if permission is None:
        # otherwise ask for user input ...
        answer = ask_user(target_type, action, target_name, tenant_id, option_i)
        # ... and process answer and update permissions
        permission = process_answer(answer, target_type, action, target_name, tenant_id, option_i)

    return permission


def get_permission(target_type, action, target_name, tenant_id) -> bool:
    """
    Returns the permission for the given action.
    If no permission value is found, None is returned

    :param target_type: The target for the action (either 'user' or 'group')
    :type target_type: str
    :param action: The action to be performed
    :type action: str
    :param target_name: The group or user name
    :type target_name: str
    :param tenant_id: The target tenant
    :type tenant_id: str
    :return: bool or None, the permission value
    """

    key = __build_key(action, tenant_id, target_name)
    if key in permissions[target_type].keys():
        return permissions[target_type][key]
    key = __build_key(action, tenant='all', target=target_name)
    if key in permissions[target_type].keys():
        return permissions[target_type][key]
    key = __build_key(action, tenant=tenant_id, target='all')
    if key in permissions[target_type].keys():
        return permissions[target_type][key]
    key = __build_key(action, tenant='all', target='all')
    if key in permissions[target_type].keys():
        return permissions[target_type][key]

    return None


def ask_user(target_type, action, target_name, tenant_id, option_i=False) -> str:
    """
    Asks the user for permission to perform a certain action.
    Returns the answer.
    The answer can be stored if the user specifies if the answer holds for:
    - all tenants, or
    - all targets (i.e. all groups or all ), or
    - both.
    This can done by adding 'a' or 't' to the answer.
    For example:
    'yat' corresponds to 'Yes, always do this action on all tenants for this target'.

    :param target_type: The target for the action (either 'user' or 'group')
    :type target_type: str
    :param action: The action in question
    :type action: str
    :param target_name: The group or user name
    :type target_name: str
    :param tenant_id: The target tenant
    :type tenant_id: str
    :param option_i: Whether the user has the option to answer with i.
    :type option_i: bool
    :return: str, the answer of the user
    """

    individual_option = "\nWrite 'i' to perform the action individually for each case. " if option_i else ""

    help_description = f"""Write 'y' to perform the action. Write 'n' to skipp this action. {individual_option}
Add 't' for 'tenant' or 'a' for 'all' to store your decision for this or all tenants.
Add 't' for 'target' or 'a' for 'all' to store your decision for this or all targets.
EXAMPLE: Write 'yat' to store your decision for the action on ALL tenants and for THIS target.
"""

    question = f"Do you want to {action} ({target_type} {target_name} on {tenant_id})? Write '{HELP_OPTION}' for help.\n"

    # ask the question
    answer = input(question).lower()
    while True:
        # catch the help option: give a more detailed description of the options
        if answer == HELP_OPTION:
            answer = input(help_description)
        # return all valid answers
        elif __parsable(answer, option_i):
            return answer
        # catch all invalid answers
        else:
            answer = input(f"Invalid answer. Write '{HELP_OPTION}' for help.\n").lower()


def process_answer(answer, target_type, action, target_name, tenant_id, option_i) -> bool:
    """
    Processes an answer and, if specified, stores it as a permission.
    Returns a boolean, whether the action should be performed.

    :param target_type: The target for the action (either 'user' or 'group')
    :type target_type: str
    :param action: The action to be performed
    :type action: str
    :param target_name: The group or user name
    :type target_name: str
    :param tenant_id: The target tenant
    :type tenant_id: str
    :param option_i: Whether the user has the option to perform the action iteratively.
    :type option_i: bool
    :return: bool, whether the action should be performed.
    """

    # simple yes or no case (not stored)
    if answer == 'y':
        return True
    if answer == 'n':
        return False
    # individual case
    if option_i and answer == 'i':
        return 'i'

    # store answer if user specified this
    permission_value = True if answer.startswith('y') else False
    tenant = 'all' if answer[1] == 'a' else tenant_id
    target = 'all' if answer[2] == 'a' else target_name
    key = __build_key(action, tenant, target)
    permissions[target_type][key] = permission_value

    return permission_value


def __parsable(answer, option_i=False) -> bool:
    """
    Checks if an answer is parsable, i.e. matches the answer pattern.

    :param answer: The answer given by the user
    :type answer: str
    :param option_i: Whether 'i' is an acceptable answer
    :type option_i: str
    :return: bool, whether the answer is parsable
    """

    return re.match(ANSWER_PATTERN, answer) or answer == HELP_OPTION or (option_i and answer == 'i')


def __build_key(action, tenant, target):
    """
    Builds the key to store the permission in the dictionary.
    """
    return action + ':' + tenant + ':' + target
