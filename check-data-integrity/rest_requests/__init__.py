"""
This package contains modules responsible for making requests to the opencast rest api.
It contains the following modules:

:Request modules:

- :Basic Requests: Get all tenants, series and events.
- Asset Requests: Get assets (ACLs or dublincore catalogs) of a series or event.
- OAIPMH Requests: Get oaipmh record of an event.

:Util modules:

- Request Error: Contains status code, url and requested asset description if a request fails.
- Get Response Content: Get content of a response in UTF8 as either json or xml.
"""
