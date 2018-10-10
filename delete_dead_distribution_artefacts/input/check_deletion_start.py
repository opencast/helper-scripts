from input_output.input import get_yes_no_answer


def check_deletion_start(dead_distribution_artefacts):
    """
    Present the distribution artefacts that can be deleted to the user and ask whether they should be deleted.

    :param dead_distribution_artefacts: The distribution artefacts that can be deleted.
    :type dead_distribution_artefacts: dict
    :return: Whether the deletion should be started.
    :rtype: bool
    """

    total = sum([len(dead_distribution_artefacts[tenant].keys()) for tenant in dead_distribution_artefacts.keys()])

    print("The distribution artefacts of the following {} media packages can be deleted:".format(total))
    print()
    print("Media package                         | Tenant")

    for tenant in dead_distribution_artefacts.keys():
        for media_package in dead_distribution_artefacts[tenant]:
            print("%36s | %s" % (media_package, tenant))
    print()

    start_recover = get_yes_no_answer("Start deletion?")
    print()

    return start_recover
