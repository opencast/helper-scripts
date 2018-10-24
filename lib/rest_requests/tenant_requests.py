from rest_requests.basic_requests import get_tenants


def filter_tenants(chosen_tenants, excluded_tenants, progress_printer, url_builder, digest_login):
    """
    Filter tenants by either choosing or excluding them (both at the same time isn't possible).

    :param chosen_tenants: The chosen tenants
    :type chosen_tenants: list or None
    :param excluded_tenants: The excluded tenants
    :type excluded_tenants: list or None
    :param progress_printer: The progress printer
    :type progress_printer: ProgressPrinter
    :param url_builder: The URL builder
    :type url_builder: URLBuilder
    :param digest_login: The login delete_artefacts for digest authentication
    :type digest_login: DigestLogin
    :return: A sorted list with tenants to check
    :rtype: list
    """

    if chosen_tenants:
        tenants = chosen_tenants
    else:
        # request tenants
        progress_printer.print_message("Requesting tenants... ", 0, False, True)
        tenants = get_tenants(url_builder.get_base_url(None), digest_login)
        progress_printer.print_message("{} tenant(s) received.\n".format(len(tenants)), 0, True, False)

    if excluded_tenants:
        progress_printer.print_message("Filtering tenants... ", 0, False, True)
        tenants = [tenant for tenant in tenants if tenant not in excluded_tenants]
        progress_printer.print_message("{} tenant(s) remain.\n".format(len(tenants)), 0, True, False)

    tenants.sort()
    return tenants
