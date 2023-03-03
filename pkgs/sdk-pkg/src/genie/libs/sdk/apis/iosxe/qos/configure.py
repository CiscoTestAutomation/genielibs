"""Common configure functions for interface"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

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

def configure_auto_qos(device, interface, qos_mode, qos_value):
    """ Configures the qos_policy on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            qos_mode ('str') : qos_mode name
            qos_value ('str'): qos_value 
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring auto_qos on {interface}".format(
            interface=interface
        )
    )

    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "auto qos {qos_mode} {qos_value}".format(qos_mode=qos_mode,qos_value=qos_value)
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure auto_qos_policy. Error:\n{error}".format(
                error=e
            )
        )

def unconfigure_auto_qos(device, interface, qos_mode, qos_value):
    """ Unconfigures the qos_policy on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to unconfigure
            qos_mode ('str') : qos_mode name
            qos_value ('str'): qos_value
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Unconfiguring auto_qos on {interface}".format(
            interface=interface
        )
    )

    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "no auto qos {qos_mode} {qos_value}".format(qos_mode=qos_mode,qos_value=qos_value)
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure auto_qos_policy. Error:\n{error}".format(
                error=e
            )
        )

def configure_auto_qos_global(device,compact):
    """ Configures the auto qos global compact
        Args:
            device ('obj'): device to use
            compact ('str'): name of compact
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring auto qos global compact" 
    )

    try:
        device.configure(
                "auto qos global {compact}".format(compact=compact) 
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure auto qos global compact. Error:\n{error}".format(
                error=e
            )
        )

def unconfigure_auto_qos_global(device,compact):
    """ unconfigures the auto qos global compact
        Args:
            device ('obj'): device to use
            compact('str'): name of compact
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "unconfiguring auto qos global compact"
    )

    try:
       device.configure("no auto qos global {compact}".format(compact=compact))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure auto qos global compact. Error:\n{error}".format(
                error=e
            )
        )

def copy_running_config_to_flash_memory(device, timeout=60):
    """ Restore config from local file using copy function
        Args:
            device (`obj`): Device object
            timeout (`str`): timeout
        Returns:
            None
        Raises:
            SubCommandFailure
         
    """
    log.debug("Restore config from local file using copy function")
    
    dialog = Dialog(
        [
            Statement(
                pattern=r".*Destination filename.*",
                action="sendline()",
                loop_continue=False,
                continue_timer=False,
            )
        ]
    )
    try:
        device.execute(
            "copy running-config flash:backup_config",
            reply=dialog, timeout=timeout
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not copy saved configuration on {device}. Error:\n{e}")

def unconfig_qos_rewrite_dscp(device):
    """Unconfig qos rewrite ip dscp on Device
        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed unconfiguring qos rewrite ip dscp on device
    """
    log.debug("Unconfig qos rewrite ip dscp on Device")
    try:
        device.configure("no qos rewrite ip dscp")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfig qos rewrite ip dscp.Error:\n{e}")

def config_qos_rewrite_dscp(device):
    """Config qos rewrite ip dscp on Device
        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed Configuring qos rewrite ip dscp on device
    """
    log.debug("Configuring qos rewrite ip dscp on Device")
    try:
        device.configure("qos rewrite ip dscp")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to config qos rewrite ip dscp.Error:\n{e}")

def config_replace_to_flash_memory(device, timeout=60):
    """ configure replace to flash memory
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raise:
            SubCommandFailure: Failed to replace to flash memory
    """
    log.debug("configure replace to flash memory")
    dialog = Dialog(
        [
            Statement(
                pattern=r".*This will apply all necessary additions and deletions.*",
                action="sendline(y)",
                loop_continue=False,
                continue_timer=False,
            )
        ]
    )
    try:
        device.execute("configure replace flash:backup_config", reply=dialog, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure replace to flash on {device}. Error:\n{e}")

