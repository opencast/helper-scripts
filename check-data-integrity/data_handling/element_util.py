"""
This module provides utility methods for series and events.
"""


def get_id(element) -> str:
    """
    Returns the id of an event or series.

    :param element: event or series
    :type element: dict
    :return: id of element
    :rtype: str
    """

    if "id" in element:
        return element["id"]
    elif "identifier" in element:
        return element["identifier"]
    else:
        raise ValueError("Element has no ID")


def has_series(event) -> bool:
    """
    Checks if the event belongs to a series.

    :param event:
    :type event: dict
    :rtype: bool
    """
    return "series" in event and event["series"]["id"]


def published_to_oaipmh(event) -> bool:
    """
    Checks if an event was published to at least one OAIPMH repository.

    :param event:
    :type event: dict
    :rtype: bool
    """

    if any("oaipmh" in publication["id"] for publication in event["publications"]):
        return True
    return False
