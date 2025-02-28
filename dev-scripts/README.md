Local Development Helper Scripts
================================

This repository contains a small collection of helper scripts for local development.  These should, in theory, be portable across systems, however your milage may vary.  If you find that they don't work please file issues so we can make these better!  Ensure this directory is in your PATH to make these work right.

mpr
---

Fetches and merges a pull request by pull request id.  Ensures the target branch of the PR matches the checked out version.  Supports multiple repositories, which is useful if you have a personal fork.  For example, many Opencast developers have a github.com/$USERNAME/opencast.git so they can file pull requests.  This script assumes your personal fork is origin, and the upstream fork where the PRs live is added as the (`upstream` remote)[https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes].  If that does not match your configuration then you will need to pass a second argument to override the remote name.

Examples:

mpr 1234 -> Merges pull request 1234 to your local clone
mpr 1234 other -> Merges pull request 1234 from the repository named other


ocbuild
-------

Detects the presence of `mvnw`, along with the JDK listed in the main pom file to use for building.  If `mvnw` is not present, then it will use the default system level `mvn`.  If the first argument is numeric it will override the pom file's JDK.

Examples:
```
ocbuild clean install -> Equivalent to mvn clean install
ocbuild 17 clean install -> Forces the use of JDK 17, otherwise identical to the above
```


ocrebuild
---------

Run this from a specific module's directory.  Uses `ocbuild` to build a module, then `mv -f`'s the built jar to the right place in the built distribution.  Remember to run `bundle:watch $bundlename` in the Karaf console to let it reload things on the fly.  This may break a running install if you reload certain modules, but most usually work.  Worst case, restarting Karaf should resolve the issues (assuming you haven't made any new bugs :D)


ocmk
----

The same as above, but for running from the root of your clone.  Pass this script a comma separated list of either module directories, or module IDs (mixing formats allowed).  This will build the target module(s) dependencies, then the modules themselves.  This does *not* build the things which depend on the target modules.  Helpful when you have made changes and are seeing weird behaviour in a module and want to be sure their dependencies are freshly built.  Uses `ocbuild`.

Examples:

ocmk :opencast-workflow-service-impl,:opencast-search-service-impl
ocmk modules/workflow-service-impl,modules/search-service-impl


ocsetup
-------

Starts Opencast's dependencies (database, opensearch) via the Docker developer containers, configures Opencast's database settings, enables Karaf debugging and webconsole, and ensures the log file is present.


ocstart
-------

Selects the Opencast distribution, detects the JDK version, and then starts Opencast.

Examples:
```
ocstart -> Starts the develop distribution, with whatever its default JDK is
ocstart admin -> Starts the admin distribution, with whatever its default JDK is
ocstart worker 17 -> Starts the worker distribution, with JDK 17
```

ocstop
------

Stops the dependencies running in Docker containers started by `ocsetup`.  Does *not* stop Opencast itself.


oclog
-----

Looks at the live log data for Opencast.  This is probably not useful for develop distributions, but it is for the rest.

Examples:
```
oclog -> Selects the first (via bash glob) Opencast log and launches `tail -f` on it.
oclog admin -> Runs `tail -f` on the admin distribution's log file
```


ocread
------

Similar to `oclog`, but uses `less` instead of `tail.  Useful for quickly getting at the logs for a given distribution.


ocpicbr
-------

Useful for building release builds of the Opencast Admin Interface and deploy them on running Opencast.  This script probably won't work for you without modifications, but assumes you have a `~/opencast` directory with at least one mainline Opencast repo clone.  Run `ocpicbr` from your admin-ui-interface clone, it builds HEAD, and then goes to the Opencast admin ui module and builds that.  Will copy the jar into the currently built Opencast distribution, remember to use `bundle:watch opencast-admin-ui-frontend` to let Karaf reload it on the fly!

Examples:
```
ocpicbr upstream -> Builds admin UI's HEAD, then cd ~/opencast/upstream/modules/admin-ui-interface, changes the url and checksum in the pom, and builds the module
```
