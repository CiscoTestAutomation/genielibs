"""Common configure/unconfigure functions for IPSEC"""

# Unicon
from unicon.core.errors import SubCommandFailure

def configure_eigrp_networks(device, process_id, ip_address=None, netmask=None, router_id=None):
    """ Configures eigrp on networks
        Args:
            device ('obj'): Device to use
            process_id ('str'): Process id for eigrp process
            ip_address ('list'): List of ip_address' to configure
            netmask ('str'): Netmask to use
            router_id('str',optional): ospf router id
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

def configure_eigrp_named_networks(device, name, autonomous_system, ip_address=None, netmask=None, router_id=None, address_family=None, vrf='', af_action=''):
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
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to add network under eigrp {name}. Error:\n{error}".format(
                name=name, error=e)
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