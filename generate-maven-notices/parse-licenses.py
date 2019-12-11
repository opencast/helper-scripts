from pathlib import Path
from sys import argv

if len(argv) < 2:
    print("Usage:", "python", argv[0], "<path to dependency.html>")
    exit(1)

if "rest-test-environment" in argv[1] or "hello-world-impl" in argv[1]:
    exit(0)

with Path(argv[1]).open("r") as f:
    line = f.readline()
    classifier = False
    while "</table>" not in line:
        line = f.readline()
        if "<tr" in line:
            line = f.readline()
            gid = line[line.find(">") + 1 : line.rfind("<")]
            if gid == "org.opencastproject":
                continue
            line = f.readline()
            if "<a" in line:
                aid = line[line.find('">') + 2 : line.rfind("</a")]
            else:
                aid = line[line.find(">") + 1 : line.find("</")]
            line = f.readline()
            line = f.readline()
            if "Classifier" in line or classifier:
                classifier = True
                line = f.readline()
            line = f.readline()
            if "<a" in line:
                licenses = []
                for l in line.split("</a>")[:-1]:
                    start = l.find('">') + 2
                    if l[start:]:
                        licenses.append(l[start:])
                lic = "-".join(licenses)
            else:
                lic = line[line.find(">") + 1 : line.find("</")]
            print("  " + "{:<38}".format(gid) + " " + "{:<49}".format(aid) + lic)
