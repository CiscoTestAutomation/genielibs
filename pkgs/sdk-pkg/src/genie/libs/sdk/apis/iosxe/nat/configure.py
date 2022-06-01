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
):
    """ Configure interface overloaad rule
        Args:
            device ('obj'): device to use
            interface ('str'): Interface which will use for overlad rule
            access_list_name ('str'): Name of extended access list
        Returns:
            console output
        Raises:
            SubCommandFailure: Nat overload rule not connfigured
    """
    cmd = ["ip nat inside source list {} interface {} overload".format(access_list_name,interface)]

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

def configure_nat_pool(
    device, 
    pool_name, 
    pool_start_ip,
    pool_end_ip,
    network_mask
):
    """ Configure NAT pool
        Args:
            device ('obj'): device to use
            pool_name ('str'): Name of pool
            pool_start_ip ('str'): Pool start ip
            pool_end_ip ('str') : Pool end ip
            network_mask ('str') : Network mask
        Returns:
            None
        Raises:
            SubCommandFailure: NAT pool not configured
    """
    cmd = ["ip nat pool {} {} {} netmask {}".format(
              pool_name,pool_start_ip,pool_end_ip,network_mask)]

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
    network_mask
):
    """ UnConfigure NAT pool 
        Args:
            device ('obj'): device to use
            pool_name ('str'): Name of pool
            pool_start_ip ('str'): Pool start ip
            pool_end_ip ('str') : Pool end ip
            network_mask ('str') : Network mask
        Returns:
            None
        Raises:
            SubCommandFailure: NAT pool not unconfigured
    """
    cmd = ["no ip nat pool {} {} {} netmask {}".format(
              pool_name,pool_start_ip,pool_end_ip,network_mask)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not UnConfigure NAT pool")
    
def configure_static_nat_route_map_rule(
    device, 
    inside_local_ip, 
    inside_global_ip,
    route_map_name
):
    """ Configure static NAT route-map rule
        Args:
            device ('obj'): device to use
            inside_local_ip ('str'): Inside local ip
            inside_global_ip ('str'): Inside global ip
            route_map_name ('str') : Name of route-map
        Returns:
            None
        Raises:
            SubCommandFailure: static NAT route-map rule not configured
    """
    cmd = ["ip nat inside source static {} {} route-map {}".format(
              inside_local_ip,inside_global_ip,route_map_name)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not Configure static NAT route-map rule")
 
def unconfigure_static_nat_route_map_rule(
    device, 
    inside_local_ip, 
    inside_global_ip,
    route_map_name
):
    """ UnConfigure static NAT route-map rule
        Args:
            device ('obj'): device to use
            inside_local_ip ('str'): Inside local ip
            inside_global_ip ('str'): Inside global ip
            route_map_name ('str') : Name of route-map
        Returns:
            None
        Raises:
            SubCommandFailure: static NAT route-map rule not unconfigured
    """
    cmd = ["no ip nat inside source static {} {} route-map {}".format(
              inside_local_ip,inside_global_ip,route_map_name)]

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
        
def configure_enable_nat_scale(device, timeout=60):

    """ Configure enable NAT scale
        Args:
            device (`obj`): Device object
            timeout ('int', optional): Max time for enable nat scale.Defaults to 60
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
    
    command = [ "no ip nat create flow-entries",
                "nat scale"]

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
        
def configure_static_nat_rule(
    device, 
    inside_local_ip, 
    inside_global_ip,
    l4_protocol = None,
    inside_port = None,
    outside_port = None,
    extendable = False
):
    """ Configure static NAT rule
        Args:
            device ('obj'): device to use
            inside_local_ip ('str'): inside local ip
            inside_global_ip ('str'): inside global ip
        Returns:
            None
        Raises:
            SubCommandFailure: static NAT rule not configured
    """
    cmd = ["ip nat inside source static {} {}".format(
              inside_local_ip,inside_global_ip)]
    if l4_protocol:
        cmd = "ip nat inside source static {} {} {} {} {}".format(
            l4_protocol,inside_local_ip,inside_port,inside_global_ip,outside_port)
        if extendable:
            cmd = cmd + ' extendable'

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not Configure static NAT rule")
        
def unconfigure_static_nat_rule(
    device, 
    inside_local_ip, 
    inside_global_ip,
    l4_protocol = None,
    inside_port = None,
    outside_port = None,
    extendable = False
):
    """ UnConfigure static NAT rule
        Args:
            device ('obj'): device to use
            inside_local_ip ('str'): inside local ip
            inside_global_ip ('str'): inside global ip
        Returns:
            None
        Raises:
            SubCommandFailure: static NAT rule not unconfigured
    """
    dialog = Dialog([Statement(pattern=r'\[no\].*', action='sendline(yes)',loop_continue=True,continue_timer=False)])
    cmd = ["no ip nat inside source static {} {}".format(
              inside_local_ip,inside_global_ip)]
    if l4_protocol:
        cmd = "no ip nat inside source static {} {} {} {} {}".format(
            l4_protocol,inside_local_ip,inside_port,inside_global_ip,outside_port)
        if extendable:
            cmd = cmd + ' extendable'

    try:
        device.configure(cmd,reply=dialog)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not UnConfigure static NAT rule")
        
def configure_static_nat_outside_rule(
    device, 
    outside_global_address, 
    outside_local_address
):
    """ Configure static NAT outside rule 
        Args:
            device ('obj'): device to use
            outside_global_address ('str'): outside global address
            outside_local_address ('str'): outside local address
        Returns:
            None
        Raises:
            SubCommandFailure: static NAT outside rule not configured
    """
    cmd = ["ip nat outside source static {} {} add-route".format(
              outside_global_address,outside_local_address)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not Configure static NAT outside rule")
        
def unconfigure_static_nat_outside_rule(
    device, 
    outside_global_address, 
    outside_local_address
):
    """ UnConfigure static NAT outside rule 
        Args:
            device ('obj'): device to use
            outside_global_address ('str'): outside global address
            outside_local_address ('str'): outside local address
        Returns:
            None
        Raises:
            SubCommandFailure: static NAT outside rule not unconfigured
    """
    cmd = ["no ip nat outside source static {} {} add-route".format(
              outside_global_address,outside_local_address)]

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
        
def configure_disable_nat_scale(device):

    """ Configure disable NAT scale
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    
    try:
        device.configure(
            [
                "ip nat create flow-entries",
                "no nat scale"           
            ]
        )
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
