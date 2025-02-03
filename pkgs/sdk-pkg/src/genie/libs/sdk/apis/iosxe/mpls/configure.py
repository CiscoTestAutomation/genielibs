"""Common configure functions for mpls"""

# Python
import logging
from unicon.eal.dialogs import Statement, Dialog

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def config_mpls_ldp_on_interface(device, interface):
    """ Config ldp on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    log.info("Configuring ldp on {interface} on {device}"\
        .format(interface=interface, device=device.name))

    try:
        device.configure(["interface {interface}"\
              .format(interface=interface), "mpls ip"])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not activate "mpls ip" on interface {interface}'.format(
                interface=interface
            )
        )
       
def clear_mpls_counters(device):
    """ Config ldp on Device

        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    log.info("clear mpls counters on {device}".format(device=device.name))

    try:
        device.execute("clear mpls counters")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not clear mpls counters on {device}, Error: {error}'.format(
                device=device.name, error=e
            )
        )       

def config_mpls_ldp_on_device(device):
    """ Config ldp on Device

        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    log.info("Configuring ldp on {device}".format(device=device.name))

    try:
        device.configure("mpls ip")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not activate "mpls ip" on {device}, Error: {error}'.format(
                device=device.name, error=e
            )
        )

def remove_mpls_ldp_from_device(device):
    """ Remove ldp from device

        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring device
    """
    try:
        log.info('Removing mpls ldp from device {device}'.format(
            device=device.name))
        device.configure("no mpls ip")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not remove "mpls ip" from {device}, Error: {error}'.format(
                device=device.name, error=e
            )
        )

def remove_mpls_ldp_from_interface(device, interface):
    """ Remove ldp on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    log.info("Removing ldp on {interface} on {device}".format(
        interface=interface, device=device.name))

    try:
        device.configure(["interface {interface}"\
              .format(interface=interface), "no mpls ip"])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not remove "mpls ip" from interface {interface}, '
            'Error: {error}'.format(interface=interface, error=e
            )
        )
        
def remove_mpls_ldp_router_id_from_device(device, interface):
    """ Remove mpls ldp router id from device

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    log.info("Removing mpls ldp router id from device {device}".format(
            device=device.name))

    try:
        device.configure("no mpls ldp router-id {intf}".format(
            intf=interface))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not remove "mpls ldp router-id" from interface {intf} '
            'on device {device}, Error: {error}'.format(
                device=device.name, intf=interface, error=e)
        )


def configure_mpls_label_mode(device, mode):

    """ configure vpn label allocation mode.
        Args:
            device (`obj`): Device object
            mode (`str`): mode used to allocate a VPN label
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:          
        if mode == "per-vrf":
            device.config("mpls label mode ALL-vrfs protocol all-afs per-vrf")
        else:
            device.config("mpls label mode all-vrfs protocol all-afs "
                          "per-prefix")		   
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring label allocation mode {mode}."
            "Error:\n{error}".format(
                mode=mode, error=e
            )
        )


def config_no_keepalive_intf(device, interface, keepalive_period=None, no_switchport=True):
    """ configure no switchport and no keepalive on Interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface on which the edge trunk config to be applied
            keepalive_period('int', optional): <0-32767>  Keepalive period (default 10 seconds)
            no_switchport ('bool'): no switchport. Default is True
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f'interface {interface}']
    if no_switchport:
        cmd.append('no switchport')
    if keepalive_period:
        cmd.append(f'no keepalive {keepalive_period}')
    else:
        cmd.append(f'no keepalive')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure('Could not configure no keepalive intf, Error:\n{e}')

        
def config_xconnect_on_interface(device, interface, neighbor, vcid):
    """ configure xconnect neighbor on Interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface on which the edge trunk config to be applied
            neighbor (`str`): Neighbor to be configured on xconnect
            vcid (`str`): Vcid to be configured through xconnect
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "xconnect {neighbor} {vcid} encapsulation mpls".format(
                                        neighbor=neighbor, vcid=vcid)
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't configure xconnect neighbor on interface {interface}."
            "Error:\n{error}".format(interface=interface, error=e)
        )

def clear_mpls_counters(device):
    """ Clear mpls counters
        Args:
            device (`obj`): Device object

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.info(
        "Clearing counters on {device}".format(device=device)
    )

    dialog = Dialog(
        [Statement(pattern=r'\[confirm\].*', action='sendline(\r)', 
                   loop_continue=True, continue_timer=False)])

    try:
        device.execute("clear mpls counters", reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear mpls counters on {device}. Error:\n{error}".format(
                device=device, error=e
            )
        )


def clear_mpls_ldp_neighbor(device, neighbor_ip):
    """ clear mpls ldp neighbor {}
        Args:
            device ('obj'): Device object
            neighbor_ip ('str'): neighbor ip

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "clear mpls ldp neighbor on {device}".format(device=device))

    try:
        device.execute("clear mpls ldp neighbor {neighbor_ip}"\
              .format(neighbor_ip=neighbor_ip))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear mpls ldp neighbor on {device}. Error:\n{error}"\
                .format(device=device, error=e)
        )

def unconfig_xconnect_on_interface(device, interface, neighbor, vcid):
    """ unconfigure xconnect neighbor on Interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface on which the edge trunk config to be applied
            neighbor (`str`): Neighbor to be configured on xconnect
            vcid (`str`): Vcid to be configured through xconnect
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "no xconnect {neighbor} {vcid} encapsulation mpls".format(
                                        neighbor=neighbor, vcid=vcid)
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't unconfigure xconnect neighbor on interface {interface}."
            "Error:\n{error}".format(interface=interface, error=e)
        )

def config_mpls_lable_protocol(device, interface=None):
    """ Config mpls lable protocol on interface or device

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to be configured
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """

    try:
        if interface is not None:
            log.info(
                    'Configuring mpls label protocol ldp on '
                    'interface {interface}'.format(interface=interface))
            device.configure(["interface {interface}".format(
                interface=interface), "mpls label protocol ldp"])
        else:
            log.info('Configuring mpls label protocol ldp on '
                    'device {device}'.format(device=device.name))
            device.configure("mpls label protocol ldp")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not activate "mpls label protocol ldp", '
            'Error: {error}'.format(error=e)
        )


def remove_mpls_lable_protocol_from_device(device):
    """ Remove mpls label protocol from device

        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    log.info("Removing mpls label protocol ldp "
            "from device {device}".format(device=device.name))

    try:
        device.configure("no mpls label protocol ldp")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not remove "mpls label protocol ldp" from device {device}, '
            'Error: {error}'.format(device=device.name, error=e)
        )


def config_mpls_ldp_router_id_on_device(device, interface, force=False):
    """ Config mpls ldp router id on device

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            force ('bool') : router-id is instantly changed when the interface is down if true
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """

    log.info("Configuring mpls ldp router id on interface {intf} "
            "on device {device}".format(intf=interface, device=device.name))

    config = "mpls ldp router-id {intf}".format(intf=interface)
    if force:
        config += " force"

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not activate "mpls ldp router-id" on interface {intf} '
            'on device {device}, Error: {error}'.format(
                intf=interface, device=device.name, error=e)
        )

def configure_mpls_te_on_interface(device, interface):
    """ configure mple te on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "mpls traffic-eng tunnels",
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure te config on interface {interface}."
            "Error:\n{error}".format(
                interface=interface, error=e
            )
        )

def configure_mpls_te_under_ospf(device, router_id, processid, area):

    """configure mpls te under ospf

        Args:
            device (`obj`): Device object
            processid (`str`): process id of ospf
            router_id ('str'): Router Id
            area ('str'): ospf area
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                "router ospf {processid}".format(processid=processid),
                "mpls traffic-eng router-id {router_id}".format(
                    router_id=router_id),
                "mpls traffic-eng area {area}".format(area=area)
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure TE under ospf protocol.Error: {error}".format(
                            Error=e)
        )

def unconfigure_mpls_te_under_ospf(device, processid, area):

    """unconfigure MPLS TE under ospf

        Args:
            device (`obj`): Device object
            processid ('str'): Process Id
            area ('str'): ospf area
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                "router ospf {processid}".format(processid=processid),
                "no mpls traffic-eng area {area}".format(area=area)
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not remove TE under ospf {processid}. Error: {error}".format(
                            processid=processid, Error=e)
        )

def configure_mpls_te_globally(device):

    """configure mpls te on device

        Args:
            device (`obj`): Device object   
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            "mpls traffic-eng tunnels"
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mpls te on device. Error: {error} ".format(
                                    error=e)
        )

def configure_ip_rsvp_bandwidth(device, interface, bandwidth=""):
    """ configure ip rsvp bandiwth on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            bandwidth ('str'): rsvp bandwidth
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    try:
        device.configure([ "interface {interface}".format(interface=interface),
            "ip rsvp bandwidth {bandwidth}".format(bandwidth=bandwidth)]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure rsvp bandwidth on {interface}."
            "Error:\n{error}".format(interface=interface, error=e)
        )

def config_mpls_ldp_explicit_on_device(device):
    """ Config mpls ldp explicit on device

        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    log.info("Configuring mpls ldp explicit on device {device}".format(
            device=device.name))

    try:
        device.configure("mpls ldp explicit-null")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not activate "mpls ldp explicit-null" '
            'on device {device}, Error: {error}'.format(
                device=device.name, error=e)
        )

def remove_mpls_ldp_explicit_from_device(device):
    """ Remove mpls ldp explicit from device

        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    log.info("Removing mpls ldp explicit from device {device}".format(
            device=device.name))

    try:
        device.configure("no mpls ldp explicit-null")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not remove "mpls ldp explicit-null" '
            'from device {device}, Error: {error}'.format(
                device=device.name, error=e)
        )


def config_speed_nonego_on_interface(device, interface):
    """ Configure speed nonego on interface

        Args:
            device (`obj`): Device object
            interface ('str'): Interface to be configured
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    log.info("Configuring speed nonego on interface {interface}".format(
            interface=interface))

    try:
        device.configure(["interface {interface}".format(
            interface=interface), "speed nonego"])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not activate "speed nonego" on '
            'interface {interface}, Error: {error}'.format(
                interface=interface, error=e)
        )


def config_encapsulation_on_interface(device, vlan, interface):
    """ Configure encapsulation on Interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface on which the edge trunk config to be applied
            vlan  (`str`): Vlan to be configured with encapsulation

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "encapsulation dot1Q {vlan}".format(vlan=vlan),
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't configure encapsulation on interface {interface}. "
            "Error:\n{error}".format(interface=interface, error=e)
        )

        
def configure_explicit_path(device, path_name, path, path_type=None):

    """ configure te explicit path

        Args:
            device (`obj`): Device object
            path_name (`str`): Name of the path
            path (`list`): list of ip address to destination
            path_type (`str`): Mention the path type
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    config = [f"ip explicit-path name {path_name} enable"]
         
    if path_type == "strict":
        for path_num,ip in enumerate(path):
            path_num=path_num+1
            config.append(f"index {path_num} next-address strict {ip}".format(
                                        path_num=path_num, ip=ip))          
    elif path_type == "loose":
        for path_num,ip in enumerate(path):
            path_num=path_num+1
            config.append(f"index {path_num} next-address loose {ip}".format(
                                        path_num=path_num ,ip=ip))
    elif path_type == "exclude_address":
        for ip in path:
            config.append(f"exclude-address {ip}".format(ip=ip))
    else:
        for path_num,ip in enumerate(path):
            path_num=path_num+1
            config.append(f"index {path_num} next-address {ip}".format(
                                        path_num=path_num, ip=ip))
    try:                
        device.config(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring explicit path {path}. Error:\n{error}"\
                .format(path=path, error=e)
        )


def config_xconnect_on_interface(device, interface, neighbor, vcid):
    """ configure xconnect neighbor on Interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface on which the edge trunk config to be applied
            neighbor (`str`): Neighbor to be configured on xconnect
            vcid (`str`): Vcid to be configured through xconnect
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "xconnect {neighbor} {vcid} encapsulation mpls".format(
                                        neighbor=neighbor, vcid=vcid)
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't configure xconnect neighbor on interface {interface}."
            "Error:\n{error}".format(interface=interface, error=e)
        )

        
def config_pseudowire_class(device, pw_class, interface):
    """ configure pseudowire class

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name/ip address
            pw_class ('str'): pseudowire class name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            ["pseudowire-class {pw_class}".format(pw_class=pw_class),
            "encapsulation mpls",
            "preferred-path interface {interface}".format(interface=interface)]
        )

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure pseudowire class {pw_class}. Error:\n{error}"\
                .format(pw_class=pw_class, error=e)
        ) 
        
def unconfig_pseudowire_class(device, pw_class):
    """ unconfigure pseudowire class

        Args:
            device (`obj`): Device object
            pw_class ('str'): pseudowire class name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("no pseudowire-class {pw_class}".format(
            pw_class=pw_class))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed at unconfiguring pseudowire class {pw_class}. "
            "Error:\n{error}".format(pw_class=pw_class, error=e)
        )  
        
def config_pw_class_interface(device, interface, peer_id, vc_id, pw_class):
    """ configure pseudowire class on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            peer_id (`str`): peer address
            vc_id (`str`): vc id 
            pw_class  (`str`): pseudowire class name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure([
            "interface {interface}".format(interface=interface),
            "xconnect {peer_id} {vc_id} encapsulation mpls pw-class {pw_class}"
            .format(peer_id=peer_id, vc_id=vc_id, pw_class=pw_class)]
        )

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure pseudowire class {pw_class} on interface "
            "{interface}.Error:\n{error}".format(
                pw_class=pw_class,interface=interface, error=e
            )
        )  
        
def configure_explicit_path_in_tunnel(device, tunnel, path_name,
                                    path_option, attribute_name=None,
                                    lockdown=False):
    """ configure explicit path in tunnel

        Args:
            device (`obj`): Device object
            tunnel (`str`): Tunnel name
            path_name (`str`): Name of the explicit path
            path_option (`str`): Mention the path option
            attribute_name (`str`): Attribute name to be set
            lockdown(`Boolean`): set the lockdown if true
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        config_list=["interface {tunnel}\n".format(tunnel=tunnel)]
        config_list.append(
            "tunnel mpls traffic-eng path-option {path_option} explicit name "
            "{path_name}".format(path_option=path_option, path_name=path_name))
        if attribute_name:
            config_list.append("attributes {attribute_name}".format(
                attribute_name=attribute_name))
        if lockdown:
            config_list.append("lockdown")
        device.configure(" ".join(config_list))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure explicit path {path_name} for {tunnel}. "
            "Error:\n{error}".format(path_name=path_name, 
                                     tunnel=tunnel, error=e)
        )  
        

def configure_service_internal(device):
    """ Configures service internal on device"""

    try:
        device.configure("service internal")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't configure service internal on device. "
            "Error:\n{error}".format(error=e)
        )

def configure_mpls_ldp_nsr(device):
    """ Configures mpls ldp nsr on device
        Args:
            device (`obj`): Device object

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure("mpls ldp nsr")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't configure mpls ldp nsr on device. "
            "Error:\n{error}".format(error=e)
        )

def configure_dynamic_path_in_tunnel(device, tunnel,
                                    path_option, attribute_name=None,
                                    lockdown=False):
    """configure dynamic path in tunnel

        Args:
            device (`obj`): Device object
            tunnel (`str`): Tunnel name
            path_option (`str`): Mention the path option
            attribute_name (`str`): Attribute name to be set
            lockdown(`Boolean`): set the lockdown if true
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        config_list=["interface {tunnel}\n".format(tunnel=tunnel)]
        config_list.append(
            "tunnel mpls traffic-eng path-option {path_option} dynamic".format(
                path_option=path_option))
        if attribute_name:
            config_list.append("attributes {attribute_name}".format(
                attribute_name=attribute_name))
        if lockdown:
            config_list.append(f"lockdown")
        device.configure(" ".join(config_list))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not dynamic path for {tunnel}. Error:\n{error}".format(
                tunnel=tunnel, error=e
            )
        ) 

def unconfigure_mpls_ldp_nsr(device):
    """ Unconfigures mpls ldp nsr on device
        Args:
            device (`obj`): Device object

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        device.configure("no mpls ldp nsr")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't unconfigure mpls ldp nsr on device. "
            "Error:\n{error}".format(error=e)
        )    
        
def configure_tunnel_bandwidth(device, tunnel_name, bandwidth, class_type=0):
    """configure  tunnel bandwidth
        Args:
	    device (`obj`): Device object
	    tunnel_name (`str`): Tunnel Name
	    bandwidth (`int`) : Tunnel bandwidth
            class_type (`int`) : Default value 0
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    
    config="interface {tunnel_name}\n".format(tunnel_name=tunnel_name)
    config+="tunnel mpls traffic-eng bandwidth {bandwidth}".format(
        bandwidth=bandwidth)
    if class_type:
        config+="tunnel mpls traffic-eng bandwidth {bandwidth} class-type "\
                "{class_type}".format(bandwidth=bandwidth, 
                                      class_type=class_type)
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure bandwidth to the tunnel {tunnel_name}."
            "Error: {error}".format(tunnel_name=tunnel_name, error=e)
        )
        
def configure_tunnel_priority(device, tunnel_name, priority, hold_priority):
    """configure tunnel priority
        Args:
	    device (`obj`): Device object
	    tunnel_name (`str`): Tunnel Name
            priority(`int`): tunnel priority
            hold_priority(`int`): hold priority for tunnel
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure([
            "interface {tunnel_name}".format(tunnel_name=tunnel_name),
            "tunnel mpls traffic-eng priority {priority} {hold_priority}"\
            .format(priority=priority, hold_priority=hold_priority)])  
    except SubCommandFailure as e:
        raise SubCommandFailure(
           "Failed to configure tunnel priority for {tunnel_name}"
           "Error. {error}".format(tunnel_name=tunnel_name, error=e)
        )
        
def unconfigure_tunnel_auto_route(device, tunnel_name, autoroute_type):
    """unconfigure autoroute announce in tunnel.
        Args: 
	    device (`obj`): Device object
	    tunnel_name (`str`): Tunnel Name
            autoroute_type (`str`): autoroute type used for tunnel
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure(["interface {tunnel_name}".\
                                format(tunnel_name=tunnel_name),
                        "no tunnel mpls traffic-eng autoroute {autoroute_type}"\
                                .format(autoroute_type=autoroute_type)]) 
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure autoroute {autoroute_type} for "
            "tunnel {tunnel_name}. Error : {error}".format(
                tunnel_name=tunnel_name, error=e)
        )
        
def configure_tunnel_auto_route(device, tunnel_name, autoroute_type):
    """configure autoroute announce in tunnel.
        Args: 
	    device (`obj`): Device object
	    tunnel_name (`str`): Tunnel Name
            autoroute_type (`str`): autoroute type used for tunnel
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure(["interface {tunnel_name}".\
                                format(tunnel_name=tunnel_name),
                        "tunnel mpls traffic-eng autoroute {autoroute_type}"\
                                .format(autoroute_type=autoroute_type)]) 
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure autoroute {autoroute_type} for "
            "tunnel {tunnel_name}. Error : {error}".format(
                tunnel_name=tunnel_name, error=e)
        )
        
def configure_tunnel_destination(device, tunnel_name, dst_ip):
    """creates tunnel destination.
        Args:
	    device (`obj`): Device object
	    tunnel_name (`str`): Tunnel Name
            dst_ip (`str`): Ip address of tunnel destination 
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure(["interface {tunnel_name}".\
                                format(tunnel_name=tunnel_name),
                        "tunnel destination {dst_ip}".format(dst_ip=dst_ip)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure tunnel destination {dst_ip}"
            "for tunnel {tunnel_name}. Error: {error}".format\
                                (dst_ip=dst_ip, tunnel_name=tunnel_name)
        ) 
        
def configure_te_tunnel(device, tunnel_name,\
        ip_config_subcmd, intf_type, intf_number):
    """creates tunnel with ip address.
        Args :
	    device (`obj`): Device object
	    tunnel_name (`str`): Tunnel Name
            ip_config_subcmd (`str`): subcommands for configuring ip address in tunnel  
            intf_type (`str`): interface type
	    intf_number(`str`): interface number
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure([
            "interface {tunnel_name}".format(tunnel_name=tunnel_name),
            "ip {ip_config_subcmd} {intf_type} {intf_number}".\
            format(ip_config_subcmd=ip_config_subcmd, intf_type=intf_type,\
            intf_number=intf_number),
            "tunnel mode mpls traffic-eng"])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure tunnel {tunnel_name}. Error: {error}"\
                        .format(tunnel_name=tunnel_name, error=e)
        ) 
        
def remove_explicit_path(device, explicit_paths):
    """Remove explicit path configuration, created for tunnel
        Args:
	    device (`obj`): Device object
	    explicit_paths (`list`): List of explicit paths to be removed
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        for path in explicit_paths:
            device.configure("no ip explicit-path name {path} enable"\
                .format(path=path)) 
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to remove explicit path {explicit_paths}, Error:{e}".
                            format(explicit_paths=explicit_paths, e=e)
        ) 
        
def config_vc_backup_peer(device, interface,
                        peer_address, backup_peer,
                        vc_id, backup_vc_id,
                        pw_class, backup_pw_class):
    '''configure backup peer vc on interface
        Args:
	    device (`obj`): Device object
	    interface (`str`): interface, backup peer need to be configured on
            peer_address (`str`): Address of the peer, main vc
            backup_peer('str'): Peer address of backup vc
            vc_id (`str`): VC ID for the back up peer
            backup_vc_id(`str`): Backup peer vc id
            pw_class(`str`): psuedowire class 
            backup_pw_class(`str`): psuedowire class of backup peer
        Returns:
            None
        Raises:
            SubCommandFailure
    '''
    try:
        device.configure([
            "interface {interface}".format(interface=interface),
            "xconnect {peer_address} {vc_id} encapsulation mpls pw-class "
            "{pw_class}".format(
                peer_address=peer_address, vc_id=vc_id, pw_class=pw_class),                  
            "backup peer {backup_peer} {backup_vc_id} pw-class "
            "{backup_pw_class}".format(
                backup_peer=backup_peer, backup_vc_id=backup_vc_id,\
                backup_pw_class=backup_pw_class)])
                            
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure back up peer on interface {interface}, "
            "Error:{e}".format(interface=interface, e=e)
        ) 
        
def config_eompls_pseudowire(device, pseudowire_name, neigh, vc_id, 
                             flow_ip=None, flow_label=None):
    
    '''configure pseudowire interface 
        Args:
            device (`obj`): Device 
            pseudowire_name (`str`): Specifies the pseudowire interface
            neigh (`str`) : Specifies the peer IP address
            vc_id (`str`) : virtual circuit (VC) ID value of the Layer 2 VPN (L2VPN) pseudowire.
            flow_ip (`str`) : Specifies load-balance factor Eg:dst-ip so on
            flow_label (`str`) : core load balancing based on flow-labels.
        Returns:
            None
        Raises:
            SubCommandFailure
    '''
    
    try:
        config=["interface pseudowire {pseudowire_name}".format(
                                 pseudowire_name=pseudowire_name),
                "encapsulation mpls",
        		"neighbor {neigh} {vc_id}".format(neigh=neigh, vc_id=vc_id)]
        if flow_ip:
            config.append("load-balance flow ip {flow_ip}".format(
                                                   flow_ip=flow_ip))
        if flow_label:
            config.append("load-balance flow-label {flow_label}".format(
                                                  flow_label=flow_label))
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure pseudowire {pseudowire_name}. Error:\n{error}".
                            format(pseudowire_name=pseudowire_name, error=e)
        )
    
def l2vpn_xconnect_context(device, context_name, pseudowire_member, interface):
    
    '''configure L2VPN xconnect context
        Args:
        device (`obj`): Device 
        context_name (`str`): l2vpn cross connect name
        pseudowire_member (`str`) : member pseudowire name 
        interface (`str`) : member interface name.
        Returns:
            None
        Raises:
            SubCommandFailure
    '''
    
    try:
        device.configure(["l2vpn xconnect context {context_name}".format(
                                                context_name=context_name),
    	                    "member {pseudowire_member}".format(
                            pseudowire_member=pseudowire_member),
    						"member {interface}".format(interface=interface)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure l2vpn xconnect context {context_name}."
            "Error:\n{error}".format(context_name=context_name,error=e)
        )    
    
def remove_l2vpn_xconnect_context(device, context_name):

    '''unconfigure l2vpn xconnect context
        Args:
	    device (`obj`): Device 
	    context_name (`str`): l2vpn cross connect name
        Returns:
            None
        Raises:
            SubCommandFailure
	'''

    try:
        device.configure(f"no l2vpn xconnect context {context_name}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not remove l2vpn xconnect context {context_name}."
            "Error:\n{error}".format(context_name=context_name, error=e)
        )    
        

def configure_mpls_ldp_graceful_restart(device):
    """ Configures mpls ldp graceful restart on device

        Args:
            device (`obj`): Device object

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        device.configure("mpls ldp graceful-restart")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't configure mpls ldp graceful restart on device. "
            "Error:\n{error}".format(error=e)
        )

def unconfigure_mpls_ldp_graceful_restart(device):
    """ Unconfigures mpls ldp graceful restart on device

        Args:
            device (`obj`): Device object

        Returns:
            None

        Raises:
            SubCommandFailure
	"""

    try:
        device.configure("no mpls ldp graceful-restart")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't unconfigure mpls ldp graceful restart on device. "
            "Error:\n{error}".format(error=e)
        )

        
def unconfigure_mpls_te_explicit_null(device, explicit_null=None, 
                                      verbatim=None):

    """unconfigure explicit null on Tunnel
        Args:
            device (`obj`): Device 
            explicit_null(`str`) : unconfigure explicit null 
            verbatim(`str`) : unconfigure verbatim
        Returns:
            None
        Raises:
            SubCommandFailure
	"""

    cmd=[]
    if explicit_null:
        cmd.append("no mpls traffic-eng signalling advertise explicit-null")
    if verbatim:
        cmd.append("no mpls traffic-eng signalling interpret explicit-null "
                   "verbatim")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not remove mpls traffic-eng signalling advertise "
            "explicit-null. Error:\n{error}".format(error=e)
        )
        
def configure_mpls_te_explicit_null(device, explicit_null=None, verbatim=None):

    """configure explicit null on Tunnel
        Args:
            device (`obj`): Device 
            explicit_null(`str`) : configure explicit null 
            verbatim(`str`) : configure verbatim
        Returns:
            None
        Raises:
            SubCommandFailure
	"""

    cmd=[]
    if explicit_null:
        cmd.append("mpls traffic-eng signalling advertise explicit-null")
    if verbatim:
        cmd.append("mpls traffic-eng signalling interpret explicit-null "
                   "verbatim")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mpls traffic-eng signalling explicit-null."
            "Error:\n{error}".format(error=e)
        )

def configure_layer2_vfi_manual(device, vfiname, vpnid, neighbors):

    """configure Layer 2 VFI manual configuration mode.
        Args:
	    device (`obj`): Device 
            vfiname(`str`): Name of VFI
            verbatim(`str`): vpnid for vpls domain
            neighbors(`list`): Specifies list of remote peering router ID.
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        for neigh in neighbors:
            device.configure(['l2 vfi {} manual'.format(vfiname),
                             'vpn id {}'.format(vpnid),
                             'neighbor {neigh} encapsulation mpls'
                                                   .format(neigh=neigh)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure vfi manual {vfiname}."
            "Error:\n{error}".format(vfiname=vfiname, error=e)
        )

def configure_layer2_vfi_context(device, vfiname, vpnid, neighbors, template):

    """configure Layer 2 VFI context configuration mode.
        Args:
	    device (`obj`): Device 
            vfiname(`str`): Name of VFI
            verbatim(`str`): vpnid for vpls domain
            neighbors(`list`): Specifies list of remote peering router ID.
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        for neigh in neighbors:
            device.configure([
                'l2 vfi context {} '.format(vfiname),
                'vpn id {}'.format(vpnid),
                'neighbor {neigh} template {template}'.format(
                    neigh=neigh, template=template)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure vfi context {vfiname}."
            "Error:\n{error}".format(vfiname=vfiname, error=e)
        )

def configure_pseudowire_encapsulation_mpls(device, pseudowire_class):
    """ Configures pseudowire encapsulation mpls

        Args:
            device (`obj`): Device object
            pseudowire_class (`str`): Pseudowire class be applied
        Returns:
            None
        Raises:
            SubCommandFailure
	"""

    try:
       device.configure(
            [
                "pseudowire-class {pw_class}".format(pw_class=pseudowire_class),
                "encapsulation mpls",
                "interworking vlan"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't configure pseudowire encapsulation mpls on device. "
            "Error:\n{error}".format(error=e)
        )
        
def unconfigure_layer2_vfi_manual(device, vfiname):

    """unconfigure Layer 2 VFI manual configuration mode.
        Args:
	    device (`obj`): Device 
            vfiname(`str`): Name of VFI
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure('no l2 vfi {} manual'.format(vfiname))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not remove vfi manual {vfiname}."
            "Error:\n{error}".format(vfiname=vfiname, error=e)
        )

def unconfigure_pseudowire_encapsulation_mpls(device, pseudowire_class):
    """ unconfigures pseudowire encapsulation mpls

        Args:
            device (`obj`): Device object
            pseudowire_class (`str`): Pseudowire class be applied
        Returns:
            None
        Raises:
            SubCommandFailure
	"""

    try:
       device.configure(
           "no pseudowire-class {pw_class}".format(
               pw_class=pseudowire_class)
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't unconfigure pseudowire encapsulation mpls on device. "
            "Error:\n{error}".format(error=e)
        )
        
def configure_attachment_circuit_vfi(device, interface, vfiname, 
                                     protocol_mode=False):

    """
    configure the Attachment Circuit with the VFI.
        Args:
	    device (`obj`): Device 
        interface(`str`): interface name
        vfiname(`str`): the Layer 2 VFI that you are binding to the VLAN port
        Returns:
            None
        Raises:
            SubCommandFailure
	"""

    if not protocol_mode:
        xconnect='xconnect vfi {}'.format(vfiname)
    else:
        xconnect="member vfi {}".format(vfiname)
    config=['interface {}'.format(interface)]
    config.append(xconnect)
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure Attachment Circuit {vfiname} on interface "
            "{interface} Error:\n{error}".format(
                interface=interface, vfiname=vfiname, error=e)
        )
        
def configure_layer2_vfi_autodiscovery(device, vfiname, vpnid):

    """configure Layer 2 VFI vpnid configuration mode.
        Args:
	    device (`obj`): Device 
            vfiname(`str`): Name of VFI
            vpnid(`str`): vpnid for vpls domain
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure(['l2 vfi {} autodiscovery'.format(vfiname),
                             'vpn id {}'.format(vpnid)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure vfi autodiscovery {vfiname}."
            "Error:\n{error}".format(vfiname=vfiname, error=e)
        )

def configure_mpls_pseudowire_xconnect_on_interface(device, interface, ip, vlan, 
                                                    pw_class):
    """ Configures mpls xconnect pseudowire class on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface on which the edge trunk config to be applied
            ip (`str`): IP address to be configured with xconnect
            vlan (`str`): Vlan id to be configured
            pw_class (`str`): Pseudowire class be applied
        Returns:
            None
        Raises:
            SubCommandFailure
	"""
    config=["interface {intf}".format(intf=interface)]
    config.append("xconnect {ip} {vlan} encapsulation mpls pw-class {pw_class}"\
        .format(ip=ip, vlan=vlan,pw_class=pw_class))

    try:
        device.configure(config)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't configure mpls xconnect pseudowire class on "
            "interface {intf} on device. "
            "Error:\n{error}".format(intf=interface, error=e)
        )
        
def unconfigure_layer2_vfi_autodiscovery(device, vfiname):

    """unconfigure Layer 2 VFI vpnid configuration mode.
        Args:
	    device (`obj`): Device 
            vfiname(`str`): Name of VFI
        Returns:
            None
        Raises:
            SubCommandFailure
	"""
    try:
        device.configure('no l2 vfi {} autodiscovery'.format(vfiname))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not remove vfi autodiscovery {vfiname}."
            "Error:\n{error}".format(vfiname=vfiname, error=e)
        )
        
def configure_mpls_label_mode_all_vrfs_protocol(
    device, address_family, label_allocation):
    """ Config mpls label mode all-vrfs protocol on device

        Args:
            device (`obj`): Device object
            address_family ('str'): address-family which is mode to be configured for
            label_allocation ('str'): label to configured for the address-family
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    try:
        device.configure(
            "mpls label mode all-vrfs protocol {address_family} {label}".format(
                address_family=address_family, label=label_allocation)
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure "mpls label mode all-vrfs protocol '
            '{address_family} {label}" on device {hostname}'.format(
                address_family=address_family, label=label_allocation, 
                hostname=device.hostname)
        )
       
def configure_autodiscovery_bgp_signalling_ldp_template(
    device, context_name, vpn_id, template_name):
    """ Config autodiscovery bgp signaling ldp template
        Args:
            device (`obj`): Device object
            context_name ('str'): context name for the template
            vpn_id ('str'): vpn id to be configured
            template_name('str'): name of the template
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    config=["l2vpn vfi context {context_name}".format(
                            context_name=context_name)]
    config.append("vpn id {vpn_id}".format(vpn_id=vpn_id))
    config.append("autodiscovery bgp signaling ldp template {template_name}"\
        .format(template_name=template_name))
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure autodiscovery bgp signalling template. '
            'Error:{e}'.format(e=e)
        )

def configure_l2vpn_vfi_context(
    device, context_name, vpn_id, member, template_name):
    """ Config l2vpn vfi context
        Args:
            device (`obj`): Device object
            context_name ('str'): context name for the template
            vpn_id ('str'): vpn id to be configured
            member('str') : member ip
            template_name('str'): name of the template
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    config=["l2vpn vfi context {context_name}".format(
                            context_name=context_name)]
    config.append("vpn id {vpn_id}".format(vpn_id=vpn_id))
    config.append("member {member} template {template_name}".format(
                           member=member, template_name=template_name))
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure l2vpn vfi context. Error:{e}'.format(e=e)
        )
        
def remove_vfi_context(device, context_name):
    """ Config autodiscovery bgp signaling ldp template
        Args:
            device (`obj`): Device object
            context_name ('str'): context name for the template
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """

    try:
        device.configure(["no l2vpn vfi context {context_name}".format(
                            context_name=context_name)]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure autodiscovery bgp signalling template. '
            'Error:{e}'.format(e=e)
        )
        
def configure_template_type_vpls(
    device, template_type, template_name, flow_classification, flow_ip_type, 
    flow_label_type):
    """ template type to be configured
        Args:
            device (`obj`): Device object
            template_type ('str'): template type for the template
            flow_classification('str'): classify the flow based on ip or ethernet
            template_name (`str`) : name of the template to be used
            flow_ip_type ('str'): define the flow ip type 
            flow_label_type ('str'): flow label to be used
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """

    config=[
        "template type {template_type} {template_name}".format(
            template_type=template_type, template_name=template_name)]
    config.append("encapsulation mpls")
    config.append("load-balance flow {flow_classification} {flow_ip_type}"\
          .format(flow_classification=flow_classification, 
                  flow_ip_type=flow_ip_type))
    config.append("load-balance flow-label {flow_label_type}"\
          .format(flow_label_type=flow_label_type))
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure template type for vpls {template_name}. '
            'Error:{e}'.format(template_name=template_name, e=e)
        )
        
def unconfigure_template_type_vpls(
    device, template_type, template_name):
    """ unconfigure template type
        Args:
            device (`obj`): Device object
            template_type ('str'): template type for the template
            template_name('str'): name of the template
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    try:
        device.configure([
            "no template type {template_type} {template_name}".format(
                template_type=template_type, template_name=template_name)]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not unconfigure template type for vpls {template_name}. '
            'Error:{e}'.format(template_name=template_name, e=e)
        )
       
def configure_traffic_eng_passive_interface(device, interface_name, neighbor, 
                                            neigh_intf_ip, ospf_neigh):
    
    '''configure traffic-eng passive-interface 
        Args:
        device (`obj`): Device 
        interface_name (`str`): interface name
        neighbor (`str`) : neighbor ip address
        neigh_intf_ip (`str`) : neighbor interface ip address
        ospf_neigh (`str`) : ospf neighbor ip
        Returns:
            None
        Raises:
            SubCommandFailure
    '''
    config=["interface {interface_name}".format(
                                                interface_name=interface_name)]
    config.append(
        "mpls traffic-eng passive-interface nbr-te-id {neighbor} "
        "nbr-if-addr {neigh_intf_ip} nbr-igp-id ospf {ospf_neigh}".format(
        neighbor=neighbor, neigh_intf_ip=neigh_intf_ip, ospf_neigh=ospf_neigh))
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure traffic-eng passive-interface under interface "
            "{interface_name}. Error:\n{error}".format(
                interface_name=interface_name,error=e)
        )        
        
def configure_mpls_static_binding(device, neighbor, mask, neigh_intf_ip):
    
    '''configure mpls static binding
        Args:
        device (`obj`): Device 
        neighbor (`str`) : neighbor ip address
        mask (`str`): mask to be used for ip address
        neigh_intf_ip (`str`) : neighbor interface ip address
        Returns:
            None
        Raises:
            SubCommandFailure
    '''
    cmd = "mpls static binding ipv4 {neighbor} {mask} output {neigh_intf_ip} "\
          "implicit-null".format(neighbor=neighbor, mask=mask, 
                                 neigh_intf_ip=neigh_intf_ip)
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mpls static binding for {neighbor}."
            "Error:\n{error}".format(neighbor=neighbor,error=e)
        )    
        
def unconfigure_mpls_static_binding(device, neighbor, mask, neigh_intf_ip):
    
    '''unconfigure mpls static binding
        Args:
        device (`obj`): Device 
        neighbor (`str`) : neighbor ip address
        mask (`str`): mask to be used for ip address
        neigh_intf_ip (`str`) : neighbor interface ip address
        Returns:
            None
        Raises:
            SubCommandFailure
    '''
    cmd="no mpls static binding ipv4 {neighbor} {mask} output {neigh_intf_ip} "\
        "implicit-null".format(neighbor=neighbor, mask=mask, 
                               neigh_intf_ip=neigh_intf_ip)
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mpls static binding for {neighbor}."
            "Error:\n{error}".format(neighbor=neighbor,error=e)
        )   

def configure_encapsulation_mpls_ldp(device, interface, neigbor, vlan_id):
    """ Configures encapsulation mpls ldp on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface on which the encapuslation
                               config to be applied
            neigbor (`str`): Neighbor id
            vlan_id (`str`): vlan id

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
       device.configure(
            [
                "interface {intf}".format(intf=interface),
                "encapsulation mpls",
                "signaling protocol ldp",
                "neighbor {neigh} {vlan}".format(neigh=neigbor, vlan=vlan_id)
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't configure encapsulation mpls lsp on interface {intf} "
            "Error:\n{error}".format(intf=interface, error=e)
        )

def configure_mpls_te_forwarding_adjacency(device, intf):
    
    '''configure mpls te forwarding-adjacency
        Args:
        device (`obj`): Device 
        intf ('str') : tunnel name
        Returns:
            None
        Raises:
            SubCommandFailure
    '''
    
    try:
        device.configure(["interface {intf}".format(intf=intf),
                        "tunnel mpls traffic-eng forwarding-adjacency"])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configuretunnel mpls traffic-eng forwarding-adjacency "
            "under tunnel {intf}. Error:\n{error}".format(intf=intf,error=e)
        )      

def configure_ldp_discovery_targeted_hello_accept(device):
    """ configure mpls ldp discovery targeted-hello accept 
        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    try:
        device.configure([
            "mpls ldp discovery targeted-hello accept"]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure mpls ldp discovery targeted-hello accept'
            'Error:{e}'.format(e=e)
        )  

def unconfigure_ldp_discovery_targeted_hello_accept(device):
    """ unconfigure mpls ldp discovery targeted-hello accept 
        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    try:
        device.configure([
            "no mpls ldp discovery targeted-hello accept"]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not unconfigure mpls ldp discovery targeted-hello accept'
            'Error:{e}'.format(e=e)
        ) 

def configure_administrative_weight(device, tunnel, weight):
    
    """ configure administrative weight in tunnel interface

        Args:
            device ('obj'): Device object
            tunnel ('str'): Tunnel name
            weight ('int'): Mention the admin weight
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    config_list=[f"interface {tunnel}",
                 f"mpls traffic-eng administrative-weight {weight}"]

    try:
        device.configure(config_list)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure administrative_weight {weight} for {tunnel}. "
            "Error:\n{error}".format(weight=weight, 
                                     tunnel=tunnel, error=e)
        )

def configure_interface_path_selection_metric(device, tunnel, metric):
    
    """ configure path selection metric for tunnel interface

        Args:
            device ('obj'): Device object
            tunnel ('str'): Tunnel name
            metric ('str'): Specify igp or te
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    config_list=[f"interface {tunnel}",
                 f"tunnel mpls traffic-eng path-selection metric {metric}"]

    try:
        device.configure(config_list)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure path-selection metric {metric} for {tunnel}. "
            "Error:\n{error}".format(metric=metric, 
                                     tunnel=tunnel, error=e)
        )

def unconfigure_ip_rsvp_bandwidth(device, interface, bandwidth=None):
    """ unconfigure ip rsvp bandiwth on interface
        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
            bandwidth ('str'): rsvp bandwidth
        Return:
            None
        Raise:
            SubCommandFailure: Failed unconfiguring interface
    """

    config_list=[f"interface {interface}",
                 f"no ip rsvp bandwidth"]
    
    if bandwidth:
        config_list.append(f"no ip rsvp bandwidth {bandwidth}")
    
    try:
        device.configure(config_list)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure rsvp bandwidth on {interface}."
            "Error:\n{error}".format(interface=interface, error=e)
        )

def unconfigure_dynamic_path_in_tunnel(device, tunnel,
                                    path_option,dynamic=False, attribute_name=None,
                                    explicit_name=None,
                                    lockdown=False,
                                    metric=None):
    """unconfigure dynamic path in tunnel
        Args:
            device ('obj'): Device object
            tunnel ('str'): Tunnel name
            path_option ('int'): Mention the path option value <1-1000>
            dynamic('Boolean'): Set to True to unconfigure dynamic path option
            attribute_name ('str'): Attribute name to be set
            explicit_name ('str'): Name for the explicit path
            lockdown('Boolean'): set the lockdown if true
            metric('str'): Specify igp or te
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config_list=[f"interface {tunnel}"]

    if dynamic:
        config_list.append(f"no tunnel mpls traffic-eng path-option {path_option} dynamic".format(path_option=path_option))
    if explicit_name:
        config_list.append(f"no tunnel mpls traffic-eng path-option {path_option} explicit name {explicit_name}".format(
            path_option=path_option,explicit_name=explicit_name))
    if attribute_name:
        config_list.append(f"no tunnel mpls traffic-eng path-option {path_option} explicit name {explicit_name} attributes {attribute_name}".format(
            path_option=path_option,explicit_name=explicit_name,attribute_name=attribute_name))
    if lockdown:
        config_list.append(f"no tunnel mpls traff path-option {path_option} dynamic lockdown".format(path_option=path_option))
    if metric:
        config_list.append(f"no tunnel mpls traffic-eng path-selection metric {metric}".format(metric=metric))

    try:
        device.configure(config_list)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure dynamic path for {tunnel}. Error:\n{error}".format(
                tunnel=tunnel, error=e
            )
        ) 

def l2vpn_xconnect_context_interface(device, context_name, pseudowire_member, interface, type):

    '''configure L2VPN xconnect context with internwtworking
        Args:
        device ('obj'): Device 
        context_name ('str'): l2vpn cross connect name
        pseudowire_member ('str') : member pseudowire name 
        interface ('str') : member interface name.
        Returns:
            None
        Raises:
            SubCommandFailure
    '''

    config_list=["interface {interface}".format(interface=interface),
                "l2vpn xconnect context {context_name}".format(context_name=context_name),
    	        "member pseudowire {pseudowire_member}".format(pseudowire_member=pseudowire_member),
    			"member {interface}".format(interface=interface),
                "internetworking {type}".format(type=type)]

    try:
        device.configure(config_list)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure l2vpn xconnect context {context_name}."
            "Error:\n{error}".format(context_name=context_name,error=e)
        ) 

def configure_mpls_te_nsr(device):

    """configure mpls te nsr on device
        Args:
            device (`obj`): Device object   
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            "mpls traffic-eng nsr"
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mpls te nsr on device. Error: {error} ".format(
                                    error=e)
        )

def configure_rsvp_gracefull_restart(device):

    """configure ip rsvp gracefull restart with mode as help-neigbor
        Args:
            device (`obj`): Device object   
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            "ip rsvp signalling hello graceful-restart mode help-neighbor"
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ip rsvp gracefull restart on device. Error: {error} ".format(
                                    error=e)
        )

def debug_lfd_label_statistics(device,label_number):
    """ configure debug lfd label statistics
        Args:
            device ('obj'): device to execute on
            label_number ('int') : label value 
            
        Return:
            None
        Raises:
            SubCommandFailure
    """
   
    try:
        device.execute("debug mpls lfd local-label {label_number} statistics-enable".format(label_number=label_number))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure debug lfd label statistics Error {e}".format(e=e))

def configure_template_pseudowire(device, template_type, template_name):
    """Configure template name
       Args:
            device ('obj'): device object
            template_type ('str'): template type
            template_name ('str'): template name
       Return:
            None
       Raises:
            SubCommandFailure
    """
    config= [
               f'template type {template_type} {template_name}',
               'encapsulation mpls'
            ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to Configure template pseudowire on {device.name}\n{e}'
        )
        
def configure_member_vfi_on_vlan_configuration(device, vlan_id, vfi_type, vfi_name):
    """ configure member vfi
        Args:
            device ('obj'): Device object
            vlan_id ('int'): vlan id 
            vfi_type ('str'): specify access-vfi or vfi
            vfi_name ('str'): specify member vfi name
        Return:
            None
        Raise:
            SubCommandFailure: Failed unconfiguring interface
    """

    config = [f'vlan configuration {vlan_id}',f'member {vfi_type} {vfi_name}']
    
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to Configure member vfi on {device.name}\n{e}'
        )
    
def configure_mpls_ldp_sync_under_ospf(device, process_id, router_id):
    """Configure router ospf mpls
       Args:
            device ('obj'): device object
            process_id ('int'): process id
            router_id ('str'): OSPF router-id in IP address format
       Return:
            None
       Raises:
            SubCommandFailure
    """
    config= [
               f'router ospf {process_id}',
               f'router-id {router_id}',
               'mpls ldp sync'
            ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to Configure router ospf mpls on {device.name}\n{e}'
        )

def config_qinq_encapsulation_on_interface(device, vlan, second_vlan, interface):
    """ Configure dot1q encapsulation on Interface with double tagging

        Args:
            device (`obj`): Device object
            interface (`str`): Interface on which the edge trunk config to be applied
            vlan  (`str`): Vlan to be configured with encapsulation
            second_vlan (`str`): Second Vlan to be configured with encapsulation

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
               f"interface {interface}",
               f"encapsulation dot1q {vlan} second-dot1q {second_vlan}"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't configure qinq encapsulation on interface {interface}. "
            "Error:\n{error}".format(interface=interface, error=e)
        )

def config_pseudowire_class_interworking(device, pw_class, interworking):
    """ configure pseudowire class with interworking
        Args:
            device (`obj`): Router on which pseudowire class has to be configured
            pw_class ('str'): pseudowire class name on which configuration needs to be applied.
            interworking (`str`): Interworking enabled or disabled for traffic in peusdowire class.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = ["pseudowire-class {pw_class}".format(pw_class=pw_class),
           "encapsulation mpls",
           "interworking {interworking}".format(interworking=interworking)]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure pseudowire class {pw_class}. Error:\n{error}"\
                .format(pw_class=pw_class, error=e)
        )
