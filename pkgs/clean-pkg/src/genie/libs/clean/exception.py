class CleanException(Exception):
    ''' base class '''
    pass

class StackMemberConfigException(CleanException):
    """
    Exception for when all the member of stack device is configured
    """
    pass