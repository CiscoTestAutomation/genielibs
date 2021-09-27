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
