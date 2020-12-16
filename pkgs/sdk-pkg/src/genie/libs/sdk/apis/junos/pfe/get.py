"""Common get info functions for pfe"""

# Python
import re
import copy
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError


log = logging.getLogger(__name__)

def get_pfe_count(device, count_type):
    """Returns count of count_type

    Args:
        device (obj): Device object
        count_type (str): Which count to return. Ex: bfd, arp, atm-oam

    Return:
        str: Count for given count_type
    """

    count_type = count_type.lower().replace(' ', '-')

    # Example dict
    # "pfe-statistics": {
        # "pfe-local-protocol-statistics": {
        #     "arp-count": str,
        #     "atm-oam-count": str,
        #     "bfd-count": str,
        #     "ether-oam-count": str,
        #     "fr-lmi-count": str,
        # }
    # }

    try:
        out = device.parse('show pfe statistics traffic')
    except SchemaEmptyParserError:
        return None

    return out.q.get_values("{}-count".format(count_type), 0)

def get_pfe_hardware_input_drops(device):
    """ Get hardware input drops

    Args:
        device (obj): Device object
        count_type (str): Which count to return. Ex: bfd, arp, atm-oam

    Return:
        str: Count for given count_type
    """

    try:
        out = device.parse('show pfe statistics traffic')
    except SchemaEmptyParserError:
        return None

    return out.q.get_values("hardware-input-drops", 0) or None