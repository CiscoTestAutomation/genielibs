"""Common configure functions for dhcp"""
# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

log = logging.getLogger(__name__)


def create_dhcp_pool(
    device, pool_name, network, mask, router_id,lease_days,lease_hrs,lease_mins
):
    """ Create DHCP pool
        Args:
            device ('obj'): device to use
            pool_name ('str'): name of the pool to be created
            network ('str'): IP of the network pool
            mask ('str'): Subnet mask of the network pool
            router_id ('str'): Default router ID
            lease_days ('str'): Number of days for the lease
            lease_hrs ('str'): Number of hours for the lease
            lease_mins ('str'): Number of minutes for the lease
        Returns:
            None
        Raises:
            SubCommandFailure: Failed creating dhcp pool
    """
    log.info(
        "Configuring DHCP pool with name={}, network={}, mask={}, and "
        "Router ID {} Lease Time days={},hrs={},mins={}".format(pool_name, network, mask, router_id,lease_days,lease_hrs,lease_mins)
    )

    try:
        device.configure(
            [
            "ip dhcp pool {}".format(pool_name),
	    "network {} {}".format(network,mask),
            "default-router {}".format(router_id),
            "lease {} {} {}".format(lease_days,lease_hrs,lease_mins)
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure DHCP pool {pool_name}".format(
                pool_name=pool_name
            )
        )

def remove_dhcp_pool(
    device, pool_name
):
    """ Remove DHCP pool
        Args:
            device ('obj'): device to use
            pool_name ('str'): name of the pool to be created
        Returns:
            None
        Raises:
            SubCommandFailure: Failed removing dhcp pool
    """
    log.info(
        "Removing DHCP pool with name={}".format(pool_name)
    )

    try:
        device.configure(
            [
            "no ip dhcp pool {}".format(pool_name),
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove DHCP pool {pool_name}".format(
                pool_name=pool_name
            )
        )

def enable_dhcp_snooping_glean(device):
    """ Enable DHCP snooping glean globally
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring DHCP snooping glean
    """
    log.info("Enabling DHCP snooping glean globally")
    try:
        device.configure("ip dhcp snooping glean")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable DHCP snooping glean Error: {error}".format(
                error=e)
        )


def disable_dhcp_snooping_glean(device):
    """ Disable DHCP snooping glean globally
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed disabling DHCP snooping glean globally
    """
    log.info("Disabling DHCP snooping glean globally")
    try:
        device.configure("no ip dhcp snooping glean")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disable DHCP snooping glean globally Error: {error}".format(
                error=e)
        )


def enable_dhcp_snooping_vlan(device, vlan):
    """ Enable DHCP snooping on vlan
        Args:
            device ('obj'): device to use
            vlan ('str'): vlan-id to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring DHCP snooping on vlan
    """
    log.info("Enabling DHCP snooping on vlan")
    try:
        device.configure(["ip dhcp snooping vlan {}".format(vlan)])
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not enable DHCP snooping on vlan {vlan}".format(
                vlan=vlan
            )
        )

def enable_dhcp_snooping(device):
    """ Enable DHCP snooping
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring DHCP snooping
    """
    log.info("Enabling DHCP snooping")
    try:
        device.configure(["ip dhcp snooping"])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable DHCP snooping, Error: {error}".format(
                error=e)

        )

def disable_dhcp_snooping_vlan(device, vlan):
    """ Disable DHCP snooping on vlan
        Args:
            device ('obj'): device to use
            vlan ('str'): vlan-id to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed disabling DHCP snooping on vlan
    """
    log.info("Disabling DHCP snooping on vlan")
    try:
        device.configure(["no ip dhcp snooping vlan {}".format(vlan)])
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not disable DHCP snooping on vlan {vlan}".format(
                vlan=vlan
            )
        )

def exclude_ip_dhcp(device, ip, high_ip=None):
    """ Exclude IP in DHCP
        Args:
            device ('obj'): device to use
            ip ('str'): ip to exclude
            high_ip ('str', optional): high ip range. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure: Failed excluding IP in DHCP config
    """
    log.info("Excluding IP in DHCP")
    try:
        device.configure([f"ip dhcp excluded-address {ip}{f' {high_ip}' if high_ip else ''}"])
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not exclude {ip} in DHCP config".format(
                ip=ip
            )
        )

def disable_dhcp_snooping_option_82(device):
    """ Disable DHCP snooping Option 82
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed disabling DHCP snooping Option 82
    """
    log.info("Disabling DHCP snooping Option 82")
    try:
        device.configure(["no ip dhcp snooping information option"])
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not disable DHCP snooping Option 82"
            )

def remove_dhcp_snooping_binding(
    device, vlan
):
    """ Remove DHCP snooping binding
        Args:
            device ('obj'): device to use
            vlan ('str'): vlan-id to remove binding
        Returns:
            None
        Raises:
            SubCommandFailure: Failed removing dhcp snooping binding
    """
    log.info(
        "Removing DHCP snooping binding with vlan = {}".format(vlan)
    )

    try:
        device.execute(
            [
            "clear ip dhcp snooping binding vlan {}".format(vlan),
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove DHCP snooping binding for vlan {vlan}".format(
                vlan = vlan
            )
        )
def enable_ip_dhcp_snooping_trust(device, interface):
    """ Enable DHCP snooping trust on interface
        Configure 'ip dhcp snooping trust' on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed enabling DHCP snooping trust on interface
    """
    log.info("Enabling DHCP snooping trust on interface")
    try:
        device.configure(
            [
             "interface {}".format(interface),
	         "ip dhcp snooping trust",
            ]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not enable DHCP snooping trust on interface {interface}".format(
                interface=interface
            )
        )

def enable_dhcp_snooping_option_82(device):
    """ Enable DHCP snooping Option 82
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed enabling DHCP snooping Option 82
    """
    log.info("Enabling DHCP snooping Option 82")
    try:
        device.configure(["ip dhcp snooping information option"])
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not enable DHCP snooping Option 82"
            )

def disable_dhcp_snooping(device):
    """ Disable DHCP snooping globally
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed disabling DHCP snooping globally
    """
    log.info("Disabling DHCP snooping globally")
    try:
        device.configure(["no ip dhcp snooping"])
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not disable DHCP snooping globally"
            )


def configure_ip_dhcp_snooping_database(device, image='', write_delay=False, delay_time=10):

    """ Configuring ip dhcp snooping database
        Args:
            device ('obj'): device to use
            image ('str',optional): image to use ,defaut is empty string
            write_delay ('bool',optional): True or False ,default is False
            delay_time ('int',optional): delay time ,default is 10
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ip dhcp snooping database
    """

    log.info("Configuring ip dhcp snooping database")

    cmd = "ip dhcp snooping database "

    if write_delay:

        cmd += f"write-delay {delay_time}"

    else:
        cmd += f"{image}"
    try:
        device.configure(
            [
                cmd
            ]
        )

    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Failed to configure ip dhcp snooping database")


def unconfigure_ip_dhcp_snooping_database(device, image='', write_delay=False, delay_time=10):

    """ Unconfiguring ip dhcp snooping database
        Args:
            device ('obj'): device to use
            image ('str',optional): image to use ,default is empty string
            write_delay ('bool',optional): True or False ,default is False
            delay_time ('int',optional): time interval ,default is 10
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ip dhcp snooping database
    """

    log.info("Unconfiguring ip dhcp snooping database")

    cmd = f"no ip dhcp snooping database "
    if write_delay:
        cmd += f"write-delay {delay_time}"
    else:
        cmd += f"{image}"
    try:
        device.configure(
            [
                cmd
            ]
        )

    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Failed to unconfigure ip dhcp snooping database")


def create_dhcp_pool_withoutrouter(
    device, pool_name, network, mask, lease_days,lease_hrs,lease_mins
):

    """ Create DHCP pool
        Args:
            device ('obj'): device to use
            pool_name ('str'): name of the pool to be created
            network ('str'): IP of the network pool
            mask ('str'): Subnet mask of the network pool
            lease_days ('int'):Parameters for lease days config
            lease_hrs ('int'):Parameters for lease hrs config
            lease_mins ('int'): Parameters for lease mins config
        Returns:
            None
        Raises:
            SubCommandFailure: Failed creating dhcp pool
    """

    log.info(
        "Configuring DHCP pool with name={}, network={}, mask={}, and "
        "Lease Time days={},hrs={},mins={}".format(pool_name, network, mask, lease_days,lease_hrs,lease_mins)
    )

    try:
        device.configure(
            [
            f"ip dhcp pool {pool_name}",
            f"network  {network} {mask}",
            f"lease {lease_days} {lease_hrs} {lease_mins}"
            ]
        )

    except SubCommandFailure as e:

        log.error(e)
        raise SubCommandFailure(
            "Could not configure DHCP pool {pool_name}".format(
                pool_name=pool_name
            )
        )

def unconfigure_ip_dhcp_snooping_verify(device, verify_type):
    """ unconfigure ip dhcp scooping verify on device
        Args:
            device (`obj`): Device object
            verify_type (`str`): verify type (i.e mac-address , no-relay-agent-address)
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring dhcp snooping verify on device
    """
    log.debug("unconfiguring ip dhcp scooping verify on device")

    try:
        device.configure(f"no ip dhcp snooping verify {verify_type}")

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ip dhcp scooping verify. Error:\n{e}"
        )

def configure_ip_dhcp_client(device, dhcp_client_type):
    """ Configure ip dhcp client on device
        Args:
            device (`obj`): Device object
            dhcp_client_type (`str`): DHCP client type (i.e broadcast-flag, default-router, forcerenew, network-discovery, update)
        Returns:
            None
        Raises:
            SubCommandFailure : ip dhcp client is not configured
    """
    log.debug("configuring DHCP client on device")

    try:
        device.configure(f"ip dhcp-client {dhcp_client_type}")

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ip DHCP client. Error:\n{e}"
        )
def enable_ip_dhcp_auto_broadcast(device):
    """ Enable ip dhcp auto-broadcast on device
        Args:
            device ('obj'): device to run on
        Returns:
            None
        Raises:
            SubCommandFailure : Failed enabling ip dhcp auto-broadcast on device
    """
    log.debug("Enabling DHCP auto-broadcast on device")

    try:
        device.configure("ip dhcp auto-broadcast")

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not enable DHCP auto-broadcast on device. Error:\n{e}"
        )

def disable_ip_dhcp_auto_broadcast(device):
    """ Disable ip dhcp auto-broadcast on device
        Args:
            device ('obj'): device to run on
        Returns:
            None
        Raises:
            SubCommandFailure : Failed disabling ip dhcp auto-broadcast on device
    """
    log.debug("Disabling DHCP auto-broadcast on device")

    try:
        device.configure("no ip dhcp auto-broadcast")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not disable DHCP auto-broadcast on device. Error:\n{e}"
            )

def configure_ip_dhcp_client_vendor_class(
        device,
        interface,
        type,
        string=None):
    """ Configure IP DHCP Client Vendor-class on interface:
        Args:
            device ('obj'): device to use
            interface ('str'): Interface to configure
            type('str'): vendor-class type (i.e. mac-address, ascii, hex, disable)
            string('str', optional): The value string when type set to ascii or hex
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ip dhcp vendor-class
    """
    log.info(f"Configure ip dhcp client vendor-class {type} on {interface}")
    if type in ['mac-address', 'disable']:
        cmd = f'ip dhcp client vendor-class {type}'

    elif type in ['ascii', 'hex'] and string:
        cmd = f'ip dhcp client vendor-class {type} {string}'

    else:
        raise SubCommandFailure("Invalid vendor-class type or string missing")

    try:
        device.configure([f"interface {interface}", cmd])

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ip dhcp vendor-class on {interface}. Error:\n{e}")


def unconfigure_ip_dhcp_client_vendor_class(
        device,
        interface,
        type):
    """ Unconfigure IP DHCP Client Vendor-class on interface:
        Args:
            device ('obj'): device to use
            interface ('str'): Interface to configure
            type('str'): vendor-class type (i.e. mac-address, ascii, hex, disable)
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ip dhcp vendor-class
    """
    log.info(f"Unconfigure ip dhcp client vendor-class {type} on {interface}")
    cmd = f'no ip dhcp client vendor-class {type}'
    try:
        device.configure([f"interface {interface}", cmd])

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ip dhcp vendor-class on {interface}. Error:\n{e}")

def enable_dhcp_smart_relay(device):
    """ Enable dhcp smart-relay on device
        Args:
            device ('obj'): device to run on
        Returns:
            None
        Raises:
            SubCommandFailure : Failed enabling smart-relay on device
    """
    log.debug("Enabling DHCP smart-relay on device")
    try:
        device.configure("ip dhcp smart-relay")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not enable DHCP smart-relay on device. Error:\n{e}"
            )

def disable_dhcp_smart_relay(device):
    """ Disable ip dhcp auto-broadcast on device
        Args:
            device ('obj'): device to run on
        Returns:
            None
        Raises:
            SubCommandFailure : Failed disabling smart-relay on device
    """
    log.debug("Disabling DHCP smart-relay on device")
    try:
        device.configure("no ip dhcp smart-relay")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not disable DHCP smart-relay on device. Error:\n{e}"
            )


def configure_dhcp_relay_information(device):

    """ Enable dhcp relay information on device
        Args:
            device ('obj'): device to run on
        Returns:
            None
        Raises:
            SubCommandFailure : Failed enabling relay information on device
    """
    log.debug("Enabling DHCP relay information on device")
    try:
        device.configure("ip dhcp relay information trust-all")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not enable DHCP relay information on device. Error:\n{e}"
            )

def unconfigure_dhcp_relay_information(device):

    """ Disable dhcp relay information on device
        Args:
            device ('obj'): device to run on
        Returns:
            None
        Raises:
            SubCommandFailure : Failed disabling relay information on device
    """
    log.debug("Disabling DHCP relay information on device")
    try:
        device.configure("no ip dhcp relay information trust-all")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not disable DHCP relay information on device. Error:\n{e}"
            )

def enable_dhcp_relay_information_option(device, vpn=False):
    """ Enable DHCP relay information option
        Args:
            device ('obj'): device to use
            vpn ('str',optional): vpn option ,defaut is empty string
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to enable dhcp relay information option
    """

    cmd = "ip dhcp relay information option"

    if vpn:
        cmd = "ip dhcp relay information option vpn"

    log.info("Enabling ip dhcp relay information option")
    try:
        device.configure(cmd)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to enable ip dhcp relay information option"
        )

def disable_dhcp_relay_information_option(device, vpn=False):
    """ Disable DHCP relay information option
        Args:
            device ('obj'): device to use
            vpn ('str',optional): vpn option ,defaut is empty string
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to disable dhcp relay information option
    """

    cmd = "no ip dhcp relay information option"
    if vpn:

        cmd = "no ip dhcp relay information option vpn"

    log.info("Disabling ip dhcp relay information option")
    try:
        device.configure(cmd)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed disable ip dhcp relay information option"
        )

def configure_dhcp_relay_short_lease(device, lease_time, interface=False):
    """ Configure DHCP relay short lease
        Args:
            device ('obj'): device to use
            lease_time ('int'): dhcp lease time
            interface ('str',optional): interface name ,defaut is empty string
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure dhcp relay short lease
    """

    cmd = []
    if interface:
        cmd.append(f"interface {interface}")
        cmd.append(f"ip dhcp relay short-lease {lease_time}")
    else:
        cmd.append(f"ip dhcp-relay short-lease {lease_time}")

    log.info("Configuring dhcp relay short lease")
    try:
        device.configure(cmd)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to configure dhcp relay short lease"
        )

def unconfigure_dhcp_relay_short_lease(device, lease_time, interface=False):
    """ Unconfigure DHCP relay short lease
        Args:
            device ('obj'): device to use
            lease_time ('int'): dhcp lease time
            interface ('str',optional): interface name ,defaut is empty string
            lease_time ('int'): dhcp lease time
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to disable dhcp relay short lease
    """

    cmd = []
    if interface:
        cmd.append(f"interface {interface}")
        cmd.append(f"no ip dhcp relay short-lease {lease_time}")
    else:
        cmd.append(f"no ip dhcp-relay short-lease {lease_time}")

    log.info("Unconfiguring dhcp relay short lease")
    try:
        device.configure(cmd)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to unconfigure dhcp relay short lease"
        )


def configure_ip_dhcp_snooping_information_option_allow_untrusted(device, interface):
    """configure ip dhcp snooping information option allow-untrusted on device
        Args:
            device (`obj`): Device object
            interface ('str'): interface to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring dhcp snooping information option allow-untrusted on device
    """
    log.info(f"configuring ip dhcp snooping information option allow-untrusted on {interface}")

    config_list = []
    config_list.append(f"interface {interface}")
    config_list.append("ip dhcp snooping information option allow-untrusted")

    try:
        device.configure(config_list)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ip dhcp snooping information option allow-untrusted. Error:\n{e}"
        )


def unconfigure_ip_dhcp_snooping_information_option_allow_untrusted(device, interface):
    """ unconfigure ip dhcp snooping information option allow-untrusted on device
        Args:
            device (`obj`): Device object
            interface ('str'): interface to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring dhcp snooping information option allow-untrusted on device
    """
    log.info(f"unconfiguring ip dhcp snooping information option allow-untrusted on {interface}")

    config_list = []
    config_list.append(f"interface {interface}")
    config_list.append("no ip dhcp snooping information option allow-untrusted")
    try:
        device.configure(config_list)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure dhcp snooping information option allow-untrusted. Error:\n{e}"
        )

def configure_ip_dhcp_snooping_information_option(device):
    """Configures dhcp snooping information option on device
       Example: ip dhcp snooping information option
       Args:
            device ('obj'): device object
       Return:
            None
       Raises:
            SubCommandFailure
    """
    log.info("Configuring dhcp snooping information option")
    try:
        device.configure("ip dhcp snooping information option")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to configure dhcp snooping information option on {device.name}\n{e}'
        )

def unconfigure_ip_dhcp_snooping_information_option(device):
    """Unconfigures dhcp snooping information option on device
       Example: no ip dhcp snooping information option
       Args:
            device ('obj'): device object
       Return:
            None
       Raises:
            SubCommandFailure
    """
    log.info("Unconfiguring dhcp snooping information option")
    try:
        device.configure("no ip dhcp snooping information option")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to unconfigure dhcp snooping information option on {device.name}\n{e}'
        )

def configure_ip_dhcp_pool(device, name):
    """Configures dhcp pool on device
       Example: ip dhcp pool POOL_88
       Args:
            device ('obj'): device object
            name ('str'): name of the pool (eg. POOL_88, testpool)
       Return:
            None
       Raises:
            SubCommandFailure
    """
    log.info(f"Configuring dhcp pool {name}")
    try:
        device.configure(f"ip dhcp pool {name}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to configure dhcp pool {name} on {device.name}\n{e}'
        )

def unconfigure_ip_dhcp_pool(device, name):
    """Unconfigures dhcp pool on device
       Example: no ip dhcp pool POOL_88
       Args:
            device ('obj'): device object
            name ('str'): name of the pool (eg. POOL_88, testpool)
       Return:
            None
       Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring dhcp pool {name}")
    try:
        device.configure(f"no ip dhcp pool {name}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to unconfigure dhcp pool {name} on {device.name}\n{e}'
        )

def configure_dhcp_channel_group_mode(device, interface, group, mode):
    """Configures Ethernet port to an EtherChannel group
       Example: channel-group 120 mode active
       Args:
            device ('obj'): device object
            interface ('str): interface to configure (eg. Gig1/0/1)
            group ('int'): Channel group number. The range is 1 to 128
            mode ('str'): EtherChannel mode (eg. active, passive, auto)
       Return:
            None
       Raises:
            SubCommandFailure
    """
    log.info(f"Configuring DHCP EtherChannel group mode {mode} on {interface}")
    config= [
        f'interface {interface}',
        f'channel-group {group} mode {mode}'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to configure DHCP channel-group mode {mode} on {interface}\n{e}'
        )

def unconfigure_dhcp_channel_group_mode(device, interface, group, mode):
    """Unconfigures Ethernet port to an EtherChannel group
       Example: no channel-group 120 mode active
       Args:
            device ('obj'): device object
            interface ('str): interface to configure (eg. Gig1/0/1)
            group ('int'): Channel group number. The range is 1 to 128
            mode ('str'): EtherChannel mode (eg. active, passive, auto)
       Return:
            None
       Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring DHCP EtherChannel group mode {mode} on {interface}")
    config= [
        f'interface {interface}',
        f'no channel-group {group} mode {mode}'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to unconfigure DHCP channel-group mode {mode} on {interface}\n{e}'
        )

def configure_cts_manual(device, interface, policy=None, sgt=None, trusted=None, propagate=None):
    """Configures cts manual on the interface
       Example: cts manual
       Args:
            device ('obj'): device object
            interface ('str'): interface to configure (eg. Gig1/0/1, Te1/0/10)
            policy ('str'): configure static policy
            sgt ('str'): sgt value
            trusted('str'): configure for trusted policy
            propagate('str'): to disable propagation
       Return:
            None
       Raises:
            SubCommandFailure
    """
    log.info(f"Configuring cts manual on {interface}")
    config= [
        f'interface {interface}',
        f'cts manual']

    if policy:
        if trusted:
            config.append(f'policy static sgt {sgt} trusted')
        else:
            config.append(f'policy static sgt {sgt}')

    if propagate:
        config.append(f'no propagate sgt')

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to configure cts manual on {interface} on {device.name}\n{e}'
        )


def unconfigure_ip_dhcp_snooping_trust(device, interface):
    """Unconfigures ip dhcp snooping trust
       Args:
            device ('obj'): device object
            interface ('str'): name of interface
       Return:
            None
       Raises:
            SubCommandFailure
    """
    cmd = [
        f"interface {interface}",
        "no ip dhcp snooping trust"
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to unconfigure no ip dhcp snooping trust on {device.name}\n{e}'
        )

def configure_ip_dhcp_pool_host(device, pool_name, host, client_identifier=None,
                                hardware_address=None, client_name=None, **kwargs):
    """ Configure DHCP host pool
        Args:
            device ('obj'): device to use
            pool_name ('str'): name of the pool to be configured
            host ('str'): IP and subnet mask of the DHCP client
            client_identifier ('str'): Unique identifier for client
            hardware_address ('str'): Hardware address of the client
            client_name ('str'): Name of the client
        Returns:
            str: Response of command
        Raises:
            SubCommandFailure: Failed to configure dhcp host pool
    """
    log.info(f"Configuring DHCP host pool {pool_name} for {host}")

    cmd_list = [f"ip dhcp pool {pool_name}",
                f"host {host}"]

    if client_identifier:
        cmd_list.append(f"client-identifier {client_identifier}")
    if hardware_address:
        cmd_list.append(f"hardware-address {hardware_address}")
    if client_name:
        cmd_list.append(f"client-name {client_name}")
    try:
        device.configure(cmd_list, **kwargs)

    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            f"Failed to configure DHCP host pool {pool_name}"
        )

def unconfigure_ip_dhcp_pool_host(device, pool_name, host, client_identifier=None,
                                hardware_address=None, client_name=None, **kwargs):
    """ Unconfigure host from DHCP pool
        Args:
            device ('obj'): device to use
            pool_name ('str'): name of the DHCP pool
            host ('str'): IP and subnet mask of the DHCP client
            client_identifier ('str'): Unique identifier for client
            hardware_address ('str'): Hardware address of the client
            client_name ('str'): Name of the client
        Returns:
            str: Response of command
        Raises:
            SubCommandFailure: Failed to unconfigure host from dhcp pool
    """
    log.info(f"Unconfiguring host {host} from DHCP pool {pool_name}")

    cmd_list = [f"ip dhcp pool {pool_name}",
                f"no host {host}"]

    if client_identifier:
        cmd_list.append(f"no client-identifier {client_identifier}")
    if hardware_address:
        cmd_list.append(f"no hardware-address {hardware_address}")
    if client_name:
        cmd_list.append(f"no client-name {client_name}")
    try:
        device.configure(cmd_list, **kwargs)

    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            f"Failed to uniconfigure host from DHCP pool {pool_name}")

def configure_ip_dhcp_exclude_vrf(device, vrf_name, low_ip_address, high_ip_address):
    """ Configure ip dhcp exclude vrf
        Args:
            device ('obj'): device to use
            vrf_name ('str'): VPN Routing/Forwarding instance name
            low_ip_address ('str'): Low IP address
            high_ip_address ('str'): High IP address
        Returns:
            None
        Raises:
            SubCommandFailure: Failed excluding IP in DHCP config
    """
    log.info("configuring ip dhcp exclude vrf")
    cmd = [f'ip dhcp excluded-address vrf {vrf_name} {low_ip_address} {high_ip_address}']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not exclude ip in DHCP config. Error:\n{e}".format(
                error=e
            )
        )
def configure_ip_dhcp_restrict_next_hop(device, interface, restrict_method):
    """ configure ip dhcp restrict-next-hop on interface
        Configure 'ip dhcp restrict-next-hop' on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            restrict_method('str'): restrict method 'both|cdp|lldp'
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configure ip dhcp restrict-next-hop on interface
    """
    log.info("configure ip dhcp restrict-next-hop on interface")
    try:
        device.configure(
            [
             'interface {}'.format(interface),
             'ip dhcp restrict-next-hop {}'.format(restrict_method),
            ]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure ip dhcp restrict-next-hop on interface {}".format(interface)
        )
def unconfigure_ip_dhcp_restrict_next_hop(device, interface):
    """ unconfigure ip dhcp restrict-next-hop on interface
        unConfigure 'ip dhcp restrict-next-hop' on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfigure ip dhcp restrict-next-hop on interface
    """
    log.info("unconfigure ip dhcp restrict-next-hop on interface")
    try:
        device.configure(
            [
             "interface {}".format(interface),
	         "no ip dhcp restrict-next-hop",
            ]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not unconfigure ip dhcp restrict-next-hop on interface {interface}".format(
                interface=interface
            )
        )
def configure_ip_dhcp_snooping_limit(device, interface, rate_limit):
    """ Configure DHCP snooping limit on interface
        Configure 'ip dhcp snooping limit' on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            rate_limit('int'): DHCP snooping rate limit
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring DHCP snooping limit rate on interface
    """
    log.info("Configure DHCP snooping limit rate on interface")
    config = [
             f"interface {interface}",
             f"ip dhcp snooping limit rate {rate_limit}",
            ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure DHCP snooping limit on interface {interface}. Error\n{e}"
            )

def configure_interface_ip_dhcp_relay_information_option_vpn_id(device, interface):
    """ Configure ip dhcp relay information option vpn-id on the interface
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured # example  "interface vlan 100" "ip dhcp relay information option vpn-id"
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to ip dhcp relay information option vpn-id
    """
    log.info("Configuring ip dhcp relay information option vpn-id on the interface")
    config =  ["interface {}".format(interface),
                "ip dhcp relay information option vpn-id"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ip dhcp relay information option vpn-id on the interface {interface}. Error\n{e}"
        )

def unconfigure_interface_ip_dhcp_relay_information_option_vpn_id(device, interface):
    """ Unconfigure ip dhcp relay information option vpn-id on the interface # example  "interface vlan 100" "ip dhcp relay information option vpn-id"
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured # example  "interface vlan 100" "ip dhcp relay information option vpn-id"
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to enable dhcp relay information option
    """
    log.info("Unconfiguring ip dhcp relay information option vpn-id on the interface")
    config =  ["interface {}".format(interface),
               "no ip dhcp relay information option vpn-id"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ip dhcp relay information option vpn-id on the interface {interface}. Error\n{e}"
        )

def configure_interface_ip_dhcp_relay_source_interface_intf_id(device, interface, intf_id):
    """ Configure interface ip dhcp relay source interface intf_id
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured # example  "interface vlan 100" "ip dhcp relay source-interface Loopback1"
            intf_id ('str'): Set source interface for relayed messages for interface ex: Loopback1 interface
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ip dhcp relay source-interface intf_id
    """
    log.info("Configuring ip dhcp relay source-interface intf_id on the interface")
    config = [
                "interface {}".format(interface),
                "ip dhcp relay source-interface {}".format(intf_id)]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ip dhcp relay source interface intf_id {interface}. Error\n{e}"
        )

def unconfigure_interface_ip_dhcp_relay_source_interface_intf_id(device, interface, intf_id):
    """ UnConfigure interface ip dhcp relay source interface intf_id
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured # example  "interface vlan 100" "no ip dhcp relay source-interface Loopback1"
            intf_id ('str'): Set source interface for relayed messages for interface ex: Loopback1 interface
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ip dhcp relay source-interface intf_id
    """
    log.info("Unconfiguring ip dhcp relay source-interface intf_id on the interface")
    config = [
                "interface {}".format(interface),
                "no ip dhcp relay source-interface {}".format(intf_id)]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ip dhcp relay source interface intf_id {interface}. Error\n{e}"
        )

def configure_dhcp_pool(device, pool_name, router_id=None, network=None, mask=None, vrf=None, dns_server=None, lease=False, lease_days=None, lease_hrs=None, lease_mins=None, lease_time=None):
    """ Configure DHCP pool
        Args:
            device ('obj'): device to use
            pool_name ('str'): name of the pool to be created
            router_id ('str', optional): router id to configure default-router. Default is None
            network ('str', optional): IP of the network pool. Default is None
            mask ('str', optional): Subnet mask of the network pool. Default is None
            vrf ('str' , optional): VRF to associate with the DHCP pool. Default is None
            dns_server ('str', optional): IP address of the DNS server. Default is None
            lease ('boolean', optional) : lease for the DHCP pool is there or not. Default is False
            lease_days ('str'): Number of days for the lease
            lease_hrs ('str'): Number of hours for the lease
            lease_mins ('str'): Number of minutes for the lease
            lease_time ('str'): Lease time for the DHCP pool
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure dhcp pool
    """
    dialog = Dialog(
        [
            Statement(
                pattern=r'.*Continue\? +\[yes\].*',
                action='sendline()'
            )
        ]
    )

    config = [f'ip dhcp pool {pool_name}']
    if router_id:
        config.append(f'default-router {router_id}')
    if network and mask:
        config.append(f'network {network} {mask}')
    if vrf:
        config.append(f'vrf {vrf}')
    if dns_server:
        config.append(f'dns-server {dns_server}')
    if lease:
        if lease_time == "infinite":
            config.append('lease infinite')
        elif lease_time == "{} {} {}".format(lease_days, lease_hrs, lease_mins):
            config.append('lease {} {} {}'.format(lease_days, lease_hrs, lease_mins))
    try:
        device.configure(config, reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure dhcp pool. Error: {e}')


def unconfigure_dhcp_pool(device, pool_name, router_id=None, network=None, mask=None, vrf=None, dns_server=None):
    """ Unconfigure DHCP pool
        Args:
            device ('obj'): device to use
            pool_name ('str'): name of the pool to be created
            router_id ('str', optional): router id to configure default-router. Default is None
            network ('str', optional): IP of the network pool. Default is None
            mask ('str', optional): Subnet mask of the network pool. Default is None
            vrf ('str' , optional): VRF to associate with the DHCP pool. Default is None
            dns_server ('str', optional): IP address of the DNS server. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure dhcp pool
    """
    dialog = Dialog(
        [
            Statement(
                pattern=r'.*Continue\? +\[yes\].*',
                action='sendline()',
                loop_continue=True,
                continue_timer=False
            )
        ]
    )

    config = [f'ip dhcp pool {pool_name}']
    if router_id:
        config.append(f'no default-router {router_id}')
    if network and mask:
        config.append(f'no network {network} {mask}')
    if vrf:
        config.append(f'no vrf {vrf}')
    if dns_server:
        config.append(f'no dns-server {dns_server}')
    try:
        device.configure(config, reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure dhcp pool. Error: {e}')


def configure_service_dhcp(device):
    """ Configure DHCP pool
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure service dhcp
    """

    config = 'service dhcp'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure service dhcp. Error: {e}')


def unconfigure_service_dhcp(device):
    """ Unconfigure DHCP pool
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure service dhcp
    """

    config = 'no service dhcp'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure service dhcp. Error: {e}')


def unconfigure_exclude_ip_dhcp(device, ip, high_ip=None, vrf=None):
    """ Unconfigure Exclude IP in DHCP
        Args:
            device ('obj'): device to use
            ip ('str'): ip to exclude
            high_ip ('str', optional): high ip range. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfigure exclude IP in DHCP config
    """
    try:
        if vrf:
            device.configure([f"no ip dhcp excluded-address vrf {vrf} {ip}{f' {high_ip}' if high_ip else ''}"])
        else:
            device.configure([f"no ip dhcp excluded-address {ip}{f' {high_ip}' if high_ip else ''}"])

    except SubCommandFailure:
        raise SubCommandFailure(f"Could not unconfigure exclude {ip} in DHCP config")

def enable_dhcp_compatibility_suboption(device, suboption, value):
    """ Enable DHCP compatibility suboption
        Args:
            device ('obj'): device to use
            suboption ('str'): Link-Selection or Server-id override suboption
            value ('str'): cisco or standard value
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    config = f"ip dhcp compatibility suboption {suboption} {value}"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to enable DHCP compatibility suboption. Error:\n{e}")

def disable_dhcp_compatibility_suboption(device, suboption):
    """ Disable DHCP compatibility suboption
        Args:
            device ('obj'): device to use
            suboption ('str'): Link-Selection or Server-id override suboption
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    config = f"no ip dhcp compatibility suboption {suboption}"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to disable DHCP compatibility suboption. Error:\n{e}")

def unconfigure_propagate_sgt(device, interface, type, cts_type):
    """ UnConfigure propagate sgt
       Args:
            device ('obj'): device object
            interface ('str'): interface to configure (eg. Gig1/0/1, Te1/0/10)
            type ('str'):  manual      Supply local configuration for CTS parameters
                           role-based  Role-based Access Control per-port config commands
            cts_type ('str'): policy     CTS policy for manual mode
                              propagate  CTS SGT Propagation configuration for manual mode
                              sap        CTS SAP configuration for manual mode
                              sap        CTS SAP configuration for manual mode
       Return:
            None
       Raises:
            SubCommandFailure
    """
    log.info(f"unconfigure propagate sgt on interface")
    config= [
              f'interface {interface}',
              f'cts {type}',
              f'no {cts_type} sgt'
            ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to unconfigure propagate sgt {interface} on {device.name}\n{e}'
        )

def unconfigure_cts_role_based_sgt_map_vlan_list(device, Vlan_id, Tag_value):
    """UnConfigure cts role-based sgt-map vlan-list 300 sgt 300
       Args:
            device ('obj'): device object
            Vlan_list ('int'): <1-4094>  VLAN id
            Tag_value ('int'): <2-65521>  Security Group Tag value
       Return:
            None
       Raises:
            SubCommandFailure
    """
    log.info(f"UnConfigure cts role-based sgt-map vlan-list 300 sgt 300")
    config= [
               f'no cts role-based sgt-map vlan-list {Vlan_id} sgt {Tag_value}'
             ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to unconfigure cts role-based sgt-map vlan-list 300 sgt 300 on {device.name}\n{e}'
        )


def configure_ip_dhcp_snooping_information_option_allow_untrusted_global(device):
    """ Configure ip dhcp snooping information option allow-untrusted on device
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring dhcp snooping information option allow-untrusted on device
    """
    cmd= f'ip dhcp snooping information option allow-untrusted'
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ip dhcp snooping information option allow-untrusted. Error:\n{e}"
        )


def unconfigure_ip_dhcp_snooping_information_option_allow_untrusted_global(device):
    """ Unconfigure ip dhcp snooping information option allow-untrusted on device
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring dhcp snooping information option allow-untrusted on device
    """
    cmd= f'no ip dhcp snooping information option allow-untrusted'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure dhcp snooping information option allow-untrusted. Error:\n{e}"
        )

def configure_interface_range_dhcp_channel_group_mode(device, start_interface, end_interface, group, mode):
    """Configures Ethernet port to an EtherChannel group
       Example: channel-group 10 mode desirable
       Args:
            device ('obj'): device object
            start_interface('str'): Starting Interface
            end_interface('str'): Ending Interface number
            group ('int'): Channel group number. The range is 1 to 128
            mode ('str'): EtherChannel mode (eg. active, passive, auto)
       Return:
            None
       Raises:
            SubCommandFailure
    """
    log.debug(f"Configuring DHCP EtherChannel group mode {mode}")
    config= [
        f'interface range {start_interface} - {end_interface}',
        f'channel-group {group} mode {mode}'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to configure DHCP channel-group mode {mode} \n{e}'
        )

def unconfigure_interface_range_dhcp_channel_group_mode(device, start_interface, end_interface, group, mode):
    """Unconfigures Ethernet port to an EtherChannel group
       Example: no channel-group 120 mode active
       Args:
            device ('obj'): device object
            start_interface('str'): Starting Interface
            end_interface('str'): Ending Interface number
            group ('int'): Channel group number. The range is 1 to 128
            mode ('str'): EtherChannel mode (eg. active, passive, auto)
       Return:
            None
       Raises:
            SubCommandFailure
    """
    log.debug(f"Unconfiguring DHCP EtherChannel group mode {mode}")
    config= [
        f'interface range {start_interface} - {end_interface}',
        f'no channel-group {group} mode {mode}'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to unconfigure DHCP channel-group mode {mode}\n{e}'
        )

def unconfigure_ip_dhcp_snooping_limit_rate(device, interface, rate_limit):
    """ Unconfigure DHCP snooping limit on interface
        Unconfigure 'no ip dhcp snooping limit' on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            rate_limit('int'): DHCP snooping rate limit
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring DHCP snooping limit rate on interface
    """
    log.debug("Unconfigure DHCP snooping limit rate on interface")
    config = [
             f"interface {interface}",
             f"no ip dhcp snooping limit rate {rate_limit}",
            ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not remove DHCP snooping limit configuration on interface {interface}. Error\n{e}"
            )

def unconfigure_ip_dhcp_snooping_verify_mac_address(device):
    """ Unconfigure ip_dhcp_snooping_verify_mac_address
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring DHCP snooping verify mac-address
    """
    log.debug("Unconfigure ip_dhcp_snooping_verify_mac_address")
    try:
        device.configure('no ip dhcp snooping verify mac-address')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not remove DHCP snooping verify mac-address. Error\n{e}"
            )

def configure_ip_dhcp_snooping_verify_mac_address(device):
    """ Configure ip_dhcp_snooping_verify_mac_address
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring DHCP snooping verify mac-address
    """
    log.debug("Configure ip_dhcp_snooping_verify_mac_address")
    try:
        device.configure('ip dhcp snooping verify mac-address')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure DHCP snooping verify mac-address. Error\n{e}"
            )

def configure_dhcp_snooping_verify_no_relay_agent_address(device):
    """ Configure DHCP snooping verify no-relay-agent-address on global
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed Configuring DHCP snooping verify no-relay-agent-address.
    """
    log.debug("Configure DHCP snooping verify no-relay-agent-address on global")
    try:
        device.configure('ip dhcp snooping verify no-relay-agent-address')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure DHCP snooping verify no-relay-agent-address. Error\n{e}"
            )

def unconfigure_dhcp_snooping_verify_no_relay_agent_address(device):
    """ Unconfigure DHCP snooping verify no-relay-agent-address on global
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring DHCP snooping verify no-relay-agent-address
    """
    log.debug("Unconfigure DHCP snooping verify no-relay-agent-address on global")
    try:
        device.configure('no ip dhcp snooping verify no-relay-agent-address')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not remove DHCP snooping verify no-relay-agent-address. Error\n{e}"
            )

def configure_dhcp_snooping_track_server_dhcp_acks(device):
    """ Configure DHCP snooping server track dhcp_acks on global
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed Configuring DHCP snooping server track dhcp_acks
    """
    log.debug("Configure DHCP snooping server track dhcp_acks on global")
    try:
        device.configure('ip dhcp snooping track server all-dhcp-acks')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure DHCP snooping server track all-dhcp-ack. Error\n{e}"
            )

def unconfigure_dhcp_snooping_track_server_dhcp_acks(device):
    """ Unconfigure DHCP snooping server track dhcp_acks on global
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed Unconfiguring DHCP snooping server track dhcp_acks
    """
    log.debug("Unconfigure DHCP snooping server track dhcp_acks on global")
    try:
        device.configure('no ip dhcp snooping track server all-dhcp-acks')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not remove DHCP snooping server track all-dhcp-ack. Error\n{e}"
            )

def configure_ip_dhcp_pool_address(device, name, address, client_id):
    """Configures dhcp pool on device
       Example: ip dhcp pool POOL_88
       Args:
            device ('obj'): device object
            name ('str'): name of the pool (eg. POOL_88, testpool)
            address ('str'): device object
            client_id ('str'): client ID in hex formate
       Return:
            None
       Raises:
            SubCommandFailure
    """
    log.debug(f"Configuring dhcp address and client_id")

    config_list = [f"ip dhcp pool {name}",
        f"address {address} client-id {client_id}"]

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to configure address and clinet-id on {device.name}\n{e}'
        )

def configure_dhcp_option43(device, pool, data_type='ascii', ascii_string=None):
    """ Configure dhcp option 4
       Args:
            device ('obj'): device object
            pool ('str'): pool name to configure
            data_type ('str'): Data type can be any. Default is ascii
            ascii_string ('str'):   Data as an NVT ASCII string  to configure
       Return:
            None
       Raises:
            SubCommandFailure
    """
    log.debug(f"configure option 43")
    config= [f'ip dhcp pool {pool}']
    if data_type == 'ascii' and ascii_string is not None:
        config.append(f'option 43 {data_type} {ascii_string}')
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to configure dhcp option 43 for pool: {pool} on {device.name}\n{e}'
        )

def configure_pnp_startup_vlan(device, vlan):
    """ Configure pnp startup vlan
       Args:
            device ('obj'): device object
            vlan ('str'): vlan id to be configured
       Return:
            None
       Raises:
            SubCommandFailure
    """
    log.debug(f"configure startup vlan {vlan}")
    config= f'pnp startup-vlan {vlan}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to configure pnp startup-vlan: {vlan} on {device.name}\n{e}'
        )

def unconfigure_pnp_startup_vlan(device, vlan):
    """ Unconfigure pnp startup vlan
       Args:
            device ('obj'): device object
            vlan ('str'): vlan id to be configured
       Return:
            None
       Raises:
            SubCommandFailure
    """
    log.debug(f"Unconfigure startup vlan")
    config= f'no pnp startup-vlan {vlan}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to Unconfigure pnp startup-vlan: {vlan} on {device.name}\n{e}'
        )

def configure_interface_ip_dhcp_relay_information_option_insert(device, interface):
    """ Configure ip dhcp relay information option-insert on the interface
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured # example  "interface vlan 100" "ip dhcp relay information option-insert"
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ip dhcp relay information option-insert
    """
    log.info("Configuring ip dhcp relay information option-insert on the interface")
    config =  ["interface {}".format(interface),
                "ip dhcp relay information option-insert"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ip dhcp relay information option-insert on the interface {interface}. Error\n{e}"
        )

def unconfigure_interface_ip_dhcp_relay_information_option_insert(device, interface):
    """ Unconfigure ip dhcp relay information option-insert on the interface # example  "interface vlan 100" "ip dhcp relay information option-insert"
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured # example  "interface vlan 100" "ip dhcp relay information option-insert"
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure dhcp relay information option-insert
    """
    log.info("Unconfiguring ip dhcp relay information option-insert on the interface")
    config =  ["interface {}".format(interface),
               "no ip dhcp relay information option-insert"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ip dhcp relay information option-insert on the interface {interface}. Error\n{e}"
        )

def configure_ip_ddns_update_method(
    device, method_name, method_option=None, dns_option=None, url=None):
    """ Configure Ip DDNS update method
        Args:
            device ('obj'): device to use
            method_name ('str'): Method name for DDNS update
            method_option ('str',optional): method option for DDNS update, default is HTTP
            dns_option ('str',optional): dns option for DDNS update, default is add
            url ('str',optional): URL used to add or remove DNS records
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ip ddns update method
    """
    log.debug(f"Configuring ip ddns update method {method_name}")

    config = [
            f"ip ddns update method {method_name}",
	        f"{method_option}",
            f"{dns_option} {url}",
            "interval maximum 0 1 0 0"
            ]
    try:
        device.configure(config)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure DDNS Update Method {method_name}. Error:\n{e}"
            )

def unconfigure_ip_ddns_update_method(device, method_name):
    """ Configure Ip DDNS update method
        Args:
            device ('obj'): device to use
            method_name ('str'): name of the method to be created

        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ip ddns update method
    """
    log.debug(f"Unconfiguring ip ddns update method {method_name}")

    config =  ["no ip ddns update method {}".format(method_name)]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ip ddns update method {method_name}. Error\n{e}"
        )

def configure_dhcp_option(device, pool, data_type='ascii', dhcp_option=None, ascii_string=None):
    """ Configure dhcp option
       Args:
            device ('obj'): device object
            pool ('str'): pool name to configure
            data_type ('str'): Data type can be any. Default is ascii
            dhcp_option ('str'): DHCP option code
            ascii_string ('str'):   Data as an NVT ASCII string  to configure
       Return:
            None
       Raises:
            SubCommandFailure
    """
    log.debug(f"configure option")
    config= [f'ip dhcp pool {pool}']
    if data_type == 'ascii' and ascii_string is not None and dhcp_option is not None:
        config += [f'option {dhcp_option} {data_type} {ascii_string}']
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to configure dhcp option for pool: {pool} on {device.name}\n{e}'
        )

def configure_interface_ip_ddns_update(device, interface, name, hostname=False):
    """ Configure ip ddns update on the interface
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured # example  "interface vlan 100"
            name ('str'): name of method or hostname
            hostname ('bool',optional): True or False ,default is False
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ip ddns update on the interface
    """
    log.debug("Configuring ip ddns update on the interface")
    cmd =  [f"interface {interface}"]
    if hostname:
        cmd.append(f"ip ddns update hostname {name}")
    else:
        cmd.append(f"ip ddns update {name}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ip ddns update on the interface {interface}. Error\n{e}"
        )

def unconfigure_interface_ip_ddns_update(device, interface, name, hostname=False):
    """ Unconfigure ip ddns update on the interface
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured # example  "interface vlan 100"
            name ('str'): name of method or hostname
            hostname ('bool',optional): True or False ,default is False
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ip ddns update on the interface
    """
    log.debug("Configuring ip ddns update on the interface")
    cmd =  [f"interface {interface}"]
    if hostname:
        cmd.append(f"no ip ddns update hostname {name}")
    else:
        cmd.append(f"no ip ddns update {name}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ip ddns update on the interface {interface}. Error\n{e}"
        )

def configure_interface_ip_dhcp_client(device, interface, option, type, tag, update=False):
    """ Configure ip dhcp client on the interface
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured # example  "interface vlan 100"
            option ('str'): it can be  class-id or client-id or default-router
            type ('str'): it can be for example interface or ascii or hex
            tag ('str',Optional): it can be value of ascii or hex, interface or vlan name
            update ('bool',Optional): True or False ,default is False
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ip dhcp client on the interface
    """
    log.debug("Configuring ip dhcp client on the interface")
    cmd =  [f"interface {interface}"]
    cmd.append(f"ip dhcp client {option} {type}")
    if option in ['authentication', 'class-id', 'client-id', 'default-router', 'option', 'request', 'route', 'vendor-class']:
        cmd.append(f"ip dhcp client {option} {type} {tag}")
    elif update:
        cmd.append(f"ip dhcp client update {option} {type} {tag}")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ip dhcp client on the interface {interface}. Error\n{e}"
        )

def unconfigure_interface_ip_dhcp_client(device, interface, option, type, tag, update=False):
    """ Unonfigure ip dhcp client on the interface
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured # example  "interface vlan 100"
            option ('str'): it can be  class-id or client-id or default-router
            type ('str'): it can be for example interface or ascii or hex
            tag ('str',Optional): it can be value of ascii or hex, interface or vlan name
            update ('bool',Optional): True or False ,default is False
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ip dhcp client on the interface
    """
    log.debug("Unconfiguring ip dhcp client on the interface")
    cmd =  [f"interface {interface}"]
    cmd.append(f"no ip dhcp client {option} {type}")
    if option in ['authentication', 'class-id', 'client-id', 'default-router', 'option', 'request', 'route', 'vendor-class']:
        cmd.append(f"no ip dhcp client {option} {type} {tag}")
    elif update:
        cmd.append(f"no ip dhcp client update {option} {type} {tag}")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ip dhcp client on the interface {interface}. Error\n{e}"
        )

def configure_ip_dhcp_ping_packets(device, packets_no):
    """ Configure ip dhcp ping packets
        Args:
            device ('obj'): device to use
            packets_no ('int'): <0-10> , number of ping packets

        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ip dhcp ping packets
    """
    log.debug("Configuring ip dhcp ping packets")
    config =  f"ip dhcp ping packets {packets_no}"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ip dhcp ping packets on device {device}. Error\n{e}"
        )

def unconfigure_ip_dhcp_ping_packets(device, packets_no):
    """ Unconfigure ip dhcp ping packets
        Args:
            device ('obj'): device to use
            packets_no ('int'): <0-10> , number of ping packets

        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ip dhcp ping packets
    """
    log.debug("Unconfiguring ip dhcp ping packets")
    config =  f"no ip dhcp ping packets {packets_no}"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ip dhcp ping packets on device {device}. Error\n{e}"
        )

def configure_ip_dhcp_remember(device):
    """ Configure ip dhcp remember
        Args:
            device ('obj'): device to use

        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ip dhcp remember
    """
    log.debug("Configuring ip dhcp remember")
    config =  f"ip dhcp remember"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ip dhcp remember on device {device}. Error\n{e}"
        )

def unconfigure_ip_dhcp_remember(device):
    """ Unconfigure ip dhcp remember
        Args:
            device ('obj'): device to use

        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ip dhcp remember
    """
    log.debug("Unconfiguring ip dhcp remember")
    config =  f"no ip dhcp remember"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to Unconfigure ip dhcp remember on device {device}. Error\n{e}"
        )

def configure_interface_ip_dhcp_relay(device, interface, type, string = None, option = None):
    """ Configure ip dhcp relay on the interface
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured #example "interface vlan 100" ip dhcp relay information trusted
            type ('str'): type for dhcp relay update #example policy-action, trusted, etc
            string('str', optional): string used to keep or remove dhcp relay information #example keep, drop, replace, etc
            option('str', optional): used for some specific string #example vpn-id None, subscriber-id abc, etc
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ip dhcp relay on the interface
    """
    log.debug("Configuring ip dhcp relay on the interface")
    config = [f'interface {interface}']
    if type in ['policy-action', 'check-reply', 'option-insert']:
        config.append(f"ip dhcp relay information {type} {string}")
    elif type in ['trusted']:
        config.append(f"ip dhcp relay information {type}")
    elif type in ['option']:
        if string and option:
            config.append(f"ip dhcp relay information {type} {string} {option}")
        elif string:
            config.append(f"ip dhcp relay information {type} {string}")
        elif option:
            config.append(f"ip dhcp relay information {type} {option}")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ip dhcp relay information {type} {string} on the interface {interface}. Error\n{e}"
        )

def unconfigure_interface_ip_dhcp_relay(device, interface, type, string = None, option = None):
    """ Unconfigure ip dhcp relay on the interface
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured #example "interface vlan 100" ip dhcp relay information trusted
            type ('str'): type for dhcp relay update #example policy-action, trusted, etc
            string ('str', optional): string used to keep or remove dhcp relay information #example keep, drop, replace, etc
            option ('str', optional): used for some specific string #example vpn-id None, subscriber-id abc, etc
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ip dhcp relay on the interface
    """
    log.debug("Unconfiguring ip dhcp relay on the interface")
    config = [f'interface {interface}']
    if type in ['policy-action', 'check-reply', 'option-insert']:
        config.append(f"no ip dhcp relay information {type} {string}")
    elif type in ['trusted']:
        config.append(f"no ip dhcp relay information {type}")
    elif type in ['option']:
        if string and option:
            config.append(f"no ip dhcp relay information {type} {string} {option}")
        elif string:
            config.append(f"no ip dhcp relay information {type} {string}")
        elif option:
            config.append(f"no ip dhcp relay information {type} {option}")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ip dhcp relay information {type} {string} on the interface {interface}. Error\n{e}"
        )

def configure_ip_dhcp_drop_inform(device):
    """ Configure ip dhcp drop-inform
        Args:
            device ('obj'): device to use

        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ip dhcp drop-inform
    """
    log.debug("Configuring ip dhcp drop-inform")
    config = [f"ip dhcp drop-inform"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ip dhcp drop-inform on {device}. Error\n{e}"
            )

def unconfigure_ip_dhcp_drop_inform(device):
    """ Unconfigure ip dhcp drop-inform
        Args:
            device ('obj'): device to use

        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ip dhcp drop-inform
    """
    log.debug("Unconfiguring ip dhcp drop-inform")
    config = [f"no ip dhcp drop-inform"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ip dhcp drop-inform on {device}. Error\n{e}"
            )

def configure_ip_dhcp_binding_cleanup_interval(device, interval_time):
    """ Configure ip dhcp binding cleanup interval
        Args:
            device ('obj') : device to use
            interval ('int'): <10-600> , cleanup interval in seconds

            Returns:
                None
            Raises:
                SubCommandFailure: Failed to unconfigure ip dhcp binding cleanup interval
    """
    log.debug("Configuring ip dhcp binding cleanup interval {interval_time}")
    config =  f"ip dhcp binding cleanup interval {interval_time}"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ip dhcp cleanup interval {interval_time} on device {device}. Error\n{e}"
        )

def unconfigure_ip_dhcp_binding_cleanup_interval(device, interval_time):
    """ Unconfigure ip dhcp binding cleanup interval
        Args:
            device ('obj') : device to use
            interval ('int'): <10-600> , cleanup interval in seconds

            Returns:
                None
            Raises:
                SubCommandFailure: Failed to unconfigure ip dhcp binding cleanup interval
    """
    log.debug("Unconfiguring ip dhcp binding cleanup interval {interval_time}")
    config =  f"no ip dhcp binding cleanup interval {interval_time}"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ip dhcp cleanup interval {interval_time} on device {device}. Error\n{e}"
        )

def configure_ip_dhcp_database(device, database_path):
    """ Configure ip dhcp database {database_path}
        Args:
            device ('obj') : device to use
            database_path ('int'): database path
            Returns:
                None
            Raises:
                SubCommandFailure: Failed to Configure ip dhcp database {database_path}
    """
    log.debug("Configuring ip dhcp database {database_path}")
    config =  f"ip dhcp database {database_path}"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ip dhcp database {database_path} on device {device}. Error\n{e}"
        )

def unconfigure_ip_dhcp_database(device, database_path):
    """ UnConfigure ip dhcp database {database_path}
        Args:
            device ('obj') : device to use
            database_path ('int'): database path
            Returns:
                None
            Raises:
                SubCommandFailure: Failed to UnConfigure ip dhcp database {database_path}
    """
    log.debug("UnConfiguring ip dhcp database {database_path}")
    config =  f"no ip dhcp database {database_path}"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ip dhcp database {database_path} on device {device}. Error\n{e}"
        )

def configure_dhcp_pool_ztp(device, pool_name, network=None, mask=None, option_1=None, ascii_string=None, option_2=None, ip_address=None):
    ''' Configure dhcp pool for ZTP
        Args:
            device ('obj'): device to use
            pool_name('str'): Configure DHCP address pools
            network('str', Optional): Network number in dotted-decimal notation
            mask('str', Optional): Subnet mask in dotted-decimal notation
            option_1('int', optional): DHCP option code
            ascii_string('str'): NVT ASCII string, truncated to 225 characters
            option_2('int'): DHCP option code
            ip_address('str'): Server's name or IP address
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure dhcp pool for ZTP
    '''

    log.debug("Configuring dhcp pool for ZTP")

    cmd = [f"ip dhcp pool {pool_name}"]
    if network and mask:
        cmd.append(f"network {network} {mask}")
    if option_1 and ascii_string:
        cmd.append(f"option {option_1} ascii {ascii_string}")
    if option_2 and ip_address:
        cmd.append(f"option {option_2} ip {ip_address}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure dhcp pool for ZTP. Error:\n{e}"
            )

def configure_interface_ip_subscriber(device, interface, ip_session, option=None, type=None, value=None, list_name=None,  initiator=False):
    """ Configure ip subscriber on interface
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to configure
            ip_session ('str'): ip session to configure
            option ('str',Optional): based on cli requirement (eg. arp, passthru, mac-address, ip-address)
            type ('str',Optional): based on cli requirement  (eg. ignore, downstream, ipv4, ipv6, list)
            value ('str',Optional): it can be different values based on type
            list_name ('str',Optional): list name to configure
            initiator ('str',Optional): IP session initiation
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring ip subscriber on interface
    """
    log.debug("Configure ip subscriber on interface")
    config = [
             f"interface {interface}",
             f"ip subscriber {ip_session}"
            ]
    if option in ['arp', 'passthru']:
        config.append(f"{option} {type} {value}")
    elif  initiator and type in ['dhcp', 'radius-proxy']:
        config.append(f"initiator {type}")
    elif list_name:
        config.append(f"initiator static ip subscriber list {list_name} ")
    elif type and option:
        config.append(f"initiator unclassified {option} {type} {list_name}" if list_name else f"initiator unclassified {option} {type}")
    elif initiator:
        config.append(f"initiator unclassified {value}")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ip subscriber on interface {interface}. Error\n{e}"
            )

def unconfigure_interface_ip_subscriber(device, interface, ip_session):
    """ Unconfigure ip subscriber on interface
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to configure
            ip_session ('str'): ip session to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring ip subscriber on interface
    """
    log.debug("Unconfigure ip subscriber on interface")
    config = [
             f"interface {interface}",
             f"no ip subscriber {ip_session}"
            ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ip subscriber on interface {interface}. Error\n{e}"
            )

def configure_ip_cef(device, option):
    """ Configure ip cef on device
        Args:
            device ('obj'): device to use
            option ('str'): option to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring ip cef on device
    """
    log.debug("Configure ip cef on device")
    config = [f"ip cef {option}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ip cef on device. Error\n{e}"
            )

def unconfigure_ip_cef(device, option):
    """ Unconfigure ip cef on device
        Args:
            device ('obj'): device to use
            option ('str'): option to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring ip cef on device
    """
    log.debug("Unconfigure ip cef on device")
    config = [f"no ip cef {option}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ip cef on device. Error\n{e}"
            )

def config_ip_dhcp_client(device, option=None, value=None, inform_trans=None, discover_trans=None, timeout=None, dns=False, update=None):
    """ Configure ip dhcp-client on device
        Args:
            device ('obj'): device to use
            option ('str',Optional): option to configure (eg. broadcast-flag, forcerenew)
            value ('int',Optional): metric value to configure. Default is None
            inform_trans ('int',Optional): Maximum number of DHCP Inform transmissions.
            discover_trans ('int',Optional): Maximum number of DHCP Discover transmissions
            timeout ('int',Optional): Timeout (in seconds) between Inform/Discover retransmission
            dns ('bool',Optional): Configure DNS. Default is False
            update ('str',Optional):  Ask server to perform no updates or update both
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring ip dhcp-client on device
    """
    log.debug("Configure ip dhcp-client on device")
    config = []
    if option in ['broadcast-flag', 'forcerenew']:
        config.append(f"ip dhcp-client {option}")
    if value is not None:
        config.append(f"ip dhcp-client default-router distance {value}")
    elif inform_trans is not None:
        if discover_trans is not None:
            if timeout is not None:
                config.append(f"ip dhcp-client network-discovery informs {inform_trans} discovers {discover_trans} period {timeout}")
            else:
                config.append(f"ip dhcp-client network-discovery informs {inform_trans} discovers {discover_trans}")
        else:
            config.append(f"ip dhcp-client network-discovery informs {inform_trans}")
    elif dns:
        if update is not None:
            config.append(f"ip dhcp-client update dns server {update}")
        else:
            config.append(f"ip dhcp-client update dns")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ip dhcp-client on device. Error\n{e}"
            )

def unconfig_ip_dhcp_client(device, option=None, value=None, inform_trans=None, discover_trans=None, timeout=None, dns=False, update=None):
    """ Unconfigure ip dhcp-client on device
        Args:
            device ('obj'): device to use
            option ('str'): option to configure (eg. broadcast-flag, forcerenew)
            value ('int', optional): metric value to configure. Default is None
            inform_trans ('int', optional): Maximum number of DHCP Inform transmissions.
            discover_trans ('int', optional): Maximum number of DHCP Discover transmissions
            timeout ('int', optional): Timeout (in seconds) between Inform/Discover retransmission
            dns ('bool', optional): Configure DNS. Default is False
            update ('str', optional):  Ask server to perform no updates or update both
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring ip dhcp-client on device
    """
    log.debug("Unconfigure ip dhcp-client on device")
    config = [f"no ip dhcp-client {option}"]
    config = []
    if option in ['broadcast-flag', 'forcerenew']:
        config.append(f"no ip dhcp-client {option}")
    if value is not None:
        config.append(f"no ip dhcp-client default-router distance {value}")
    elif inform_trans is not None:
        if discover_trans is not None:
            if timeout is not None:
                config.append(f"no ip dhcp-client network-discovery informs {inform_trans} discovers {discover_trans} period {timeout}")
            else:
                config.append(f"no ip dhcp-client network-discovery informs {inform_trans} discovers {discover_trans}")
        else:
            config.append(f"no ip dhcp-client network-discovery informs {inform_trans}")
    elif dns:
        if update is not None:
            config.append(f"no ip dhcp-client update dns server {update}")
        else:
            config.append(f"no ip dhcp-client update dns")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ip dhcp client on device. Error\n{e}"
            )

def configure_ip_dhcp_server(device, tag=None, option=None, type=None, lease=False):
    """ Configure ip dhcp-server on device
        Args:
            device ('obj'): device to use
            tag ('str'): options to configure (eg. name, query, vrf)
            option ('str'): option to configure (eg. check-source, retries, timeout)
            type ('str'): value to configure
            lease ('bool', optional): Set global lease query parameters
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring ip dhcp-server on device
    """
    log.debug("Configure ip dhcp-server on device")
    config = []
    if tag:
        config.append(f"ip dhcp-server {tag}")
    elif lease:
        if option is not None:
            config.append(f"ip dhcp-server query lease {option} {type}")
        else:
            config.append(f"ip dhcp-server query lease check-source")
    else:
        config.append(f"ip dhcp-server vrf {option} {type}")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ip dhcp server on device. Error\n{e}"
            )

def unconfigure_ip_dhcp_server(device, tag=None, option=None, type=None, lease=False):
    """ Unconfigure ip dhcp-server on device
        Args:
            device ('obj'): device to use
            tag ('str'): options to configure (eg. name, query, vrf)
            option ('str'): option to configure (eg. check-source, retries, timeout)
            type ('str'): value to configure
            lease ('bool', optional): Set global lease query parameters
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring ip dhcp-server on device
    """
    log.debug("Unconfigure ip dhcp-server on device")
    config = []
    if tag:
        config.append(f"no ip dhcp-server {tag}")
    elif lease:
        if option is not None:
            config.append(f"no ip dhcp-server query lease {option} {type}")
        else:
            config.append(f"no ip dhcp-server query lease check-source")
    else:
        config.append(f"no ip dhcp-server vrf {option} {type}")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ip dhcp server on device. Error\n{e}"
            )

def  configure_tftp_server(device, storage, config_file):
    """ Configure tftp-server on device
        Args:
            device ('obj'): device to use
            storage ('str'): storage to configure (eg. flash, bootflash)
            config_file ('str'): configuration file to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring tftp server on device
    """
    log.debug("Configure tftp-server on device")
    config = [f"tftp-server {storage}{config_file}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure tftp-server on device. Error\n{e}"
            )

def unconfigure_tftp_server(device, storage, config_file):
    """ Unconfigure tftp-server on device
        Args:
            device ('obj'): device to use
            storage ('str'): storage to configure (eg. flash, bootflash)
            config_file ('str'): configuration file to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring tftp server on device
    """
    log.debug("Unconfigure tftp-server on device")
    config = [f"no tftp-server {storage}{config_file}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure tftp-server on device. Error\n{e}"
            )

def configure_interface_service_policy_type_control_default(device, interface, policy_name):
    """ Configure interface service-policy type control default
        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured #example "interface vlan 100"
            policy_name ('str'): name of the policy to be configured
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure service-policy type control default on the interface
    """
    log.debug("Configuring service-policy type control default on the interface")
    config = [f'interface {interface}',
              f'service-policy type control default {policy_name}']
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure interface service-policy type control default on the interface {interface}. Error\n{e}"
        )

def configure_ip_dhcp_class_static(device, option, description= None, relay=False, hex_string=None, bit_mask=None):
    """ Configure ip dhcp class static
        Args:
            device ('obj'): device to use
            option ('str'): option to configure
            description ('str'): Up to 240 characters describing this class #example - ciscoworkspace
            relay ('bool'): relay information #example - True, False
            bit_mask ('str'): bit mask #example - ffffff
            hex_string ('str'): hex string #example - aabbcc
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ip dhcp class static
    """
    log.debug("Configuring ip dhcp class {option}")
    config =  [f"ip dhcp class {option}"]
    if description:
        config.append(f'remark {description}')
    elif relay:
        config.append(f'relay agent information')
        if hex_string and bit_mask:
            config.append(f'relay-information hex {hex_string} mask {bit_mask}')
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ip dhcp class static on {device}. Error\n{e}"
        )

def configure_ipv6_dhcp_pool(device, pool_name, address_prefix, bootfile_url):
    """ Configure IPv6 DHCP pool
        Args:
            device ('obj'): device to use
            pool_name ('str'): name of the DHCPv6 pool to be created
            address_prefix ('str'): IPv6 address prefix
            bootfile_url ('str'): URL for the bootfile
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure IPv6 DHCP pool
    """
    log.info(f"Configuring IPv6 DHCP pool {pool_name} with address prefix {address_prefix} and bootfile URL {bootfile_url}")

    config_commands = [
        f"ipv6 dhcp pool {pool_name}",
        f"address prefix {address_prefix}",
        f"bootfile-url {bootfile_url}"
    ]

    try:
        device.configure(config_commands)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure IPv6 DHCP pool {pool_name}. Error: {e}"
        )    

def configure_tftp_server_boot(device, file_path):
    """ Configure TFTP server
        Args:
            device ('obj'): device to use
            file_path ('str'): path to the file to be served by TFTP
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure TFTP server
    """
    log.debug(f"Configuring TFTP server with file {file_path}")
    config = [
        f"tftp-server {file_path}"
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure TFTP server with file {file_path}. Error:\n{e}"
        )
