"""Common verification functions for l2route"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def verify_l2route_mac_route_flag(device, expected_flag, mac_address=None, 
    max_time=30, check_interval=10
):
    """ Verify for route flags for the corresponding mac (if given)

        Args:
            device ('obj'): device to use
            expected_flag ('str'): flags
            mac_address ('str'): Mac
            max_time ('int', optional): maximum time to wait in seconds,
                default is 30
            check_interval ('int', optional): how often to check in seconds,
                default is 10
        Returns:
            result ('bool'): verified result
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        received_flags =  device.api.get_l2route_mac_route_flags(
             device=device,
             mac_address=mac_address,
             )
        if received_flags and mac_address:
            if expected_flag in received_flags.values():
                return True
        elif received_flags:
            actual_flags = []
            for i in received_flags.values():
                actual_flags.extend(i)
            # Checking whether expected flag exists 
            if expected_flag in actual_flags:
                return True
        else:
            timeout.sleep()

    if not received_flags:
        log.error("Could not get mac route flags along with mac_address")
    else:
        log.error('Expected flag is "{expected_flag}",and actual flag is '
            '"{received_flags}"'.format(expected_flag=
                expected_flag, received_flags=received_flags)
        )

    return False

