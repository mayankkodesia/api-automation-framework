
class productBaseException(Exception):
    """"Base Exception class for all type of framework Exception"""

    def __str__(self):
        print str(self)

class IncompleteFrameworkException(productBaseException):
    """"""
    pass

class UnknownFrameworkException(productBaseException):
    """"""
    pass

class UnknownEndpointException(productBaseException):
    """"""
    pass

class InvalidProductException(productBaseException):
    """"""
    pass

