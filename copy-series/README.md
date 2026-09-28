# Script to copy series, including the full set of (extended) metadata and ACL from one Opencast to another

With this script you can easily copy all of the series from one cluster to another.  This is useful when debugging
metadata issues and you want the list of series without needing to manually repopulate.

## How to Use

### Configuration

First you need to configure the script in `copy-series.sh`:

| Configuration Key | Description                                      | Default                             |
| :---------------- | :----------------------------------------------- | :---------------------------------- |
| `FROM_HOST`       | The (tenant-specific) admin node URL to          |                                     |
|                   |  fetch series data from                          | https://develop.opencast.org        |
| `FROM_CREDS`      | The digest username and password for `FROM_HOST` | `opencast_system_account:CHANGE_ME` |
| `TO_HOST`         | The (tenant-specific) admin node URL to          |                                     |
|                   |  apply series data to                            | http://localhost                    |
| `TO_CREDS`        | The digest username and password for `TO_HOST`   | `opencast_system_account:CHANGE_ME` |


### Usage

`bash copy-series.sh`

The script does not have any parameters.  Progress is logged to stdout by the individual subprocesses.

## Requirements

This script requires `bash`, `cat`, `curl`, and `jq`.
