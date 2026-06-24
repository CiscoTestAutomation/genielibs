"""Common configure functions for dhcp"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

log = logging.getLogger(__name__)


def configure_interface_ip_dhcp_client(device, interface, option, type, tag=None, is_update=False):
    """ Configure ip dhcp client on the interface

        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured (eg. GigabitEthernet0/0)
            option ('str'): option to configure (eg. broadcast-flag, class-id, client-id, default-router, etc.)
            type ('str'): it can be for example clear, interface, ascii or hex
            tag ('str',Optional): it can be value of ascii or hex, interface or vlan name. Defaults to None
            is_update ('bool',Optional): when True, emit the ``ip dhcp client update <option> <type> [tag]`` form. Defaults to False
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ip dhcp client on the interface
    """
    log.debug("Configuring ip dhcp client on the interface")
    cmd = [f"interface {interface}"]
    cmd.append(f"ip dhcp client {option} {type}")
    if option in ['authentication', 'class-id', 'client-id', 'default-router', 'option', 'request', 'route', 'vendor-class']:
        if tag:
            cmd.append(f"ip dhcp client {option} {type} {tag}")
    elif is_update and tag:
        cmd.append(f"ip dhcp client update {option} {type} {tag}")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ip dhcp client on the interface {interface}. Error\n{e}"
        )


def unconfigure_interface_ip_dhcp_client(device, interface, option, type, tag=None, is_update=False):
    """ Unconfigure ip dhcp client on the interface

        Args:
            device ('obj'): device to use
            interface ('str'): name of the interface to be configured (eg. GigabitEthernet0/0)
            option ('str'): option to unconfigure (eg. broadcast-flag, class-id, client-id, default-router, etc.)
            type ('str'): it can be for example clear, interface, ascii or hex
            tag ('str',Optional): it can be value of ascii or hex, interface or vlan name. Defaults to None
            is_update ('bool',Optional): when True, emit the ``no ip dhcp client update <option> <type> [tag]`` form. Defaults to False
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure ip dhcp client on the interface
    """
    log.debug("Unconfiguring ip dhcp client on the interface")
    cmd = [f"interface {interface}"]
    cmd.append(f"no ip dhcp client {option} {type}")
    if option in ['authentication', 'class-id', 'client-id', 'default-router', 'option', 'request', 'route', 'vendor-class']:
        if tag:
            cmd.append(f"no ip dhcp client {option} {type} {tag}")
    elif is_update and tag:
        cmd.append(f"no ip dhcp client update {option} {type} {tag}")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ip dhcp client on the interface {interface}. Error\n{e}"
        )


def create_dhcp_pool(
    device, pool_name, network, mask, router_id,
    lease_days, lease_hrs, lease_mins,
):
    """ Create DHCP pool

    Creates the pool and configures the essential settings (network,
    default-router, lease). Optional sub-commands (vrf, dns-server,
    domain-name, lease infinite, multi-address default-router/dns) are
    handled by :func:`modify_dhcp_pool`.

        Args:
            device ('obj'): device to use
            pool_name ('str'): name of the pool to be created
            network ('str'): IP of the network pool
            mask ('str'): Subnet mask of the network pool
            router_id ('str'): Default router ID
            lease_days ('str' or 'int'): Number of days for the lease
            lease_hrs ('str' or 'int'): Number of hours for the lease
            lease_mins ('str' or 'int'): Number of minutes for the lease
        Returns:
            None
        Raises:
            SubCommandFailure: Failed creating dhcp pool
    """
    log.debug("Creating DHCP pool %s", pool_name)

    config = [
        f"ip dhcp pool {pool_name}",
        f"network {network} {mask}",
        f"default-router {router_id}",
        f"lease {lease_days} {lease_hrs} {lease_mins}",
    ]

    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            f"Could not configure DHCP pool {pool_name}"
        )


def remove_dhcp_pool(device, pool_name):
    """ Remove DHCP pool

        Args:
            device ('obj'): device to use
            pool_name ('str'): name of the pool to be removed
        Returns:
            None
        Raises:
            SubCommandFailure: Failed removing dhcp pool
    """
    log.debug("Removing DHCP pool %s", pool_name)

    try:
        device.configure(f"no ip dhcp pool {pool_name}")
    except SubCommandFailure:
        raise SubCommandFailure(
            f"Could not remove DHCP pool {pool_name}"
        )


def modify_dhcp_pool(
    device, pool_name, network=None, mask=None, router_id=None,
    lease_days=None, lease_hrs=None, lease_mins=None,
    lease_infinite=False, vrf=None, dns_server=None, domain_name=None,
    negate=False,
):
    """ Add or remove sub-commands under an existing DHCP pool

    The pool itself is preserved; only the supplied sub-commands are
    configured (``negate=False``) or removed (``negate=True``).
    ``router_id`` and ``dns_server`` accept either a single string or a
    list/tuple of addresses.

        Args:
            device ('obj'): device to use
            pool_name ('str'): name of the existing pool to modify
            network ('str', optional): IP of the network pool.
                Defaults to None
            mask ('str', optional): Subnet mask of the network pool.
                Defaults to None
            router_id ('str' or list, optional): default-router
                address(es). Defaults to None
            lease_days ('str' or 'int', optional): Number of days for
                the lease. Defaults to None
            lease_hrs ('str' or 'int', optional): Number of hours for
                the lease. Defaults to None
            lease_mins ('str' or 'int', optional): Number of minutes
                for the lease. Defaults to None
            lease_infinite ('bool', optional): when True targets
                ``lease infinite`` (overrides lease_days/hrs/mins).
                Defaults to False
            vrf ('str', optional): vrf name. Defaults to None
            dns_server ('str' or list, optional): dns-server
                address(es). Defaults to None
            domain_name ('str', optional): domain-name. Defaults to None
            negate ('bool', optional): when True, prefixes each
                sub-command with ``no`` to remove it. Defaults to False
        Returns:
            None
        Raises:
            SubCommandFailure: Failed modifying dhcp pool
    """
    log.debug("Modifying DHCP pool %s (negate=%s)", pool_name, negate)

    dialog = Dialog(
        [
            Statement(
                pattern=r'.*Continue\? +\[yes\].*',
                action='sendline()'
            )
        ]
    )

    prefix = "no " if negate else ""
    config = [f"ip dhcp pool {pool_name}"]
    if vrf:
        config.append(f"{prefix}vrf {vrf}")
    if network and mask:
        config.append(f"{prefix}network {network} {mask}")
    if router_id:
        if isinstance(router_id, (list, tuple)):
            config.append(f"{prefix}default-router {' '.join(router_id)}")
        else:
            config.append(f"{prefix}default-router {router_id}")
    if dns_server:
        if isinstance(dns_server, (list, tuple)):
            config.append(f"{prefix}dns-server {' '.join(dns_server)}")
        else:
            config.append(f"{prefix}dns-server {dns_server}")
    if domain_name:
        config.append(f"{prefix}domain-name {domain_name}")
    if lease_infinite:
        config.append(f"{prefix}lease infinite")
    elif lease_days is not None:
        parts = [str(lease_days)]
        if lease_hrs is not None:
            parts.append(str(lease_hrs))
        if lease_mins is not None:
            parts.append(str(lease_mins))
        config.append(f"{prefix}lease {' '.join(parts)}")

    if len(config) == 1:
        log.debug("No sub-commands provided to modify_dhcp_pool; nothing to do")
        return

    try:
        device.configure(config, reply=dialog)
    except SubCommandFailure:
        raise SubCommandFailure(
            f"Could not modify DHCP pool {pool_name}"
        )
