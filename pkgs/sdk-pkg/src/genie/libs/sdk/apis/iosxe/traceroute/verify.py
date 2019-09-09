# PYthon
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# iosxe traceroute
from genie.libs.parser.iosxe.traceroute import Traceroute

log = logging.getLogger(__name__)


def verify_traceroute_first_hop_address(
    device, prefix, expected_first_hop_address
):
    """ Verify if first hop ip address is expected one
        Args:
            device ('obj'): Device object
            prefix ('str'): Prefix address
            expected_hop_address ('str'): Expected next hop ip address
        Returns:
            True/False
        Raises:
            None
    """

    parsed_output = device.api.get_traceroute_parsed_output(
        device=device, prefix=prefix
    )
    if not parsed_output:
        return False

    # Since we are checking first hop, '1' is hard coded
    first_hop = (
        parsed_output["traceroute"]
        .get(prefix, {})
        .get("hops", {})
        .get("1", {})
        .get("paths", {})
        .get(1, {})
        .get("address", None)
    )

    if not first_hop:
        return False
    elif expected_first_hop_address == first_hop:
        log.info('First hop address is {address} as expected'.format(address=expected_first_hop_address))
        return True
    else:
        log.info(
            "First hop address {address} is not as expected".format(
                address=first_hop
            )
        )
        return False
