"""Common configure functions for vrf"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure


log = logging.getLogger(__name__)


def configure_vrf_description(device, vrf, description):
    """Configure vrf description

        Args:
            device (`obj`): Device object
            vrf (`str`): VRF name
            description(`str`): Description

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                "vrf definition {vrf}".format(vrf=vrf),
                "description {description}".format(description=description),
            ]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure description '{desc}' on "
            "vrf {vrf}".format(desc=description, vrf=vrf)
        )
def unconfigure_vrf(device,vrf):

    """Remove ospf on device

        Args:
            device (`obj`): Device object
            vrf (`int`): vrf id

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        device.configure(f"no vrf definition {vrf}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring, Please verify"
        ) from e

def unconfigure_vrf_description(device, vrf):
    """Unconfigure vrf description

        Args:
            device (`obj`): Device object
            vrf (`str`): VRF name

        Returns:
            None

        Raises:
            SubCommandFailure            
    """
    try:
        device.configure(
            ["vrf definition {vrf}".format(vrf=vrf), "no description"]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove description on " "vrf {vrf}".format(vrf=vrf)
        )

def unconfigure_vrf_definition_on_device(
    device, vrf_name):
    """ unconfig vrf definition on device

        Args:
            device (`obj`): Device object
            vrf_name ('str'): name of the vrf
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    try:
        device.configure("no vrf definition {vrf_name}".format(
                            vrf_name=vrf_name
                        )
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not unconfigure "vrf definition {vrf_name}" on device'.format(
                    vrf_name=vrf_name)
        )

