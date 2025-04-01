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


def configure_ipv6_pim_bsr_candidate_bsr(device, ipv6_address, candidate_filter=None,
                                         priority=None, scope=None, mask_length=None, vrf=None):
    """ Configure ipv6 pim candidate bsr
    Args:
        device ('obj'): Device object
        ipv6_address ('str'): ipv6_address for candidate
        mask_length ('int'): BSR Hash mask length
        candidate_filter ('str', optional): RP candidate filter
        priority ('int', optional):BSR Priority
        scope ('int', optional):IPv6 Scope value
        vrf ('str', optional): vrf name
    Returns:
        None
    Raises:
        SubCommandFailure : Failed to configure ipv6 pim candidate bsr
    """

    log.info(f"Configure ipv6 pim candidate bsr")

    if vrf:
        cmd = f"ipv6 pim vrf {vrf} bsr candidate bsr {ipv6_address}"
    else:
        cmd = f"ipv6 pim bsr candidate bsr {ipv6_address}"

    if mask_length:
        cmd += f" {mask_length}"
    if priority:
        cmd += f" priority {priority}"
    if scope:
        cmd += f" scope {scope}"
    if candidate_filter:
        cmd += f" accept-rp-candidate {candidate_filter}"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipv6 pim candidate bsr, Error:\n{e}"
        )


def configure_ipv6_pim_bsr_candidate_rp(device, ipv6_address, group_list=None, priority=None,
                                        interval=None, scope=None, bidir=False, vrf=None):
    """ Configure ipv6 pim candidate rp
    Args:
        device ('obj'): Device object
        ipv6_address ('str'): ipv6_address for candidate
        group_list ('str', optional): Group list
        priority ('int', optional): priority for configured RP
        interval ('int', optional): advertisement interval for configured RP
        scope ('int', optional):IPv6 Scope value
        bidir ('bool', optional): configure a bidir RP
        vrf ('str', optional): vrf name
    Returns:
        None
    Raises:
        SubCommandFailure : Failed to configure ipv6 pim candidate rp
    """

    log.info(f"Configure ipv6 pim candidate rp")

    if vrf:
        cmd = f"ipv6 pim vrf {vrf} bsr candidate rp {ipv6_address}"
    else:
        cmd = f"ipv6 pim bsr candidate rp {ipv6_address}"
    if group_list:
        cmd += f" group-list {group_list}"
    if interval:
        cmd += f" interval {interval}"
    if priority:
        cmd += f" priority {priority}"
    if bidir:
        cmd += " bidir"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipv6 pim candidate rp, Error:\n{e}"
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

def configure_ip_multicast_routing_distributed(device, no_spd=False, punt_limit=None):
    """Configure IP multicast routing
    Args:
        device (`obj`): Device object
        no_spd (): If True, turn off selective packet discard. Default False.
        punt_limit (`str` or `int`): Punt limit. Acceptable values are:
                                     integer (packets per second)
                                     default
                                     disable
    Return:
        None
    Raise:
        SubCommandFailure: Failure while configuring
    """
    if punt_limit and not isinstance(punt_limit, int):
        if punt_limit not in ["default", "disable"]:
            raise SubCommandFailure(
                f"Invalid punt limit. Expected: integer/'default'/'disable', got {punt_limit}"
            )
    cmd = "ip multicast-routing distributed"
    if no_spd:
        cmd += " no-spd"
    if punt_limit:
        cmd += f" punt-limit {punt_limit}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ip multicast routing distributed. Error:\n{e}"
        )

def unconfigure_ip_multicast_routing_distributed(device, no_spd=False, punt_limit=None):
    """Unconfigure IP multicast routing
    Args:
        device (`obj`): Device object
        no_spd (): Selective packet discard
        punt_limit (`str` or `int`): Punt limit. Acceptable values are:
                                     integer (packets per second)
                                     default
                                     disable
    Return:
        None
    Raise:
        SubCommandFailure: Failure while configuring
    """
    if punt_limit and not isinstance(punt_limit, int):
        if punt_limit not in ["default", "disable"]:
            raise SubCommandFailure(
                f"Invalid punt limit. Expected: integer/'default'/'disable', got {punt_limit}"
            )
    cmd = "no ip multicast-routing distributed"
    if no_spd:
        cmd += " no-spd"
    if punt_limit:
        cmd += f" punt-limit {punt_limit}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ip multicast routing distributed. Error:\n{e}"
        )

def configure_ipv6_multicast_routing(device, vrf_name=None):
    """ Configure Enable IPv6 multicast routing
    Args:
        device ('obj'): Device object
        vrf_name('str', optional): Name of vrf for which we are enabling multicast-routing
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    config = f"ipv6 multicast-routing{f' vrf {vrf_name}' if vrf_name else ''}"

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ipv6 multicast routing. Error:\n{error}".format(error=e)
        )

def unconfigure_ipv6_multicast_routing(device, vrf_name=None):
    """ Unconfigure IPv6 multicast routing
    Args:
        device ('obj'): Device object
        vrf_name('str', optional): Name of vrf for which we are removing multicast-routing
    Return:
        None
    Raise:
        SubCommandFailure: Failed unconfiguring
    """
    config = f"no ipv6 multicast-routing{f' vrf {vrf_name}' if vrf_name else ''}"

    try:
        device.configure(config)
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

def configure_ip_pim_bsr_candidate(device, interface, mask_length):
    """ Configure ip pim bsr-candidate on interface <interface>
        Args:
            device ('obj'): Device object
            interface('str'): interface details on which we config
            mask_length('int'): Hash Mask length for RP selection
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to configure ip pim bsr-candidate on interface
    """

    log.debug(f"Configure ip pim bsr-candidate on interface {interface}")

    cmd = f"ip pim bsr-candidate {interface} {mask_length}"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to Configure ip pim bsr-candidate on interface {interface}. Error:\n{e}"
        )

def configure_ip_pim_rp_candidate_priority(device, interface, priority_value):
    """ Configure ip pim rp-candidate priority on device
        Args:
            device ('obj'): Device object
            interface('str'): interface details on which we config
            priority_value('int'): priority value to be set
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to configure ip pim rp-candidate priority on device
    """

    log.debug(f"Configure ip pim rp-candidate priority on device")

    cmd = f"ip pim rp-candidate {interface} priority {priority_value}"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to Configure ip pim rp-candidate priority on device {device}. Error:\n{e}"
        )

def configure_ip_igmp_snooping_tcn_flood(device, query_count):
    """ Configures flood query count to IGMP snooping TCN behavior
        Example : ip igmp snooping tcn flood query count 3

        Args:
            device ('obj'): device to use
            query_count ('int'): number of multicast traffic queries (1-10)

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info("configuring flood query count on ip igmp snooping tcn on {device}".format(
        device=device.name, count=query_count
        )
    )
    configs = "ip igmp snooping tcn flood query count {count}".format(count=query_count)
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Failed to configure query count {count} on device {dev}. Error:\n{error}".format(
                count=query_count,
                dev=device.name,
                error=e
            )
        )

def unconfigure_ip_igmp_snooping_tcn_flood(device):
    """ Unconfigures flood query count to IGMP snooping TCN behavior
        Example : no ip igmp snooping tcn flood query count

        Args:
            device ('obj'): device to use

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info("unconfiguring ip igmp snooping tcn flood query count on {device}".format(
        device=device.name
        )
    )
    configs = "no ip igmp snooping tcn flood query count"
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Failed to unconfigure flood query count on device {dev}. Error:\n{error}".format(
                dev=device.name,
                error=e
            )
        )

def configure_ip_igmp_snooping_last_member_query_interval(device, time):
    """ Configures the IGMP last-member query interval on an interface
        Example : ip igmp snooping last-member-query-interval 1500

        Args:
            device ('obj'): device to use
            time ('int'): interval, in milliseconds, at which host query messages are sent (100-25500)

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info("configuring IGMP last-member query interval on {device}".format(
        device=device.name
        )
    )
    configs = "ip igmp snooping last-member-query-interval {time}".format(time=time)
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Failed to configure last-member-query-interval {time} on device {dev}. Error:\n{error}".format(
                time=time,
                dev=device.name,
                error=e
            )
        )

def unconfigure_ip_igmp_snooping_last_member_query_interval(device):
    """ Restore the default IGMP query interval on an interface
        Example : no ip igmp snooping last-member-query-interval

        Args:
            device ('obj'): device to use

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info("Restoring default query interval on {device}".format(
        device=device.name
        )
    )
    configs = "no ip igmp snooping last-member-query-interval"
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Failed to restore default query interval on device {dev}. Error:\n{error}".format(
                dev=device.name,
                error=e
            )
        )


def configure_ipv6_mld_vlan_immediate_leave(device, id):
    """ Configure Enable IPv6 mld vlan immediate leave
    Args:
        device (`obj`): Device object
        id ('int'): VLAN ID
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "ipv6 mld snooping vlan {id} immediate-leave".format(id=id)
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ipv6 mld vlan {id} immediate-leave. Error:\n{error}".format(id=id, error=e)
        )

def unconfigure_ipv6_mld_vlan_immediate_leave(device, id):
    """ Unconfigure Enable IPv6 mld vlan immediate leave
    Args:
        device (`obj`): Device object
        id ('int'): VLAN ID
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "no ipv6 mld snooping vlan {id} immediate-leave".format(id=id)
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure ipv6 mld vlan {id} immediate-leave. Error:\n{error}".format(id=id, error=e)
        )


def configure_ipv6_mld_vlan(device, id):
    """ Configure Enable IPv6 mld vlan
    Args:
        device (`obj`): Device object
        id ('int'): VLAN ID
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "ipv6 mld snooping vlan {id}".format(id=id)
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ipv6 mld vlan {id}. Error:\n{error}".format(id=id, error=e)
        )

def unconfigure_ipv6_mld_vlan(device, id):
    """ Unconfigure Enable IPv6 mld vlan
    Args:
        device (`obj`): Device object
        id ('int'): VLAN ID
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "no ipv6 mld snooping vlan {id}".format(id=id)
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure ipv6 mld vlan {id}. Error:\n{error}".format(id=id, error=e)
        )


def configure_ipv6_pim_rp_address(device, address):
    """ Configure Enable ipv6 pim rp-address
    Args:
        device (`obj`): Device object
        address ('str'): rp address
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "ipv6 pim rp-address {address}".format(address=address)
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ipv6 pim rp-address {address}. Error:\n{error}".format(naaddressme=address, error=e)
        )

def unconfigure_ipv6_pim_rp_address(device, address):
    """ Unconfigure Enable ipv6 pim rp-address
    Args:
        device (`obj`): Device object
        address ('str'): ipv6 address
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "no ipv6 pim rp-address {address}".format(address=address)
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure ipv6 pim rp-address {address}. Error:\n{error}".format(address=address, error=e)
        )

def configure_ipv6_mld_join_group(device, address, interface_id):
    """ Configure Enable ipv6 mld join-group
    Args:
        device (`obj`): Device object
        address ('str'): ipv6 address
        interface_id ('str'): id of the interface to be configured
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    cmd = [
            f"interface {interface_id}",
            f"ipv6 mld join-group {address}",
          ]
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ipv6 mld join-group  {address}. Error:\n{error}".format(address=address, error=e)
        )
def unconfigure_ipv6_mld_join_group(device, address, interface_id):
    """ Unconfigure Enable ipv6 mld join-group
    Args:
        device (`obj`): Device object
        address ('str'): ipv6 address
        interface_id ('str'): id of the interface to be configured
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    cmd = [
            f"interface {interface_id}",
            f"no ipv6 mld join-group {address}",
          ]
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure ipv6 mld join-group  {address}. Error:\n{error}".format(address=address, error=e)
        )

def configure_ipv6_mld_snooping_vlan_static_interface(device, vlan_id, address, interface_id):
    """ Configure Enable ipv6 mld snooping vlan static interfac
    Args:
        device (`obj`): Device object
        address ('str'): ipv6 address
        interface_id ('str'): id of the interface to be configured
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """

    try:
        device.configure(f"ipv6 mld snooping vlan {vlan_id} static {address} interface {interface_id}")

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ipv6 mld join-group  {address}. Error:\n{error}".format(address=address, error=e)
        )

def unconfigure_ipv6_mld_snooping_vlan_static_interface(device, vlan_id, address, interface_id):
    """ Unconfigure Enable ipv6 mld snooping vlan static interfac
    Args:
        device (`obj`): Device object
        address ('str'): ipv6 address
        interface_id ('str'): id of the interface to be configured
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """

    try:
        device.configure(f"no ipv6 mld snooping vlan {vlan_id} static {address} interface {interface_id}")

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure ipv6 mld join-group  {address}. Error:\n{error}".format(address=address, error=e)
        )

def unconfigure_ipv6_mld_snooping_vlan_mrouter_interface(device, vlan_id, interface_id):
    """ Unconfigure ipv6 mld snooping vlan <vlan-id> mrouter interface <interface-id>
    Args:
        device (`obj`): Device object
        vlan_id ('int'): vlan id to unconfigure
        interface_id ('str'): interface id
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    cmd = f"no ipv6 mld snooping vlan {vlan_id} mrouter interface {interface_id}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure Multicast routing. Error:\n{error}".format(error=e)
        )

def configure_clear_ipv6_mld_counters(device):
    """ Configure clear ipv6 mld counters
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Clear ipv6 mld counters on {device}".format(device=device))

    try:
        device.execute('clear ipv6 mld counters')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear ipv6 mld counters on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )


def configure_ip_igmp_ssm_map_enable(device):
    """ Configure ip igmp ssm-map enable
    Args:
        device (`obj`): Device object
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    cmd = f"ip igmp ssm-map enable"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ip igmp ssm-map enable. Error:\n{error}".format(error=e)
        )

def configure_ip_igmp_snooping_vlan_mrouter_interface(device, vlan_id, interface_id):
    """ Configure ip igmp snooping vlan mrouter interface
    Args:
        device (`obj`): Device object
        vlan_id ('int'): vlan id
        interfac_id ('str'): interface id
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    cmd = f"ip igmp snooping vlan {vlan_id} mrouter interface {interface_id}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ip igmp snooping vlan mrouter interface. Error:\n{error}".format(error=e)
        )

def configure_debug_ip_pim(device):
    """ Configure debug ip pim
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.execute('debug ip pim')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not debug ip pim on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_ip_igmp_snooping_vlan_static_ipaddr_interface(device, vlan_id, ip_add, interface_name, port):
    """ Configure ip igmp snooping vlan static ipaddr interface
    Args:
        device (`obj`): Device object
        vlan_id ('int'): vlan id
        ip_add ('str'):  ip address
        interface_name ('str'): the name of interface
        port ('int'): port number
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    cmd = f"ip igmp snooping vlan {vlan_id} static {ip_add} interface {interface_name} {port} "
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ip igmp snooping vlan static ipaddr interface. Error:\n{error}".format(error=e)
        )

def configure_ip_igmp_snooping_vlan_mrouter_learn_pim_dvmrp(device, vlan_id):
    """ Configure ip igmp snooping vlan mrouter learn pim-dvmrp
    Args:
        device (`obj`): Device object
        vlan_id ('int'): vlan id

    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    cmd = f"ip igmp snooping vlan {vlan_id} mrouter learn pim-dvmrp "
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ip igmp snooping vlan mrouter learn pim-dvmrp . Error:\n{error}".format(error=e)
        )


def configure_ip_igmp_join_group_source(device, interface, group_address, source_address=""):
    """ Configures ip igmp join-group to an vlan interface
        Example : ip igmp join-group 239.100.100.101 source 4.4.4.4

        Args:
            device ('obj'): device to use
            interface ('str'): interface or Vlan number (Eg. ten1/0/1 or vlan 10)
            group_address ('str'): IP group addres
            source_address ('str', optional): IP source address

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring ip igmp join-group on {device.name}")
    config = [f"interface {interface}"]
    if source_address:
        config.append(f"ip igmp join-group {group_address} source {source_address}")
    else:
        config.append(f"ip igmp join-group {group_address}")

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ip igmp join-group on device {device.name}. Error:\n{e}")

def configure_ip_igmp_ssmmap_static(device, acl_name, source_address):
    """ Configure ip igmp ssm-map static
    Args:
        device ('obj'): Device object
        acl_name ('int'): acl name
        source_address ('str'): ssm source address

    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    cmd = f"ip igmp ssm-map static {acl_name} {source_address}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ip igmp ssm-map static {acl_name} {source_address}. Error:\n{e}")

def configure_ip_igmp_ssm_map(device):
    """ Configures ip igmp ssm-map
        Example : ip igmp ssm-map enable

        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring ip igmp ssm-map on {device.name}")
    cmd = "ip igmp ssm-map enable"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ip igmp ssm-map on device {device.name}. Error:\n{e}")

def unconfigure_ip_igmp_ssm_map(device):
    """ Unconfigures ip igmp ssm-map
        Example : no ip igmp ssm-map enable

        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring ip igmp ssm-map on {device.name}")
    cmd = "no ip igmp ssm-map enable"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure ip igmp ssm-map on device {device.name}. Error:\n{e}")

def configure_ip_igmp_ssm_map_query_dns(device):
    """ Configures ip igmp ssm-map query dns
        Example : ip igmp ssm-map query dns

        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring ip igmp ssm-map query dns on {device.name}")
    cmd = "ip igmp ssm-map query dns"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ssm-map query dns on device {device.name}. Error:\n{e}")

def unconfigure_ip_igmp_ssm_map_query_dns(device):
    """ Unconfigures ip igmp ssm-map query dns
        Example : no ip igmp ssm-map query dns

        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring ip igmp ssm-map query dns on {device.name}")
    cmd = "no ip igmp ssm-map query dns"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure ssm-map query dns on device {device.name}. Error:\n{e}")

def enable_ip_igmp_snooping_report_suppression(device):
    """ Enables a limit on membership report traffic sent to multicast-capable routers
        Example : ip igmp snooping report-suppression

        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Enabling igmp report-suppression on {device.name}")
    try:
        device.configure("ip igmp snooping report-suppression")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to enable igmp report-suppression on device {device.name}. Error:\n{e}")

def disable_ip_igmp_snooping_report_suppression(device):
    """ Disables the report-suppression
        Example : no ip igmp snooping report-suppression

        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Disabling igmp report-suppression on {device.name}")
    try:
        device.configure("no ip igmp snooping report-suppression")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to disable igmp report-suppression on device {device.name}. Error:\n{e}")

def unconfigure_ip_igmp_ssmmap_static(device, acl_name, source_address):
    """ Unconfigure ip igmp ssm-map static
    Args:
        device ('obj'): Device object
        acl_name ('int'): acl name
        source_address ('str'): ssm source address
    Return:
        None
    Raise:
        SubCommandFailure: Failed to Unconfigure
    """
    cmd = f"no ip igmp ssm-map static {acl_name} {source_address}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not Unconfigure ip igmp ssm-map static {acl_name} {source_address}. Error:\n{e}")

def configure_ip_igmp_access_group(device, interface, acl_name):
    """ Configure ip igmp access_group
    Args:
        device ('obj'): Device object
        interface ('int'): interface to configure
        acl_name ('int'): acl name
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    cmd = [f'interface {interface}',
	       f'ip igmp access-group {acl_name}']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ip igmp access-group {acl_name} on interface. Error:\n{e}")

def configure_ipv6_mld_snooping_vlan_mrouter_interface(device, vlan_id, interface_id):
    """ configure ipv6 mld snooping vlan <vlan-id> mrouter interface <interface-id>

    Args:
        device ('obj'): Device object
        vlan_id ('int'): vlan id to unconfigure
        interface_id ('str'): interface id
    Return:
        None
    Raise:
        SubCommandFailure: Failed unconfigure rp address
    """
    cmd = f"ipv6 mld snooping vlan {vlan_id} mrouter interface {interface_id}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Could not configure ipv6 mld snooping vlan. Error:\n{error}".format(error=e))

def configure_ip_pim_enable_bidir_enable(device):
    """ configure ip pim bidir
        Example : ip pim bidir-enable

        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("ip pim bidir-enable")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ip pim bidir on device {device.name}. Error:\n{e}")


def unconfigure_ip_pim_enable_bidir_enable(device):
    """ unconfigure ip pim bidir
        Example : ip pim bidir-enable

        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("no ip pim bidir-enable")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure ip pim bidir on device {device.name}. Error:\n{e}")


def configure_ip_pim_rp_address(device, ip_address, option):
    """Configures a IP pim address group range

    Args:
        device ('obj'): Device object
        ip_address ('str'): IP address
        option ('str') : can be user choice bidir,override, ccess-list reference for group <1-99> or <1300-1999>

    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring rp address
    """
    cmd = f"ip pim rp-address {ip_address} {option}"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Failed to configure ip pim rp-address {device.name}. Error:\n{e}")


def unconfigure_ip_pim_rp_address(device, ip_address, option):
    """unconfigures  IP pim address group range

    Args:
        device ('obj'): Device object
        ip_address ('str'): IP address
        option ('str') : can be user choice bidir,override, ccess-list reference for group <1-99> or <1300-1999>

    Return:
        None
    Raise:
        SubCommandFailure: Failed unconfigure rp address
    """
    cmd = f"no ip pim rp-address {ip_address} {option}"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Failed to unconfigure ip pim rp-address {device.name}. Error:\n{e}")

def unconfigure_ip_igmp_join_group_source(device, interface, group_address, source_address=""):
    """ unconfigures ip igmp join-group to an vlan interface
        Example : ip igmp join-group 239.100.100.101 source 4.4.4.4
        Args:
            device ('obj'): device to use
            interface ('str'): interface or Vlan number (Eg. ten1/0/1 or vlan 10)
            group_address ('str'): IP group addres
            source_address ('str', optional): IP source address
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring ip igmp join-group on {device.name}")
    config = [f"interface {interface}"]
    if source_address:
        config.append(f"no ip igmp join-group {group_address} source {source_address}")
    else:
        config.append(f"no ip igmp join-group {group_address}")

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure ip igmp join-group on device {device.name}. Error:\n{e}")


def configure_ipv6_mld_snooping_enhance(device, variable_number=None, interval=None,
                                query=None, flood=None, flood_count=None ):
    """ Configure Enable IPv6 mld snooping
    Args:
        device ('obj'): Device object
        variable_number ('int', optional): variabl number value range <1-3>  Robustness Variable number
        interval ('int', optional): inverval value range , <100-32768>  Last listener query interval
        query  ('str', optional): yes/no to enable the command
        flood ('int', optional): flood value range from
        flood_count ('int', optional): flood count value range  1-10
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """

    cmd = f"ipv6 mld snooping "

    if variable_number:
        cmd += f"robustness-variable {variable_number}"
    if interval:
        cmd += f"last-listener-query-interval {interval}"
    if query:
        cmd += f"tcn query solicit"
    if flood:
        cmd += f"tcn flood query count {flood_count}"

    try:
         device.configure(cmd)
    except SubCommandFailure as e:
         raise SubCommandFailure(
             "Failed to configure IPv6 mld snooping on device {dev}. Error:\n{error}".format(dev=device.name, error=e))


def unconfigure_ipv6_mld_snooping_enhance(device, variable_number=None, interval=None,
                                query=None, flood=None, flood_count=None ):
    """ unconfigure IPv6 mld snooping
    Args:
        device ('obj'): Device object
        variable_number ('int', optional): variabl number value range <1-3>  Robustness Variable number
        interval ('int', optional): inverval value range , <100-32768>  Last listener query interval
        query  ('str', optional): yes/no to enable the command
        flood ('int', optional): flood value range from
        flood_count ('int', optional): flood count value range  1-10
    Return:
        None
    Raise:
        SubCommandFailure: Failed unconfigure
    """
    cmd = f"no ipv6 mld snooping "

    if variable_number:
        cmd += f"robustness-variable {variable_number}"
    if interval:
        cmd += f"last-listener-query-interval {interval}"
    if query:
        cmd += f"tcn query solicit"
    if flood:
        cmd += f"tcn flood query count {flood_count}"

    try:
         device.configure(cmd)
    except SubCommandFailure as e:
         raise SubCommandFailure(
             "Failed to unconfigure IPv6 mld snooping on device {dev}. Error:\n{error}".format(dev=device.name, error=e))


def configure_ip_pim_ssm(device, range=None):
    """configure ip pim ssm default on device.
        Args:
            device ('obj'): Device object
            range ('str'): Access list number or  IP named access list
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    log.info("configuring ip pim ssm on {device}".format(device=device.name))
    if range==None:
        configs ="ip pim ssm default"
    else:
        configs = "ip pim ssm range {range}".format(range=range)
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Failed to configure ip pim ssm on device {dev}. Error:\n{error}".format(dev=device.name,error=e))


def unconfigure_ip_pim_ssm(device):
    """unconfigure ip pim ssm default on device.
        Args:
            device ('obj'): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed unconfigure ip pim
    """
    log.info("unconfiguring ip pim ssm on {device}".format(device=device.name))
    configs ="no ip pim ssm"
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Failed to unconfigure ip pim ssm on {dev} . Error:\n{error}".format(dev=device.name,error=e))


def unconfigure_ip_igmp_snooping_vlan_mrouter_interface(device, vlan_id, interface_id):
    """ unconfigure ip igmp snooping vlan mrouter interface
    Args:
        device ('obj'): Device object
        vlan_id ('int'): vlan id
        interfac_id ('str'): interface id
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    cmd = f"no ip igmp snooping vlan {vlan_id} mrouter interface {interface_id}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure ip igmp snooping vlan mrouter interface. Error:\n{error}".format(error=e)
        )

def configure_ipv6_mld_access_group(device, interface=None, groupe_name=None):
    """ Configure ipv6 mld  access_group
    Args:
        device ('obj'): Device object
        interface ('int', optional): interface to configure
        groupe_name ('str', optional): Named access list specifying access group range
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    cmd = []

    if interface:
        cmd.append(f"int {interface}")
        cmd.append(f"ipv6 mld access-group {groupe_name}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ipv6 mld access-group on device. Error:\n{e}")

def unconfigure_ipv6_mld_access_group(device, interface=None, groupe_name=None):
    """ unconfigure ipv6 mld  access_group
    Args:
        device ('obj'): Device object
        interface ('int', optional): interface to configure
        groupe_name ('str', optional): Named access list specifying access group range
    Return:
        None
    Raise:
        SubCommandFailure: Failed unonfiguring
    """
    cmd = []

    if interface:
        cmd.append(f"int {interface}")
        cmd.append(f"no ipv6 mld access-group {groupe_name}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ipv6 mld access-group on device. Error:\n{e}")

def unconfigure_ipv6_pim_bsr_candidate_bsr(device, ipv6_address, vrf=None):
    """ Unconfigure ipv6 pim candidate bsr
    Args:
        device ('obj'): Device object
        ipv6_address ('str'): ipv6_address for candidate
        vrf ('str', optional): vrf name
    Returns:
        None
    Raises:
        SubCommandFailure : Failed to unconfigure ipv6 pim candidate bsr
    """

    log.info(f"Unconfigure ipv6 pim candidate bsr")

    if vrf:
        cmd = f"no ipv6 pim vrf {vrf} bsr candidate bsr {ipv6_address}"
    else:
        cmd = f"no ipv6 pim bsr candidate bsr {ipv6_address}"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ipv6 pim candidate bsr, Error:\n{e}"
        )


def unconfigure_ipv6_pim_bsr_candidate_rp(device, ipv6_address, vrf=None):
    """ Configure ipv6 pim candidate rp
    Args:
        device ('obj'): Device object
        ipv6_address ('str'): ipv6_address for candidate
        vrf ('str', optional): vrf name
    Returns:
        None
    Raises:
        SubCommandFailure : Failed to configure ipv6 pim candidate rp
    """

    log.info(f"Unconfigure ipv6 pim candidate rp")

    if vrf:
        cmd = f"no ipv6 pim vrf {vrf} bsr candidate rp {ipv6_address}"
    else:
        cmd = f"no ipv6 pim bsr candidate rp {ipv6_address}"


    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ipv6 pim candidate rp, Error:\n{e}"
        )


def config_pim_acl(device, acl_name):
    """ Configure ipv6 pim access-list
    Args:
        device ('obj'): Device object
        acl_name('str'): Standard access-list name
    Returns:
        None
    Raises:
        SubCommandFailure : Failed to configure ipv6 pim accept-register list acl_name
    Example:
        device.api.config_pim_acl(acl_name="ssm_source")
    """

    log.info(f"Configure ipv6 pim accept-register list acl_name")

    cmd = f"ipv6 pim accept-register list {acl_name}"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipv6 pim accept-register list acl_name, Error:\n{e}"
        )

def unconfig_pim_acl(device, acl_name):
    """ Unconfigure ipv6 pim access-list
    Args:
        device ('obj'): Device object
        acl_name('str'): Standard access-list name
    Returns:
        None
    Raises:
        SubCommandFailure : Failed to unconfigure ipv6 pim accept-register list acl_name
    Example:
        device.api.unconfig_pim_acl(acl_name="ssm_source")
    """

    log.info(f"Unconfigure ipv6 pim accept-register list acl_name")

    cmd = f"no ipv6 pim accept-register list {acl_name}"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ipv6 pim accept-register list acl_name, Error:\n{e}"
        )


def configure_ipv6_mld_join_group_acl(device, address, interface_id, acl_name):
    """ Configure Enable ipv6 mld join-group
    Args:
        device (`obj`): Device object
        address ('str'): ipv6 address
        interface_id ('str'): id of the interface to be configured
        acl_name('str): acl_name
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    Example:
        device.api.configure_ipv6_mld_join_group_acl(address="FF3E:6::1",interface_id="Loopback1",acl_name="ssm_source")
    """
    cmd = [
            f"interface {interface_id}",
            f"ipv6 mld join-group {address} source-list {acl_name}",
          ]
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ipv6 mld join-group {address} source-list {acl_name}. Error:\n{error}".format(address=address, acl_name=acl_name,error=e)
        )

def unconfigure_ip_pim(device, interface, mode):
    """ Disables PIM sparse mode on an interface.
        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
            mode ('str'): specifiy pim mode

        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    log.info("Unconfiguring pim mode on {interface} on {device}"\
        .format(interface=interface, device=device.name))

    configs = [f"interface {interface}",
               f"no ip pim {mode}"]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure ip pim {mode} on interface {interface} on device {dev}. Error:\n{error}".format(
                mode=mode,
                interface=interface,
                dev=device.name,
                error=e,
            )
        )

def configure_pim_register_source(device, interface, vrf_name=None, is_ipv6=False):
    """ Uncnfigure pim register-source interface

        Args:
            device ('obj'): Device object
            interface ('str'): Name of interface being used as source
            vrf_name ('str',optional): Name of vrf for which we are setting pim source.
            is_ipv6 ('bool',optional): (True | False) 'True' for ipv6 pim configuration. Default is False.
        Returns:
            None

        Raises:
            SubCommandFailure

    """
    ip_type = 'ipv6' if is_ipv6 else 'ip'
    vrf_cfg = f'vrf {vrf_name} ' if vrf_name else ''

    configs = [f"{ip_type} pim {vrf_cfg}register-source {interface}"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure register-source for pim on device {device.name}. Error:\n{e}")

def unconfigure_pim_register_source(device, interface, vrf_name=None, is_ipv6=False):
    """ Unconfigure pim register-source interface

        Args:
            device ('obj'): Device object
            interface ('str'): Name of interface being used as source
            vrf_name ('str',optional): Name of vrf for which we are setting pim source.
            is_ipv6 ('bool',optional): (True | False) 'True' for ipv6 pim configuration. Default is False.
        Returns:
            None

        Raises:
            SubCommandFailure

    """
    ip_type = 'ipv6' if is_ipv6 else 'ip'
    vrf_cfg = f'vrf {vrf_name} ' if vrf_name else ''

    configs = [f"no {ip_type} pim {vrf_cfg}register-source {interface}"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure register-source for pim on device {device.name}. Error:\n{e}")

def configure_ip_forward_protocol_nd(device):
    """ Configure ip forward-protocol network disk on device.
        Args:
            device ('obj'): Device object
        Return:
            None
        Raise:
        SubCommandFailure: Failed to configure ip forward-protocol network disk on device.
    """
    log.info("configuring ip forward-protocol nd on {device}")
    configs = "ip forward-protocol nd"
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
        f'Failed to configure ip forward-protocol network disk on {device}. Error:\n{e}'
        )

def unconfigure_ip_forward_protocol_nd(device):
    """ Unconfigure ip forward-protocol network disk on device.
        Args:
            device ('obj'): Device object
        Return:
            None
        Raise:
        SubCommandFailure: Failed to unconfigure ip forward-protocol network disk on device.
    """
    log.info("unconfiguring ip forward-protocol nd on {device}")
    configs = "no ip forward-protocol nd"
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
        f'Failed to unconfigure ip forward-protocol network disk on {device}. Error:\n{e}'
        )


def configure_ip_msdp_peer(device, hostname, remote_as_number, interface=None):
    """ Configures ip msdp peer
        Args:
            device ('obj')    : device to use
            hostname ('str')  : hostname or ip address
            remote_as_number ('str'): remote as number
            interface ('str', optional) : configires connect-source if defined. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'ip msdp peer {hostname}'
    if interface:
        cmd += f' connect-source {interface}'
    cmd += f' remote-as {remote_as_number}'

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configures ip msdp peer. Error: {e}')


def configure_ip_msdp_cache_sa_state(device):
    """ Configures ip msdp cache-sa-state
        Args:
            device ('obj')    : device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'ip msdp cache-sa-state'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configures ip msdp cache-sa-state. Error: {e}')

def configure_mld_version(device, interface_no, version_no):
    """Configure mld version
       Args:
            device ('obj'): device object
            interface_no ('int'): interface number
            version_no ('int'): version number
       Return:
            None
       Raises:
            SubCommandFailure
    """
    config= [
               f'int vlan {interface_no}',
               f'ipv6 mld version {version_no}'
            ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to Configure mld version on {device.name}\n{e}')


def config_ip_pim_vrf(device, vrf_num, mode):
    """ Enables ip pim vrf mode on device.

        Args:
            device (`obj`): Device object
            vrf_num (`str`): vrf number
            mode (`str`): specifiy ip pim vrf mode
        Return:
            None
        Raise:
            SubCommandFailure
    """
    log.info(f"Configuring ip pim vrf {mode} on {device}")

    cmd = f"ip pim vrf {vrf_num} {mode}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ip pim vrf Error:\n{e}")


def unconfig_ip_pim_vrf(device, vrf_num, mode):
    """ Enables ip pim vrf mode on device.

        Args:
            device (`obj`): Device object
            vrf_num (`str`): vrf number
            mode (`str`): specifiy ip pim vrf mode
        Return:
            None
        Raise:
            SubCommandFailure
    """
    log.info(f"Unconfiguring ip pim vrf {mode} on {device}")

    cmd = f"no ip pim vrf {vrf_num} {mode}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ip pim vrf Error:\n{e}")


def config_ip_multicast_routing_vrf_distributed(device, vrf_name):

    """ configure ip multicast-routing vrf distributed on device
        Example :

        Args:
            device (`obj`): Device object
            vrf_name('str'): name of the vrf
        Returns:
            None
    """
    try:
        device.configure("ip multicast-routing vrf {} distributed".format(vrf_name))
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Configure ip multicast-routing vrf vrf_name distributed. Error {e}".format(e=e)
        )

def unconfig_ip_multicast_routing_vrf_distributed(device, vrf_name):

    """Unconfigure ip multicast-routing vrf distributed on device
        Example :

        Args:
            device (`obj`): Device object
            vrf_name('str'): name of the vrf
        Returns:
            None
    """
    try:
        device.configure("no ip multicast-routing vrf {} distributed".format(vrf_name))
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Unconfigure ip multicast-routing vrf distributed Error {e}".format(e=e)
        )

def configure_ip_msdp_vrf_peer(device, peer, vrf, intf=None):

    """ Configures ip msdp vrf <> peer
        Args:
            device ('obj')    : device to use
            peer ('str')  : name or ip address of the peer
            vrf ('vrf')  : name of the vrf
            intf ('str', optional) : configires connect-source if defined. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'ip msdp vrf {vrf} peer {peer}'
    if intf:
        cmd += f' connect-source {intf}'

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configures ip msdp vrf peer. Error: {e}')

def unconfigure_ip_msdp_vrf_peer(device, peer, vrf, intf=None):

    """ Unconfigures ip msdp vrf <> peer
        Args:
            device ('obj')    : device to use
            peer ('str')  : name or ip address of the peer
            vrf ('vrf')  : name of the vrf
            intf ('str', optional) : configires connect-source if defined. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'no ip msdp vrf {vrf} peer {peer}'
    if intf:
        cmd += f' connect-source {intf}'

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigures ip msdp vrf peer. Error: {e}')

def configure_ipv6_pim_rp_vrf(device, vrf_name, address):
    """ Configure IPv6 PIM RP for a VRF
    Args:
        device (`obj`): Device object
        vrf_name (`str`): VRF name
        address (`str`): RP address
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    cmd = f"ipv6 pim vrf {vrf_name} rp-address {address}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure IPv6 PIM RP for VRF {vrf_name}:\n{e}"
        )

def configure_ip_pim_bsr_rp_candidate(device, vrf_name=None, interface_name=None):
    """ Configure ip pim candidate rp or bsr for both global and VRF contexts.
        Args:
            device ('obj'): Device
            vrf_name ('str', optional): VRF name
            interface_name ('str', Optional): Interface name
        Returns:
            None
        Raises:
            SubCommandFailure: If the configuration fails on the device
    """

    log.debug(f"Configure ip pim candidate rp or bsr for both global and VRF contexts")

    if vrf_name:
        cmds = [
            f"ip pim vrf {vrf_name} bsr-candidate {interface_name}",
            f"ip pim vrf {vrf_name} rp-candidate {interface_name}"
        ]
    else:
        cmds = [
            f"ip pim bsr-candidate {interface_name}",
            f"ip pim rp-candidate {interface_name}"
        ]

    try:
        device.configure(cmds)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ip pim candidate rp or bsr for both global and VRF contexts on device {device.name}. Error:\n{e}"
            )
