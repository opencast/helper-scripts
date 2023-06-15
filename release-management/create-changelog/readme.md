Generate Changelog for Opencast
===============================

This script generated a changelog based on merged pull requests. To generate a
changelog for a given version, run the script with the git branch name, start
date and optionally end date as arguments.

Example for 14.x
---------------

```
- [[#4945](https://github.com/opencast/opencast/pull/4945)] -
  Drop orphan statistics database index
```

Changelog for N.x version
-------------------------

    python changelog.py r/N.x <N.x-branch-cut-date>

Changelog for N.0 version
-------------------------

Since these versions are developed on both `develop` and their specific release
branched, two requests need to be made and merged:

    python changelog.py develop <begin-of-development> <N.x-branch-cut-date>
    python changelog.py r/N.x <N.x-branch-cut-date>

Note that the Github API may generate duplicate entries between the two lists depending on dates and timezones.

Dates
-----
Computing the dates can be annoying.  You need to find the earliest commit belonging to various combinations of branches.

    git log --pretty=%as -n1 $(diff -u <(git rev-list --first-parent r/N.x) <(git rev-list --first-parent develop) | sed -ne 's/^ //p' | head -1)

As an example, to generate the full list for Opencast 14 you need to know

 - The changelog for `develop` between the `r/13.x` branching off, and `r/14.x` being started
 - The changelog for `r/14.x` up to `14.0`

To find the first begin-of-development date

    git log --pretty=%as -n1 $(diff -u <(git rev-list --first-parent r/13.x) <(git rev-list --first-parent develop) | sed -ne 's/^ //p' | head -1)

To find the 14.x branch date

    git log --pretty=%as -n1 $(diff -u <(git rev-list --first-parent r/14.x) <(git rev-list --first-parent develop) | sed -ne 's/^ //p' | head -1)

So the final changelog calls would be

    % python changelog.py develop 2022-11-16 2023-05-15
    % python changelog.py r/14.x 2023-05-15

API Limits
----------

Github enforces API limits, which this script can easily hit - especially if you run it multiple times when debugging!
To raise this limit, you may need to create a Personal Access Token with appropriate permissions (read only to the
upstream repo), and pass that as the *fifth* parameter.
