# -*- coding: utf-8 -*-

class Error(Exception):

    """Base class for exceptions in this package."""
    pass


class AccountTypeError(Error):

    """
    Exception raised for trying to use enterprise or personal account features
    with the wrong account type.

    Attributes:
        msg -- error message
    """

    def __init__(self, msg):
        self.msg = msg


class UnexpectedDataError(Error):

    """
    Exception raised for unexpected data returned from the API.

    Attributes:
        msg -- error message
    """

    def __init__(self, msg):
        self.msg = msg


class ApiError(Error):

    """
    Exception raised for API responses whose status code is not 200.

    Attributes:
        status_code -- status code of the response
        api_id -- API error id
        api_msg -- API error message
    """

    def __init__(self, status_code, api_id, api_msg):
        self.status_code = status_code
        self.api_id = api_id
        self.api_msg = api_msg
