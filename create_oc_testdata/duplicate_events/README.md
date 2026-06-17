# Script for duplicating events on an Opencast system

This script duplicates the specified Events on the Opencast system.

## How to Use

### Configuration

The script can be configured by editing the values in `config.py`:

| Configuration Key         | Description                                  | Default/Example                           |
| :------------------------ | :------------------------------------------- | :---------------------------------------- |
| `target_url`              | The server URL of the target tenant          | http://localhost:8080                     |
| `yaml_file_path`          | The path to the yaml file with the event IDs | ../create_oc_testdata/data/event_ids.yaml |
| `number_of_duplicates`    | The number of duplicates per event           | 2                                         |
| `digest_user`             | The user name of the digest user             | opencast_system_account                   |
| `digest_pw`               | The password of the digest user              | CHANGE_ME                                 |


The configured digest user needs to exist on the specified Opencast system. 

### Usage

The script can be called with the following parameters (all parameters in brackets are optional):

`python main.py [-t TARGET_URL ] [-n NUMBER_OF_DUPLICATES ] [-f YAML_FILE_PATH]`

| Short Option | Long Option | Description                                      |
| :----------: | :---------- | :----------------------------------------------- |
| `-t`         | `--target`  | The target url of the Opencast system            |
| `-n`         | `--number`  | The number of duplicates to be created           |
| `-f`         | `--file`    | The path to the file containing the event IDs    |

#### Usage example

`python main.py -t localhost:8080 -n 2 -f data/event_ids.yaml`

## Requirements

This script was written for Python 3.8.

It uses modules contained in the _lib_ directory.
