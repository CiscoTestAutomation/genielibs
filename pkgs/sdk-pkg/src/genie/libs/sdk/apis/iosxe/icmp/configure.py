"""Common configure functions for L3-ICMP"""

# Python
import logging
import re
import jinja2

# Genie
from genie.utils.timeout import Timeout

# Utils
from genie.libs.sdk.apis.iosxe.running_config.get import (
    get_running_config_section_dict,
)

# Steps
from pyats.aetest.steps import Steps

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_icmp_ip_reachables(device, interface, line, ip_address, ip_subnet):
    """ Configures sending of ICMP unreachable messages for an interface
        Example: ip unreachables

        Args:
            device ('obj'): device to configure on
            interface ('str'): name of the interface (eg. Tel1/0/10)
            line ('str'): Up to 230 characters describing the interface
            ip_address ('str'): IP Address A.B.C.D (eg. 50.1.1.2)
            ip_subnet ('str'): IP subnet mask A.B.C.D (eg. 255.255.0.0)

        Return:
            None

        Raises:
            SubCommandFailure: Failed executing command
    """

    log.info(f"Configuring ip reachables on device {device.name}")
    config = [
        f'interface {interface}',
        f'description {line}',
        f'no switchport',
        f'ip address {ip_address} {ip_subnet}',
        f'ip unreachables'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure ip unreachables on device {device.name}. Error:\n{e}")

def unconfigure_icmp_ip_reachables(device, interface, line, ip_address, ip_subnet):
    """ Unconfigures sending of ICMP unreachable messages for an interface
        Example: no ip unreachables

        Args:
            device ('obj'): device to configure on
            interface ('str'): name of the interface (eg. Tel1/0/10)
            line ('str'): Up to 230 characters describing the interface
            ip_address ('str'): IP Address A.B.C.D (eg. 50.1.1.2)
            ip_subnet ('str'): IP subnet mask A.B.C.D (eg. 255.255.0.0)

        Return:
            None

        Raises:
            SubCommandFailure: Failed executing command
    """

    log.info(f"Unconfiguring ip reachables on device {device.name}")
    config = [
        f'interface {interface}',
        f'description {line}',
        f'no switchport',
        f'ip address {ip_address} {ip_subnet}',
        f'no ip unreachables'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not unconfigure ip unreachables on device {device.name}. Error:\n{e}")