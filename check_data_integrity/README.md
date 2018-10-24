# Overview

This module consists of two scripts: One for checking the data of an opencast instance for inconsistencies called
`check.py` and one for fixing some of the inconsistencies found called `fix.py`, along with some utility functionality
separated by script. More detailed descriptions of what these scripts do and how they can be used follow below.

Additionally to the modules in this folder both scripts use modules contained in the _lib_ directory.

## Script for checking data integrity

This script can be used to check the integrity of certain data in Opencast. The main goal of this script is to focus on
the effects of the most common problems of Opencast which can lead to data of series or events getting lost, corrupted
or no longer up-to-date.

### Usage

This script can be called with the following parameters (all parameters in brackets are optional, the others required;
options in braces represent alternatives):

    check.py -o OPENCAST [-t CHOSEN_TENANTS] [-e EXCLUDED-TENANTS] -u USER [-p PASSWORD] [-c {dc,acl,dc_acl,oaipmh,all}]
    [-s] [-l] [-n] [-r] [-d RESULTS_DIR]

| Short option | Long option          | Description                                                                                         | Default                           |
| :----------: | :------------------- | :-------------------------------------------------------------------------------------------------- | :-------------------------------- |
| `-o`         | `--opencast`         | URL of the Opencast instance without protocol                                                       |                                   |
| `-t`         | `--chosen-tenants`   | List* of tenants to be checked (can't be used with `--excluded-tenants`)                            | All tenants are chosen            |
| `-e`         | `--excluded-tenants` | List* of tenants to be excluded (can't be used with `--tenants`)                                    | No tenants are excluded           |
| `-u`         | `--user`             | User for digest authentication                                                                      |                                   |
| `-p`         | `--password`         | Password for digest authentication                                                                  | Prompt for password after startup |
| `-c`         | `--check`            | Defines which checks are to be performed (options: `dc`, `acl`, `dc_acl`, `oaipmh`, `all`)          | All checks are performed          |
| `-s`         | `--silent`           | Flag for disabling progress output (can't be used with `--no-fancy-output`)                         | Progress output enabled           |
| `-l`         | `--https`            | Flag for enabling HTTPS                                                                             | HTTP                              |
| `-n`         | `--no-fancy-output`  | Flag for disabling progress bars if the terminal can't display them (can't be used with `--silent`) | Fancy output enabled              |
| `-r`         | `--no-series-error`  | Flag for treating events without series as malformed                                                | Events without series are valid   |
| `-d`         | `--results-dir`      | Path to results directory                                                                           | Current working directory         |

(\* Options with multiple arguments can be used by specifying the option once, followed by at least one or more argument(s) separated by spaces (see example below.)

##### Usage example

    check.py -o producer.opencast.org -e tube mh_default_org -u opencast_system_account -p CHANGE_ME -c dc -l -n -r -d
    /home/me/Desktop/results

### Requirements

- Python 3
- `requests`-Package

##### A few words on compatibility

The script mainly uses `/admin-ng/` endpoints for receiving the data (with the exception of Dublin Core catalogs and
ACLs of series, which are both requested from the series service) since they provide the necessary data in a convenient
way, though this bears the risk of incompatibility with future Opencast versions. This script was tested with Opencast
4.x, 5.x and the current (11/09/2018) state of develop and is not guaranteed to work with earlier or later versions,
though it can be assumed that compatibility could be achieved fairly easily by adapting the files in the `rest_requests`
module and adding more/different parsing functionality if necessary.

### Checks performed by this script

The checks that are performed by this script can be limited with the `--check` parameter. The following options are
available:

| Option   | Description                                                                                       |
| :------- | :------------------------------------------------------------------------------------------------ |
| `dc`     | Only check Dublin Core catalogs, skip ACLs and OAI-PMH.                                           |
| `acl`    | Only check ACLs, skip Dublin Core catalogs and OAI-PMH.                                           |
| `dc_acl` | Check ACLs and Dublin Core catalogs, skip OAI-PMH.                                                |
| `oaipmh` | Same effect as `all` since the Dublin Core catalogs and ACLs are needed for the check of OAI-PMH. |
| `all`    | Default setting, all checks are performed.                                                        |

By default, all checks are performed. They can be grouped into the following subcategories, each with its own set of
conditions:

- General checks that are always performed:
  * If an event belongs to a series, the series ID of the event should match exactly one series of those that currently
  exist (not more than one, not none).
  * Additionally with the `--no-series-error` flag it can be enforced that events should always belong to series.

- Dublin Core catalog checks:
  * An event should have exactly one episode Dublin Core catalog (not more than one, not none).
  * If an event belongs to a series, it should have exactly one series Dublin Core catalog (not more than one, not
  none).
    * Additionally that Dublin Core catalog should match that of the series itself.
  * If an event doesn't belong to a series, it shouldn't have one (or more) series Dublin Core catalogs

- ACL checks:
  * If an event doesn't belong to a series*, it should have exactly one episode ACL (not more than one, not none).
  * If an event belongs to a series, it should have exactly one series ACL (not more than one, not none).
    * Additionally that ACL should match that of the series itself.
  * If an event doesn't belong to a series, it shouldn't have one (or more) series ACLs.

- OAI-PMH checks:
  * The same conditions for ACLs and Dublin Core catalogs of an event also apply to those in an OAI-PMH repository.
  * Additionally they should match those of the corresponding event that was published to this repository:
    * If an element exists for the event it should exist in the OAI-PMH repository.
      * Additionally the contents should match.
    * If an element doesn't exist for the event (e.g. no episode ACL), then it also should not exist in the OAI-PMH
    repository.

(\* This is the only difference between the checks of Dublin Core catalogs and ACLs: An episode ACL can be missing if
there is a series ACL instead, an episode Dublin Core catalog should *never* be missing.)

In addition to any violation of the conditions described above, any errors during parsing or requesting of data via the
REST endpoints are also collected.

**Attention:** If an element fails one or more of these tests (e.g. there's more than one series Dublin Core catalog for
an event), then in place of that element a `Malformed` object is returned that contains all the errors encountered.
Further tests involving this element (e.g. comparison with the Dublin Core catalog of the corresponding series) are
then skipped since they can not be conducted in a meaningful way. Because of this it might make sense to run the script
again after one type of error has been fixed.

##### Comparing ACLs and Dublin Core catalogs

Currently only ACLs are parsed into a different data structure (with a tuple of role and action as the key and the
Boolean signifying whether it's an allow-rule as the value) since these are not available in the same formats for
series and events. Because of this, the comparison of ACLs is not order-sensitive and only checks if each rule that is
present in one ACL is contained in the other ACL with the same values and vice versa. Dublin Core catalogs are in
contrast compared by checking each attribute and its value for equality in order since they should match exactly between
events and their corresponding series.

##### What is not checked by this script

* The right amount of ACLs and Dublin Core catalogs of *series* is not checked explicitly since
  1. all series are saved in a database so it's not possible for a series to have more than one ACL or Dublin Core
  catalog, and
  2. if a series is missing it's ACL or Dublin Core catalog a 404 Error will be encountered on request to the series
  service.
* It is also currently not checked whether there is data contained in an OAI-PMH repository that doesn't belong to a
currently existing event (e.g. when an event was deleted but wasn't retracted from OAI-PMH before).

### Execution

The data integrity checks are executed as follows:

    Parse arguments, check for correctness, initialize settings
    If no digest password: Ask for digest password
    If no chosen tenants: Get all tenants
    If excluded-tenants: Filter tenants
    For each tenant:
        Get all series
        If necessary: Get Dublin Core catalogs of series
        If necessary: Get ACLs of series
        Get all events
        Check relationship of events to series
        If necessary: Get episode & series Dublin Core catalogs of events and check them
        If necessary: Get episode & series ACLs of events and check them
        If necessary:
            For each event:
                For each OAI-PMH repository it was published to:
                    Compare episode & series Dublin Core catalogs
                    Compare episode & series ACLs
        Print results for current tenant
    Print all results for a final overview

## Script for fixing data inconsistencies

This script can be used to fix some of the data inconsistencies found by the script presented above.

### Usage

This script can be called with the following parameters (all parameters in brackets are optional, the others required;
options in braces represent alternatives):

    fix.py -o OPENCAST [-c CHOSEN_TENANTS] [-e EXCLUDED-TENANTS] -u USER [-p PASSWORD] [-s] [-l] [-d RESULTS_DIR]
    [-w WAITING_PERIOD] [-b BATCH_SIZE]

| Short option | Long option          | Description                                                                                         | Default                           |
| :----------: | :------------------- | :-------------------------------------------------------------------------------------------------- | :-------------------------------- |
| `-o`         | `--opencast`         | URL of the Opencast instance without protocol                                                       |                                   |
| `-c`         | `--chosen-tenants`   | List* of tenants to be checked (can't be used with `--excluded-tenants`)                            | All tenants are chosen            |
| `-e`         | `--excluded-tenants` | List* of tenants to be excluded (can't be used with `--tenants`)                                    | No tenants are excluded           |
| `-u`         | `--user`             | User for digest authentication                                                                      |                                   |
| `-p`         | `--password`         | Password for digest authentication                                                                  | Prompt for password after startup |
| `-n`         | `--no-fancy-output`  | Flag for disabling progress bars if the terminal can't display them (can't be used with `--silent`) | Fancy output enabled              |
| `-l`         | `--https`            | Flag for enabling HTTPS                                                                             | HTTP                              |
| `-d`         | `--results-dir`      | Path to results directory                                                                           | Current working directory         |
| `-w`         | `--waiting-period`   | Waiting period in seconds                                                                           | 60 seconds                        |
| `-b`         | `--batch-size`       | Amount of workflows to start without waiting in between                                             | 100 workflows                     |

(\* Options with multiple arguments can be used by specifying the option once, followed by at least one or more
argument(s) separated by spaces (see example below.)

##### Usage example

    fix.py -o producer.opencast.org -c tenant1 tenant2 -u opencast_system_account -p CHANGE_ME -s -d
    /home/me/Desktop/results -w 120 -b 50

##### Use case for _batch size_ and _waiting period_
When this script starts workflows to fix errors, it has to be ensured that it doesn't start hundreds of workflows in a
short period of time since this could overflow the opencast system. For this a _batch size_ and a _waiting period_ can
be defined: After each batch of workflows, the script will wait the defined amount of seconds before starting the next
batch.

### Requirements

- Python 3
- `requests`-Package

##### A few words on compatibility

This script was tested with Opencast 4.x, 5.x and the current state of develop (11/09/2018) and is not guaranteed to
work with earlier or later versions, though it can be assumed that compatibility could be achieved fairly easily by
adapting the files in the `rest_requests` module and adding more/different parsing functionality if necessary.

### Fixes performed by this script

Currently the following errors can be fixed:

* Events missing their series Dublin Core catalog
* Events with a series Dublin Core catalog that does not match the one of the series the event currently belongs to

Both of those errors are fixed by setting/resetting the series Dublin Core catalog of the event with that of the series
by starting a workflow that gets the series Dublin Core catalog from the series service, attaches it to the media
package and creates a new snapshot.

In the future, this script might be extended to cover other errors as well, the focus being on common errors since
only those warrant the effort of scripting a solution instead of simply fixing them manually.

### Execution

The data integrity fixes are executed as follows:

    Parse arguments, check for correctness, initialize settings
    If no digest password: Ask for digest password
    Parse results
    If no chosen tenants: Get all tenants from results
    If excluded-tenants: Filter tenants
    For each tenant:
        For each error:
            For each event belonging to the current tenant affected by this error:
                If batch size reached: Wait for defined period
                If first event or answer == "next": Ask user whether to fix next event/all remaining events with this error
                    If answer == "skip": Skip rest of events with this error
                    Else if answer == "abort": Quit script
                Get media package from asset manager
                Start workflow to fix event
                Log success or failure

##### User control

The user has control over which events are fixed. This gives the user the chance to check the correctness of a fix
before continuing with the remaining events.

The user gets asked "Fix?" preceded by information about the next event that could be fixed and followed by a brief
overview of the valid answers if it's either
* the first event with this error, or
* if the user answered "next" to the last question before.

Valid answers are:

| Answer | Meaning                                                                                                                                                                                           |
|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `n`    | Fix only the _next_ event with this error for the current tenant.                                                                                                                                 |
| `r`    | Fix all _remaining_ events with this errors for the current tenant.                                                                                                                               |
| `s`    | _Skip_ the rest of the events with this error for the current tenant and continue with the next error if there is one, otherwise with the next tenant if there is one, otherwise quit the script. |
| `a`    | _Abort_ the script immediately without fixing any more events.                                                                                                                                    |
| `h`    | Get a more detailed _help_ description of the valid answers than those following the question, similar to those in this documentation.                                                            |


##### Logging
For each day a new log file is created as a csv file with the name "fix_log_" followed by the current date in "Y-m-d"
format. If a log file for the current day already exists, new information is appended at the end. For each event where a
fix is attempted, the following information is written to the log:

| Column       | Description                                                                                                                                                 |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
|timestamp     | The date and time of the attempted fix                                                                                                                      |
|media package | The media package ID                                                                                                                                        |
|tenant        | The tenant ID                                                                                                                                               |
|error         | A description of the error to be fixed, e.g. 'events missing the series Dublin Core catalog' (matching the filename in the results of the check script)     |
|fix           | The fix e.g. '(re)setting series Dublin Core catalog of event from series service' or 'could not be fixed' followed by the reason why if the attempt failed |
