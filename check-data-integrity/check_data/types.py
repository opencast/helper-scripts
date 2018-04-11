"""
This module defines the description for types of elements, catalogs and assets, mostly for building the error messages
"""

from util.enum import enum

ElementType = enum(
    SERIES = "series",
    EVENT = "event",
    OAIPMH = "OAIPMH record of repository {}",
    SERIES_EVENT = "series and event",
    EVENT_OAIPMH = "event and OAIPMH record of repository {}"
)

CatalogType = enum(
    SERIES = "series",
    EPISODE = "episode",
    BOTH = "episode and series"
)

AssetType = enum(
    DC = "dublincore",
    ACL = "acl"
)