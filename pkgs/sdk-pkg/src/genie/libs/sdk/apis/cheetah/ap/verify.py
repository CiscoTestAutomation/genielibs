import logging
from genie.utils.timeout import Timeout

log = logging.getLogger(__name__)


def verify_operation_state(device, operation_state, max_time=100, check_interval=10):
    """Verify the operation state of devcie
        Args:
            device (obj): Device object
            operation_state (str): Operation state of device
            max_time (int, optional): Maximum time in seconds. Defaults to 100
            check_interval (int, optional): check interval in seconds. Defaults to 10

        Returns:
            True - if the expected Operation is seen
            False - if the expected Operation is NOT seen

        Raises:
            N/A

        """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if operation_state == device.api.get_operation_state():
            return True
        timeout.sleep()

    return False


def verify_controller_name(device, controller_name, max_time=100, check_interval=10):
    """Verify the controller name to which device is associated
        Args:
            device (obj): Device object
            controller_name (str): Name of the wireless controller
            max_time (int, optional): Maximum time in seconds. Defaults to 100
            check_interval (int, optional): check interval in seconds. Defaults to 10

        Returns:
            True - if the device is associated to expected controller
            False - if the device is not associated to expected controller

        Raises:
            N/A

        """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if controller_name == device.api.get_controller_name():
            return True
        timeout.sleep()

    return False


def verify_controller_ip(device, controller_ip_address, max_time=100, check_interval=10):
    """Verify the controller name to which device is associated
        Args:
            device (obj): Device object
            controller_ip_address (str): IP/IPv6 of the wireless controller
            max_time (int, optional): Maximum time in seconds. Defaults to 100
            check_interval (int, optional): check interval in seconds. Defaults to 10

        Returns:
            True - if the device is associated to expected controller IP/Ipv6 address
            False - if the device is not associated to expected controller IP/Ipv6 address

        Raises:
            N/A

        """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if controller_ip_address == device.api.get_ip_address():
            return True
        timeout.sleep()

    return False
