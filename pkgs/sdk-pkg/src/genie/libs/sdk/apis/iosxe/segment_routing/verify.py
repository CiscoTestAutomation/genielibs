"""Common verification functions for Segment-Routing"""

# Python
import logging

# pyATS
from genie.utils.timeout import Timeout

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import (
    SchemaEmptyParserError
)

log = logging.getLogger(__name__)


def verify_sid_in_segment_routing(device, address_family=None):
    """ Verifies if SID is found in segment-routing
        from command 'show segment-routing mpls connected-prefix-sid-map ipv4'
        
        Args:
            device (`obj`): Device to be executed command
            address_family (`str`): Address family name
        Raises:
            None
        Returns
            True
            False

    """

    if not address_family:
        address_family = 'ipv4'

    try:
        out = device.parse(
            "show segment-routing mpls connected-prefix-sid-map {}".format(address_family)
        )
    except (SchemaEmptyParserError):
        return False

    sid_count = 0
    try:
        sid_count = len(
            out["segment_routing"]["bindings"]["connected_prefix_sid_map"][
                address_family
            ]["ipv4_prefix_sid" if address_family is 'ipv4' else 'ipv6_prefix_sid'].keys()
        )
    except KeyError:
        pass
    return sid_count != 0

def verify_status_of_segment_routing(device, state=None):
    """ Verifies if state matches expected_state state in segment-routing
        from command 'show segment-routing mpls state'
        
        Args:
            device (`obj`): Device to be executed command
            state (`str`): Expected state
        Raises:
            None
        Returns
            True
            False

    """
    if not state:
        state = 'ENABLED'
        
    state_found = None
    try:
        out = device.parse("show segment-routing mpls state")
    except (SchemaEmptyParserError):
        return False
    try:
        state_found = out["sr_mpls_state"]
    except KeyError:
        return False
    return state_found.upper() == state.upper()

