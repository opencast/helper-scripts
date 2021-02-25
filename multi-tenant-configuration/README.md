# Multi-tenants User configuration scripts for Opencast
**ToDo**

This script ... 

Currently this script does not ... 

## How to Use

### Configuration
**ToDo**

The script is configured by editing the values in `config.py`:

| Configuration Key | Description                               | Default/Example              |
| :---------------- | :---------------------------------------- | :--------------------------- |
| `url`             | The URL of the global admin node ?        | https://tenant1.opencast.com |
| `tenant_url_pattern` | The URL pattern of the target tenants  | https://tenant2.opencast.com |
| `tenant_urls`     | A dictioanry of server URLs of the target tenants       | https://tenant2.opencast.com |
| `digest_user`     | The user name of the digest user          | opencast_system_account      |
| `digest_pw`       | The password of the digest user           | CHANGE_ME                    |
| `env_path`        | The id of the workflow to start on ingest | reimport-workflow            |

**TODo**: check the below ...

_The configured digest user needs to exist on both tenants and have the same password for both of them. This is because
the script ingests the assets via URL, which is faster, but the user needs to be able to access the source tenant from
the target tenant for this to work. Additionally the user currently needs to have ROLE_ADMIN to be able to use
`/assets/{episodeid}`._

_For the future, Basic Authentication and the use of an endpoint that doesn't require the Admin role (e.g.
`api/events/{id}`) would be preferable, so you can simply add a frontend user with the necessary rights (ingest,
access to the events/series) and the same password to both tenants._

### Usage
**ToDo**

The script can be called with the following parameters (all parameters in brackets are optional):

`main.py ... `

| Short Option | Long Option | Description                                                     |
| :----------: | :---------- | :-------------------------------------------------------------- |
| `-t`         | `--tenant`  | The id(s) of the tenant to be configured                        |
| `-e`         | `--environment` | The environment where to find the configuration file (either `staging` or `production`) |
| ... | ... | ... | 

#### Usage example
**ToDo**

`main.py ... `

## Requirements
**ToDo**

This scrypt was written for Python 3.8. You can install the necessary packages with

`pip install -r requirements.txt`

Additionally, this script uses modules contained in the _lib_ directory.
