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

def configure_mdt_auto_discovery_mldp(device, vrf_name, address_family):

    """ configure mdt auto-discovery mldp

        Args:
            device (`obj`): Device object
            vrf_name ('str'): name of the vrf
            address_family ('str'):  mention the address-family.
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    confg = "vrf definition {vrf_name}".format(vrf_name=vrf_name)
    confg += "\n address-family {address_family}".format(address_family=address_family)
    confg += "\n mdt auto-discovery mldp"
    try:
        device.configure(confg)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure "mdt auto-discovery mldp under vrf definition {vrf_name}" on device'.format(
                    vrf_name=vrf_name)
        )

def configure_mdt_overlay_use_bgp(device, vrf_name, address_family):

    """ Enables BGP as the overlay protocol

        Args:
            device (`obj`): Device object
            vrf_name ('str'): name of the vrf
            address_family ('str'):  mention the address-family.
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring vrf
    """
    confg = "vrf definition {vrf_name}".format(vrf_name=vrf_name)
    confg += "\n address-family {address_family}".format(address_family=address_family)
    confg += "\n mdt overlay use-bgp"
    try:
        device.configure(confg)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure "mdt overlay use-bgp under vrf definition {vrf_name}" on device'.format(
                    vrf_name=vrf_name)
        )

def unconfigure_mdt_auto_discovery_mldp(device, vrf_name, address_family):

    """ unconfigure mdt auto-discovery mldp

        Args:
            device (`obj`): Device object
            vrf_name ('str'): name of the vrf
            address_family ('str'):  mention the address-family.
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    confg = "vrf definition {vrf_name}".format(vrf_name=vrf_name)
    confg += "\n address-family {address_family}".format(address_family=address_family)
    confg += "\n no mdt auto-discovery mldp"
    try:
        device.configure(confg)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure "mdt auto-discovery mldp under vrf definition {vrf_name}" on device'.format(
                    vrf_name=vrf_name)
        )

def unconfigure_mdt_overlay_use_bgp(device, vrf_name, address_family):

    """ unconfigure BGP as the overlay protocol

        Args:
            device (`obj`): Device object
            vrf_name ('str'): name of the vrf
            address_family ('str'):  mention the address-family.
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    confg = "vrf definition {vrf_name}".format(vrf_name=vrf_name)
    confg += "\n address-family {address_family}".format(address_family=address_family)
    confg += "\n no mdt overlay use-bgp"
    try:
        device.configure(confg)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure "no mdt overlay use-bgp under vrf definition {vrf_name}" on device'.format(
                    vrf_name=vrf_name)
        )


def configure_vrf_definition_family(device,vrf,address_family=None,family_type=''):
    """ Configures Address Family on VRF
        Args:
            device ('obj')    : device to use
            vrf ('str'): VRF name
            address_family ('str).  'ipv4', 'ipv6',
            family_type ('str,optional). (i.e unicast, multicast). Default is ''.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    #initialize list variable
    config_list = []
    config_list.append("vrf definition {vrf}".format(vrf=vrf))
    if address_family == 'ipv4':
        config_list.append("address-family ipv4 {family_type}".format(family_type=family_type))
    elif address_family == 'ipv6':
        config_list.append("address-family ipv6 {family_type}".format(family_type=family_type))
    try:
        device.configure(config_list)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure VRF Definition'
        )