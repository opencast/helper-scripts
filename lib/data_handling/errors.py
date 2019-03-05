class SeriesError(Exception):
    """
    Represents all errors that can hinder the recovery of a series.
    Simply contains an error message and nothing else.
    """
    pass


class MediaPackageError(Exception):
    """
    Represents all errors that can hinder the recovery of a media package.
    Simply contains an error message and nothing else.
    """
    pass


def optional_series_error(error, ignore_errors, exception=None):
    """
    Print a warning if errors should be ignored, otherwise raise a SeriesError

    :param error: The message that should be printed as a warning or raised as an error
    :type error: str
    :param ignore_errors: Whether to raise an error or print a warning
    :type ignore_errors: bool
    :param exception: The exception that caused the error
    :type exception: Exception
    :raise SeriesError:
    """
    if ignore_errors:
        print("Warning: {}".format(error))
    else:
        raise SeriesError(error) from exception


def optional_mp_error(error, ignore_errors, exception=None):
    """
    Print a warning if errors should be ignored, otherwise raise a MediaPackageError

    :param error: The message that should be printed as a warning or raised as an error
    :type error: str
    :param ignore_errors: Whether to raise an error or print a warning
    :type ignore_errors: bool
    :param exception: The exception that caused the error
    :type exception: Exception
    :raise MediaPackageError:
    """
    if ignore_errors:
        print("Warning: {}".format(error))
    else:
        raise MediaPackageError(error) from exception
