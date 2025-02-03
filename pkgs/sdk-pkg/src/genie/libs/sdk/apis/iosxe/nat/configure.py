"""Common configure functions for nat"""
# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Statement, Dialog
from unicon.eal.dialogs import Dialog, Statement

log = logging.getLogger(__name__)

def configure_nat_in_out(
    device, 
    inside_interface=None, 
    outside_interface=None,
):
    """ Enable nat IN and OUT over interface 
        Args:
            device ('obj'): device to use
            inside_interface ('str'): enable nat in over this interface, default value is None
            outside_interface ('str'): enable nat out over this interface, default value is None
        Returns:
            console output
        Raises:
            SubCommandFailure: NAT IN OUT not enable over interface
    """
    cmd = []
    if inside_interface:
        cmd.append("interface {}".format(inside_interface))
        cmd.append("ip nat inside")

    if outside_interface:
        cmd.append("interface {}".format(outside_interface))
        cmd.append("ip nat outside")

    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Enable NAT. Error:\n{error}".format(error=e)
        )
    return out

def configure_nat_overload_rule(
    device, 
    interface, 
    access_list_name,
    overload=True
):
    """ Configure interface overloaad rule
        Args:
            device ('obj'): device to use
            interface ('str'): Interface which will use for overlad rule
            access_list_name ('str'): Name of extended access list
            overload ('bool', optional): overload True or False. Default is True
        Returns:
            console output
        Raises:
            SubCommandFailure: Nat overload rule not connfigured
    """
    cmd = f'ip nat inside source list {access_list_name} interface {interface}'
    if overload:
        cmd += ' overload'
    out = None
    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Configure NAT overload rule. Error:\n{error}".format(error=e)
        )
    return out

def unconfigure_nat_in_out(
    device, 
    inside_interface=None, 
    outside_interface=None,
):
    """ Disable nat IN and OUT over interface 
        Args:
            device ('obj'): device to use
            inside_interface ('str'): Disable nat in from this interface, default value is None
            outside_interface ('str'): Disable nat out From this interface, default value is None
        Returns:
            console output
        Raises:
            SubCommandFailure: NAT IN OUT not enable over interface
    """
    cmd = []
    if inside_interface:
        cmd.append("interface {}".format(inside_interface))
        cmd.append("no ip nat inside")
    if outside_interface:
        cmd.append("interface {}".format(outside_interface))
        cmd.append("no ip nat outside")

    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Disable NAT. Error:\n{error}".format(error=e)
        )
    return out

def unconfigure_nat_overload_rule(
    device, 
    interface, 
    access_list_name,
):
    """ UnConfigure interface overload rule
        Args:
            device ('obj'): device to use
            interface ('str'): Interface which will use for overlad rule
            access_list_name ('str'): Name of extended access list
        Returns:
            console output
        Raises:
            SubCommandFailure: Nat overload rule not unconfigured
    """
    cmd = ["no ip nat inside source list {} interface {} overload".format(access_list_name, interface)]

    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not UnConfigure NAT overload rule. Error:\n{error}".format(error=e)
        )
    return out

def configure_nat_pool(device, pool_name, pool_start_ip=None, pool_end_ip=None, network_mask=None,
        prefix_length=None, pool_type=None, start_ip_address=None, end_ip_address=None):
    """ Configure NAT pool
        Args:
            device ('obj'): device to use
            pool_name ('str'): Name of pool
            pool_start_ip ('str', optional): Pool start ip. Default is None
            pool_end_ip ('str', optional) : Pool end ip. Default is None
            network_mask ('str', optional) : Network mask. Default is None
            prefix_length ('str', optional) : Network prefix length. Default is None
            pool_type ('str', optional) : pool type. ex: match-host. Default is None
            start_ip_address ('str', optional): address start ip. Default is None
            end_ip_address ('str', optional) : address end ip. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure: NAT pool not configured
    """
    cmd = [f'ip nat pool {pool_name}']
    if pool_start_ip and pool_end_ip:
        cmd[0] += f' {pool_start_ip} {pool_end_ip}'
    if network_mask:
        cmd[0] += f' netmask {network_mask}'
        if start_ip_address and end_ip_address:
            cmd.append(f'address {start_ip_address} {end_ip_address}')
    elif prefix_length:
        cmd[0] += f' prefix-length {prefix_length}'
        if start_ip_address and end_ip_address:
            cmd.append(f'address {start_ip_address} {end_ip_address}')
    if pool_type:
        cmd[0] += f' type {pool_type}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not Configure NAT pool")

def unconfigure_nat_pool(
    device, 
    pool_name, 
    pool_start_ip,
    pool_end_ip,
    network_mask = None,
    prefix_length = None
):
    """ Configure NAT pool
        Args:
            device ('obj'): device to use
            pool_name ('str'): Name of pool
            pool_start_ip ('str'): Pool start ip
            pool_end_ip ('str') : Pool end ip
            network_mask ('str', optional) : Network mask. Default is None
            prefix_length ('int', optional) : Prefix length. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure: NAT pool not configured
    """
    cmd = f"no ip nat pool {pool_name} {pool_start_ip} {pool_end_ip}"
    if network_mask:
        cmd += f' netmask {network_mask}'
    elif prefix_length:
        cmd += f' prefix-length {prefix_length}'

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not UnConfigure NAT pool")
    
def configure_static_nat_route_map_rule(
    device, 
    inside_local_ip, 
    inside_global_ip,
    route_map_name,
    no_alias=False
):
    """ Configure static NAT route-map rule
        Args:
            device ('obj'): device to use
            inside_local_ip ('str'): Inside local ip
            inside_global_ip ('str'): Inside global ip
            route_map_name ('str') : Name of route-map
            no_alias ('bool', optional): no alias static route. Default is False
        Returns:
            None
        Raises:
            SubCommandFailure: static NAT route-map rule not configured
    """
    cmd = "ip nat inside source static {} {} route-map {}".format(
              inside_local_ip,inside_global_ip,route_map_name)
    if no_alias:
        cmd += " no-alias"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not Configure static NAT route-map rule")
 
def unconfigure_static_nat_route_map_rule(
    device, 
    inside_local_ip, 
    inside_global_ip,
    route_map_name,
    no_alias=False
):
    """ UnConfigure static NAT route-map rule
        Args:
            device ('obj'): device to use
            inside_local_ip ('str'): Inside local ip
            inside_global_ip ('str'): Inside global ip
            route_map_name ('str') : Name of route-map
            no_alias ('bool', optional): no alias static route. Default is False
        Returns:
            None
        Raises:
            SubCommandFailure: static NAT route-map rule not unconfigured
    """
    cmd = "no ip nat inside source static {} {} route-map {}".format(
              inside_local_ip,inside_global_ip,route_map_name)
    if no_alias:
        cmd += " no-alias"          
    
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not UnConfigure static NAT route-map rule")
    
def configure_nat_port_route_map_rule(
    device,
    protocol, 
    inside_local_ip, 
    local_port,
    inside_global_ip,
    global_port,
    route_map_name
):
    """ Configure NAT port route-map rule
        Args:
            device ('obj'): device to use
            protocol ('str'): Protocol 
            inside_local_ip ('str'): Inside local ip
            local_port ('str'): Local port
            inside_global_ip ('str'): Inside global ip
            global_port ('str'): Global port
            route_map_name ('str') : Name of route-map
        Returns:
            None
        Raises:
            SubCommandFailure: NAT port route-map rule not configured
    """
    cmd = ["ip nat inside source static {} {} {} {} {} route-map {}".format(
              protocol,inside_local_ip,local_port,inside_global_ip,global_port,route_map_name)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not Configure NAT port route-map rule")
    
def unconfigure_nat_port_route_map_rule(
    device, 
    protocol,
    inside_local_ip, 
    local_port,
    inside_global_ip,
    global_port,
    route_map_name
):
    """ UnConfigure NAT port route-map rule
        Args:
            device ('obj'): device to use
            protocol ('str'): Protocol 
            inside_local_ip ('str'): Inside local ip
            local_port ('str'): Local port
            inside_global_ip ('str'): Inside global ip
            global_port ('str'): Global port
            route_map_name ('str') : Name of route-map
        Returns:
            None
        Raises:
            SubCommandFailure: NAT port route-map rule not unconfigured
    """
    cmd = ["no ip nat inside source static {} {} {} {} {} route-map {}".format(
              protocol,inside_local_ip,local_port,inside_global_ip,global_port,route_map_name)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not UnConfigure NAT port route-map rule")
        
def configure_dynamic_nat_route_map_rule(
    device,
    route_map_name,
    pool_name
):
    """ Configure dynamic NAT route-map rule
        Args:
            device ('obj'): device to use
            route_map_name ('str'): Name of route-map
            pool_name ('str'): Name of pool
        Returns:
            None
        Raises:
            SubCommandFailure: dynamic NAT route-map rule not configured
    """
    cmd = ["ip nat inside source route-map {} pool {}".format(
              route_map_name,pool_name)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not Configure dynamic NAT route-map rule")
        
def unconfigure_dynamic_nat_route_map_rule(
    device, 
    route_map_name,
    pool_name
):
    """ UnConfigure dynamic NAT route-map rule
        Args:
            device ('obj'): device to use
            route_map_name ('str'): Name of route-map
            pool_name ('str'): Name of pool
        Returns:
            None
        Raises:
            SubCommandFailure: dynamic NAT route-map rule not unconfigured
    """
    cmd = ["no ip nat inside source route-map {} pool {}".format(
              route_map_name,pool_name)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not UnConfigure dynamic NAT route-map rule")
        
def configure_dynamic_nat_pool_overload_route_map_rule(
    device,
    route_map_name,
    pool_name
):
    """ Configure dynamic NAT pool overload route-map rule
        Args:
            device ('obj'): device to use
            route_map_name ('str'): Name of route-map
            pool_name ('str'): Name of pool
        Returns:
            None
        Raises:
            SubCommandFailure: dynamic NAT pool overload route-map rule not configured
    """
    cmd = ["ip nat inside source route-map {} pool {} overload".format(
              route_map_name,pool_name)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Could not Configure dynamic NAT pool overload route-map rule")
        
def unconfigure_dynamic_nat_pool_overload_route_map_rule(
    device,
    route_map_name,
    pool_name
):
    """ UnConfigure dynamic NAT pool overload route-map rule
        Args:
            device ('obj'): device to use
            route_map_name ('str'): Name of route-map
            pool_name ('str'): Name of pool
        Returns:
            None
        Raises:
            SubCommandFailure: dynamic NAT pool overload route-map rule not unconfigured
    """
    cmd = ["no ip nat inside source route-map {} pool {} overload".format(
              route_map_name,pool_name)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not UnConfigure dynamic NAT pool overload route-map rule") 
        
def configure_dynamic_nat_interface_overload_route_map_rule(
    device,
    route_map_name,
    out_interface
):
    """ Configure dynamic NAT interface overload route-map rule
        Args:
            device ('obj'): device to use
            route_map_name ('str'): Name of route-map
            out_interface ('str'): Out interface
        Returns:
            None
        Raises:
            SubCommandFailure: dynamic NAT interface overload route-map rule not configured
    """
    cmd = ["ip nat inside source route-map {} interface {} overload".format(
              route_map_name,out_interface)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not Configure dynamic NAT interface overload route-map rule")
        
def unconfigure_dynamic_nat_interface_overload_route_map_rule(
    device,
    route_map_name,
    out_interface
):
    """ UnConfigure dynamic NAT interface overload route-map rule
        Args:
            device ('obj'): device to use
            route_map_name ('str'): Name of route-map
            out_interface ('str'): Out interface
        Returns:
            None
        Raises:
            SubCommandFailure: dynamic NAT interface overload route-map rule not unconfigured
    """
    cmd = ["no ip nat inside source route-map {} interface {} overload".format(
              route_map_name,out_interface)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not UnConfigure dynamic NAT interface overload route-map rule")
        
def configure_standard_access_list(
    device,
    acl_number,
    permission,
    source_ip,
    wild_mask    
):
    """ Configure standard access-list
        Args:
            device ('obj'): device to use
            acl_number ('str'): Acl number
            permission ('str'): (permit | deny)
            source_ip ('str'): Source ip
            wild_mask ('str'): Wild mask
        Returns:
            None
        Raises:
            SubCommandFailure: standard access-list not configured
    """
    cmd = ["access-list {} {} {} {}".format(
              acl_number,permission,source_ip,wild_mask)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not Configure standard access-list")

def unconfigure_standard_access_list(
    device,
    acl_number,
    permission,
    source_ip,
    wild_mask    
):
    """ UnConfigure standard access-list
        Args:
            device ('obj'): device to use
            acl_number ('str'): Acl number
            permission ('str'): (permit | deny)
            source_ip ('str'): Source ip
            wild_mask ('str'): Wild mask
        Returns:
            None
        Raises:
            SubCommandFailure: standard access-list not unconfigured
    """
    cmd = ["no access-list {} {} {} {}".format(
              acl_number,permission,source_ip,wild_mask)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not UnConfigure standard access-list")
        
def configure_enable_nat_scale(device, timeout=60, nat_aot=True, nat_scale=True):

    """ Configure enable NAT scale
        Args:
            device (`obj`): Device object
            timeout ('int', optional): Max time for enable nat scale.Defaults to 60
            nat_aot ('boolean', optional): Flag to enable nat aot
            nat_scale ('boolean', optional): Flag to enable nat scale
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    
    dialog = Dialog([
             Statement(
             pattern=r'.*% Are you sure you want to continue\? \[yes\]',
             action='sendline(yes)',
             loop_continue=False,
             continue_timer=False)])
    command = []       
    if nat_aot:
        command.append("no ip nat create flow-entries")
    if nat_scale:
        command.append("nat scale")
        
    try:
       device.configure(
       command,
       reply=dialog,
       timeout=timeout,
       append_error_pattern=['.*Command cannot be executed.*'])
       
    except Exception as err:
        log.error("Failed to configure nat scale: {err}".format(err=err))
        raise Exception(err)  
        
def configure_dynamic_nat_rule(
    device,
    acl_name,
    pool_name   
):
    """ Configure dynamic NAT rule
        Args:
            device ('obj'): device to use
            acl_name ('str'): Acl name
            pool_name ('str'): Pool name
        Returns:
            None
        Raises:
            SubCommandFailure: dynamic NAT rule not configured
    """
    cmd = ["ip nat inside source list {} pool {}".format(
              acl_name,pool_name)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not Configure dynamic NAT rule")

def unconfigure_dynamic_nat_rule(
    device,
    acl_name,
    pool_name   
):
    """ UnConfigure dynamic NAT rule
        Args:
            device ('obj'): device to use
            acl_name ('str'): Acl name
            pool_name ('str'): Pool name
        Returns:
            None
        Raises:
            SubCommandFailure: dynamic NAT rule not unconfigured
    """
    cmd = ["no ip nat inside source list {} pool {}".format(
              acl_name,pool_name)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not UnConfigure dynamic NAT rule") 

def configure_static_nat_network_rule(
    device,
    inside_local_ip,
    inside_global_ip,
    mask 
):
    """ Configure static NAT network rule
        Args:
            device ('obj'): device to use
            inside_local_ip ('str'): inside local ip
            inside_global_ip ('str'): inside global ip
            mask('str'):network mask
        Returns:
            None
        Raises:
            SubCommandFailure: static NAT network rule not configured
    """
    cmd = "ip nat inside source static network {} {} {}".format(
              inside_local_ip, inside_global_ip, mask)
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not Configure static NAT network rule")

def unconfigure_static_nat_network_rule(
    device,
    inside_local_ip,
    inside_global_ip,
    mask
):
    """ UnConfigure static NAT network rule
        Args:
            device ('obj'): device to use
            inside_local_ip ('str'): inside local ip
            inside_global_ip ('str'): inside global ip
            mask('str'):network mask
        Returns:
            None
        Raises:
            SubCommandFailure: static NAT network rule not unconfigured
    """
    cmd = "no ip nat inside source static network {} {} {}".format(
              inside_local_ip, inside_global_ip, mask)
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure static NAT network rule")
        
def configure_static_nat_rule(
    device, 
    inside_local_ip, 
    inside_global_ip,
    l4_protocol = None,
    inside_port = None,
    outside_port = None,
    extendable = False,
    vrf=None,
    no_alias=False
):
    """ Configure static NAT rule
        Args:
            device ('obj'): device to use
            inside_local_ip ('str'): inside local ip
            inside_global_ip ('str'): inside global ip
            l4_protocol ('str', optional): tcp ot udp protocol. Default is None
            inside_port ('int', optional): tcp ot udp inside port number. Default is None
            outside_port ('int', optional): tcp ot udp outside port number. Default is None
            extendable ('bool', optional): extend the translation. Default is False
            vrf ('str', optional): vrf name. Default is None
            no_alias ('bool', optional): no alias static route. Default is False
        Returns:
            None
        Raises:
            SubCommandFailure: static NAT rule not configured
    """
    cmd = f"ip nat inside source static {inside_local_ip} {inside_global_ip}"
    if l4_protocol:
        cmd = f"ip nat inside source static {l4_protocol} {inside_local_ip} {inside_port} {inside_global_ip} {outside_port}"
    if vrf:
        cmd += f" vrf {vrf}"
    if extendable:
        cmd += ' extendable'
    if no_alias:
        cmd += " no-alias"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not Configure static NAT rule. Error:\n{e}")
        
def unconfigure_static_nat_rule(
    device, 
    inside_local_ip, 
    inside_global_ip,
    l4_protocol = None,
    inside_port = None,
    outside_port = None,
    extendable = False,
    vrf=None,
    no_alias=False
):
    """ UnConfigure static NAT rule
        Args:
            device ('obj'): device to use
            inside_local_ip ('str'): inside local ip
            inside_global_ip ('str'): inside global ip
            l4_protocol ('str', optional): tcp ot udp protocol. Default is None
            inside_port ('int', optional): tcp ot udp inside port number. Default is None
            outside_port ('int', optional): tcp ot udp outside port number. Default is None
            extendable ('bool', optional): extend the translation. Default is False
            vrf ('str', optional): vrf name. Default is None
            no_alias ('bool', optional): no alias static route. Default is False
        Returns:
            None
        Raises:
            SubCommandFailure: static NAT rule not unconfigured
    """
    dialog = Dialog([Statement(pattern=r'\[no\].*', action='sendline(yes)',loop_continue=True,continue_timer=False)])
    cmd = f"no ip nat inside source static {inside_local_ip} {inside_global_ip}"
    if l4_protocol:
        cmd = f"no ip nat inside source static {l4_protocol} {inside_local_ip} {inside_port} {inside_global_ip} {outside_port}"
    if vrf:
        cmd += f" vrf {vrf}"
    if extendable:
        cmd += ' extendable'
    if no_alias:
        cmd += " no-alias"
    try:
        device.configure(cmd,reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not UnConfigure static NAT rule. Error:\n{e}")
        
def configure_static_nat_outside_rule(device, outside_global_address, outside_local_address,
        l4_protocol=None, global_port=None, local_port=None, network=False, network_mask=None,
        extendable=False, add_route=False, vrf=None):
    """ Configure static NAT outside rule 
        Args:
            device ('obj'): device to use
            outside_global_address ('str'): outside global address
            outside_local_address ('str'): outside local address
            l4_protocol ('str', optional): tcp ot udp protocol. Default is None
            global_port ('int', optional): tcp ot udp global port number. Default is None
            local_port ('int', optional): tcp ot udp local port number. Default is None
            network ('bool', optional): configures static netwrok. Default is False
            network_mask ('str', optional): network mask or prefix. Default is None
            extendable ('bool', optional): extend the translation. Default is False
            add_route ('bool', optional): add static route. Default is False
            vrf ('str', optional): vrf name. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure: static NAT outside rule not configured
    """
    cmd = 'ip nat outside source static'
    if l4_protocol and global_port and local_port:
        cmd += f' {l4_protocol} {outside_global_address} {global_port} {outside_local_address} {local_port}'
    elif network and network_mask:
        cmd += f' network {outside_global_address} {outside_local_address} {network_mask}'
    else:
        cmd += f' {outside_global_address} {outside_local_address}'
    if vrf:
        cmd += f" vrf {vrf}"
    if extendable:
        cmd += ' extendable'
    if add_route:
        cmd += ' add-route'

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not Configure static NAT outside rule")
        
def unconfigure_static_nat_outside_rule(device, outside_global_address, outside_local_address,
        l4_protocol=None, global_port=None, local_port=None, network=False, network_mask=None,
        extendable=False, add_route=True, vrf=None):
    """ UnConfigure static NAT outside rule 
        Args:
            device ('obj'): device to use
            outside_global_address ('str'): outside global address
            outside_local_address ('str'): outside local address
            l4_protocol ('str', optional): tcp ot udp protocol. Default is None
            global_port ('int', optional): tcp ot udp global port number. Default is None
            local_port ('int', optional): tcp ot udp local port number. Default is None
            network ('bool', optional): configures static netwrok. Default is False
            network_mask ('str', optional): network mask or prefix. Default is None
            extendable ('bool', optional): extend the translation. Default is False
            add_route ('bool', optional): add static route. Default is True
            vrf ('str', optional): vrf name. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure: static NAT outside rule not unconfigured
    """
    cmd = 'no ip nat outside source static'
    if l4_protocol and global_port and local_port:
        cmd += f' {l4_protocol} {outside_global_address} {global_port} {outside_local_address} {local_port}'
    elif network and network_mask:
        cmd += f' network {outside_global_address} {outside_local_address} {network_mask}'
    else:
        cmd += f' {outside_global_address} {outside_local_address}'
    if vrf:
        cmd += f" vrf {vrf}"
    if extendable:
        cmd += ' extendable'
    if add_route:
        cmd += ' add-route'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not UnConfigure static NAT outside rule")

def configure_crypto_ikev2_NAT_keepalive(device, keepalive_time):
    """ Configure crypto ikev2 nat keepalive <time in sec>
    Args:
        device (`obj`): Device object
        keepalive_time (`int`): keepalive time in secs
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    config_list = []
    config_list.append(f'crypto ikev2 nat keepalive {keepalive_time}')
    # Configure Peer Attributes
    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure Crypto Ikev2 nat keepalive timer. Error: {e}'
        )

def unconfigure_crypto_ikev2_NAT_keepalive(device, keepalive_time):
    """ unConfigure crypto ikev2 nat keepalive <time in secs>
    Args:
        device (`obj`): Device object
        keepalive_time (`int`): keepalive time in secs
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            f'no crypto ikev2 nat keepalive {keepalive_time}'
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not unconfigure Crypto Ikev2 nat keepalive timer. Error: {e}'
        )

def configure_nat_route_map(
    device, 
    route_map_name, 
    permission,
    sequence_number,
    acl_name=None
):
    """ configure NAT route map
        Args:
            device ('obj'): device to execute on
            route_map_name ('str'): route map name
            permission ('str'): permit|deny
            sequence_number ('str'): sequence number
            acl_name ('str'): acl name|acl number
        Return:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("route-map {} {} {}".format(route_map_name, permission, sequence_number))
    
    if acl_name:
        configs.append("match ip address {}".format(acl_name))
        
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not Configure NAT route map")
        
def unconfigure_nat_route_map(
    device, 
    route_map_name, 
    permission,
    sequence_number,
):
    """ unconfigure NAT route map
        Args:
            device ('obj'): device to execute on
            route_map_name ('str'): route map name
            permission ('str'): permit|deny
            sequence_number ('str'): sequence number
        Return:
            None
        Raises:
            SubCommandFailure
    """
    cmd = "no route-map {} {} {}".format(route_map_name, permission, sequence_number)
        
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not UnConfigure NAT route map")
        
def configure_nat_extended_acl(
    device, 
    acl_name, 
    permission=None,
    src_ip=None,
    src_wild_mask=None,
    dest_ip=None,
    dest_wild_mask=None     
):
    """ configure NAT extended acl
        Args:
            device ('obj'): device to execute on
            acl ('str'): acl name
            permission ('str'): permit|deny
            src_ip ('str'): source ip
            src_wild_mask ('str'): source wild mask
            dest_ip('str'): destination ip
            dest_wild_mask('str'): destination wild mask
        Return:
            None
        Raises:
            SubCommandFailure
    """
    configs=[]
    configs.append("ip access-list extended {}".format(acl_name))
    
    if permission:
        configs.append("{} ip {} {} {} {}".format(permission, src_ip, src_wild_mask, dest_ip, dest_wild_mask))
        
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not Configure NAT extended acl")
        
def configure_dynamic_nat_outside_rule(
    device, 
    acl_name, 
    pool_name
):
    """ Configure dynamic NAT outside rule 
        Args:
            device ('obj'): device to use
            acl_name ('str'): acl name
            pool_name ('str'): pool name
        Returns:
            None
        Raises:
            SubCommandFailure: dynamic NAT outside rule not configured
    """
    cmd = ["ip nat outside source list {} pool {} add-route".format(
              acl_name,pool_name)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not Configure dynamic NAT outside rule")
        
def unconfigure_dynamic_nat_outside_rule(
    device, 
    acl_name, 
    pool_name
):
    """ UnConfigure dynamic NAT outside rule 
        Args:
            device ('obj'): device to use
            acl_name ('str'): acl name
            pool_name ('str'): pool name
        Returns:
            None
        Raises:
            SubCommandFailure: dynamic NAT outside rule not unconfigured
    """
    cmd = ["no ip nat outside source list {} pool {} add-route".format(
              acl_name,pool_name)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not UnConfigure dynamic NAT outside rule")
        
def configure_disable_nat_scale(device, nat_aot=True, nat_scale=True):

    """ Configure disable NAT scale
        Args:
            device (`obj`): Device object
            nat_aot ('boolean', optional): Flag to disable nat aot
            nat_scale ('boolean', optional): Flag to disable nat scale
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    
    command = []       
    if nat_aot:
        command.append("ip nat create flow-entries")
    if nat_scale:
        command.append("no nat scale")
    
    try:
        device.configure(command)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure disable NAT scale") 
        
def configure_nat_translation_timeout(
    device, 
    protocol_timeout, 
    timeout_value
):
    """ Configure ip nat translation timeout 
        Args:
            device ('obj'): device to use
            protocol_timeout ('str'): udp-timeout | tcp-timeout | timeout
            timeout_value ('str'): timeout value
        Returns:
            None
        Raises:
            SubCommandFailure: ip nat translation timeout not configured
    """
    cmd = ["ip nat translation {} {}".format(
              protocol_timeout,timeout_value)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not Configure ip nat translation timeout") 
        
def unconfigure_nat_translation_timeout(
    device, 
    protocol_timeout
):
    """ UnConfigure ip nat translation timeout 
        Args:
            device ('obj'): device to use
            protocol_timeout ('str'): udp-timeout | tcp-timeout | timeout
        Returns:
            None
        Raises:
            SubCommandFailure: ip nat translation timeout not unconfigured
    """
    cmd = ["no ip nat translation {}".format(
              protocol_timeout)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not UnConfigure ip nat translation timeout")      

def configure_nat_pool_overload_rule(
    device,
    acl_name,
    pool_name
):
    """ Configure dynamic NAT pool overload rule
        Args:
            device ('obj'): device to use
            acl_name ('str'): Acl name
            pool_name ('str'): Pool name
        Returns:
            None
        Raises:
            SubCommandFailure: dynamic NAT rule not configured
    """
    cmd = ["ip nat inside source list {} pool {} overload".format(
              acl_name, pool_name)]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not Configure ip nat pool overload")   
        
def force_unconfigure_static_nat_route_map_rule(device, inside_local_ip, inside_global_ip, route_map_name, timeout = 60):

    """ Force UnConfigure static NAT route-map rule
        Args:
            device ('obj'): device to use
            inside_local_ip ('str'): Inside local ip
            inside_global_ip ('str'): Inside global ip
            route_map_name ('str') : Name of route-map
            timeout ('int', optional): Max time for force unconfigure static NAT route-map rule.Defaults to 60
        Returns:
            None
        Raises:
            Exception: static NAT route-map rule not force unconfigured
    """
    
    dialog = Dialog([
             Statement(
             pattern=r'.*Static entry in use, do you want to delete child entries\? \[no\].*',
             action='sendline(yes)',
             loop_continue=True,
             continue_timer=False)])
    
    cmd = ["no ip nat inside source static {} {} route-map {}".format(
              inside_local_ip,inside_global_ip,route_map_name)]

    try:
       device.configure(cmd, reply=dialog, timeout=timeout, append_error_pattern=['.*Command cannot be executed.*'])
    except Exception as err:
        log.error("Failed to force unconfigure static NAT route-map rule: {err}".format(err=err))
        raise Exception(err)

def configure_nat64_interface(device, interface):
    """ Configure nat64 on interface 
        Args:
            device ('obj'): device to use
            interface ('str'): interface/vlan/sub-interface
        Returns:
            None
        Raises:
            SubCommandFailure: nat64 enable not configured
    """
    try:
        device.configure(
            [
                "interface {}".format(interface),
                "nat64 enable"           
            ]
        )
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not enable NAT64 on interface")
        
def unconfigure_nat64_interface(device, interface):
    """ Unconfigure nat64 on interface 
        Args:
            device ('obj'): device to use
            interface ('str'): interface/vlan/sub-interface
        Returns:
            None
        Raises:
            SubCommandFailure: nat64 enable not unconfigured
    """
    try:
        device.configure(
            [
                "interface {}".format(interface),
                "no nat64 enable"           
            ]
        )
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure nat64 on interface")
        
def configure_nat64_prefix_stateful(device, prefix, prefix_length, interface = None, vrf_name = None):
    """ Configure nat64 prefix stateful 
        Args:
            device ('obj'): device to use
            interface ('str'): interface
            prefix ('str'): prefix
            prefix_lenght ('str'): prefix length
            vrf_name ('str'): vrf name
        Returns:
            None
        Raises:
            SubCommandFailure: nat64 prefix not configured
    """
    cmd = []
        
    if interface:
        cmd = [
                "interface {}".format(interface),
                "nat64 prefix stateful {}/{}".format(prefix,prefix_length)           
              ]  
    elif vrf_name:
        cmd= f"nat64 prefix stateful {prefix}/{prefix_length} vrf {vrf_name}"
    else:
        cmd = "nat64 prefix stateful {}/{}".format(prefix,prefix_length)
          
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure nat64 prefix stateful")
        
def unconfigure_nat64_prefix_stateful(device, interface=None, prefix=None, prefix_length=None, vrf_name=None):
    """ Unconfigure nat64 prefix stateful 
        Args:
            device ('obj'): device to use
            interface ('str'): interface
            prefix ('str'): prefix
            prefix_lenght ('str'): prefix length
            vrf_name ('str'): vrf name
        Returns:
            None
        Raises:
            SubCommandFailure: nat64 prefix not unconfigured
    """
    cmd = []
    
    if interface:
        cmd = [
                "interface {}".format(interface),
                "no nat64 prefix stateful {}/{}".format(prefix,prefix_length)           
              ] 
    elif vrf_name:
        cmd= f"no nat64 prefix stateful {prefix}/{prefix_length} vrf {vrf_name}"                 
    elif prefix:
        cmd = ["no nat64 prefix stateful {}/{}".format(prefix,prefix_length)]        
    else:
        cmd = ["no nat64 prefix stateful"]
                
    try:
        device.configure(cmd)        
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure nat64 prefix stateful")
        
def configure_nat64_v6v4_static(device, ipv6_address, ipv4_address, vrf_name=None, match_in_vrf=None):
    """ Configure nat64 v6v4 static 
        Args:
            device ('obj'): device to use
            ipv6_address ('str'): ipv6 address
            ipv4_address ('str'): ipv4 address
            vrf_name ('str'): vrf name
            match_in_vrf ('str'): match-in-vrf
        Returns:
            None
        Raises:
            SubCommandFailure: nat64 v6v4 static not configured
    """
    if vrf_name:
        if match_in_vrf:
            cmd= f"nat64 v6v4 static {ipv6_address} {ipv4_address} vrf {vrf_name} {match_in_vrf}" 
        else:
            cmd= f"nat64 v6v4 static {ipv6_address} {ipv4_address} vrf {vrf_name}" 
    else:
        cmd = ["nat64 v6v4 static {} {}".format(ipv6_address,ipv4_address)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure nat64 v6v4 static")
        
def unconfigure_nat64_v6v4_static(device, ipv6_address, ipv4_address, vrf_name=None, match_in_vrf=None):
    """ Unconfigure nat64 v6v4 static 
        Args:
            device ('obj'): device to use
            ipv6_address ('str'): ipv6 address
            ipv4_address ('str'): ipv4 address
            vrf_name ('str'): vrf name
            match_in_vrf ('str'): match-in-vrf
        Returns:
            None
        Raises:
            SubCommandFailure: nat64 v6v4 static not unconfigured
    """
    dialog = Dialog([
             Statement(
             pattern=r'.*Static entry in use, do you want to delete child entries\? \[no\].*',
             action='sendline(yes)',
             loop_continue=True,
             continue_timer=False)])
    if vrf_name:
        if match_in_vrf:
            cmd= f"no nat64 v6v4 static {ipv6_address} {ipv4_address} vrf {vrf_name} {match_in_vrf}" 
        else:
            cmd= f"no nat64 v6v4 static {ipv6_address} {ipv4_address} vrf {vrf_name}" 
    else:
        cmd = ["no nat64 v6v4 static {} {}".format(ipv6_address,ipv4_address)]

    try:
        device.configure(cmd,reply=dialog)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure nat64 v6v4 static")
        
def configure_nat64_v6v4_static_protocol_port(
    device, 
    protocol, 
    ipv6_address,
    ipv6_port, 
    ipv4_address, 
    ipv4_port
):
    """ Configure nat64 v6v4 static protocl 
        Args:
            device ('obj'): device to use
            protocol ('str'): protocol-tcp/udp
            ipv6_address ('str'): ipv6 address
            ipv6_port ('str'): ipv6 port number
            ipv4_address ('str'): ipv4 address
            ipv4_port ('str'): ipv4 port number
        Returns:
            None
        Raises:
            SubCommandFailure: nat64 v6v4 static protocol not configured
    """
    cmd = ["nat64 v6v4 static {} {} {} {} {}".format(protocol,ipv6_address,ipv6_port,ipv4_address,ipv4_port)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure nat64 v6v4 static protocol")

def unconfigure_nat64_v6v4_static_protocol_port(
    device, 
    protocol, 
    ipv6_address, 
    ipv6_port, 
    ipv4_address, 
    ipv4_port
):
    """ Unconfigure nat64 v6v4 static protocl 
        Args:
            device ('obj'): device to use
            protocol ('str'): protocol-tcp/udp
            ipv6_address ('str'): ipv6 address
            ipv6_port ('str'): ipv6 port number
            ipv4_address ('str'): ipv4 address
            ipv4_port ('str'): ipv4 port number
        Returns:
            None
        Raises:
            SubCommandFailure: nat64 v6v4 static protocol not unconfigured
    """
    cmd = ["no nat64 v6v4 static {} {} {} {} {}".format(protocol,ipv6_address,ipv6_port,ipv4_address,ipv4_port)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure nat64 v6v4 static protocol")
        
def configure_nat64_v4_pool(
    device, 
    pool_name, 
    start_ipv4_address, 
    end_ipv4_address
):
    """ Configure nat64 v4 pool 
        Args:
            device ('obj'): device to use
            pool_name ('str'): any pool name
            start_ipv4_address ('str'): ipv4 address
            end_ipv4_address ('str'): ipv4 address
        Returns:
            None
        Raises:
            SubCommandFailure: nat64 v4 pool not configured
    """
    cmd = ["nat64 v4 pool {} {} {}".format(pool_name,start_ipv4_address,end_ipv4_address)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure nat64 v4 pool ")

def unconfigure_nat64_v4_pool(
    device, 
    pool_name, 
    start_ipv4_address, 
    end_ipv4_address
):
    """ Unconfigure nat64 v4 pool 
        Args:
            device ('obj'): device to use
            pool_name ('str'): any pool name
            start_ipv4_address ('str'): ipv4 address
            end_ipv4_address ('str'): ipv4 address
        Returns:
            None
        Raises:
            SubCommandFailure: nat64 v4 pool not unconfigured
    """
    cmd = ["no nat64 v4 pool {} {} {}".format(pool_name,start_ipv4_address,end_ipv4_address)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure nat64 v4 pool ")
        
def configure_nat64_v4_list_pool(
    device, 
    acl_list_number_name, 
    pool_name,
    vrf_name=None,
    match_in_vrf=None
):
    """ Configure nat64 v4 list pool 
        Args:
            device ('obj'): device to use
            acl_list_number_name ('str'): access list number or name
            pool_name ('str'): any pool name
            vrf_name ('str'): vrf name
            match_in_vrf ('str'): match-in-vrf
        Returns:
            None
        Raises:
            SubCommandFailure: nat64 v4 list pool not configured
    """
    if vrf_name:
        if match_in_vrf:
            cmd= f"nat64 v6v4 list {acl_list_number_name} pool {pool_name} vrf {vrf_name} {match_in_vrf}"
        else:
            cmd= f"nat64 v6v4 list {acl_list_number_name} pool {pool_name} vrf {vrf_name}" 
    else:
        cmd = ["nat64 v6v4 list {} pool {}".format(acl_list_number_name,pool_name)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure nat64 v4 list pool ")

def unconfigure_nat_pool_overload_rule(
    device,
    acl_name,
    pool_name
):
    """ UnConfigure dynamic NAT pool overload rule
        Args:
            device ('obj'): device to use
            acl_name ('str'): Acl name
            pool_name ('str'): Pool name
        Returns:
            None
        Raises:
            SubCommandFailure: dynamic NAT rule not unconfigured
    """
    cmd = ["no ip nat inside source list {} pool {} overload".format(
              acl_name, pool_name)]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure nat pool")
        
def unconfigure_nat64_v4_list_pool(
    device, 
    acl_list_number_name, 
    pool_name,
    vrf_name=None,
    match_in_vrf=None
):
    """ Unconfigure nat64 v4 list pool 
        Args:
            device ('obj'): device to use
            acl_list_number_name ('str'): access list number or name
            pool_name ('str'): any pool name
            vrf_name ('str'): vrf name
            match_in_vrf ('str'): match-in-vrf
        Returns:
            None
        Raises:
            SubCommandFailure: nat64 v4 list pool not unconfigured
    """
    if vrf_name:
        if match_in_vrf:
            cmd= f"no nat64 v6v4 list {acl_list_number_name} pool {pool_name} vrf {vrf_name} {match_in_vrf}"
        else:
            cmd= f"no nat64 v6v4 list {acl_list_number_name} pool {pool_name} vrf {vrf_name}"
    else:
        cmd = ["no nat64 v6v4 list {} pool {}".format(acl_list_number_name,pool_name)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure nat64 v4 list pool ")
        
def configure_nat64_v4_list_pool_overload(
    device, 
    acl_list_number_name, 
    pool_name,
    vrf_name=None,
    match_in_vrf=None
):
    """ Configure nat64 v4 list pool overload
        Args:
            device ('obj'): device to use
            acl_list_number_name ('str'): access list number or name
            pool_name ('str'): any pool name
            vrf_name ('str'): vrf name
            match_in_vrf ('str'): match-in-vrf
        Returns:
            None
        Raises:
            SubCommandFailure: nat64 v4 list pool overload not configured
    """
    if vrf_name:
        if match_in_vrf:
            cmd= f"nat64 v6v4 list {acl_list_number_name} pool {pool_name} vrf {vrf_name} overload {match_in_vrf}"
        else:
            cmd= f"nat64 v6v4 list {acl_list_number_name} pool {pool_name} vrf {vrf_name} overload"
    else:
        cmd = ["nat64 v6v4 list {} pool {} overload".format(acl_list_number_name,pool_name)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure nat64 v4 list pool overload")
        
def unconfigure_nat64_v4_list_pool_overload(
    device, 
    acl_list_number_name, 
    pool_name,
    vrf_name=None,
    match_in_vrf=None
):
    """ Unconfigure nat64 v4 list pool overload 
        Args:
            device ('obj'): device to use
            acl_list_number_name ('str'): access list number or name
            pool_name ('str'): any pool name
            vrf_name ('str'): vrf name
            match_in_vrf ('str'): match-in-vrf
        Returns:
            None
        Raises:
            SubCommandFailure: nat64 v4 list pool overload not unconfigured
    """
    if vrf_name:
        if match_in_vrf:
            cmd= f"no nat64 v6v4 list {acl_list_number_name} pool {pool_name} vrf {vrf_name} overload {match_in_vrf}"
        else:
            cmd= f"no nat64 v6v4 list {acl_list_number_name} pool {pool_name} vrf {vrf_name} overload"
    else:
        cmd = ["no nat64 v6v4 list {} pool {} overload".format(acl_list_number_name,pool_name)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure nat64 v4 list pool overload ")
        
def configure_nat64_translation_timeout(
    device, 
    protocol_name, 
    timeout_value
):
    """ Configure nat64 translation timeout 
        Args:
            device ('obj'): device to use
            protocol_name ('str'): protocols tcp,udp,icmp,bind
            timeout_value ('str'): timeout value in seconds
        Returns:
            None
        Raises:
            SubCommandFailure: nat64 translation timeout not configured
    """
    cmd = ["nat64 translation timeout {} {}".format(
              protocol_name,timeout_value)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not Configure nat64 translation timeout")
        
def unconfigure_nat64_translation_timeout(
    device, 
    protocol_name, 
    timeout_value = None
):
    """ Unconfigure nat64 translation timeout 
        Args:
            device ('obj'): device to use
            protocol_name ('str'): protocols tcp,udp,icmp,bind
            timeout_value ('str'): timeout value in seconds
        Returns:
            None
        Raises:
            SubCommandFailure: nat64 translation timeout not unconfigured
    """
    cmd = []
        
    if timeout_value:
        cmd = ["no nat64 translation timeout {} {}".format(
              protocol_name,timeout_value)]
    else:
        cmd = "no nat64 translation timeout {}".format(protocol_name)
    
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure nat64 translation timeout")
        
def configure_nat_ipv6_acl(
    device, 
    acl_name, 
    permission=None, 
    ipv6_address=None, 
    sequence_number=None
):
    """ Configure NAT ipv6 acl
        Args:
            device ('obj'): device to execute on
            acl_name ('str'): acl name
            permission ('str'): permit|deny
            ipv6_address ('str'): IPv6 address
            sequence_number ('str'): Sequence number
        Return:
            None
        Raises:
            SubCommandFailure    
    """
    configs=[]
    configs.append("ipv6 access-list {}".format(acl_name))
    
    if permission:
        configs.append("{} ipv6 {} any sequence {}".format(permission, ipv6_address, sequence_number))
    
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not Configure NAT ipv6 acl")

def configure_nat64_nd_ra_prefix(device, 
    prefix, prefix_length, interface=None,
    sub_interface=None, life_time=None, 
    int1=None, int2=None, 
    start_int=None, end_int=None
):
    """ Configure nat64 nd ra prefix  
        Args:
            device ('obj'): device to use
            prefix ('str'): prefix
            prefix_length ('int'): prefix length
            interface ('str', optional): interface
            sub_interface('str', optional): Subinterface to be added to interface name
            life_time ('int', optional): lifetime
            int1('str', optional): Interface 1
            int2('str', optional): Interface 2
            start_int('str', optional): Starting Interface
            end_int('str', optional): Ending Interface number
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = []
    
    #Configure nd ra prefix on an sub-interface
    if sub_interface:
        interface_name = interface + "." + sub_interface
        cmd = [f"interface {interface_name}\n"]
    #Configure nd ra prefix on an interface
    else:
        if int1 and int2:
            cmd = [f"interface range {int1},{int2}"]
        elif start_int and end_int:
            cmd = [f"interface range {start_int} - {end_int}"]
        else:
            cmd = [f"interface {interface}"]

    if life_time:  
        cmd += [f"ipv6 nd ra nat64-prefix {prefix}/{prefix_length} lifetime {life_time}"]
    else:          
        cmd += [f"ipv6 nd ra nat64-prefix {prefix}/{prefix_length}"]                                    
            
    try:
        device.configure(cmd)        
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure nat64 nd ra prefix")
        
def unconfigure_nat64_nd_ra_prefix(device, 
    prefix, prefix_length, interface=None,
    sub_interface=None, 
    int1=None, int2=None, 
    start_int=None, end_int=None
):
    """ UnConfigure nat64 nd ra prefix  
        Args:
            device ('obj'): device to use
            prefix ('str'): prefix
            prefix_length ('int'): prefix length
            interface ('str', optional): interface
            sub_interface('str', optional): Subinterface to be added to interface name
            int1('str', optional): Interface 1
            int2('str', optional): Interface 2
            start_int('str', optional): Starting Interface
            end_int('str', optional): Ending Interface number
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = []
    
    #UnConfigure nd ra prefix on an sub-interface
    if sub_interface:
        interface_name = interface + "." + sub_interface
        cmd = [f"interface {interface_name}"]
    #UnConfigure nd ra prefix on an interface
    else:
        if int1 and int2:
            cmd = [f"interface range {int1},{int2}"]
        elif start_int and end_int:
            cmd = [f"interface range {start_int} - {end_int}"]
        else:
            cmd = [f"interface {interface}"]

    cmd += [f"no ipv6 nd ra nat64-prefix {prefix}/{prefix_length}"]                                    
            
    try:
        device.configure(cmd)        
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure nat64 nd ra prefix")

def configure_ip_access_group_in_out(
    device,
    interface,
    acl_name,
    acl_direction,
):
    """ Enable ip access_group IN and OUT over interface 
        Args:
            device ('obj'): device to use
            acl_name ('str'): name of the ACL
            acl_direction ('str'): in or out direction of the acl
            interface ('str'): enable ip access_group {aclname}in/out on this interface
        Returns:
            console output
        Raises:
            SubCommandFailure: ip access_group IN OUT not enabled over interface
    """
    cmd = [
                f"interface {interface}",
                f"ip access-group {acl_name} {acl_direction}"           
          ]  

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Enable the ip access-group. Error:\n{error}".format(error=e)
        )

def unconfigure_ip_access_group_in_out(
    device,
    interface,
    acl_name,
    acl_direction,
):
    """ Disable ip access_group IN and OUT over interface 
        Args:
            device ('obj'): device to use
            acl_name ('str'): name of the ACL
            acl_direction ('str'): in or out direction of the acl
            interface ('str'): disable ip access_group {acl_name} in/out over this interface
        Returns:
            console output
        Raises:
            SubCommandFailure: ip access_group IN OUT is enabled over interface
    """
    cmd = [
                f"interface {interface}",
                f"no ip access-group {acl_name} {acl_direction}"
          ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disable the ip access-group. Error:\n{error}".format(error=e)
        )


def unconfigure_outside_static_nat_rule(device, outside_local_address, outside_global_address, l4_protocol = None,
    global_port = None, local_port = None, network=False, network_mask=None, extendable = False, add_route = False):
    """ UnConfigure static NAT rule
        Args:
            device ('obj'): device to use
            outside_local_address ('str'): outside local ip
            outside_global_address ('str'): outside global ip
            l4_protocol ('str', optional): tcp ot udp protocol. Default is None
            global_port ('int', optional): tcp ot udp global port number. Default is None
            local_port ('int', optional): tcp ot udp local port number. Default is None
            network ('bool', optional): configures static netwrok. Default is False
            network_mask ('str', optional): network mask or prefix. Default is None
            extendable ('bool', optional): extend the translation. Default is False
            add_route ('bool', optional): add static route. Default is False
        Returns:
            None
        Raises:
            SubCommandFailure: static NAT rule not unconfigured
    """
    dialog = Dialog([Statement(
        pattern=r'\[no\].*',
        action='sendline(yes)',
        loop_continue=True,
        continue_timer=False
        )])
    cmd = 'no ip nat outside source static'
    if l4_protocol and global_port and local_port:
        cmd += f' {l4_protocol} {outside_global_address} {global_port} {outside_local_address} {local_port}'
    elif network and network_mask:
        cmd += f' network {outside_global_address} {outside_local_address} {network_mask}'
    else:
        cmd += f' {outside_global_address} {outside_local_address}'
    if extendable:
        cmd += ' extendable'
    if add_route:
        cmd += ' add-route'
    try:
        device.configure(cmd, reply=dialog)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not UnConfigure static NAT rule")


def unconfigure_nat_pool_address(device, pool_name, start_ip_address, end_ip_address,
                                 network_mask=None, prefix_length=None, pool_type=None):
    """ Unconfigure NAT pool address
        Args:
            device ('obj'): device to use
            pool_name ('str'): Name of pool
            start_ip_address ('str'): address start ip.
            end_ip_address ('str') : address end ip.
            network_mask ('str', optional) : Network mask. Default is None
            prefix_length ('str', optional) : Network prefix length. Default is None
            pool_type ('str', optional) : pool type. ex: match-host. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure: Could not Unconfigure NAT pool address
    """
    cmd = [f'ip nat pool {pool_name}']
    if network_mask:
        cmd[0] += f' netmask {network_mask}'
        cmd.append(f'no address {start_ip_address} {end_ip_address}')
    elif prefix_length:
        cmd[0] += f' prefix-length {prefix_length}'
        cmd.append(f'no address {start_ip_address} {end_ip_address}')
    if pool_type:
        cmd[0] += f' type {pool_type}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not Unconfigure NAT pool address")


def configure_static_nat_route_map_no_alias_rule(device, translation, local_ip, global_ip, add_route=False):
    """ Configure static NAT route-map rule
        Args:
            device ('obj'): device to use
            translation ('str'): inside or outside translation
            local_ip ('str'): inside/outside local ip
            global_ip ('str'): inside/outside global ip
            add_route ('bool', optional) : Add outside route-map. Default is False
        Returns:
            None
        Raises:
            SubCommandFailure: static NAT route-map rule not configured
    """
    config = []
    if translation == 'inside':
        config.append(f"ip nat {translation} source static {local_ip} {global_ip} no-alias")
    elif translation == 'outside':
        config.append(f"ip nat {translation} source static {global_ip} {local_ip} no-alias{' add-route' if add_route else ''}")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not Configure static NAT route-map rule")


def unconfigure_static_nat_route_map_no_alias_rule(device, translation, local_ip, global_ip, add_route=False):
    """ Unconfigure static NAT route-map rule
        Args:
            device ('obj'): device to use
            translation ('str'): inside or outside translation
            local_ip ('str'): inside/outside local ip
            global_ip ('str'): inside/outside global ip
            add_route ('bool', optional) : Add outside route-map. Default is False
        Returns:
            None
        Raises:
            SubCommandFailure: static NAT route-map rule not configured
    """
    config = []
    if translation == 'inside':
        config.append(f"no ip nat {translation} source static {local_ip} {global_ip} no-alias")
    elif translation == 'outside':
        config.append(f"no ip nat {translation} source static {global_ip} {local_ip} no-alias{' add-route' if add_route else ''}")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not Unconfigure static NAT route-map rule")


def configure_nat_translation_max_entries(device, entry_type, entry_name='', number_of_entries=''):
    """ Configure ip nat translation max-entries 
        Args:
            device ('obj'): device to use
            entry_type ('str'): entry type. For ex: vrf, list, host
            entry_name ('str', optional): entry name if entry type is host/vrf/list. Default is ''
            number_of_entries ('int', optional): number of entries. Default is ''
        Returns:
            None
        Raises:
            SubCommandFailure: ip nat translation max-entries not configured
    """
    cmd = f"ip nat translation max-entries {entry_type} {entry_name} {number_of_entries}"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not Configure ip nat translation max-entries. Error:{e}")


def configure_static_nat_source_list_rule(device, translation, list_name, pool_name=None, 
            interface=None, vrf_name=None, overload=None, egress_interface=None, oer=None):
    """ Configure static NAT source list rule
        Args:
            device ('obj'): device to use
            translation ('str'): inside or outside translation
            list_name ('str'): Access list name or number
            pool_name ('str', optional): Name pool of global addresses. Default is None
            interface ('bool', optional) : Specify interface for global address. Default is None
            vrf_name ('str', optional): Specify vrf. Default is None
            overload ('str', optional): Overload an address translation. Default is None
            egress_interface ('str', optional): Specify egress interface for translated traffic. Default is None
            oer ('str', optional): Use with vtemplate only. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure: static NAT source list rule not configured
    """
    cmd = f'ip nat {translation} source list {list_name}'
    if pool_name:
        cmd += f' pool {pool_name}'
    elif interface:
        cmd += f' interface {interface}'
    if vrf_name:
        cmd += f' vrf {vrf_name}'
    elif egress_interface:
        cmd += f' egress-interface {egress_interface}'
    if oer:
        cmd += f' oer'
    if overload is not None:
        cmd += f' overload{f" {overload}" if overload else ""}'
        if overload == 'egress-interface':
            cmd += f' {egress_interface}'

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not Configure static NAT source list rule. Error:{e}")


def unconfigure_nat_translation_max_entries(device, entry_type, entry_name='', number_of_entries=''):
    """ Unconfigure ip nat translation max-entries 
        Args:
            device ('obj'): device to use
            entry_type ('str'): entry type. For ex: vrf, list, host
            entry_name ('str', optional): entry name if entry type is host/vrf/list. Default is ''
            number_of_entries ('int', optional): number of entries. Default is ''
        Returns:
            None
        Raises:
            SubCommandFailure: ip nat translation max-entries not configured
    """
    cmd = f"no ip nat translation max-entries {entry_type} {entry_name} {number_of_entries}"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not Unconfigure ip nat translation max-entries. Error:{e}")


def unconfigure_static_nat_source_list_rule(device, translation, list_name, pool_name=None, 
            interface=None, vrf_name=None, overload=None, egress_interface=None, oer=None):
    """ Unconfigure static NAT source list rule
        Args:
            device ('obj'): device to use
            translation ('str'): inside or outside translation
            list_name ('str'): Access list name or number
            pool_name ('str', optional): Name pool of global addresses. Default is None
            interface ('bool', optional) : Specify interface for global address. Default is None
            vrf_name ('str', optional): Specify vrf. Default is None
            overload ('str', optional): Overload an address translation. Default is None
            egress_interface ('str', optional): Specify egress interface for translated traffic. Default is None
            oer ('str', optional): Use with vtemplate only. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure: static NAT source list rule not configured
    """
    cmd = f'no ip nat {translation} source list {list_name}'
    if pool_name:
        cmd += f' pool {pool_name}'
    elif interface:
        cmd += f' interface {interface}'
    if vrf_name:
        cmd += f' vrf {vrf_name}'
    elif egress_interface:
        cmd += f' egress-interface {egress_interface}'
    if oer:
        cmd += f' oer'
    if overload is not None:
        cmd += f' overload{f" {overload}" if overload else ""}'
        if overload == 'egress-interface':
            cmd += f' {egress_interface}'

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not Unconfigure static NAT source list rule. Error:{e}")


def configure_nat64_mapt_domain(device, domain_num, dmr, bmr,
                                bmr_ip, share_ratio, start_port=None,
                                pset_id=None, local_ip=None):
    """ Configure mapt domain on device
        Args:
            device ('obj'): device object
            domain_num ('str'): mapt domain num
            dmr ('str'): dmr ipv6 prefix
            bmr ('str'): bmr ipv6 prefix
            bmr_ip ('str'): bmr ipv4 prefix
            share_ratio ('str'): share ratio
            start_port ('str', optional): start port. Default value is None
            pset_id ('str', optional): pset id, default value is None
            local_ip ('str', optional): local ip prefix, default value is None
        Returns:
            config
        Raises:
            SubCommandFailure: Failed to configure mapt domain
    """

    config = [f'nat64 map-t domain {domain_num}',
              f'default-mapping-rule {dmr}',
              'basic-mapping-rule',
              f'ipv6-prefix {bmr}',
              f'ipv4-prefix {bmr_ip}']
    cmd = f'port-parameters share-ratio {share_ratio}'\
        f'{f" start-port {start_port}" if start_port else ""}'
    config.append(cmd)
    if pset_id:
        cmd = f'port-set-id {pset_id}'
        config.append(cmd)
    if local_ip:
        cmd = f'local-ipv4-prefix {local_ip}'
        config.append(cmd)
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to config mapt domain. Error:\n{e}")


def unconfigure_nat64_mapt_domain(device, domain_num):
    """ UnConfigure mapt domain on device
        Args:
            device ('obj'): device object
            domain_num ('str'): mapt domain num
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure map-t domain
    """
    try:
        device.configure(f'no nat64 map-t domain {domain_num}')
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfig mapt domain. Error:\n{e}")


def configure_nat64_route(device, ip, interface, vrf=None, enable=True):
    """ Configure nat64 route on device
        Args:
            device ('obj'): device object
            ip ('str'): ipv4 prefix
            interface ('str'): output interface
            vrf ('str', optional): vrf name. Default value is None
            enable (boolean, optional): configure or unconfigure
        Returns:
            config
        Raises:
            SubCommandFailure: Failed to configure nat64 route
    """
    if enable:
        cmd = ''
    else:
        cmd = 'no '
    cmd += f'nat64 route'\
        f'{f" vrf {vrf}" if vrf else ""}'\
        f'  {ip} {interface}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to config nat64 route. Error:\n{e}")


def configure_nat64_mapt_ce(device, enable=True):
    """ Enables nat64 mapt ce on device
        Args:
            device ('obj'): Device object
            enable (boolean): configure or unconfigure
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if enable:
        config = ''
    else:
        config = 'no '
    config += "nat64 settings map-t ce"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure nat64 mapt ce on "
            "device. Error:\n{e}".format(e=e)
        )


def configure_nat_service_all_algs(device, enable=True):
    """ Enable or disable all algs on device
        Args:
            device ('obj'): Device object
            enable (boolean): configure or unconfigure
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if enable:
        config = ''
    else:
        config = 'no '
    config += "ip nat service all-algs"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure nat service all-algs on "
            "device. Error:\n{e}".format(e=e)
        )


def configure_nat_setting_gatekeeper_size(device, size, enable=True):
    """ Enable or disable gate keeper size on device
        Args:
            device ('obj'): Device object
            size ('str'): gate keeper size
            enable (boolean): configure or unconfigure
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if enable:
        config = ''
    else:
        config = 'no '
    config += f'ip nat settings gatekeeper-size {size}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure nat gatekeeper size on "
            "device. Error:\n{e}".format(e=e)
        )
