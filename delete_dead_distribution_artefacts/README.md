# Script for the deletion of old distribution artefacts

Currently distribution artefacts in the _streams_ or _downloads_ folder can be left over if the corresponding 
media package is deleted. This script can be used to clean up these dead distribution artefacts.

Additionally to the modules in this folder this script uses modules contained in the _lib_ directory.

### Usage

This script can be called with the following parameters (all parameters in brackets are optional, the others required):

`main.py -o OPENCAST -d DISTRIBUTION_DIRS [DISTRIBUTION_DIRS ...] [-t CHOSEN_TENANTS [CHOSEN_TENANTS ...]]
[-e EXCLUDED_TENANTS [EXCLUDED_TENANTS ...]] [-c CHANNELS [CHANNELS ...]] -u USER [-p PASSWORD] [-s] [-l] [-n]`

| Short option | Long option           | Description                                                                                              | Default                            |
| :----------: | :-------------------- | :------------------------------------------------------------------------------------------------------- | :--------------------------------- |
| `-o`         | `--opencast`          | URL of the Opencast instance without protocol                                                            |                                    |
| `-d`         | `--distribution-dirs` | List* of paths to the directories containing distribution artefacts                                      |                                    |
| `-t`         | `--chosen-tenants`    | List* of tenants to be checked (can't be used with `--excluded-tenants`)                                 | All tenants are chosen             |
| `-e`         | `--excluded-tenants`  | List* of tenants to be excluded (can't be used with `--tenants`)                                         | No tenants are excluded            |
| `-c`         | `--channels`          | List* of channels to search for distribution artefacts                                                   | All channels are searched          |
| `-u`         | `--user`              | User for digest authentication                                                                           |                                    |
| `-p`         | `--password`          | Password for digest authentication                                                                       | Prompt for password after start-up |
| `-s`         | `--silent`            | Flag for disabling progress output (can't be used with `--no-fancy-output`)                              | Progress output enabled            |
| `-l`         | `--https`             | Flag for enabling HTTPS                                                                                  | HTTP                               |
| `-n`         | `--no-fancy-output`   | Flag for disabling progress bars in case the terminal can't display them (can't be used with `--silent`) | Fancy output enabled               |

(\* Options with multiple arguments can be used by specifying the option once, followed by at least one or more
argument(s) separated by spaces (see example below.)

##### Usage example

    main.py -o develop.opencast.org -u opencast_system_account -p CHANGE_ME -d /data/opencast/downloads
    /data/opencast/streams -m 8834ac27-f930-4042-b2e7-4f5c6c4db14a 446576e6-56d2-439e-9b9d-555cc8c910b3
    -t tenant1 tenant2 -c internal -s -l

### Requirements

- Python 3
- `requests`-Package

### The Deletion Process

The deletion of dead distribution artefacts is executed in the following way:

    Parse arguments and check them for correctness
    If no digest password: Ask for digest password
    If no chosen tenants: Get all tenants
    If excluded-tenants: Filter tenants
    For each tenant:
          For each distribution path:
              For each specified channel or all channels if unspecified:
                  Find distribution artefacts
    If any distribution artefacts found:
        For all distribution artefacts sorted by media package:
            Check if associated media package still exists by requesting /assets/episode/<id>
            If it no longer exists:
                Add distribution artefacts belonging to this media package to dead distribution artefacts       
        If any dead distribution artefacts found:
            Present them to the user and ask for confirmation
            If confirmation:
                For each distribution artefact:
                    Delete from disk
                    Write to log

##### Logging
For each day a new log file is created as a csv file with the name "deleted_distribution_artefacts_log_" followed by the current date in "Y-m-d"
format. If a log file for the current day already exists, new information is appended at the end. For each deleted distribution artefact, the following information is written to the log:

| Column               | Description                                                                                                                                                |
|----------------------|-----------------------------------------------|
|timestamp             | The date and time of the deletion             |
|tenant                | The tenant ID                                 |
|media package         | The media package ID                          |                                                                                                                                           |
|distribution artefact | The path to the deleted distribution artefact |