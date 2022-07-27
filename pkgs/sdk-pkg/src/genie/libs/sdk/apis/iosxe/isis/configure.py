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