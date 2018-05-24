class RequestError(Exception):
    """
    Exception for when a request fails with a status code other than 200 or an error.
    Contains an error message:

    :error: Either simple error message containing only the resource description and status code (for errors to be
            collected) or more specific error message also containing the URL (for more serious errors to be displayed
            immediately)

    """

    def __init__(self, error):
        """
        Constructor

        :param error: error message
        :type error: str
        """
        self.error = error

    @classmethod
    def with_statuscode(cls, url, status_code, element_description, asset_type_description=None,
                        asset_description=None):
        """
        Create a Request Error for a failed request to the given url with the given status code and an error message
        containing the given descriptions for the resource we were trying to get.

        :param url: The URL the request went to
        :type url:str
        :param status_code: The status code of the response
        :type status_code: str
        :param element_description: The description of the requested element(s) or the element belonging to the
                                    requested asset (required)
        :type element_description: str
        :param asset_type_description: The description of the asset type if an asset was requested (optional)
        :type asset_type_description: str
        :param asset_description: The description of the requested asset if an asset was requested (optional)
        :type asset_description: str
        """

        # specific error
        if asset_type_description or asset_description:

            error = "{} where the request for the {} {} failed with status code {}".format(element_description,
                                                                                           asset_type_description,
                                                                                           asset_description,
                                                                                           status_code)

        # more general error
        else:
            error = "Request for {} at url {} failed with status code {}.".format(element_description, url, status_code)

        return RequestError(error)

    @classmethod
    def with_error(cls, url, error, element_description, asset_type_description=None, asset_description=None):
        """
        Create a Request Error for a failed request to the given url with the given error and the given descriptions for
        the resource we were trying to get.

        :param url: The URL the request went to
        :type url:str
        :param error: The encountered error
        :type error: str
        :param element_description: The description of the requested element(s) or the element belonging to the
                                    requested asset (required)
        :type element_description: str
        :param asset_type_description: The description of the asset type if an asset was requested (optional)
        :type asset_type_description: str
        :param asset_description: The description of the requested asset if an asset was requested (optional)
        :type asset_description: str
        """

        # specific error
        if asset_type_description or asset_description:

            error = "{} where the request for {} {} failed with error {}".format(element_description,
                                                                                 asset_type_description,
                                                                                 asset_description,
                                                                                 error)

        # more general error
        else:
            error = "Request for {} at url {} failed with error {}.".format(element_description, url, error)

        return RequestError(error)
