import csv
import datetime
import os


class LogWriter:
    """
    Writer for writing any fixes made by this script to a log in case something goes wrong.
    """

    def __init__(self, logname, *header):
        """
        Constructor
        """

        today = datetime.date.today().strftime("%Y-%m-%d")
        filename = "{}_{}.csv".format(logname, today)

        new = False
        if not os.path.isfile(filename):
            new = True

        self.file = open(filename, 'a')  # append to log in case it already exists
        self.writer = csv.writer(self.file)

        if new:
            header = ['timestamp', *header]
            self.writer.writerow(header)
            self.file.flush()

    def write_to_log(self, *line):
        """
        Write the result of fixing on event into the log file

        :param line: Line to write to log
        :type line: str
        """
        timestamp = datetime.datetime.now()
        line = [timestamp, *line]

        self.writer.writerow(line)
        self.file.flush()

    def close_log(self):
        """
        Close log when script is done or an error occurs (very important!)
        """
        self.file.close()
