"""
This module defines a Malformed object to replace an element or asset if any errors were encountered while checking it.
It contains the error messages for the encountered errors.
"""

from collections import namedtuple

Malformed = namedtuple('Malformed', ['errors'])
