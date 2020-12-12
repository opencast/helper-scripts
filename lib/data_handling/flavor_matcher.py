def __split_flavor(flavor):
    """
    Split a flavor into type and subtype.

    :param flavor: The flavor to split
    :type flavor: str
    :return: type, subtype
    :rtype: str, str
    :raise: ValueError
    """
    flavor_types = flavor.split("/")
    if len(flavor_types) != 2:
        raise ValueError("Invalid flavor")

    flavor_type = flavor_types[0]
    flavor_subtype = flavor_types[1]
    return flavor_type, flavor_subtype


def matches_flavor(asset_flavor, config_flavors):
    """
    Check if a flavor matches the flavors in a list. The latter can contain the placeholder "*".

    :param asset_flavor: The flavor to check
    :type asset_flavor: str
    :param config_flavors: The flavors to match (can contain "*")
    :type config_flavors: list
    :return: Whether the flavor matches.
    :rtype: bool
    """

    asset_flavor_type, asset_flavor_subtype = __split_flavor(asset_flavor)
    for config_flavor in config_flavors:
        config_flavor_type, config_flavor_subtype = __split_flavor(config_flavor)

        if (config_flavor_type == "*" or config_flavor_type == asset_flavor_type) and \
           (config_flavor_subtype == "*" or config_flavor_subtype == asset_flavor_subtype):
            return True

    return False
