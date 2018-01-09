
class iSightBaseException(Exception):
    """"Base Exception class for all type of framework Exception"""

    def __str__(self):
        print str(self)

class IncompleteFrameworkException(iSightBaseException):
    """"""
    pass

class UnknownFrameworkException(iSightBaseException):
    """"""
    pass

class UnknownEndpointException(iSightBaseException):
    """"""
    pass

class InvalidProductException(iSightBaseException):
    """"""
    pass

