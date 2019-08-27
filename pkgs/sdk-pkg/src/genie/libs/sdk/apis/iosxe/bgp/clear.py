"""Common clear functions for bgp"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def clear_ip_bgp_vrf_af_soft(device, vrf, address_family, bgp_as):
    """ BGP soft clear using vrf, address family and AS number

        Args:
            device ('obj'): device object
            vrf ('str'): vrf name
            address_family ('str'): address family
            as_number ('int'): BGP AS number
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    try:
        device.execute(
            "clear ip bgp vrf {vrf} {address_family} {as_number} soft".format(
                vrf=vrf, address_family=address_family, as_number=bgp_as
            )
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not reset bgp connections on device {device}".format(
                device=device.name
            )
        )


def clear_bgp_neighbors_soft(device, direction="", neighbor_address="ALL"):
    """ Reset connection to a BGP neighbor or to all neighbors, diretion in or out
        Args:
            device ('obj') : Device object
            direction ('str'): Direction type:
                ex.)
                    direction = "in"
                    direction = "out"
            neighbor (`str`): Neighbor address
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    if neighbor_address.upper() == "ALL":
        if direction:
            cmd = "clear ip bgp * soft {}".format(direction)
        else:
            cmd = "clear ip bgp * soft"
    else:
        if direction:
            cmd = "clear ip bgp {} soft {}".format(neighbor_address, direction)
        else:
            cmd = "clear ip bgp {} soft".format(neighbor_address)

    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not soft clear device {dev}".format(dev=device.name)
        )
