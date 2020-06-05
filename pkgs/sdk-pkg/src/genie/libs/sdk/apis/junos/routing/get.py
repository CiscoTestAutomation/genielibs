'''Common get info functions for running-config'''
# Python
import re
import logging
# unicon
from unicon.core.errors import SubCommandFailure
from genie.metaparser.util.exceptions import SchemaEmptyParserError

from genie.libs.sdk.apis.utils import get_config_dict
from genie.utils import Dq
log = logging.getLogger(__name__)

def get_active_outgoing_interface(device, destination_address, extensive=False):
    """ Get active outgoing interface value

        Args:
            device (`obj`): Device object
            destination_address (`str`): Destination address value
            extensive ('bool'): Try command with extensive 
        Returns:
            Interface name
    """

    try:
        if extensive:
            out = device.parse('show route protocol static extensive')
        else:
            out = device.parse('show route protocol static')
    except SchemaEmptyParserError:
        return None
    
    # Example dictionary structure:
    #         {
    #             "rt": [
    #                 {
    #                     "rt-destination": "10.169.14.240/32",
    #                     "rt-entry": {
    #                         "nh": [
    #                             {
    #                                 "to": "10.169.14.121",
    #                                 "via": "ge-0/0/1.0"
    #                             }
    #                         ],
    #                         "rt-tag": "100",
    #                         "preference": "5",
    #                         "protocol-name": "Static"
    #                     }
    #                 }
    #             ],
    #             "table-name": "inet.0",
    #             "total-route-count": "240"
    #         },
    rt_list = Dq(out).get_values("rt")

    for rt_dict in rt_list:
        rt_destination_ = Dq(rt_dict).get_values("rt-destination", 0)
        if not rt_destination_.startswith(destination_address):
            continue

        active_tag_ = Dq(rt_dict).get_values("active-tag", None)
        if not active_tag_:
            continue

        via_ = Dq(rt_dict).get_values("via", None)
        if not via_:
            continue

        return via_.pop()
    
    return None