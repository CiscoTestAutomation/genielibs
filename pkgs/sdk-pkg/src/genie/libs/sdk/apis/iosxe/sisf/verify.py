"""Common verification functions for sisf"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.libs.parser.utils.common import Common
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def _verify_policy_configurations(output, config_dict):
    """ Helper function to verify non-nested configurations
        Args:
            output('dict'): output from parser
            config_dict('dict'): configurations to check
        Returns:
            True
            False
        Raises:
            None
    """
    for key, value in config_dict.items():
        if output[key] != value:
            log.info('Configuration {config} is either not found or incorrect. Expected '
                     '{value}. Instead found {target_value}.'
                     .format(config=key, value=value, target_value=output[key]))
            return False

    return True


def _verify_missing_policy_configurations(output, config_dict):
    """ Helper function to verify missing configurations
        Args:
            output('dict'): output from parser
            config_dict('dict'): configurations to check
        Returns:
            True
            False
        Raises:
            None
    """
    for key, value in config_dict.items():
        if value:
            if key in output:
                log.info('Configuration {config} is set. Unset it to pass.'.format(config=key))
                return False
    return True


def _verify_ipv6_policy(output, policy_name, vlan, iface, feature):
    """ Helper function to verify ipv6 policies
        Args:
            output('dict'): output from parser
            policy_name('str'): policy name
            vlan('str'): vlan target
            iface('str'): interface target
            feature('str'): sisf features
        Returns:
            True
            False
        Raises:
            None
    """
    if output['device']:
        devices = output['device']
        if vlan:
            target = "vlan " + vlan
        elif iface:
            target = iface

        for _, device_num, in enumerate(devices):
            if devices[device_num]['target'] == target and devices[device_num]['policy_name'] == policy_name \
                and devices[device_num]['feature'] == feature:
                return True

    return False


def verify_device_tracking_policies(device, policy_name, vlan=None, iface=None, feature='Device-tracking',
                    max_time=20, check_interval=10):
    """ Verify device tracking policies

        Args:
            device('obj'): device object
            policy_name('str'): policy name
            vlan('str'): vlan target
            iface('str'): interface target
            feature('str'): sisf features. Default "Device-tracking"
            max_time('int',optional): max check time. Defaults to 20
            check_interval('int',optional): check intervals. Defaults to 10
        Returns:
            Bool
        Raises:
            None
    """
    target = None
    if vlan:
        target = "vlan " + vlan
    elif iface:
        target = iface
    else:
        log.error('No Target provide')
        return False

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        output = device.parse('show device-tracking policies')
        if output['policies']:
            policies = output['policies']
            for i in range(1, len(policies)+1):
                if (policies[i]['policy_name'] == policy_name and
                        policies[i]['target'] == target and policies[i]['feature'] == feature):
                    log.debug('Target policy found on expected target')
                    return True

        timeout.sleep()

    log.debug('Target policy not found')
    return False

def verify_empty_device_tracking_policies(device, max_time=60, check_interval=10):
    """ Verify device tracking policies is empty

        Args:
            device('obj'): device object
            max_time('int',optional): max check time. Defaults to 60
            check_interval('int',optional): check intervals. Defaults to 10
        Returns:
            Bool
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.parse('show device-tracking policies')
        except SchemaEmptyParserError:
            return True
    timeout.sleep()

    log.debug('Device-tracking policies is not empty:\n{}'.format(output))
    return False

def verify_device_tracking_policy_configuration(device, policy_name, security_level='guard',
                                                trusted_port=None, device_role=None,
                                                data_glean=None, prefix_glean=None,
                                                neighbor_discovery=None, dhcp6=None, arp=None,
                                                dhcp4=None, ipv4_limit_address_count=None,
                                                ipv6_limit_address_count=None, cache_guard=None,
                                                tracking=None, max_time=1, check_interval=1):
    """ Verify device-tracking policy configurations
        Args:
            device('obj'): device object
            policy_name('str'): policy name
            security_level('str'): security level, default='guard'
            trusted_port('str', optional): trusted port (yes | no). Defaults to None
            device_role('str', optional): device role. Defaults to None
            data_glean('str', optional): data glean. Defaults to None
            prefix_glean('str', optional): prefix glean. Defaults to None
            neighbor_discovery('str', optional): neighbor discovery (gleaning | not gleaning). Defaults to None
            dhcp6('str', optional): dhcp6 (gleaning | not gleaning). Defaults to None
            arp('str', optional): arp (gleaning | not gleaning). Defaults to None
            dhcp4('str', optional): dhcp6 (gleaning | not gleaning). Defaults to None
            ipv4_limit_address_count('int', optional): ipv4 address count limit. Defaults to None
            ipv6_limit_address_count('int', optional): ipv6 address count limit. Defaults to None
            cache_guard('str', optional): cache guard. Defaults to None
            tracking('str', optional): tracking. Defaults to None
            max_time('int',optional): max check time. Defaults to 1
            check_interval('int',optional): check intervals. Defaults to 1
        Returns:
            True
            False
        Raises:
            None
    """
    config_dict = {
        "trusted_port": trusted_port,
        "security_level": security_level,
        "device_role": device_role,
        "data_glean": data_glean,
        "prefix_glean": prefix_glean,
        "cache_guard": cache_guard,
        "tracking": tracking,
    }

    address_limits_dict = {
        "ipv4": ipv4_limit_address_count,
        "ipv6": ipv6_limit_address_count,
    }

    protocols = {
        "nd": neighbor_discovery,
        "dhcp6": dhcp6,
        "arp": arp,
        "dhcp4": dhcp4,
    }

    config_dict = dict(filter(lambda x: x[1] is not None, config_dict.items()))
    address_limits_dict = dict(filter(lambda x: x[1] is not None, address_limits_dict.items()))
    protocols = dict(filter(lambda x: x[1] is not None, protocols.items()))

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        output = device.parse('show device-tracking policy {policy}'.format(policy=policy_name))
        if output.get('configuration', None):
            target_configs = output['configuration']
            if not _verify_policy_configurations(target_configs, config_dict):
                return False

            if target_configs.get('limit_address_count', None):
                target_address_limit_configs = target_configs['limit_address_count']
                if not _verify_policy_configurations(target_address_limit_configs,
                                                     address_limits_dict):
                    return False

            for key, value in protocols.items():
                if target_configs[key]['is_gleaning'] != value:
                    log.info('{protocol} is expected to be {value}. Instead found {target_value}.'
                             .format(protocol=key, value=value, \
                                     target_value=target_configs[key]['is_gleaning']))
                    return False

        timeout.sleep()

    log.info('Configurations are correct')
    return True


def verify_missing_device_tracking_policy_configuration(device, policy_name, trusted_port=False,
                                                        data_glean=False, prefix_glean=False,
                                                        ipv4_limit_address_count=False,
                                                        ipv6_limit_address_count=False,
                                                        cache_guard=False, tracking=False,
                                                        max_time=1, check_interval=1):
    """ Verify missing device-tracking policy configurations
        Args:
            device('obj'): device object
            policy_name('str'): policy name
            trusted_port('bool', optional): trusted port. Defaults to False
            data_glean('bool', optional): data glean. Defaults to False
            prefix_glean('bool', optional): prefix glean. Defaults to False
            ipv4_limit_address_count('bool', optional): ipv4 address count limit. Defaults to False
            ipv6_limit_address_count('bool', optional): ipv6 address count limit. Defaults to False
            cache_guard('bool', optional): cache guard. Defaults to False
            tracking('bool', optional): tracking. Defaults to False
            max_time('int',optional): max check time. Defaults to 1
            check_interval('int',optional): check intervals. Defaults to 1
        Returns:
            True
            False
        Raises:
            None
    """
    config_dict = {
        "trusted_port": trusted_port,
        "data_glean": data_glean,
        "prefix_glean": prefix_glean,
        "cache_guard": cache_guard,
        "tracking": tracking,
    }

    address_limits_dict = {
        "ipv4": ipv4_limit_address_count,
        "ipv6": ipv6_limit_address_count,
    }

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        output = device.parse('show device-tracking policy {policy}'.format(policy=policy_name))
        if output['configuration']:
            target_configs = output['configuration']
            if not _verify_missing_policy_configurations(target_configs, config_dict):
                return False

            if target_configs.get('limit_address_count', None):
                target_address_limit_configs = target_configs['limit_address_count']
                if not _verify_missing_policy_configurations(target_address_limit_configs,
                                                             address_limits_dict):
                    return False

        timeout.sleep()

    log.info('Correct configurations are missing on target')
    return True


def verify_ip_mac_binding_not_in_network(device, macAddr, ipAddr=None, max_time=20, check_interval=10):
    """ Verify the ip-mac binding does not exist in the network

        Args:
            device('obj'): device object
            macAddr('str'): mac address (XXXX.XXXX.XXXX)
            ipAddr('str'): ip address
            max_time('int',optional): max check time. Defaults to 20
            check_interval('int', optional): check intervals. Defaults to 10
        Returns:
            Bool
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        output = device.parse('show device-tracking database')
        if not output['device']:
            log.debug("Binding table is empty")
            return True

        entries = output['device']

        for i in range(1, len(entries)+1):
            if entries[i]['link_layer_address'] == macAddr:
                if (not ipAddr or entries[i]['network_layer_address'] == ipAddr):
                    log.debug('Entry mac {} should not been found in target'.format(macAddr))
                    return False
        timeout.sleep()

    log.debug('Verified mac {} not in table'.format(macAddr))
    return True


def verify_ip_mac_binding_in_network(device, ipAddr, macAddr, origin,
                                     preflevel, clientid=None, max_time=60, check_interval=10):
    """ Verify the ip-mac binding is present on device

        Args:
            device('obj'): device object
            ipAddr('str'): ip address
            macAddr('str'): mac address (XXXX.XXXX.XXXX)
            origin('str'): binding table entry origin
            preflevel('int'): binding table entry preflevel
            clientid('str', optional): client mac address (aiming for dhcp entry). Defaults to None
            max_time('int', optional): max check time. Defaults to 60
            check_interval('int', optional): check intervals. Defaults to 10
        Returns:
            Bool
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        output = device.parse('show device-tracking database')
        if output:
            entries = output['device']
            for i in range(1, len(entries)+1):
                if entries[i]['dev_code'] == origin:
                    if entries[i]['network_layer_address'] == ipAddr and \
                       entries[i]['link_layer_address'] == macAddr and \
                       entries[i]['pref_level_code'] == preflevel:
                        log.debug('{} entry {} matching criteria found'.format(origin, ipAddr))
                        return True
        log.debug('Entry {} not found, retry in {}s...'.format(ipAddr, check_interval))
        timeout.sleep()

    log.debug('Entry {} still not found after {}s'.format(ipAddr, max_time))
    return False


def verify_ip_mac_binding_count(device, origin, expected, max_time=60, check_interval=10):

    """ Verify ip mac binding count in device tracking database

        Args:
            device('obj'): device object
            origin('str'): binding table entry origin
            expected('int'): expected number for specific type of entry
            max_time('int',optional): max check time. Defaults to 60
            check_interval('int',optional): check intervals. Defaults to 10
        Returns:
            Bool
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    count = 0
    while timeout.iterate():
        output = device.parse('show device-tracking database')
        if output['device']:
            entries = output['device']

            for i in range(1, len(entries)+1):
                if entries[i]['dev_code'] == origin:
                    count += 1

        if count == expected:
            log.debug('Sepcific {} entry number met the expected'.format(origin))
            return True
        timeout.sleep()

    log.debug('Sepcific {} entry number not met the expected'.format(origin))
    return False


def verify_empty_device_tracking_database(device, max_time=60, check_interval=10):

    """ Verify ip mac binding count in device tracking database

        Args:
            device('obj'): device object
            max_time('int',optional): max check time. Defaults to 60
            check_interval('int',optional): check intervals. Defaults to 10
        Returns:
            Bool
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    count = 0
    while timeout.iterate():
        try:
            output = device.parse("show device-tracking database")
        except SchemaEmptyParserError:
            return True
        timeout.sleep()

    log.debug('Device-tracking database is not empty:\n{}'.format(output))
    return False

def verify_ipv6_nd_raguard_policy(device, policy_name, vlan=None, iface=None,
                                  feature='Source guard', max_time=20, check_interval=10):
    """ Verify the ipv6 nd raguard policies
        Args:
            device('obj'): device object
            policy_name('str'): policy name
            vlan('str'): vlan target
            iface('str'): interface target
            feature('str', optional): sisf features. Defaults to "RA guard"
            max_time('int', optional): max check time. Defaults to 20
            check_interval('int', optional): check intervals. Defaults to 10
        Returns:
            True
            False
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        output = device.parse('show ipv6 nd raguard policy {policy}'.format(policy=policy_name))
        if _verify_ipv6_policy(output, policy_name, vlan, iface, feature):
            log.info('Target policy found on expected target')
            return True
        timeout.sleep()

    log.info('Target policy not found')
    return False


def verify_ipv6_nd_raguard_configuration(device, policy_name, trusted_port=None, device_role=None,
                                         max_hop_limit=None, min_hop_limit=None,
                                         managed_config_flag=None, other_config_flag=None,
                                         max_router_preference=None, match_ra_prefix=None,
                                         match_ipv6_access_list=None, max_time=20,
                                         check_interval=10):
    """ Verify ipv6 nd raguard configurations
        Args:
            device('obj'): device object
            policy_name('str'): policy name
            trusted_port('str', optional): trusted port (yes | no). Defaults to None
            device_role('str', optional): device role. Defaults to None
            max_hop_limit('int', optional): maximum hop limit. Defaults to None
            min_hop_limit('int', optional): minimum hop limit. Defaults to None
            managed_config_flag('str', optional): managed config flag (on | off). Defaults to None
            other_config_flag('str', optional): other config flag (on | off). Defaults to None
            max_router_preference('str', optional): maximum router preference. Defaults to None
            match_ra_prefix('str', optional): match ra prefix-list. Defaults to None
            match_ipv6_access_list('str', optional): match ipv6 access-list. Defaults to None
            max_time('int', optional): max check time. Defaults to 20
            check_interval('int', optional): check intervals. Defaults to 10
        Returns:
            True
            False
        Raises:
            None
    """
    config_dict = {
        "trusted_port": trusted_port,
        "device_role": device_role,
        "max_hop_limit": max_hop_limit,
        "min_hop_limit": min_hop_limit,
        "managed_config_flag": managed_config_flag,
        "other_config_flag": other_config_flag,
        "max_router_preference": max_router_preference,
        "match_ra_prefix": match_ra_prefix,
        "match_ipv6_access_list": match_ipv6_access_list,
    }

    config_dict = dict(filter(lambda x: x[1] is not None, config_dict.items()))

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        output = device.parse('show ipv6 nd raguard policy {policy}'.format(policy=policy_name))
        if output['configuration']:
            target_configs = output['configuration']
            if _verify_policy_configurations(target_configs, config_dict):
                log.info('Configurations are correct on target')
                return True
            else:
                return False
        timeout.sleep()

    log.info('Configurations cannot be found')
    return False


def verify_missing_ipv6_nd_raguard_configuration(device, policy_name, trusted_port=False,
                                                 max_hop_limit=False, min_hop_limit=False,
                                                 managed_config_flag=False, other_config_flag=False,
                                                 max_router_preference=False, match_ra_prefix=False,
                                                 match_ipv6_access_list=False, max_time=20,
                                                 check_interval=10):
    """ Verify missing ipv6 nd raguard configurations
        Args:
            device('obj'): device object
            policy_name('str'): policy name
            trusted_port('bool', optional): trusted port. Defaults to False
            max_hop_limit('bool', optional): maximum hop limit. Defaults to False
            min_hop_limit('bool', optional): minimum hop limit. Defaults to False
            managed_config_flag('bool', optional): managed config flag. Defaults to False
            other_config_flag('bool', optional): other config flag. Defaults to False
            max_router_preference('bool', optional): maximum router preference. Defaults to False
            match_ra_prefix('bool', optional): match ra prefix-list. Defaults to False
            match_ipv6_access_list('bool', optional): match ipv6 access-list. Defaults to False
            max_time('int', optional): max check time. Defaults to 20
            check_interval('int', optional): check intervals. Defaults to 10
        Returns:
            True
            False
        Raises:
            None
    """
    config_dict = {
        "trusted_port": trusted_port,
        "max_hop_limit": max_hop_limit,
        "min_hop_limit": min_hop_limit,
        "managed_config_flag": managed_config_flag,
        "other_config_flag": other_config_flag,
        "max_router_preference": max_router_preference,
        "match_ra_prefix": match_ra_prefix,
        "match_ipv6_access_list": match_ipv6_access_list,
    }

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        output = device.parse('show ipv6 nd raguard policy {policy}'.format(policy=policy_name))
        if output['configuration']:
            target_configs = output['configuration']
            if _verify_missing_policy_configurations(target_configs, config_dict):
                log.info('Correct configurations are missing on target')
                return True
            else:
                return False
        timeout.sleep()

    return False


def verify_ipv6_source_guard_policy(device, policy_name, vlan=None, iface=None,
                                    feature='Source guard', max_time=20, check_interval=10):
    """ Verify the ipv6 source guard policies
        Args:
            device('obj'): device object
            policy_name('str'): policy name
            vlan('str'): vlan target
            iface('str'): interface target
            feature('str'): sisf features. Defaults to "Source guard"
            max_time('int', optional): max check time. Defaults to 20
            check_interval('int', optional): check intervals. Defaults to 10
        Returns:
            True
            False
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        output = device.parse('show ipv6 source-guard policy {policy}'.format(policy=policy_name))
        if _verify_ipv6_policy(output, policy_name, vlan, iface, feature):
            log.info('Target policy found on expected target')
            return True
        timeout.sleep()

    log.info('Target policy not found')
    return False


def verify_ipv6_source_guard_configuration(device, policy_name, trusted=None,
                                           validate_address=None, validate_prefix=None,
                                           permit=None, deny=None, max_time=20,
                                           check_interval=10):
    """ Verify ipv6 source guard configurations
        Args:
            device('obj'): device object
            policy_name('str'): policy name
            trusted_port('str', optional): trusted port (yes | no). Defaults to None
            validate_address('str', optional): validate address (yes | no). Defaults to None
            validate_prefix('str', optional): validate prefix (yes | no). Defaults to None
            permit('str', optional): permit traffic. Defaults to None
            deny('str', optional): deny traffic. Defaults to None
            max_time('int', optional): max check time. Defaults to 20
            check_interval('int', optional): check intervals. Defaults to 10
        Returns:
            True
            False
        Raises:
            None
    """
    config_dict = {
        "trusted": trusted,
        "validate_address": validate_address,
        "validate_prefix": validate_prefix,
        "permit": permit,
        "deny": deny,
    }

    config_dict = dict(filter(lambda x: x[1] is not None, config_dict.items()))

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        output = device.parse('show ipv6 source-guard policy {policy}'.format(policy=policy_name))
        if output['configuration']:
            target_configs = output['configuration']
            if _verify_policy_configurations(target_configs, config_dict):
                log.info('Configurations are correct on target')
                return True
            else:
                return False
        timeout.sleep()

    log.info('Configurations cannot be found')
    return False


def verify_missing_ipv6_source_guard_configuration(device, policy_name, trusted=False,
                                                   validate_prefix=False, permit=False,
                                                   deny=False, max_time=20,
                                                   check_interval=10):
    """ Verify missing ipv6 source guard configurations
        Args:
            device('obj'): device object
            policy_name('str'): policy name
            trusted_port('bool', optional): trusted port. Defaults to False
            validate_prefix('bool', optional): validate prefix. Defaults to False
            permit('bool', optional): permit traffic. Defaults to False
            deny('bool', optional): deny traffic. Defaults to False
            max_time('int', optional): max check time. Defaults to 20
            check_interval('int', optional): check intervals. Defaults to 10
        Returns:
            True
            False
        Raises:
            None
    """
    config_dict = {
        "trusted": trusted,
        "validate_prefix": validate_prefix,
        "permit": permit,
        "deny": deny,
    }

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        output = device.parse('show ipv6 source-guard policy {policy}'.format(policy=policy_name))
        if output['configuration']:
            target_configs = output['configuration']
            if _verify_missing_policy_configurations(target_configs, config_dict):
                log.info('Correct configurations are missing on target')
                return True
            else:
                return False
        timeout.sleep()

    return False


def verify_device_tracking_counters_vlan(device, vlanid, message_type, protocol, message,
                                         count, max_time=20, check_interval=10):
    """ Verify missing ipv6 source guard configurations
        Args:
            device('obj'): device object
            vlanid('str'): vlan id
            message_type('str'): message type - can be one of [received, received_broadcast_multicast, bridged, broadcast_multicast_to_unicast, limited_broadcast_to_local]
            protocol('str'): protocol
            message('str'): message type
            count('int'): number of packets
            max_time('int', optional): max check time. Defaults to 20
            check_interval('int', optional): check intervals. Defaults to 10
        Returns:
            True
            False

        Raises:
            None
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        output = device.parse('show device-tracking counters vlan {vlanid}'.format(vlanid=vlanid))
        query = output.q.contains(int(vlanid)).contains(message_type) \
                        .contains(protocol).get_values(message)
        if query:
            message_count = query[0]
            if message_count == count:
                return True
            else:
                log.info('Expected count: {count}. Instead got count: {target_count}.'.format(
                         count=count, target_count=message_count))
                return False
        timeout.sleep()

    log.info('Packet is not found in the counters. Looking for arguments - ' \
             'vlanid: "{vlanid}", message_type: "{message_type}", protcol: "{protocol}" ' \
             'message: "{message}", count: "{count}" in parsed dictionary: {output}' \
             .format(vlanid=vlanid, message_type=message_type, protocol=protocol,
                     message=message, count=count, output=output))
    return False


def verify_device_tracking_counters_vlan_dropped(device, vlanid, feature, protocol, message,
                                                 num_dropped, max_time=20, check_interval=10):
    """ Verify missing ipv6 source guard configurations
        Args:
            device('obj'): device object
            vlanid('str'): vlan id
            feature('str'): feature
            protocol('str'): protocol
            message('str'): message type
            num_dropped('int'): number of dropped packets
            max_time('int', optional): max check time. Defaults to 20
            check_interval('int', optional): check intervals. Defaults to 10
        Returns:
            True
            False
        Raises:
            None
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        output = device.parse('show device-tracking counters vlan {vlanid}'.format(vlanid=vlanid))
        dropped = output.get('vlanid', {}).get(int(vlanid), {}) \
                        .get('dropped', {}).get(feature, {})
        if dropped:
            if dropped['protocol'] == protocol and dropped['message'] == message and \
               dropped['dropped'] == num_dropped:
                return True
            else:
                log.info('Expected protocol: {protocol}, message: {message}, dropped: {dropped}. '
                         'Instead got protocol: {target_protocol}, message: {target_message}, '
                         'dropped: {target_dropped}.'.format(
                                protocol=protocol, message=message, dropped=num_dropped,
                                target_protocol=dropped['protocol'],target_message=dropped['message'],
                                target_dropped=dropped['dropped']))
                return False
        timeout.sleep()

    log.info('Dropped message type cannot be found')
    return False


def verify_device_tracking_counters_vlan_faults(device, vlanid, faults,
                                                max_time=10, check_interval=5):
    """ Verify missing ipv6 source guard configurations
        Args:
            device('obj'): device object
            vlanid('str'): vlan id
            faults('list('str')'): list of faults
            max_time('int', optional): max check time. Defaults to 10
            check_interval('int', optional): check intervals. Defaults to 5
        Returns:
            True
            False
        Raises:
            None
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        output = device.parse('show device-tracking counters vlan {vlanid}'.format(vlanid=vlanid))
        target_faults = output.get('vlanid', {}).get(int(vlanid), {}).get("faults", [])
        if faults:
            if target_faults:
                for fault in faults:
                    if fault not in target_faults:
                        log.info('Fault {fault} is not found on the target'.format(fault=fault))
                        return False
            else:
                log.info('Expected faults, but there are none the target')
                return False
        else:
            if target_faults:
                log.info('Expected no faults, but there are faults the target')
                return False
            else:
                log.info('There are no faults the target as expected')
                return True
        timeout.sleep()

    log.info('The correct faults are found on the target'.format(fault=fault))
    return True


def verify_device_tracking_counters_interface(device, interface, message_type, protocol, message,
                                              count, max_time=20, check_interval=10):
    """ Verify missing ipv6 source guard configurations
        Args:
            device('obj'): device object
            interface('str'): interface name
            message_type('str'): message type - can be one of [received, received_broadcast_multicast, bridged, broadcast_multicast_to_unicast, limited_broadcast_to_local]
            protocol('str'): protocol
            message('str'): message type
            count('int'): number of packets
            max_time('int', optional): max check time. Defaults to 20
            check_interval('int', optional): check intervals. Defaults to 10
        Returns:
            True
            False

        Raises:
            None
    """

    interface = Common.convert_intf_name(interface.capitalize())
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        output = device.parse('show device-tracking counters interface {interface}'.format(interface=interface))
        query = output.q.contains(interface).contains(message_type) \
                        .contains(protocol).get_values(message)
        if query:
            message_count = query[0]
            if message_count == count:
                return True
            else:
                log.info('Expected count: {count}. Instead got count: {target_count}.'.format(
                         count=count, target_count=message_count))
                return False
        timeout.sleep()

    log.info('Packet is not found in the counters. Looking for arguments - ' \
             'interface: "{interface}", message_type: "{message_type}", protcol: "{protocol}" ' \
             'message: "{message}", count: "{count}" in parsed dictionary: {output}' \
             .format(interface=interface, message_type=message_type, protocol=protocol,
                     message=message, count=count, output=output))
    return False