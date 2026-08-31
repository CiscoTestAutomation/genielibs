# Copyright (c) 2026 by Cisco Systems, Inc.
# All rights reserved.

"""Common get info functions for spanning-tree"""

# Python
import re
import logging
from unicon.core.errors import SubCommandFailure
from genie.libs.parser.utils.common import Common as genie_common
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_show_spanning_tree_output(device):
    '''
    Get show spanning-tree output
    Args:
        device (`obj`): Device object
    Returns:
        output (`str`): show spanning-tree output
    '''
    try:
        output = device.execute("show spanning-tree")
        return output
    except SubCommandFailure as e:
        logging.error(f"Failed to execute 'show spanning-tree' on {device}. Error: {e}")
        return None


def get_show_spanning_tree_interface_detail_output(device, interface):
    '''
    Get show spanning-tree interface {interface} detail output
    Args:
        device (`obj`): Device object
        interface (`str`): Interface name
    Returns:
        Dict with spanning-tree interface detail output
    '''
    try:
        return device.parse(f"show spanning-tree interface {interface} detail")
    except (SchemaEmptyParserError, SubCommandFailure, Exception) as e:
        log.error(f"Could not get spanning-tree interface {interface} info, "
                  f"exception is: {e}")
        return None


def get_spanning_tree_interface_cost(device, vlan, interface):
    '''
    Get spanning-tree interface cost
    Args:
        device (`obj`): Device object
        vlan (`str`): vlan name
        interface (`str`): Interface name
    Returns:
        cost (`str`): spanning-tree interface cost
    '''
    res = device.parse(f'show spanning-tree interface {interface}')
    vlan_dict = res.get('vlan', {})
    for port_info in vlan_dict:
        if vlan is not None and vlan.lower() not in port_info.lower():
            continue
        cost = vlan_dict[port_info].get('cost')
        return cost


def get_interface_spanning_tree_portfast_output(device, interface):
    """ Get configure interface spanning_tree portfast output
    Args:
        device ('obj') : Device object
        interface ('str') : interface name
    Returns:
        output ('str'): spanning_tree portfast output
    """
    output = device.config([f'interface {interface}', 'spanning-tree portfast'])
    return output


def get_configure_spanning_tree_guard_root_output(device, interface=None):
    """ Get configure spanning_tree guard root output
    Args:
        device ('obj') : Device object
        interface ('str') : interface name
    Returns:
        output ('str'): spanning_tree guard root output
    """
    if interface is None:
        output = device.configure(['spanning-tree guard root'], error_pattern=[])
    else:
        output = device.configure([f'interface {interface}', 'spanning-tree guard root'])
    return output


def get_configure_spanning_tree_mst_instance_output(device, instance, vlan):
    """ Get configure spanning_tree mst instance output
    Args:
        device ('obj') : Device object
        instance ('str') : mst instance name
        vlan ('str') : vlan name
    Returns:
        output ('str'): spanning_tree mst instance output
    """
    output = device.configure(['spanning-tree mst configuration', f'instance {instance} vlan {vlan}'])
    return output


def get_spanning_tree_interfaces(device):
    """ Get spanning_tree interfaces
    Args:
        device ('obj') : Device object
    Returns:
        output ('str'): spanning_tree interfaces output
    """
    res = device.execute('show spanning-tree')
    interfaces = re.findall(r'[A-Z][a-z]+\d(?:\/\d\/\d+)?(?:\s)', res, re.MULTILINE)
    return_list = []
    for i in set(interfaces):
        return_list.append(genie_common.convert_intf_name(i))
    return return_list
