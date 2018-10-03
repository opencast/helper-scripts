Generate Changelog for Opencast
===============================

This script generated a changelog based on merged pull requests. To generate a
changelog for a given version, run the script with the git branch name, start
date and optionally end date as arguments.


Example for 4.x
---------------

```
% python changelog.py r/4.x 2018-03-29                                                                                                                       (git)-[master] [148] 
- [MH-12923 serviceregistry initializes a db connection twice
  ](https://github.com/opencast/opencast/pull/267)
...
```

For version 4.0 you would additionally add the changes listed by

    % python3 changelog.py develop 2017-09-22 2018-04-03


Changelog for x.0 version
-------------------------

Since these versions are developed on both `develop` and their specific release
branched, two requests need to be made and merged:

    % python changelog.py develop <begin-of-development> <x.0-branch-cut-date>
    % python changelog.py r/5.x <begin-of-development>
