'''Common verify functions for interface'''
# Python
import logging
from ipaddress import IPv4Interface

# Genie
from genie.utils.timeout import Timeout
from genie.utils import Dq
from genie.metaparser.util.exceptions import SchemaEmptyParserError

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


def verify_interface_state_up(
    device, interface, max_time=60, check_interval=10
):
    """Verify interface state is up and and line protocol is up

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            max_time (`int`): max time
            check_interval (`int`): check interval
        Returns:
            result(`bool`): True if is up else False
    """

    return verify_interface_in_state(device, interface, verify_ip=False, max_time=max_time, check_interval=check_interval)


def verify_interface_errors(device,
                            interface,
                            expected_value=None,
                            input=False,
                            output=False,
                            max_time=30,
                            check_interval=10):
    """ Verify interface input and output errors

        Args:
            device (`obj`): Device object
            interface (`str`): Pass interface in show command
            expected_value (`int`, Optional): Expected errors values. Defaults to None
            input (`bool`, Optional): True if input errors to verify. Default to False.
            output (`bool`, Optional): True if output errors to verify. Default to False.
            max_time (`int`, Optional): Max time, default: 60 seconds
            check_interval (`int`, Optional): Check interval, default: 10 seconds

        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            cmd = 'show interface {interface}'.format(
                interface=interface)
            out = device.parse(cmd)
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        interface, data = next(iter(out.items()))
        data = Dq(data)
        if input and output:
            input_errors = data.get_values("in_errors", 0)
            output_errors = data.get_values("out_errors", 0)
            if input_errors == output_errors == expected_value:
                return True
        elif input:
            input_errors = data.get_values("in_errors", 0)
            if input_errors == expected_value:
                return True
        elif output:
            output_errors = data.get_values("out_errors", 0)
            if output_errors == expected_value:
                return True

        timeout.sleep()
        continue

    return False

def verify_interface_state_admin_down(
    device, interface, max_time=60, check_interval=10
):
    """Verify interface state is administratively down and line protocol is down

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            max_time (`int`): max time
            check_interval (`int`): check interval
        Returns:
            result(`bool`): True if is up else False
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            cmd = 'show interface {interface}'.format(
                interface=interface)
            out = device.parse(cmd)
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Any(): {
        #     'oper_status': str,
        #     Optional('line_protocol'): str,

        oper_status = out.q.get_values("oper_status", 0)
        line_protocol = out.q.get_values("line_protocol", 0)
        enabled = out.q.get_values("enabled", 0)
        if oper_status == line_protocol == "down" and enabled == False:
            return True
        timeout.sleep()

    return False

def verify_interface_state_down(
    device, interface, max_time=60, check_interval=10
):
    """Verify interface state is down and line protocol is down

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            max_time (`int`): max time
            check_interval (`int`): check interval
        Returns:
            result(`bool`): True if is up else False
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            cmd = 'show interface {interface}'.format(
                interface=interface)
            out = device.parse(cmd)
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Any(): {
        #     'oper_status': str,
        #     Optional('line_protocol'): str,

        oper_status = out.q.get_values("oper_status", 0)
        line_protocol = out.q.get_values("line_protocol", 0)
        enabled = out.q.get_values("enabled", 0)
        if oper_status == line_protocol == "down" and enabled:
            return True
        timeout.sleep()

    return False

def verify_interface_state_admin_up(
    device, interface, max_time=60, check_interval=10
):
    """Verify interface state is administratively up and line protocol is up

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            max_time (`int`): max time
            check_interval (`int`): check interval
        Returns:
            result(`bool`): True if is up else False
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            cmd = 'show interface {interface}'.format(
                interface=interface)
            out = device.parse(cmd)
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        
        # Any(): {
        #     'oper_status': str,
        #     Optional('line_protocol'): str,

        oper_status = out.q.get_values("oper_status", 0)
        line_protocol = out.q.get_values("line_protocol", 0)
        enabled = out.q.get_values("enabled", 0)
        if oper_status == line_protocol == "up" and enabled:
            return True
        timeout.sleep()

    return False
