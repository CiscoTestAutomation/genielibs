"""Common configure functions for interface"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Steps
from pyats.aetest.steps import Steps

# Genie
from genie.harness.utils import connect_device

log = logging.getLogger(__name__)

def config_standby_console_enable(device):
    """ Enable standby console

        Args:
            device (`obj`): Device object

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    log.info("Configuring standby console enable cli")

    try:
        device.configure(
            [
                "redundancy",
                "main-cpu",
                "standby console enable"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Enabling Standby Console failed. Error: {error}".format(error=e)
        )
        
def configure_redundancy(device):
    """ configure redundancy on device
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
       
    try:
        out = device.configure(['redundancy', 'mode sso'])
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure redundancy mode to SSO . Error:\n{e}")

def configure_redundancy_interchassis_group(
    device,
    group,
    member_ip=None,
    backbone_interface=None,
    monitor_peer_bfd=False,
    mlacp_system_mac=None,
    mlacp_system_priority=None,
    mlacp_node_id=None,
):
    """Configure redundancy interchassis group parameters.

    Args:
        device (`obj`): Device object
        group (`str`): Interchassis group id
        member_ip (`str`, optional): Member peer IP
        backbone_interface (`str`, optional): Backbone interface name
        monitor_peer_bfd (`bool`, optional): Configure monitor peer bfd
        mlacp_system_mac (`str`, optional): MLACP system MAC
        mlacp_system_priority (`str`, optional): MLACP system priority
        mlacp_node_id (`str`, optional): MLACP node id

    Returns:
        None

    Raises:
        SubCommandFailure: Failed configuring redundancy interchassis group
    """

    log.info("Configuring redundancy interchassis group")

    configs = ['redundancy', f'interchassis group "{group}"']

    if monitor_peer_bfd:
        configs.append('monitor peer bfd')

    if member_ip is not None:
        configs.append(f'member ip "{member_ip}"')

    if backbone_interface is not None:
        configs.append(f'backbone interface "{backbone_interface}"')

    if mlacp_system_mac is not None:
        configs.append(f'mlacp system-mac "{mlacp_system_mac}"')

    if mlacp_system_priority is not None:
        configs.append(f'mlacp system-priority "{mlacp_system_priority}"')

    if mlacp_node_id is not None:
        configs.append(f'mlacp node-id "{mlacp_node_id}"')

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure redundancy interchassis group on {device.name}. "
            f"Error:\n{e}"
        )

def unconfigure_redundancy(device):
    """ unconfigure redundancy on device
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
       
    try:
        out = device.configure(['redundancy', 'mode none'])
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure redundancy mode . Error:\n{e}")
