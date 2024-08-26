# Opencast Data Migration Scripts

This scripts should help to deal with Opencast endpoints and data structures like mediapackage in first place.
It was initially used by data migration scripts but also to verify existence of publication.

## Migration scripts
The idea behind the migration scripts is to download all published and archived data from source Opencast
and reproduce the state on a target Opencast without transcoding media files again. The goals are

- keep series and mediapackage IDs
- reproduce last state/snapshot of series and mediapackage on target system
  - will migrate
    - themes
    - capture agents
    - series
    - mediapackages
      - scheduled events
      - last archived version/snapshot only
      - engage publication
      - external api publication may be created with data from engage publication
  - but will not migrate
    - users
    - streaming formats (HLS, DASH,...)
    - older snapshots of mediapackage
    - mediapakages with state other than finished or scheduled
- keep load at minimum
  - do not transcode media if possible
- save storage where ever possible
  - make use of hard linking
  - share media between engage and external api publication
- robustness
  - scripts will skip series or mediapackage migration if already exists on target system
    - allow script restart
  - skip broken mediapackages and print error message
    - keep going
- handling of dedicated distribution server
- handling of signed URLs (to be improved)
- filter data to migrate
  - by series
  - creation date
  - etc.


# Disclaimer
Please review the scripts before using! No warranty at all.

# How to get started
First review the code before using!

## Requirements
- Python 3.8+
- Python virtual environment (recommended)

## Installation

```shell
# Create python virtual environment (need only to be done once)
python3 -m venv venv
# Enable python virtual environment
source venv/bin/actiavte
# Update python package manager pip (need only to be done once)
pip install --upgrade pip
# Install dependencies (need only to be done once)
pip install -r requirements.txt
# Run script
python migrate_opencast_data.py
```

# Author
elan e.V.

# License
[BSD 2-Clause](LICENSE)
