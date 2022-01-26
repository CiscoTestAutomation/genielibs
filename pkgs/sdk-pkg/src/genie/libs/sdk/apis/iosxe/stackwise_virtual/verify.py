"""Common verify functions for stackwise-vitual"""

# Python
import logging

# Unicon
from genie.metaparser.util.exceptions import SchemaEmptyParserError

def verify_traffic_flow_on_svl_interfaces(device, min_packet_flow):
    """ Verify that packets are not flowings on svl links
        Args:
            device(`obj`): Device object
            min_packet_flow (`int`): control packets expected to flow.
        returns:
            True if traffic is not flowing, false in all other cases
    """
    res = True
    try:
        output=device.parse("show stackwise-virtual")
    except SchemaEmptyParserError as e:
            return False

    for intf in output.q.get_values("ports"):
        output=device.parse("show interface {intf} counters".format(intf=intf)) 
        if not ((output.q.get_values('inmcastpkts')[0] < min_packet_flow) and  \
                (output.q.get_values('outmcastpkts')[0] < min_packet_flow)):
            res = False 

        if not ((output.q.get_values('inucastpkts')[0] < min_packet_flow) and \
                (output.q.get_values('outucastpkts')[0] < min_packet_flow)):
            res = False
    return res 
