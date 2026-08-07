"""Common verify functions for hw_module"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout

log = logging.getLogger(__name__)


def verify_show_hw_module_subslot_oir(
        device, subslot, expected_oir_status, max_time=300,
        check_interval=5):
    """Verify OIR status in show hw-module subslot output for a subslot

    Args:
        device ('obj'): device object
        subslot ('str'): subslot name
        expected_oir_status ('str'): expected OIR status
        max_time ('int'): max time to wait
        check_interval ('int'): interval time to check
    Returns:
        result ('bool'): True/False
    """
    timeout = Timeout(max_time=max_time, interval=check_interval)
    get_oir_status = None
    while timeout.iterate():
        res = device.api.get_hw_module_subslot_oir(subslot=subslot)
        if res is None:
            timeout.sleep()
            continue
        get_oir_status = res.get('subslots', {}).get(subslot, {}).\
            get('operational_status')
        if expected_oir_status == get_oir_status:
            return True
        else:
            timeout.sleep()
    else:
        return False


def verify_platform_hardware_subslot_module_interface_status_mac_learning(
        device, subslot, interface, learning_mode, learning_state=None,
        forward_action=None, notify_to_cpu=None):
    """Verify MAC learning status for a subslot interface

    Args:
        device ('obj'): device object
        subslot ('str'): subslot name
        interface ('str'): interface name
        learning_mode ('str'): expected learning mode
        learning_state ('str', optional): expected learning state
        forward_action ('str', optional): expected forward action
        notify_to_cpu ('str', optional): expected notify to cpu
    Returns:
        result ('bool'): True/False
    """
    def __dict_compare(expect, actual):
        for k in expect:
            if k in actual:
                if isinstance(expect[k], dict) and \
                        isinstance(actual[k], dict):
                    if not __dict_compare(expect[k], actual[k]):
                        return False
                elif isinstance(expect[k], list) and \
                        isinstance(actual[k], list):
                    for element in expect[k]:
                        if element not in actual[k]:
                            return False
                elif expect[k] != actual[k]:
                    log.debug(f"{k} mismatch: expected {expect[k]}, "
                              f"actual {actual[k]}")
                    return False
            else:
                log.debug(f"{k} does not exist, expect {expect[k]}")
                return False
        return True

    expected_learning = {"learning_mode": learning_mode}
    if learning_state is not None:
        expected_learning["learning_state"] = learning_state
    if forward_action is not None:
        expected_learning["forward_action"] = forward_action
    if notify_to_cpu is not None:
        expected_learning["notify_to_cpu"] = notify_to_cpu

    res = device.api.\
        get_platform_hardware_subslot_module_interface_status(
            subslot=subslot, interface=interface)
    if res is None:
        return False
    actual_learning = res.get('mac_learning', {})
    if __dict_compare(expected_learning, actual_learning):
        return True
    else:
        return False
