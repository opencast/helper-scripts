
class Logger:
    """
    minimal logger to either be verbose or don't print messages at all.
    """
    verbose = True

    def __init__(self, verbose: bool):
        """
        Constructor
        """
        self.verbose = verbose

    def log(self, *args):
        if self.verbose:
            print(*args)
