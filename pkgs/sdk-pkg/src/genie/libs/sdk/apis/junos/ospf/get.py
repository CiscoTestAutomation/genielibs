"""Common get info functions for OSPF"""

# Python
import logging

# pyATS
from pyats.easypy import runtime

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError


log = logging.getLogger(__name__)


def get_ospf_interface_and_area(device):
    """ Retrieve interface for ospf on junos device

        Args:
            device ('obj'): Device object

        Returns:
            interface and area value dictionary
    """
    try:
        out = device.parse("show ospf interface brief")
    except SchemaEmptyParserError as spe:
        raise SchemaEmptyParserError(
            "Could not parse output for" " command 'show ospf interface brief'"
        ) from spe

    key_val = {}

    try:
        interface_dict = out["instance"]["master"]["areas"]
        for k, v in interface_dict.items():
            for interface in v["interfaces"].keys():
                key_val.update({interface: k})
    except KeyError as ke:
        raise KeyError("Key issue with exception: {}".format(str(ke))) from ke
    return key_val
