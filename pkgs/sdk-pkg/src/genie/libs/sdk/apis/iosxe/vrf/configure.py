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
    confg = ["vrf definition {vrf_name}".format(vrf_name=vrf_name),
            "address-family {address_family}".format(address_family=address_family),
            "mdt overlay use-bgp"]
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
    confg = ["vrf definition {vrf_name}".format(vrf_name=vrf_name),
            "address-family {address_family}".format(address_family=address_family),
            "no mdt overlay use-bgp"]
    try:
        device.configure(confg)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure "no mdt overlay use-bgp under vrf definition {vrf_name}" on device'.format(
                    vrf_name=vrf_name)
        )
        
def configure_vpn_id_in_vrf(device, vrf_name, vpn_id):

    """ configure vpn id in vrf

        Args:
            device (`obj`): Device object
            vrf_name ('str'): name of the vrf
            vpn_id ('str'):  VPN ID identifies the VPN to which the IP address belongs.
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    confg = ["vrf definition {vrf_name}".format(vrf_name=vrf_name),
            "vpn id {vpn_id}".format(vpn_id=vpn_id)]
    try:
        device.configure(confg)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure "vpn id {vpn_id} under vrf definition {vrf_name}" on device'.format(
                    vpn_id=vpn_id,
                    vrf_name=vrf_name)
        )

def configure_mdt_preference_under_vrf(device, vrf_name, address_family, mdt_type):

    """ configure mdt preference type in vrf

        Args:
            device (`obj`): Device object
            vrf_name ('str'): name of the vrf
            address_family ('str'):  mention the address-family.
            mdt_type ('str'): specifies a preference for a particular MDT type.
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    confg = ["vrf definition {vrf_name}".format(vrf_name=vrf_name),
            "address-family {address_family}".format(address_family=address_family),
            "mdt preference {mdt_type}".format(mdt_type=mdt_type)]
    try:
        device.configure(confg)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure "mdt prefernce {mdt_type} under vrf definition {vrf_name}" on device'.format(
                    mdt_type=mdt_type,
                    vrf_name=vrf_name)
        )
        
def configure_default_mpls_mldp(device, vrf_name, address_family, default_mdt_group):

    """ configure mdt type in vrf

        Args:
            device (`obj`): Device object
            vrf_name ('str'): name of the vrf
            address_family ('str'):  mention the address-family.
            default_mdt_group ('str'): configures a default MDT group for a VPN VRF instance.
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    confg = ["vrf definition {vrf_name}".format(vrf_name=vrf_name),
            "address-family {address_family}".format(address_family=address_family),
            "mdt default mpls mldp  {default_mdt_group}".format(default_mdt_group=default_mdt_group)]
    try:
        device.configure(confg)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure "mdt default mpls mldp{default_mdt_group} under vrf definition {vrf_name}" on device'.format(
                    default_mdt_group=default_mdt_group,
                    vrf_name=vrf_name)
        )

def configure_mdt_data_mpls_mldp(device, vrf_name, address_family, mdt_data):

    """ configure mdt data in vrf

        Args:
            device (`obj`): Device object
            vrf_name ('str'): name of the vrf
            address_family ('str'):  mention the address-family.
            mdt_data ('str'): Specifies a range of addresses to be used in the data MDT pool.
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    confg = ["vrf definition {vrf_name}".format(vrf_name=vrf_name),
            "address-family {address_family}".format(address_family=address_family),
            "mdt data mpls mldp {mdt_data}".format(mdt_data=mdt_data)]
    try:
        device.configure(confg)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure "mdt data mpls mldp{mdt_data} under vrf definition {vrf_name}" on device'.format(
                    mdt_data=mdt_data,
                    vrf_name=vrf_name)
        )
        
def configure_multicast_routing_mvpn_vrf(device, vrf):
    """ Enables IP multicast routing for the MVPN VRF specified for the vrf-name argument.
        Args:
            device (`obj`): Device object
            vrf (`str`): VRF name
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """

    configs = "ip multicast-routing vrf {vrf}".format(vrf=vrf)
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure Multicast with Multi VRF {vrf} on device {dev}. Error:\n{error}".format(
                vrf=vrf,
                dev=device.name,
                error=e,
            )
        )
        
def configure_mdt_strict_rpf_interface_vrf(device, vrf, address_family):
    """ Enables per-PE LSPVIF interface to implement strict-RPF check.
        Args:
            device (`obj`): Device object
            vrf (`str`): VRF name
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    configs = ["vrf definition {vrf}".format(vrf=vrf),
               "address-family {address_family}".format(address_family=address_family),
               "mdt strict-rpf interface"]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure strict rpf interface with Multi VRF {vrf} on device {dev}. Error:\n{error}".format(
                vrf=vrf,
                dev=device.name,
                error=e,
            )
        )
        
def configure_mdt_partitioned_mldp_p2mp(device, vrf, address_family):
    """ Enables both IPv4 and IPv6 address-families to be configured for partitioned MDT under vrf
        Args:
            device (`obj`): Device object
            vrf (`str`): VRF name
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
 
    configs = ["vrf definition {vrf}".format(vrf=vrf),
               "address-family {address_family}".format(address_family=address_family),
               "mdt partitioned mldp p2mp"]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure mdt partitioned mldp p2mp with Multi VRF {vrf} on device {dev}. Error:\n{error}".format(
                vrf=vrf,
                dev=device.name,
                error=e,
            )
        )
        
def configure_mdt_data_threshold(device, vrf_name, address_family, threshold):

    """ configure mdt threshold in vrf

        Args:
            device (`obj`): Device object
            vrf_name ('str'): name of the vrf
            address_family ('str'):  mention the address-family.
            threshold ('int'): defines the bandwidth threshold value in kilobits per second.
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    confg = ["vrf definition {vrf_name}".format(vrf_name=vrf_name),
            "address-family {address_family}".format(address_family=address_family),
            "mdt data threshold {threshold}".format(threshold=threshold)]
    try:
        device.configure(confg)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure "mdt data threshold{threshold} under vrf definition {vrf_name}" on device'.format(
                    threshold=threshold,
                    vrf_name=vrf_name)
        )

def unconfigure_mdt_data_threshold(device, vrf_name, address_family, threshold):

    """ unconfigure mdt threshold in vrf

        Args:
            device (`obj`): Device object
            vrf_name ('str'): name of the vrf
            address_family ('str'):  mention the address-family.
            threshold ('int'): defines the bandwidth threshold value in kilobits per second.
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    confg = ["vrf definition {vrf_name}".format(vrf_name=vrf_name),
            "address-family {address_family}".format(address_family=address_family),
            "no mdt data threshold {threshold}".format(threshold=threshold)]
    try:
        device.configure(confg)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not unconfigure "mdt data threshold{threshold} under vrf definition {vrf_name}" on device'.format(
                    threshold=threshold,
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

def configure_vrf_definition_stitching(device, vrf_name, rd_value, ip_version, route_target_value, stitching_value):

    """
    Configure vrf definition for stitching ipv4 and ipv6 address family
    
    Args:
        device('obj'): Device object
        vrf_name('str'): Name of the vrf definition
        rd_value('str'): VRF RD value 1:100
        ip_version('str'): ipv4 version or ipv6 version
        route_target_value: Route target value for vrf
        stitching_value: Route-target Stitching value
    Returns:
        None
    
    Raises:
        SubCommandFailure
    
    Example of vrf definition for ipv4 address family and ipv6 address family

        vrf definition red
          rd 1:100
          !
          address-family ipv4
          route-target export 100:100
          route-target import 100:100
          route-target export 1:1 stitching
          route-target import 1:1 stitching
          exit-address-family
   
    """
    configs = []
    configs.append("vrf definition {}". format(vrf_name))
    configs.append("rd {}".format(rd_value))
    configs.append("address-family {}".format(ip_version))
    configs.append("route-target export {}".format(route_target_value))
    configs.append("route-target import {}".format(route_target_value))
    configs.append("route-target export {} stitching".format(stitching_value))
    configs.append("route-target import {} stitching".format(stitching_value))
    configs.append("exit-address-family")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Failed to configure vrf definition in global configuration mode")

def unconfigure_vrf_definition_stitching(device, vrf_name, ip_version, stitching_value):

    """
    Unconfigure stitching part for ipv4 and ipv6 address-family under vrf definition
    
    Args:
        device('obj'): Device object
        vrf_name('str'): Name of the vrf definition
        ip_version('str'): address-family to unconfigure ipv4 and ipv6 address-family.
        stitching_value: Route-target Stitching value, excample 1:1
    Returns:
        None
    
    Raises:
        SubCommandFailure
    
    Example of unconfigure stitching under vrf definition for ipv4 address family and ipv6 address family

        vrf definition red
          !
          address-family ipv4
          no route-target export 1:1 stitching
          no route-target import 1:1 stitching
          exit-address-family
          !
          address-family ipv6
          no route-target export 1:1 stitching
          no route-target import 1:1 stitching
          exit-address-family
   
    """
    unconfig = []
    unconfig.append("vrf definition {}". format(vrf_name))
    unconfig.append("address-family {}".format(ip_version))
    unconfig.append("no route-target export {} stitching".format(stitching_value))
    unconfig.append("no route-target import {} stitching".format(stitching_value))
    unconfig.append("exit-address-family")

    try:
        device.configure(unconfig)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Failed to configure vrf definition in global configuration mode")
