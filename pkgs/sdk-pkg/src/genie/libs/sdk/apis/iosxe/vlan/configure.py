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

def configure_vtp_mode(device,mode):
    """ Configures global VTP mode
        Args:
            device ('obj'): device to use
            mode ('str'):  VTP mode (i.e transparent, client, server)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure('vtp mode {mode}'.format(mode=mode))
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure VTP mode'
        )

def configure_pvlan_svi_mapping(device, svi_vlan, mapping_vlan):
    """ Configures Private Vlan Mapping on SVI
        Args:
            device ('obj'): device to use
            svi_vlan ('str'): SVI interface
            mapping_vlan ('str'): Private vlan to map to
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    # Initialize list variable
    config_list = []
    config_list.append("interface {svi_vlan}".format(svi_vlan=svi_vlan))
    config_list.append("private-vlan mapping {mapping_vlan}".format(mapping_vlan=mapping_vlan))

    try:
        device.configure(config_list)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure PVLAN-mapping'
        )


def configure_pvlan_primary(device, primary_vlan, secondary_vlan=None):
    """ Configures Primary Private Vlan
        Args:
            device ('obj'): device to use
            primary_vlan ('str'): Primary private vlan
            secondary_vlan ('str',optional): Secondary isolated/community vlan
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config_list = []
    # vlan 100
    # private-vlan primary
    config_list.append("vlan {primary_vlan} \n"
                       "private-vlan primary".format(primary_vlan=primary_vlan))
    # private-vlan association 101
    if secondary_vlan != None:
        config_list.append("private-vlan association {secondary_vlan}".format(secondary_vlan=secondary_vlan))

    try:
        device.configure(config_list)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure Primary Pvlan'
        )

def configure_pvlan_type(device,vlan,pvlan_type):
    """ Configures Isolated Private Vlan
        Args:
            device ('obj'): device to use
            vlan ('str'): Vlan id
            pvlan_type ('str'): Private vlan type (i.e isolated, primary, community)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    # Initialize list variable
    config_list = []
    config_list.append("vlan {vlan}".format(vlan=vlan))
    config_list.append("private-vlan {pvlan_type}".format(pvlan_type=pvlan_type))

    try:
        device.configure(config_list)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure Primary Pvlan'
        )