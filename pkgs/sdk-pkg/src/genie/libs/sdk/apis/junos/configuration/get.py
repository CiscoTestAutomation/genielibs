"""Common get info functions for configuration"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def get_configuration_mpls_label_switched_path_name(device, path):
    """ Get path name from show configuration protocols mpls label-switched-path {path}

    Args:
        device (obj): Device object
        path (str): File to check

    Returns:
        str or None: Configured primary name
    """

    # Example dict
    # "configuration": {
    #             "protocols": {
    #                 "mpls": {
    #                     "label-switched-path": {
    #                         "primary": {
    #                             "name": str,
    #                         }
    #                     }
    #                 }
    #             }
    #         }

    try:
        out = device.parse('show configuration protocols mpls label-switched-path {path}'.format(
            path=path
        ))
    except SchemaEmptyParserError:
        return None

    return out.q.get_values('name', 0) or None


def get_configuration_mpls_paths(device, path):
    """ Get all paths from show configuration protocols mpls path {path}

    Args:
        device (obj): Device object
        path (str): Path to check

    Returns:
        List or None: All path addresses
    """

    # Example dict
    # "configuration": {
    #         "protocols": {
    #             "mpls": {
    #                 "path": {
    #                     "path-list": [{
    #                         'name': str,
    #                     }]
    #                 }
    #             }
    #         }
    #     }

    try:
        out = device.parse('show configuration protocols mpls path {path}'.format(
            path=path
        ))
    except SchemaEmptyParserError:
        return None

    return out.q.get_values('name') or None

def get_configuration_interface_family_bridge_vlan_id(device, interface,
    unit):
    """ Get vlan-di from 
        show configuration interface {interface} unit {unit} family bridge vlan-id

    Args:
        device (obj): Device object
        interface (str): Interface name
        unit (str): Unit value

    Returns:
        str: vlan-id
    """

    try:
        out = device.parse('show configuration interface {interface} unit {unit} family bridge vlan-id'.format(
            interface=interface,
            unit=unit
        ))
    except SchemaEmptyParserError:
        return None
    # Example dict
    # 'configuration': {
    #             'interfaces': {
    #                 'interface': {
    #                     'name': 'ge-0/0/1',
    #                     'unit': {
    #                         'family': {
    #                             'bridge': {
    #                                 'vlan-id': '10'
    #                                 }
    vlan_id = out.q.get_values('vlan-id', 0)
    
    return vlan_id if vlan_id else None