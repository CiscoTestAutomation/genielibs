"""Common configure functions for vrf"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.libs.sdk.apis.utils import tftp_config


log = logging.getLogger(__name__)


def configure_vrf_rd_value(
    device, vrf_name, rd_value, address_type, target_vpn_community,
    target_vpn_asn_ip_value, route_target_value_optional=''
):
    """ Configure VRF & RD Value
        Args:
            device ('obj'): device to use
            vrf_name ('str'): vrf name value (Ex: red)
            rd_value ('str'): rd vlaue (Ex: 2:100)
            address_type ('str'): address family vlaue (Ex: ipv4)
            target_vpn_community ('str'): route target transaction type (Ex: import or export)
            target_vpn_asn_ip_value ('str'): route target transaction value (Ex: 2:100, 1:100, etc)
            route_target_value_optional ('str'): route target additional value after route_target_value (Ex: stitching or '')
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure VRF & RD Value
    """
    log.info(
        "Configuring VRF & RD Value={} ".format(vrf_name)
    )

    try:
        device.configure([
            "vrf definition {}".format(vrf_name),
            "rd {}".format(rd_value),
            "address-family {}".format(address_type),
            "route-target {} {} {}".format(target_vpn_community,
                                           target_vpn_asn_ip_value,
                                           route_target_value_optional),
            "exit-address-family",
        ])

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure VRF & RD Value {defination}".format(
                defination=vrf_name
            )
        )


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


def unconfigure_vrf(device, vrf):

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


def unconfigure_vrf_definition_on_device(device, vrf_name):
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
    confg = [
        "vrf definition {vrf_name}".format(vrf_name=vrf_name),
        "address-family {address_family}".format(
            address_family=address_family),
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
    confg = [
        "vrf definition {vrf_name}".format(vrf_name=vrf_name),
        "address-family {address_family}".format(address_family=address_family),
        "no mdt overlay use-bgp"
    ]

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
    confg = [
        "vrf definition {vrf_name}".format(vrf_name=vrf_name),
        "vpn id {vpn_id}".format(vpn_id=vpn_id)
    ]

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
    confg = [
        "vrf definition {vrf_name}".format(vrf_name=vrf_name),
        "address-family {address_family}".format(address_family=address_family),
        "mdt preference {mdt_type}".format(mdt_type=mdt_type)
    ]

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
    confg = [
        "vrf definition {vrf_name}".format(vrf_name=vrf_name),
        "address-family {address_family}".format(address_family=address_family),
        "mdt data mpls mldp {mdt_data}".format(mdt_data=mdt_data)
    ]

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

def create_ip_vrf(device, vrf_name):
    """ Create ip vrf
        Args:
            device ('obj'): device to use
            vrf_name ('str'): vrf name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"ip vrf {vrf_name}"

    log.debug("Creating ip vrf")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Failed to create ip vrf"
        )


def delete_ip_vrf(device, vrf_name):
    """ Remove ip vrf
        Args:
            device ('obj'): device to use
            vrf_name ('str'): vrf name
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f"no ip vrf {vrf_name}"

    log.debug("Removing ip vrf")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Failed to remove ip vrf"
        )

def configure_ip_vrf_forwarding_interface(device, interface, vrf_name):
    """ Create ip vrf forwarding on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface name
            vrf_name ('str'): vrf name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ip vrf forwarding
    """

    cmd = []
    cmd.append(f"interface {interface}")
    cmd.append(f"ip vrf forwarding {vrf_name}")

    log.info("Creating ip vrf forwarding on interface")
    try:
        device.configure(cmd)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to configure ip vrf forwarding"
        )

def unconfigure_ip_vrf_forwarding_interface(device, interface, vrf_name):
    """ Remove ip vrf forwarding on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface name
            vrf_name ('str'): vrf name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ip vrf forwarding
    """

    cmd = []
    cmd.append(f"interface {interface}")
    cmd.append(f"no ip vrf forwarding {vrf_name}")

    log.info("Removing ip vrf forwarding")
    try:
        device.configure(cmd)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to unconfigure ip vrf forwarding"
        )


def configure_scale_vrf_via_tftp(
    device,
    server,
    vrf_name,
    vrf_name_step,
    vrf_count,
    unconfig=False,
    tftp=False):
    """ Configure scale vrfs via tftp config

        Args:
            device ('obj'): Device to use
            server ('str'): Testbed.servers
            vrf_name ('int'): Start of vrf name
            vrf_name_step ('int'): Size of vlan range step
            vrf_count ('int'): How many vrfs
            unconfig ('bool'): Unconfig or not
            tftp ('bool'): Tftp config or not

        Raises:
            Failure

        Returns:
            None
            cmds_block str if not tftp configure

    """
    cmds = ''
    if unconfig:
        for count in range(vrf_count):
            cmds += '''
            no vrf definition {vrf}
            '''.format(vrf=vrf_name)

            vrf_name += vrf_name_step
    else:
        for count in range(vrf_count):
            cmds += '''
            vrf definition {vrf}
                rd {vrf}:{vrf}
                !
                address-family ipv4
                exit-address-family
                !
                address-family ipv6
                exit-address-family
            !
            '''.format(vrf=vrf_name)

            vrf_name += vrf_name_step

    if tftp:
        try:
            tftp_config(device, server, cmds)
        except Exception:
            raise Exception('tftp_config failed.')
    else:
        return cmds


def configure_mdt_data_vxlan(device, vrf_name, address_family, ip, mask):

    """ configure mdt data vxlan network in vrf
        Args:
            device (`obj`): Device object
            vrf_name ('str'): name of the vrf
            address_family ('str'):  mention the address-family.
            ip ('str'): network ip address
            mask ('str'): mask
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring mdt data vxlan
    """
    config = [ f"vrf definition {vrf_name}",
               f"address-family {address_family}",
               f"mdt data vxlan {ip} {mask}"]

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure {config} on device {device}.Error:\n{e}'
        )


def unconfigure_mdt_data_vxlan(device, vrf_name, address_family, ip, mask):

    """ unconfigure mdt data vxlan network in vrf
        Args:
            device (`obj`): Device object
            vrf_name ('str'): name of the vrf
            address_family ('str'):  mention the address-family.
            ip ('str'): network ip address
            mask ('str'): mask
        Return:
            None
        Raise:
            SubCommandFailure: Failed unconfiguring mdt data vxlan
    """
    config = [f"vrf definition {vrf_name}",
              f"address-family {address_family}",
              f"no mdt data vxlan {ip} {mask}"]

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure {config} on device {device}.Error:\n{e}'
        )

def configure_vrf_forwarding_interface(device, interface, vrf_name):
    """ Create vrf forwarding on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface name
            vrf_name ('str'): vrf name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ip vrf forwarding
    """

    cmd = []
    cmd.append(f"interface {interface}")
    cmd.append(f"vrf forwarding {vrf_name}")

    log.info("Creating vrf forwarding on interface")
    try:
        device.configure(cmd)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to configure vrf forwarding"
        )

def unconfigure_vrf_forwarding_interface(device, interface, vrf_name):
    """ Remove vrf forwarding on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface name
            vrf_name ('str'): vrf name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ip vrf forwarding
    """

    cmd = []
    cmd.append(f"interface {interface}")
    cmd.append(f"no vrf forwarding {vrf_name}")

    log.info("Removing vrf forwarding")
    try:
        device.configure(cmd)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to unconfigure vrf forwarding"
        )

def configure_mdt_overlay_use_bgp_spt_only(device, vrf_name, address_family):

    """ configure mdt overlay under vrf
        Args:
            device ('obj'): Device object
            vrf_name ('str'): name of the vrf
            address_family ('str'):  mention the address-family.
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring vrf
    """
    confg = [
        f'vrf definition {vrf_name}'.format(vrf_name=vrf_name),
        f'address-family {address_family}'.format(
            address_family=address_family),
        f'mdt overlay use-bgp spt-only']
    try:
        device.configure(confg)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure "mdt overlay use-bgp spt-only under vrf definition {vrf_name}" on device. Error:\n{e}')

def configure_default_vxlan(device, vrf_name, address_family, multicast_group_address):

    """ configure mdt default in vxlan
        Args:
            device ('obj'): Device object
            vrf_name ('str'): name of the vrf
            address_family ('str'):  mention the address-family.
            multicast_group_address ('str'): vxlan multicast group address
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring default vxlan
    """
    confg = [f'vrf definition {vrf_name}',
            f'address-family {address_family}',
            f'mdt default vxlan  {multicast_group_address}']
    try:
        device.configure(confg)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure mdt default vxlan under vrf definition on device. Error:\n{e}')


def unconfigure_default_vxlan(device, vrf_name, address_family, multicast_group_address):

    """ Unconfigure mdt default in vxlan
        Args:
            device ('obj'): Device object
            vrf_name ('str'): name of the vrf
            address_family ('str'):  mention the address-family.
            multicast_group_address ('str'): vxlan multicast group address
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring default vxlan
    """
    confg = [f'vrf definition {vrf_name}',
             f'address-family {address_family}',
             f'no mdt default vxlan  {multicast_group_address}']
    try:
        device.configure(confg)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not unconfigure mdt default vxlan under vrf definition on device. Error:\n{e}')


def configure_mdt_auto_discovery_vxlan(device, vrf_name, address_family, keyword=""):

    """ configure mdt auto-discovery vxlan
        Args:
            device ('obj'): Device object
            vrf_name ('str'): name of the vrf
            address_family ('str'):  mention the address-family.
            keyword('str',optional): Enable Inter-AS BGP auto-discovery for vxlan
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring mdt auto-discovery on vrf
    """
    config = [f'vrf definition {vrf_name}',
             f'address-family {address_family}']
    if keyword == 'inter-as':
        config.append(f'mdt auto-discovery vxlan inter-as')
    else:
        config.append(f'mdt auto-discovery vxlan')
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure mdt auto-discovery vxlan on device vrf {vrf_name} definition. Error:\n{e}"
        )


def unconfigure_mdt_auto_discovery_vxlan(device, vrf_name, address_family):

    """ configure mdt auto-discovery vxlan
        Args:
            device (`obj`): Device object
            vrf_name ('str'): name of the vrf
            address_family ('str'):  mention the address-family.
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    confg = [f"vrf definition {vrf_name}",
             f"address-family {address_family}",
              "no mdt auto-discovery vxlan"]
    try:
        device.configure(confg)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not unconfigure "mdt auto-discovery vxlan under vrf definition {vrf_name}" on device'.format(
                    vrf_name=vrf_name)
        )


def configure_mdt_auto_discovery_inter_as(device, vrf_name, address_family):
    """ configure mdt auto-discovery inter-as
        Args:
            device ('obj'): Device object
            vrf_name ('str'): name of the vrf
            address_family ('str'):  mention the address-family.
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring mdt auto-discovery on vrf
    """
    config = [f'vrf definition {vrf_name}',
             f'address-family {address_family}',
             'mdt auto-discovery interworking vxlan-pim inter-as',
             'mdt auto-discovery pim inter-as']
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure mdt auto-discovery inter-as on device vrf {vrf_name}. Error:\n{e}")


def configure_rd_address_family_vrf(device, vrf_name, rd_name, address_family):

    """ configure rd and address family on vrf

        Args:
            device (`obj`): Device object
            vrf_name ('str'): name of the vrf
            rd_name ('str'):  IP-address:nn or 4BASN:nn  VPN Route Distinguisher
            address_family ('str'):  mention the address-family ipv4 or ipv6

        Return:
            None
        Raise:
            SubCommandFailure: Failed to configure rd and address family on vrf
    """
    confg = [
        "vrf definition {vrf_name}".format(vrf_name=vrf_name),
        "rd {rd_name}".format(rd_name=rd_name),
        "address-family {address_family}".format(
            address_family=address_family)]
    try:
        device.configure(confg)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure rd and address family on vrf {vrf_name} on device.Error:\n{e}"
        )

def configure_mdt_default(device, vrf_name, address_family, ip_address):
    """Configure mdt default
       Args:
            device ('obj'): device object
            vrf_name ('str') : vrf name
            address_family ('str'): address family
            ip_address ('str'): IP multicast group address
       Return:
            None
       Raises:
            SubCommandFailure
    """
    config= [
               f'vrf definition {vrf_name}',
               f'address-family {address_family}',
               f'mdt default {ip_address}'
            ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to Configure mdt default on {device.name}\n{e}')

def configure_mdt_auto_discovery_inter_as_mdt_type(device, vrf_name, address_family, mdt_type=None):
    """ configure mdt auto-discovery inter-as mdt type
        Args:
            device ('obj'): Device object
            vrf_name ('str'): name of the vrf
            address_family ('str'): mention the address-family ipv4 or ipv6.
            mdt_type ('str'): specify the MDT configuration type interworking or pim.
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring mdt auto-discovery on vrf
    """
    config = [
        f'vrf definition {vrf_name}',
        f'address-family {address_family}']
    if mdt_type == 'interworking':
        config.append(f'mdt auto-discovery interworking vxlan-pim inter-as')
    elif mdt_type == 'pim':
        config.append(f'mdt auto-discovery pim inter-as')
    else:
        raise ValueError(f"Invalid MDT type: {mdt_type}. Must be 'interworking' or 'pim'.")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure mdt auto-discovery inter-as mdt type on device vrf {vrf_name}. Error:\n{e}")

def configure_data_mdt(device, vrf_name, address_family, ip_address, wildcard_mask, threshold):
    """ Configure Data MDT
        Args:
            device ('obj'): Device object
            vrf_name ('str'): VRF name
            address_family ('str'): Address family (e.g., ipv4, ipv6)
            ip_address ('str'): IP address
            wildcard_mask ('str'): Wildcard mask
            threshold ('int'): Threshold value
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure Data MDT
    """
    config = [
        f"vrf definition {vrf_name}",
        f"address-family {address_family}",
        f"mdt data {ip_address} {wildcard_mask} threshold {threshold}"
    ]

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure Data MDT on device {device.name}. Error:\n{e}"
        )

def configure_vrf_rd_rt(device, vrf_name, rd, rt):
    """ Configure VRF RD and RT
        Args:
            device ('obj'): Device object
            vrf_name ('str'): VRF name(Mgmt-vrf, VRF1, etc.)
            rd ('str'): VPN Route Distinguisher(ASN:nn, IP-address:nn or 4BASN:nn)
            rt ('str'): Target VPN Extended Community(both, import, export)
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure VRF RD and RT
    """
    config = [
        f'ip vrf {vrf_name}',
        f'rd {rd}',
        f'route-target {rt} {rd}'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure VRF RD and RT on device {device.name}. Error:\n{e}"
        )
