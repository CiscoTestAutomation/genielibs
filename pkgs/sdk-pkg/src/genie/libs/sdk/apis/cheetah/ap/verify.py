import logging

log = logging.getLogger(__name__)


def verify_operation_state(device, operation_state):
    """Verify the AP operation state once.

    Args:
        device (obj): AP device object.
        operation_state (str): Expected AP operation state.

    Returns:
        bool: True when the expected state is observed; otherwise False.
    """
    return operation_state == device.api.get_operation_state()


def verify_controller_name(device, controller_name):
    """Verify the controller name once.

    Args:
        device (obj): AP device object.
        controller_name (str): Expected wireless-controller name.

    Returns:
        bool: True when the expected controller is observed; otherwise False.
    """
    return controller_name == device.api.get_controller_name()


def verify_controller_ip(device, controller_ip_address):
    """Verify the controller address once.

    Args:
        device (obj): AP device object.
        controller_ip_address (str): Expected controller IP address.

    Returns:
        bool: True when the expected address is observed; otherwise False.
    """
    return controller_ip_address == device.api.get_ip_address()
