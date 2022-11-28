"""Common verify info functions for protocols"""
# Python
import logging
import re
# Unicon
from unicon.core.errors import SubCommandFailure
log = logging.getLogger(__name__)

def verify_neighbor_count(device, protocol, neighbor, value, neighbor_count):
    """ verify the neighbor count

        Args:
            device('obj'): device to configure on
            protocol('str'): Protocol name
            neighbor'str'): neighbor (or) neighbors
            value ('str'): grep the count using specific value
            neighbor_count (int): expected neighbor count details
        Return:
            boolean
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(
        "verify the neighbor count  on device for  protocol {protocol} neighbor {neighbor} value {value}".format(
           protocol=protocol, neighbor=neighbor, value=value
        )
    )
    cmd = f'show {protocol} {neighbor} | count {value}'
    try:
        output = device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not executing neighbor count on device".format(protocol=protocol,neighbor=neighbor,value=value, e=e)
        )
    p = re.compile(r"^Number of lines which match regexp\s*=\s*(?P<count>[\d]+)$")
    count = int(p.search(output).groupdict().get('count', 0))

    if count == neighbor_count:
        return True
    else:
        return False