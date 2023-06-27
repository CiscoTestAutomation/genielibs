"""Common configure functions for arp"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

log = logging.getLogger(__name__)


def configure_arp_timeout(device, interface, timeout):
    """ Config arp timeout on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            timeout (`int`): timeout in second
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring arp timeout on interface {} with value {}".format(
            interface, timeout
        )
    )
    try:
        device.configure(
            [
                "interface {}".format(interface),
                "arp timeout {}".format(timeout),
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring arp timeout "
            "on interface {interface} with value {timeout} "
            "on device {device}, "
            "Error: {e}".format(
                interface=interface,
                timeout=timeout,
                device=device.name,
                e=str(e),
            )
        ) from e

def clear_arp_cache(device, ip_address=None, counter=None, interface=None, vrf=None):
    """ Clears device cache

        Args:
            device (`obj`): Device object
            ip_address (`str`): ip address of arp entry
            counters (`str`): counter type of arp entry
            interface (`str`): interface to clear arp entry
            vrf (`str`): vrf to clear arp entry
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = 'clear arp-cache'
    if vrf and ip_address:
        cmd+= ' vrf {vrf} {ip_address}'.format(vrf=vrf, ip_address=ip_address)
    elif ip_address:
        cmd+= ' {ip_address}'.format(ip_address=ip_address)
    elif counter:
        cmd+= ' counters {counter}'.format(counter=counter)
    elif interface:
        cmd+= ' interface {interface}'.format(interface=interface)
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to {cmd} on device {device}, '
            f'Error: {e} {device.name}, {str(e)}'
        ) from e

def remove_arp_timeout(device, interface):
    """ Remove arp timeout configuration

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("Removing arp timeout on interface {}".format(interface))
    try:
        device.configure(["interface {}".format(interface), "no arp timeout"])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in removing arp timeout "
            "on interface {interface} "
            "on device {device}, "
            "Error: {e}".format(
                interface=interface, device=device.name, e=str(e)
            )
        ) from e


def configure_static_arp(device, ip_address, mac_address):
    """ Configure static arp

        Args:
            device (`obj`): Device object
            ip_address (`str`): IP address
            mac_address (`str`): MAC address
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("Configuring static arp")
    try:
        device.configure(
            "arp {ip_address} {mac_address} arpa".format(
                ip_address=ip_address, mac_address=mac_address
            )
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring static arp "
            "with IP address {ip_address} "
            "and MAC address {mac_address} "
            "on device {device}, "
            "Error: {e}".format(
                ip_address=ip_address,
                mac_address=mac_address,
                device=device.name,
                e=str(e),
            )
        ) from e

def configure_ip_arp_inspection_vlan(
        device,
        vlan):

    """ Config ip arp inspection vlan on device
        Args:
            device ('obj'): Device object
            vlan  ('int'): vlan id
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
               f"ip arp inspection vlan {vlan}",
            ]
        )

    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Failed to config ip arp inspection vlan.")


def unconfigure_ip_arp_inspection_vlan(
        device,
        vlan):

    """ Unconfig ip arp inspection vlan on device
        Args:
            device ('obj'): Device object
            vlan  ('int'): vlan id
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure(
            [
               f"no ip arp inspection vlan {vlan}",
            ]
        )

    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Failed to unconfig ip arp inspection vlan")


def configure_ip_arp_inspection_validateip(device, address_type='ip'):

    """ Configure ip arp inspection validate {address_type} on device
        Args:
            device ('obj'): Device object
            address_type ('str', optional): Address type. Default is 'ip'
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"ip arp inspection validate {address_type}"]
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            f"Failed to configure ip arp inspection validate {address_type}.")


def unconfigure_ip_arp_inspection_validateip(device, address_type='ip'):

    """ Unconfigure ip arp inspection validate ip  on device
        Args:
            device ('obj'): Device object
            address_type ('str', optional): Address type. Default is 'ip'
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [f"ip arp inspection validate {address_type}"]
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            f"Failed to unconfigure ip arp inspection validate {address_type}.")

def configure_ip_arp_inspection_on_interface(device, interface, type, rate=None):
    """ Config ip arp inspection on interface
        Args:
            device ('obj'): Device object
            interface ('str'): interface name
            type ('str'): interface limit or trust
            rate ('int', optional): Packets per second
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if rate:
        cmd = [f"ip arp inspection {type} rate {rate}"]
    else:
        cmd = [f"ip arp inspection {type}"]
    try:
        device.configure(["interface {interface}".format(interface=interface), cmd])

    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Failed to config ip arp inspection on interface")

def unconfigure_ip_arp_inspection_on_interface(device, interface, type, rate=None):
    """ Unconfig ip arp inspection on interface
        Args:
            device ('obj'): Device object
            interface ('str'): interface name
            type ('str'): interface limit or trust
            rate ('int', optional): Packets per second
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if rate:
        cmd = [f"no ip arp inspection {type} rate {rate}"]
    else:
        cmd = [f"no ip arp inspection {type}"]
    try:
        device.configure(["interface {interface}".format(interface=interface), cmd])

    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Failed to unconfig ip arp inspection on interface")


def configure_ip_arp_inspection_log_buffer(device, buffer_type, entries, interval=None):

    """ Configure ip arp inspection log-buffer {type} {entries} on device
        Args:
            device ('obj'): Device object
            buffer_type ('str'): log-buffer type 'entries' or 'logs'.
            entries ('int'): Number of entries.
            interval ('int', optional): Interval in seconds. Default is None.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"ip arp inspection log-buffer {buffer_type} {entries}"
    if interval:
        cmd += f" interval {interval}"
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            f"Failed to configure ip arp inspection log-buffer {buffer_type}.")

def unconfigure_ip_arp_inspection_log_buffer(device, buffer_type):

    """ Unconfigure ip arp inspection log-buffer {type} on device
        Args:
            device ('obj'): Device object
            buffer_type ('str'): log-buffer type 'entries' or 'logs'.
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [f"no ip arp inspection log-buffer {buffer_type}"]
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            f"Failed to unconfigure ip arp inspection log-buffer {buffer_type}.")

def clear_ip_arp_inspection(device, intype):
    """ Clears ip arp inspection
        Args:
            device (`obj`): Device object
            intype (`str`): statistics or log
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.execute(f"clear ip arp inspection {intype}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to clear ip arp inspection  {device} . Error:\n{e}")

def configure_ip_arp_inspection_vlan_logging(device, range, log_config, log_type=None):
    ''' Configure ip arp inspection vlan logging
        Args:
            device ('obj'): Device object
            range ('str'):   WORD  vlan range, example: 1,3-5,7,9-11
            log_config ('str'): acl-match --->  matchlog  Log packets on ACE logging configuration
                                                none      Do not log packets that match ACLs
                                dhcp-bindings ->  all     Log all packets that match DHCP bindings
                                                  none    Do not log packets that match DHCP bindings
                                                  permit  Log DHCP Binding Permitted packets
                                arp-probe ---->  <cr>  <cr>
            log_type(optional): acl-match      Logging of packets that match ACLs
                                arp-probe      Log ARP probe packets with zero sender IP addr
                                dhcp-bindings  Logging of packet that match DHCP bindings
        Returns:
            None
        Raises:
            SubCommandFailure
    '''
    
    cmd = f"ip arp inspection vlan {range}" 
    if log_type:
        cmd += f" logging {log_type} {log_config}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Failed to configure ip arp inspection vlan logging")


def unconfigure_ip_arp_inspection_vlan_logging(device, range, log_config, log_type=None):    
    '''Unconfigure ip arp inspection vlan logging
        Args:
            device ('obj'): Device object
            range ('str'):   WORD  vlan range, example: 1,3-5,7,9-11
            log_config ('str'): acl-match --->  matchlog  Log packets on ACE logging configuration
                                                none      Do not log packets that match ACLs
                                dhcp-bindings ->  all     Log all packets that match DHCP bindings
                                                  none    Do not log packets that match DHCP bindings
                                                  permit  Log DHCP Binding Permitted packets
                                arp-probe ---->  <cr>  <cr>
            log_type(optional): acl-match      Logging of packets that match ACLs
                                arp-probe      Log ARP probe packets with zero sender IP addr
                                dhcp-bindings  Logging of packet that match DHCP bindings
        Returns:
            None
        Raises:
            SubCommandFailure
    '''
    cmd = f"no ip arp inspection vlan {range}" 
    if log_type:
        cmd += f" logging {log_type} {log_config}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Failed to unconfigure ip arp inspection vlan logging")

def configure_arp_access_list_permit_ip_host(
    device, name, action, ip_address, mac_address, log_match=True):
    '''Configures arp access-list with ip host
        Example : arp access-list allowed_acl
                    permit ip host 10.1.1.1 mac any log
        Args:
            device ('obj'): device to use
            name ('str'): access-list name (eg. allowed_acl)
            action ('str'): Specify packets to forward or reject (eg. permit, deny)
            ip_address ('str'): Sender Host IP address (eg. 10.1.1.1)
            mac_address ('str'): Sender MAC address (eg. any)
            log_match ('str'): Log on match
        Returns:
            None
        Raises:
            SubCommandFailure
    '''
    log.info(f'Configures arp access-list with ip host on {device.name}')
    cmd = [f'arp access-list {name}']
    if log_match:
        cmd.append(f'{action} ip host {ip_address} mac {mac_address} log')
    else:
        cmd.append(f'{action} ip host {ip_address} mac {mac_address}')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to configure arp access-list with ip host on device {device.name}. Error:\n{e}'
        )

def configure_ip_arp_inspection_filter(device, arp_name, vlan_id):
    ''' Clears ip arp inspection
        Args:
            device (`obj`): Device object
            arp_name (`str`): allowed_acl
            vlan_id ('str'): vlan id
        Returns:
            None
        Raises:
            SubCommandFailure
    '''
    cmd=[f"ip arp inspection filter {arp_name} vlan {vlan_id}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to clear ip arp inspection  {device} . Error:\n{e}"
            )

def unconfigure_ip_arp_inspection_filter(device, arp_name, vlan_id):
    ''' configures ip arp inspection filter
        Args:
            device (`obj`): Device object
            arp_name (`str`): allowed_acl
            vlan_id ('str'): vlan id
        Returns:
            None
        Raises:
            SubCommandFailure
    '''
    cmd=[f"no ip arp inspection filter {arp_name} vlan {vlan_id}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to clear ip arp inspection  {device} . Error:\n{e}"
            )
    
def unconfigure_arp_access_list(device, list_type, word):
    ''' unconfigures arp access-list
        Args:
            device (`obj`): Device object
            list_type (`str`): access-list
            word ('str'): allowed_acl
        Returns:
            None
        Raises:
            SubCommandFailure
    '''
    cmd=[f"no arp {list_type} {word}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to clear ip arp inspection  {device} .Error:\n{e}"
            )
