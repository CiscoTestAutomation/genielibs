"""Common configure functions for l2 qos"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_wrr_queue_bandwidth(device, bandwidth=None):
    """
    Configure WRR queue bandwidth on the device.
    Args:
        device ('obj'): Device object
        bandwidth ('list'): Bandwidth value, bandwidth should be specified
                            if device's weight is configurable
    Returns:
        None
    Raises:
        SubCommandFailure
    """

    if bandwidth:
        cmd = f"wrr-queue bandwidth {' '.join(map(str, bandwidth))}"
    else:
        cmd = "wrr-queue bandwidth"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure WRR queue bandwidth {bandwidth} "
            f"on the device, Error: {e}")


def unconfigure_wrr_queue_bandwidth(device):
    """
    Unconfigure WRR queue bandwidth on the device.
    Args:
        device ('obj'): Device object
    Returns:
        None
    Raises:
        SubCommandFailure
    """

    cmd = "no wrr-queue bandwidth"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure WRR queue bandwidth on the device, "
            f"Error: {e}")


def configure_wrr_queue_cos_map(device, queue_id, cos_list):
    """
    Configure WRR queue cos map on the device.
    Args:
        device ('obj'): Device object
        queue_id ('int'): Queue ID, 1..8
        cos_list ('list'): List of CoS values, 0..7
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"wrr-queue cos-map {queue_id} {' '.join(map(str, cos_list))}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure WRR queue cos map on the device, "
            f"Error: {e}")


def unconfigure_wrr_queue_cos_map(device):
    """
    Unconfigure WRR queue cos map on the device.
    Args:
        device ('obj'): Device object
    Returns:
        None
    Raises:
        SubCommandFailure
    """

    cmd = "no wrr-queue cos-map"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure WRR queue cos map on the device, "
            f"Error: {e}")


def configure_interface_switchport_priority_default(
        device, interface, priority):
    """
    Configure interface switchport priority default on the device.
    Args:
        device ('obj'): Device object
        interface ('str'): Interface name
        priority ('int'): Priority value, 0..7
    Returns:
        None
    Raises:
        SubCommandFailure
    """

    cmd = [f"interface {interface}",
           f"switchport priority default {priority}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure switchport priority default on '
            f'{interface}. Error: {e}')


def unconfigure_interface_switchport_priority_default(device, interface):
    """
    Unconfigure interface switchport priority default on the device.
    Args:
        device ('obj'): Device object
        interface ('str'): Interface name
    Returns:
        None
    Raises:
        SubCommandFailure
    """

    cmd = [f"interface {interface}",
           "no switchport priority default"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not unconfigure switchport priority default on '
            f'{interface}. Error: {e}')


def configure_interface_switchport_priority_override(device, interface):
    """
    Configure interface switchport priority override on the device.
    Args:
        device ('obj'): Device object
        interface ('str'): Interface name
    Returns:
        None
    Raises:
        SubCommandFailure
    """

    cmd = [f"interface {interface}",
           "switchport priority override"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure switchport priority override on '
            f'{interface}. Error: {e}')


def unconfigure_interface_switchport_priority_override(device, interface):
    """
    Unconfigure interface switchport priority override on the device.
    Args:
        device ('obj'): Device object
        interface ('str'): Interface name
    Returns:
        None
    Raises:
        SubCommandFailure
    """

    cmd = [f"interface {interface}",
           "no switchport priority override"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not unconfigure switchport priority override on '
            f'{interface}. Error: {e}')


def configure_interface_switchport_priority_extend_cos(device, interface, cos):
    """
    Configure interface switchport priority extend cos on the device.
    Args:
        device ('obj'): Device object
        interface ('str'): Interface name
        cos ('int'): COS value, 0..7
    Returns:
        None
    Raises:
        SubCommandFailure
    """

    cmd = [f"interface {interface}",
           f"switchport priority extend cos {cos}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure switchport priority extend cos on '
            f'{interface}. Error: {e}')


def unconfigure_interface_switchport_priority_extend_cos(device, interface):
    """
    Unconfigure interface switchport priority extend cos on the device.
    Args:
        device ('obj'): Device object
        interface ('str'): Interface name
    Returns:
        None
    Raises:
        SubCommandFailure
    """

    cmd = [f"interface {interface}",
           "no switchport priority extend cos"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not unconfigure switchport priority extend cos on '
            f'{interface}. Error: {e}')


def configure_interface_switchport_priority_extend_trust(device, interface):
    """
    Configure interface switchport priority extend trust on the device.
    Args:
        device ('obj'): Device object
        interface ('str'): Interface name
    Returns:
        None
    Raises:
        SubCommandFailure
    """

    cmd = [f"interface {interface}",
           "switchport priority extend trust"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure switchport priority extend trust on '
            f'{interface}. Error: {e}')


def unconfigure_interface_switchport_priority_extend_trust(device, interface):
    """
    Unconfigure interface switchport priority extend trust on the device.
    Args:
        device ('obj'): Device object
        interface ('str'): Interface name
    Returns:
        None
    Raises:
        SubCommandFailure
    """

    cmd = [f"interface {interface}",
           "no switchport priority extend trust"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not unconfigure switchport priority extend trust on '
            f'{interface}. Error: {e}')
