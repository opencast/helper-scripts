from parsing_configurations import log
import re


permissions = {
    'user': {},
    'group': {}
}
ANSWER_PATTERN = r"^[yn]$|^[yn][ta][ta]$"
HELP_OPTION = 'h'


def check_or_ask_for_permission(target_type, action, target_name, tenant_id, option_i=False) -> bool:

    # check if permission is already defined
    permission = get_permission(target_type, action, target_name, tenant_id)
    if permission is None:
        # otherwise ask for user input ...
        answer = ask_user(target_type, action, target_name, tenant_id, option_i)
        # ... and process answer and update permissions
        permission = process_answer(answer, target_type, action, target_name, tenant_id, option_i)

    return permission


def get_permission(target_type, action, target_name, tenant_id) -> bool:

    log('permissions: ', permissions)

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

    individual_option = "\n    Write 'i' to perform the action individually for each case. " if option_i else ""

    help_description = f"""    Write 'y' to perform the action. Write 'n' to skipp this action. {individual_option}
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
        elif parsable(answer) or (option_i and answer == 'i'):
            return answer
        # catch all invalid answers
        else:
            answer = input(f"Invalid answer. Write '{HELP_OPTION}' for help.\n").lower()


def parsable(answer) -> bool:

    if re.match(ANSWER_PATTERN, answer) or answer == HELP_OPTION:
        return True
    else:
        return False


def __build_key(action, tenant, target):
    return action + ':' + tenant + ':' + target


def process_answer(answer, target_type, action, target_name, tenant_id, option_i) -> bool:

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
