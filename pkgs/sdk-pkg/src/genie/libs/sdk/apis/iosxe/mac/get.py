"""Common get info functions for mac"""

# Python
import logging
import re 

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Unicon
from unicon.core.errors import SubCommandFailure

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
            {}: When nothing has been found
        Raises:
            None
    """
    try:
        out = device.parse("show bridge-domain {}".format(bridge_domain))
    except SchemaEmptyParserError as e:
        return {}

    mac_table = out["bridge_domain"][bridge_domain].get("mac_table")

    return mac_table


def get_mac_table_from_address_family(device, address_family):
    """ Gets mac table from address_family

        Args:
            device (`obj`): device object
            address_family ('str'): address_family
        Return:
            mac_table (`dict`): mac table dict
            {}: When nothing has been found
        Raises:
            None
    """
    try:
        mac_output = device.parse("show {} mac".format(address_family))
    except SchemaEmptyParserError as e:
        return {}

    mac_table = dict()
    for evi in mac_output['evi']:
        mac_table[evi] = []
        for bdid in mac_output['evi'][evi]['bd_id']:
            for eth_tag in mac_output['evi'][evi]['bd_id'][bdid]['eth_tag']:
                for mac in mac_output['evi'][evi]['bd_id'][bdid]['eth_tag'][eth_tag]['mac_addr']:
                    # Adding list of mac addresses to corresponding evi's
                    mac_table[evi].append(mac)

    return mac_table
