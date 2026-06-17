Generate Changelog for Opencast
===============================

These scripts generate a changelog based on the merged pull requests. The entries are sorted by merge date (descending).
For stable releases, changes merged into the legacy version are also included, but marked with an *.

**Example Result:**

```
- [[#4945](https://github.com/opencast/opencast/pull/4945)] -
  Drop orphan statistics database index
```

Changelog for N.0 version
-------------------------

Generate a list of changes since the `N-1.0` release with 

    python changelog_major.py N <N-1.x branch cut date> <N.x branch cut date> <date of N-1.0 release> 
    [<date of N.0 release>]

This includes changes to `develop` between the branch cuts for `N-1` and `N` as well as the changes to `r/N.x` since
the branch cut for `N`. Changes to the legacy version since the release of `N-1.0` are included with an *.

The date of the last release can easily be checked on GitHub. The dates of the branch cuts _should_ be listed in the
relevant release schedule in the documentation as part of the release notes. If they're not (or they're incorrect), you
can find out the branch cut date by finding the earliest commit belonging to both branches like this:

    git log --pretty=%as -n1 $(diff -u <(git rev-list --first-parent r/N.x) <(git rev-list --first-parent develop) | sed -ne 's/^ //p' | head -1)

Please check afterwards if pull requests merged right on one of the edge of one of the passed dates should be included
in the changelog.

Example for 17.0:

    python changelog_major.py 17 2024-05-06 2024-11-06 2024-06-12

Changelog for N.x version
-------------------------

Generate a list of the changes since the last N.x-1 release with

    python changelog_minor.py N <include-legacy> <date of N.x-1 release> [<date of N.x release>]

Set `include-legacy` to `True` for releases for the stable version, this will then automatically include changes to the
legacy version during the same time-frame.

The date of the last release can easily be checked on GitHub. Please note that PRs merged directly on the day of the
last release might already be contained in that changelog, so check for duplicates.

Example for 17.2:

    python changelog_minor.py 17 True 2025-01-23

A note about GitHub's rate limiting
-----------------------------------

If you run into GitHub's API limit and encounter an error like this:

    [[#3903](https://github.com/opencast/opencast/pull/3903)] -
      Common persistence util classes that also implement transaction retries
    Traceback (most recent call last):
      File "opencast-helper-scripts/release-management/create-changelog/changelog.py", line 62, in <module>
        main(branch, start_date, end_date, pat)
      File "opencast-helper-scripts/release-management/create-changelog/changelog.py", line 34, in main
        merged = pr.get('merged_at')
             ^^^^^^
    AttributeError: 'str' object has no attribute 'get'

you  raise the limit by creating a [Personal Access Token](https://github.com/settings/tokens) with
read-only access to the upstream repo and passing that as the *last* parameter (which means in that case you _need_ to
pass all prior arguments as well).