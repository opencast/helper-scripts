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

| Configuration Key     | Description                                   | Default/Example              |
| :-------------------- | :-------------------------------------------- | :--------------------------- |
| `server_url`            | The URL of the global admin node              | `"http://localhost:8080"`    |
| `tenant_url_pattern`  | The URL pattern of the target tenants         | `"http://{}:8080"`           |
| `tenant_urls`         | Optional dictionary of server URLs per tenant | `{'tenant1': 'http://tenant1:8080', 'tenant2': 'http://tenant2:8080'}` |
| `digest_user`         | The user name of the digest user              | `opencast_system_account`    |
| `digest_pw`           | The password of the digest user               | `CHANGE_ME`                  |
| `env_path`            | The path to the environment configuration file| `"environment/{}/opencast-organizations.yml"` |
| `group_path`          | The path to the group configuration file      | `"configurations/group_configuration.yaml"` |

The configured digest user needs to exist on all tenants and has to have the same password. 

The optional dictionary `tenant_urls` can be used if the tenant-id is not an exact part of the tenant URL or the URLs don't follow a common pattern. 

#### group config:
The group names in the group config file must be unique per Tenant!

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
