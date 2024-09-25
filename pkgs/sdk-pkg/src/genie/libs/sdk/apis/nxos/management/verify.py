import re

def is_management_interface(device, name):
    ''' Verify if interface is a management interface

    Args:
        name (str): Interface name

    Returns:
        True or False
    '''

    if re.match('^mgmt0$', name):
        return True

    return False