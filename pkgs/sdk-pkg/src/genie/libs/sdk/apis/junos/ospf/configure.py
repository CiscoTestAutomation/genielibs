"""Common configure functions for OSPF"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_ospf_passive_interface(device, interface, area):
    """configure passive interface

        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'
            area (`str`): IP address of area

        Returns:
            None
        
        Raise:
            SubCommandFailure
    """
    config = []
    config.append(
        "set protocols ospf area {} interface "
        "{} passive\n".format(area, interface)
    )

    try:
        device.configure("".join(config))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure passive on {interface}. Error:\n{error}".format(
                interface=interface, error=e
            )
        )


def remove_ospf_passive_interface(device, interface, area):
    """remove passive interface on junos device

        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'
            area (`str`): IP address of area

        Returns:
            None
        
        Raise:
            SubCommandFailure
    """
    config = []
    config.append(
        "delete protocols ospf area {} interface "
        "{} passive\n".format(area, interface)
    )

    try:
        device.configure("".join(config))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not remove passive configuration on {interface}. Error:\n{error}".format(
                interface=interface, error=e
            )
        )
