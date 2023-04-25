class CustomError(Exception):
    """Exception raised for errors in the functions.
    It appears when input-data is in inappropriate format.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

