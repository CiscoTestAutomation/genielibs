"""Common configure functions for RIPng on IOS"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_ripng(device, pid):
    """Configure RIPng on device.

        Args:
            device ('obj'): Device object
            pid ('str'): RIPng process id
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(f"ipv6 router rip {pid}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure RIPng {pid} on device. Error:\n{e}"
        )


def unconfigure_ripng(device, pid):
    """Unconfigure RIPng on device.

        Args:
            device ('obj'): Device object
            pid ('str'): RIPng process id
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(f"no ipv6 router rip {pid}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure RIPng {pid} on device. Error:\n{e}"
        )


def configure_interface_ripng(device, interface, pid):
    """Enable RIPng on an interface.

        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
            pid ('str'): RIPng process id
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f"interface {interface}",
        f"ipv6 rip {pid} enable",
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure RIPng {pid} on interface "
            f"{interface}. Error:\n{e}"
        )


def unconfigure_interface_ripng(device, interface, pid):
    """Disable RIPng on an interface.

        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
            pid ('str'): RIPng process id
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f"interface {interface}",
        f"no ipv6 rip {pid} enable",
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure RIPng {pid} on interface "
            f"{interface}. Error:\n{e}"
        )
