"""Common configure functions for bgp"""

# Python
import logging
import re
import jinja2

# Genie
from genie.utils.timeout import Timeout
from unicon.eal.dialogs import Dialog, Statement

# Utils
from genie.libs.sdk.apis.iosxe.running_config.get import (
    get_running_config_section_dict,
)

# Steps
from pyats.aetest.steps import Steps

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_isis_network_entity(device,network_entity):
    """ Configure network_entity on ISIS router
        Args:
            device('obj'): device to configure on
            network_entity('str'): network_entity of device
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(
        "Configuring router ISIS on {hostname}\n"
        "    -isis network_entity: {network_entity}".format(
            hostname=device.hostname, network_entity=network_entity
        )
    )
    config = [
                'router isis',
                'net {network_entity}'.format(network_entity=network_entity)
            ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure network_entity {network_entity} on "
            "ISIS router:\n{e}".format(hostname=device.hostname, network_entity=network_entity, e=e)
        )

def remove_isis_configuration(device):
    """ Remove isis configuration
        Args:
            device ('obj'): Device object
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(
        "Remove  ISIS configuration on {hostname}\n"
    )
    config = [
                'no router isis',
            ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not  Remove  ISIS configuration on "
            .format(hostname=device.hostname, e=e)
        )

def config_interface_isis(device, interface,ipv6=False,mtu=None):
    """config ISIS on interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            ipv6 ('boolean',optional): Flag to configure IPv6 (Default False)
            mtu ('str',optional): mtu configuration on interface
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        'Configuring ISIS on interface {interface}\n'.format(interface=interface)
    )
    config = []
    config.append("interface {interface}".format(interface=interface))
    if ipv6:
        config.append("ipv6 router isis")
    else:
        config.append("ip router isis")
    if mtu:
        config.append("clns mtu {mtu}".format(mtu=mtu))
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure isis on interface {interface} on "
            .format(hostname=device.hostname, interface=interface, e=e)
        )

def unconfig_interface_isis(device, interface,ipv6=False):
    """Unconfig ISIS on interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            ipv6 ('boolean',optional): Flag to configure IPv6 (Default False)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Unconfiguring isis on interface {interface}\n".format(interface=interface)
    )
    config = []
    config.append("interface {interface}".format(interface=interface))
    if ipv6:
        config.append("no ipv6 router isis")
    else:
        config.append("no  ip router isis")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure isis on interface {interface} on "
            .format(hostname=device.hostname, interface=interface, e=e)
        )

def configure_isis_with_router_name_network_entity(device, router_name, network_entity=None):
    """ Configure isis with router name
        Args:
            device('obj'): device to configure on
            router_name ('str'):configure the isis router name
            network_entity('str',optional): network_entity of device
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(
        "Configuring isis with router name {router_name} on {hostname}".format(
            hostname=device.hostname, router_name=router_name, 
        )
    )
    config = []
    config.append('router isis {router_name}'.format(router_name=router_name))
    if network_entity:
        config.append('net {network_entity}'.format(network_entity=network_entity))
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure isis with router name {router_name} on {hostname}"
            "ISIS router:\n{e}".format(hostname=device.hostname, router_name=router_name, e=e)
        )

def unconfigure_isis_with_router_name(device,router_name):
    """ Unconfigure isis with router name
        Args:
            device('obj'): device to configure on
            router_name ('str'):configure the isis router name
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(
        "Configuring isis with router name {router_name} on {hostname}".format(
            hostname=device.hostname, router_name=router_name, 
        )
    )
    config = ['no router isis {router_name}'.format(router_name=router_name)]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure isis with router name {router_name} on {hostname}"
            "ISIS router:\n{e}".format(hostname=device.hostname, router_name=router_name, e=e)
        )

def config_interface_with_isis_router_name(device, interface, router_name):
    """config ISIS router name on interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            router_name ('str'):configure the isis router name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        'Configuring ISIS router name {router_name} on interface {interface}\n'.format(
        router_name=router_name,interface=interface)
    )
    config = []
    config.append("interface {interface}".format(interface=interface))
    config.append("ip router isis {router_name}".format(router_name=router_name))
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure isis router name {router_name} on interface {interface} on {hostname}"
            .format(hostname=device.hostname, router_name=router_name, interface=interface, e=e)
        )

def unconfig_interface_isis_router_name(device, interface, router_name):
    """Unconfig ISIS router name on interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            router_name ('str'):configure the isis router name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Unconfiguring isis {router_name} on interface {interface}\n".format(router_name=router_name,interface=interface)
    )
    config = []
    config.append("interface {interface}".format(interface=interface))
    config.append("no ip router isis {router_name}".format(router_name=router_name))
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure isis {router_name} on interface {interface} on {hostname}"
            .format(hostname=device.hostname, router_name=router_name, interface=interface, e=e)
            )

def configure_isis_keychain_key(device, keychain_name, key_id, text):
    """ Configures the authentication string for a key on a key-chain
        Args:
            device('obj'): device to configure on
            keychain_name ('str'): name of the key chain
            key_id('int'): id of the key on key chain (Range 0-2147483647)
            text('str'): The unencrypted user password (Maximum 80 characters)
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(
        "Configuring isis key with key-string on {hostname}".format(
            hostname=device.hostname 
        )
    )
    config = []
    config.append('key  chain {name}'.format(name=keychain_name))
    config.append('key {id}'.format(id=key_id))
    config.append('key-string {text}'.format(text=text))
    try:
        device.configure(config)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Could not configure isis with key-string on device {dev}. Error:\n{error}".format(
                dev=device.name,
                error=e
            )
        )

def unconfigure_isis_keychain_key(device, keychain_name):
    """ Unconfigures the isis key chain
        Args:
            device('obj'): device to configure on
            keychain_name ('str'): name of the key chain
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(
        "Unconfiguring isis key chain {name} on {hostname}".format(
            name=keychain_name,
            hostname=device.hostname 
        )
    )
    try:
        device.configure("no key chain {name}".format(name=keychain_name))
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Could not unconfigure isis key chain {name} on device {dev}. Error:\n{error}".format(
                name=keychain_name,
                dev=device.name,
                error=e
            )
        )

def configure_isis_authentication_mode(device, interface, mode, level=None):
    """ Configures the ISIS authentication mode
        Args:
            device('obj'): device to configure on
            interface ('str'): name of the interface
            mode('str'): Authentication mode for PDUs (md5 or text)
            level('str'): Level for ISIS authentication (level-1 or level-2)
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(
        "Configuring isis authentication mode {mode} on {dev}".format(
            mode=mode,
            dev=device.name
        )
    )
    config = []
    config.append('interface {interface}'.format(interface=interface))
    if level==None:
        config.append('isis authentication mode {mode}'.format(mode=mode))
    else:
        config.append('isis authentication mode {mode} {level}'.format(mode=mode, level=level))
    try:
        device.configure(config)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Could not configure isis authentication mode {mode} on device {dev}. Error:\n{error}".format(
                mode=mode,
                dev=device.name,
                error=e
            )
        )

def unconfigure_isis_authentication_mode(device, interface, mode, level=None):
    """ Unconfigures the ISIS authentication mode
        Args:
            device('obj'): device to configure on
            interface ('str'): name of the interface
            mode('str'): Authentication mode for PDUs (md5 or text)
            level('str'): Level for ISIS authentication (level-1 or level-2)
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(
        "Unconfiguring isis authentication mode {mode} on {dev}".format(
            mode=mode,
            dev=device.name
        )
    )
    config = []
    config.append('interface {interface}'.format(interface=interface))
    if level==None:
        config.append('no isis authentication mode {mode}'.format(mode=mode))
    else:
        config.append('no isis authentication mode {mode} {level}'.format(mode=mode, level=level))
    try:
        device.configure(config)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Could not unconfigure isis authentication mode {mode} on device {dev}. Error:\n{error}".format(
                mode=mode,
                dev=device.name,
                error=e
            )
        )

def configure_isis_authentication_key_chain(device, interface, key_chain_name):
    """ Configures the ISIS authentication Key-chain
        Args:
            device('obj'): device to configure on
            interface ('str'): name of the interface
            key_chain_name('str'): Name of the key-chain
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(
        "Configuring isis authentication key-chain {name} on {dev}".format(
            name=key_chain_name,
            dev=device.name
        )
    )
    config = []
    config.append('interface {interface}'.format(interface=interface))
    config.append('isis authentication key-chain {name}'.format(name=key_chain_name))
    try:
        device.configure(config)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Could not configure isis authentication key-chain {name} on device {dev}. Error:\n{error}".format(
                name=key_chain_name,
                dev=device.name,
                error=e
            )
        )

def unconfigure_isis_authentication_key_chain(device, interface, key_chain_name):
    """ Unconfigures the ISIS authentication Key-chain
        Args:
            device('obj'): device to configure on
            interface ('str'): name of the interface
            key_chain_name('str'): Name of the key-chain
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(
        "Unconfiguring isis authentication key-chain {name} on {dev}".format(
            name=key_chain_name,
            dev=device.name
        )
    )
    config = []
    config.append('interface {interface}'.format(interface=interface))
    config.append('no isis authentication key-chain {name}'.format(name=key_chain_name))
    try:
        device.configure(config)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Could not unconfigure isis authentication key-chain {name} on device {dev}. Error:\n{error}".format(
                name=key_chain_name,
                dev=device.name,
                error=e
            )
        )

def configure_isis_circuit_type(device, interface, level=None):
    """ Configures the ISIS ciruit type
        Args:
            device('obj'): device to configure on
            interface ('str'): name of the interface
            level('str'): level for ISIS circuit type (level-1, level-1-2 or level-2-only)
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(
        "Configuring isis circuit-type on interface {interface} on {dev}".format(
            interface=interface,
            dev=device.name
        )
    )
    config = []
    config.append('interface {interface}'.format(interface=interface))
    if level==None:
        config.append('isis circuit-type')
    else:
        config.append('isis circuit-type {level}'.format(level=level))
    try:
        device.configure(config)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Could not configure isis circuit-type on interface {interface} on device {dev}. Error:\n{error}".format(
                interface=interface,
                dev=device.name,
                error=e
            )
        )

def unconfigure_isis_circuit_type(device, interface):
    """ Unconfigures the ISIS ciruit type
        Args:
            device('obj'): device to configure on
            interface ('str'): name of the interface
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(
        "Unconfiguring isis circuit-type on interface {interface} on {dev}".format(
            interface=interface,
            dev=device.name
        )
    )
    config = []
    config.append('interface {interface}'.format(interface=interface))
    config.append('no isis circuit-type')
    try:
        device.configure(config)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Could not unconfigure isis circuit-type on interface {interface} on device {dev}. Error:\n{error}".format(
                interface=interface,
                dev=device.name,
                error=e
            )
        )

def configure_isis_password(device, interface, password):
    """ Configures the ISIS password
        Args:
            device('obj'): device to configure on
            interface ('str'): name of the interface
            password('str'): password for ISIS
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(
        "Configuring isis password on {interface} on {dev}".format(
            interface=interface,
            dev=device.name
        )
    )
    config = []
    config.append('interface {interface}'.format(interface=interface))
    config.append('isis password {pwd}'.format(pwd=password))
    try:
        device.configure(config)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Could not configure isis password on interface {interface} on device {dev}. Error:\n{error}".format(
                interface=interface,
                dev=device.name,
                error=e
            )
        )

def unconfigure_isis_password(device, interface, password):
    """ Unconfigures the ISIS password
        Args:
            device('obj'): device to configure on
            interface ('str'): name of the interface
            password('str'): password for ISIS
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(
        "Unconfiguring isis password on {interface} on {dev}".format(
            interface=interface,
            dev=device.name
        )
    )
    config = []
    config.append('interface {interface}'.format(interface=interface))
    config.append('no isis password {pwd}'.format(pwd=password))
    try:
        device.configure(config)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Could not unconfigure isis password on interface {interface} on device {dev}. Error:\n{error}".format(
                interface=interface,
                dev=device.name,
                error=e
            )
        )

def configure_isis_network_type(device, network_entity, is_type=None, bfd=None, adjacency=None):
    """ Configure network_entity on ISIS router
        Args:
            device('obj'): device to configure on
            network_entity('str'): network_entity of device
            is_type('str', optional): level-1 (or) Level-2 , by default is None
            bfd ('str', optional) : bfd name, default value is None
            adjacency ('str', optional) : adjacency details, default value is None
        Return:
            N/A
        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(
        "configure the isis network type {is_type}\n".format(is_type=is_type)
    )
    config = []
    config.append("router isis")
    config.append("net {network_entity}".format(network_entity=network_entity))
    if is_type:
        config.append("is-type {is_type}".format(is_type=is_type))
    if bfd:
        config.append("bfd {bfd}".format(bfd=bfd))
    if adjacency:
        config.append("{adjacency}".format(adjacency=adjacency))
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure isis network type {is_type}"
            .format(is_type=is_type, e=e)
        )

def configure_isis_redistributed_connected(device):
    """ configure redistribute connected under isis
        Args:
            device (`obj`): device to execute on
        Return:
            None
        Raises:
            SubCommandFailure
    """
    config=["router isis"]
    config.append("redistribute connected")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to configure redistribute connected under isis on {device} ".format(device=device, e=e)
        )

def clear_isis(device):
    """ clear isis
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("clear isis on {device}".format(device=device))

    dialog = Dialog([Statement(pattern=r'\[confirm\].*', action='sendline(\r)',loop_continue=True,continue_timer=False)])

    try:
        device.execute("clear isis *", reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear isis on {device}. Error:\n{error}".format(device=device, error=e)
        )

def configure_isis_router_configs(device, max_paths=None):
    """ Configures ISIS Router
        Args:
            device ('obj'):                 device to use
            max_paths ('int', optional):    Number of paths (Default is None)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config_list = ["router isis"]

    if max_paths:
        config_list.append(f"maximum-paths {max_paths}")
    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure Router ISIS. Error:\n{error}'.format(error=e)
        )


def unconfigure_isis_router_configs(device, max_paths=None):
    """ Unconfigures ISIS Router
        Args:
            device ('obj'):  device to use
            max_paths ('int', optional):  Number of paths (Default is None)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config_list = ["router isis"]

    if max_paths:
        config_list.append(f"no maximum-paths {max_paths}")

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not Unconfigure Router ISIS. Error:\n{error}'.format(error=e)
        )
