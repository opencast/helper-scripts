def count_media_packages(distribution_artefacts):
    """
    Count media packages in nested list.

    :param distribution_artefacts: Nested list containing distribution artefacts mapped to media packages and tenants
    :type distribution_artefacts: dict
    :return: Amount of media packages
    :rtype: int
    """
    return sum([len(distribution_artefacts[tenant].keys()) for tenant in distribution_artefacts.keys()])


def count_distribution_artefacts(distribution_artefacts):
    """
    Count distribution artefacts in nested list.

    :param distribution_artefacts: Nested list containing distribution artefacts mapped to media packages and tenants
    :type distribution_artefacts: dict
    :return: Amount of distribution artefacts
    :rtype: int
    """
    return sum([sum([len(distribution_artefacts[tenant][media_package]) for media_package in
                     distribution_artefacts[tenant].keys()]) for tenant in distribution_artefacts.keys()])


def get_max_path_len(distribution_artefacts):
    """
    Get the max length of the paths to the distribution artefacts.

    :param distribution_artefacts: Nested list containing distribution artefacts mapped to media packages and tenants
    :type distribution_artefacts: dict
    :return: Max path length
    :rtype: int
    """

    return max(max(max([[[len(dist_list) for dist_list in distribution_artefacts[tenant][media_package]]
                        for media_package in distribution_artefacts[tenant]]
                   for tenant in distribution_artefacts.keys()])))
