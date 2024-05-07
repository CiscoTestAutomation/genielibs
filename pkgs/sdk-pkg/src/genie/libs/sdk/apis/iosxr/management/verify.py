
def is_management_interface(device, name):
    ''' Verify if interface is a management interface

    Args:
        name (str): Interface name

    Returns:
        True or False
    '''

    if name.startswith('Mgmt'):
        return True

    return False
