"""Common verify functions for routing"""

# Python
import re
import logging

# pyATS
from genie.utils import Dq

# Genie
from genie.utils.timeout import Timeout
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.libs.sdk.apis.utils import get_config_dict
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Unicon
from unicon.core.errors import SubCommandFailure


log = logging.getLogger(__name__)

def get_interface_output_pps(device, interface):
    """ Retrieve output pps value from interface
        Args:
            device ('obj'): Device object
            interface ('str'): Interface name

        Returns:
            Output pps value
    """
    out = None
    try:
        out = device.parse('monitor interface traffic')
    except SchemaEmptyParserError as e:
        return None
    
    if not out:
        return None
    # Example dict
    # {
    #     "monitor-time": {
    #         "06:01:12": {
    #             "hostname": "genie",
    #             "interface": {
    #                 "ge-0.0.0": {
    #                     "output-packets": 0
    #                 },
    #             }
    #         }
    #     }
    # }
    output_pps = Dq(out).contains(interface). \
        get_values('output-pps')
    if not output_pps:
        return None
    return output_pps.pop()
