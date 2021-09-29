"""Common configure/unconfigure functions for evpn"""

# Python
import logging
import re

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_evpn_instance_vlan_based_with_reoriginate_rt5(device, instance):
    """ Configuring l2vpn evpn instance vlan based by re-originating RT-5
        Args:
            device (`obj`): Device object
            instance (`int`): instance number
        Returns:
            console ouput ('str'): incase of successful configuration
        Raises:
            SubCommandFailure
    """
    config = []
    config.append("l2vpn evpn instance {} vlan-based".format(instance))
    config.append("re-originate route-type5")

    try:
        output = device.configure(config)
    except SubCommandFailure as e:
        log.error("Configuration failed for re-origination of route-type 5"
            "of instance: {} with exception:\n{}".format(instance, str(e))
        )

    return output


def unconfigure_evpn_instance_vlan_based(device, instance):
    """ Unconfiguring l2vpn evpn instance configuration
        Args:
            device (`obj`): Device object
            instance (`int`): instance number
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            "no l2vpn evpn instance {instance} vlan-based".format(
                instance=instance)
        )
    except SubCommandFailure as e:
        log.error("Could not unconfig l2vpn evpn instance {instance},"
             "Error:\n{error}".format(instance=instance, error=e)
        )
        raise
