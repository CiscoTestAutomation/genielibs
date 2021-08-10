"""Common get functions for sisf"""

# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def get_device_tracking_policy_name_configurations(device, policy):
    """ Get device-tracking policy configurations
        Args:
            device ('obj'): device object
            policy ('str'): policy name
        Returns:
            Dictionary
            None
        Raises:
            None
    """
    try:
        out = device.parse('show device-tracking policy {policy}'.format(policy=policy))
        return out.get('configuration', None)
    except SchemaEmptyParserError:
        log.info("Command has not returned any results")

    return None


def get_device_tracking_database_details_binding_table_configurations(device):
    """ Get device-tracking policy configurations
        Args:
            device ('obj'): device object
        Returns:
            Dictionary
            None
        Raises:
            None
    """
    try:
        out = device.parse('show device-tracking database details')
        return out.get('binding_table_configuration', None)
    except SchemaEmptyParserError:
        log.info("Command has not returned any results")

    return None


def get_device_tracking_database_details_binding_table_count(device, state=False):
    """ Get device-tracking policy configurations
        Args:
            device ('obj'): device object
            state('bool', optional): get state count if True. Defaults to False
        Returns:
            Dictionary
            None
        Raises:
            None
    """
    if state:
        key = 'binding_table_state_count'
    else:
        key = 'binding_table_count'

    try:
        out = device.parse('show device-tracking database details')
        return out.get(key, None)
    except SchemaEmptyParserError:
        log.info("Command has not returned any results")

    return None


def get_ipv6_nd_raguard_policy_configurations(device, policy):
    """ Get ipv6 nd raguard policy configurations
        Args:
            device ('obj'): device object
            policy ('str'): policy name
        Returns:
            Dictionary
            None
        Raises:
            None
    """
    try:
        out = device.parse('show ipv6 nd raguard policy {policy}'.format(policy=policy))
        return out.get('configuration', None)
    except SchemaEmptyParserError:
        log.info("Command has not returned any results")

    return None


def get_ipv6_source_guard_policy_configurations(device, policy):
    """ Get ipv6 source guard policy configurations
        Args:
            device ('obj'): device object
            policy ('str'): policy name
        Returns:
            Dictionary
            None
        Raises:
            None
    """
    try:
        out = device.parse('show ipv6 source-guard policy {policy}'.format(policy=policy))
        return out.get('configuration', None)
    except SchemaEmptyParserError:
        log.info("Command has not returned any results")

    return None


def get_device_tracking_counters_vlan_message_type(device, vlanid, message_type="received"):
    """ Get device_tracking vlan count message type
        Args:
            device ('obj'): device object
            vlanid ('str'): vlan
            message_type ('str', optional): message type. Defaults to "received"
        Returns:
            Dictionary
            None
        Raises:
            None
    """
    try:
        out = device.parse('show device-tracking counters vlan {vlanid}'.format(vlanid=vlanid))
    except SchemaEmptyParserError:
        log.info("Command has not returned any results")

    message_dict = out.get("vlanid", {}).get(int(vlanid), {})
    if not message_dict:
        log.info("There is no activity corresponding to the message type {type}"
                .format(type=message_type))
        return None

    return message_dict


def get_device_tracking_counters_vlan_faults(device, vlanid):
    """ Get device_tracking vlan count message type
        Args:
            device ('obj'): device object
            vlanid ('str'): vlan
        Returns:
            List
            None
        Raises:
            None
    """
    try:
        out = device.parse('show device-tracking counters vlan {vlanid}'.format(vlanid=vlanid))
    except SchemaEmptyParserError:
        log.info("Command has not returned any results")

    fault_list = out.get("vlanid", {}).get(int(vlanid), {}).get("faults", [])
    if not fault_list:
        log.info("There are no faults on vlan {vlanid}".format(vlanid=vlanid))
        return None

    return fault_list
