DEFAULT_TENANT = "mh_default_org"

class URLBuilder:

    def __init__(self, opencast, https):

        self.opencast = opencast

        if https:
            self.protocol = "https"
        else:
            self.protocol = "http"

    def get_base_url(self, tenant):
            """
            Build a basic url for requests using the chosen protocol, possibly a tenant, and the opencast URL.
            Default protocol is http. Handing over the default tenant is equivalent to handing over None.

            :param tenant: current tenant or None
            :type tenant: str or None
            :return: url
            :rtype: str
            """

            if not tenant or tenant == DEFAULT_TENANT:
                return "{}://{}".format(self.protocol, self.opencast)
            else:
                return "{}://{}.{}".format(self.protocol, tenant, self.opencast)