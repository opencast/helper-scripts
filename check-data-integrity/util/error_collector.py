from collections import defaultdict

class ErrorCollector:
    """
    Collects the errors for each tenant and prints them out in the end.
    """

    def __init__(self):
        self.errors = {}
        self.TENANT_ERROR = "Tenant Error"

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

        print("Results for tenant {}:".format(tenant))

        if not self.errors[tenant].keys():
            print("\t\tNo malformed data found.")

        elif self.TENANT_ERROR in self.errors[tenant].keys():
            error = self.errors[tenant][self.TENANT_ERROR]
            print("\t\tTenant could not be checked: {}".format(error))

        else:

            for message in self.errors[tenant].keys():
                id_list = sorted(self.errors[tenant].get(message))
                print("\t\t{} element(s) encountered the error '{}': {}".format(len(set(id_list)), message,
                                                                                ', '.join(set(id_list))))

        print()

    def print_results_for_current_tenant(self):
        self.__print_results_for_tenant(self.current_tenant)

    def print_all_results(self):
        """
        Prints the encountered errors for each tenant.
        """

        print("Complete results:")
        tenants = sorted(self.errors.keys())

        for tenant in tenants:
            self.__print_results_for_tenant(tenant)