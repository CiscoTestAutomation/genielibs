"""Common get info functions for NVE"""

# Python
import logging

from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def get_nve_vnis(device):
    """ Get NVE VNI table entries
        Args:
            device ('obj'): device object
        Returns:
            Dictionary
        Raises:
            None
    """

    cli = "show nve vni"

    try:
        return device.parse(cli)
    except SchemaEmptyParserError:
        log.info("Command has not returned any results")
        return {}


def get_nve_interface_tunnel(device, nve_intf):
    """ Get NVE interface tunnel information
        Args:
            device ('obj'): device object
            nve_intf ('str'): NVE Interface
        Returns:
            tunnel('str'): Tunnel interface
        Raises:
            None
    """

    cli = "show nve interface {} detail".format(nve_intf)

    try:
        out = device.parse(cli)
    except SchemaEmptyParserError:
        log.info("Command has not returned any results")
        return ''

    if out.q.get_values('tunnel_intf'):
        return out.q.get_values('tunnel_intf')[0]
    else:
        return ''