""" This module represents the check-argument. """
from utility.enum import enum

Checks = enum(
    DC="dc",
    ACL="acl",
    DC_ACL="dc_acl",
    OAIPMH="oaipmh",
    ALL="all"
)


class CheckSettings:
    """
    Contains the settings that define which data is supposed to be checked: ACLs, Dublin Core catalogs, oaipmh
    or everything.
    Since the check of OAIPMH needs the ACLs and Dublin Core catalogs of series and events, these are always requested
    (and checked) when the OAIPMH check is enabled.
    """

    def __init__(self, check):
        if not check:
            self.check = Checks.ALL
        else:
            self.check = check

    def check_acl(self):
        """
        :return: whether ACLs are supposed to be requested and checked for errors.
        :rtype: bool
        """
        return (self.check == Checks.ACL or self.check == Checks.ALL or self.check == Checks.OAIPMH or
                self.check == Checks.DC_ACL)

    def check_dc(self):
        """
        :return: whether Dublin Core catalogs are supposed to be requested and checked for errors.
        :rtype: bool
        """
        return (self.check == Checks.DC or self.check == Checks.ALL or self.check == Checks.OAIPMH or
                self.check == Checks.DC_ACL)

    def check_oaipmh(self):
        """
        :return: whether OAIPMH is supposed to be checked for errors.
        :rtype: bool
        """

        return self.check == Checks.ALL or self.check == Checks.OAIPMH
