#!/usr/bin/env python

import json


def main():
    with open('workflow.json', 'r') as f:
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

    with open('workflow.dat', 'w') as f:
        for op in operations:
            percent = op[2] * 100.0 / runtime
            f.write('%-20s %-12s %8.03f %8.03f\n' %
                    (op[0], op[1], op[2], percent))


if __name__ == '__main__':
    main()
