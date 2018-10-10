DEFAULT_TENANT = "mh_default_org"


class URLBuilder:

    def __init__(self, opencast_url, https):
        """
        Constructor

        :param opencast_url: URL to an opencast instance
        :type opencast_url: str
        :param https: Whether to use https
        :type https: bool
        """

        self.opencast = opencast_url

        if https:
            self.protocol = "https"
        else:
            self.protocol = "http"

    def get_base_url(self, tenant=None):
        """
        Build a basic url for requests using the chosen protocol, possibly a tenant, and the opencast URL.
        Default protocol is http. Handing over the default tenant is equivalent to handing over None.

        :param tenant: Tenant ID or None
        :type tenant: str or None
        :return: Base url for requests
        :rtype: str
        """

        if not tenant or tenant == DEFAULT_TENANT:
            return "{}://{}".format(self.protocol, self.opencast)
        else:
            return "{}://{}.{}".format(self.protocol, tenant, self.opencast)
