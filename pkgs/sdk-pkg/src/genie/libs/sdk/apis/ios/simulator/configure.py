"""Common configure functions for simulator"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_simulator_radius_server(device, server_ip, user_prefixes=None,
                                      client_ip=None, shared_secret=None,
                                      remove_prefixes=None):
    """ Configure simulator radius server on device

        Args:
            device (`obj`): Device object
            server_ip (`str`): RADIUS server IP address
            user_prefixes (`list`, optional): List of dicts with keys:
                - prefix (`str`): Username prefix
                - subscriber (`int` or `str`): Subscriber ID
                Defaults to None
            client_ip (`str`, optional): Client IP address. Defaults to None
            shared_secret (`str`, optional): Shared secret key. Defaults to None
            remove_prefixes (`list`, optional): List of prefix strings to remove
                (e.g. ['aaaa', 'bbbb']). Defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"simulator radius server {server_ip}"]
    if remove_prefixes:
        for prefix in remove_prefixes:
            cmd.append(f" no user-name prefix {prefix}")
    if user_prefixes:
        for up in user_prefixes:
            cmd.append(f" user-name prefix {up['prefix']} subscriber {up['subscriber']}")
    if client_ip and shared_secret:
        cmd.append(f" client {client_ip} shared-secret {shared_secret}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure simulator radius server {server_ip}. Error: {e}"
        )


def unconfigure_simulator_radius_server(device, server_ip):
    """ Unconfigure simulator radius server on device

        Args:
            device (`obj`): Device object
            server_ip (`str`): RADIUS server IP address
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(f"no simulator radius server {server_ip}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure simulator radius server {server_ip}. Error: {e}"
        )


def configure_simulator_radius_key(device, key):
    """ Configure simulator radius key on device

        Args:
            device (`obj`): Device object
            key (`str`): RADIUS key
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(f"simulator radius key {key}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure simulator radius key. Error: {e}"
        )


def unconfigure_simulator_radius_key(device, key):
    """ Unconfigure simulator radius key on device

        Args:
            device (`obj`): Device object
            key (`str`): RADIUS key
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(f"no simulator radius key {key}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure simulator radius key. Error: {e}"
        )


def configure_simulator_radius_subscriber(device, subscriber_id, service=None,
                                          attributes=None, vsas=None,
                                          authentication=None, remove_first=True,
                                          framed_prefix=None, negate=False):
    """ Configure simulator radius subscriber on device

        Args:
            device (`obj`): Device object
            subscriber_id (`int`): Subscriber ID number
            service (`str`, optional): Service type (e.g. 'framed', 'outbound').
                Defaults to None
            attributes (`list`, optional): List of dicts with keys:
                - id (`int`): Attribute number
                - type (`str`): Attribute type (e.g. 'numeric', 'string')
                - value (`int` or `str`): Attribute value
                Defaults to None
            vsas (`list`, optional): List of VSA strings
                (e.g. 'cisco generic 1 string "subscriber:accounting-list=acct1"')
                Defaults to None
            authentication (`str`, optional): Authentication string
                (e.g. 'user1 CoA secret123'). Defaults to None
            remove_first (`bool`, optional): Send 'no simulator radius subscriber'
                before configuring. Defaults to True
            framed_prefix (`str`, optional): Framed IPv6 prefix
                (e.g. '2001:db8:1::/64'). Defaults to None
            negate (`bool`, optional): If True, prepends 'no ' to framed_prefix
                and attribute lines. Defaults to False
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    no = "no " if negate else ""
    cmd = []
    if remove_first:
        cmd.append(f"no simulator radius subscriber {subscriber_id}")
    cmd.append(f"simulator radius subscriber {subscriber_id}")
    if service:
        cmd.append(f" service {service}")
    if framed_prefix:
        cmd.append(f" {no}framed ipv6 prefix {framed_prefix}")
    if authentication:
        cmd.append(f" authentication {authentication}")
    if vsas:
        for vsa in vsas:
            cmd.append(f" vsa {vsa}")
    if attributes:
        for attr in attributes:
            cmd.append(f" {no}attribute {attr['id']} {attr['type']} {attr['value']}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure simulator radius subscriber {subscriber_id}. Error: {e}"
        )


def unconfigure_simulator_radius_subscriber(device, subscriber_id):
    """ Unconfigure simulator radius subscriber on device

        Args:
            device (`obj`): Device object
            subscriber_id (`int`): Subscriber ID number
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(f"no simulator radius subscriber {subscriber_id}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure simulator radius subscriber {subscriber_id}. Error: {e}"
        )


def configure_service_simulator_radius(device, client_ip, access_ports,
                                       accounting_ports, host_ip, auth_port,
                                       acct_port):
    """ Configure service simulator radius server with client and host

        Args:
            device (`obj`): Device object
            client_ip (`str`): RADIUS client IP address
            access_ports (`str`): Access ports (e.g. '1812 1812')
            accounting_ports (`str`): Accounting ports (e.g. '1813 1813')
            host_ip (`str`): RADIUS host IP address
            auth_port (`str`): Authentication port
            acct_port (`str`): Accounting port
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        "service simulator radius server",
        f" simulator radius client {client_ip} access-ports"
        f" {access_ports} accounting-ports {accounting_ports}",
        f" simulator radius host {host_ip}"
        f" auth-port {auth_port} acct-port {acct_port}",
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure service simulator radius. Error: {e}"
        )


def unconfigure_service_simulator_radius(device, client_ip, access_ports,
                                         accounting_ports, host_ip, auth_port,
                                         acct_port):
    """ Unconfigure service simulator radius server with client and host

        Args:
            device (`obj`): Device object
            client_ip (`str`): RADIUS client IP address
            access_ports (`str`): Access ports (e.g. '1812 1812')
            accounting_ports (`str`): Accounting ports (e.g. '1813 1813')
            host_ip (`str`): RADIUS host IP address
            auth_port (`str`): Authentication port
            acct_port (`str`): Accounting port
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        "no service simulator radius server",
        f"no simulator radius client {client_ip} access-ports"
        f" {access_ports} accounting-ports {accounting_ports}",
        f"no simulator radius host {host_ip}"
        f" auth-port {auth_port} acct-port {acct_port}",
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure service simulator radius. Error: {e}"
        )
