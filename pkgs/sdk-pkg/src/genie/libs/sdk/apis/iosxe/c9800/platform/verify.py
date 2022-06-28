import logging
from genie.utils.timeout import Timeout
import re

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
