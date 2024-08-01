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
from unicon.eal.dialogs import Dialog, Statement


def configure_interface_span_portfast(device, interface, mode=''):
    """ Configures Spanning Tree Portfast on port
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
            mode ('str',optional) : Options are disable/trunk. Default is '' (i.e no mode)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    #initialize list variable
    config_list = [f"interface {interface}"]
    if mode == 'trunk':
        config_list.append("spanning-tree portfast edge trunk")
    else:
        config_list.append(f"spanning-tree portfast {mode}")
    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure Spanning Tree Portfast on {interface} on {device.name}. Error:\n{e}'
        )
