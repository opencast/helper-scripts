This script allow you to start a workflow on an archived event.

Install:
```
$ pip3 install -r requirments.txt
```

Usage:
```
$ python3 start-workflow.py  --help
usage: start-workflow.py [-h] -m MEDIAPACKAGE -w WORKFLOW [-W PROPERTIES]
                         [-o OPENCAST] [-u USER] [-p PASSWORD]

optional arguments:
  -h, --help            show this help message and exit
  -m MEDIAPACKAGE, --mediapackage MEDIAPACKAGE
                        media package identifier
  -w WORKFLOW, --workflow WORKFLOW
                        workflow definition identifier
  -W PROPERTIES, --properties PROPERTIES
                        workflow configuration properties (key=value)
  -o OPENCAST, --opencast OPENCAST
                        url of the opencast instance
  -u USER, --user USER  digest user name
  -p PASSWORD, --password PASSWORD
                        digest password
```

Example:
```
python3 start-workflow.py -o https://develop.opencast.org -m XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX -w republish-metadata \
                          -W publishToEngage=false -W publishToOaiPmh=true
```

An additional script is created to start workflows on a list of media packages.

Usage:
```
$ sh start-multiple-workflows.sh --help
usage: start-multiple-workflows.sh -w WORKFLOW [-W PROPERTIES] [-o OPENCAST] [-u USER] [-p PASSWORD] [-h]

required arguments:
  -w WORKFLOW, --workflow WORKFLOW
                        workflow definition identifier
optional arguments:
  -h, --help            show this help message and exit
  -W PROPERTIES, --properties PROPERTIES
                        workflow configuration properties (key=value)
  -o OPENCAST, --opencast OPENCAST
                        url of the opencast instance
  -u USER, --user USER  digest user name
  -p PASSWORD, --password PASSWORD
                        digest password
```

Example:
```
cat mediapackages.txt | sh start-multiple-workflows.sh -o https://develop.opencast.org -w republish-metadata \
                                                       -W publishToEngage=false -W publishToOaiPmh=true
```
