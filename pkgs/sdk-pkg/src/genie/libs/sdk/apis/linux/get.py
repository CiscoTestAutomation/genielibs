"""Common get functions for linux"""

import logging
import re
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def get_file_contents(device, filename, remove_cr=True):
    """
    Args:
        device(`obj`)
        filename(`str`): Absolute path to the file
        remove_cr('str'): Remove carriage return (\r) from the file contents.
    Returns:
        File contents as a string
    """
    cmd = f"cat {filename}"

    try:
        output = str(device.execute(cmd))
        if remove_cr:
            return output.replace('\r', "")
        return output
    except SubCommandFailure as e:
        SubCommandFailure(f"Failed to get the file contents. Error\n {e}")

def get_ip_route_for_ipv4(device, ipv4):
    """
    Args:
        device(`obj`): Device object 
        ipv4(`IPv4Address`): the ip that we want to check the routing table for 
    Returns:
        ip_route('str'): the string format for ip route
    """
    cmd = f"ip route get {ipv4}"
    try:
        output = device.execute(cmd)
    except SubCommandFailure as e:
        SubCommandFailure(f"Failed to get the file contents. Error\n {e}")
    pattern = re.compile(r'.*src (?P<route>[0-9.]+).*')
    route_match = pattern.match(output)
    if route_match:
        return route_match.groupdict().get('route')

    
