DEFAULT_TENANT = "mh_default_org"


def get_base_url(opencast, https, tenant):
        """
        Build a basic url for requests using the chosen protocol, possibly a tenant, and the admin node URL.
        Default protocol is http. Handing over the default tenant is equivalent to handing over None.

        :param opencast: URL to opencast instance
        :type opencast: str
        :param https: Whether to use https
        :type https: bool
        :param tenant: current tenant or None
        :type tenant: str or None
        :return: url
        :rtype: str
        """

        if https:
            protocol = "https"
        else:
            protocol = "http"

        if not tenant or tenant == DEFAULT_TENANT:
            return "{}://{}".format(protocol, opencast)
        else:
            return "{}://{}.{}".format(protocol, tenant, opencast)
