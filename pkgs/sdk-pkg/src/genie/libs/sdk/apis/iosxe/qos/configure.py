"""Common configure functions for interface"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Steps
from pyats.aetest.steps import Steps

# Genie
from genie.conf.base import Interface
from genie.libs.conf.base import IPv4Address, IPv6Address
from genie.libs.conf.interface import IPv4Addr, IPv6Addr
from genie.harness.utils import connect_device

# Interface
from genie.libs.sdk.apis.iosxe.interface.get import (
    get_interface_running_config,
)
from genie.libs.sdk.apis.iosxe.interface.get import (
    get_interface_connected_adjacent_router_interfaces,
)

# utils
from genie.libs.sdk.apis.utils import mask_to_int

log = logging.getLogger(__name__)

def configure_qos_policy(device, interface, access_type, policy_name):
    """ Configures the qos_policy on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            access_type ('str') : type of interface or VC
            policy_name ('str') : name of the policy
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring qos_policy on {interface}".format(
            interface=interface
        )
    )

    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "service-policy {access_type} {policy_name}".format(access_type=access_type,policy_name=policy_name)
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure qos_policy. Error:\n{error}".format(
                error=e
            )
        )

def unconfigure_qos_policy(device, interface, access_type, policy_name):
    """ Unconfigure the qos_policy on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            access_type ('str') : type of interface or VC
            policy_name ('str') : name of the policy
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Unconfiguring qos_policy on {interface} ".format(
            interface=interface
        )
    )

    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "no service-policy {access_type} {policy_name}".format(access_type=access_type,policy_name=policy_name)
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure qos_policy. Error:\n{error}".format(
                error=e
            )
        )

