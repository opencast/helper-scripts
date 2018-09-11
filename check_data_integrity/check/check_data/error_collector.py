import datetime
import sys
import time
from collections import defaultdict

import os


class ErrorCollector:
    """
    Collect the errors for each tenant, print them out and save them to files.
    """

    def __init__(self):
        """
        Constructor
        """

        self.errors = {}
        self.TENANT_ERROR = "Tenant Error"
        self.current_tenant = None

    def tenant(self, tenant):
        """
        Start error collection for a new tenant.

        :param tenant: The new tenant to be checked
        :type tenant: str
        """

        self.errors[tenant] = defaultdict(list)
        self.current_tenant = tenant

    def collect_errors(self, malformed, element_id):
        """
        Collect the errors from a malformed object and adds them to those of the current tenant for the given element.

        :param malformed: Malformed data containing the encountered errors
        :type malformed: Malformed
        :param element_id: ID of the element the malformed data belongs to
        :type element_id: str
        """

        for error in malformed.errors:
            self.errors[self.current_tenant][error].append(element_id)

    def set_tenant_error(self, error):
        """
        Set an error for the whole current tenant.

        :param error:
        :type error: str
        """

        self.errors[self.current_tenant][self.TENANT_ERROR] = error

    def __print_results_for_tenant(self, tenant):
        """
        Print the encountered errors for the given tenant.
        :param tenant: The tenant for which results should be printed
        :type tenant: str
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
        """
        Print results for the current tenant.
        """
        self.__print_results_for_tenant(self.current_tenant)

    def print_all_results(self):
        """
        Prints the results for all tenants.
        """

        print("\nComplete results:")
        tenants = sorted(self.errors.keys())

        for tenant in tenants:
            print("Tenant {}: ".format(tenant), end='', flush=True)
            self.__print_results_for_tenant(tenant)
            print()

    def save_results(self, directory):
        """
        Writes the results to files. Creates a result directory containing the current date and time and subdirectories
        for each tenant. Each type of error gets it's own file with the IDs of the affected elements.

        :param directory: The directory for the results
        :type directory: str
        """

        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H_%M_%S')

        results_dir = os.path.join(directory, 'data_integrity_check_results_{}'.format(timestamp))
        os.makedirs(results_dir)

        tenants = sorted(self.errors.keys())
        for tenant in tenants:

            if self.errors[tenant].keys() and self.TENANT_ERROR not in self.errors[tenant].keys():
                tenant_dir = os.path.join(results_dir, tenant)
                os.makedirs(tenant_dir)

                for message in self.errors[tenant].keys():

                    id_list = sorted(self.errors[tenant].get(message))

                    message = message.replace(" ", "_")
                    message = message.replace("(", "")
                    message = message.replace(")", "")

                    filename = os.path.join(tenant_dir, '{}.txt'.format(message))
                    with open(filename, 'w', newline='') as file:
                        for element_id in id_list:
                            file.write("{}\n".format(element_id))
