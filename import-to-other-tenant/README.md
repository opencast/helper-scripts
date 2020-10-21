# Script for the re-import of recordings to another tenant

This script exports recordings from one tenant and re-imports them into another, starting a workflow on ingest. This is
useful when sharing capture agents between tenants.

Currently this script does not perform deletion, so the recordings will have to be manually removed from
the source tenant. Furthermore, only archived assets are imported, so the events will have to be published (again).

If the series defined for the imported events does not exist on the target tenant, it will be created. However, existing
series will not be updated. It is recommended to use a specific export-import-series so all imported events can be
easily found on the target tenant and then moved to their correct series.

## How to Use

### Configuration
The script is configured by editing the values in `config.py`:

| Configuration Key | Description                               | Default/Example              |
| :---------------- | :---------------------------------------- | :--------------------------- |
| `source_url`      | The server URL of the source tenant       | https://tenant1.opencast.com |
| `target_url`      | The server URL of the target tenant       | https://tenant2.opencast.com |
| `digest_user`     | The user name of the digest user          | opencast_system_account      |
| `digest_pw`       | The password of the digest user           | CHANGE_ME                    |
| `workflow_id`     | The id of the workflow to start on ingest | reimport-workflow            |
| `workflow_config` | The configuration for that workflow       | {"autopublish": "false"}     |


The configured digest user needs to exist on both tenants and have the same password for both of them. This is because
the script ingests the assets via URL, which is faster, but the user needs to be able to access the source tenant from
the target tenant for this to work. Additionally the user currently needs to have ROLE_ADMIN to be able to use
`/assets/{episodeid}`.

For the future, Basic Authentication and the use of an endpoint that doesn't require the Admin role (e.g.
`api/events/{id}`) would be preferable, so you can simply add a frontend user with the necessary rights (ingest,
access to the events/series) and the same password to both tenants.

### Usage

The script can be called with the following parameters (all parameters in brackets are optional):

`main.py [-e EVENT_ID [EVENT_ID ...]] [-s SERIES_ID [SERIES_ID ...]]`

Either event ids (`-e`) or series ids (`-s`) have to be provided, but not both.

| Short Option | Long Option | Description                                                     |
| :----------: | :---------- | :-------------------------------------------------------------- |
| `-e`         | `--events`  | The id(s) of the event(s) to be imported                        |
| `-s`         | `--series`  | The id(s) of the series with events to be imported              |

#### Usage example

`main.py -e fe8cf34d-c6e9-4dc8-adaa-402dcae0532a 7b42129d-f286-4e66-8dc5-ade8fc882ae6`

## Requirements

This scrypt was written for Python 3.8. You can install the necessary packages with

`pip install -r requirements.txt`

Additionally, this script uses modules contained in the _lib_ directory.
