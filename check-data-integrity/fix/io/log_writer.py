import csv
import datetime
import os


class LogWriter:
    """
    Writer for writing any fixes made by this script to a log in case something goes wrong.
    """

    def __init__(self):
        """
        Constructor
        """

        today = datetime.date.today().strftime("%Y-%m-%d")
        filename = "fix_log_{}.csv".format(today)

        new = False
        if not os.path.isfile(filename):
            new = True

        self.file = open(filename, 'a')  # append to log in case it already exists
        self.writer = csv.writer(self.file)

        if new:
            header = ['timestamp', 'mediapackage', 'tenant', 'error', 'fix']
            self.writer.writerow(header)

    def write_to_log(self, mediapackage, tenant, error, fix):
        """
        Write the result of fixing on event into the log file

        :param mediapackage: ID of the fixed mediapackage
        :type mediapackage: str
        :param tenant: ID of the tenant the mediapackage belongs to
        :type tenant: str
        :param error: Description of the error that was fixed
        :type error: str
        :param fix: Description of fix that was conducted
        :type fix: str
        """
        timestamp = datetime.datetime.now()

        self.writer.writerow([timestamp, mediapackage, tenant, error, fix])
        self.file.flush()

    def close_log(self):
        """
        Close log when script is done or an error occurs (very important!)
        """
        self.file.close()
