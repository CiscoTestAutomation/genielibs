"""Common configure functions for bgp"""

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

def configure_isis_network_entity(device,network_entity):
    """ Configure network_entity on ISIS router
        Args:
            device('obj'): device to configure on
            network_entity('str'): network_entity of device
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(
        "Configuring router ISIS on {hostname}\n"
        "    -isis network_entity: {network_entity}".format(
            hostname=device.hostname, network_entity=network_entity
        )
    )
    config = [
                'router isis',
                'net {network_entity}'.format(network_entity=network_entity)
            ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure network_entity {network_entity} on "
            "ISIS router:\n{e}".format(hostname=device.hostname, network_entity=network_entity, e=e)
        )

def remove_isis_configuration(device):
    """ Remove isis configuration
        Args:
            device ('obj'): Device object
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(
        "Remove  ISIS configuration on {hostname}\n"
    )
    config = [
                'no router isis',
            ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not  Remove  ISIS configuration on "
            .format(hostname=device.hostname, e=e)
        )

def config_interface_isis(device, interface,ipv6=False):
    """config ISIS on interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            ipv6 ('boolean',optional): Flag to configure IPv6 (Default False)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        'Configuring ISIS on interface {interface}\n'.format(interface=interface)
    )
    config = []
    config.append("interface {interface}".format(interface=interface))
    if ipv6:
        config.append("ipv6 router isis")
    else:
        config.append("ip router isis")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure isis on interface {interface} on "
            .format(hostname=device.hostname, interface=interface, e=e)
        )

def unconfig_interface_isis(device, interface,ipv6=False):
    """Unconfig ISIS on interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            ipv6 ('boolean',optional): Flag to configure IPv6 (Default False)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Unconfiguring isis on interface {interface}\n".format(interface=interface)
    )
    config = []
    config.append("interface {interface}".format(interface=interface))
    if ipv6:
        config.append("no ipv6 router isis")
    else:
        config.append("no  ip router isis")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure isis on interface {interface} on "
            .format(hostname=device.hostname, interface=interface, e=e)
        )

def configure_isis_with_router_name_network_entity(device, router_name, network_entity=None):
    """ Configure isis with router name
        Args:
            device('obj'): device to configure on
            router_name ('str'):configure the isis router name
            network_entity('str',optional): network_entity of device
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(
        "Configuring isis with router name {router_name} on {hostname}".format(
            hostname=device.hostname, router_name=router_name, 
        )
    )
    config = []
    config.append('router isis {router_name}'.format(router_name=router_name))
    if network_entity:
        config.append('net {network_entity}'.format(network_entity=network_entity))
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure isis with router name {router_name} on {hostname}"
            "ISIS router:\n{e}".format(hostname=device.hostname, router_name=router_name, e=e)
        )

def unconfigure_isis_with_router_name(device,router_name):
    """ Unconfigure isis with router name
        Args:
            device('obj'): device to configure on
            router_name ('str'):configure the isis router name
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(
        "Configuring isis with router name {router_name} on {hostname}".format(
            hostname=device.hostname, router_name=router_name, 
        )
    )
    config = ['no router isis {router_name}'.format(router_name=router_name)]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure isis with router name {router_name} on {hostname}"
            "ISIS router:\n{e}".format(hostname=device.hostname, router_name=router_name, e=e)
        )

def config_interface_with_isis_router_name(device, interface, router_name):
    """config ISIS router name on interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            router_name ('str'):configure the isis router name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        'Configuring ISIS router name {router_name} on interface {interface}\n'.format(
        router_name=router_name,interface=interface)
    )
    config = []
    config.append("interface {interface}".format(interface=interface))
    config.append("ip router isis {router_name}".format(router_name=router_name))
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure isis router name {router_name} on interface {interface} on {hostname}"
            .format(hostname=device.hostname, router_name=router_name, interface=interface, e=e)
        )

def unconfig_interface_isis_router_name(device, interface, router_name):
    """Unconfig ISIS router name on interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            router_name ('str'):configure the isis router name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Unconfiguring isis {router_name} on interface {interface}\n".format(router_name=router_name,interface=interface)
    )
    config = []
    config.append("interface {interface}".format(interface=interface))
    config.append("no ip router isis {router_name}".format(router_name=router_name))
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure isis {router_name} on interface {interface} on {hostname}"
            .format(hostname=device.hostname, router_name=router_name, interface=interface, e=e)
            )