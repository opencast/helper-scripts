from input_output.input import get_configurable_answer
from util.count import get_max_path_len
from utility.enum import enum

PresentAnswer = enum(
    ASK="a",
    DELETE="d",
    QUIT="q"
)


def present_dead_distribution_artefacts(dead_distribution_artefacts, level=0):
    """
    Present the distribution artefacts that can be deleted to the user.

    :param dead_distribution_artefacts: The distribution artefacts that can be deleted.
    :type dead_distribution_artefacts: dict
    :param level: The level to indent the message to (default: 0)
    :type level: int
    """

    max_path_len = get_max_path_len(dead_distribution_artefacts)

    print(" Tenant         | Media package                        | Distribution artefacts")
    print(" {}".format("-"*(max_path_len + 56)))
    max([(len(x), x) for x in ('a', 'b', 'aa')])

    for tenant in dead_distribution_artefacts.keys():
        for mp_count, media_package in enumerate(dead_distribution_artefacts[tenant]):

            for dist_count, distribution_artefact in enumerate(dead_distribution_artefacts[tenant][media_package]):

                tenant_str = (tenant if (mp_count == 0 and dist_count == 0) else "")
                media_package_str = (media_package if dist_count == 0 else "")

                print("{:>15} | {:>36} | {}".format(tenant_str, media_package_str, distribution_artefact))

    print()

    long_descriptions = ["asking for each media package",
                         "deleting all without asking",
                         "quitting the script"]
    short_descriptions = ["ask", "delete", "quit"]
    options = ['a', 'd', 'q']

    question = "Do you wish to delete all or be asked for each media package?"

    answer = get_configurable_answer(options, short_descriptions, long_descriptions, question, level)
    return answer
