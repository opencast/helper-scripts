# Script for the recovery of mediapackages

This script can be used to re-ingest one or more media packages from a backup of the archive.

### Usage

`main.py -o OPENCAST [-s] -u USER [-p PASSWORD] -b BACKUP [-m MEDIAPACKAGES [MEDIAPACKAGES ...]] [-t TENANT] [-w WORKFLOW_ID] [-l]`

| Short option       | Long option          | Description  | Default |
| :-------------: |:-------------| :-----| :-----------|
| `-o`            | `--opencast` | URL of the opencast instance ||
| `-s`      | `-- https`      |   Flag for enabling https | http|
| `-u` | `--user`      |   User for digest authentication |  |
| `-p` | `--password` | Password for digest authentication | Read password in after start-up |
| `-b` | `--backup` | Path to backup of archive |  |
| `-m` | `--mediapackages` | One or multiple mediapackage IDs to be recovered | Recover all mediapackages contained in backup for specified tenant |
| `-t` | `--tenant` | A tenant ID | mh_default_org |
| `-w`| `--workflow-id` | Workflow to run on the re-ingested mediapackage | Default workflow configured in opencast |
| `-l` | `--last-version` | Flag for always choosing the last version of a mediapackage | Ask user for version

All parameters in braces are optional, the others required.

##### Usage Example:
`main.py` `-o` develop.opencast.org `-s` `-u` opencast_system_account `-p` CHANGE_ME `-b` /backups/archive_backup `-m` 8834ac27-f930-4042-b2e7-4f5c6c4db14a 446576e6-56d2-439e-9b9d-555cc8c910b3 `-t` mh_default_org `-w` schedule-and-upload `-l`

### Requirements
- Python 3
- `requests`-Package

### A few things to consider:
- Neither the mediapackage itself nor all its subelements (tracks, catalogs, attachments) retain their IDs since this poses the risk of conflicts.
- Tags are also not retained for all mediapackage elements, so the workflow on ingest will have to retag them.
- The Tenant ID is not only used for finding the mediapackages in the backup but also for re-ingesting them, so it's currently not possible to re-ingest a mediapackage to another tenant than the one it originally belonged.

# The Recovery Process
The recovery of one or more mediapackage(s) from backup is executed the following way:

    Parse arguments, check for correctness
    If no digest password: Read in digest password
    If no tenant: Set default tenant
    If no mediapackage ids: Get ids of all mediapackages contained in backup for tenant
    For each mediapackage id:
        Find mediapackage folder in backup
        If not found: Print error, skip recovery of this mediapackage
        If last-version-Flag set: Pick last version
        Else: Ask user for version to be recovered by presenting all available versions
    Present user with all mediapackages that can be recovered (id, version, path) and ask for confirmation
    If no confirmation: Abort recovery
    Else:
        For each recoverable mediapackage:
            Create new mediapackage with /ingest/createMediaPackage
            Get all mediapackage elements (tracks, catalogs, attachments) of old mediapackage by parsing manifest
            If manifest can't be parsed: Print error, skip mediapackage
            If mediapackage is missing a type of elements or has unexpected elements: Print warning
            Add all tracks to new mediapackage with /ingest/addTrack
            Add all attachments to new mediapackage with ingest/addAttachment
            Add all catalogs to new mediapackage with ingest/addCatalog
            Ingest new mediapackage with provided workflow or default workflow
            If successful: Print new id of mediapackage and started workflow with id
            Else: Print error