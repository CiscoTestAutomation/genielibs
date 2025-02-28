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

def configure_ipv6_dhcp_relay_source(device, interface):
    """ Configure ipv6 dhcp-relay source-interface {interface}
        Args:
            device ('obj'): device to use
            interface ('str'):  interface name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring ipv6 dhcp-relay source-interface {interface}")
    cmd = [f'ipv6 dhcp-relay source-interface {interface}']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure ipv6 dhcp-relay source-interface. Error:\n{e}')
        
def unconfigure_ipv6_dhcp_relay_source(device, interface):
    """ UnConfigure ipv6 dhcp-relay source-interface {interface}
        Args:
            device ('obj'): device to use
            interface ('str'):  interface name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"UnConfiguring ipv6 dhcp-relay source-interface {interface}")
    cmd = [f'no ipv6 dhcp-relay source-interface {interface}']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure ipv6 dhcp-relay source-interface. Error:\n{e}')

def configure_interface_ipv6_nd_managed_config_flag(device, interface):
    """ Configure ipv6 nd managed-config-flag on the interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ipv6 nd managed-config-flag
    """
    log.debug("Configuring ipv6 nd managed-config-flag on the interface")
    config =  [f"interface  {interface}",
               f"ipv6 nd managed-config-flag"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipv6 nd managed-config-flag on the interface {interface}. Error\n{e}"
        )

def unconfigure_interface_ipv6_nd_managed_config_flag(device,interface):
    """ Unconfigure ipv6 nd managed-config-flag on the interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ipv6 nd managed-config-flag
    """
    log.debug("Unconfiguring ipv6 nd managed-config-flag on the interface")
    config =  [f"interface  {interface}",
               f"no ipv6 nd managed-config-flag"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ipv6 nd managed-config-flag on the interface {interface}. Error\n{e}"
        )
    
def configure_ipv6_dhcp_relay_bulk_lease(device, option, value = None):
    """ Configure ipv6 dhcp-relay bulk-lease
        Args:
            device ('obj'): device to use
            option ('str'): option for ipv6 dhcp-relay bulk-lease  #example - disable, retry, timeout
            value ('int', optional): <0-15> , used while performing options like retry and timeout.
            
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ipv6 dhcp-relay bulk-lease
    """
    log.debug("Configuring ipv6 dhcp-relay bulk-lease")
    config = []
    if option in ['retry','timeout']:
        config.append(f"ipv6 dhcp-relay bulk-lease {option} {value}")
    elif option in ['disable']:
        config.append(f"ipv6 dhcp-relay bulk-lease {option}")
    
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipv6 dhcp {option}.Error\n{e}"
        )
    
def unconfigure_ipv6_dhcp_relay_bulk_lease(device, option, value = None):
    """ Unconfigure ipv6 dhcp-relay bulk-lease
        Args:
            device ('obj'): device to use
            option ('str'): option for ipv6 dhcp-relay bulk-lease  #example - disable, retry, timeout
            value ('int', optional): <0-15> , used while performing options like retry and timeout.
            
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ipv6 dhcp-relay bulk-lease
    """
    log.debug("Unconfiguring ipv6 dhcp-relay bulk-lease")
    config = []
    if option in ['retry','timeout']:
        config.append(f"no ipv6 dhcp-relay bulk-lease {option} {value}")
    elif option in ['disable']:
        config.append(f"no ipv6 dhcp-relay bulk-lease {option}")
    
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ipv6 dhcp {option}.Error\n{e}"
        )

def configure_ipv6_dhcp_ping_packets(device, packets_no):
    """ Configure ipv6 dhcp ping packets
        Args:
            device ('obj'): device to use
            packets_no ('str): number of packets we need to send
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to ping ipv6 dhcp packets
    """
    log.debug("Configuring ipv6 dhcp ping packets")
    try:
        device.configure('ipv6 dhcp ping packets {}'.format(packets_no))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ipv6 dhcp ping packets on {device}. Error\n{e}"
            )

def configure_ipv6_dhcp_server_join_all_dhcp_server(device):
    """ Configure ipv6 dhcp server join all-dhcp-server
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ipv6 dhcp server join all-dhcp-server
    """
    log.debug("Configuring ipv6 dhcp server join all-dhcp-server")
    try:
        device.configure('ipv6 dhcp server join all-dhcp-server')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ipv6 dhcp server join all-dhcp-server on {device}. Error\n{e}"
            )

def unconfigure_ipv6_dhcp_server_join_all_dhcp_server(device):
    """ Unconfigure ipv6 dhcp server join all-dhcp-server
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ipv6 dhcp server join all-dhcp-server
    """
    log.debug("Unconfiguring ipv6 dhcp server join all-dhcp-server")
    try:
        device.configure('no ipv6 dhcp server join all-dhcp-server')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ipv6 dhcp server join all-dhcp-server on {device}. Error\n{e}"
            )

def configure_ipv6_dhcp_route_add(device, route_add):
    """ Configure ipv6 dhcp route-add
        Args:
            device ('obj'): device to use
            route_add ('str'): route name to configure. example - iana-route-add, iapd-route-add
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ipv6 dhcp route-add
    """
    log.debug("Configuring ipv6 dhcp {route_add}")
    config = [f"ipv6 dhcp {route_add}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ipv6 dhcp {route_add} on {device}. Error\n{e}"
            )

def unconfigure_ipv6_dhcp_route_add(device, route_add):
    """ Unconfigure ipv6 dhcp route-add
        Args:
            device ('obj'): device to use
            route_add ('str'): route name to unconfigure example - iana-route-add, iapd-route-add
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ipv6 dhcp route-add
    """
    log.debug("Unconfiguring ipv6 dhcp {route_add}")
    config = [f"no ipv6 dhcp {route_add}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ipv6 dhcp {route_add} on {device}. Error\n{e}"
            )

def configure_ipv6_dhcp_binding_track_ppp(device):
    """ Configure ipv6 dhcp binding track ppp
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ipv6 dhcp binding track ppp
    """
    log.debug("Configuring ipv6 dhcp binding track ppp")
    try:
        device.configure('ipv6 dhcp binding track ppp')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ipv6 dhcp binding track ppp on {device}. Error\n{e}"
            )

def unconfigure_ipv6_dhcp_binding_track_ppp(device):
    """ Unconfigure ipv6 dhcp binding track ppp
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ipv6 dhcp binding track ppp
    """
    log.debug("Unconfiguring ipv6 dhcp binding track ppp")
    try:
        device.configure('no ipv6 dhcp binding track ppp')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ipv6 dhcp binding track ppp on {device}. Error\n{e}"
            )

def configure_ipv6_dhcp_relay_destination_global(device, interface, ipv6_address):
    """ Configure interface ipv6 dhcp relay destination global ipv6 address
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured # example Vlan100"
            ipv6_address ('str'): IPv6 destination address Ex: 20::1
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ipv6 dhcp relay destination global ipv6 address
    """
    log.debug("Configuring ipv6 dhcp relay destination global ipv6 address on the interface")
    cmd = [f"interface {interface}",
           f"ipv6 dhcp relay destination global {ipv6_address}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipv6 dhcp relay destination global ipv6 address on {interface}. Error\n{e}"
        )

def unconfigure_ipv6_dhcp_relay_destination_global(device, interface, ipv6_address):
    """ Unconfigure interface ipv6 dhcp relay destination global ipv6 address
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured # example Vlan100"
            ipv6_address ('str'): IPv6 destination address Ex: 20::1
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ipv6 dhcp relay destination global ipv6 address
    """
    log.debug("Unconfiguring ipv6 dhcp relay destination global ipv6 address on the interface")
    config = [f"interface {interface}",
              f"no ipv6 dhcp relay destination global {ipv6_address}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ipv6 dhcp relay destination global ipv6 address on {interface}. Error\n{e}"
        )

def configure_ipv6_dhcp_pool_functions(device, pool_name, option, vrf_name = None, pre_addr = None, ipv6_addr = None,
 dns_name = None, dns_name_ip = None ,enterprise_id = None, type = None, suboption_no = None, ascii_name = None):
    """ Configure ipv6 dhcp pool
        Args:
            device ('obj'): device to use
            pool_name ('str'): name of the pool to be created example - POOL_88
            option ('str'): option to be configure example - vrf, address, domain-name, capwap-ac, dns-server, option, vendor-specific
            vrf_name ('str', optional): vrf name to be configure example - Mgmt-vrf
            pre_addr ('str', optional): address prefix to be configure in the format x:x::y/<z> example - 2001::1/64
            ipv6_addr ('str', optional): capwap-ac address to be configure in the format X:X:X:X::X example - 2001:0DB8:0:0::1
            dns_name ('str', optional): domain-name to be configure example - cisco.com
            enterprise_id ('str', optional): vendor-specific to be configure in the range <1-4294967295> example - 100
            dns_name_ip ('str', optional): dns-server to be configure with name or ipv6 address, example - 2001:0DB8:0:0::1, abc, etc
            suboption_no ('str', optional): suboption number in the range <1-65535> example - 100
            type ('str', optional): type to be configure example - suboption
            ascii_name ('str', optional): ascii name to be configure example - cisco
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ipv6 dhcp pool
    """
    log.debug("Configuring ipv6 dhcp pool functions")
    config =[f"ipv6 dhcp pool {pool_name}"]
    if option in ['vrf']:
        config.append(f"{option} {vrf_name}")
    elif option in ['address']:
        config.append(f"{option} prefix {pre_addr}")
    elif option in ['domain-name']:
        config.append(f"{option} {dns_name}")
    elif option in ['capwap-ac']:
        config.append(f"{option} address {ipv6_addr}")
    elif option in ['dns-server']:
        config.append(f"{option} {dns_name_ip}")
    elif option in ['option']:
        config.append(f"{option} include-all")
    elif option in ['vendor-specific']:
        config.append(f"{option} {enterprise_id}")
        if type in ['suboption']:
            config.append(f"{type} {suboption_no} ascii {ascii_name}")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipv6 dhcp pool functions on {device}. Error\n{e}"
        )

def unconfigure_ipv6_dhcp_pool(device, pool_name):
    """ Unconfigure ipv6 dhcp pool
        Args:
            device ('obj'): device to use
            pool_name ('str'): name of the pool to be removed example - POOL_88
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ipv6 dhcp pool
    """
    log.debug("Unconfiguring ipv6 dhcp pool")
    config = [f"no ipv6 dhcp pool {pool_name}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ipv6 dhcp pool on {device}. Error\n{e}"
        )

def configure_interface_ipv6_dhcp_client_request_vendor(device, interface):
    """ Configure ipv6 dhcp client request vendor on the interface
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured # example  "interface vlan 100" 
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ipv6 dhcp client request vendor
    """
    log.info("Configuring ipv6 dhcp client request vendor on the interface")
    config =  [f"interface {interface}",
               f"ipv6 dhcp client request vendor"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipv6 dhcp client request vendor on the interface {interface}. Error\n{e}"
        )

def unconfigure_interface_ipv6_dhcp_client_request_vendor(device, interface):
    """ Unconfigure ipv6 dhcp client request vendor on the interface
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured # example  "interface vlan 100" 
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ipv6 dhcp client request vendor
    """
    log.info("Unconfiguring ipv6 dhcp client request vendor on the interface")
    config =  [f"interface {interface}",
               f"no ipv6 dhcp client request vendor"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ipv6 dhcp client request vendor on the interface {interface}. Error\n{e}"
        )  

def configure_interface_ipv6_dhcp_client_information(device, interface, min_time):
    """ Configure ipv6 dhcp client information refresh minimum on the interface
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured # example  "interface vlan 100" 
            min_time ('int'): Time in seconds
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ipv6 dhcp client information refresh minimum
    """
    log.info("Configuring ipv6 dhcp client information refresh minimum on the interface")
    config =  [f"interface {interface}",
               f"ipv6 dhcp client information refresh minimum {min_time}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipv6 dhcp client information refresh minimum on the interface {interface}. Error\n{e}"
        ) 

def unconfigure_interface_ipv6_dhcp_client_information(device, interface, min_time):
    """ Unconfigure ipv6 dhcp client information refresh minimum on the interface
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured # example  "interface vlan 100" 
            min_time ('int'): Time in seconds
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ipv6 dhcp client information refresh minimum
    """
    log.info("Unconfiguring ipv6 dhcp client information refresh minimum on the interface")
    config =  [f"interface {interface}",
               f"no ipv6 dhcp client information refresh minimum {min_time}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ipv6 dhcp client information refresh minimum on the interface {interface}. Error\n{e}"
        )

def configure_ipv6_dhcp_test_relay(device, ip_addr=None, opt_num=None, num=None, hex_string=None, reply=False, notification=False):
    """ Configure ipv6 dhcp test relay on device
        Args:
            device ('obj'): device to use 
            ip_addr('str'): IPv6 peer address
            opt_num ('str'): Option number
            num ('str'): Decimal option number
            hex_string ('str'): Hex bytes to add 
            reply ('bool'): DHCPv6 relay notifications, by default false
            notification ('bool'): by default false
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ipv6 dhcp test relay on device
    """
    log.info("Configuring ipv6 dhcp test relay on device")
    cmd = []
    cmd.append(f"ipv6 dhcp test relay packet-control") 
    if notification:
        cmd.append(f"ipv6 dhcp test relay notifications")
    if ip_addr:
        cmd.append(f"ipv6 dhcp test relay drop peeraddr {ip_addr}")
    if opt_num and hex_string:
        cmd.append(f"ipv6 dhcp test relay forward add {opt_num} {hex_string}")
    if reply:
        cmd.append(f"ipv6 dhcp test relay reply add vsio {num} {hex_string}")                          
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipv6 dhcp test relay on device. Error\n{e}"
        )
    
def unconfigure_ipv6_dhcp_test_relay(device, ip_addr=None, option=None, num=None, hex_string=None, reply=False, notification=False):
    """ Unconfigure ipv6 dhcp test relay on device
        Args:
            device ('obj'): device to use 
            ip_addr('str'): IPv6 peer address
            option ('str'): Option number
            num ('str'): Decimal option number
            hex_string ('str'): Hex bytes to add 
            reply ('bool',Optional): DHCPv6 relay notifications, by default false
            notification ('bool'): by default false
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ipv6 dhcp test relay on device
    """
    log.info("Unconfiguring ipv6 dhcp test relay on device")
    cmd =  []
    cmd.append(f"no ipv6 dhcp test relay packet-control")  
    if ip_addr:
        cmd.append(f"no ipv6 dhcp test relay drop peeraddr {ip_addr}")
    if option and hex_string:
        cmd.append(f"no ipv6 dhcp test relay forward add {option} {hex_string}")
    if reply:
        cmd.append(f"no ipv6 dhcp test relay reply add vsio {num} {hex_string}")
    if notification:
        cmd.append(f"no ipv6 dhcp test relay notifications")    
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ipv6 dhcp test relay on device. Error\n{e}"
        )

def configure_ipv6_dhcp_test_server(device, hex_string):
    """ Configure ipv6 dhcp test server on device
        Args:
            device ('obj'): device to use 
            hex_string ('str'): Hex bytes to add in relay packet
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ipv6 dhcp test server on device
    """
    log.info("Configuring ipv6 dhcp test server on device")
    config =  [f"ipv6 dhcp test server add vsio {hex_string}"]   
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipv6 dhcp test server on device. Error\n{e}"
        )

def unconfigure_ipv6_dhcp_test_server(device, hex_string):
    """ Unconfigure ipv6 dhcp test server on device
        Args:
            device ('obj'): device to use 
            hex_string ('str'): Hex bytes to add in relay packet
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ipv6 dhcp test server on device
    """
    log.info("Unconfiguring ipv6 dhcp test server on device")
    config =  [f"no ipv6 dhcp test server add vsio {hex_string}"]   
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ipv6 dhcp test server on device. Error\n{e}")    

def unconfigure_ipv6_dhcp_client_pd_on_interface(device, interface, prefix_name=None, rapid_commit=False,
                                               ipv6_prefix=None):
    """ unconfigure ipv6 dhcp client pd on interface
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
            prefix_name ('str', optional): Prefix name. Default is None.
            ipv6_prefix ('str', optional): IPv6 address with prefix length. Ex: ::1/128. Default is None.
            rapid_commit ('bool', optional): Rapid commit is valid if prefix name is not None. Default is False.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f'interface {interface}']
    if prefix_name:
        cmd.append(f"no ipv6 dhcp client pd {prefix_name}{' rapid-commit' if rapid_commit else ''}")
    if ipv6_prefix:
        cmd.append(f'no ipv6 dhcp client pd hint {ipv6_prefix}')
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ipv6 dhcp client pd on interface:\n{e}")

def configure_interface_ipv6_rip(device, interface, rip_name, default_information=None, default_metric=None, metric_offset=None, summary_address=None):                                       
    """
    Configure ipv6 rip on an interface.

    Args:
        device (obj): Device object
        interface (str): Interface name
        rip_name (str): RIP process name
        enable (bool, optional): Enable/disable RIP routing. Defaults to False.
        default_information (str, optional): Configure handling of default route. Options: 'only', 'originate'.
        default_metric (int, optional): Default route metric. Range: 1-15. Defaults to None.
        metric_offset (int, optional): Adjust default metric increment. Range: 1-16. Defaults to None.
        summary_address (str, optional): Configure address summarization. Defaults to None.

    Raises:
        SubCommandFailure: Failed configuring ipv6 rip on interface
    """
    log.debug(f"Configure ipv6 rip on interface {interface} with RIP name {rip_name}")
    config = [f"interface {interface}"]

    if rip_name:
        if default_information is not None:
            if default_metric is not None:
                config.append(f"ipv6 rip {rip_name} default-information {default_information} metric {default_metric}")
            else:
                config.append(f"ipv6 rip {rip_name} default-information {default_information}")
        elif metric_offset is not None:
            config.append(f"ipv6 rip {rip_name} metric-offset {metric_offset}")
        elif summary_address is not None:
            config.append(f"ipv6 rip {rip_name} summary-address {summary_address}")
        else:
            config.append(f"ipv6 rip {rip_name} enable")

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ipv6 rip on interface {interface}. Error\n{e}"
        )   

def unconfigure_interface_ipv6_rip(device, interface, rip_name, default_information=None, default_metric=None, metric_offset=None, summary_address=None):                                       
    """
    Unconfigure ipv6 rip on an interface.

    Args:
        device (obj): Device object
        interface (str): Interface name
        rip_name (str): RIP process name
        enable (bool, optional): Enable/disable RIP routing. Defaults to False.
        default_information (str, optional): Configure handling of default route. Options: 'only', 'originate'.
        default_metric (int, optional): Default route metric. Range: 1-15. Defaults to None.
        metric_offset (int, optional): Adjust default metric increment. Range: 1-16. Defaults to None.
        summary_address (str, optional): Configure address summarization. Defaults to None.

    Raises:
        SubCommandFailure: Failed unconfiguring ipv6 rip on interface
    """
    log.debug(f"Unconfigure ipv6 ripon interface {interface} with RIP name {rip_name}")
    config = [f"interface {interface}"]

    if rip_name:
        if default_information is not None:
            if default_metric is not None:
                config.append(f"no ipv6 rip {rip_name} default-information {default_information} metric {default_metric}")
            else:
                config.append(f"no ipv6 rip {rip_name} default-information {default_information}")
        elif metric_offset is not None:
            config.append(f"no ipv6 rip {rip_name} metric-offset {metric_offset}")
        elif summary_address is not None:
            config.append(f"no ipv6 rip {rip_name} summary-address {summary_address}")
        else:
            config.append(f"no ipv6 rip {rip_name} enable")

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ipv6 rip on interface {interface}. Error\n{e}"
        )

def configure_interface_ipv6_dhcp_server_allow_hint(device, interface, pool_name):
    """ Configure ipv6 dhcp server {pool_name} allow-hint on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            pool_name ('str'): pool name to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring ipv6 dhcp server {pool_name} allow-hint on interface
    """
    log.debug("Configure ipv6 dhcp server {pool_name} allow-hint on interface")
    config = [
             f"interface {interface}",
             f"ipv6 dhcp server {pool_name} allow-hint",
            ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ipv6 dhcp server {pool_name} allow-hint on interface {interface}. Error\n{e}"
            )
    
def unconfigure_interface_ipv6_dhcp_server_allow_hint(device, interface, pool_name):
    """ Unconfigure ipv6 dhcp server {pool_name} allow-hint on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            pool_name ('str'): pool name to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring ipv6 dhcp server {pool_name} allow-hint on interface
    """
    log.debug("Unconfigure ipv6 dhcp server {pool_name} allow-hint on interface")
    config = [
             f"interface {interface}",
             f"no ipv6 dhcp server {pool_name} allow-hint",
            ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ipv6 dhcp server {pool_name} allow-hint on interface {interface}. Error\n{e}"
            )

def configure_ipv6_dhcp_server(device, option, type):
    """ Configure ipv6 dhcp server on device
        Args:
            device ('obj'): device to use
            option ('str'): option to configure (eg. join, vrf)
            type ('str'): type to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring ipv6 dhcp server on device
    """
    log.debug("Configure ipv6 dhcp server on device")
    config = [f"ipv6 dhcp server {option} {type}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ipv6 dhcp server on device. Error\n{e}"
            )        

def unconfigure_ipv6_dhcp_server(device, option, type):
    """ Unconfigure ipv6 dhcp server on device
        Args:
            device ('obj'): device to use
            option ('str'): option to configure (eg. join, vrf)
            type ('str'): type to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring ipv6 dhcp server on device
    """
    log.debug("Unconfigure ipv6 dhcp server on device")
    config = [f"no ipv6 dhcp server {option} {type}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ipv6 dhcp server on device. Error\n{e}"
            )

def configure_ipv6_dhcp_relay_option(device, option):
    """ Configure ipv6 dhcp-relay option on device
        Args:
            device ('obj'): device to use
            option ('str'): option to configure (eg. client-link-add, vpn)
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring ipv6 dhcp-relay option on device
    """
    log.debug("Configure ipv6 dhcp-relay option on device")
    config = [f"ipv6 dhcp-relay option {option}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ipv6 dhcp-relay option on device. Error\n{e}"
            )

def unconfigure_ipv6_dhcp_relay_option(device, option):
    """ Unconfigure ipv6 dhcp-relay option on device
        Args:
            device ('obj'): device to use
            option ('str'): option to configure (eg. client-link-address, vpn)
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring ipv6 dhcp-relay option on device
    """
    log.debug("Unconfigure ipv6 dhcp-relay option on device")
    config = [f"no ipv6 dhcp-relay option {option}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ipv6 dhcp-relay option on device. Error\n{e}"
            )            