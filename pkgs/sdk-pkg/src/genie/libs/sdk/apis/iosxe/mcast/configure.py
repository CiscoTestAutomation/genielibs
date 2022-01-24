"""Common configure functions for ip multicast routing"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_ip_multicast_routing(device):

    """ configure ip multicast routing on device

        Args:
            device (`obj`): Device object
        Returns:
            None
    """
    try:
        device.configure("ip multicast-routing")
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Configure ip multicast-routing. Error {e}".format(e=e)
        )

def unconfigure_ip_multicast_routing(device):

    """Unconfigure ip multicast routing on device

        Args:
            device (`obj`): Device object
        Returns:
            None
    """
    try:
        device.configure("no ip multicast-routing")
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Unconfigure ip multicast-routing. Error {e}".format(e=e)
        )

def configure_ip_multicast_vrf_routing(device, vrf_name):

    """ configure ip multicast routing vrf on device
        Example : 

        Args:
            device (`obj`): Device object
            vrf_name('str'): name of the vrf 
        Returns:
            None
    """
    try:
        device.configure("ip multicast-routing vrf {}".format(vrf_name))
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Configure ip multicast-routing vrf vrf_name. Error {e}".format(e=e)
        )

def unconfigure_ip_multicast_vrf_routing(device, vrf_name):

    """Unconfigure ip multicast routing vrf on device
        Example : 

        Args:
            device (`obj`): Device object
            vrf_name('str'): name of the vrf 
        Returns:
            None
    """
    try:
        device.configure("no ip multicast-routing vrf {}".format(vrf_name))
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Unconfigure ip multicast-routing vrf Error {e}".format(e=e)
        )

def configure_interface_pim(device,interface,pim_mode):

    """ Configure pim in interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            pim_mode (`str`): PIM mode (sparse-mode | sparse-dense-mode)

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("interface {intf}".format(intf=interface))
    configs.append("ip pim {mode}".format(mode=pim_mode))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure PIM mode {mode} on  interface "
            "{interface} on device {dev}. Error:\n{error}".format(
                mode=pim_mode,
                interface=interface,
                dev=device.name,
                error=e,
            )
        )

def unconfigure_interface_pim(device,interface,pim_mode):

    """ unconfigure pim in interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            pim_mode (`str`): PIM mode (sparse-mode | sparse-dense-mode)

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("interface {intf}".format(intf=interface))
    configs.append("no ip pim {mode}".format(mode=pim_mode))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure PIM mode {mode} on  interface "
            "{interface} on device {dev}. Error:\n{error}".format(
                mode=pim_mode,
                interface=interface,
                dev=device.name,
                error=e,
            )
        )
