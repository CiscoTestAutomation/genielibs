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

def unconfigure_bfd_on_interface(
    device, interface
):
    """ Unconfigures bfd on interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring bfd on interface

    """
    log.info(
        "Unconfiguring bfd on "
        "interface {}".format(interface)
    )

    try:
        device.configure(
            [
                "interface {}".format(interface),
                "no bfd interval"
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not unconfigure bfd on interface {interface}".format(
                interface=interface
            )
        )

def configure_bfd_neighbor_on_interface(
    device, interface, address_family, neighbor_address
):
    """ Configures bfd neighbor on interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            address_family ('str'): ipv4|ipv6 address family
            neighbor_address ('str'): neighbor address
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring bfd on interface

    """
    log.debug(
        "Configuring bfd with address_family={}, neighbor_address={} on "
        "interface {}".format(address_family, neighbor_address, interface)
    )

    try:
        device.configure(
            [
                "interface {}".format(interface),
                "bfd neighbor {} {} ".format(
                    address_family, neighbor_address
                ),
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure bfd neighbor on interface {interface}".format(
                interface=interface
            )
        )

def unconfigure_bfd_neighbor_on_interface(
    device, interface, address_family, neighbor_address
):
    """ Unconfigures bfd on interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            address_family ('str'): ipv4|ipv6 address family
            neighbor_address ('str'): neighbor address
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring bfd on interface

    """
    log.debug(
        "UnConfiguring bfd with address_family={}, neighbor_address={} on "
        "interface {}".format(address_family, neighbor_address, interface)
    )

    try:
        device.configure(
            [
                "interface {}".format(interface),
                "no bfd neighbor {} {} ".format(
                    address_family, neighbor_address
                ),
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not unconfigure bfd neighbor on interface {interface}".format(
                interface=interface
            )
        )

def unconfigure_bfd_value_on_interface(device, interface, value):
    """ Unconfigures bfd on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            bfd ('str'): bfd value to unconfigure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring bfd on interface
    """
    log.info(
        "Unconfiguring bfd on "
        "interface {}".format(interface)
    )
    config = [
                "interface {}".format(interface),
                "no bfd {}".format(value)
            ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure bfd value on interface {interface}. Error:\n{e}"
        )

def enable_bfd_on_isis_ipv6_address(device, interface):
    """ Enabled bfd on isis ipv6 address on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure under
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring bfd on isis ipv6 address
    """
    log.info("Enabling bfd on isis ipv6 address")
    cmd = ["interface {}".format(interface), "isis ipv6 bfd"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
             f"Could not enable bfd on isis ipv6 address on interface {interface}. Error:\n{e}"
        )

def disable_bfd_on_isis_ipv6_address(device, interface):
    """ Disables bfd on isis ipv6 address
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure under
        Returns:
            None
        Raises:
            SubCommandFailure: Failed disabling bfd on isis ipv6 address
    """
    log.info("Disabling bfd on isis ipv6 address")
    cmd = ["interface {}".format(interface), "no isis ipv6 bfd"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not disable bfd on isis ipv6 address on interface {interface}. Error:\n{e}"
        )

