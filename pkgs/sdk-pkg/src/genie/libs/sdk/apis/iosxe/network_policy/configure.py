"""Common configure functions for Network Policy"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_interface_network_policy(device, interface, profile):
    """
    Configure Network Policy on Interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            profile ('int'): Network Policy profile number

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        device.configure(
            [
                f"interface {interface}",
                f"network-policy {profile}",
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Configure Interface Network-Policy Profile"
            "{interface}. Error:\n{error}".format(interface=interface, error=e)
        )

def unconfigure_interface_network_policy(device, interface, profile):
    """
    Unconfigure Network Policy on Interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            profile ('int'): Network Policy profile number

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        device.configure(
            [
                f"interface {interface}",
                f"no network-policy {profile}",
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Unconfigure Interface Network-Policy Profile"
            "{interface}. Error:\n{error}".format(interface=interface, error=e)
        )

def configure_network_policy_profile_voice_vlan(device, profile, vlan, cos=None, dscp=None, voice_signaling=True):
    """configure Network-Policy Profile on target device
        Args:
            device (`obj`): Device object
            profile (`int`): profile number
            vlan (`int`): vlan id
            cos ('int', optional): cos value (Default is None)
            dscp ('int', optional): dscp value (Default is None)
            voice_signaling ('boolean',optional): Flag to configure voice-signaling (Default True)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"network-policy profile {profile}", f"voice vlan {vlan}"]
    if cos:
        cmd.append(f"voice vlan {vlan} cos {cos}")
    if dscp:
        cmd.append(f"voice vlan {vlan} dscp {dscp}")
    if voice_signaling and cos and dscp:
        cmd.append(f"voice-signaling vlan {vlan}")
        cmd.append(f"voice-signaling vlan {vlan} cos {cos}")
        cmd.append(f"voice-signaling vlan {vlan} dscp {dscp}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure network-policy profile {profile}. Error:\n{e}"
        )

def unconfigure_network_policy_profile_voice_vlan(device, profile, vlan, voice_signaling=True, cos=None, dscp=None):
    """unconfigure Network-Policy Profile on target device
        Args:
            device (`obj`): Device object
            profile (`int`): profile number
            vlan (`int`): vlan id
            voice_signaling ('boolean',optional): Flag to unconfigure voice-signaling (Default True)
            cos ('int', optional): cos value (Default is None)
            dscp ('int', optional): dscp value (Default is None)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"network-policy profile {profile}", f"no voice vlan {vlan}"]
    if voice_signaling and cos and dscp:
        cmd.append("no voice-signaling vlan")
        cmd.append(f"no voice-signaling vlan {vlan} cos {cos}")
        cmd.append(f"no voice-signaling vlan {vlan} dscp {dscp}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure network-policy profile {profile}. Error:\n{e}"
        )

def unconfigure_network_policy_profile_number(device, profile_number):
    """unconfigure Network-Policy Profile on target device
        Args:
            device ('obj'): Device object
            profile_number ('int'): profile number
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"no network-policy profile {profile_number}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure network-policy profile {profile_number}. Error:\n{e}")
def unconfigure_global_network_policy(device, profile):
    """
    Unconfigure Network Policy Gloablly
        Args:
            device (`obj`): Device object
            profile ('int'): Network Policy profile number

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        device.configure(
            [
                f"no network-policy profile {profile}",
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not Unconfigure Network-Policy Profile. Error:\n{e}"
        )
