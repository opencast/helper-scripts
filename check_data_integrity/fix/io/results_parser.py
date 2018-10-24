import os

from utility.enum import enum


FixableError = enum(

    EVENTS_MISSING_SERIES_DC="events missing the series Dublin Core catalog",
    EVENTS_NONEQUAL_SERIES_DC="events with a series Dublin Core catalog unequal with that of their series"
)


class ResultsParser:
    """
    Class for parsing the results found by the check script.
    """

    def __init__(self, results_dir):
        """
        Constructor that parses the results into a dictionary with subdictionaries for each tenant containing lists
        with event ids for the different errors. Errors that currently can't be fixed by this script are ignored.
        """

        self.results = {}

        dir_name, tenant_dirs, files = next(os.walk(results_dir))

        for tenant_dir in tenant_dirs:

            self.results[tenant_dir] = {}

            directory, subdirs, files = next(os.walk(os.path.join(results_dir, tenant_dir)))

            for filename in files:

                error = filename[:-4].replace("_", " ")
                self.results[tenant_dir][error] = []

                filepath = os.path.join(results_dir, tenant_dir, filename)

                with open(filepath, 'r', newline='') as file:

                    for line in file:

                        self.results[tenant_dir][error].append(line.rstrip('\n'))

    def get_events_with_error(self, tenant, error):
        """
        Return the ids of events belonging to the given tenant that encountered the given error.

        :param tenant: Tenant the events should belong to
        :type tenant: str
        :param error: Error the events should have encountered
        :type error: FixableError

        :return:
        """

        return [event_id for event_id in self.results[tenant][error]] if error in error in self.results[tenant].keys() \
            else []

    def get_tenants(self):
        """
        Get all tenants for which results were found.

        :return: tenants contained in results
        :rtype: list
        """
        return list(self.results.keys())
