# Script for the recovery of media packages

This script can be used to re-ingest one or more media packages from a backup of the archive.

Additionally to the modules in this folder this script uses modules contained in the _lib_ directory.

### Usage

This script can be called with the following parameters (all parameters in brackets are optional, the others required):

`main.py -o OPENCAST [-s] -u USER [-p PASSWORD] [-b BACKUP] [-m MEDIA_PACKAGE [MEDIA_PACKAGE ...]] [-t TENANT]
[-w WORKFLOW_ID] [-l] [-r RSYNC_HISTORY]`

Either a path to the archive backup (`-b`) or a path to the rsync history (`-r`) has to be provided.

| Short option | Long option       | Description                                                  | Default                                                             |
| :----------: | :---------------- | :----------------------------------------------------------- | :------------------------------------------------------------------ |
| `-o`         | `--opencast`      | URL of the Opencast instance without protocol                |                                                                     |
| `-s`         | `--https`         | Flag for enabling HTTPS                                      | HTTP                                                                |
| `-u`         | `--user`          | User for digest authentication                               |                                                                     |
| `-p`         | `--password`      | Password for digest authentication                           | Prompt for password after start-up                                  |
| `-b`         | `--backup`        | Path to backup of archive (raw copy of the archive tree)     |                                                                     |
| `-t`         | `--tenant`        | A tenant ID                                                  | `mh_default_org`                                                    |
| `-m`         | `--media-packages`| One or more media package IDs to be recovered                | Recover all media packages contained in backup for specified tenant |
| `-w`         | `--workflow-id`   | Workflow to run on the re-ingested media package             | Default workflow configured in opencast                             |
| `-l`         | `--last-version`  | Flag for always choosing the last version of a media package | Ask user for version                                                |
| `-r`         | `--rsync-history` | Path to rsync history                                        |                                                                     |

##### Usage example

    main.py -o develop.opencast.org -s -u opencast_system_account -p CHANGE_ME -b /backups/archive_backup -m
    8834ac27-f930-4042-b2e7-4f5c6c4db14a 446576e6-56d2-439e-9b9d-555cc8c910b3 -t mh_default_org -w recover-mp -l

### Requirements

- Python 3
- `requests`-Package

### Recovery from a backup of the archive

The script expects the backup to be a raw copy of the archive folder (not compressed). The following directory
structure is expected: `<backup path>/<tenant id>/<media package id>/<version>`

### Recovery from rsync history

The script can also try to recover a media package from rsync history if a path to that history is provided.
This is useful for media packages that are already deleted in the regular backup. Rsync history will be considered if a
media package cannot be found in the regular backup or if all media packages from a tenant should be recovered. The
following directory structure is expected: `<rsync history path>/<date>/<tenant id>/<media package id>/<version>`
If a media package is contained in more than one date folder, the most recent is chosen.

### A few things to consider

- Neither the media package itself nor any of its sub elements (tracks, catalogs, attachments) retain their IDs since
this poses the risk of conflicts.
- Contrary to that, a recovered series _does_ retain its ID.
- Tags are also not retained for any media package element, so the given workflow will have to re-tag them upon ingest.
- The Tenant ID is not only used for finding the media packages in the backup but also for re-ingesting them, so it's
currently not possible to re-ingest a media package to a different tenant from the one to which it originally belonged.
- If requests to your opencast instance are failing, try disabling or enabling HTTPS via the `-s` flag.

### The Recovery Process

The recovery of one or more media package(s) from a backup of the archive is executed in the following way:

    Parse arguments, check for correctness
    If no digest password: Ask for digest password
    If no tenant: Use default tenant
    If no media package IDs: Get IDs of all media packages for tenant contained in backup and rsync history
    For each media package ID:
        Find media package folder in backup
        If not found: Try rsync history if available
        If still not found: Skip recovery of this media package
        If last-version-flag set: Pick last version
        Else: Ask user to choose version
    Present user with all media packages that can be recovered (id, version, path) and ask for confirmation
    If no confirmation: Abort recovery
    Else:
        For each recoverable media package:
            Create new media package with /ingest/createMediaPackage
            Get all media package elements (tracks, catalogs, attachments) of old media package by parsing manifest
            If manifest can't be parsed: Skip media package
            If series no longer exists: Recover series with series Dublin Core catalog and optional series ACL
            Add all tracks to new media package with /ingest/addTrack
            Add all non-series attachments to new media package with /ingest/addAttachment
            Add all non-series catalogs to new media package with /ingest/addCatalog
            Ingest new media package with provided workflow or default workflow
            If successful: Print new ID of media package and started workflow with ID
            Else: Print error

### The workflow
If no workflow id is specified, the default workflow configured in opencast will be started on the re-ingested
media package. Alternatively, a basic workflow that can be further customized is attached to this script as
`workflow_example.xml`. It executes the following steps:
* Attach series assets like the series catalog and the series ACL to the media package
* Inspect the tracks of the media package
* Tag all media package elements with _archive_
* Archive all media package elements

This workflow does currently _not_ publish the media package.

### Recovery of series
If the episode Dublin Core catalog of a media package references a series that no longer exists, it will be recreated
with the series Dublin Core catalog and optionally the series ACL. This is done by checking the series ID, so if by
chance a new series with the same ID has been created since the backup the media package will be wrongly attached to it
and the old series will not be recovered.

Additionally the series Dublin Core catalog and the series ACL are not re-ingested with the rest of the media package
since this could revert changes to the series that happened after the backup of the media package.