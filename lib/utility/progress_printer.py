import datetime
import sys
import time


class ProgressPrinter:
    """
    This printer prints the progress of a script out nicely. It can be set to silent.
    """

    def __init__(self, silent, no_fancy_output=False):
        """
        Constructor

        :param silent: Whether the printer should print anything
        :type silent: bool
        :param no_fancy_output: Whether fancy output including progress bars is disabled (default: False)
        :type no_fancy_output: bool
        """
        self.silent = silent
        self.no_fancy_output = no_fancy_output
        self.indent = ""
        self.last_message = ""
        self.previous_line_ended = True

    def print_empty_line(self):
        """
        Print an empty line if printer isn't silent.
        """
        if not self.silent:
            print()

    def print_message(self, message, level=0, newline_after=True, newline_before=True):
        """
        Print the given message indented with tabs depending on the level if the printer is not set on silent.
        This can also be used to print multiple times to the same line.

        :param message: The message
        :type message: str
        :param level: The level to indent the message to
        :type level: int
        :param newline_after: Whether the message should be followed by a linebreak (default: True)
        :type newline_after: bool
        :param newline_before: Whether the message should be printed in a new line (default: True)
        :type newline_before: bool
        """

        if self.silent:
            return  # don't print anything

        self.indent = ProgressPrinter.get_indent(level)  # get indentation

        if self.no_fancy_output:

            print("{}{}".format(self.indent, message))  # simply print the indented message
            return

        if newline_before:

            self.clear_line()
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
        """
        Print a progress bar and the progress in percent if printer isn't silent.

        :param count: Amount of elements that have already been processed.
        :type count: int
        :param total: Total amount of elements to be processed.
        :type total: int
        """

        if self.silent:
            return

        if self.no_fancy_output:  # keep it simple, no progress bars

            if count == (total - 1):
                print("{}{}".format(self.indent, "...finished. \n"))

            elif count == 0:
                print('{}Progress:  0%'.format(self.indent), end='\r', flush=True)

            else:
                percent = int((count / total) * 100)
                print('{}Progress: {:2}%'.format(self.indent, percent), end='\r', flush=True)

        else:  # do fancy stuff with progress bars

            progress_bar = "|{}|".format(" "*100)

            if count == (total - 1):
                self.clear_line()
                self.back_to_previous_line()

                print("{}{}".format(self.indent, self.last_message+"finished.\n"))

            elif count == 0:
                print('{}Progress: {}  0%'.format(self.indent, progress_bar), end='\r', flush=True)

            else:
                percent = int((count / total) * 100)
                progress_bar = progress_bar.replace(" ", "#", int(percent))

                print("{}Progress: {} {:2}%".format(self.indent, progress_bar, percent), end='\r', flush=True)

########################################################################################################################
    def print_progress_message(self, message, level=0):

        if self.silent:
            return

        self.indent = ProgressPrinter.get_indent(level)

        print('{}{}'.format(self.indent, message), end='\r', flush=True)

    def begin_progress_message(self, message, level=0):

        if self.silent:
            return

        self.print_message(message, level)

    def end_progress_message(self, message, level=0):

        if self.silent:
            return

        self.clear_line()
        self.back_to_previous_line()

        self.indent = ProgressPrinter.get_indent(level)

        print("{}{}{}".format(self.indent, self.last_message, message))
########################################################################################################################

    def print_time(self, waiting_period, message):
        """
        Print the remaining waiting time after each second with a custom message.

        :param waiting_period: Amount of seconds to wait
        :type waiting_period: int
        :param message: Message to print after each second
        :type message: str
        """

        if self.silent:
            return

        tstep = datetime.timedelta(seconds=1)
        tnext = datetime.datetime.now() + tstep

        while waiting_period > 0:

            print("{}{}".format(self.indent, message.format(waiting_period)), end='\r', flush=True)

            tdiff = tnext - datetime.datetime.now()
            time.sleep(tdiff.total_seconds())

            waiting_period = waiting_period - 1
            tnext = tnext + tstep

        print("{}{}".format(self.indent, message.format(0)), end='\r', flush=True)

    @staticmethod
    def get_indent(level):
        """
        Get an indent to a certain level.

        :param level: The level to which to indent (0 = no indent)
        :type level: int
        """
        return "    " * level

    @staticmethod
    def clear_line():
        """
        Clear the current line.
        """
        sys.stdout.write("\033[K")  # clear line

    @staticmethod
    def back_to_previous_line():
        """
        Jump back to the previous line.
        """
        sys.stdout.write("\033[F")
