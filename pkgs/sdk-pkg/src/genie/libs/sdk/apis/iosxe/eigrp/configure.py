"""Common configure/unconfigure functions for IPSEC"""

# Unicon
from unicon.core.errors import SubCommandFailure

def configure_eigrp_networks(device, process_id, ip_address=None, netmask=None, router_id=None, bfd=None):
    """ Configures eigrp on networks
        Args:
            device ('obj'): Device to use
            process_id ('str'): Process id for eigrp process
            ip_address ('list'): List of ip_address' to configure
            netmask ('str'): Netmask to use
            router_id('str',optional): ospf router id
            bfd ('str', optional) : bfd name, default value is None
        Returns:
            N/A
        Raises:
            SubCommandFailure
    """
    cmd = ['router eigrp {process_id}'.format(process_id=process_id)]
    if ip_address:
        for ip in ip_address:
            cmd.append('network {ip_address} {netmask}'
                   .format(ip_address=ip, netmask=netmask))
    if router_id:
        cmd.append('router-id {router_id}'.format(router_id=router_id))
    if bfd:
        cmd.append("bfd {bfd}".format(bfd=bfd))
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to add network under eigrp {process_id}. Error:\n{error}".format(
                process_id=process_id, error=e)
        )

def configure_interface_eigrp_v6(device,interfaces,process_id):
    """ Configures switchport mode on interface
        Args:
            device ('obj')     device to use
            interfaces ('list'). List of interfaces to configure
            process_id ('str). EIGRP process id
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    #initialize list variable
    config_list = []
    for intf in interfaces:
        config_list.append("interface {intf}".format(intf=intf))
        config_list.append("ipv6 eigrp {process_id}".format(process_id=process_id))
    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure IPv6 Eigrp on interface. Error:\n{error}'.format(error=e)
        )

def unconfigure_interface_eigrp_v6(device,interfaces,process_id):
    """ Configures switchport mode on interface
        Args:
            device ('obj')     device to use
            interfaces ('list'). List of interfaces to unconfigure
            process_id ('str). EIGRP process id
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    #initialize list variable
    config_list = []
    for intf in interfaces:
        config_list.append("interface {intf}".format(intf=intf))
        config_list.append("no ipv6 eigrp {process_id}".format(process_id=process_id))
    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not unconfigure IPv6 Eigrp on interface. Error:\n{error}'.format(error=e)
        )


def enable_ipv6_eigrp_router(device,process_id):
    """ Configures switchport mode on interface
        Args:
            device ('obj')     device to use
            process_id ('str). EIGRP process id
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config_list = []
    config_list.append("ipv6 router eigrp {process_id}".format(process_id=process_id))
    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not Enable IPv6 Eigrp Router. Error:\n{error}'.format(error=e)
        )

def unconfigure_ipv6_eigrp_router(device,process_id):
    """ Unconfigures IPv6 Eigrp Router
        Args:
            device ('obj')     device to use
            process_id ('str). EIGRP process id
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config_list  = ["no ipv6 router eigrp {process_id}".format(process_id=process_id)]

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not unconfigure IPv6 Eigrp Router. Error:\n{error}'.format(error=e)
        )

def unconfigure_eigrp_router(device,process_id):
    """ Unconfigures IPv6 Eigrp Router
        Args:
            device ('obj')     device to use
            process_id ('str). EIGRP process id
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config_list = ["no router eigrp {process_id}".format(process_id=process_id)]

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not unconfigure IPv6 Eigrp Router. Error:\n{error}'.format(error=e)
        )

def configure_eigrp_named_networks(device, name, autonomous_system=None, ip_address=None,
    netmask=None, router_id=None, address_family=None, vrf='', af_action='', eigrp_router_id=None):
    """ Configures eigrp on networks
        Args:
            device ('obj'): Device to use
            name ('str'): EIGRP named mode name
            autonomous_system ('str', optional): Autonomous system number valid if address_family is set. (Default is None)
            ip_address ('list', optional): List of ip_address' to configure ( Default is None )
            netmask ('str',optional): Netmask to use ( Default is None )
            router_id ('str',optional): eigrp router id ( Default is None )
            address_family ('str',optional): address family to configure ( Default is None )
            vrf ('str', optional): vrf to configure ( Default is '' )
            af_action ('str',optional): unicast or multicast (Default is '')
            eigrp_router_id ('str', optional): Eigrp router ID in Ip address format (Default is None)
        Returns:
            N/A
        Raises:
            SubCommandFailure
    """
    cmd = []
    cmd.append('router eigrp {name}'.format(name=name))

    if address_family and vrf != '':
        cmd.append("address-family {address_family} {af_action} vrf {vrf} autonomous-system {autonomous_system}".format(
            address_family=address_family, af_action=af_action, vrf=vrf, autonomous_system=autonomous_system ))
    if address_family and vrf == '':
        cmd.append("address-family {address_family} {af_action} autonomous-system {autonomous_system}".format(
            address_family=address_family, af_action=af_action, autonomous_system=autonomous_system ))

    if ip_address:
        for ip in ip_address:
            cmd.append('network {ip_address} {netmask}'
                   .format(ip_address=ip, netmask=netmask))
    if router_id:
        cmd.append('router-id {router_id}'.format(router_id=router_id))
    if eigrp_router_id:
        cmd.append(f'eigrp router-id {eigrp_router_id}')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to add network under eigrp {name}. Error:\n{error}".format(
                name=name, error=e)
        )

def configure_ipv6_eigrp_named_networks(device, eigrp_name, autonomous_system, protocol_name, autonomous_system_number, af_action='', bandwidth='',topology_name=''):
    """ Configures eigrp on networks
        Args:
            device ('obj'): Device to use
            eigrp_name ('str'): EIGRP named mode name
            autonomous_system ('str'): Autonomous system number
            protocol_name ('str',optional): protocol should mention
            autonomous_system_number ('str',optional): Autonomous system number 
	        af_action ('str',optional): unicast or multicast (Default is '')
            bandwidth ('str',optional): bandwidth
            topology_name ('str',optional): topology name
	         
            
        Returns:
            N/A
        Raises:
            SubCommandFailure
    """
    cmd = [f'router eigrp {eigrp_name}',
            f'address-family ipv6 {af_action} autonomous-system {autonomous_system}',
            f'topology {topology_name}',
            f'redistribute {protocol_name} {autonomous_system_number}',
            f'default-metric {bandwidth}'] 
		
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to add network under eigrp {eigrp_name}. Error:\n{error}".format(
                eigrp_name=eigrp_name, error=e)
        )

def configure_vrf_ipv6_eigrp_named_networks(device, eigrp_name, af_action, vrf_name, autonomous_system, nsf=''):
    """ 
    API for the CLI :- 
        router eigrp {eigrp_name}\naddress-family ipv6 {af_action} vrf {vrf_name} autonomous-system {autonomous_system}\n {nsf}
        e.g.
        Args:
            device ('obj'): Device object
            eigrp_name ('str'): EIGRP named mode name
            af_action ('str',optional): unicast or multicast (Default is '') 
            vrf_name ('str', optional): vrf name to configure ( Default is '' )
            autonomous_system ('str'): Autonomous system number
            nsf - optional
        Return:
            None
        Raise:
            SubCommandFailure
    """
    cmd = [f'router eigrp {eigrp_name}', 
           f'address-family ipv6 {af_action} vrf {vrf_name} autonomous-system {autonomous_system}',
           f'{nsf}']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure ipv6 vrf under eigrp {eigrp_name}. Error:\n{error}".format(
                eigrp_name=eigrp_name, error=e)
        )


def unconfigure_eigrp_named_router(device,name):
    """ Unconfigures IPv6 Eigrp Router
        Args:
            device ('obj'): Device to use
            name ('str): EIGRP named mode name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = ["no router eigrp {name}".format(name=name)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not unconfigure eigrp named mode router. Error:\n{error}'.format(error=e)
        )

def configure_eigrp_redistributed_connected(device, eigrp_process_id):

    """ configure redistribute connected under eigrp
        Args:
            device (`obj`): device to execute on
            eigrp_process_id (`int`): process id of eigrp
        Return:
            None
        Raises:
            SubCommandFailure
    """
    config=["router eigrp {eigrp_process_id}".format(
                                    eigrp_process_id=eigrp_process_id)]
    config.append("redistribute connected")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure redistribute connected under eigrp "
            "{eirp_process_id}, Error: {error}".format(
               eigrp_process_id=eigrp_process_id,
               error=e
            )
        )

def configure_eigrp_named_networks_with_af_interface(device, name, autonomous_system, ip_address=None, netmask=None, router_id=None, address_family=None, vrf='', af_action='',af_interface=None):
    """ Configures eigrp on networks
        Args:
            device ('obj'): Device to use
            name ('str'): EIGRP named mode name
            autonomous_system ('str'): Autonomous system number
            ip_address ('list', optional): List of ip_address' to configure ( Default is None )
            netmask ('str',optional): Netmask to use ( Default is None )
            router_id ('str',optional): eigrp router id ( Default is None )
            address_family ('str',optional): address family to configure ( Default is None )
            vrf ('str', optional): vrf to configure ( Default is '' )
            af_action ('str',optional): unicast or multicast (Default is '')
            af_interface('str'optional): interface name ( Default is None )
        Returns:
            N/A
        Raises:
            SubCommandFailure
    """
    cmd = []
    cmd.append('router eigrp {name}'.format(name=name))

    if address_family and vrf != '':
        cmd.append("address-family {address_family} {af_action} vrf {vrf} autonomous-system {autonomous_system}".format(
            address_family=address_family, af_action=af_action, vrf=vrf, autonomous_system=autonomous_system ))
    if address_family and vrf == '':
        cmd.append("address-family {address_family} {af_action} autonomous-system {autonomous_system}".format(
            address_family=address_family, af_action=af_action, autonomous_system=autonomous_system ))

    if ip_address:
        for ip in ip_address:
            cmd.append('network {ip_address} {netmask}'
                   .format(ip_address=ip, netmask=netmask))
    if router_id:
        cmd.append('eigrp router-id {router_id}'.format(router_id=router_id))
    if af_interface:
        cmd.append('af-interface {af_interface}\n'.format(af_interface=af_interface))
        cmd.append('bfd\n')
        cmd.append('exit-af-interface')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to add network under eigrp {name}. Error:\n{error}".format(
                name=name, error=e)
        )


def configure_eigrp_router_configs(device, process_id, max_paths=None, auto_summary=False):
    """ Configures Eigrp Router configs
        Args:
            device ('obj'):     device to use
            process_id ('str'): EIGRP process id
            max_paths ('int', optional):  Number of paths. (Default is None)
            auto_summary ('bool', optional): Set to True to Configure auto-summary. (Default is False)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config_list = [f"router eigrp {process_id}"]

    if max_paths:
        config_list.append(f"maximum-paths {max_paths}")
    
    if auto_summary:
        config_list.append('auto-summary')

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure Router EIGRP Configs. Error:\n{error}'.format(error=e)
        )


def unconfigure_eigrp_router_configs(device, process_id, max_paths=None, auto_summary=False):
    """ Unconfigures Eigrp Router Configs
        Args:
            device ('obj'):     device to use
            process_id ('str'): EIGRP process id
            max_paths ('int', optional):  Number of paths. (Default is None)
            auto_summary ('bool', optional): Set to True to Unonfigure auto-summary. (Default is False)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config_list = [f'router eigrp {process_id}']

    if max_paths:
        config_list.append('no maximum-paths')
    
    if auto_summary:
        config_list.append('no auto-summary')

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not Unconfigure Router EIGRP Configs. Error:\n{error}'.format(error=e)
        )
