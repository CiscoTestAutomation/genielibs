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

def clear_ip_bgp(device):
    """ clear ip bgp *
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure: Failed executing command
    """

    log.debug("Clearing ip bgp on {device}".format(device=device))

    try:
        device.execute("clear ip bgp *")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear ip bgp on {device}. Error:\n{error}".format(device=device, error=e)
        )


def clear_ip_bgp_af_as(device, address_family, as_numbers):
    """ BGP soft clear using address family and AS number
        i.e 'clear ip bgp {address_family} {as_number}'
        Args:
            device ('obj'): device object
            address_family ('str'): address family
            as_numbers ('list'/'int'): BGP AS number
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    cmd = []
    if isinstance(as_numbers,list):
        for as_number in as_numbers:
            cmd.append(f"clear ip bgp {address_family} {as_number}")
    else:
        cmd = f'clear ip bgp {address_family} {as_numbers}'

    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not clear ip bgp {address_family} as {as_numbers} on device"
            f" {device}.Error:\n{e}"
        )

def clear_bgp_all_as(device, as_number):
   """ clear all bgp AS number
        i.e 'clear bgp all {as_number}'
        Args:
            device ('obj'): device object
            as_number ('int'): BGP AS number
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
   cmd = f'clear bgp all {as_number}'

   try:
        device.execute(cmd)
   except SubCommandFailure as err:
        raise SubCommandFailure(
            f"Could not clear bgp all as {as_number} on device. Error:\n{err}")