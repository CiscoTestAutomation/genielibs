'''Common verify functions for interface'''
# Python
import logging
from ipaddress import IPv4Interface

# Genie
from genie.utils.timeout import Timeout

log = logging.getLogger(__name__)


def verify_bundle_in_state(device, bundle, interface, status='up', link_state='active', 
                           max_time=60, check_interval=20):
    ''' Verify bundle state

        Args:
            device (`obj`): Device object
            bundle (`str`): Bundle name
            interface (`bool`): Bundle interface
            status (`str`): Expected bundle status
            link_state (`str`): Expected line state
            max_time (`int`): Max time
            check_interval (`int`): Check interval
        Returns:
            result (`bool`): Verified result
    '''
    cmd = 'show bundle {}'.format(bundle)
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse(cmd)
        except Exception as e:
            log.error("Failed to parse '{}':\n{}".format(cmd, e))
            timeout.sleep()
            continue

        oper_status = out.get('interfaces', {}).get(bundle, {})\
                        .get('oper_status', '').lower()

        ls = out.get('interfaces', {}).get(bundle, {}).get('port', {}).get(interface, {})\
                .get('link_state', '').lower()

        log.info("Bundle {} status is {}, expected value is {}"
            .format(bundle, oper_status, status))

        log.info("Interface {} link state is {}, expected value is {}"
            .format(interface, ls, link_state))

        if oper_status == status.lower() and ls == link_state.lower():
            return True
        
        timeout.sleep()
    
    return False


def verify_interface_in_state(device, interface, verify_status=True, oper_status='up', 
                              line_protocol='up', verify_ip=True, ip='', subnet='', 
                              max_time=60, check_interval=20):
    ''' Verify interface state and ip

        Args:
            device (`obj`): Device object
            interface (`str`): Interfaces name
            verify_status (`bool`): To verify interface status
            oper_status (`str`): Expected oper status
            line_protocol (`str`): Expected line protocol status
            verify_ip (`bool`): To verify interface ip
            ip (`str`): Expected interface ip
            subnet (`str`): Expected interface ip subnet
            max_time (`int`): Max time
            check_interval (`int`): Check interval
        Returns:
            result (`bool`): Verified result
    '''
    cmd = 'show interfaces {}'.format(interface)
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse(cmd)
        except Exception as e:
            log.error("Failed to parse '{}':\n{}".format(cmd, e))
            timeout.sleep()
            continue
            
        result = True
        if verify_status:
            oper_status_v = out.get(interface, {}).get('oper_status', '').lower()
            line_protocol_v = out.get(interface, {}).get('line_protocol', '').lower()

            log.info("Interface {} status is {}, expected value is {}"
                .format(interface, oper_status_v, oper_status))
            log.info("Interface {} line protocol is {}, expected value is {}"
                .format(interface, line_protocol_v, line_protocol))

            if (oper_status_v != oper_status.lower() or 
                line_protocol_v != line_protocol.lower()):
                result = False

        if verify_ip:
            ipaddr = out.get(interface, {}).get('ipv4', {}).keys()
            if ipaddr:
                ipv4 = IPv4Interface(list(ipaddr)[0])
            else:
                log.error("Interface {} doesn't have ipv4 address".format(interface))
                timeout.sleep()
                continue

            log.info("Interface {} IP is {}, expected value is {}"
                .format(interface, ipv4.ip, ip))
            if str(ipv4.ip) != ip:
                result = False

            if subnet:
                log.info("Interface {} IP netmask is {}, expected value is {}"
                    .format(interface, ipv4.netmask, subnet))
                if str(ipv4.netmask) != subnet:
                    result = False

        if result:
            return True

        timeout.sleep()

    return False
