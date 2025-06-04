"""Common configure functions for TACACS and RADIUS server"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_tacacs_server(device, server_config):
    """ Configure tacacs server

        Args:
            device ('obj'): Device object
            server_configs('list'): List of configuration for servers
                Each dictionary in the list contains following keys:
                    host ('str'): host ip address
                    timeout ('int'): server time out value in seconds
                    key_type ('int'): key type for tacacs server
                    key ('str'): key value from tacacs server
                    server ('str'): server ip address/ipv6/fqdn for address configuration
                    address_type ('str'): Type of server address - 'ipv4', 'ipv6', or 'fqdn'. Default is 'ipv4'
                    single_connection ('bool'): Enable single-connection
                    tls_port ('int'): Port number for TLS connection
                    tls_idle_timeout ('int'): Idle timeout for TLS connection
                    tls_connection_timeout ('int'): Connection timeout for TLS
                    tls_retries ('int'): Number of retries for TLS connection
                    tls_trustpoint_client ('str'): Client trustpoint name
                    tls_trustpoint_server ('str'): Server trustpoint name
                    tls_source_interface ('str'): Source interface for TLS
                    tls_ip_tacacs_source_interface ('str'): Source interface for IPv4 TLS
                    tls_ip_vrf_forwarding ('str'): VRF forwarding for IPv4 TLS
                    tls_ipv6_tacacs_source_interface ('str'): Source interface for IPv6 TLS
                    tls_ipv6_vrf_forwarding ('str'): VRF forwarding for IPv6 TLS
                    tls_match_server_identity_dns_id ('str'): TLS server identity DNS-ID
                    tls_match_server_identity_ip_address ('str'): TLS server identity IP address
                    tls_match_server_identity_srv_id ('str'): TLS server identity SRV-ID
                ex.)
                    [
                        {
                            'host': 'TACACS_SERVER',
                            'timeout': 10,
                            'key_type': 7,
                            'key': '01239132C123',
                            'server': '192.168.21.1',
                            'address_type': 'ipv4',
                            'single_connection': True,
                            'tls_port': 49,
                            'tls_idle_timeout': 60,
                            'tls_connection_timeout': 5,
                            'tls_retries': 3,
                            'tls_trustpoint_client': 'CLIENT_TP',
                            'tls_trustpoint_server': 'SERVER_TP',
                            'tls_source_interface': 'GigabitEthernet0/0',
                            'tls_ip_tacacs_source_interface': 'GigabitEthernet1',
                            'tls_ip_vrf_forwarding': 'Mgmt-vrf',
                            'tls_ipv6_tacacs_source_interface': 'GigabitEthernet1',
                            'tls_ipv6_vrf_forwarding': 'Mgmt-vrf',
                            'tls_match_server_identity_dns_id': 'cisco.com',
                            'tls_match_server_identity_ip_address': '10.0.0.1',
                            'tls_match_server_identity_srv_id': 'cisco.com',
                        },
                        {
                            'host': 'tacacs.cisco.com',
                            'timeout': 10,
                            'key_type': 7,
                            'key': '01239132C123',
                            'server': 'tacacs.cisco.com',
                            'address_type': 'fqdn'
                        },
                        {
                            'host': 'TACACS_SERVER_IPV6',
                            'timeout': 10,
                            'key_type': 7,
                            'key': '01239132C123',
                            'server': '2001:db8::1',
                            'address_type': 'ipv6'
                        }
                    ]

        Returns:
            Response received from configuring the command
        Raises:
            SubCommandFailure: Failed configuring tacacs server
    """

    config = []
    for sc in server_config:
        if "host" in sc:
            config.append("tacacs server {}\n".format(sc["host"]))
            
            # Handle different address types
            address_type = sc.get("address_type", "ipv4")  # Default to ipv4 if not specified
            if address_type == "ipv4":
                config.append("address ipv4 {}\n".format(sc["server"]))
            elif address_type == "ipv6":
                config.append("address ipv6 {}\n".format(sc["server"]))
            elif address_type == "fqdn":
                config.append("address fqdn {}\n".format(sc["server"]))

        if "single_connection" in sc and sc["single_connection"]:
            config.append("single-connection\n")

        if "timeout" in sc:
            config.append("timeout {}\n".format(sc["timeout"]))
        if "key_type" in sc and "key" in sc:
            config.append(
                "key {} {}\n".format(sc["key_type"], sc["key"])
            )
        
        # Add TLS configuration options
        if "tls_port" in sc:
            config.append("tls port {}\n".format(sc["tls_port"]))

        if "tls_idle_timeout" in sc:
            config.append("tls idle-timeout {}\n".format(sc["tls_idle_timeout"]))

        if "tls_connection_timeout" in sc:
            config.append("tls connection-timeout {}\n".format(sc["tls_connection_timeout"]))

        if "tls_retries" in sc:
            config.append("tls retries {}\n".format(sc["tls_retries"]))

        if "tls_trustpoint_client" in sc:
            config.append("tls trustpoint client {}\n".format(sc["tls_trustpoint_client"]))

        if "tls_trustpoint_server" in sc:
            config.append("tls trustpoint server {}\n".format(sc["tls_trustpoint_server"]))
        
        # Add new IPv4 TLS configuration options
        if "tls_ip_tacacs_source_interface" in sc:
            config.append("tls ip tacacs source-interface {}\n".format(sc["tls_ip_tacacs_source_interface"]))

        if "tls_ip_vrf_forwarding" in sc:
            config.append("tls ip vrf forwarding {}\n".format(sc["tls_ip_vrf_forwarding"]))

        # Add new IPv6 TLS configuration options
        if "tls_ipv6_tacacs_source_interface" in sc:
            config.append("tls ipv6 tacacs source-interface {}\n".format(sc["tls_ipv6_tacacs_source_interface"]))

        if "tls_ipv6_vrf_forwarding" in sc:
            config.append("tls ipv6 vrf forwarding {}\n".format(sc["tls_ipv6_vrf_forwarding"]))

        # Add TLS match server identity configuration options
        if "tls_match_server_identity_dns_id" in sc:
            config.append("tls match-server-identity dns-id {}\n".format(sc["tls_match_server_identity_dns_id"]))

        if "tls_match_server_identity_ip_address" in sc:
            config.append("tls match-server-identity ip-address {}\n".format(sc["tls_match_server_identity_ip_address"]))

        if "tls_match_server_identity_srv_id" in sc:
            config.append("tls match-server-identity srv-id {}\n".format(sc["tls_match_server_identity_srv_id"]))

        config.append("exit\n")

    try:
        response = device.configure("".join(config))
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure tacacs server on device {device}".format(
                device=device.name
            )
        )
    return response


def configure_radius_server(device, server_config):
    """ Configure radius server

        Args:
            device ('obj'): Device object
            server_config('dict'): Dictionary of configuration for server
                dictionary contains following keys:
                    server_name ('str'): Radius server name
                    ipv4 (Hostname or A.B.C.D):  IPv4 Address of radius server
                    ipv6 (Hostname or X:X:X:X::X):  IPv6 Address of radius server
                    auth_port (<0-65534>): UDP port for RADIUS authentication server
                    acct_port (<0-65534>): UDP port for RADIUS accounting server
                    key_encryption (int(0,6,7)): 0(UNENCRYPTED key), 6(ENCRYPTED key), 7(HIDDEN key)
                    key (LINE): Radius server pre shared secret key
                    timeout (<1-1000>): Time to wait (in seconds) for this radius server to reply
                    retransmit (<0-100>): Number of retries to active server (overrides default)
                    dscp_auth (<1-63>): Radius DSCP (Differentiated Services Code Point) marking value for Authentication
                    dscp_acct (<1-63>): Radius DSCP (Differentiated Services Code Point) marking value for Accounting
        Returns:
            None
        Raises:
            SubCommandFailure

        ex.)
            {
                'server_name': 'radius_server',
                'ipv4': '11.15.23.213',
                'auth_port': '1812,
                'acct_port': '1813',
                'key_encryption': '7',
                'key': 'Cisco',
                'timeout': '100',
                'retransmit': '5',
                'dscp_auth': '20',
                'dscp_acct': '10'
            }

        configures below cli commands:
            'radius server radius_server',
            'address ipv4 11.15.23.213 auth-port 1812 acct-port 1813',
            'key 7 Cisco',
            'timeout 100',
            'retransmit 5',
            'dscp auth 20',
            'dscp acct 10'
    """

    config_list = []

    # radius server <server_name>
    if 'server_name' in server_config:
        config_list.append("radius server {}".format(server_config['server_name']))

    # address ipv4 <ipv4> auth-port <auth_port> acct-port <acct_port> |
    # address ipv4 <ipv4> acct-port <acct_port>
    if 'ipv4' in server_config:
        if 'auth_port' in server_config and 'acct_port' in server_config:
            config_list.append("address ipv4 {} auth-port {} acct-port {}".
                               format(server_config['ipv4'], server_config['auth_port'], server_config['acct_port']))
        elif 'auth_port' not in server_config and 'acct_port' in server_config:
            config_list.append("address ipv4 {} acct-port {}".format(server_config['ipv4'], server_config['acct_port']))

    # address ipv6 <ipv6> auth-port <auth_port> acct-port <acct_port> |
    # address ipv6 <ipv6> acct-port <acct_port>
    if 'ipv6' in server_config:
        if 'auth_port' in server_config and 'acct_port' in server_config:
            config_list.append("address ipv6 {} auth-port {} acct-port {}".format(
                server_config['ipv6'], server_config['auth_port'], server_config['acct_port']
            ))
        elif 'auth_port' not in server_config and 'acct_port' in server_config:
            config_list.append("address ipv6 {} acct-port {}".format(
                server_config['ipv6'], server_config['acct_port']
            ))

    # key <key_encryption> <key> |
    # key <key>
    if 'key_encryption' in server_config:
        config_list.append("key {} {}".format(server_config['key_encryption'], server_config['key']))
    elif 'key' in server_config:
        config_list.append("key {}".format(server_config['key']))

    # timeout <timeout>
    if 'timeout' in server_config:
        config_list.append("timeout {}".format(server_config['timeout']))

    # retransmit <retransmit>
    if 'retransmit' in server_config:
        config_list.append("retransmit {}".format(server_config['retransmit']))

    # dscp auth <dscp_auth>
    if 'dscp_auth' in server_config:
        config_list.append(f"dscp auth {server_config['dscp_auth']}")

    # dscp acct <dscp_acct>
    if 'dscp_acct' in server_config:
        config_list.append(f"dscp acct {server_config['dscp_acct']}")

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure radius server on device {device.name}. Error:\n{e}')

def unconfigure_radius_server(device, server_name):
    """ Unconfigure radius server
        Args:
            device ('obj'): Device object
            server_name('str'): Name for the radius server configuration
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = f'no radius server {server_name}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to unconfigure radius server on device {device.name}. Error:\n{e}')

def configure_radius_server_dtls_trustpoint(device, server_name=None, trustpoint_server=None, trustpoint_client=None):
    """ Configure radius server dtls trustpoint

        Args:
            device ('obj'): Device object
            server_name('str', optional): Radius server name
            trustpoint_server('str', optional): Trustpoint server name
            trustpoint_client('str', optional): Trustpoint client name

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config_list = []

    if server_name:
        config_list.append(f'radius server {server_name}')
    if trustpoint_server:
        config_list.append(f'dtls trustpoint server {trustpoint_server}')
    if trustpoint_client:
        config_list.append(f'dtls trustpoint client {trustpoint_client}')

    if not config_list:
        raise ValueError("At least one of server_name, trustpoint_server, or trustpoint_client must be provided")

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure radius server dtls trustpoint on device {device.name}. Error:\n{e}')

def configure_radius_server_with_dtls(device, server_name='TMP_NAME', enable_dtls=False):
    """ Configure radius server with optional DTLS

        Args:
            device ('obj'): Device object
            server_name ('str', optional): Radius server name. Defaults to 'TMP_NAME'.
            enable_dtls ('bool', optional): Flag to enable DTLS. Defaults to False.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config_list = [f'radius server {server_name}']

    if enable_dtls:
        config_list.append('dtls')

    config_list.append('exit')

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure radius server with DTLS on device {device.name}. Error:\n{e}')

def configure_radius_server_dtls_connection(device, server_name='TMP_NAME', dtls_connectiontimeout=None):
    """ Configure radius server with optional DTLS and connection timeout

        Args:
            device ('obj'): Device object
            server_name ('str', optional): Radius server name. Defaults to 'TMP_NAME'.
            dtls_connectiontimeout ('int', optional): Connection timeout value for DTLS. Defaults to None.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config_list = [f'radius server {server_name}']

    if dtls_connectiontimeout is not None:
        config_list.append(f'dtls connectiontimeout {dtls_connectiontimeout}')

    config_list.append('exit')

    log.info(f"Configuring radius server with the following commands: {config_list}")

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure radius server with DTLS and connection timeout on device {device.name}. Error:\n{e}')

def configure_radius_server_dtls_ip(device, server_name='TMP_NAME', source_interface='vlan 199'):
    """ Configure radius server with DTLS and source interface

        Args:
            device ('obj'): Device object
            server_name ('str', optional): Radius server name. Defaults to 'TMP_NAME'.
            source_interface ('str', optional): Source interface for radius. Defaults to 'vlan 199'.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config_list = [
        f'radius server {server_name}',
        'dtls',
        f'ip radius source-interface {source_interface}',
        'exit'
    ]

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure radius server with DTLS on device {device.name}. Error:\n{e}')

def configure_radius_server_dtls_idletimeout(device, server_name='TMP_NAME', dtls_idletimeout=None):
    """ Configure radius server with optional DTLS and idle timeout

        Args:
            device ('obj'): Device object
            server_name ('str', optional): Radius server name. Defaults to 'TMP_NAME'.
            dtls_idletimeout ('int', optional): Idle timeout value for DTLS. Defaults to None.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config_list = [f'radius server {server_name}']

    log.debug(f"Configuring radius server with the following commands: {config_list}")

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure radius server with DTLS and idle timeout on device {device.name}. Error:\n{e}')

def configure_radius_server_dtls_watchdoginterval(device, server_name=None, watchdoginterval=None):
    """ Configure radius server dtls watchdoginterval
        Args:
            device ('obj'): Device object
            server_name('str', optional): Radius server name
            watchdoginterval('int', optional): DTLS watchdog interval
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config_list = []

    if server_name:
        config_list.append(f'radius server {server_name}')
    if watchdoginterval:
        config_list.append(f'dtls watchdoginterval {watchdoginterval}')

    if not config_list:
        raise ValueError("At least one of server_name or watchdoginterval must be provided")

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure radius server dtls watchdoginterval on device {device.name}. Error:\n{e}')

def configure_radius_server_with_dtls_ipv6(device, server_name='TMP_NAME', source_interface='vlan 199'):
    """ Configure radius server with DTLS IPv6 source interface
        Args:
            device ('obj'): Device object
            server_name('str'): Radius server name
            source_interface('str'): Source interface for DTLS IPv6
            vlan('str'): Vlan for source interface
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config_list = [
        f'radius server {server_name}',
        f'dtls ipv6 radius source-interface {source_interface}'
    ]

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure radius server with DTLS IPv6 on device {device.name}. Error:\n{e}')


def configure_radius_server_dtls_port(device, server_name=None, dtls_port=None):
    """ Configure radius server dtls port
        Args:
            device ('obj'): Device object
            server_name('str', optional): Radius server name
            dtls_port('int', optional): DTLS port number

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config_list = []
    
    if server_name:
        config_list.append(f'radius server {server_name}')
    if dtls_port:
        config_list.append(f'dtls port {dtls_port}')
    
    if not config_list:
        raise ValueError("At least one of server_name or dtls_port must be provided")
    
    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure radius server dtls port on device {device.name}. Error:\n{e}')
