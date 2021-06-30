"""Common verification functions for sisf"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout

log = logging.getLogger(__name__)


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
        output = device.parser('show device-tracking database')
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
