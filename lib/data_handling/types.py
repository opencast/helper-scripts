"""
This module defines the description for elements, assets and assettypes, mostly for building the error messages,
as singular, plural and unknown/both.
"""
from utility.enum import enum


class Description:

    def __init__(self, singular, plural, unknown):
        self.singular_description = singular
        self.plural_description = plural
        self.unknown_description = unknown

    def format(self, *formatting_strings):
        self.singular_description = self.singular_description.format(*formatting_strings)
        self.plural_description = self.plural_description.format(*formatting_strings)
        self.unknown_description = self.unknown_description.format(*formatting_strings)
        return self

    def singular(self):
        return self.singular_description

    def plural(self):
        return self.plural_description

    def unknown(self):
        return self.unknown_description


# Elements can be an event, a series or an OAIPMH record.
ElementDescription = enum(
    SERIES=Description("series", "series", "series"),
    EVENT=Description("event", "events", "event(s)"),
    OAIPMH=Description("OAIPMH record of repository {}", "OAIPMH records of repository {}",
                       "OAIPMH record(s) of repository {}")
)

# Assets belong to elements and can be either dublincore catalogs or ACLs.
AssetDescription = enum(
    DC=Description("dublincore catalog", "dublincore catalogs", "dublincore catalog(s)"),
    ACL=Description("ACL", "ACLs", "ACL(s)")
)

# Assets (ACL or dublincore catalogs) can either be of type episode, series or both/undefined.
AssetTypeDescription = enum(
    SERIES=Description("series", "series", "series"),
    EPISODE=Description("episode", "episode", "episode"),
    BOTH=Description("", "", "")
)
