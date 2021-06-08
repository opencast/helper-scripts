# Script to create groups for testing

With this script, you can easily create multiple groups for testing. Can be extended to include specific roles, 
users and so on.

## How to Use

### Configuration

First you need to configure the script in `config.py`:

| Configuration Key | Description                      | Default                 |
| :---------------- | :------------------------------- | :---------------------- |
| `admin_url`       | The (tenant-specific) admin URL  | http://localhost:8080   |
| `digest_user`     | The user name of the digest user | opencast_system_account |
| `digest_pw`       | The password of the digest user  | CHANGE_ME               |


### Usage

The script can be called with the following parameters (all parameters in brackets are optional):

`main.py -a AMOUNT_OF_GROUPS`

| Short Option | Long Option | Description                                                     |
| :----------: | :---------- | :-------------------------------------------------------------- |
| `-a`         | `--amount`  | How many groups to create (default: 100)                        |

#### Usage example

`main.py -a 200`

## Requirements

This script was written for Python 3.8. You can install the necessary packages with

`pip install -r requirements.txt`

Additionally, this script uses modules contained in the _lib_ directory.