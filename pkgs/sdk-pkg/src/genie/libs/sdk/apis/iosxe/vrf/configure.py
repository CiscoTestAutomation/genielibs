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
