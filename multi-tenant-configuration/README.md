# Multi-tenants User configuration scripts for Opencast

This script simplifies the process of multi-tenant configuration.
It allows to read in configurations of tenants and opencast organizations and checks if these configurations match the ones found on the respective opencast system.

The *configuration* file `opencast-organizations.yml` in the environment folder contains specifications for:  

- Opencast Organizations  
- Switchcast System Accounts  
- Capture Agent Accounts  
- Tenants  
- Users (and their Roles)  

the *configuration* file `scripts/config/group_configuration.json` contains specifications for the Groups: 
- Group name
- Group description
- Tenant (on which this group should exist) 
- Group members

## How to Use

### Configuration

The script is configured by editing the values in `config.py`:

| Configuration Key | Description                               | Default/Example              |
| :---------------- | :---------------------------------------- | :--------------------------- |
| `url`             | The URL of the global admin node ?        | https://tenant1.opencast.com |
| `tenant_url_pattern` | The URL pattern of the target tenants  | https://tenant2.opencast.com |
| `tenant_urls`     | A dictioanry of server URLs of the target tenants       | https://tenant2.opencast.com |
| `digest_user`     | The user name of the digest user          | `opencast_system_account`      |
| `digest_pw`       | The password of the digest user           | `CHANGE_ME`                    |
| `env_path`        | The id of the workflow to start on ingest | reimport-workflow            |

**TODo**: check the below ...

_The configured digest user needs to exist on both tenants and have the same password for both of them. This is because
the script ingests the assets via URL, which is faster, but the user needs to be able to access the source tenant from
the target tenant for this to work. Additionally the user currently needs to have ROLE_ADMIN to be able to use
`/assets/{episodeid}`._

_For the future, Basic Authentication and the use of an endpoint that doesn't require the Admin role (e.g.
`api/events/{id}`) would be preferable, so you can simply add a frontend user with the necessary rights (ingest,
access to the events/series) and the same password to both tenants._

#### group config:
The names in the group config file must be unique per Tenant!

### Usage

The script can be called with the following command (all parameters in brackets are optional):

`python main.py -e ENVIRONMENT [-t TENANT_ID] [-c CHECK] [-v True]`

| Param | Description |
| :---: | :---------- |
| `-e` / `--environment` | The environment where to find the configuration file (either `staging` or `production`) |
| `-t` / `--tenant-id` | The id of the target tenant to be configured |
| `-c` / `--check` | checks to be performed (`users`, `groups`, `cast` or `capture`) (default: `all`) | 
| `-v` / `--verbose` | enables logging to be prompted if set to `True` | 

#### example:

`python main.py -e staging -t tenant1 -c groups -v True`

## Requirements

This script was written for Python 3.8. You can install the necessary packages with

**ToDo check the requirements file**

`pip install -r requirements.txt`

Additionally, this script uses modules contained in the _lib_ directory.
