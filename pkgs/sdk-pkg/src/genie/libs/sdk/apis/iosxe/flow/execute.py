import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

"""Execute CLI functions for flow"""
def execute_set_fnf_debug(device):
    """ set platform software trace fed switch active fnf debug
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"set platform software trace fed switch active fnf debug"
    try:
        device.execute(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not set platform software trace fed switch active fnf debug on device. Error:\n{e}')

def execute_set_fnf_verbose(device):
    """ set platform software trace fed switch active fnf verbose
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"set platform software trace fed switch active fnf verbose"
    try:
        device.execute(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not set platform software trace fed switch active fnf verbose on device. Error:\n{e}')

def execute_monitor_capture_start_capture_filter(device, capture_name, capture_filter):
    """
        Execute monitor capture <capture_name> start capture-filter <capture_filter>
        Example: monitor capture test start capture-filter ANY
        Args:
            device ('obj'): Device Object
            capture_name ('str'): Name of Capture
            capture_filter ('str'): Capture filter String
    """
    cmd = f"monitor capture {capture_name} start capture-filter {capture_filter}"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not execute monitor capture {capture_name} start capture_filter {capture_filter}. \nError: {e}")

def execute_monitor_capture_file_location_flash(device, capture_name, file_name, number_of_file = '', size_of_file = ''):
    """
        Execute:
        - monitor capture <capture_name> file location flash:<file_name>
        - monitor capture <capture_name> file location flash:<file_name> ring <number_of_file> size <size_of_file>
        Example:
        - monitor capture test file location flash:testin.pcap
        - monitor capture test file location flash:testin.pcap ring 4 size 1
        Args:
            device ('obj'): Device Object
            capture_name ('str'): Name of Capture
            file_name ('str'): Name of file
            number_of_file (int): Number of File (<2-10> Number of files in the file ring)
            size_of_file (int): File size (<1-100> Total size of file(s) in MB)
    """
    cmd = [
        f'monitor capture {capture_name} file location flash:{file_name}',
        f'monitor capture {capture_name} file location flash:{file_name} size {size_of_file}',
        f'monitor capture {capture_name} file location flash:{file_name} ring {number_of_file}',
        f'monitor capture {capture_name} file location flash:{file_name} ring {number_of_file} size {size_of_file}',
        ]

    command = ''
    if number_of_file:
        if size_of_file:
            command = cmd[3]
        else:
            command = cmd[2]
    if size_of_file:
        command = cmd[1]
    else:
        command = cmd[0]
    try:
        device.execute(command)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not perform {command}. \nError: {e}')

def execute_monitor_capture_class_map(device, capture_name, class_name):
    """
        Execute monitor capture <capture_name> class-map <class_name>
        Example: monitor capture test class-map myclassmap
        Args:
            device ('obj'): Device Object
            capture_name ('str'): Name of Capture
            class_name ('str'): Class name
    """
    cmd = f"monitor capture {capture_name} class-map {class_name}"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not execute monitor capture {capture_name} class-map {class_name}. \nError: {e}")

def execute_monitor_capture_clear(device, capture_name):
    """
        Execute monitor capture <capture_name> clear
        Example: monitor capture test clear
        Args:
            device ('obj'): Device Object
            capture_name ('str'): Name of Capture
    """
    cmd = f"monitor capture {capture_name} clear"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not execute monitor capture {capture_name} clear. \nError: {e}")

def execute_monitor_capture_limit_duration(device, capture_name, duration):
    """
        Execute monitor capture {capture_name} limit duration {duration}
        Example: monitor capture test limit duration 40
        Args:
            device ('obj'): Device Object
            capture_name ('str'): Name of Capture
            duration ('int'): Duration in Seconds : Min 1 - Max 1000000
    """
    cmd = f"monitor capture {capture_name} limit duration {duration}"

    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not execute monitor capture {capture_name} limit duration {duration}. \nError: {e}")

def execute_monitor_capture_access_list(device, capture_name, access_list_name):
    """
        Execute monitor capture {capture_name} access-list {access_list_name}
        Example: monitor capture test access-list MYACLV6
        Args:
            device ('obj'): Device Object
            capture_name ('str'): Name of Capture
            access_list_name ('str'): Access list name
    """
    cmd = f"monitor capture {capture_name} access-list {access_list_name}"

    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not execute monitor capture {capture_name} access-list {access_list_name}. \nError: {e}")

def execute_monitor_capture_vlan_in_match_any(device, capture_name, vlan_id):
    """
        Execute monitor capture {capture_name} vlan {vlan_id} in match any
        Example: monitor capture test vlan 33 in match any
        Args:
            device ('obj'): Device Object
            capture_name ('str'): Name of Capture
            vlan_id ('int'): Vlan ID
    """
    cmd = f"monitor capture {capture_name} vlan {vlan_id} in match any"

    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not execute monitor capture {capture_name} vlan {vlan_id} in match any. \nError: {e}")
