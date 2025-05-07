# occu - Opencast Config Updater

This script helps with updating an Opencast that's managed via Ansible playbook.
It simplifies updating adjusted config files to keep them in line with the upstream config files.

## Requirements

The script expects to be run in the root of your Ansible playbook.
It is also expected that you cloned the Opencast repository and have fetched the tags of all relevant versions (i.e. `git fetch --tags upstream`).
The location of the clone can be specified as `OCCU_OCDIR` (see below).

## Installation

Add the script to your `$PATH` and set required config variables.
For example, adjust and add the following to your `.bashrc` or `.zshrc`:

```sh
# Install occu
export PATH="$PATH:/home/lukas/dev/helper-scripts/config-updater/"
export OCCU_MERGETOOL="meld"        # Tool to use for 3-way merges
export OCCU_OCDIR="~/dev/opencast"  # Path to where you cloned the OC repo
```

## Usage

There are three subcommands.
You would typically use `occu status`, followed by one `occu merge` per file that needs adjustments.
For all commands, you have to pass the base and target version as first two parameters.
The base version is the OC version that your playbook is currently at, the target version is the one you want to update to.

You can run all subcommands without arguments to show a brief usage note.

## `occu status`

This command iterates over all OC config files in your playbooks Opencast role and checks for each, whether the file had any changes between the two specified versions.
(It checks `./roles/opencast` by default, but you can override this path as third parameter.)
Example:

```
$ occu status 16.9 17.3
----- Checking files in 'roles/opencast/{templates,files}/'

Files without upstream changes between 16.9 and 17.3 (no update needed):
 ‣ files/etc/org.opencastproject.caption.converters.WebVttCaptionConverter.cfg
 ‣ files/etc/encoding/opencast.properties
 ‣ files/etc/org.opencastproject.fsresources.StaticResourceServlet.cfg

Files with upstream changes between 16.9 and 17.3 (merge required!):
 ‣ files/etc/org.opencastproject.speechtotext.impl.engine.WhisperCppEngine.cfg
 ‣ files/etc/workflows/partial-publish.xml
 ‣ files/etc/workflows/schedule-and-upload.xml
 ‣ templates/custom.properties.j2

Unclear (manual checking needed!):
 ‣ files/etc/workflows/partial-whispercpp.xml
      → could not find file in repo: etc/workflows/partial-whispercpp.xml
```

The script found 8 config files in total and categorized them into three categories:
- The first section contains config files that were not changed in Opencast between the two versions.
  Hence, they need no adjustment in your Playbook.
- The second section contains files that were changed in Opencast.
  Those need updates, so for each you would call run `occu merge`.
- The third section contains files where `occu` is not sure: you have to judge for yourself if they need updating.

## `occu list`

This simply lists all files in `etc` in the OC repository that changed between the two specified version.
It's basically a simple `git diff` command, in case you need more info than `occu status` provides.

```
occu list 17.1 17.3
Opencast files in 'etc/' that changed between 17.1 and 17.3:
M	etc/org.opencastproject.elasticsearch.index.ElasticsearchIndex.cfg
M	etc/ui-config/mh_default_org/paella7/config.json
```

## `occu merge`

This opens your configured merge tool in 3-way merge mode for a specific config file.
Let's say you update from 17.1 to 17.3, then the following files are passed to the merge tool:
- "base": the community version of the file at version 17.1
- "left": the community version of the file at version 17.3
- "right": your ansible version of the file

The output is specified as your ansible file, so if you save the merge in your tool, that file is overwritten.

```
$ occu merge 17.1 17.3 roles/opencast/templates/custom.properties.j2
```
