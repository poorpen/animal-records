class ApplicationException(Exception):
    """base application exception """

    def message(self):
        ...