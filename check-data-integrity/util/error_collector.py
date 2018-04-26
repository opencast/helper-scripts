import datetime
import sys
import time
from collections import defaultdict

import os


class ErrorCollector:
    """
    Collects the errors for each tenant and prints them out in the end.
    """

    def __init__(self):
        self.errors = {}
        self.TENANT_ERROR = "Tenant Error"
        self.current_tenant = None

    def tenant(self, tenant):
        """
        Switches error collection to a new tenant.

        :param tenant:
        :type tenant: str
        """

        self.errors[tenant] = defaultdict(list)
        self.current_tenant = tenant

    def collect_errors(self, malformed, id):
        """
        Collects the errors from a malformed object and adds them to those of the current tenant.

        :param malformed:
        :type malformed: Malformed
        :param id:
        :type id: str
        """

        for error in malformed.errors:
            self.errors[self.current_tenant][error].append(id)

    def set_tenant_error(self, error):
        """
        Sets an error for the whole tenant.

        :param error:
        :type error: str
        """

        self.errors[self.current_tenant][self.TENANT_ERROR] = error

    def __print_results_for_tenant(self, tenant):
        """
        Prints the encountered errors for current tenant.
        """

        if not self.errors[tenant].keys():
            print("No malformed data found.")

        elif self.TENANT_ERROR in self.errors[tenant].keys():
            error = self.errors[tenant][self.TENANT_ERROR]
            print("{}".format(error))

        else:

            print("Malformed data found: ", file=sys.stderr)

            for message in self.errors[tenant].keys():
                id_list = sorted(self.errors[tenant].get(message))
                print("\t\t{} {}".format(len(set(id_list)), message), file=sys.stderr)

    def print_results_for_current_tenant(self):
        self.__print_results_for_tenant(self.current_tenant)

    def print_all_results(self):
        """
        Prints the encountered errors for each tenant.
        """

        print("\nComplete results:")
        tenants = sorted(self.errors.keys())

        for tenant in tenants:
            print("Tenant {}: ".format(tenant), end='', flush=True)
            self.__print_results_for_tenant(tenant)
            print()

    def write_to_file(self, dir):
        """
        Writes the encountered into files.

        :param dir: The directory for the results
        :type dir: str
        """

        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H_%M_%S')

        results_dir = os.path.join(dir, 'data_integrity_check_results_{}'.format(timestamp))
        os.makedirs(results_dir)

        tenants = sorted(self.errors.keys())
        for tenant in tenants:

            if self.errors[tenant].keys() and not self.TENANT_ERROR in self.errors[tenant].keys():
                tenant_dir = os.path.join(results_dir, tenant)
                os.makedirs(tenant_dir)

                for message in self.errors[tenant].keys():

                    id_list = sorted(self.errors[tenant].get(message))

                    message = message.replace(" ", "_")
                    message = message.replace("(", "")
                    message = message.replace(")", "")

                    filename = os.path.join(tenant_dir, '{}.txt'.format(message))
                    with open(filename, 'w', newline='') as file:
                        for id in id_list:
                            file.write("{}\n".format(id))