# Script to export videos

With this script, you can export archived or published video tracks from Opencast.

## How to Use

### Configuration

First you need to configure the script in `config.py`:

| Configuration Key     | Description                                                                 | Example                                  |
| :-------------------- | :-------------------------------------------------------------------------- | :--------------------------------------- |
| `admin_url`           | The (tenant-specific) admin URL                                             | https://tenant.admin.opencast.com        |
| `presentation_url`    | The (tenant-specific) presentation URL\*                                    | https://tenant.presentation.opencast.com |
| `digest_user`         | The user name of the digest user                                            | opencast_system_account                  |
| `digest_pw`           | The password of the digest user                                             | CHANGE_ME                                |
| `stream_security`     | Whether to sign the URLs before downloading                                 | False                                    |
| `export_archived`     | Whether to export archived tracks                                           | True                                     |
| `export_search`       | Whether to export tracks from the search service\*                          | True                                     |
| `export_publications` | The publication channel(s) for which published tracks should be exported\*  | \["engage-player"\]                      |
| `export_mimetypes`    | The type(s) of video to export (empty: videos of all types)                 | \["video/mp4"]\                          |
| `export_flavors`      | The flavor(s) of videos to export (empty: videos of all flavors)            | \["delivery/*"\]                         |
| `export_catalogs`     | The flavor(s) of catalogs to export (empty: no catalogs)                    | \["smil/cutting", "dublincore/*"\]       |
| `target_directory`    | The path to the directory for the exported videos                           | /home/user/Desktop/videos                |
| `create_series_dirs`  | Whether to create a directory for each series when using the `-s`option     | False                                    |
| `original_filenames`  | Whether to keep the original filenames (otherwise track id is used)         | False                                    |

&ast; Use the search option to export tracks used by the Engage Player, since the engage-player publication doesn't
actually contain the tracks. For this to work you need to configure the presentation url if you have a separate
presentation node.

### Usage

The script can be called with the following parameters (all parameters in brackets are optional):

`main.py [-e EVENT_ID [EVENT_ID ...]] [-s SERIES_ID [SERIES_ID ...]]`

Either event ids (`-e`) or series ids (`-s`) have to be provided, but not both.

| Short Option | Long Option | Description                                                     |
| :----------: | :---------- | :-------------------------------------------------------------- |
| `-e`         | `--events`  | The id(s) of the event(s) to be exported                        |
| `-s`         | `--series`  | The id(s) of the series with events to be exported              |

#### Usage example

`main.py -e fe8cf34d-c6e9-4dc8-adaa-402dcae0532a 7b42129d-f286-4e66-8dc5-ade8fc882ae6`

## Requirements

This script was written for Python 3.8. You can install the necessary packages with

`pip install -r requirements.txt`

Additionally, this script uses modules contained in the _lib_ directory.