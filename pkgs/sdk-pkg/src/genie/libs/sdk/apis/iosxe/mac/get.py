"""Common get info functions for mac"""

# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_mac_aging_timer(device, bridge_domain):
    """ Get Aging-Timer from bridge domain

        Args:
            device (`obj`): device object
            bridge_domain (`int`): bridge domain id
        Return:
            aging_time (`int`): aging-time in second
            None 
        Raises:
            None
    """
    try:
        out = device.parse("show bridge-domain {}".format(bridge_domain))
    except SchemaEmptyParserError as e:
        return None

    aging_time = out["bridge_domain"][bridge_domain]["aging_timer"]

    return aging_time


def get_mac_table(device, bridge_domain):
    """ Get mac table from bridge domain

        Args:
            device (`obj`): device object
            bridge_domain (`int`): bridge domain id
        Return:
            mac_table (`dict`): mac table dict
            None: When nothing has been found
        Raises:
            None
    """
    try:
        out = device.parse("show bridge-domain {}".format(bridge_domain))
    except SchemaEmptyParserError as e:
        return None

    mac_table = out["bridge_domain"][bridge_domain].get("mac_table")

    return mac_table
