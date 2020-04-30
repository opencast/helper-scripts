#!/usr/bin/env python

import json
import glob


def main():
    fileNum = 0
    for file in glob.glob("*.json"):
        fileNum += 1
        prep(file, fileNum)


def prep(wFfile, fileNum):
    with open(wFfile, 'r') as f:
        instance = json.load(f)

    operations = []
    runtime = 0
    for operation in instance.get('workflow', {}).get('operations', {})\
                             .get('operation', []):
        id = operation.get('id')
        state = operation.get('state')
        started = operation.get('started')
        completed = operation.get('completed')
        try:
            duration = (int(completed) - int(started)) / 1000.0
            runtime += duration
        except TypeError:
            duration = 0

        operations.append((id, state, duration))

    with open('workflow' + str(fileNum) + '.dat', 'w') as f:
        for op in operations:
            percent = op[2] * 100.0 / runtime
            seconds = op[2]
            hours = int(seconds / 3600)
            seconds = seconds - hours * 3600
            minutes = int(seconds / 60)
            seconds = seconds - minutes * 60
            if hours:
                time = '%02d:%02d:%02d' % (hours, minutes, seconds)
            else:
                time = '%02d:%02d' % (minutes, seconds)
            f.write('%-20s %-12s %8.03f %8.03f  %-10s\n' %
                    (op[0], op[1], op[2], percent, time))


if __name__ == '__main__':
    main()
