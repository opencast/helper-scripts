class ProgressPrinter():
    """
    This printer prints the progress of the script out nicely. It can be set on silent.
    """

    def __init__(self, silent):
        """
        :param silent: Whether the printer should print
        :type silent: bool
        """
        self.silent = silent

    def print(self, message, level):
        """
        Prints the given message indented with tabs depending on the level if the printer is not set on silent.

        :param message:
        :type message: str
        :param level:
        :type level: int
        """
        if not self.silent:
            indent = "\t\t"*level
            print("{}{}".format(indent, message))