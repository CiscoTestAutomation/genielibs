"""Common configure functions for bfd"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_bfd_on_interface(
    device, interface, interval, min_rx, multiplier
):
    """ Configures bfd on interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            interval ('str'): interval
            min_rx ('str'): min_rx
            multiplier ('str'): multiplier
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring bfd on interface

    """
    log.info(
        "Configuring bfd with interval={}, min_rx={}, multiplier={}, on "
        "interface {}".format(interval, min_rx, multiplier, interface)
    )

    try:
        device.configure(
            [
                "interface {}".format(interface),
                "bfd interval {} min_rx {} multiplier {}".format(
                    interval, min_rx, multiplier
                ),
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure bfd on interface {interface}".format(
                interface=interface
            )
        )


def enable_bfd_on_ospf(device, interface):
    """ Enabled bfd on ospf protocol on interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure under
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring bfd on ospf protocol
    """
    log.info("Enabling bfd on ospf protocol")
    try:
        device.configure(["interface {}".format(interface), "ip ospf bfd"])
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not enable bfd on ospf protocol on interface {interface}".format(
                interface=interface
            )
        )


def disable_bfd_on_ospf(device, interface):
    """ Disables bfd on ospf protocol

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure under
        Returns:
            None
        Raises:
            SubCommandFailure: Failed disabling bfd on ospf protocol
    """
    log.info("Disabling bfd on ospf protocol")
    try:
        device.configure(["interface {}".format(interface), "no ip ospf bfd"])
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not disable bfd on ospf protocol on interface {interface}".format(
                interface=interface
            )
        )


def enable_bfd_static_route(device, interface, ip_address):
    """ Enables bfd static route on device

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure under
            ip_address ('str'): ip address of destination
        Returns:
            None
        Raises:
            SubCommandFailure: Failed enabling bfd static rout on device
    """
    log.info(
        "Enabling bfd static route on {} to {}".format(interface, ip_address)
    )
    try:
        device.configure(
            ["ip route static bfd {} {}".format(interface, ip_address)]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure bfd static route on interface {interface}".format(
                interface=interface
            )
        )
