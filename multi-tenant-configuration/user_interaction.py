from parsing_configurations import log
import re


permissions = {
    'user': {},
    'group': {}
}
ANSWER_PATTERN = r"^[yn]$|^[yn][ta][ta]$"
HELP_OPTION = 'h'
ALL = 'all'


def check_or_ask_for_permission(target_type, action, target_name, tenant_id, option_i=False) -> bool:

    # check if permission is already defined
    permission = get_permission(target_type, action, target_name, tenant_id)
    if permission is None:
        # otherwise ask for user input
        answer = ask_user(target_type, action, target_name, tenant_id, option_i)
        # process answer and update permissions
        permission = process_answer(answer, target_type, action, target_name, tenant_id, option_i)

    return permission


def get_permission(target_type, action, target_name, tenant_id) -> bool:

    log('permissions: ', permissions)

    # permission = None
    # target_permission = None
    # tenant_permission = None

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

    # try:
    #     for p in permissions[target_type][action]:
    #         # most specific permission
    #         if p.tenant == tenant_id and p.target == target_name:
    #             permission = p.permission_value
    #             break
    #         # either tenant or target specific
    #         elif p.tenant == 'all' and p.target == target_name:
    #             target_permission = p.permission_value
    #         elif p.tenant == tenant_id and p.target == 'all':
    #             tenant_permission = p.permission_value
    #         # most general permission
    #         elif p.tenant == 'all' and p.target == 'all':
    #             permission = p.permission_value
    #
    #     # target permission is prioritized over tenant permission
    #     # both will overwrite a general permission
    #     if target_permission is not None:
    #         permission = target_permission
    #     elif tenant_permission is not None:
    #         permission = tenant_permission

    # if no permission is found, None is returned
    # except KeyError:
    #     print('no permission found')
    #
    # return permission


def ask_user(target_type, action, target_name, tenant_id, option_i=False) -> str:

    help_description = "Valid answers are: \nHELP DESCRIPTION"

    individual_option = "\n    Write 'i' to perform the action individually for each case. " if option_i else ""

    question = f"""Do you want to {action} ({target_type} {target_name} on {tenant_id})? 
    Write 'y' to perform the action. Write 'n' to skipp this action. {individual_option}Write '{HELP_OPTION}' for help.
    Add 't' for 'tenant' or 'a' for 'all' to store your decision for this or all tenants.
    Add 't' for 'target' or 'a' for 'all' to store your decision for this or all targets.
    EXAMPLE: Write 'yat' to store your decision for the action on ALL tenants and for THIS target.
"""

    answer = ''
    while True:
        # catch the help option: give a more detailed description of the options
        if answer == HELP_OPTION:
            answer = input(help_description)
        # ask the question
        else:
            answer = input(question).lower()
        # return all valid answers
        if parsable(answer) or (option_i and answer == 'i'):
            return answer
        else:
            print("Invalid answer.\n")


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
        return answer

    # store answer if user specified this
    permission_value = True if answer.startswith('y') else False
    tenant = 'all' if answer[1] == 'a' else tenant_id
    target = 'all' if answer[2] == 'a' else target_name
    # p = Permission(tenant, target, permission_value)
    key = __build_key(action, tenant, target)
    permissions[target_type][key] = permission_value

    # try:
    #     # permissions[target_type][action].append(p)
    #     permissions[target_type][action][tenant][target] = permission_value
    # except:
    #     permissions[target_type][action] = [p]

    return permission_value

