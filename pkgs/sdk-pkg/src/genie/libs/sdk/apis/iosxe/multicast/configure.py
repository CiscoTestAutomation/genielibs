"""Common configure functions for pim"""

# Python
import logging
from unicon.eal.dialogs import Statement, Dialog

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.libs.conf.base import IPv4Address
from genie.libs.sdk.apis.utils import tftp_config

log = logging.getLogger(__name__)


def config_ip_pim(device, interface, mode):
    """ Enables PIM sparse mode on an interface.

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            mode (`str`): specifiy pim mode
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    log.info("Configuring pim mode on {interface} on {device}"\
        .format(interface=interface, device=device.name))

    configs = "interface {intf} \n".format(intf=interface)
    configs += "ip pim {mode}".format(mode=mode)
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure ip pim {mode} on interface {interface} on device {dev}. Error:\n{error}".format(
                mode=mode,
                interface=interface,
                dev=device.name,
                error=e,
            )
        )
        
def config_rp_address(device, vrf, ip_address):
    """Configures a static IP address of a rendezvous point for a multicast group range.

        Args:
            device (`obj`): Device object
            vrf (`str`): VRF name
            ip_address (`str`): IP address of the group-range 
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring rp address
    """
    log.info("Configuring rp address for a multicast vrf {vrf} on {device}"\
        .format(vrf=vrf, device=device.name))

    configs = "ip pim vrf {vrf} rp-address {ip_address}".format(vrf=vrf,ip_address=ip_address)
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure rp-address {ip_address} for a multicast vrf {vrf} on device {dev}. Error:\n{error}".format(
                ip_address=ip_address,
                vrf=vrf,
                dev=device.name,
                error=e,
            )
        )

def config_multicast_routing_mvpn_vrf(device, vrf):
    """ Enables IP multicast routing for the MVPN VRF specified for the vrf-name argument.

        Args:
            device (`obj`): Device object
            vrf (`str`): VRF name
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    log.info("Configuring multicast routing for the MVPN VRF {vrf} on {device}"\
        .format(vrf=vrf, device=device.name))

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
    
def configure_igmp_version(device, interface, version):
    """configures the IGMP version that the switch uses on interfaces.

        Args:
            device (`obj`): Device object
            interface (`str`): mentions interface name
            version (`int`): specifies the IGMP version that the switch uses.
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """

    configs = "interface {interface}".format(interface=interface)
    configs += "\n ip igmp version {version}".format(version=version)
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure IGMP version {version} on {interface} on device {dev}. Error:\n{error}".format(
                version=version,
                interface=interface,
                dev=device.name,
                error=e,
            )
        )
        
def unconfigure_igmp_version(device, interface, version):
    """configures the IGMP version that the switch uses on interfaces.

        Args:
            device (`obj`): Device object
            interface (`str`): mentions interface name
            version (`int`): specifies the IGMP version that the switch uses.
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """

    configs = "interface {interface}".format(interface=interface)
    configs += "\n no ip igmp version {version}".format(version=version)
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure IGMP version {version} on {interface} on device {dev}. Error:\n{error}".format(
                version=version,
                interface=interface,
                dev=device.name,
                error=e,
            )
        )
        
def configure_ip_pim_vrf_ssm_default(device, vrf):
    """configure ip pim vrf ssm default on device.
        Args:
            device (`obj`): Device object
            vrf (`str`): VRF name
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """

    configs = "ip pim vrf {vrf} ssm default".format(vrf=vrf)
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure ip pim vrf {vrf} ssm default on device {dev}. Error:\n{error}".format(
                vrf=vrf,
                dev=device.name,
                error=e,
            )
        )

def unconfigure_ip_pim_vrf_ssm_default(device, vrf):
    """unconfigure ip pim vrf ssm default on device
        Args:
            device (`obj`): Device object
            vrf (`str`): VRF name
        Return:
            None
        Raise:
            SubCommandFailure: Failed unconfiguring interface
    """

    configs = "no ip pim vrf {vrf} ssm default".format(vrf=vrf)
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure ip pim vrf {vrf} ssm default on device {dev}. Error:\n{error}".format(
                vrf=vrf,
                dev=device.name,
                error=e,
            )
        )

def config_standard_acl_for_ip_pim(
        device,
        acl_name,
        permission,
        host_ip,
        host_wildcard,
        vrf,
        rp_address,
        bir_enabled=False
):
    """ Configures a standard IP access list.
        Args:
            device ('obj'): device object
            acl_name ('str'): acl name
            permission ('str'): (permit | deny)
            host_ip ('str'): source start ip
            host_wildcard ('str'): increment step for source ip
            vrf ('str'): vrf name
            rp_address ('str'): mention the IP address of the rendezvous point for the group.
            bir_enabled ('boolean', optional): sets true if enabled.  Defaults to False.
        Returns:
            config
        Raises:
            SubCommandFailure: Failed to configure access-list
    """
    configs = []
    configs.append("ip access-list standard {}".format(acl_name))
    configs.append("{permission} {host_ip} {host_wildcard}".format(
                permission=permission, host_ip=host_ip, host_wildcard=host_wildcard))
    if bir_enabled:
        configs.append("ip pim bidir-enable")
        configs.append("ip pim vrf {vrf} rp-address {rp_address} {acl_name} bidir".format(
                    vrf=vrf, rp_address=rp_address, acl_name=acl_name))
    else:
        configs.append("ip pim vrf {vrf} rp-address {rp_address} {acl_name}".format(
                    vrf=vrf, rp_address=rp_address, acl_name=acl_name))   
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure Access-list {acl} on device {dev}. Error:\n{error}".format(
                acl=acl_name,
                dev=device.name,
                error=e,
            )
        )
        
def unconfig_standard_acl_for_ip_pim(
        device,
        acl_name,
):
    """ Configures a standard IP access list.
        Args:
            device ('obj'): device object
            acl_name ('str'): acl name
        Returns:
            config
        Raises:
            SubCommandFailure: Failed to configure access-list
    """
    try:
        device.configure("no ip access-list standard {}".format(acl_name))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure Access-list {acl} on device {dev}. Error:\n{error}".format(
                acl=acl_name,
                dev=device.name,
                error=e,
            )
        )

def configure_static_ip_pim_rp_address(device,ip_address,vrf=None):
    """Configures a static IP address of a rendezvous point for a multicast group range.

    Args:
        device (`obj`): Device object
        vrf (`str`): VRF name
        ip_address (`str`): IP address of the group-range
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring rp address
    """
    log.info("Configuring rp address on {device}".format(device=device.name))
    if vrf == None:
       configs = "ip pim rp-address {ip_address}".format(ip_address=ip_address)
    else:
       configs = "ip pim vrf {vrf} rp-address {ip_address}".format(vrf=vrf,ip_address=ip_address)
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Failed to configure rp-address {ip_address} device {dev}. Error:\n{error}".format(ip_address=ip_address,dev=device.name,error=e)
        )

def configure_static_ipv6_pim_rp_address(device,ipv6_address,vrf=None):
    """Configures a static IPv6 address of a rendezvous point for a multicast group range.

    Args:
        device (`obj`): Device object
        vrf (`str`): VRF name
        ip_address (`str`): IPv6 address of rp
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring rp address
    """
    log.info("Configuring rp address on {device}".format(device=device.name))
    if vrf==None:
        configs = "ipv6 pim rp-address {ipv6_address}".format(ipv6_address=ipv6_address)
    else:
        configs = "ipv6 pim vrf {vrf} rp-address {ipv6_address}".format(vrf=vrf,ipv6_address=ipv6_address)
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Failed to configure rp-address {ipv6_address} on device {dev}. Error:\n{error}".format(ipv6_address=ipv6_address,vrf=vrf,dev=device.name,error=e)
        )

def unconfigure_static_ip_pim_rp_address(device,ip_address,vrf=None):
    """Unconfigures a static IP address of a rendezvous point for a multicast group range.

    Args:
        device (`obj`): Device object
        vrf (`str`): VRF name
        ip_address (`str`): IP address of the group-range
    Return:
        None
    Raise:
        SubCommandFailure: Failed unconfiguring rp address
    """
    log.info("Unconfiguring rp address on {device}".format(device=device.name))
    if vrf == None:
       configs = "no ip pim rp-address {ip_address}".format(ip_address=ip_address)
    else:
       configs = "no ip pim vrf {vrf} rp-address {ip_address}".format(vrf=vrf,ip_address=ip_address)
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Failed to unconfigure rp-address {ip_address} device {dev}. Error:\n{error}".format(ip_address=ip_address,dev=device.name,error=e)
        )

def unconfigure_static_ipv6_pim_rp_address(device,ipv6_address,vrf=None):
    """Unconfigures a static IPv6 address of a rendezvous point for a multicast group range.

    Args:
        device (`obj`): Device object
        vrf (`str`): VRF name
        ip_address (`str`): IPv6 address of rp
    Return:
        None
    Raise:
        SubCommandFailure: Failed unconfiguring rp address
    """
    log.info("Unconfiguring rp address on {device}".format(device=device.name))
    if vrf==None:
        configs = "no ipv6 pim rp-address {ipv6_address}".format(ipv6_address=ipv6_address)
    else:
        configs = "no ipv6 pim vrf {vrf} rp-address {ipv6_address}".format(vrf=vrf,ipv6_address=ipv6_address)
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Failed to unconfigure rp-address {ipv6_address} on device {dev}. Error:\n{error}".format(ipv6_address=ipv6_address,vrf=vrf,dev=device.name,error=e)
        )

def configure_ipv6_multicast_routing(device):
    """ Configure Enable IPv6 multicast routing
    Args:
        device (`obj`): Device object
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "ipv6 multicast-routing"
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ipv6 multicast routing. Error:\n{error}".format(error=e)
        )

def unconfigure_ipv6_multicast_routing(device):
    """ Configure Enable IPv6 multicast routing
    Args:
        device (`obj`): Device object
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """

    try:
        device.configure("no ipv6 multicast-routing")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure Multicast routing. Error:\n{error}".format(error=e)
        )


def configure_scale_igmp_groups_via_tftp(device,
                                         server,
                                         intf_name,
                                         group_mode,
                                         group_start,
                                         group_step,
                                         goup_count,
                                         unconfig=False,
                                         tftp=False):
    """ configure ip igmp static/join group on device interface
        Example :
        interface GigabitEthernet4
            ip igmp join-group 235.0.0.1
            ip igmp join-group 235.0.0.2

        Args:
            device ('obj'): Device to use
            server ('str'): Testbed.servers
            intf_name ('str'): Interface name
            group_mode ('str'): static-group or join-group
            group_start ('str'): Start IP of multicast groups. eg.235.0.0.1
            group_step ('str'): Size of multicast group step. eg.0.0.0.1
            goup_count ('int'): How many groups
            unconfig ('bool'): Unconfig or not
            tftp ('bool'): Tftp config or not
        Returns:
            None
            cmds_block str if not tftp configure
    """
    cmds = ''
    if unconfig:
        no_str = 'no'
    else:
        no_str = ''

    mcast_group = IPv4Address(group_start)

    for count in range(goup_count):
        cmds += '''
        interface {intf}
            {no_str} ip igmp {group_mode} {mcast_group}
        '''.format(intf=intf_name,
                   no_str=no_str,
                   group_mode=group_mode,
                   mcast_group=mcast_group)

        mcast_group += int(IPv4Address(group_step))

    if tftp:
        try:
            tftp_config(device, server, cmds)
        except Exception:
            raise Exception('tftp_config failed.')
    else:
        return cmds


def configure_scale_service_reflection_via_tftp(device,
                                                server,
                                                intf_name,
                                                src_filter_intf,
                                                dst_pre_trans,
                                                dst_pre_trans_step,
                                                dst_after_trans,
                                                dst_after_trans_step,
                                                mask_len,
                                                src_after_trans,
                                                src_after_trans_step,
                                                sr_count,
                                                unconfig=False,
                                                tftp=False):
    """ configure ip service reflection on device VIF interface
        Example :
        interface Vif1
            ip service reflect GigabitEthernet0/0/2 destination 66.3.1.0 to 232.2.2.0 mask-len 24 source 110.1.0.4

        Args:
            device ('obj'): Device to use
            server ('str'): Testbed.servers
            intf_name ('str'): Interface name VIF1
            src_filter_intf ('str'): Source filter interface GigabitEthernet0/0/2 or ''
            dst_pre_trans ('str'): Dst ip before translation eg.66.3.1.0
            dst_pre_trans_step ('str'): Step of dst ip before translation. eg.0.0.1.0
            dst_after_trans ('str'): Dst ip after translation eg.232.2.2.0
            dst_after_trans_step ('str'): Step of dst ip before translation. eg.0.0.1.0
            mask_len ('int'): mask length of prefix. eg.24
            src_after_trans ('str'): Src ip after translation eg.110.1.0.4
            src_after_trans_step ('str'): Step of Src ip after translation. eg.0.0.0.1
            sr_count ('int'): How many service reflection rules
            unconfig ('bool'): Unconfig or not
            tftp ('bool'): Tftp config or not
        Returns:
            None
            cmds_block str if not tftp configure
    """
    cmds = ''
    if unconfig:
        no_str = 'no'
    else:
        no_str = ''

    dst_prefix = IPv4Address(dst_pre_trans)
    dst_mcast_group = IPv4Address(dst_after_trans)
    translated_src = IPv4Address(src_after_trans)

    for count in range(sr_count):
        cmds += '''
        interface {intfVIF}
            {no_str} ip service reflect {sr_filter} destination {dst_prefix} to {dst_mcast_group} mask-len {mask} source {src}
        '''.format(intfVIF=intf_name,
                   sr_filter=src_filter_intf,
                   dst_prefix=dst_prefix,
                   dst_mcast_group=dst_mcast_group,
                   mask=mask_len,
                   src=translated_src,
                   no_str=no_str)

        dst_prefix += int(IPv4Address(dst_pre_trans_step))
        dst_mcast_group += int(IPv4Address(dst_after_trans_step))
        translated_src += int(IPv4Address(src_after_trans_step))

    if tftp:
        try:
            tftp_config(device, server, cmds)
        except Exception:
            raise Exception('tftp_config failed.')
    else:
        return cmds
