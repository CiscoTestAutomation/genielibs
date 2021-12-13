"""Common configure functions for pim"""

# Python
import logging
from unicon.eal.dialogs import Statement, Dialog

# Unicon
from unicon.core.errors import SubCommandFailure

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