# Script for populating an Opencast system with test data

This script creates random samples of Events (and Series) on the specified Opencast system.

## How to Use

### Configuration

The script is configured by editing the values in `config.py`:

| Configuration Key  | Description                                 | Default/Example                           |
| :----------------- | :------------------------------------------ | :---------------------------------------- |
| `target_url`       | The server URL of the target tenant         | http://localhost:8080                     |
| `test_video_path`  | The path to a test video to be used         | ../create_oc_testdata/data/test_video.mkv |
| `yaml_file_path`   | The path to the file to store the ecent IDs | ../create_oc_testdata/data/event_ids.yaml |
| `number_of_events` | The number of Events to be created          | 4                                         |
| `number_of_series` | The number of Series to be created          | 2                                         |
| `digest_user`      | The user name of the digest user            | opencast_system_account                   |
| `digest_pw`        | The password of the digest user             | CHANGE_ME                                 |


The configured digest user needs to exist on the specified Opencast system. 

### Usage

The script can be called with the following parameters (all parameters in brackets are optional):

`python main.py [-t TARGET_URL ] [-n NUMBER_OF_EVENTS ] [-f TEST_VIDEO_PATH]`

| Short Option | Long Option | Description                                |
| :----------: | :---------- | :----------------------------------------- |
| `-t`         | `--target`  | The target url of the Opencast system      |
| `-n`         | `--number`  | The number of Events to be created         |
| `-f`         | `--file`    | The path to a test video                   |

#### Usage example

`python main.py -t localhost:8080 -n 10 -f home/test/video.mp3`

## Requirements

This script was written for Python 3.8.

It uses modules contained in the _lib_ directory.
