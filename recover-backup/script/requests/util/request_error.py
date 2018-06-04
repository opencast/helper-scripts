class RequestError(Exception):
    """
    Exception for when a request fails with a status code other than 200.
    Contains two error messages.

    :error: Simple error message containing only the resource description and status code for errors to be collected.
    :full message: More specific error message also containing the URL, for more serious errors to be displayed
    immediately.
    """

    def __init__(self, error, full_message):
        """

        :param error:
        :param full_message:
        """
        self.error = error
        self.full_message = full_message

    @classmethod
    def with_status_code(cls, resource_description, url, status_code):
        """
        Creates a Request Error for a failed request to the given url with the given status code and an error message
        containing the given description for the resource we were trying to get.

        :param resource_description:
        :type resource_description: str
        :param url:
        :type url:str
        :param status_code:
        :type status_code: str
        """

        error = "Request for {} failed with status code {}".format(resource_description, status_code)
        full_message = "Request for {} at url {} failed with status code {}.".format(resource_description, url,
                                                                                     status_code)
        return RequestError(error, full_message)

    @classmethod
    def with_error(cls, resource_description, url, error):
        """
        Creates a Request Error for a failed request to the given url with the given error and a given description for
        the resource we were trying to get.

        :param resource_description:
        :type resource_description: str
        :param url:
        :type url:str
        :param error
        :type error: str
        """

        error = "Request for {} failed with error {}".format(resource_description, error)
        full_message = "Request for {} at url {} failed with error {}.".format(resource_description, url, error)
        return RequestError(error, full_message)

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
        :raise: ValueError if this RequestError doesn't have a status code
        """
        if not self.has_status_code():
            raise ValueError("Attribute status_code not found.")
        return self.error.split(" ")[-1]

    def get_error(self):
        """
        Get the error that caused this request error if there is one.

        :return: The error if it exists
        :rtype: str
        :raise: ValueError if this RequestError doesn't have an error
        """
        if not self.has_error():
            raise ValueError("Attribute error not found.")
        return self.error.split(" ")[-1]
