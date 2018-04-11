"""
This package contains modules related to checking the data integrity:

- :Get Assets: Request assets from the rest API and check them for errors before returning them, return Malformed objects instead if any errors were found.
- :Check data: Check elements for errors and return the error messages for any that are found.
- :Errors: Build the error messages.
- :Malformed: Is a placeholder for any element that is malformed in any way, contains error messages for all errors that were encountered for this element.
- :Types: Contains Enums for element, catalog and asset types, mostly for building the error messages.
"""