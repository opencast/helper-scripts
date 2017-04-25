#!/bin/bash


LANGUAGE="$(python -c 'print "Test"')"

NAME="$(python -c 'import random; list = open("names.txt", "r"); names = list.readlines(); names = [x.strip() for x in names]; list.close(); print(random.choice(names));')"
TITLE="$(python -c 'import random; list = open("excuses.txt", "r"); excuses = list.readlines(); excuses = [x.strip() for x in excuses]; list.close(); print(random.choice(excuses));')"

echo "${TITLE}"
echo "${NAME}"