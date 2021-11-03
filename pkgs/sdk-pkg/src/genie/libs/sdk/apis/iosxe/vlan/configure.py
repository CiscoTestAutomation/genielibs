"""Common configure functions for vlan"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def config_vlan(device, vlanid):
    """ Configures a VLAN on Interface or Device
    e.g.
    vlan 666

        Args:
            device (`obj`): Device object
            vlanid (`str`): Vlan id
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    configs = []
    configs.append("vlan {vlanid}".format(vlanid=vlanid))
    configs.append("no shutdown")
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure vlan {vlanid}, Error: {error}'.format(
                vlanid=vlanid, error=e)
        )

def config_ip_on_vlan(device, vlan_id, ipv4_address=None,
                      subnetmask=None, ipv6_address=None,
                      ipv6_prefix_len=None):
    """Configure an IPv4/IPv6 address on a vlan

        Args:
            device (`obj`): Device object
            vlanid (`str`): Vlan id
            ipv4_address (`str`): IPv4 address
            subnetmask (`str`): Subnet mask to be used for IPv4 address
            ipv6_address (`str`): Ipv6 address
            ipv6_prefix_len (`int`): length of IPv6 prefix
        Return:
            None
        Raise:
            SubCommandFailure: Failed to configure Ipv4/Ipv6 address on vlan
    """

    try:
        if ipv4_address and subnetmask:
            device.configure([f'interface vlan {vlan_id}',
                            f'ip address {ipv4_address} {subnetmask}'])

        if ipv6_address and ipv6_prefix_len:
            device.configure([f'interface vlan {vlan_id}',
                            'ipv6 enable',
                            f'ipv6 address {ipv6_address}/{ipv6_prefix_len}'])

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure Ipv4/Ipv6 address on vlan {vlan_id}, '
            f'Error: {e}'
        )

def unconfig_vlan(device, vlanid):
    """ vlan on Interface or Device configuration removal

        Args:
            device (`obj`): Device object
            vlanid (`str`): Vlan id
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    try:
        device.configure("no vlan {vlanid}".format(vlanid=vlanid))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not remove vlan {vlanid}, Error: {error}'.format(
                vlanid=vlanid, error=e)
        )

def config_vlan_tag_native(device):
    """ Configure vlan dot1q tag native

        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring device
    """

    try:
        device.configure("vlan dot1q tag native")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure vlan dot1q tag native, Error: {error}'.format(
                error=e)
        )

def unconfig_vlan_tag_native(device):
    """ Unconfigure vlan dot1q tag native

        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring device
    """

    try:
        device.configure("no vlan dot1q tag native")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not remove vlan dot1q tag native, Error: {error}'.format(
                error=e)
        )
 
def configure_vlan_vpls(device, vlanid):
    """ Config vpls on vlan

        Args:
            device (`obj`): Device object
            vlanid (`str`): Vlan id
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """

    try:
        device.configure(
            [
                "vlan configuration {vlanid}".format(vlanid=vlanid),
                "member vfi vpls",
                "vlan dot1q tag native",
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure vpls on vlan {vlanid}, Error: {error}'.format(
                vlanid=vlanid, error=e)
        )

def unconfigure_vlan_vpls(device, vlanid):
    """ Unconfig vpls on vlan

        Args:
            device (`obj`): Device object
            vlanid (`str`): Vlan id
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """

    try:
        device.configure([
            "no vlan configuration {vlanid}".format(vlanid=vlanid),
            "no vlan dot1q tag native"])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not unconfigure vpls on vlan {vlanid}, Error: {error}'.format(
                vlanid=vlanid, error=e)
        )


def unconfigure_vlan_configuration(device, vlanid):
    """ Unconfguring vlan configuration in the device
        Args:
            device (`obj`): Device object
            vlanid ('int') : vlan id
        Returns:
            None
        Raises:
            SubCommandFailure
        Example: no vlan configuration 101
    """
    try:
        device.configure(
            "no vlan configuration {vlanid}".format(vlanid=vlanid)
        )
    except SubCommandFailure as e:
        log.error("Unable to unconfig vlan {}, Error:\n{}".format(vlanid, e))
        raise
