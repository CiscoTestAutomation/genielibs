"""Common configure functions for cts"""

import logging
from genie.libs.parser.utils.common import Common
from unicon.eal.dialogs import Dialog, Statement
from unicon.core.errors import (
    SubCommandFailure,
    StateMachineError,
    TimeoutError,
    ConnectionError,
)
log = logging.getLogger(__name__)

def configure_cts_authorization_list(device, authlist):
    """ Configure Local authorization list to use for CTS
        Args:
            device ('obj'): device to use
            authlist ('str'): Named authorization list to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring Local authorization list
    """
    log.info("Configure Local authorization list")
    try:
        device.configure(["cts authorization list {}".format(authlist)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configuring Local authorization list {}.Error: {}".format(authlist, str(e))
        )


def enable_cts_enforcement(device):
    """ Enable cts role-based enforcement
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to enable cts role-based enforcement
    """
    log.info("Enable CTS enforcement")
    try:
        device.configure(["cts role-based enforcement"])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable CTS enforcement.Error:\n{}".format(str(e))
        )


def enable_cts_enforcement_vlan(device, vlan):
    """ Enable DHCP snooping on vlan
        Args:
            device ('obj'): device to use
            vlan ('str'): vlan-id to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to enable cts role-based enforcement
    """
    log.info("Enable CTS enforcement on vlan")
    try:
        device.configure(["cts role-based enforcement vlan {}".format(vlan)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable CTS enforcement on vlan {}.Error:\n{}".format(vlan, str(e))
        )


def configure_device_sgt(device, sgt):
    """ Configure Device SGT
        Args:
            device ('obj'): device to use
            sgt (`int`): Security Group Tag (SGT) value
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Configure Device SGT
    """
    log.info("Configure device SGT %s" %sgt)
    try:
        device.configure(["cts sgt {}".format(sgt)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure device sgt {}.Error: {}".format(sgt,str(e))
        )


def configure_vlan_to_sgt_mapping(device, vlan, sgt):
    """ Configure Vlan SGT
        Args:
            device ('obj'): device to use
            vlan ('str'): vlan-id to configure
            sgt (`int`): Security Group Tag (SGT) value
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Configure Vlan SGT
    """
    log.info("Configure vlan-to-sgt mapping")
    try:
        device.configure(["cts role-based sgt-map vlan-list {} sgt {}".format(vlan, sgt)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure vlan-to-sgt mapping for vlan {vlan},sgt {sgt}.Error:{err}"\
            .format(vlan=vlan, sgt=sgt,err=str(e))
        )


def configure_ipv4_to_sgt_mapping(device, ipv4, sgt):
    """ Configure Ipv4 SGT
        Args:
            device ('obj'): device to use
            ipv4 ('str'): IPv4 address to configure
            sgt (`int`): Security Group Tag (SGT) value
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Configure Ipv4 SGT
    """
    log.info("Configure IP to sgt mapping")
    try:
        device.configure(["cts role-based sgt-map {} sgt {}".format(ipv4, sgt)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ip-to-sgt mapping for ip {ipv4}, sgt {sgt}.Error: {err}".format\
            (ipv4=ipv4, sgt=sgt,err=str(e))
        )


def configure_ipv4_subnet_to_sgt_mapping(device, ipv4, subnet, sgt):
    """ Configure subnet SGT
        Args:
            device ('obj'): device to use
            ipv4 ('str'): IPv4 address to configure
            subnet ('str'): Subnet to verify inside
            sgt (`str`): Security Group Tag (SGT) value
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Configure subnet SGT
    """
    log.info("Configure subnet to sgt mapping")
    try:
        device.configure(["cts role-based sgt-map {}/{} sgt {}".format(ipv4, subnet, sgt)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure sgt {sgt} mapping for {ipv4}/{subnet}.Error: {err}".format\
            (sgt=sgt, ipv4=ipv4, subnet=subnet,err=str(e))
        )

def assign_static_ipv4_sgacl(device, src_sgt, dest_sgt, sgacl):
    """ Assign static SGACL(Ipv4)
        Args:
            device ('obj'): device to use
            src_sgt (`str`): Source Group Tag
            dest_sgt (`str`): Destination Group Tag
            sgacl ('str'): Role-based Access-list name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to assign static SGACL(IPv4)
    """
    log.info("Assign static ipv4 SGACL")
    try:
        device.configure(["cts role-based permissions from {} to {} ipv4 {}".format\
                          (src_sgt, dest_sgt, sgacl)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure static ipv4 sgacl {sgacl} from {src_sgt} to {dest_sgt}.Error:{err}"\
            .format(sgacl=sgacl, src_sgt=src_sgt, dest_sgt=dest_sgt,err=str(e))
        )


def assign_default_ipv4_sgacl(device, sgacl):
    """ Assign a default static SGACL(ipv4)
        Args:
            device ('obj'): device to use
             sgacl ('str'): Role-based Access-list name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to assign default static SGACL(ipv4)
    """
    log.info("Assign default ipv4 SGACL")
    try:
        device.configure(["cts role-based permissions default ipv4 {}".format(sgacl)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure default sgacl {}.Error: {}".format(sgacl,str(e))
        )

def configure_cts_credentials(device, credential_id, password):
    """ Configure CTS credentials
        Args:
            device ('obj'): device to use
            credential_id ('str'): Specify the CTS device ID
            password (`str`): Specify device's CTS password
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Configure cts credential
    """
    log.info("Configure cts credentials")
    cts_cred = Statement(
        pattern=r'.*Are you sure you want to change the Device ID\? \(y\/n\)\s*\[n\]',
        action='sendline(y)',
        loop_continue=True,
        continue_timer=False)
    try:
        device.execute("cts credentials id {} password {}".format(credential_id, password), reply=Dialog([cts_cred]))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to  configure cts credentials"
        )

def configure_pac_key(device,server_name,key):
    """ Configure pack key on a given Radius server
        Args:
            device ('obj'): device to use
            server_name ('str'):  Name for the radius server configuration
            key ('str'): Per-server encryption key
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure pac key
    """
    log.info("Configure pac key")
    cmd = ""
    cmd += (
        "radius server {}\n"
        "pac key {}\n"
        "exit\n".format(server_name,key)
        )
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure configure pac key.Error: {}".format(str(e))
        )

def configure_port_sgt(device,interface,sgt,trusted=True):
    """ Configure port sgt on physical interface
        Args:
            device ('obj'): device to use
            interface (`str`): Interface name
            sgt ('int'): Security Group Tag (SGT) value
            trusted('bool'): Trusted/Untrusted
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure port sgt
    """
    converted_interface = Common.convert_intf_name(interface)
    log.info("Configure port sgt")
    cmd = ""
    cmd += (
        "interface {}\n"
        "cts manual\n".format(converted_interface)
        )
    if trusted:
        cmd += "policy static sgt {} trusted\n".format(sgt)
    else:
        cmd += "policy static sgt {}\n".format(sgt)
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure port sgt {} on interface {}.Error: {}".format(sgt,interface,str(e))
        )

def unconfigure_cts_authorization_list(device, authlist):
    """ Unconfigure Local authorization list to use for CTS
        Args:
            device ('obj'): device to use
            authlist ('str'): Named authorization list to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure Local authorization list
    """
    log.info("unconfigure Local authorization list")
    try:
        device.configure(["no cts authorization list {}".format(authlist)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure Local authorization list {}.Error: {}".format(authlist, str(e))
        )

def disable_cts_enforcement(device):
    """ Disable cts role-based enforcement
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to disable cts role-based enforcement
    """
    log.info("Diable CTS enforcement")
    try:
        device.configure(["no cts role-based enforcement"])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disble CTS enforcement.Error:\n{}".format(str(e))
        )

def disable_cts_enforcement_vlan(device, vlan):
    """ disable cts role-based enforcement on given vlan
        Args:
            device ('obj'): device to use
            vlan ('str'): vlan-id to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to disable cts role-based enforcement
    """
    log.info("Disable CTS enforcement on vlan")
    try:
        device.configure(["no cts role-based enforcement vlan {}".format(vlan)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disble CTS enforcement on vlan {}.Error:\n{}".format(vlan, str(e))
        )

def unconfigure_ipv4_to_sgt_mapping(device, ipv4, sgt):
    """ Unconfigure Ipv4 SGT
        Args:
            device ('obj'): device to use
            ipv4 ('str'): IPv4 address to configure
            sgt (`int`): Security Group Tag (SGT) value
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Unconfigure Ipv4 SGT
    """
    log.info("Unconfigure IP to sgt mapping")
    try:
        device.configure(["no cts role-based sgt-map {} sgt {}".format(ipv4, sgt)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Unconfigure ip-to-sgt mapping for ip {ipv4}, sgt {sgt}.Error: {err}".format\
            (ipv4=ipv4, sgt=sgt,err=str(e))
        )

def unconfigure_ipv4_subnet_to_sgt_mapping(device, ipv4, subnet, sgt):
    """ Unconfigure Ipv4 Subnet to SGT mapping
        Args:
            device ('obj'): device to use
            ipv4 ('str'): IPv4 address to configure
            subnet ('str'): Subnet to verify inside
            sgt (`int`): Security Group Tag (SGT) value
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Unconfigure Ipv4 Subnet to SGT mapping
    """
    log.info("Unconfigure Ipv4 Subnet to SGT mapping")
    try:
        device.configure(["no cts role-based sgt-map {}/{} sgt {}".format(ipv4, subnet, sgt)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure sgt {sgt} mapping for {ipv4}/{subnet}.Error: {err}".format\
            (sgt=sgt, ipv4=ipv4, subnet=subnet,err=str(e))
        )

def remove_static_ipv4_sgacl(device, src_sgt, dest_sgt, sgacl):
    """ Remove static SGACL(Ipv4)
        Args:
            device ('obj'): device to use
            src_sgt (`str`): Source Group Tag
            dest_sgt (`str`): Destination Group Tag
            sgacl ('str'): Role-based Access-list name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to remove static SGACL(IPv4)
    """
    log.info("Remove static ipv4 SGACL")
    try:
        device.configure(["no cts role-based permissions from {} to {} ipv4 {}".format\
                          (src_sgt, dest_sgt, sgacl)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not remove static ipv4 sgacl {sgacl} from {src_sgt} to {dest_sgt}.Error:{err}"\
            .format(sgacl=sgacl, src_sgt=src_sgt, dest_sgt=dest_sgt,err=str(e))
        )

def remove_default_ipv4_sgacl(device, sgacl):
    """ Remove a default static SGACL(ipv4)
        Args:
            device ('obj'): device to use
             sgacl ('str'): Role-based Access-list name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to remove default static SGACL(ipv4)
    """
    log.info("Remove default ipv4 SGACL")
    try:
        device.configure(["no cts role-based permissions default ipv4 {}".format(sgacl)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not remove default sgacl {}.Error: {}".format(sgacl,str(e))
        )

def remove_default_ipv6_sgacl(device, sgacl):
    """ Remove a default static SGACL(ipv6)
        Args:
            device ('obj'): device to use
            sgacl ('str'): Role-based Access-list name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to remove default static SGACL(ipv6)
    """
    log.info("Remove default ipv6 SGACL")
    try:
        device.configure(["no cts role-based permissions default ipv6 {}".format(sgacl)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not remove default sgacl ipv6 {}.Error: {}".format(sgacl,str(e))
        )

def clear_cts_credentials(device):
    """ clear CTS credentials
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to clear cts credential
    """
    log.info("clear cts credentials")
    cts_cred = Statement(
        pattern=r'.*Are you sure you want to delete all CTS credentials and PACs\? \(y\/n\)\s*\[n\]',
        action='sendline(y)',
        loop_continue=True,
        continue_timer=False)
    try:
        device.execute("clear cts credentials", reply=Dialog([cts_cred]))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to clear cts credentials"
        )

def clear_cts_counters(device):
    """ Clear CTS credentials
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to clear cts counters
    """
    try:
        device.execute('clear cts role-based counters')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to clear cts counters"
        )

def configure_sap_pmk_on_cts(device, interface, key_string, method):

    """ Configures sap pmk on cts

        Args:
            device ('obj'): device to use
            interface ('str'): interface to use
            key_string ('str'): key chain to configure
            method ('str'): encrption method to configure

        Return:
            None

        Raise:
            SubCommandFailure
    """
    cmd = [f"interface {interface}", "cts manual", f"sap pmk {key_string} mode-list {method}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure sap pmk. Error:\n{error}".format(error=e)
        )

def unconfigure_cts_manual(device, interface):
    """ unconfigures cts manual
        Args:
            device ('obj'): Device object
            interface ('str'): interface to use

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    cmd = [f"interface {interface}",  "no cts manual"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure cts manual. Error:\n{error}".format(error=e)
        )

def cts_refresh_policy(device, refresh_peer=False, peer_id=None, refresh_sgt=False, sgt_id=None):
    """ Refresh CTS policy
        Args:
            device ('obj'): device to use
            refresh_peer ('bool', optional): refresh peer or not, default is False
            peer_id ('str', optional): peer id to refresh, default is None
            refresh_sgt ('bool', optional): refresh sgt or not, default is False
            sgt_id ('str', optional): sgt id to refresh, default is None
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to refresh cts policy
    """
    cmd = "cts refresh policy"

    if refresh_peer:
        cmd += " peer"
        if peer_id:
            cmd += f" {peer_id}"

    elif refresh_sgt:
        if sgt_id in ("default", "unknown") or sgt_id.isdigit():
                cmd += f" sgt {sgt_id}"
        else:
            log.error(f'Invalid argument: {sgt_id}. Accepted values: "default", "unknown", sgt_id')
            return
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to refresh cts policy - Error:\n{e}"
        )

def cts_refresh_environment_data(device):
    """ Refresh CTS environment-data
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to refresh cts environment-data
    """
    try:
        device.execute('cts refresh environment-data')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to refresh cts environment-data - Error:\n{e}"
        )

def cts_refresh_pac(device):
    """ Refresh CTS pac
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to refresh cts pac
    """
    try:
        device.execute('cts refresh pac')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to refresh cts pac - Error:\n{e}"
        )

def configure_ipv6_to_sgt_mapping(device, ipv6, sgt):
    """ Configure Ipv6 SGT mapping
        Args:
            device ('obj'): device to use
            ipv6 ('str'): IPv6 address to configure
            sgt ('int'): Security Group Tag (SGT) value
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Configure Ipv6 SGT mapping
    """
    log.info("Configure IP to sgt mapping")
    cmd = f"cts role-based sgt-map {ipv6} sgt {sgt}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure ipv6 SGT mapping")

def unconfigure_ipv6_to_sgt_mapping(device, ipv6, sgt):
    """ Unconfigure Ipv6 SGT mapping
        Args:
            device ('obj'): device to use
            ipv6 ('str'): IPv6 address to configure
            sgt ('int'): Security Group Tag (SGT) value
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure Ipv6 SGT mapping
    """
    log.info("Unconfigure IP to sgt mapping")
    cmd = f"no cts role-based sgt-map {ipv6} sgt {sgt}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure ipv6 SGT mapping")

def configure_ipv6_subnet_to_sgt_mapping(device, ipv6, subnet, sgt):
    """ Configure subnet SGT
        Args:
            device ('obj'): device to use
            ipv6 ('str'): IPv6 address to configure
            subnet ('str'): Subnet to verify inside
            sgt ('str'): Security Group Tag (SGT) value
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Configure subnet SGT
    """
    log.info("Configure subnet to sgt mapping")
    cmd = f"cts role-based sgt-map {ipv6}/{subnet} sgt {sgt}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure subnet SGT")

def unconfigure_ipv6_subnet_to_sgt_mapping(device, ipv6, subnet, sgt):
    """ Unconfigure subnet SGT
        Args:
            device ('obj'): device to use
            ipv6 ('str'): IPv6 address to configure
            subnet ('str'): Subnet to verify inside
            sgt ('str'): Security Group Tag (SGT) value
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure subnet SGT
    """
    log.info("Unconfigure subnet to sgt mapping")
    cmd = f"no cts role-based sgt-map {ipv6}/{subnet} sgt {sgt}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure subnet SGT")

def configure_host_ip_to_sgt_mapping(device, ip_address, sgt):
    """ Configure host Ip address SGT
        Args:
            device ('obj'): device to use
            ip_address ('str'): IP address to configure
            sgt ('int'): Security Group Tag (SGT) value
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Configure host ip_address SGT
    """
    log.info("Configure IP to sgt mapping")
    cmd = f"cts role-based sgt-map host {ip_address} sgt {sgt}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure host ip_address SGT")

def unconfigure_host_ip_to_sgt_mapping(device, ip_address, sgt):
    """ Unconfigure host Ip address SGT
        Args:
            device ('obj'): device to use
            ip_address ('str'): IP address to configure
            sgt ('int'): Security Group Tag (SGT) value
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure host ip_address SGT
    """
    log.info("Unconfigure IP to sgt mapping")
    cmd = f"no cts role-based sgt-map host {ip_address} sgt {sgt}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure host ip_address SGT")

def configure_ip_to_sgt_mapping_vrf(device, vrf_name, ip_address, sgt):
    """ Configure vrf Ip address SGT
        Args:
            device ('obj'): device to use
            vrf_name ('str'): vrf name
            ip_address ('str'): IP address to configure
            sgt ('int'): Security Group Tag (SGT) value
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Configure vrf ip_address SGT
    """
    log.info("Configure vrf and IP to sgt mapping")
    cmd = f"cts role-based sgt-map vrf {vrf_name} {ip_address} sgt {sgt}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure vrf and IP to sgt mapping")

def unconfigure_ip_to_sgt_mapping_vrf(device, vrf_name, ip_address, sgt):
    """ Unconfigure vrf Ip address SGT
        Args:
            device ('obj'): device to use
            vrf_name ('str'): vrf name
            ip_address ('str'): IP address to configure
            sgt ('int'): Security Group Tag (SGT) value
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Unconfigure vrf ip_address SGT
    """
    log.info("Unconfigure vrf and IP to sgt mapping")
    cmd = f"no cts role-based sgt-map vrf {vrf_name} {ip_address} sgt {sgt}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure vrf and IP to sgt mapping")

def configure_ip_subnet_to_sgt_mapping_vrf(device, vrf_name, ip_address, subnet, sgt):
    """ Configure vrf Ip address subnet SGT
        Args:
            device ('obj'): device to use
            vrf_name ('str'): vrf name
            ip_address ('str'): IP address to configure
            subnet ('str'): Subnet to verify inside
            sgt ('int'): Security Group Tag (SGT) value
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Configure vrf ip_address subnet SGT
    """
    log.info("Configure vrf and IP subnet to sgt mapping")
    cmd = f"cts role-based sgt-map vrf {vrf_name} {ip_address}/{subnet} sgt {sgt}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure vrf and IP subnet to sgt mapping")

def unconfigure_ip_subnet_to_sgt_mapping_vrf(device, vrf_name, ip_address, subnet, sgt):
    """ Unconfigure vrf Ip address subnet SGT
        Args:
            device ('obj'): device to use
            vrf_name ('str'): vrf name
            ip_address ('str'): IP address to configure
            subnet ('str'): Subnet to verify inside
            sgt ('int'): Security Group Tag (SGT) value
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure vrf ip_address subnet SGT
    """
    log.info("Unconfigure vrf and IP subnet to sgt mapping")
    cmd = f"no cts role-based sgt-map vrf {vrf_name} {ip_address}/{subnet} sgt {sgt}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure vrf and IP subnet to sgt mapping")

def configure_cts_role_based_permission(device, src_sgt, dest_sgt, protocol_version, rbacl_name):
    """ Configure cts role based permissions
        Args:
            device ('obj'): device to use
            src_sgt ('str'): Source Group Tag
            dest_sgt ('str'): Destination Group Tag
            protocol_version ('str'): protocol version to configure (ipv4 or ipv6)
            rbacl_name ('str'): rbacl name to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Configure cts role based permissions
    """
    log.info("Configure cts role based permissions")
    cmd = f"cts role-based permissions from {src_sgt} to {dest_sgt} {protocol_version} {rbacl_name}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure cts role based permissions")

def unconfigure_cts_role_based_permission(device, src_sgt, dest_sgt, protocol_version):
    """ Unconfigure cts role based permissions
        Args:
            device ('obj'): device to use
            src_sgt ('str'): Source Group Tag
            dest_sgt ('str'): Destination Group Tag
            protocol_version ('str'): protocol version to configure (ipv4 or ipv6)
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Unconfigure cts role based permissions
    """
    log.info("Unconfigure cts role based permissions")
    cmd = f"no cts role-based permissions from {src_sgt} to {dest_sgt} {protocol_version}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure cts role based permissions")

def configure_cts_role_based_permission_default(device, protocol_version, rbacl_name):
    """ Configure cts role based permissions default
        Args:
            device ('obj'): device to use
            protocol_version ('str'): protocol version to configure (ipv4 or ipv6)
            rbacl_name ('str'): rbacl name to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Configure cts role based permissions default
    """
    log.info("Configure cts role based permissions default")
    cmd = f"cts role-based permissions default {protocol_version} {rbacl_name}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure cts role based permissions default")

def unconfigure_cts_role_based_permission_default(device, protocol_version):
    """ Unconfigure cts role based permissions default
        Args:
            device ('obj'): device to use
            protocol_version ('str'): protocol version to configure (ipv4 or ipv6)
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Unconfigure cts role based permissions default
    """
    log.info("Unconfigure cts role based permissions default")
    cmd = f"no cts role-based permissions default {protocol_version}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure cts role based permissions default")

def configure_cts_role_based_monitor(
    device, default=None, protocol_version=None,
    src_sgt=None,dst_sgt=None
):
    """ Configure cts role based monitor
        Args:
            device ('obj'): device to use
            default ('str'): default
            protocol_version ('str'): protocol version to configure (ipv4 or ipv6)
            src_sgt ('str'): Source Group Tag
            dst_sgt ('str'): Destination Group Tag
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Configure cts role based monitor
    """
    log.info("Configure cts role based monitor")

    if default:
        cmd = f"cts role-based monitor permissions {default} {protocol_version}"
    elif src_sgt:
        cmd = f"cts role-based monitor permissions from {src_sgt} to {dst_sgt} {protocol_version}"
    else:
        cmd = "cts role-based monitor all"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure cts role based monitor")

def unconfigure_cts_role_based_monitor(
    device,default=None,protocol_version=None,
    src_sgt=None,dst_sgt=None
):
    """ Unconfigure cts role based monitor
        Args:
            device ('obj'): device to use
            default ('str'): default
            protocol_version ('str'): protocol version to configure (ipv4 or ipv6)
            src_sgt ('str'): Source Group Tag
            dst_sgt ('str'): Destination Group Tag
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Unconfigure cts role based monitor
    """
    log.info("Unconfigure cts role based monitor")
    if default:
        cmd = f"no cts role-based monitor permissions {default} {protocol_version}"
    elif src_sgt:
        cmd = f"no cts role-based monitor permissions from {src_sgt} to {dst_sgt} {protocol_version}"
    else:
        cmd = "no cts role-based monitor all"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure cts role based monitor")

def configure_cts_enforcement_interface(device, interface):
    """ Configure cts role-based enforcement on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface
        Returns:
            None
        Raises:
            SubCommandFailure: cts role-based enforcement not configured
    """
    log.info("Configure cts role-based enforcement on interface")
    cmd = [f"interface {interface}",  "cts role-based enforcement"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure cts role-based enforcement on interface")

def unconfigure_cts_enforcement_interface(device, interface):
    """ Unconfigure cts role-based enforcement on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface
        Returns:
            None
        Raises:
            SubCommandFailure: cts role-based enforcement not unconfigured
    """
    log.info("Unconfigure cts role-based enforcement on interface")
    cmd = [f"interface {interface}",  "no cts role-based enforcement"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure cts role-based enforcement on interface")

def configure_ip_role_based_acl(
    device,acl_name,ip_type,protocol=None,permission=None,log=None,
    prec_value=None,dscp_value=None,port_type=None,
    port_match_condition=None,port_match_value=None,
    port_range_start=None,port_range_end=None
):
    """ Configure ip role based ACL on device
        Args:
            device ('obj'): device object
            ip_type ('str'): ip address type ip or ipv6
            protocol ('str'): protocol includes ip,ipv6,icmp,tcp,udp
            acl_name ('str'): access-list name
            permission ('str'): (permit | deny)
            log ('str'): Log matches against this entry
            prec_value ('str'): Precedence value (critical | flash | priority | network)
            dscp_value ('str'): dscp value (afll | af12 | af13)
            port_type ('str'): src/dst port type
            port_match_condition ('str'): eq/lt/gt on a given port number
            port_match_value ('str'): Port number value
            port_range_start ('str'): Start Port number range
            port_range_end ('int'): End Port number range
        Returns:
            config
        Raises:
            SubCommandFailure: Failed to configure role based access-list
    """
    cmd = []
    cmd.append(f"{ip_type} access-list role-based {acl_name}")
    sub_cmnd = f'{permission} {protocol}'
    if protocol in ['ip', 'ipv6', 'icmp']:
        if log:
            sub_cmnd += f' {log}'
        elif prec_value:
            sub_cmnd += f' precedence {prec_value}'
        elif dscp_value:
            sub_cmnd += f' dscp {dscp_value}'
    elif protocol in ['tcp', 'udp']:
        if port_match_condition:
            sub_cmnd += f' {port_type} {port_match_condition} {port_match_value}'
        elif port_range_start:
            sub_cmnd += f' {port_type} range {port_range_start} {port_range_start}'
    cmd.append(sub_cmnd)
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure cts role-based acl")

def unconfigure_ip_role_based_acl(device, acl_name, protocol):
    """ Unconfigure ip role based ACL on device
        Args:
            device ('obj'): device to use
            acl_name ('str'): acl name
            protocol ('str'): protocol includes ip,ipv6
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ip role based ACL on device
    """
    log.info("Unconfigure ip role based ACL on device")
    cmd = f"no {protocol} access-list role-based {acl_name}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure ip role based ACL on device")

def configure_cts_enforcement_logging(device, log_interval):
    """ Configure cts enforcement logging
        Args:
            device ('obj'): device to use
            log_interval ('str'): logging interval in seconds
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Configure cts enforcement logging
    """
    log.info("Configure cts enforcement logging")
    cmd = f"cts role-based enforcement logging-interval {log_interval}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure cts enforcement logging. Error:\n {e}")

def unconfigure_cts_enforcement_logging(device, log_interval):
    """ Unconfigure cts enforcement logging
        Args:
            device ('obj'): device to use
            log_interval ('str'): logging interval in seconds
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Unconfigure cts enforcement logging
    """
    log.info("Unconfigure cts enforcement logging")
    cmd = f"no cts role-based enforcement logging-interval {log_interval}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not unconfigure cts enforcement logging. Error:\n {e}")

def clear_cts_counters_ipv6(device):
    """ Clear CTS counters ipv6
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to clear CTS counters ipv6
    """
    try:
        device.execute('clear cts role-based counters ipv6')
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not clear CTS counters ipv6. Error:\n {e}")

def configure_cts_aaa_methods(device, server_grp, list_name):
    """ Configure cts aaa methods
        Args:
            device ('obj'): device to use
            server_grp ('str'): server group name
            list_name ('str'): cts authorisation list name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Configure cts aaa methods
    """
    log.info("Configure cts aaa methods")
    cmd = [f"aaa authentication dot1x default group {server_grp}", f"aaa authorization network {list_name} group {server_grp}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure cts aaa methods. Error:\n {e}")

def unconfigure_cts_aaa_methods(device, server_grp, list_name):
    """ Unconfigure cts aaa methods
        Args:
            device ('obj'): device to use
            server_grp ('str'): server group name
            list_name ('str'): cts authorisation list name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Unconfigure cts aaa methods
    """
    log.info("Unconfigure cts aaa methods")
    cmd = [f"no aaa authentication dot1x default group {server_grp}", f"no aaa authorization network {list_name} group {server_grp}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not unconfigure cts aaa methods. Error:\n {e}")

def clear_cts_counters_ipv4(device):
    """ Clear CTS counters ipv4
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to clear CTS counters ipv4
    """
    try:
        device.execute('clear cts role-based counters ipv4')
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not clear CTS counters ipv4. Error:\n {e}")

def enable_cts_enforcement_vlan_list(device, vlan):
    """ enable cts role-based enforcement on given vlan range
        Args:
            device ('obj'): device to use
            vlan ('str'): vlan range to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to enable cts role-based enforcement vlan list
    """
    log.debug("Enable CTS enforcement on vlan-list")
    try:
        device.configure(["cts role-based enforcement vlan-list {}".format(vlan)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable CTS enforcement on vlan {}.Error:\n{}".format(vlan, str(e))
        )

def disable_cts_enforcement_vlan_list(device, vlan):
    """ disable cts role-based enforcement on given vlan range
        Args:
            device ('obj'): device to use
            vlan ('str'): vlan range to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to disable cts role-based enforcement vlan list
    """
    log.info("Disable CTS enforcement on vlan-list")
    try:
        device.configure(["no cts role-based enforcement vlan-list {}".format(vlan)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disble CTS enforcement on vlan {}.Error:\n{}".format(vlan, str(e))
        )

def configure_interface_cts_role_based_sgt_map(device, interface, vlan, sgt):
    """ Configure interface cts role-based sgt-map
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            vlan ('str'): vlan to configure
            sgt ('int'): Security Group Tag (SGT) value
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure interface cts role-based sgt-map
    """
    log.info("Configure interface cts role-based sgt-map")
    cmd = ["interface {}".format(interface), "cts role-based sgt-map vlan {} sgt {}".format(vlan, sgt)]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure interface cts role-based sgt-map.Error:\n{}".format(str(e))
        )

def unconfigure_interface_cts_role_based_sgt_map(device, interface, vlan, sgt):
    """ Unconfigure interface cts role-based sgt-map 
        Args:
            device ('obj'): device to use
            interface ('str'): interface to unconfigure
            vlan ('str'): vlan to unconfigure
            sgt ('int'): Security Group Tag (SGT) value
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure interface cts role-based sgt-map
    """
    log.info("Unconfigure interface cts role-based sgt-map")
    cmd = ["interface {}".format(interface), "no cts role-based sgt-map vlan {} sgt {}".format(vlan, sgt)]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure interface cts role-based sgt-map.Error:\n{}".format(str(e))
        )
