# Script to start a workflow for multiple events belonging to different tenants

With this script, you can start workflows for multiple events belonging to different tenants, if the tenant-specific 
Admin URLs follow a pattern. To use this, you need to put the event ids into files named after the tenant they belong 
to, one id per line.
Currently, this script doesn't support workflow parameters. In contrast to start-workflow-from-archive, this script uses
/admin-ng/tasks/new to start the workflow, not workflow/start.

## How to Use

### Configuration

First you need to configure the script in `config.py`:

| Configuration Key | Description                                                 | Default/Example         |
| :---------------- | :---------------------------------------------------------- | :---------------------- |
| `url_pattern`      | The pattern for the tenant-specific URLs to the admin node  | https://{}.opencast.com |
| `digest_user`     | The user name of the digest user                            | opencast_system_account |
| `digest_pw`       | The password of the digest user                             | CHANGE_ME               |

### Usage

The script can be called with the following parameters:

`main.py -w WORKFLOW_DEFINITION -d DIRECTORY`

| Short Option | Long Option   | Description                                       |
| :----------: | :------------ | :------------------------------------------------ |
| `-w`         | `--workflow`  | The workflow to start                             |
| `-d`         | `--directory` | The path to the directory with the event id files |

#### Usage example

`main.py -w republish-metadata -d /home/user/Desktop/events`

## Requirements

This script was written for Python 3.8. You can install the necessary packages with

`pip install -r requirements.txt`

Additionally, this script uses modules contained in the _lib_ directory.