# Script for populating an Opencast system with test data

This script creates random samples of Events (and Series) on the specified Opencast system.

## How to Use

### Configuration

The script is configured by editing the values in `config.py`:

| Configuration Key | Description                               | Default/Example              |
| :---------------- | :---------------------------------------- | :--------------------------- |
| `target_url`      | The server URL of the target tenant       | https://tenant2.opencast.com |
| `digest_user`     | The user name of the digest user          | opencast_system_account      |
| `digest_pw`       | The password of the digest user           | CHANGE_ME                    |
| `workflow_id`     | The id of the workflow to start on ingest | reimport-workflow            |
| `workflow_config` | The configuration for that workflow       | {"autopublish": "false"}     |


The configured digest user needs to exist on the specified Opencast system. 

### Usage

The script can be called with the following parameters (all parameters in brackets are optional):

`main.py [-t TARGET_URL ] [-n NUMBER_OF_EVENTS ]`

| Short Option | Long Option | Description                                |
| :----------: | :---------- | :----------------------------------------- |
| `-t`         | `--target`  | The target url of the Opencast system      |
| `-n`         | `--number`  | The number of Events to be created         |
| `-f`         | `--file`    | The path to a test video                   |

#### Usage example

`main.py -t localhost:8080 -n 10 -f home/test/video.mp3`

## Requirements

This script was written for Python 3.8.

It uses modules contained in the _lib_ directory.
