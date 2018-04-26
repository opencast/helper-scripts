# Script for the recovery of media packages

This script can be used to re-ingest one or more media packages from a backup of the archive.

### Usage

`main.py -o OPENCAST [-s] -u USER [-p PASSWORD] -b BACKUP [-m MEDIA_PACKAGE [MEDIA_PACKAGE ...]] [-t TENANT] [-w WORKFLOW_ID] [-l]`

| Short option    | Long option       | Description                                                  | Default                                                            |
| :-------------: | :---------------- | :----------------------------------------------------------- | :----------------------------------------------------------------- |
| `-o`            | `--opencast`      | URL of the Opencast instance                                 |                                                                    |
| `-s`            | `--https`         | Flag for enabling HTTPS                                      | HTTP                                                               |
| `-u`            | `--user`          | User for digest authentication                               |                                                                    |
| `-p`            | `--password`      | Password for digest authentication                           | Prompt for password after start-up                                 |
| `-b`            | `--backup`        | Path to backup of archive                                    |                                                                    |
| `-t`            | `--tenant`        | A tenant ID                                                  | `mh_default_org`                                                   |
| `-m`            | `--media-packages`| One or more media package IDs to be recovered                | Recover all media packages contained in backup for specified tenant|
| `-w`            | `--workflow-id`   | Workflow to run on the re-ingested mediapackage              | Default workflow configured in opencast                            |
| `-l`            | `--last-version`  | Flag for always choosing the last version of a media package | Ask user for version                                               |

All parameters in braces are optional, the others required.

##### Usage example

    main.py -o develop.opencast.org -s -u opencast_system_account -p CHANGE_ME -b /backups/archive_backup -m 8834ac27-f930-4042-b2e7-4f5c6c4db14a 446576e6-56d2-439e-9b9d-555cc8c910b3 -t mh_default_org -w schedule-and-upload -l

### Requirements

- Python 3
- `requests`-Package

### A few things to consider

- Neither the media package itself nor any of its subelements (tracks, catalogs, attachments) retain their IDs since this poses the risk of conflicts.
- Tags are also not retained for any media package element, so the given workflow will have to retag them upon ingest.
- The Tenant ID is not only used for finding the media packages in the backup but also for re-ingesting them, so it's currently not possible to re-ingest a media package to a different tenant from the one to which it originally belonged.

# The Recovery Process

The recovery of one or more media package(s) from a backup is executed in the following way:

    Parse arguments, check for correctness
    If no digest password: Ask for digest password
    If no tenant: Set default tenant
    If no media package IDs: Get IDs of all media packages for tenant contained in backup
    For each media package ID:
        Find media package folder in backup
        If not found: Print error, skip recovery of this media package
        If last-version-flag set: Pick last version
        Else: Ask user for version to be recovered by presenting all available versions
    Present user with all media packages that can be recovered (id, version, path) and ask for confirmation
    If no confirmation: Abort recovery
    Else:
        For each recoverable media package:
            Create new media package with /ingest/createMediaPackage
            Get all media package elements (tracks, catalogs, attachments) of old media package by parsing manifest
            If manifest can't be parsed: Print error, skip media package
            If media package is missing a type of element or has unexpected elements: Print warning
            Add all tracks to new media package with /ingest/addTrack
            Add all attachments to new media package with /ingest/addAttachment
            Add all catalogs to new media package with /ingest/addCatalog
            Ingest new media package with provided workflow or default workflow
            If successful: Print new ID of media package and started workflow with ID
            Else: Print error
