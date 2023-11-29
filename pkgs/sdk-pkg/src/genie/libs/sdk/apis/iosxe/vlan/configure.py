"""Common configure functions for vlan"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def config_vlan(device, vlanid):
    """ Configures a VLAN on Interface or Device
    e.g.
    vlan 666

        Args:
            device (`obj`): Device object
            vlanid (`str`): Vlan id
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    configs = []
    configs.append("vlan {vlanid}".format(vlanid=vlanid))
    configs.append("no shutdown")
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure vlan {vlanid}, Error: {error}'.format(
                vlanid=vlanid, error=e)
        )

def config_ip_on_vlan(device, vlan_id, ipv4_address=None,
                      subnetmask=None, ipv6_address=None,
                      ipv6_prefix_len=None, secondary=False):
    """Configure an IPv4/IPv6 address on a vlan

        Args:
            device (`obj`): Device object
            vlan_id (`str`): Vlan id
            ipv4_address (`str`): IPv4 address
            subnetmask (`str`): Subnet mask to be used for IPv4 address
            ipv6_address (`str`): Ipv6 address
            ipv6_prefix_len (`int`): length of IPv6 prefix
            seconday ('bool'): True/False
        Return:
            None
        Raise:
            SubCommandFailure: Failed to configure Ipv4/Ipv6 address on vlan
    """

    try:
        if ipv4_address and subnetmask:
            if secondary:
                device.configure([f'interface vlan {vlan_id}',
                            f'ip address {ipv4_address} {subnetmask} secondary'])
            else:
                device.configure([f'interface vlan {vlan_id}',
                            f'ip address {ipv4_address} {subnetmask}'])

        if ipv6_address and ipv6_prefix_len:
            device.configure([f'interface vlan {vlan_id}',
                            'ipv6 enable',
                            f'ipv6 address {ipv6_address}/{ipv6_prefix_len}'])

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure Ipv4/Ipv6 address on vlan {vlan_id}, '
            f'Error: {e}'
        )

def unconfig_ip_on_vlan(device, vlan_id, ipv4_address=None,
                      subnetmask=None, ipv6_address=None,
                      ipv6_prefix_len=None,secondary=False):
    """unconfigures an IPv4/IPv6 address on a vlan

        Args:
            device (`obj`): Device object
            vlan_id (`str`): Vlan id
            ipv4_address (`str`): IPv4 address
            subnetmask (`str`): Subnet mask to be used for IPv4 address
            ipv6_address (`str`): Ipv6 address
            ipv6_prefix_len (`int`): length of IPv6 prefix
            secondary ('bool'): True/False
        Return:
            None
        Raise:
            SubCommandFailure: Failed to unconfigure Ipv4/Ipv6 address on vlan
    """

    try:
        if ipv4_address and subnetmask:
            if secondary:
                device.configure([f'interface vlan {vlan_id}',
                            f'no ip address {ipv4_address} {subnetmask} secondary'])
            else:
                device.configure([f'interface vlan {vlan_id}',
                            f'no ip address {ipv4_address} {subnetmask}'])

        if ipv6_address and ipv6_prefix_len:
            device.configure([f'interface vlan {vlan_id}',
                            f'no ipv6 address {ipv6_address}/{ipv6_prefix_len}'])

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not unconfigure Ipv4/Ipv6 address on vlan {vlan_id}, '
            f'Error: {e}'
        )

def unconfig_vlan(device, vlanid):
    """ vlan on Interface or Device configuration removal

        Args:
            device (`obj`): Device object
            vlanid (`str`): Vlan id
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    try:
        device.configure("no vlan {vlanid}".format(vlanid=vlanid))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not remove vlan {vlanid}, Error: {error}'.format(
                vlanid=vlanid, error=e)
        )

def config_vlan_tag_native(device):
    """ Configure vlan dot1q tag native

        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring device
    """

    try:
        device.configure("vlan dot1q tag native")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure vlan dot1q tag native, Error: {error}'.format(
                error=e)
        )

def configure_vlan_vpls(device, vlanid):
    """ Config vpls on vlan

        Args:
            device (`obj`): Device object
            vlanid (`str`): Vlan id
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """

    try:
        device.configure(
            [
                "vlan configuration {vlanid}".format(vlanid=vlanid),
                "member vfi vpls",
                "vlan dot1q tag native",
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure vpls on vlan {vlanid}, Error: {error}'.format(
                vlanid=vlanid, error=e)
        )


def configure_vtp_mode(device,mode):
    """ Configures global VTP mode
        Args:
            device ('obj'): device to use
            mode ('str'):  VTP mode (i.e transparent, client, server)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure('vtp mode {mode}'.format(mode=mode))
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure VTP mode'
        )

def configure_pvlan_svi_mapping(device, svi_vlan, mapping_vlan):
    """ Configures Private Vlan Mapping on SVI
        Args:
            device ('obj'): device to use
            svi_vlan ('str'): SVI interface
            mapping_vlan ('str'): Private vlan to map to
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    # Initialize list variable
    config_list = []
    config_list.append("interface {svi_vlan}".format(svi_vlan=svi_vlan))
    config_list.append("private-vlan mapping {mapping_vlan}".format(mapping_vlan=mapping_vlan))

    try:
        device.configure(config_list)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure PVLAN-mapping'
        )


def configure_pvlan_primary(device, primary_vlan, secondary_vlan=None):
    """ Configures Primary Private Vlan
        Args:
            device ('obj'): device to use
            primary_vlan ('str'): Primary private vlan
            secondary_vlan ('str',optional): Secondary isolated/community vlan
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    config_list = []
    # vlan 100
    # private-vlan primary
    config_list.append("vlan {primary_vlan} \n"
                       "private-vlan primary".format(primary_vlan=primary_vlan))
    # private-vlan association 101
    if secondary_vlan != None:
        config_list.append("private-vlan association {secondary_vlan}".format(secondary_vlan=secondary_vlan))

    try:
        device.configure(config_list)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure Primary Pvlan'
        )

def configure_access_vlan(device , vlanid, interface):
    """ configuring access vlan configuration on interface
        Args:
            device (`obj`): Device object
            vlanid ('int') : vlan id
            interface ('str) : interface name
        Returns:
            Bool
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
                    [f"int {interface}",
                    "switchport mode access",
                    f"switchport access vlan {vlanid}",
                    "no shutdown"
                    ]
                )
        return True
    except SubCommandFailure as e:
        log.error("Unable to configure vlan {}, Error:\n{}".format(vlanid, e))
        raise SubCommandFailure(
            'Could not create access on vlan {vlanid}, Error: {error}'.format(vlanid, e)
            )


def configure_pvlan_type(device,vlan,pvlan_type):
    """ Configures Isolated Private Vlan
        Args:
            device ('obj'): device to use
            vlan ('str'): Vlan id
            pvlan_type ('str'): Private vlan type (i.e isolated, primary, community)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    # Initialize list variable
    config_list = []
    config_list.append("vlan {vlan}".format(vlan=vlan))
    config_list.append("private-vlan {pvlan_type}".format(pvlan_type=pvlan_type))

    try:
        device.configure(config_list)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure Primary Pvlan'
        )

def config_vlan_range(device, vlanid_start, vlanid_end, timeout=None):
    """ Configures a VLAN on Device
        e.g.
        vlan 1 - 4094

        Args:
            device (`obj`): Device object
            vlanid_start (`int`): Vlan id start
            vlanid_end (`int`): Vlan id end
            timeout(int, optional): provide the time out time

        Return:
            None
        Raise:
            SubCommandFailure
    """
    configs = []
    configs.append(f"vlan {vlanid_start}-{vlanid_end}")
    configs.append("no shutdown")
    try:
        if timeout:
            device.configure(configs, timeout=timeout)
        else:
            device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure vlan on device. Error:\n{e}"
        )

def unconfig_vlan_range(device, vlanid_start, vlanid_end, timeout=None):
    """ Unconfigures a VLAN on Device
        e.g.
        no vlan 1 - 4094

        Args:
            device (`obj`): Device object
            vlanid_start (`int`): Vlan id start
            vlanid_end (`int`): Vlan id end
            timeout(int, optional): provide the time out time

        Return:
            None
        Raise:
            SubCommandFailure
    """
    configs = []
    configs.append(f"no vlan {vlanid_start}-{vlanid_end}")
    try:
        if timeout:
            device.configure(configs, timeout=timeout)
        else:
            device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure vlan on device. Error:\n{e}"
        )

def unconfig_vlan_tag_native(device):
    """ Unconfigure vlan dot1q tag native

        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring device
    """

    try:
        device.configure("no vlan dot1q tag native")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not remove vlan dot1q tag native, Error: {error}'.format(
                error=e)
        )

def configure_vlan_shutdown(device, vlanid):
    """ Shutdown a VLAN on Interface or Device
    e.g.
    vlan 666
	  shutdown

        Args:
            device (`obj`): Device object
            vlanid (`str`): Vlan id
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    configs = ["vlan {vlanid}".format(vlanid=vlanid), "shutdown"]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not shutdown vlan {vlanid}, Error: {error}'.format(
                vlanid=vlanid, error=e)
        )

def unconfigure_vlan_configuration(device, vlanid):
    """ Unconfigure vlan configuration
        Args:
            device (`obj`): Device object
            vlanid (`str`): Vlan id
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    try:
        device.configure("no vlan configuration {vlanid}".format(vlanid=vlanid))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not remove vlan configuration {vlanid}, Error: {error}'.format(
                vlanid=vlanid, error=e)
        )

def unconfigure_vlan_vpls(device, vlanid):
    """ Unconfig vpls on vlan
        Args:
            device (`obj`): Device object
            vlanid (`str`): Vlan id
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """

    try:
        device.configure([
            "no vlan configuration {vlanid}".format(vlanid=vlanid),
            "no vlan dot1q tag native"])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not unconfigure vpls on vlan {vlanid}, Error: {error}'.format(
                vlanid=vlanid, error=e)
        )

def configure_private_vlan_on_vlan(device, vlan1, vlan2):

    """ configure switchport mode trunk to the interface
        Args:
            device (`obj`): Device object
            vlan1 (`str`): vlan to be added to the port
            vlan2 (`str`): vlan to be added to the port
        Returns:
            None
    """
    log.debug("Configuring private vlan on VLAN")

    try:
        device.configure(
            [
                f"vlan {vlan1}",
                "private-vlan isolated",
                f"vlan {vlan2}",
                "private-vlan primary",
                f"private-vlan association {vlan1}",
            ]
        )

    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure private vlan on {vlan1} {vlan2}. Error:\n{e}")


def configure_flow_monitor_vlan_configuration(device, vlan, monitor_name, sampler_name, direction):

    """ configure flow monitor under vlan configuration
        Args:
            device ('obj'):       Device object
            vlan ('str'):         vlan to be added to the port
            monitor_name ('str'): Name of the flow monitor to be configured
            sampler_name ('str'): Name of the sampler to be configured
            direction ('str'):    Direction to be configured(input/output)

        Returns:
            None
    """
    log.debug("Configuring flow monitor under vlan configuration")

    cmd = [f"vlan configuration {vlan}",
           f"ip flow monitor {monitor_name} sampler {sampler_name} {direction}"]
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure flow monitor on vlan {vlan}. Error:\n{e}")


def unconfigure_flow_monitor_vlan_configuration(device, vlan, monitor_name, sampler_name, direction):

    """ unconfigure flow monitor under vlan configuration
        Args:
            device ('obj'):       Device object
            vlan ('str'):         vlan to be added to the port
            monitor_name ('str'): Name of the flow monitor to be configured
            sampler_name ('str'): Name of the sampler to be configured
            direction ('str'):    Direction to be configured(input/output)

        Returns:
            None
    """
    log.debug("Unconfiguring flow monitor under vlan configuration")

    cmd = [f"vlan configuration {vlan}",
           f"no ip flow monitor {monitor_name} sampler {sampler_name} {direction}"]
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure flow monitor on vlan {vlan}. Error:\n{e}")

def configure_ethernet_vlan_unlimited(device, subslot):
    """ Configure ethernet vlan unlimited on subslot
        Args:
            device ('obj'): device to use
            subslot ('str'): subslot to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ethernet vlan unlimited
    """

    cmd = f"hw-module subslot {subslot} ethernet vlan unlimited"

    log.info(f"Configuring ethernet vlan unlimited on subslot {subslot}")
    try:
        device.configure(cmd)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to configure ethernet vlan unlimited"
        )

def unconfigure_ethernet_vlan_unlimited(device, subslot):
    """ Unconfigure ethernet vlan unlimited on subslot
        Args:
            device ('obj'): device to use
            subslot ('str'): subslot to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to ubconfigure ethernet vlan unlimited
    """

    cmd = f"no hw-module subslot {subslot} ethernet vlan unlimited"

    log.info(f"Unconfiguring ethernet vlan unlimited on subslot {subslot}")
    try:
        device.configure(cmd)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to unconfigure ethernet vlan unlimited"
        )

def configure_vtp_domain(device, vtp_domain):
    """Configure vtp domain on the device

        Args:
            device ('obj'): device to use
            vtp_domain ('str'): vtp domain name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure VTP domain
    """
    cmd = f"vtp domain {vtp_domain}"

    try:
        device.configure(cmd)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to configure VTP domain"
        )

def configure_vtp_version(device, vtp_version):
    """Configure vtp domain on the device

        Args:
            device ('obj'): device to use
            vtp_version('int'): vtp version
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure VTP version
    """
    cmd = f"vtp version {vtp_version}"

    try:
        device.configure(cmd)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to configure VTP version"
        )

def unconfigure_vtp_version(device):
    """Unconfigure vtp version on the device
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure VTP version
    """
    cmd = ("no vtp version")

    try:
        device.configure(cmd)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to unconfigure VTP version"
        )

def configure_interface_vtp(device, interface):
    """Configure vtp on a interface

    Args:
        device ('obj'): device to use
        interface ('str') : interface to add configs
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure VTP on interface
    """
    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append('vtp')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure vtp on interface {interface}. Error:\n{e}")

def unconfigure_interface_vtp(device, interface):
    """Unconfigure vtp on a interface

    Args:
        device ('obj'): device to use
        interface ('str') : interface to add configs
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure VTP on interface
    """
    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append('no vtp')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure vtp on interface {interface}. Error:\n{e}")

def configure_switchport_trunk_allowed_vlan_remove(device, interface, number):
    """Configure switchport trunk allowed vlan remove

    Args:
        device ('obj'): device to use
        interface ('str') : interface to add configs
        number ('int'): vlan id of disallowed vlans when this port is in trunking mode

        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure VTP on interface
    """
    cmd = [
        f"interface {interface}",
        f"switchport trunk allowed vlan remove {number}"
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure switchport trunk allowed vlan remove on this device. Error:\n{e}")

def configure_switchport_trunk_allowed_vlan_except(device, interface, number):
    """Configure switchport trunk allowed vlan except

    Args:
        device ('obj'): device to use
        interface ('str') : interface to add configs
        number ('int'): vlan id of disallowed vlans when this port is in trunking mode

        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure VTP on interface
    """
    cmd = [
        f"interface {interface}",
        f"switchport trunk allowed vlan except {number}"
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to switchport trunk allowed vlan except on this device. Error:\n{e}")

def configure_interface_port_channel(device,
channel_number, mapping_number, mapping_value):
    """ Get interface members
        Args:
            device ('obj'): Device object
            channel_number ('int') : channel number of interface range  <1-128>
            mapping_number ('int') : mapping number
            mapping_value ('int') : mapping value
        Returns:
            interface members
        Raises:
            None
    """
    cmd = [f'interface port-channel {channel_number}',
     f'switchport private-vlan mapping {mapping_number} {mapping_value}']

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure port channel on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def unconfigure_interface_port_channel(
    device, channel_number,
    mapping_number, mapping_value):
    """ Get interface members
        Args:
            device ('obj'): Device object
            channel_number ('int') : channel number of interface
            mapping_number ('int') : mapping number
            mapping_value ('int') : mapping value
        Returns:
            interface members
        Raises:
            None
    """
    cmd = [f'interface port-channel {channel_number}',
    f'no switchport private-vlan mapping {mapping_number} {mapping_value}']

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure port channel on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_default_switchport_trunk_vlan(device, interface):
    """ Get interface members
        Args:
            device ('obj'): Device object
            interface ('str'): interface to search member for
        Returns:
            interface members
        Raises:
            None
    """
    cmd = [f'interface {interface}',
    f'default switchport trunk native vlan']

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure switchport trunk vlan on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def unconfigure_default_switchport_trunk_vlan(device, interface):
    """ Get interface members
        Args:
            device ('obj'): Device object
            interface ('str'): interface to search member for
        Returns:
            interface members
        Raises:
            None
    """
    cmd = [f'interface {interface}',
    f'default switchport trunk native vlan']

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure switchport trunk vlan on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_vlan_state_suspend(device,
interface, vlan, state1):
    """ Get interface members
        Args:
            device ('obj'): Device object
            interface ('str'): interface to search member for
            vlan ('str'): vlan 100
		    state ('str') : in which state
        Returns:
            interface members
        Raises:
            Nonel
    """
    cmd = [f'interface {interface}',
    f'vlan {vlan}', f'state {state1}']

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure vlan state suspend on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def unconfigure_vlan_state_suspend(device,
interface, vlan, state1):
    """ Get interface members
        Args:
            device ('obj'): Device object
            interface ('str'): interface to search member for
            vlan ('str'): vlan 100
		    state ('str') : in which state
        Returns:
            interface members
        Raises:
            Nonel
    """
    cmd = [f'interface {interface}',
    f'vlan {vlan}', f'state {state1}']

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure vlan state suspend on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_vlan_state_active(device,
interface, vlan, state):
    """ Get interface members
        Args:
            device ('obj'): Device object
            interface ('str'): interface to search member for
            vlan ('str'): vlan 100
		    state ('str') : in which state
        Returns:
            interface members
        Raises:
            Nonel
    """
    cmd = [f'interface {interface}',
    f'vlan {vlan}', f'state {state}']

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure vlan state active on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def unconfigure_vlan_state_active(device,
interface, vlan, state):
    """ Get interface members
        Args:
            device ('obj'): Device object
            interface ('str'): interface to search member for
            vlan ('str'): vlan 100
		    state ('str') : in which state
        Returns:
            interface members
        Raises:
            Nonel
    """
    cmd = [f'interface {interface}',
    f'vlan {vlan}', f'state {state}']

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure vlan state active on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )
def configure_vtp_password(device, vtp_password):
    """Configure vtp password on the device

        Args:
            device ('obj'): device to use
            vtp_password('str'): vtp password
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure VTP password
    """
    cmd = f"vtp password {vtp_password}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure vtp password on device {device}. Error:\n{e}")

def unconfigure_vtp_password(device, vtp_password):
    """unconfigure vtp password on the device

        Args:
            device ('obj'): device to use
            vtp_password('str'): vtp password
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure VTP password
    """
    cmd = f"no vtp password {vtp_password}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure vtp password on device {device}. Error:\n{e}")

def configure_interface_vlan_priority(device, vlan_id, priority):
    """
        Args:
            device ('obj'): Device object
            vlan_id ('int') : <1-4094>  Vlan interface id
            priority ('int') : <50-200>  Vlan interface priority
        Returns:
            None
        Raises:
            SubcommandFailure: Failed executing command
    """
    log.debug("interface vlan {vlan_id}".format(vlan_id=vlan_id))
    configs = []
    configs.append("interface vlan {vlan_id}".format(vlan_id=vlan_id))
    configs.append("standby {vlan_id} priority {priority}".format(vlan_id=vlan_id, priority=priority))
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not set the vlan {vlan_id} priority {priority} on {device}. Error:\n{error}".format(
                vlan_id=vlan_id, priority=priority, device=device, error=e
            )
        )  

def configure_interface_vlan_range_priority(device, vlan_id_from, vlan_id_to, stby_value, priority):
    """
        Args:
            device ('obj'): Device object
            vlan_id_from ('int') : <1-4094>  Vlan interface vlan_id_from
            vlan_id_to ('int') : <1-4094>  Vlan interface vlan_id_to
            stby_value ('int') : value after stanby (Ex. : 0)
            priority ('int') : <50-200>  Vlan interface priority
        Returns:
            None
        Raises:
            SubcommandFailure: Failed executing command
    """

    log.debug("interface range vlan {vlan_id_from}-{vlan_id_to}".format(vlan_id_from=vlan_id_from,vlan_id_to=vlan_id_to))
    configs = []
    configs.append("interface range vlan {vlan_id_from}-{vlan_id_to}".format(vlan_id_from=vlan_id_from, vlan_id_to=vlan_id_to))
    configs.append("standby {stby_value} priority {priority}".format(stby_value=stby_value, priority=priority))
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not set the vlan range {vlan_id_from}-{vlan_id_to} priority {priority} on {device}. Error:\n{error}".format(
                vlan_id_from=vlan_id_from, vlan_id_to=vlan_id_to, priority=priority, device=device, error=e
            )
        )  

def configure_switchport_trunk_pruning_vlan_except(device, interface, string):
    """Configure switchport trunk pruning vlan except
        Example: interface gigabitEthernet2/0/1
                switchport trunk pruning vlan except 1,9,1002-1005
    Args:
        device ('obj'): device to use
        interface ('str') : interface to add configs
        string ('str'): WORD VLAN IDs of disallowed VLANS when this port is in trunking mode
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    log.info(f"configuring switchport trunk pruning vlan on {device.name}")
    cmd = [
           f'interface {interface}',
           f'switchport trunk pruning vlan except {string}'
        ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure switchport trunk pruning on this device. Error:\n{e}")

def configure_vtp_trunk_interface(device, interface):
    """ Configures global VTP trunk interface
        Example: vtp trunk gig2/0/2
    Args:
        device ('obj'): device to use
        interface ('str'):  interface to configure
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    log.info(f"configuring vtp trunk on {device.name} {interface}")
    cmd = f'vtp trunk {interface}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure VTP trunk interface. Error:\n{e}')


def configure_vlan_group_list(device, group_name, vlan):
    """ Configures vlan group list
        Args:
            device ('obj'): device to use
            group_name ('str'):  Vlan group name
            vlan ('str'): vlan numbers. Ex: '1', '4-9', '4,19,54'
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f'vlan group {group_name} vlan-list {vlan}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure vlan group list. Error:\n{e}')


def unconfigure_vlan_group_list(device, group_name, vlan):
    """ Unconfigures vlan group list
        Args:
            device ('obj'): device to use
            group_name ('str'):  Vlan group name
            vlan ('str'): vlan numbers. Ex: '1', '4-9', '4,19,54'
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f'no vlan group {group_name} vlan-list {vlan}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure vlan group list. Error:\n{e}')

def configure_default_vtp_version(device):
    """ Configure default vtp version
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f'default vtp version'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure default vtp version. Error:\n{e}')
    
def configure_vlan_name(device,vlan,name):
    """ Configure vlan name
        Args:
            device ('obj'): device to use
            vlan ('str): vlan number 
            name ('str): name of the vlan
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f'vlan {vlan}',f'name {name}']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure the vlan name. Error:\n{e}')

def unconfigure_pvlan_primary(device, primary_vlan, secondary_vlan=None):
    """ Unconfigures Primary Private Vlan
        Args:
            device ('obj'): device to use
            primary_vlan ('str'): Primary private vlan
            secondary_vlan ('str',optional): Secondary isolated/community vlan
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    config = [f"vlan {primary_vlan}", "no private-vlan primary"]
    if secondary_vlan:
        config.append(f"no private-vlan association {secondary_vlan}")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not unconfigure Primary Pvlan. Error:\n{e}'
        )

def unconfigure_pvlan_type(device, vlan, pvlan_type):
    """ unconfigures Isolated/community Private Vlan
        Args:
            device ('obj'): device to use
            vlan ('str'): Vlan id
            pvlan_type ('str'): Private vlan type (i.e isolated, primary, community)
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    config = [f"vlan {vlan}", f"no private-vlan {pvlan_type}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure private-vlan. Error:\n{e}')

def configure_vtp_pruning(device):
    """ Configure vtp pruning
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f'vtp pruning'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure vtp pruning. Error:\n{e}')
    
def unconfigure_vtp_pruning(device):
    """ Unconfigure vtp pruning
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f'no vtp pruning'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure no vtp pruning. Error:\n{e}')
        
def configure_switchport_trunk_pruning_vlan(device, interface, pruning_vlan):
    """ Configure switchport trunk pruning vlan
        Args:
            device ('obj'): device to use
            interface ('str'): interface name
            pruning_vlan ('str'): pruning vlan
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f'interface {interface}',f'switchport trunk pruning vlan {pruning_vlan}']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure switchport trunk pruning vlan. Error:\n{e}')

def unconfigure_switchport_trunk_pruning_vlan(device, interface, pruning_vlan):
    """ Unconfigure switchport trunk pruning vlan
        Args:
            device ('obj'): device to use
            interface ('str'): interface name
            pruning_vlan ('str'): pruning vlan            
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f'interface {interface}',f'no switchport trunk pruning vlan {pruning_vlan}']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure no switchport trunk pruning vlan. Error:\n{e}')

def unconfigure_vtp_mode(device, mode):
    """ Unconfigures global VTP mode
        Args:
            device ('obj'): device to use
            mode ('str'):  VTP mode (i.e transparent, client, server)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f'no vtp mode {mode}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure no vtp mode. Error:\n{e}')

def configure_shutdown_vlan_interface_range(device, vlan_id_from, vlan_id_to):
    """
        Args:
            device ('obj'): Device object
            vlan_id_from ('int') : <1-4094>  Vlan interface number staring from
            vlan_id_to ('int') : <1-4094>  Vlan interface number end to
        Returns:
            None
        Raises:
            SubcommandFailure: Failed executing command
    """

    log.debug("interface range vlan {vlan_id_from}-{vlan_id_to}".format(vlan_id_from=vlan_id_from, vlan_id_to=vlan_id_to))
    configs = []
    configs.append("interface range vlan {vlan_id_from}-{vlan_id_to}".format(vlan_id_from=vlan_id_from, vlan_id_to=vlan_id_to))
    configs.append("shutdown")
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not shut the vlan range {vlan_id_from}-{vlan_id_to} on {device}. Error:\n{error}".format(
                vlan_id_from=vlan_id_from,vlan_id_to=vlan_id_to,device=device, error=e
            )
        ) 


def configure_no_shutdown_vlan_interface_range(device, vlan_id_from, vlan_id_to):
    """
        Args:
            device ('obj'): Device object
            vlan_id_from ('int') : <1-4094>  Vlan interface number staring from
            vlan_id_to ('int') : <1-4094>  Vlan interface number end to
        Returns:
            None
        Raises:
            SubcommandFailure: Failed executing command
    """
    log.debug("interface range vlan {vlan_id_from}-{vlan_id_to}".format(vlan_id_from=vlan_id_from, vlan_id_to=vlan_id_to))
    configs = []
    configs.append("interface range vlan {vlan_id_from}-{vlan_id_to}".format(vlan_id_from=vlan_id_from, vlan_id_to=vlan_id_to))
    configs.append("no shutdown")
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not shut the vlan range {vlan_id_from}-{vlan_id_to} on {device}. Error:\n{error}".format(
                vlan_id_from=vlan_id_from,vlan_id_to=vlan_id_to,device=device, error=e
            )
        ) 