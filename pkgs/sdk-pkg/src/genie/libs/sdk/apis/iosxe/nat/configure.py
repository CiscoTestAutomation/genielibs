"""Common configure functions for nat"""
# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_nat_in_out(
    device, 
    inside_interface=None, 
    outside_interface=None,
):
    """ Enable nat IN and OUT over interface 
        Args:
            device ('obj'): device to use
            inside_interface ('str'): enable nat in over this interface, default value is None
            outside_interface ('str'): enable nat out over this interface, default value is None
        Returns:
            console output
        Raises:
            SubCommandFailure: NAT IN OUT not enable over interface
    """
    cmd = []
    if inside_interface:
        cmd.append("interface {}".format(inside_interface))
        cmd.append("ip nat inside")

    if outside_interface:
        cmd.append("interface {}".format(outside_interface))
        cmd.append("ip nat outside")

    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Enable NAT. Error:\n{error}".format(error=e)
        )
    return out

def configure_nat_overload_rule(
    device, 
    interface, 
    access_list_name,
):
    """ Configure interface overloaad rule
        Args:
            device ('obj'): device to use
            interface ('str'): Interface which will use for overlad rule
            access_list_name ('str'): Name of extended access list
        Returns:
            console output
        Raises:
            SubCommandFailure: Nat overload rule not connfigured
    """
    cmd = ["ip nat inside source list {} interface {} overload".format(access_list_name,interface)]

    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Configure NAT overload rule. Error:\n{error}".format(error=e)
        )
    return out

def unconfigure_nat_in_out(
    device, 
    inside_interface=None, 
    outside_interface=None,
):
    """ Disable nat IN and OUT over interface 
        Args:
            device ('obj'): device to use
            inside_interface ('str'): Disable nat in from this interface, default value is None
            outside_interface ('str'): Disable nat out From this interface, default value is None
        Returns:
            console output
        Raises:
            SubCommandFailure: NAT IN OUT not enable over interface
    """
    cmd = []
    if inside_interface:
        cmd.append("interface {}".format(inside_interface))
        cmd.append("no ip nat inside")
    if outside_interface:
        cmd.append("interface {}".format(outside_interface))
        cmd.append("no ip nat outside")

    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Disable NAT. Error:\n{error}".format(error=e)
        )
    return out

def unconfigure_nat_overload_rule(
    device, 
    interface, 
    access_list_name,
):
    """ UnConfigure interface overload rule
        Args:
            device ('obj'): device to use
            interface ('str'): Interface which will use for overlad rule
            access_list_name ('str'): Name of extended access list
        Returns:
            console output
        Raises:
            SubCommandFailure: Nat overload rule not unconfigured
    """
    cmd = ["no ip nat inside source list {} interface {} overload".format(access_list_name, interface)]

    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not UnConfigure NAT overload rule. Error:\n{error}".format(error=e)
        )
    return out


