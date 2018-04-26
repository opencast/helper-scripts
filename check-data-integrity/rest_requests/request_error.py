class RequestError(Exception):
    '''
    Exception for when a request fails with a status code other than 200.
    Contains two error messages.

    :error: Either simple error message containing only the resource description and status code (for errors to be
    collected) or more specific error message also containing the URL (for more serious errors to be displayed immediately)

    '''

    def __init__(self, error):
        """

        :param error:
        """
        self.error = error

    @classmethod
    def with_statuscode(cls, url, status_code, element_description, catalog_description = None, asset_description = None):
        '''
        Creates a Request Error for a failed request to the given url with the given status code and an error message
        containing the given description for the resource we were trying to get.

        :param url:
        :type url:str
        :param status_code:
        :type status_code: str
        :param element_description:
        :type element_description: str
        :param catalog_description:
        :type catalog_description: str
        :param asset_description:
        :type asset_description: str
        '''

        # specific error
        if catalog_description or asset_description:

            error = "{} where the request for the {} {} failed with status code {}".format(element_description,
                                                                                           catalog_description,
                                                                                           asset_description,
                                                                                           status_code)

        # more general error
        else:
            error = "Request for {} at url {} failed with status code {}.".format(element_description, url, status_code)

        return RequestError(error)

    @classmethod
    def with_error(cls, url, error, element_description, catalog_description = None, asset_description = None):

        '''
        Creates a Request Error for a failed request to the given url with the given error and a given description for
        the resource we were trying to get.

        :param url:
        :type url:str
        :param error
        :type error: str
        :param element_description:
        :type element_description: str
        :param catalog_description:
        :type catalog_description: str
        :param asset_description:
        :type asset_description: str
        '''

        # specific error
        if catalog_description or asset_description:

            error = "{} where the request for {} {} failed with error {}".format(element_description,
                                                                                 catalog_description, asset_description,
                                                                                 error)

        # more general error
        else:
            error = "Request for {} at url {} failed with error {}.".format(element_description, url, error)

        return RequestError(error)