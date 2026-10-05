import logging
import re

from genie.metaparser.util.exceptions import (
    SchemaEmptyParserError,
    SchemaMissingKeyError,
    SchemaUnsupportedKeyError,
)
from genie.utils.timeout import Timeout
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def verify_wireless_management_trustpoint_name(device, trustpoint_name, max_time=60, check_interval=10):
    """Verify the given trustpoint has configured
    Args:
        device (obj): Device object
        trustpoint_name (str): trustpoint name
        max_time (int, optional): Maximum time in seconds. Defaults to 60
        check_interval (int, optional): check interval in seconds. Defaults to 10

    Returns:
        True - if the expected trustpoint is configured
        False - if the expected trustpoint is NOT configured

    Raises:
        N/A

    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if trustpoint_name == device.api.get_wireless_management_trustpoint_name():
            return True
        timeout.sleep()

    return False


def verify_pki_trustpoint_state(device, trustpoint_name, max_time=60, check_interval=10):
    """Verify the pki state  has configured
    Args:
        device (obj): Device object
        trustpoint_name (str): trustpoint name
        max_time (int, optional): Maximum time. Defaults to 60
        check_interval (int, optional): check interval. Defaults to 10

    Returns:
        True - if the values of keys_generated, issuing_ca_authenticated, certificate_requests are "yes"
        False - if the values of keys_generated, issuing_ca_authenticated, certificate_requests are other then "yes"

    Raises:
        None

    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        pki_trustpoint_state = device.api.get_pki_trustpoint_state(
            trustpoint_name=trustpoint_name)
        if (pki_trustpoint_state['keys_generated'] == pki_trustpoint_state['issuing_ca_authenticated'] ==
                pki_trustpoint_state['certificate_requests'] == "yes"):
            return True
        timeout.sleep()

    return False

def verify_tx_power(device, ap_name, tx_power, max_time=60, check_interval=10):
    """Verify the given tx power has configured
    Args:
        device (obj): Device object
        tp_name (str): trustpoint name
        tx_power (str): transmit power 
        max_time (int, optional): Maximum time in seconds. Defaults to 60
        check_interval (int, optional): check interval in seconds. Defaults to 10

    Returns:
        True - if the expected trustpoint is configured
        False - if the expected trustpoint is NOT configured

    Raises:
        N/A

    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        tx_power_fetch = device.api.get_tx_power(ap_name)
        if tx_power == re.search(r'\d+', tx_power_fetch).group(): 
            return True
        timeout.sleep()

    return False

def verify_unused_channel(device, unused_channel_lst, max_time=60, check_interval=10):
    """Verify the given un used channel list 
    Args:
        device (obj): Device object
        unused_channel_lst (list): un used channel list
        max_time (int, optional): Maximum time in seconds. Defaults to 60
        check_interval (int, optional): check interval in seconds. Defaults to 10

    Returns:
        True - if the expected un used channel list is configured
        False - if the expected un used channel list is NOT configured

    Raises:
        N/A

    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        unused_channel_lst_fetch = device.api.get_unused_channel()
        if(set(unused_channel_lst).issubset(set(unused_channel_lst_fetch))):
            return True
        timeout.sleep()

    return False


def verify_assignment_mode(device, assignment_mode, max_time=60, check_interval=10):
    """Verify the given assignment mode 
    Args:
        device (obj): Device object
        assignment_mode (str): configured assignment mode 
        max_time (int, optional): Maximum time in seconds. Defaults to 60
        check_interval (int, optional): check interval in seconds. Defaults to 10

    Returns:
        True - if the expected assignment mode is configured
        False - if the expected assignment mode is NOT configured

    Raises:
        N/A

    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if assignment_mode == device.api.get_assignment_mode():
            return True
        timeout.sleep()

    return False


def verify_ap_mode(device, access_points, ap_mode='local', max_time=600,
                   check_interval=10):
    """Verify the operating mode of each specified access point.

    Args:
        device (obj): Device object.
        access_points (list[str]): Access point names to verify.
        ap_mode (str, optional): Expected AP mode. Defaults to ``local``.
        max_time (int, optional): Maximum time in seconds for each AP.
            Defaults to 600.
        check_interval (int, optional): Time in seconds between checks.
            Defaults to 10.

    Returns:
        bool: ``True`` if every AP uses the expected mode, otherwise
            ``False``.
    """
    for ap_name in access_points:
        timeout = Timeout(max_time, check_interval)
        while timeout.iterate():
            actual_mode = device.api.get_ap_mode(ap_name)
            if not actual_mode:
                log.warning(
                    "Access point '%s' is not registered; retrying in %s "
                    "seconds", ap_name, check_interval)
                timeout.sleep()
                continue

            if actual_mode.lower() == ap_mode.lower():
                break

            log.error(
                "Access point '%s' mode '%s' does not match expected mode "
                "'%s'", ap_name, actual_mode, ap_mode)
            return False
        else:
            log.error(
                "Access point '%s' did not register within %s seconds",
                ap_name, max_time)
            return False

    return True


def verify_installation_mode(device, installation_mode='INSTALL'):
    """Verify the configured wireless installation mode.

    Args:
        device (obj): Device object.
        installation_mode (str, optional): Expected installation mode.
            Defaults to ``INSTALL``.

    Returns:
        bool: ``True`` if the installation mode matches, otherwise ``False``.
    """
    actual_mode = device.api.get_installation_mode()
    if (isinstance(actual_mode, str) and
            actual_mode.lower() == installation_mode.lower()):
        return True

    log.error(
        "Installation mode '%s' does not match expected mode '%s'",
        actual_mode, installation_mode)
    return False


def verify_ha_state(device, max_time=900, check_interval=30):
    """Verify that the HA peer is hot standby and its chassis is ready.

    Args:
        device (obj): Device object.
        max_time (int, optional): Maximum time in seconds for each HA check.
            Defaults to 900.
        check_interval (int, optional): Time in seconds between checks.
            Defaults to 30.

    Returns:
        bool: ``True`` if both redundancy and chassis checks pass, otherwise
            ``False``.
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            redundancy = device.parse('show redundancy states')
        except (SchemaEmptyParserError, SchemaMissingKeyError,
                SchemaUnsupportedKeyError, SubCommandFailure) as error:
            log.error("Failed to parse 'show redundancy states': %s", error)
            return False

        peer_state = redundancy.get('peer_state', '')
        if peer_state and 'STANDBY HOT' in peer_state:
            break

        log.warning(
            "HA peer is not in STANDBY HOT state; retrying in %s seconds",
            check_interval)
        timeout.sleep()
    else:
        log.error(
            'HA peer did not reach STANDBY HOT within %s seconds', max_time)
        return False

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            chassis = device.parse('show chassis')
        except (SchemaEmptyParserError, SchemaMissingKeyError,
                SchemaUnsupportedKeyError, SubCommandFailure) as error:
            log.error("Failed to parse 'show chassis': %s", error)
            return False

        chassis_entries = chassis.get('chassis_index', {}).values()
        if any(
            entry.get('role') == 'Standby' and
            entry.get('current_state') == 'Ready'
            for entry in chassis_entries
        ):
            return True

        log.warning(
            "Standby chassis is not ready; retrying in %s seconds",
            check_interval)
        timeout.sleep()

    log.error('Standby chassis did not become ready within %s seconds',
              max_time)
    return False


def verify_ap_fabric_summary(device, ap_list, max_time=600,
                             check_interval=10):
    """Verify that all specified access points are registered.

    Args:
        device (obj): Device object.
        ap_list (list[str]): Access point names to verify.
        max_time (int, optional): Maximum time in seconds for each access
            point. Defaults to 600.
        check_interval (int, optional): Time in seconds between checks.
            Defaults to 10.

    Returns:
        bool: ``True`` if every access point is registered, otherwise
            ``False``.
    """
    for ap_name in ap_list:
        timeout = Timeout(max_time, check_interval)
        while timeout.iterate():
            fabric_ap_state = device.api.get_fabric_ap_state(ap_name)
            if (isinstance(fabric_ap_state, str) and
                    fabric_ap_state.lower() == 'registered'):
                break

            log.warning(
                "Access point '%s' is not registered; retrying in %s "
                "seconds", ap_name, check_interval)
            timeout.sleep()
        else:
            log.error(
                "Access point '%s' did not register within %s seconds",
                ap_name, max_time)
            return False

    return True


def verify_access_tunnel_summary(device, ap_name, ap_ip, rloc_ip,
                                 max_time=600, check_interval=10):
    """Verify the AP and RLOC addresses in the access tunnel summary.

    Args:
        device (obj): Device object.
        ap_name (str): Access point name.
        ap_ip (str): Expected access point IP address.
        rloc_ip (str): Expected RLOC IP address.
        max_time (int, optional): Maximum time in seconds. Defaults to 600.
        check_interval (int, optional): Time in seconds between checks.
            Defaults to 10.

    Returns:
        bool: ``True`` if both addresses match, otherwise ``False``.
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        actual_ap_ip = device.api.get_ap_ip(ap_name)
        actual_rloc_ip = device.api.get_rloc_ip(ap_name)

        if actual_ap_ip == ap_ip and actual_rloc_ip == rloc_ip:
            return True

        log.warning(
            "Access tunnel for AP '%s' does not match yet: expected AP IP "
            "'%s' and RLOC IP '%s', received AP IP '%s' and RLOC IP '%s'; "
            "retrying in %s seconds",
            ap_name, ap_ip, rloc_ip, actual_ap_ip, actual_rloc_ip,
            check_interval)
        timeout.sleep()

    log.error(
        "Access tunnel for AP '%s' did not match within %s seconds",
        ap_name, max_time)
    return False


def verify_wireless_process(device, check_processes, max_time=600,
                            check_interval=10):
    """Verify that all specified wireless processes are running.

    Args:
        device (obj): Device object.
        check_processes (list[str]): Wireless process names to verify.
        max_time (int, optional): Maximum time in seconds for each process.
            Defaults to 600.
        check_interval (int, optional): Time in seconds between checks.
            Defaults to 10.

    Returns:
        bool: ``True`` if every process is running, otherwise ``False``.
    """
    for process in check_processes:
        timeout = Timeout(max_time, check_interval)
        while timeout.iterate():
            platform_matches = (
                device.api.get_matching_line_processes_platform(process))
            if not platform_matches or int(platform_matches) < 1:
                log.warning(
                    "Process '%s' is not present in processes platform; "
                    "retrying in %s seconds", process, check_interval)
                timeout.sleep()
                continue

            if not device.api.get_processes_platform_dict(process):
                log.warning(
                    "Process '%s' is not running in processes platform; "
                    "retrying in %s seconds", process, check_interval)
                timeout.sleep()
                continue

            software_matches = (
                device.api.get_matching_line_platform_software(process))
            if not software_matches or int(software_matches) < 1:
                log.warning(
                    "Process '%s' is not present in platform software; "
                    "retrying in %s seconds", process, check_interval)
                timeout.sleep()
                continue

            if device.api.get_platform_software_dict(process):
                break

            log.warning(
                "Process '%s' is not running on the standby member; "
                "retrying in %s seconds", process, check_interval)
            timeout.sleep()
        else:
            log.error(
                "Process '%s' did not come up within %s seconds",
                process, max_time)
            return False

    return True
