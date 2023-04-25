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
            server_config('list'): List of configuration for server
                dictionary contains following 3 keys:
                    host ('str'): host ip address
                    timeout ('int'): server time out value in seconds
                    key_type ('int'): key type for tacacs server
                    key ('str'): key value from tacacs server
                    server ('str'): server ip address
                ex.)
                    [
                        {
                            'host': '192.168.21.1',
                            'timeout': 10,
                            'key_type': 7,
                            'key': '01239132C123',
                            'server': '192.168.21.1'
                        },
                        {
                            'host': '192.168.21.2',
                            'timeout': 10,
                            'key_type': 7,
                            'key': '01239132C123',
                            'server': '192.168.21.2'
                        }
                    ] 
                        
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring tacacs server 
    """

    config = []
    for sc in server_config:
        if "host" in sc:
            config.append("tacacs server {}\n".format(sc["host"]))
            config.append("address ipv4 {}\n".format(sc["host"]))
        if "timeout" in sc:
            config.append("timeout {}\n".format(sc["timeout"]))
        if "key_type" in sc and "key" in sc:
            config.append(
                "key {} {}\n".format(sc["key_type"], sc["key"])
            )

        config.append("exit\n")

        try:
            device.configure("".join(config))
        except SubCommandFailure:
            raise SubCommandFailure(
                "Could not configure tacacs server on device {device}".format(
                    device=device.name
                )
            )


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
