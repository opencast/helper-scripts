# Script for checking data integrity
This script can be used to check the integrity of certain data in opencast. The main goal of this script is to focus on the effects of the most common problems in opencast which can lead to data of series or events getting lost, corrupted or no longer being up-to-date.

### Usage
This script can be called with the following parameters (all parameters in braces are optional, the others required):
`main.py -o OPENCAST -u USER [-p PASSWORD] [-c {dc,acl,oaipmh,all}] [-s] [-t]`

| Short option       | Long option          | Description  | Default |
| :-------------: |:-------------| :-----| :-----------|
| `-o`            | `--opencast` | URL of opencast ||
| `-u` | `--user`      |   User for digest authentication |  |
| `-p` | `--password` | Password for digest authentication | Read password in after start-up |
| `-c` | `--check` | Defines which checks are to be performed, valid arguments are: *dc*, *acl*, *dc&acl*, *oaipmh*, *all*| All checks are performed |
| `-s`      | `-- silent`      |   Flag for disabling progress output | Progress output enabled |
| `-t`      | `-- https`      |   Flag for enabling https | Http |

##### Usage Example
`main.py` `-a` producer.opencast.org `-u` opencast_system_account `-p` CHANGE_ME `-c` dc `-t`

### Requirements
- Python 3
- `requests`-Package

##### A few words on compability
For receiving the data mainly `/admin-ng/` endpoints are used (with the exception of dublincore catalogs and ACLs of series that are requested from the series service) since they provide the necessary data in convenient ways, though this bears the risk of incompability with later opencast versions. This script was tested with Opencast 4.x and 5.x and is not garanteed to work with earlier or later versions, though it can be assumed that compability could be achieved fairly easily by adapting the files in the `rest_requests` module and adding more/different parsing functionality if necessary.

### Checks performed by this script
The checks that are performed by this script can be limited with the `--check` parameter. The following options are available:

| Option       | Description         |
| :------------- |:-------------|
| *dc*            | Only check dublincore catalogs, skip ACLs and OAIPMH. |
| *acl*            | Only check ACLs, skip dublincore catalogs and OAIPMH. |
| *dc&acl*            | Check ACLs and dublincore catalogs, skip OAIPMH. |
| *oaipmh*         | Same effect as *all* since the dublincore catalogs and ACLs are needed for the check of OAIPMH. |
| *all*            | Default setting, all checks are performed. |

By default, all checks are performed. They can be grouped into the following subcategories, each with their own set of conditions:

- General checks that are always performed:
  * If an event belongs to a series, the series id of the event should match exactly one series of those that currently exist (not more than one and not one that doesn't currently exist).

- Dublincore catalog checks:
  * An event should have exactly one episode dublincore catalog (not more than one and not none).
  * If an event belongs to a series, it should have exactly one series dublincore catalog (not more than one, not none).
    * Additionally that dublincore catalog should match that of the series itself.
  * If an event doesn't belong to a series, it shouldn't have one (or more) series dublincore catalogs

- ACL checks:
  * If an event doesn't belong to a series*, it should have exactly one episode ACL (not more than one and not none).
  * If an event belongs to a series, it should have exactly one series ACL (not more than one, not none).
    * Additionally that ACL should match that of the series itself.
  * If an event doesn't belong to a series, it shouldn't have one (or more) series ACLs.

- OAIPMH checks:
    * The same conditions for ACLs and dublincore catalogs of an event also apply to those in an OAIPMH repository.
    * Additionally they should match those of the corresponding event that was published to this repository:
        * If an element exists for the event it should exist in the OAIPMH repository.
            * Additionally the contents should match.
        * If an element doesn't exist for the event (e.g. no episode ACL), then it also should not exist in the OAIPMH repository.

(\* This is the only difference between the checks of dublincore catalogs and ACLs: An episode ACL can be missing if there is a series ACL instead, an episode dublincore catalog should *never* be missing.)

Additionally to any violation of the conditions described above, any errors during parsing or requesting of data via the rest endpoints are also collected and displayed to the user.

**Attention:** If an element fails one more more of these tests (e.g. there's more than one series dublincore catalog for an event), then in place of that element a Malformed object is returned that contains the encountered errors. Further tests including this element (e.g. comparison with the dublincore catalog of the corresponding series) are then skipped since they can not be conducted in a meaningful way. Because of this it might make sense to run the script again after one kind of error has been fixed.

##### Comparing ACLs and dublincore catalogs
Currently only ACLs are parsed into a different data structure (with a tuple of role and action as the key and the boolean signifying whether it's an allow rule as the value) since these are not available in the same formats for series and events. Because of this, the comparison of ACLs is not order-sensitive and only checks if each rule that is present in one ACL is contained in the other ACL with the same values and vice versa. On the contrary, dublincore catalogs are compared by checking each attribute and its value for equality in order since they should match exactly between events and their corresponding series.

##### What is not checked by this script
* The right amount of ACLs and dublincore catalogs of *series* is not checked explicitly since
    1. all series are saved in a database so it's not possible for a series to have more than one ACL or dublincore catalog, and
    2. if a series is missing it's ACL or dublincore catalog a 404 Error will be encountered on request to the series service.
* It is also currently not checked whether there is data contained in an OAIPMH repository that doesn't belong to a currently existing event (e.g. when an event was deleted, but wasn't retracted from OAIPMH before).

### Execution Overview
The data integrity checks are executed as follows:

    Parse arguments, check for correctness, set settings
    If no digest password: Read in digest password
    Get tenants
    For each tenant:
        Get all series
        If necessary: Get dublincore catalogs of series
        If necessary: Get ACLs of series
        Get all events
        Check relationship of events to series (belongs to one existing series or none?)
        If necessary: Get episode & series dublincore catalogs of events and check them if necessary (right amount, matching those of series?)
        If necessary: Get episode & series ACLs of events and check them (right amount, matching those of series?)
        If necessary:
            For each event:
                For each oaipmh repository it was published to:
                    Compare episode & series dc (matching amount and content?)
                    Compare episode & series ACL (matching amount and content?)
        Print results for current tenant
    Print all results again for a final overview