"""Common configure functions for dhcpv6"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def create_dhcp_pool_ipv6(device, pool_name, ipv6_prefix, lifetime, pref_lifetime):
    """ Create DHCP IPv6 pool
        Args:
            device ('obj'): device to use
            pool_name ('str'): name of the pool to be created
            ipv6_prefix ('str'): IPv6 prefix
            lifetime ('int'): lifetime in seconds
            pref_lifetime ('int'): preferred lifetime in seconds
        Returns:
            None
        Raises:
            SubCommandFailure: Failed creating IPv6 DHCP pool
    """
    log.info(
        "Configuring IPv6 DHCP pool with name={pool_name}, ipv6_prefix={ipv6_prefix}, lifetime={lifetime}, and "
        "Preferred Lifetime {pref_lifetime} ".format(pool_name=pool_name, ipv6_prefix=ipv6_prefix, lifetime=lifetime, pref_lifetime=pref_lifetime)
    )

    try:
        device.configure(
            [
                "ipv6 dhcp pool {pool_name}".format(pool_name=pool_name),
                "address prefix {ipv6_prefix} lifetime {lifetime} {pref_lifetime}".format(ipv6_prefix=ipv6_prefix, lifetime=lifetime, pref_lifetime=pref_lifetime)
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure IPv6 DHCP pool {pool_name}".format(
                pool_name=pool_name
            )
        )

def remove_dhcp_pool_ipv6(device, pool_name):
    """ Remove DHCP IPv6 pool
        Args:
            device ('obj'): device to use
            pool_name ('str'): name of the pool to be created
        Returns:
            None
        Raises:
            SubCommandFailure: Failed removing IPv6 DHCP pool
    """
    log.info(
        "Removing IPv6 DHCP pool with name={pool_name}".format(pool_name=pool_name)
    )

    try:
        device.configure(
            [
                "no ipv6 dhcp pool {pool_name}".format(pool_name=pool_name),
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove IPv6 DHCP pool {pool_name}".format(
                pool_name=pool_name
            )
        )

def enable_dhcp_ldra(device, **kwargs):
    """
    Enabling DHCP ldra
        Args:
            device ('obj'): device to use
        Returns:
            str: Response of command
        Raises:
            SubCommandFailure: Failed to enable ldra
    """
    log.info("Enabling DHCP ldra")
    try:
        return device.configure(
            [
                "ipv6 dhcp-ldra enable"
            ], **kwargs
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not enable DHCP ldra globally"
            )

def remove_enable_dhcp_ldra(device, **kwargs):
    """
    Removing enable DHCP ldra
        Args:
            device ('obj'): device to use
        Returns:
            str: Response of command
        Raises:
            SubCommandFailure: Failed to remove enable ldra
    """
    log.info("Removing enable DHCP ldra")
    try:
        return device.configure(
            [
                "no ipv6 dhcp-ldra enable"
            ], **kwargs
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove enable DHCP ldra globally"
            )

def disable_dhcp_ldra(device, **kwargs):
    """
    Disabling DHCP ldra
        Args:
            device ('obj'): device to use
        Returns:
            str: Response of command
        Raises:
            SubCommandFailure: Failed to disable ldra
    """
    log.info("Disabling DHCP ldra")
    try:
        return device.configure(
            [
                "ipv6 dhcp-ldra disable"
            ], **kwargs
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not disable DHCP ldra globally"
            )

def remove_disable_dhcp_ldra(device, **kwargs):
    """
    Removing disable DHCP ldra
        Args:
            device ('obj'): device to use
        Returns:
            str: Response of command
        Raises:
            SubCommandFailure: Failed to remove disable ldra
    """
    log.info("Removing disable DHCP ldra")
    try:
        return device.configure(
            [
                "no ipv6 dhcp-ldra disable"
            ], **kwargs
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove disable DHCP ldra globally"
            )

def configure_ldra_remote_id(device, remote_id=None, **kwargs):
    """
    Configuring DHCP ldra remote-id
        Args:
            device ('obj'): device to use
            remote_id ('str'): remote-id for ldra
        Returns:
            str: Response of command
        Raises:
            SubCommandFailure: Failed to configure ldra remote-id
    """
    log.info("Configuring DHCP ldra remote-id")
    try:
        if remote_id:
            return device.configure(
                [
                    "ipv6 dhcp-ldra remote-id {}".format(remote_id)
                ], **kwargs
            )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure DHCP ldra remote-id"
            )

def remove_ldra_remote_id(device, remote_id=None, **kwargs):
    """
    Remove DHCP ldra remote-id
        Args:
            device ('obj'): device to use
            remote_id ('str'): remote-id for ldra
        Returns:
            str: Response of command
        Raises:
            SubCommandFailure: Failed to remove ldra remote-id
    """
    log.info("Removing DHCP ldra remote-id")
    try:
        if remote_id:
            return device.configure(
                [
                    "no ipv6 dhcp-ldra remote-id {}".format(remote_id)
                ], **kwargs
            )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove DHCP ldra remote-id"
            )

def configure_ldra_policy_vlan(device, vlan_id=None, policy=None, **kwargs):
    """
    Configuring DHCP ldra policy on vlan
        Args:
            device ('obj'): device to use
            vlan_id ('str'): vlan_id to attach policy
            policy ('str'): policy to attach in vlan
        Returns:
            str: Response of command
        Raises:
            SubCommandFailure: Failed to configure ldra policy on vlan
    """
    log.info("Configuring ldra policy on vlan {}".format(vlan_id))
    try:
        if vlan_id and policy:
            return device.configure(
                [
                    "vlan configuration {}".format(vlan_id),
                    "ipv6 dhcp ldra attach-policy {}".format(policy)
                ], **kwargs
            )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure ldra policy on vlan {}".format(vlan_id)
            )

def remove_ldra_policy_vlan(device, vlan_id=None, policy=None, **kwargs):
    """
    Remove DHCP ldra policy on vlan
        Args:
            device ('obj'): device to use
            vlan_id ('str'): vlan_id to attach policy
            policy ('str'): policy to attach in vlan
        Returns:
            str: Response of command
        Raises:
            SubCommandFailure: Failed to remove ldra policy on vlan
    """
    log.info("Removing ldra policy on vlan {}".format(vlan_id))
    try:
        if vlan_id and policy:
            return device.configure(
                [
                    "vlan configuration {}".format(vlan_id),
                    "no ipv6 dhcp ldra attach-policy {}".format(policy)
                ], **kwargs
            )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove ldra policy on vlan {}".format(vlan_id)
            )

def configure_ldra_interface(
        device, interface=None, vlan_id=None, policy=None, interface_id=None, **kwargs):
    """
    Configuring DHCP ldra on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            vlan_id ('str'): vlan_id to attach policy
            policy ('str'): policy to attach in vlan
            interface_id ('str'): interface-id for ldra interface
        Returns:
            str: Response of command
        Raises:
            SubCommandFailure: Failed to configure ldra on interface
    """
    log.info("Configuring ldra on interface {}".format(interface))
    
    cmd = []
    if interface:
        cmd.append(f"interface {interface}")
    if vlan_id:
        cmd.extend([
            'switchport',
            f'switchport access vlan {vlan_id}'
        ])
    if policy:
        cmd.append(f"ipv6 dhcp-ldra attach-policy {policy}")
    if interface_id:
        cmd.append(f"ipv6 dhcp-ldra interface-id {interface_id}")
        
    try:
        device.configure(cmd)

    except SubCommandFailure as err:
        raise SubCommandFailure(
            "Could not configure ldra on interface {}, Reason: {}".format(interface, err)
            )

def remove_ldra_interface(
        device, interface=None, vlan_id=None, policy=None, interface_id=None, **kwargs):
    """
    Remove DHCP ldra remote-id
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            vlan_id ('str'): vlan_id to attach policy
            policy ('str'): policy to attach in vlan
        Returns:
            str: Response of command
        Raises:
            SubCommandFailure: Failed to remove ldra on interface
    """
    log.info("Removing ldra on interface {}".format(vlan_id))
    try:
        if interface and vlan_id:
            cmd_list = [
                "interface {}".format(interface)
                ]
            if policy:
                cmd_list.append("no ipv6 dhcp-ldra attach-policy {}".format(policy))
            if interface_id:
                cmd_list.append("no ipv6 dhcp-ldra interface-id {}".format(interface_id))
            cmd_list.append("no switchport access vlan {}".format(vlan_id))
            cmd_list.append("no switchport")
            return device.configure(cmd_list, **kwargs)

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove ldra on interface {}".format(interface)
            )

def configure_dhcp_pool_ipv6_domain_name(device, pool_name, domain_name, dns_server=None):
    """ Configure domain-name under DHCP IPv6 pool
        Args:
            device ('obj'): device to use
            pool_name ('str'): name of the pool to be created
            domain_name ('str'): domain name to configure
            dns_server('str',optional): dns server to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed creating domain_name under IPv6 DHCP pool
    """
    log.debug(
        "Configuring domain-name under IPv6 DHCP pool {pool_name} with name={domain_name}".
            format(pool_name=pool_name,domain_name=domain_name)
    )
    cmd = [f'ipv6 dhcp pool {pool_name}', f'domain-name {domain_name}']
    if dns_server:
        cmd+= [f'dns-server {dns_server}']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure domain_name {domain_name} IPv6 DHCP pool {pool_name}.Error:\n{error}".format(
                domain_name=domain_name,
                pool_name=pool_name,
                error=e
            )
        )

def configure_ipv6_dhcp_client_vendor_class(
        device,
        interface,
        type,
        string=None):
    """ Configure IPV6 DHCP Client Vendor-class on interface:
        Args:
            device ('obj'): device to use
            interface ('str'): Interface to configure
            type('str'): vendor-class type (i.e. mac-address, ascii, hex, disable)
            string('str', optional): The value string when type set to ascii or hex
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ipv6 dhcp vendor-class
    """
    log.info(f"Configure ipv6 dhcp client vendor-class {type} on {interface}")
    if type in ['mac-address', 'disable']:
        cmd = f'ipv6 dhcp client vendor-class {type}'

    elif type in ['ascii', 'hex'] and string:
        cmd = f'ipv6 dhcp client vendor-class {type} {string}'

    else:
        raise SubCommandFailure("Invalid vendor-class type or string missing")

    try:
        device.configure([f"interface {interface}", cmd])

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipv6 dhcp vendor-class on {interface}. Error:\n{e}")

def unconfigure_ipv6_dhcp_client_vendor_class(
        device,
        interface,
        type):
    """ Unconfigure IPv6 DHCP Client Vendor-class on interface:
        Args:
            device ('obj'): device to use
            interface ('str'): Interface to configure
            type('str'): vendor-class type (i.e. mac-address, ascii, hex, disable)
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ipv6 dhcp vendor-class
    """
    log.info(f"Unconfigure ipv6 dhcp client vendor-class {type} on {interface}")
    cmd = f'no ipv6 dhcp client vendor-class {type}'
    try:
        device.configure([f"interface {interface}", cmd])

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ipv6 dhcp vendor-class on {interface}. Error:\n{e}")


def configure_dhcp_pool_dns_server(device, ip_version, pool_name, dns_server):
    """ Configure dns-server under dhcp pool
        Args:
            device ('obj'): device to use
            ip_version ('str'): ip or ipv6 version.
            pool_name ('str'): name of the pool to be created
            dns_server ('str'): dns server to configure

        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure dns-server under dhcp pool
    """

    config = [f"{ip_version} dhcp pool {pool_name}", f"dns-server {dns_server}"]
    try:
        device.configure(config)

    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure dns-server {dns_server} under dhcp pool {pool_name}. Error:\n{e}")

def configure_ipv6_dhcp_relay_trust(device, interface):
    """ Configures ipv6 dhcp relay trust
        Args:
            device ('obj'): device to use
            interface ('str'):  interface name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring ipv6 dhcp relay trust on {device.name} {interface}")
    cmd = [f'interface {interface}','ipv6 dhcp relay trust']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure ipv6 dhcp relay trust on device interface. Error:\n{e}')

def unconfigure_ipv6_dhcp_relay_trust(device, interface):
    """ Unconfigures ipv6 dhcp relay trust
        Args:
            device ('obj'): device to use
            interface ('str'):  interface name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring ipv6 dhcp relay trust on {device.name} {interface}")
    cmd = [f'interface {interface}','no ipv6 dhcp relay trust']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure ipv6 dhcp relay trust on device interface. Error:\n{e}')
    
def configure_ipv6_dhcp_relay_option_vpn(device, interface):
    """ Configures ipv6 dhcp relay option vpn
        Args:
            device ('obj'): device to use
            interface ('str'):  interface name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring ipv6 dhcp relay option vpn on {device.name} {interface}")
    cmd = [f'interface {interface}','ipv6 dhcp relay option vpn']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure ipv6 dhcp relay option vpn on device interface. Error:\n{e}')

def unconfigure_ipv6_dhcp_relay_option_vpn(device, interface):
    """ Unconfigures ipv6 dhcp relay option vpn
        Args:
            device ('obj'): device to use
            interface ('str'):  interface name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring ipv6 dhcp relay option vpn on {device.name} {interface}")
    cmd = [f'interface {interface}','no ipv6 dhcp relay option vpn']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not Unconfigure ipv6 dhcp relay option vpn on device interface. Error:\n{e}')

def configure_ipv6_dhcp_relay_source_interface_intf_id(device, interface, intf_id):
    """ Configure interface ipv6 dhcp relay source interface intf_id 
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured # example Vlan100"
            intf_id ('str'): Set source interface for relayed messages for interface ex: Loopback1 interface
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ipv6 dhcp relay source-interface intf_id
    """
    log.info("Configuring ip dhcp relay source-interface intf_id on the interface")
    cmd = [f"interface {interface}",f"ipv6 dhcp relay source-interface {intf_id}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipv6 dhcp relay source interface intf_id {interface}. Error\n{e}"
        )

def unconfigure_ipv6_dhcp_relay_source_interface_intf_id(device, interface, intf_id):
    """ Unconfigure interface ipv6 dhcp relay source interface intf_id 
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface # example Vlan100"
            intf_id ('str'): Set source interface for relayed messages for interface ex: Loopback1 interface
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ipv6 dhcp relay source-interface intf_id
    """
    log.info("Configuring ip dhcp relay source-interface intf_id on the interface")
    cmd = [f"interface {interface}",f"no ipv6 dhcp relay source-interface {intf_id}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ipv6 dhcp relay source interface intf_id {interface}. Error\n{e}"
        )

def configure_ipv6_dhcp_relay_destination_ipv6address(device, interface, ipv6_address,vrf_name=None):
    """ Configure interface ipv6 dhcp relay destination ipv6 address 
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured # example Vlan100"
            ipv6_address ('str'): IPv6 destination address Ex: 20::1
            vrf_name ('str',Optional): vrf name Ex: green
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ipv6 dhcp relay destination ipv6 address
    """
    log.info("Configuring ipv6 dhcp relay destination ipv6 address on the interface")
    cmd = [f"interface {interface}"]
    if vrf_name:
        cmd.append(f"ipv6 dhcp relay destination vrf {vrf_name} {ipv6_address}")
    else:
        cmd.append(f"ipv6 dhcp relay destination {ipv6_address}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipv6 dhcp relay destination ipv6 address on {interface}. Error\n{e}"
        )

def unconfigure_ipv6_dhcp_relay_destination_ipv6address(device, interface, ipv6_address,vrf_name=None):
    """ Unconfigure interface ipv6 dhcp relay destination ipv6 address 
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured # example Vlan100"
            ipv6_address ('str'): IPv6 destination address Ex: 20::1
            vrf_name ('str',Optional): vrf name Ex: green
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ipv6 dhcp relay destination ipv6 address
    """
    log.info("Unconfiguring ipv6 dhcp relay destination ipv6 address on the interface")
    cmd = [f"interface {interface}"]
    if vrf_name:
        cmd.append(f"no ipv6 dhcp relay destination vrf {vrf_name} {ipv6_address}")
    else:
        cmd.append(f"no ipv6 dhcp relay destination {ipv6_address}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ipv6 dhcp relay destination ipv6 address on {interface}. Error\n{e}"
        )
