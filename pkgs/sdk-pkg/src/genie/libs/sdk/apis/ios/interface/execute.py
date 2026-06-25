"""Common execute functions for interface"""

# Python
import logging
import re

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def execute_ping(device, proto, dest, repeat=100, timeout=2):
    """ Execute ping on device and return success rate
        Example: ping ip 10.1.1.1 repeat 100 timeout 2
        Args:
            device (`obj`): Device object
            proto (`str`): Protocol (e.g. 'ip', 'ipv6')
            dest (`str`): Destination address
            repeat (`int`, optional): Number of pings. Defaults to 100
            timeout (`int`, optional): Timeout in seconds. Defaults to 2
        Returns:
            int: Success rate percentage
        Raises:
            SubCommandFailure
    """
    try:
        output = device.execute(
            f"ping {proto} {dest} repeat {repeat} timeout {timeout}"
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to execute ping {proto} {dest}. Error: {e}"
        )
    # Example output line being matched:
    #   Success rate is 100 percent (5/5), round-trip min/avg/max = 1/2/4 ms
    match = re.search(r'Success rate is (\d+) percent', output)
    if match:
        return int(match.group(1))
    return 0
