import os

workflow_dir = "workflow_definitions"


def get_workflow_definition(workflow):
    """
    Get workflow definition as string from file.

    :param workflow: Requested workflow
    :type workflow: Workflow
    :return: Workflow definition
    :rtype str:
    """

    workflow_path = os.path.abspath(os.path.join("fix", "workflows", workflow_dir, workflow))

    with open(workflow_path, 'r', newline='') as file:
        workflow = file.read()

    return workflow
