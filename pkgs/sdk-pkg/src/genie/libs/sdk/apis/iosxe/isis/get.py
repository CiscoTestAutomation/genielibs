"""Common get info functions for IS-IS"""

# Python
import logging

# unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError


log = logging.getLogger(__name__)

def get_isis_interface_metric(device, interfaces=None, level='level-2'):
    """
    Gets IS-IS interface metric

    Args:
        device (, optional): Device used to run commands
        interfaces ('list'): List of interfaces. Defaults to None
        level ('str): IS-IS level. Default to 'level-2'

    Returns List with ISIS interface metric like:
        [{'interface': 'Ethernet2/0', 'metric': 10, 'ipv6_metric': 10]
    """

    isis_intf_metric = []

    try:
        out = device.parse('show running-config all | section ^interface')
    except SchemaEmptyParserError:
        return []

    if not interfaces:
        interfaces = out.q.contains('isis').get_values('interfaces')

    for intf in interfaces:
        metric = out.q.contains_key_value('interfaces', intf).contains(level).contains('ipv4').get_values('metric', 0)
        ipv6_metric = out.q.contains_key_value('interfaces', intf).contains(level).contains('ipv6').get_values('metric', 0)
        isis_intf_metric.append({'interface': intf, 'metric': metric, 'ipv6_metric': ipv6_metric})

    return isis_intf_metric
    