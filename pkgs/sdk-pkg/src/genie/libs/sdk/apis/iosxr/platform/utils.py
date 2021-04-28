import re


def is_connected_via_vty(device, alias=None):
    ''' Check if we are connected via VTY
    '''
    if alias:
        conn = getattr(device, alias)
    else:
        conn = device
    show_users = conn.execute(r'show users')
    if re.search(r'\* +vty', show_users):
        return True
    return False
