"""Common get functions for sisf"""

# Python
import logging
import re

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

def get_ip_theft_syslogs(device):
    """Gets IP Theft syslog

    Args:
        device (obj): device object
    Returns:
        Dictionary
        None
    Raises:
        None
    """
    try:
        out = device.parse('show logging | include %SISF-4-IP_THEFT')
    except SchemaEmptyParserError:
        return {}

    # Need to perform additional parsing to extract IP Theft specific data
    # *Sep 15 12:53:06.383 EST:
    timematch = r'.(?P<timestamp>[A-Za-z]{3}\s+\d+ \d+:\d+:\d+\.\d+( [A-Z]+)?:)'

    # *Sep 15 12:53:06.383 EST: %SISF-4-IP_THEFT: IP Theft IP=2001:DB8::101 VLAN=20 MAC=dead.beef.0001 IF=Twe1/0/1 New MAC=dead.beef.0002 New I/F=Twe1/0/1
    theft1 = re.compile(
        timematch +
        r'\s+%SISF-4-IP_THEFT: IP Theft' +
        r'\s+IP=(?P<ip>([a-fA-F\d\:]+)|(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))' +
        r'\s+VLAN=(?P<vlan>\d+)' +
        r'\s+MAC=(?P<mac>([a-fA-F\d]{4}\.){2}[a-fA-F\d]{4})' +
        r'\s+IF=(?P<interface>[\w\/\.\-\:]+)' +
        r'\s+New Mac=(?P<new_mac>([a-fA-F\d]{4}\.){2}[a-fA-F\d]{4})' +
        r'\s+New I/F=(?P<new_if>[\w\/\.\-\:]+)'
    )

    # *Sep 16 19:22:29.392 EST: %SISF-4-IP_THEFT: IP Theft IP=2001:DB8::105 VLAN=20 Cand-MAC=dead.beef.0002 Cand-I/F=Twe1/0/1 Known MAC over-fabric Known I/F over-fabric
    theft2 = re.compile(
        timematch +
        r'\s+%SISF-4-IP_THEFT: IP Theft' +
        r'\s+IP=(?P<ip>([a-fA-F\d\:]+)|(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))' +
        r'\s+VLAN=(?P<vlan>\d+)' +
        r'\s+Cand-MAC=(?P<cand_mac>([a-fA-F\d]{4}\.){2}[a-fA-F\d]{4})' +
        r'\s+Cand-I/F=(?P<cand_if>[\w\/\.\-\:]+)'
    )

    # *Oct 20 16:58:24.807 EST: %SISF-4-IP_THEFT: IP Theft IP=2001:DB8::105 VLAN=20 MAC=dead.beef.0001 IF=Twe1/0/1 New I/F over fabric
    theft3 = re.compile(
        timematch +
        r'\s+%SISF-4-IP_THEFT: IP Theft' +
        r'\s+IP=(?P<ip>([a-fA-F\d\:]+)|(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))' +
        r'\s+VLAN=(?P<vlan>\d+)' +
        r'\s+MAC=(?P<mac>([a-fA-F\d]{4}\.){2}[a-fA-F\d]{4})' +
        r'\s+IF=(?P<if>[\w\/\.\-\:]+)'
    )

    log_dict = {}
    for log_entry in out['logs']:
        m = theft1.match(log_entry)
        if m:
            entry = {}
            group = m.groupdict()

            ip = group['ip']
            vlan = group['vlan']
            mac = group['mac']
            interface = group['interface']
            new_mac = group['new_mac']
            new_interface = group['new_if']

            entry['ip'] = ip
            entry['vlan'] = vlan
            entry['mac'] = mac
            entry['interface'] = interface
            entry['new_mac'] = new_mac
            entry['new_interface'] = new_interface

            log_dict.setdefault('entries', []).append(entry)

        m = theft2.match(log_entry)
        if m:
            entry = {}
            group = m.groupdict()

            ip = group['ip']
            vlan = group['vlan']
            new_mac = group['cand_mac']
            new_if = group['cand_if']

            entry['ip'] = ip
            entry['vlan'] = vlan
            entry['new_mac'] = new_mac
            entry['new_interface'] = new_if

            log_dict.setdefault('entries', []).append(entry)

        m = theft3.match(log_entry)
        if m:
            entry = {}
            group = m.groupdict()

            ip = group['ip']
            vlan = group['vlan']
            mac = group['mac']
            new_if = group['if']

            entry['ip'] = ip
            entry['vlan'] = vlan
            entry['mac'] = mac
            entry['new_interface'] = new_if

            log_dict.setdefault('entries', []).append(entry)

    return log_dict