import os
import sys

sys.path.append(os.path.join(os.path.abspath('..'), "lib"))

import datetime
import config
import io
from collections import defaultdict, Counter
from rest_requests.request_error import RequestError
from args.digest_login import DigestLogin
from rest_requests.basic_requests import get_tenants
from rest_requests.workflow_requests import get_list_of_workflow_instances
from pathlib import Path


def main():
    """
    Export workflow statistics.
    """

    digest_login = DigestLogin(user=config.digest_user, password=config.digest_pw)
    tenants = get_tenants(config.url, digest_login)

    start_date = datetime.date.fromisoformat(config.start_date)
    end_date = datetime.date.fromisoformat(config.end_date)
    delta = end_date - start_date
    max_week = int(delta.days / 7) - 1

    tenant_dir = "tenant-statistics"
    Path(os.path.join(config.export_dir, tenant_dir)).mkdir(parents=True, exist_ok=True)

    tenant_counts = dict()
    for tenant in tenants:
        if tenant not in config.exclude_tenants:
            tenant_url = config.url_pattern.format(tenant) if config.url_pattern else config.url

            try:
                tenant_count = __count_workflows_for_tenant(tenant_url, digest_login, config.workflow_definitions,
                                                            start_date, end_date)
                __export_tenant_statistics(config.export_dir, tenant_dir, tenant, tenant_count, max_week,
                                           config.week_offset)

                tenant_counts[tenant] = tenant_count
                print("{} done.".format(tenant))
            except RequestError as e:
                print("Workflows for tenant {} could not be counted: {}".format(tenant, str(e)))

    __export_tenant_filenames(config.export_dir, tenant_dir, tenant_counts)
    __export_aggregate_statistics(config.export_dir, max_week, config.week_offset, tenant_counts)
    print("Done!\n")


def __export_tenant_filenames(export_dir, tenant_dir, tenant_counts):
    # sum up total and then sort tenants by it
    tenant_total_counts = {tenant: sum(tenant_count.values()) for tenant, tenant_count in tenant_counts.items()}
    sorted_tenant_total_counts = dict(sorted(tenant_total_counts.items(), key=lambda item: item[1], reverse=True))

    with io.open(os.path.join(export_dir, "filenames.txt"), 'w') as file:
        for tenant in sorted_tenant_total_counts.keys():
            if sorted_tenant_total_counts[tenant] != 0:
                print("{} {}".format(tenant, sorted_tenant_total_counts[tenant]))
                file.write("{}/{}-workflow-statistics.dat\n".format(tenant_dir, tenant))


def __export_aggregate_statistics(export_dir, max_week, week_offset, tenant_counts):
    # sum up numbers from each tenant
    c = Counter()
    for d in tenant_counts.values():
        c.update(d)
    aggregate_count = dict(c)

    with io.open(os.path.join(export_dir, "workflow-statistics.dat"), 'w') as file:
        for week in range(0, max_week):
            file.write("{}   {}\n".format(week + week_offset + 1, aggregate_count[week]))


def __export_tenant_statistics(export_dir, tenant_dir, tenant, tenant_count, max_week, week_offset):
    with io.open(os.path.join(export_dir, tenant_dir, "{}-workflow-statistics.dat".format(tenant)), 'w') as file:
        for week in range(0, max_week):
            file.write("{}   {}\n".format(week + week_offset + 1, tenant_count[week]))


def __count_workflows_for_tenant(tenant_url, digest_login, workflow_definitions, start_date, end_date):
    tenant_count = defaultdict(int)

    for workflow_definition in workflow_definitions:
        page_offset = 0
        limit = 100
        get_workflows = True
        while get_workflows:
            workflow_instances = get_list_of_workflow_instances(tenant_url, digest_login,
                                                                {"state": "SUCCEEDED",
                                                                 "workflowdefinition": workflow_definition,
                                                                 "startPage": str(page_offset),
                                                                 "count": str(limit), "compact": "False"})

            for workflow_instance in workflow_instances:
                operations = workflow_instance["operations"]["operation"]

                if operations:
                    timestamp = operations[0]["started"]  # start of first operation
                    workflow_start_date = datetime.date.fromtimestamp(timestamp/1000)  # milliseconds to seconds

                    if start_date <= workflow_start_date <= end_date:
                        delta = workflow_start_date - start_date
                        week = int(delta.days / 7)
                        tenant_count[week] += 1
            get_workflows = len(workflow_instances) == limit
            page_offset += 1
            print("        {} workflow instances counted.".format(page_offset * limit + len(workflow_instances)))
        print("    {} done.".format(workflow_definition))
    return tenant_count


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborting process.")
        sys.exit(0)
