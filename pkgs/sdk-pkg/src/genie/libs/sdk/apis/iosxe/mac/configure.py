"""Common configure functions for mac"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def config_mac_aging_time(device, bridge_domain, aging_time):
    """ Config mac-aging time under bridge domain

        Args:
            device (`obj`): device object
            bridge_domain (`int`): bridge domain id
            aging_time (`int`): mac aging-time
        Return:
            None
        Raises:
            SubCommandFailure: Failed configuring device
    """
    log.info(
        "Configuring mac aging-time to {} seconds under "
        "bridge domain {}".format(aging_time, bridge_domain)
    )
    try:
        device.configure(
            [
                "bridge-domain {}".format(bridge_domain),
                "mac aging-time {}".format(aging_time),
            ]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure aging time under bridge domain {bridge_domain}".format(
                bridge_domain=bridge_domain
            )
        )


def unconfig_mac_aging_time(device, bridge_domain):
    """ Unconfig mac-aging time under bridge domain

        Args:
            device (`obj`): device object
            bridge_domain (`int`): bridge domain id
        Return:
            None
        Raises:
            SubCommandFailure: Failed configuring device
    """
    log.info(
        "Removing mac aging-time configuration under "
        "bridge domain {}".format(bridge_domain)
    )
    try:
        device.configure(
            ["bridge-domain {}".format(bridge_domain), "no mac aging-time"]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not unconfigure aging time under bridge domain {bridge_domain}".format(
                bridge_domain=bridge_domain
            )
        )


def config_mac_learning(device, bridge_domain):
    """ Config mac learning under bridge domain

        Args:
            device (`obj`): device object
            bridge_domain (`int`): bridge domain id
        Return:
            None
        Raises:
            SubCommandFailure: Failed configuring device
    """
    log.info(
        "Configuring mac learning under bridge domain {}".format(bridge_domain)
    )
    try:
        device.configure(
            ["bridge-domain {}".format(bridge_domain), "mac learning"]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure mac learning under bridge domain {bridge_domain}".format(
                bridge_domain=bridge_domain
            )
        )


def unconfig_mac_learning(device, bridge_domain):
    """ Unconfig mac learning under bridge domain

        Args:
            device (`obj`): device object
            bridge_domain (`int`): bridge domain id
        Return:
            None
        Raises:
            SubCommandFailure: Failed configuring device
    """
    log.info(
        "Removing mac learning under bridge domain {}".format(bridge_domain)
    )
    try:
        device.configure(
            ["bridge-domain {}".format(bridge_domain), "no mac learning"]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not unconfigure mac learning under bridge domain {bridge_domain}".format(
                bridge_domain=bridge_domain
            )
        )
def configure_mac_address_table_aging(device, aging_time):
    """ Config mac-aging time on device
        Args:
            device (`obj`): device object
            aging_time (`int`): mac aging-time
        Return:
            None
        Raises:
            SubCommandFailure: Failed configuring device
    """
    try:
        device.configure(f'mac address-table aging-time {aging_time}')
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure aging time"
            ) 

def configure_mac_global_address_table_static(device, mac, vlan, interface=None):
    """Configure address-table static under global mac on this device
        Args:
            device ('obj'): Device object
            mac ('str'): 48 bit mac address
            vlan ('int'): vlan id
            interface ('str',optional): interface
        Returns:
                None
        Raises:
                SubCommandFailure
    """

    if interface:
        cmd = f'mac address-table static {mac} vlan {vlan} interface {interface}'
    else:
        cmd = f'mac address-table static {mac} vlan {vlan} drop'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure address-table static under global mac on this device. Error:\n{e}")

def unconfigure_mac_global_address_table_static(device, mac, vlan, interface=None):
    """Unconfigure address-table static under global mac on this device
        Args:
            device ('obj'): Device object
            mac ('str'): 48 bit mac address
            vlan ('int'): vlan id
            interface ('str',optional): interface
        Returns:
                None
        Raises:
                SubCommandFailure
    """

    if interface:
        cmd = f'no mac address-table static {mac} vlan {vlan} interface {interface}'
    else:
        cmd = f'no mac address-table static {mac} vlan {vlan} drop'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure address-table static under global mac on this device. Error:\n{e}")

def configure_mac_global_address_table_notification_change(device, change_option="", size=None, interval=None):
    """Configure address-table notification change under global mac on this device
        Args:
            device ('obj'): Device object
            change_option ('str',optional): change option history-size/interval
            size ('int',optional): Number of MAC notifications to be stored
            interval ('int',optional): Interval between the MAC notifications
        Returns:
                None
        Raises:
                SubCommandFailure
    """

    if change_option.lower()== "history-size":
        cmd = f'mac address-table notification change history-size {size}'
    elif change_option.lower()== "interval":
        cmd = f'mac address-table notification change interval {interval}'
    else:
        cmd = 'mac address-table notification change'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure address-table notification change under global mac on this device. Error:\n{e}")

def unconfigure_mac_global_address_table_notification_change(device, change_option="", size=None, interval=None):
    """Unconfigure address-table notification change under global mac on this device
        Args:
            device ('obj'): Device object
            change_option ('str',optional): change option history-size/interval
            size ('int',optional): Number of MAC notifications to be stored
            interval ('int',optional): Interval between the MAC notifications
        Returns:
                None
        Raises:
                SubCommandFailure
    """

    if change_option.lower()== "history-size":
        cmd = f'no mac address-table notification change history-size {size}'
    elif change_option.lower()== "interval":
        cmd = f'no mac address-table notification change interval {interval}'
    else:
        cmd = 'no mac address-table notification change'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure address-table notification change under global mac on this device. Error:\n{e}")

def configure_mac_address_table_notification_change(device,change_option="",size=None,interval=None):
    """Configure mac-address-table notification change on this device
        Args:
            device ('obj'): Device object
            change_option ('str',optional): change option history-size/interval
            size ('int',optional): Number of MAC notifications to be stored
            interval ('int',optional): Interval between the MAC notifications
        Returns:
                None
        Raises:
                SubCommandFailure
    """

    if change_option.lower()== "history-size":
        cmd = f'mac-address-table notification change history-size {size}'
    elif change_option.lower()== "interval":
        cmd = f'mac-address-table notification change interval {interval}'
    else:
        cmd = 'mac-address-table notification change'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure mac-address-table notification change on this device. Error:\n{e}")

def unconfigure_mac_address_table_notification_change(device,change_option="",size=None,interval=None):
    """Unconfigure mac-address-table notification change on this device
        Args:
            device ('obj'): Device object
            change_option ('str',optional): change option history-size/interval
            size ('int',optional): Number of MAC notifications to be stored
            interval ('int',optional): Interval between the MAC notifications
        Returns:
                None
        Raises:
                SubCommandFailure
    """

    if change_option.lower()== "history-size":
        cmd = f'no mac-address-table notification change history-size {size}'
    elif change_option.lower()== "interval":
        cmd = f'no mac-address-table notification change interval {interval}'
    else:
        cmd = 'no mac-address-table notification change'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure mac-address-table notification change on this device. Error:\n{e}")

def configure_default_mac_global_address_table_notification_change(device,change_option="",size=None,interval=None):
    """Configure default address-table notification change under global mac on this device
        Args:
            device ('obj'): Device object
            change_option ('str',optional): change option history-size/interval
            size ('int',optional): Number of MAC notifications to be stored
            interval ('int',optional): Interval between the MAC notifications
        Returns:
                None
        Raises:
                SubCommandFailure
    """
    if change_option.lower()== "history-size":
        cmd = f'default mac address-table notification change history-size {size}'
    elif change_option.lower()== "interval":
        cmd = f'default mac address-table notification change interval {interval}'
    else:
        cmd = 'default mac address-table notification change'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure default address-table notification change under global mac on this device. Error:\n{e}")

def configure_mac_address_table_learning(device, vlan_id):
    """ Config mac-learning on device
        Args:
            device (`obj`): device object
            vlan_id (`int`): vlan id 
        Return:
            None
        Raises:
            SubCommandFailure 
    """
    try:
        device.configure(f'mac address-table learning vlan {vlan_id}')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure the mac address-table learning vlan. Error:\n{error}".format(error=e)
        )

def unconfigure_mac_address_table_learning(device, vlan_id):
    """ Unconfig mac-learning on device
        Args:
            device (`obj`): device object
            vlan_id (`int`): vlan id 
        Return:
            None
        Raises:
            SubCommandFailure 
    """
    try:
        device.configure(f'no mac address-table learning vlan {vlan_id}')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure the mac address-table learning vlan. Error:\n{error}".format(error=e)
        )

def configure_mac_address_table_aging_default(device, aging, vlan_id=1):
    """ Config mac-aging time default on device
        Args:
            device (`obj`): device object
            aging (`str`,`int`): mac aging-time
            ex:)
                <0-0>         Enter 0 to disable aging
                <10-1000000>  Enter aging-time
                routed-mac    Set RM Aging interval
                vlan          VLAN Keyword
                <cr>          <cr>
            vlan_id (`int`): Vlan number for aging-time option vlan (keeping default as vlan 1)

        Return:
            None
        Raises:
            SubCommandFailure: Failed configuring device
    """
    if aging == "routed-mac":
        cmd = 'default mac address-table aging-time routed-mac'
    elif aging == "vlan":
        cmd = f'default mac address-table aging-time vlan {vlan_id}'
    else:
        cmd = f'default mac address-table aging-time {aging}'

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure default mac address-table aging . Error:\n{error}".format(error=e)
            ) 

def configure_mac_address_table_static(device, mac_address, vlan_number, interface):
    """ 
    API for the CLI :- 
        mac address-table static {mac_address,} vlan {vlan_number} interface {interface}
        e.g.
        Args:
            device ('obj'): Device object
            mac_address('str'): MAC address
            vlan_number('int'): Vlan ID number
            interface('str'): interface name
        Return:
            None
        Raise:
            SubCommandFailure
    """
    cmd = f"mac address-table static {mac_address} vlan {vlan_number} interface {interface}"
    try:
        output = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure mac address table on device {device} . Error:\n{e}")

def unconfigure_mac_address_table_static(device, mac_address, vlan_number, interface):
    """ 
    API for the CLI :- 
        no mac address-table static {MAC_Address} vlan {vlan_ID_number} interface {interface}
        e.g.
        Args:
            device ('obj'): Device object
            mac_address('str'): MAC address
            vlan_number('int'): Vlan ID number
            interface('str'): interface name
        Return:
            None
        Raise:
            SubCommandFailure
    """
    cmd = f"no mac address-table static {mac_address} vlan {vlan_number} interface {interface}"
    try:
        output = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure mac address table on device {device} . Error:\n{e}")
