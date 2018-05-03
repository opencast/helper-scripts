import sys


class ProgressPrinter:
    """
    This printer prints the progress of the script out nicely. It can be set on silent.
    """

    def __init__(self, silent, no_fancy_output=False):
        """
        :param silent: Whether the printer should print
        :type silent: bool
        :param no_fancy_output: Whether fancy output including progress bars is disabled
        :type no_fancy_output: bool
        """
        self.silent = silent
        self.no_fancy_output = no_fancy_output
        self.indent = ""
        self.last_message = ""
        self.previous_line_ended = True

    def print_message(self, message, level=0, newline_after=True, newline_before=True):
        """
        Prints the given message indented with tabs depending on the level if the printer is not set on silent.

        :param message:
        :type message: str
        :param level:
        :type level: int
        :param newline_after: Whether the message should be followed by a linebreak
        :type newline_after: bool
        :param newline_before: Whether the message should be printed in a new line
        :type newline_before: bool
        """

        if self.silent:
            return  # don't print anything

        self.indent = "\t\t" * level

        if self.no_fancy_output:

            print("{}{}".format(self.indent, message))  # do not any of that fancy stuff
            return

        if newline_before:

            self.__clear_line()
            self.last_message = message

            if not self.previous_line_ended:
                print("\n")

            if newline_after:
                print("{}{}".format(self.indent, message))
                self.previous_line_ended = True
            else:
                print("{}{}".format(self.indent, message), end='', flush=True)
                self.previous_line_ended = False

        else:
            self.last_message = self.last_message + message

            if newline_after:
                print("{}".format(message))
                self.previous_line_ended = True
            else:
                print("{}".format(message), end='', flush=True)
                self.previous_line_ended = False

    def print_progress(self, count, total):

        if self.silent:
            return

        if self.no_fancy_output:

            if count == (total - 1):
                print("{}{}".format(self.indent, "...finished. \n"))

            elif count == 0:
                print('{}Progress:  0%'.format(self.indent), end='\r', flush=True)

            else:
                percent = int((count / total) * 100)
                print('{}Progress: {:2}%'.format(self.indent, percent), end='\r', flush=True)

        else:

            progress_bar = "|{}|".format(" "*100)

            if count == (total - 1):
                self.__clear_line()
                self.__back_to_previous_line()

                print("{}{}".format(self.indent, self.last_message+"finished.\n"))

            elif count == 0:
                print('{}Progress: {}  0%'.format(self.indent, progress_bar), end='\r', flush=True)

            else:
                percent = int((count / total) * 100)
                progress_bar = progress_bar.replace(" ", "#", int(percent))

                print("{}Progress: {} {:2}%".format(self.indent, progress_bar, percent), end='\r', flush=True)

    @staticmethod
    def __clear_line():
        sys.stdout.write("\033[K")  # clear line

    @staticmethod
    def __back_to_previous_line():
        sys.stdout.write("\033[F")
