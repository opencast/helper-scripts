"""
This module makes enum definition easier.
"""
def enum(**named_values):
    """
    Create an enum with the following values.

    :param named_values:
    :return: enum
    :rtype: Enum
    """
    return type('Enum', (), named_values)