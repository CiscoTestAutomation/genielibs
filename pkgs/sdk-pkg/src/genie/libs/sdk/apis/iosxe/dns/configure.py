"""Common configure functions for DNS"""


# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_ip_domain_lookup(
    device,
    source_interface=None,
):
    """ Enable domain lookup 
        Args:
            device ('obj'): device to use
            source_interface ('string', Optional): Name of the interface
        Returns:
            console output
        Raises:
            SubCommandFailure: domian configuration
    """

    cmd = ['ip domain lookup']
    if source_interface:
        cmd.append(f"ip domain lookup source-interface {source_interface}")
    
    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure domain lookup. Error:\n{error}'.format(error=e)
        )
    return out

def unconfigure_ip_domain_lookup(
    device, 
    source_interface=None,
):
    """ Disable ip domain lookup 
        Args:
            device ('obj'): device to use
        Returns:
            console output
        Raises:
            SubCommandFailure: domian Unconfiguration
    """
    cmd = ['no ip domain lookup']
    if source_interface:
        cmd.append(f"no ip domain lookup source-interface {source_interface}")

    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not Un-configure domain lookup. Error:\n{error}'.format(error=e)
        )
    return out

def configure_ip_name_server(
    device, 
    domain_ip,
    vrf=None,
):
    """ Enable ip name server 
        Args:
            device ('obj'): device to use
            domain_ip ('str'): dns server ip or proxy server ip.
            vrf ('str', Optional): name of the vrf
        Returns:
            console output
        Raises:
            SubCommandFailure: domian configuration
    """
    if vrf:
        cmd = f"ip name-server vrf {vrf} {domain_ip}"
    else:
        cmd = f"ip name-server {domain_ip}"
    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ip name server . Error:\n{error}".format(error=e)
        )
    return out

def unconfigure_ip_name_server(
    device, 
    domain_ip,
    vrf=None,
):
    """ Disable ip name server
        Args:
            device ('obj'): device to use
            domain_ip ('str'): dns server ip or proxy server ip.
            vrf ('str', Optional): name of the vrf
        Returns:
            console output
        Raises:
            SubCommandFailure: domian Unconfiguration
    """

    if vrf:
        cmd = f"no ip name-server vrf {vrf} {domain_ip}"
    else:
        cmd = f"no ip name-server {domain_ip}"
        
    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Un-configure ip name server. Error:\n{error}".format(error=e)
        )
    return out

def configure_ip_host(
    device, 
    hostname,
    ip_address,
    vrf=None,
):
    """ Configure ip host with domain name and ip address 
        Args:
            device ('obj'): device to use
            hostname ('str'): Name of the host
            ip_address ('str'): IP Address of the host
            vrf ('str', Optional): name of the vrf
        Returns:
            console output
        Raises:
            SubCommandFailure: ip host configuration
    """

    if vrf:
        cmd = f"ip host vrf {vrf} {hostname}"
    else:
        cmd = f"ip host {hostname}"
    
    if isinstance(ip_address, list):
        cmd += " " + " ".join(ip_address)
    else:
        cmd += f" {ip_address}"

    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ip host. Error:\n{error}".format(error=e)
        )
    return out

def unconfigure_ip_host(
    device, 
    hostname,
    ip_address,
    vrf=None,
):
    """ Enable ip name server 
        Args:
            device ('obj'): device to use
            hostname ('str'): Name of the host
            ip_address ('str'): IP Address of the host
            vrf ('str', Optional): name of the vrf
        Returns:
            console output
        Raises:
            SubCommandFailure: ip host Un-configuration
    """

    if vrf:
        cmd = f"no ip host vrf {vrf} {hostname}"
    else:
        cmd = f"no ip host {hostname}"

    if isinstance(ip_address, list):
        cmd += " " + " ".join(ip_address)
    else:
        cmd += f" {ip_address}"
    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Un-configure ip host. Error:\n{error}".format(error=e)
        )
    return out

def configure_ip_dns_server(
    device
):
    """ Enable ip DNS server 
        Args:
            device ('obj'): device to use
        Returns:
            console output
        Raises:
            SubCommandFailure: DNS configuration
    """

    cmd = f"ip dns server"
    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ip dns server . Error:\n{error}".format(error=e)
        )
    return out

def unconfigure_ip_dns_server(
    device
):
    """ Disable ip DNS server 
        Args:
            device ('obj'): device to use
        Returns:
            console output
        Raises:
            SubCommandFailure: DNS Un-configuration
    """

    cmd = f"no ip dns server"
    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Un-configure ip dns server . Error:\n{error}".format(error=e)
        )
    return out

def configure_ip_host_view(
    device, 
    viewname,
    hostname,
    ip_addresses=None,
):
    """ Configure ip host with domain name and optional ip addresses 
        Args:
            device ('obj'): device to use
            viewname ('str'): Name of the view name
            hostname ('str'): Name of the host
            ip_addresses ('list', optional): List of IP Addresses for the host. Default is None
            
        Returns:
            console output
        Raises:
            SubCommandFailure: ip host configuration
    """
    cmd = f"ip host view {viewname} {hostname}"
    if ip_addresses:
        if isinstance(ip_addresses, list):
            cmd += " " + " ".join(ip_addresses)
        else:
            cmd += f" {ip_addresses}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ip host view. Error:\n{error}".format(error=e)
        )
    
def unconfigure_ip_host_view(
    device, 
    viewname,
    hostname,
    ip_addresses=None,
):
    """ Unconfigure ip host view with domain name and optional ip addresses 
        Args:
            device ('obj'): device to use
            viewname ('str'): Name of the view name
            hostname ('str'): Name of the host
            ip_addresses ('list', optional): List of IP Addresses for the host. Default is None
            
        Returns:
            console output
        Raises:
            SubCommandFailure: ip host view unconfiguration
    """
    cmd = f"no ip host view {viewname} {hostname}"
    if ip_addresses:
        if isinstance(ip_addresses, list):
            cmd += " " + " ".join(ip_addresses)
        else:
            cmd += f" {ip_addresses}"
    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure ip host view. Error:\n{error}".format(error=e)
        )
    return out    
       
def configure_ip_dns_view_list(
    device,
    view_list_name,
    view_name=None,
    default_view=False,
    evaluation_order=None,
    vrf_name=None,
):
    """ Configure ip dns view list 
        Args:
            device ('obj'): device to use
            view_list_name ('str'): Name of the view list
            view_name ('str', Optional): Name of the view
            default_view ('bool', Optional): Configure default view
            evaluation_order ('str', Optional): Evaluation order of the view
            vrf_name ('str', Optional): Name of the vrf
        Returns:
            console output
        Raises:
            SubCommandFailure: ip dns view list configuration
    """

    cmd = [f"ip dns view-list {view_list_name}"]
    if vrf_name:
        if default_view:
            cmd.append(f"view vrf {vrf_name} default {view_name} {evaluation_order}")
        else:
            cmd.append(f"view vrf {vrf_name} {view_name} {evaluation_order}")
    else:
        if default_view:
            cmd.append(f"view default {view_name} {evaluation_order}")
        else:
            cmd.append(f"view {view_name} {evaluation_order}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ip dns view list. Error:\n{error}".format(error=e)
        )

def unconfigure_ip_dns_view_list(
    device,
    view_list_name,
):
    """ Unconfigure ip dns view list 
        Args:
            device ('obj'): device to use
            view_list_name ('str'): Name of the view list
        Returns:
            console output
        Raises:
            SubCommandFailure: ip dns view list unconfiguration
    """

    cmd = f"no ip dns view-list {view_list_name}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure ip dns view list. Error:\n{error}".format(error=e)
        )        

def configure_ip_dns_view(
    device,
    default_view=False,
    view_name=None,
    vrf_name=None,
    action=False,
    action_type="forwarding",
):
    """ Configure ip dns view 
        Args:
            device ('obj'): device to use
            view_name ('str', Optional): Name of the view
            default_view ('bool', Optional): Configure default view
            vrf_name ('str', Optional): Name of the vrf
            action ('bool', Optional): Configure dns forwarding or no dns forwarding
            action_type ('str', Optional): Type of action to be configured. Default is "forwarding".
        Returns:
            None
        Raises:
            SubCommandFailure: ip dns view configuration
    """

    cmd = f"ip dns view"
    if vrf_name:
        cmd += f" vrf {vrf_name}"
    if view_name and not default_view:
        cmd += f" {view_name}\n"
    if default_view and view_name is None:
        cmd += f" default\n"
    if action:
        cmd += f"dns {action_type}"
    else:
        cmd += f"no dns {action_type}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ip dns view. Error:\n{error}".format(error=e)
        )

def unconfigure_ip_dns_view(device, view_name=None, default_view=False, vrf_name=None):
    """ Unconfigure ip dns view 
        Args:
            device ('obj'): device to use
            view_name ('str', Optional): Name of the view
            default_view ('bool', Optional): Configure default view
            vrf_name ('str', Optional): Name of the vrf
        Returns:
            None
        Raises:
            SubCommandFailure: ip dns view unconfiguration
    """

    cmd = f"no ip dns view"
    if vrf_name:
        cmd += f" vrf {vrf_name}"
    if view_name and not default_view:
        cmd += f" {view_name}"
    if default_view and view_name is None:
        cmd += " default"    

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure ip dns view. Error:\n{error}".format(error=e)
        )

def configure_ip_host_vrf_view(device, vrf_name, view_name=None, hostname=None, ip_address=None):
    '''Configure ip host vrf <vrf_name>
        Args:
            device ('obj'): device to use
            vrf_name ('str'): Name of the VRF
            view_name ('str', Optional): Name of the DNS view. Default is None
            hostname ('str', Optional): Name of the host. Default is None
            ip_address ('list' or 'str', Optional): IP Address of the host. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configure ip host vrf view
    '''

    cmd = f"ip host vrf {vrf_name}"
    if view_name:
        cmd += f" view {view_name}"    
    if hostname:
        cmd += f" {hostname}"
    if ip_address:
        if isinstance(ip_address, list):
            cmd += " " + " ".join(ip_address)
        else:
            cmd += f" {ip_address}"    
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ip host vrf view. Error:\n{error}".format(error=e)
        )

def unconfigure_ip_host_vrf_view(device, vrf_name, view_name=None, hostname=None, ip_address=None):
    '''Unconfigure ip host vrf <vrf_name>
        Args:
            device ('obj'): device to use
            vrf_name ('str'): Name of the VRF
            view_name ('str', Optional): Name of the DNS view. Default is None
            hostname ('str', Optional): Name of the host. Default is None
            ip_address ('list' or 'str', Optional): IP Address of the host. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfigure ip host vrf view
    '''

    cmd = f"no ip host vrf {vrf_name}"
    if view_name:
        cmd += f" view {view_name}"    
    if hostname:
        cmd += f" {hostname}"
    if ip_address:
        if isinstance(ip_address, list):
            cmd += " " + " ".join(ip_address)
        else:
            cmd += f" {ip_address}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure ip host vrf view. Error:\n{error}".format(error=e)
        )                             

def configure_interface_ip_dns_view_group(
    device,
    interface,
    view_group_name
):
    """  ip dns view-group on an interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface name (e.g., 'GigabitEthernet1/0/1')
            view_group_name ('str'): DNS view-group name
        Returns:
            console output
        Raises:
            SubCommandFailure: Failed to configure ip dns view-group on interface
    """
    log.debug(f"Configuring ip dns view-group {view_group_name} on interface {interface}")

    cmd = [
        f"interface {interface}",
        f"ip dns view-group {view_group_name}"
    ]
    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ip dns view-group {view_group_name} on interface {interface}. Error:\n{e}"
        )
    return out

def unconfigure_interface_ip_dns_view_group(
    device,
    interface,
    view_group_name
):
    """ Unconfigure ip dns view-group from an interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface name (e.g., 'GigabitEthernet1/0/1')
            view_group_name ('str'): DNS view-group name
        Returns:
            console output
        Raises:
            SubCommandFailure: Failed to unconfigure ip dns view-group on interface
    """
    log.debug(f"Unconfiguring ip dns view-group {view_group_name} from interface {interface}")

    cmd = [
        f"interface {interface}",
        f"no ip dns view-group {view_group_name}"
    ]

    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ip dns view-group from interface {interface}. Error:\n{e}"
        )
    return out
