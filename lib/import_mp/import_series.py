from data_handling.errors import optional_series_error
from data_handling.transform_acl import transform_acl
from input_output.get_dummy_series_dc import get_dummy_series_dc
from input_output.read_file import read_file
from rest_requests.get_response_content import get_xml_content, get_string_content
from rest_requests.request import get_request
from rest_requests.series_requests import create_series


def import_series(series_id, base_url, digest_login, ignore_errors, series_catalogs, series_attachments=None):
    """
    Import a series by recreating it with the series Dublin Core catalog and optionally a series ACL.

    :param series_id: The ID of the series
    :type series_id: str
    :param base_url: The base url for the rest requests.
    :type base_url: str
    :param digest_login: User and password for digest authentication.
    :type digest_login: DigestLogin
    :param ignore_errors: Whether to ignore errors and imported the media package anyway
    :type ignore_errors: bool
    :param series_catalogs: The series catalogs
    :type series_catalogs: list
    :param series_attachments: The series attachments (optional)
    :type series_attachments: list or None
    :raise SeriesError:
    """

    series_dcs = [catalog for catalog in series_catalogs if catalog.flavor == "dublincore/series"]
    series_acls = [attachment for attachment in series_attachments if attachment.flavor == "security/xacml+series"]

    if len(series_dcs) > 1 or len(series_acls) > 1:
        optional_series_error("More than one series Dublin Core catalog or ACL in series {}.".format(series_id),
                              ignore_errors)

    if not series_dcs:
        optional_series_error("Series Dublin Core catalog of series {} missing.".format(series_id), ignore_errors)

    series_dc_contents = []
    series_acl_contents = []

    for series_dc in series_dcs:
        try:
            if series_dc.path:
                series_dc_content = read_file(series_dc.path)
            else:
                series_dc_content = get_string_content(get_request(series_dc.url, digest_login, "")) # TODO error handling

            series_dc_contents.append(series_dc_content)
        except Exception as e:
            optional_series_error("Series Dublin Core catalog of series {} could not be read.".format(series_id),
                                  ignore_errors, e)

    for series_acl in series_acls:
        try:
            if series_acl.path:
                series_acl_content = read_file(series_acl.path)
            else:
                series_acl_content = get_string_content(get_request(series_acl.url, digest_login, "")) # TODO error handling
        except Exception as e:
            optional_series_error("Series ACL of series {} could not be read.".format(series_id), ignore_errors, e)
            continue

        try:
            series_acl_content = transform_acl(series_acl_content)
            series_acl_contents.append(series_acl_content)
        except Exception as e:
            optional_series_error("Series ACL of series {} could not be transformed.".format(series_id), ignore_errors,
                                  e)

    series_dc_content = series_dc_contents[0] if series_dc_contents else get_dummy_series_dc(series_id)
    series_acl_content = series_acl_contents[0] if series_acl_contents else None

    create_series(base_url, digest_login, series_dc_content, series_acl_content)
