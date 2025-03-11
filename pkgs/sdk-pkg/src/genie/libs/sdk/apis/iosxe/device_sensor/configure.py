"""Common configure functions for device sensor"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_device_sensor_filter_list(device, protocol, list_name, tlv_name=None, 
                                        tlv_number=None, option_name=None, option_number=None):
    """ Configure device sensor filter list
    Args:
        device ('obj'): device to use
        protocol ('str'): Protocol names like cdp, dhcp, lldp.
        list_name ('str'): Protocol list name.
        tlv_name ('str', optional): TLV type list name. Default is None.
        tlv_number ('int', optional): TLV type list number. Default is None.
        option_name ('str', optional): Option type list name. Default is None.
        option_number ('str', optional): Option type list name. Default is None.
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to configure device sensor filter list
    """

    cmd = [f'device-sensor filter-list {protocol} list {list_name}']
    if tlv_name:
        cmd.append(f'tlv name {tlv_name}')
    if tlv_number:
        cmd.append(f'tlv number {tlv_number}')
    if option_name:
        cmd.append(f'option name {option_name}')
    if option_number:
        cmd.append(f'option number {option_number}')
    try:
        device.configure(cmd)
    
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure device sensor filter list. Error:\n{e}")


def unconfigure_device_sensor_filter_list(device, protocol, list_name, tlv_name=None, 
                                          tlv_number=None, option_name=None, option_number=None, filter_list=False):
    """ Unconfigure device sensor filter list
    
    Args:
        device ('obj'): device to use
        protocol ('str'): Protocol names like cdp, dhcp, lldp.
        list_name ('str'): Protocol list name.
        tlv_name ('str', optional): TLV type list name. Default is None.
        tlv_number ('int', optional): TLV type list number. Default is None.
        option_name ('str', optional): Option type list name. Default is None.
        option_number ('str', optional): Option type list name. Default is None.
        filter_list ('bool', optional): Unconfigures filter-list name. Default is False.
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to unconfigure device sensor filter list
    """

    cmd = [f'device-sensor filter-list {protocol} list {list_name}']
    if tlv_name:
        cmd.append(f'no tlv name {tlv_name}')
    if tlv_number:
        cmd.append(f'no tlv number {tlv_number}')
    if option_name:
        cmd.append(f'no option name {option_name}')
    if option_number:
        cmd.append(f'no option number {option_number}')
    if filter_list:
        cmd = [f'no device-sensor filter-list {protocol} list {list_name}']
    try:
        device.configure(cmd)
    
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure device sensor filter list. Error:\n{e}")


def configure_radius_server_vsa(device, vsa_attribute, send_attribute=None, disallow_attribute=None, 
                                req_attribute=None, protocol=None):

    """ Configure Radius Interface via vrf
    Args:
        device ('obj'): device to use
        vsa_attribute ('str'): Vendor specific attribute to be configured(Eg:disallow/send)
        send_attribute ('str', optional): Send attribute to be configured(Eg:accounting/authentication/cisco-nas-port/nas-port)
        disallow_attribute ('str', optional): Forbid certain VSA behaviour
        req_attribute ('str', optional): Send in requests(Eg:3gpp2/nas-port)
        protocol ('str', optional): Protocol(Eg:pppoa/pppoe)

    Returns:
        None

    Raises:
        SubCommandFailure: Failed configuring Radius Server VSA

    """
    cmd =[]

    if disallow_attribute:
        cmd = f"radius-server vsa {vsa_attribute} {disallow_attribute}"

    elif send_attribute and req_attribute and protocol:
        cmd = f"radius-server vsa {vsa_attribute} {send_attribute} {req_attribute} protocol {protocol} vsa1"

    elif send_attribute and req_attribute:
        cmd = f"radius-server vsa {vsa_attribute} {send_attribute} {req_attribute}"

    elif send_attribute:
        cmd = f"radius-server vsa {vsa_attribute} {send_attribute}"    
    
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not Configure Radius Server VSA. Error\n{e}"
        )


def configure_device_sensor_notify(device, notify_attribute):

    """ Configure Device sensor notify
    Args:
        device ('obj'): device to use
        notify_attribute ('str'): Options for when to trigger identity update events(Eg:all-changes/new-tlvs)
    Returns:
        None
    Raises:
        SubCommandFailure: Failed configuring Device-sensor notify 

    """
    cmd = f"device-sensor notify {notify_attribute}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not Configure Device-sensor notify. Error\n{e}"
        )


def configure_device_sensor_filter_spec(device, protocol, exclude=False, 
                                           include=False, exclude_filter =None, exclude_list=None, include_list=None):

    """ Configure Device sensor filter spec
    Args:
        device ('obj'): device to use
        protocol ('str'): Sensor Protocol Filter Spec Configuration(Eg:cdp/dhcp/dhcpv6/lldp)
        exclude ('bool', optional): Configure exclude filter
        include ('bool', optional): Configure include filter
        exclude_filter ('str', optional): Exclude filter type(Eg:all/list)
        exclude_list ('str', optional): Exclude list name
        include_list ('str', optional): Include list name
    Returns:
        None
    Raises:
        SubCommandFailure: Failed configuring Device sensor filter spec

    """
    cmd =[]

    if exclude and exclude_list:
        cmd = f"device-sensor filter-spec {protocol} exclude {exclude_filter} {exclude_list}"

    elif exclude and exclude_filter is not None:
        cmd = f"device-sensor filter-spec {protocol} exclude {exclude_filter}"

    elif include and include_list is not None:
        cmd = f"device-sensor filter-spec {protocol} include list {include_list}"
    
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not Configure Device sensor filter spec. Error\n{e}"
        )

def configure_device_sensor_dhcpv6_snooping(device, interface):
    """Configure device-sensor dhcpv6-snooping on an interface
    Args:
        device ('obj'): Device object
        interface ('str'): Interface name
    Returns:
        None
    Raises:
        SubCommandFailure: Failed configuring device-sensor dhcpv6-snooping
    """
    cmd = [
        f"interface {interface}",
        "device-sensor dhcpv6-snooping"
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure device-sensor dhcpv6-snooping on interface {interface}. Error:\n{e}"
        )

def unconfigure_device_sensor_dhcpv6_snooping(device, interface):
    """Configure device-sensor dhcpv6-snooping on an interface
    Args:
        device ('obj'): Device object
        interface ('str'): Interface name
    Returns:
        None
    Raises:
        SubCommandFailure: Failed configuring device-sensor dhcpv6-snooping
    """
    cmd = [
        f"interface {interface}",
        "no device-sensor dhcpv6-snooping"
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure device-sensor dhcpv6-snooping on interface {interface}. Error:\n{e}"
        )
