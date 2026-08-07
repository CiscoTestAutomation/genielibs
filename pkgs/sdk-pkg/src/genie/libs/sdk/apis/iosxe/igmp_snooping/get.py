"""Common get info functions for IGMP snooping"""

# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_igmp_snooping_group(device, vlan, group):
    """Retrieve ip igmp snooping group entry
        Args:
            device ('obj'): device object
            vlan ('str'): vlan id
            group ('str'): group ip address
        Returns:
            Dict: the matched group entry, or {} if not found, e.g.
                {
                    'vlan': '20',
                    'type': 'I',
                    'version': 'v2',
                    'port_list': 'Gi0/1/5 Gi0/1/6',
                }
        Raises:
            None
    """
    try:
        out = device.parse(f'show ip igmp snooping groups vlan {vlan} {group}')
    except SchemaEmptyParserError:
        log.debug("Command has not returned any results")
        return {}
    entry = out.q.contains(group)
    if entry.count() == 0:
        log.debug(f"No matched entry found for group {group}")
        return {}
    return out['igmp_groups'][group]


def get_igmp_snooping_groups_count(device, vlan=None):
    """
    Retrieve ip igmp snooping groups count
    Args:
        device ('obj'): device object
        vlan ('str', optional): vlan id
    Returns:
        Dict: groups count, or {} if no result. When no vlan, e.g.
                {
                    'total_number_of_groups': {
                        'igmp_groups_count': 831,
                    },
                }
            When vlan is given, e.g.
                {
                    'vlan': {
                        '20': {'count': 256},
                    },
                }
    Raises:
        None
    """

    cli = "show ip igmp snooping groups count"
    if vlan:
        cli = f"show ip igmp snooping groups vlan {vlan} count"
    try:
        out = device.parse(cli)
    except SchemaEmptyParserError:
        log.debug("Command has not returned any results")
        return {}
    return out


def get_igmp_vrf_snooping_groups(device, vrf):
    """
    Retrieve ip igmp snooping groups of vrf
    Args:
        device ('obj'): device object
        vrf ('str'): vrf name
    Returns:
        Dict: groups keyed by index, or {} if no result, e.g.
                {
                    '1': {
                        'vlan': 20,
                        'group': '224.1.1.1',
                        'type': 'I',
                        'version': 'v2',
                        'port_list': ['GigabitEthernet0/1/6'],
                    },
                }
    Raises:
        None
    """

    cli = f"show ip igmp vrf {vrf} snooping groups"

    try:
        out = device.parse(cli)
    except SchemaEmptyParserError:
        log.debug("Command has not returned any results")
        return {}
    return out


def get_igmp_groups(device, interface=None):
    """
    Retrieve ip igmp groups
    Args:
        device ('obj'): device object
        interface ('str', optional): interface name
    Returns:
        Dict: groups keyed by address, or {} if no result, e.g.
                {
                    'igmp_groups': {
                        '228.0.8.204': {
                            'intf': 'Vlan10',
                            'uptime': '00:02:26',
                            'expires': '00:02:45',
                            'last_reporter': '60.1.1.2',
                        },
                    },
                }
    Raises:
        None
    """

    cli = "show ip igmp groups"
    if interface:
        cli += f" {interface}"
    try:
        out = device.parse(cli)
    except SchemaEmptyParserError:
        log.debug("Command has not returned any results")
        return {}
    return out


def get_igmp_vrf_groups(device, vrf):
    """
    Retrieve ip igmp groups of vrf
    Args:
        device ('obj'): device object
        vrf ('str'): vrf name
    Returns:
        Dict: groups keyed by address, or {} if no result, e.g.
                {
                    'igmp_group_address': {
                        '224.1.1.1': {
                            'interface': 'Vlan20',
                            'uptime': '00:00:09',
                            'expires': '00:02:50',
                            'last_reporter': '50.50.2.2',
                        },
                    },
                }
    Raises:
        None
    """

    cli = f"show ip igmp vrf {vrf} groups"

    try:
        out = device.parse(cli)
    except SchemaEmptyParserError:
        log.debug("Command has not returned any results")
        return {}
    return out


def get_igmp_snooping(device):
    """
    Get ip igmp snooping information
    Args:
        device ('obj'): device object
    Returns:
        Dict: global and per-vlan snooping info, or {} if no result, e.g.
                {
                    'igmp_snooping_oper_state': 'Enabled',
                    'igmpv3_snooping': 'Enabled',
                    'report_supression': 'Enabled',
                    'eht_db_limit': 100000,
                    'eht_db_count': 0,
                    ...
                    'vlan': {
                        '1': {
                            'igmp_snooping_admin_state': 'Enabled',
                            'igmp_snooping_oper_state': 'Enabled',
                            ...
                        },
                    },
                }
    Raises:
        None
    """

    cli = "show ip igmp snooping"

    try:
        out = device.parse(cli)
    except SchemaEmptyParserError:
        log.debug("Command has not returned any results")
        return {}
    return out
