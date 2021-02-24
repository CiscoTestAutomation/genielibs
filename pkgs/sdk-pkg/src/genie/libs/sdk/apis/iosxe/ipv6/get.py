"""Common get info functions for interface"""

# Python
import logging

# unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError


log = logging.getLogger(__name__)


def get_ipv6_interface_link_local_address(device, interface):
    """ Get local link address

        Args:
            device (`obj`): Device object
            interface (`str`): Interface value

        Returns:
            link-local address (`str`): Link-Local address
    """
    try:
        out = device.parse('show ipv6 interface {interface}'.format(
            interface=interface
        ))
    except SchemaEmptyParserError:
        return None

    return out.q.contains('.*link.*|ip', 
        regex=True).get_values('ip', 0) or None