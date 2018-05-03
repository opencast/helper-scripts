"""
This module defines the description for types of elements, catalogs and assets, mostly for building the error messages
"""
from collections import namedtuple

from util.enum import enum

Type = namedtuple("Type", ["singular", "plural", "unknown"])

ElementType = enum(
    SERIES=Type("series", "series", "series"),
    EVENT=Type("event", "events", "event(s)"),
    OAIPMH=Type("OAIPMH record of repository {}", "OAIPMH records of repository {}",
                "OAIPMH record(s) of repository {}")
)

CatalogType = enum(
    SERIES=Type("series", "series", "series"),
    EPISODE=Type("episode", "episode", "episode"),
    BOTH=Type("", "", "")
)

AssetType = enum(
    DC=Type("dublincore catalog", "dublincore catalogs", "dublincore catalog(s)"),
    ACL=Type("ACL", "ACLs", "ACL(s)")
)
