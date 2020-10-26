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
        super(RequestError, self).__init__(error)
        self.error = error

    @classmethod
    def with_status_code(cls, url, status_code, element_description, asset_type_description=None,
                         asset_description=None):
        """
        Create a Request Error for a failed request to the given url with the given status code and an error message
        containing the given descriptions for the resource we were trying to get.

        :param url: The URL the request went to
        :type url:str
        :param status_code: The status code of the response
        :type status_code: str
        :param element_description: The description of the requested element(s) or the element belonging to the
                                    requested asset
        :type element_description: str
        :param asset_type_description: The description of the asset type if an asset was requested
        :type asset_type_description: str
        :param asset_description: The description of the requested asset if an asset was requested
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
                                    requested asset
        :type element_description: str
        :param asset_type_description: The description of the asset type if an asset was requested
        :type asset_type_description: str
        :param asset_description: The description of the requested asset if an asset was requested
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

    def has_status_code(self):
        """
        Whether the error message contains a status code (as opposed to an error).
        :return: True if the error message contains a status code, False otherwise
        :rtype: bool
        """
        return "status code" in self.error

    def has_error(self):
        """
        Whether the error message contains an error that occurred (as opposed to a status code).
        :return: True if the error message contains an error, False otherwise
        :rtype: bool
        """
        return "error" in self.error

    def get_status_code(self):
        """
        Get the status code that caused this RequestError if there is one.
        :return: The status code if it exists
        :rtype: str
        :raise ValueError: If this RequestError doesn't have a status code
        """
        if not self.has_status_code():
            raise ValueError("Attribute status_code not found.")
        return self.error.split(" ")[-1].split(".")[0]

    def get_error(self):
        """
        Get the error that caused this request error if there is one.
        :return: The error if it exists
        :rtype: str
        :raise ValueError: If this RequestError doesn't have an error
        """
        if not self.has_error():
            raise ValueError("Attribute error not found.")
        return self.error.split(" ")[-1].split(".")[0]
