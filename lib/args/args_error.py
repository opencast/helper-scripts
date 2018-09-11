def args_error(parser, error=None):
    """
    Print usage of script and an error message in case there is one, and quit the script.

    :param parser: The arguments parser
    :type parser: argparse.ArgumentParser
    :param error: Optional error message
    :type error: str
    """

    if error:
        print(error)

    parser.print_usage()
    parser.exit()
