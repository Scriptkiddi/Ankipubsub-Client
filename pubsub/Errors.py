class AuthError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class NotFoundError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
