"""Common configure functions for NTP"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def remove_ntp_system_peer(device, system_peer, vrf=None):
    """ Remove ntp system peer config

        Args:
            device (`obj`): Device object
            system_peer ('str'): System peer IP address
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    remove_config = ''
    log.info("Getting ntp server infomation")
    out = device.execute('show running-config | include ntp server')
    for line in out.splitlines():
        line = line.strip()
        if vrf and vrf != 'default':
            if system_peer in line and vrf in line:
                remove_config = line
                break
        else:
            if system_peer in line:
                remove_config = line
                break

    log.info("Removing ntp server: {}".format(remove_config))
    try:
        device.configure("no {}".format(remove_config))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in removing ntp system "
            "peer {system_peer} on device {device}, "
            "Error: {e}".format(
                system_peer=system_peer, device=device.name, e=str(e)
            )
        )


def remove_ntp_server(device, servers):
    """ Remove all configured server using routes

        Args:
            device ('obj'): Device object
            servers ('list'): List of servers to remove(server)
                ex.)
                    servers = ['192.168.36.11', '192.168.36.12']
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = []
    for route in servers:
        config.append("no ntp server {}".format(route))

    try:
        device.configure("\n".join(config))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in removing ntp servers "
            "on device {device}, "
            "Error: {e}".format(device=device.name, e=str(e))
        ) from e


def configure_ntp_master(device, stratum=None):
    """ Configure ntp master

        Args:
            device ('obj'): Device object
            stratum ('str'): Specify a different stratum level 
                from which NTP clients get their time synchronized. 
                The range is from 1 to 15.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if not stratum or stratum >= 1 and stratum <= 15:
        try:
            device.configure(
                "ntp master {}".format("" if not stratum else stratum)
            )
        except SubCommandFailure as e:
            raise SubCommandFailure(
                "Failed in configuring ntp master "
                "on device {device}, "
                "Error: {e}".format(device=device.name, e=str(e))
            ) from e
    else:
        raise SubCommandFailure(
            "Invalid input. Stratum value must "
            "be empty or integer value between 1 and 15"
        )

def remove_ntp_master(device):
    """ Unconfigure ntp master

        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Unconfigure NTP master")
    configs = []
    configs.append("no ntp master")
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure NTP master"
            "Error: {error}".format(error=e)
            )

def configure_ntp_iburst(device, route):
    """ Configure ntp iburst using ip address

        Args:
            device ('obj'): Device object
            route ('str'): IP address to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("ntp server {} iburst".format(route))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring ntp iburst "
            "on device {device}, "
            "Error: {e}".format(device=device.name, e=str(e))
        ) from e


def configure_ntp_server(device, ntp_config, vrf=None):
    """ Configures ntp server

        Args:
            device ('obj'): device to configure on
            ntp_config ('list'): List containing server ip address
            vrf ('str'): Optional VRF to be used during configuration
                ex.)
                   ntp_config = [ 
                        '192.168.1.1',
                        '192.168.1.2'
                    ]
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    if not isinstance(ntp_config, list):
        raise SubCommandFailure("ntp_config must be a list")

    config = []
    for ip in ntp_config:
        if vrf:
            config.append("ntp server vrf {} {}".format(vrf, ip))
        else:
            config.append("ntp server {}".format(ip))

    try:
        device.configure("\n".join(config))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring ntp server "
            "on device {device}, "
            "Error: {e}".format(device=device.name, e=str(e))
        ) from e


def unconfigure_ntp_server(device, ntp_config, vrf=None):
    """ Unconfigures ntp server

        Args:
            device ('obj'): device to configure on
            ntp_config ('list'): List containing server ip address
            vrf ('str'): Optional VRF to be used during configuration
                ex.)
                   ntp_config = [ 
                        '192.168.1.1',
                        '192.168.1.2'
                    ]
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    if not isinstance(ntp_config, list):
        raise SubCommandFailure("ntp_config must be a list")

    config = []
    for ip in ntp_config:
        if vrf == None:
            config.append("no ntp server {}".format(ip))
        else:
            config.append("no ntp server vrf {} {}".format(vrf, ip))

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in unconfiguring ntp server "
            "on device {device}, "
            "Error: {e}".format(device=device.name, e=str(e))
        ) from e


def configure_ntp_auth_key(device, key_id, key_value, key_type, key_enc_type=0):
    """ Configures ntp authentication key

        Args:
            device ('obj'): device to configure on
            key_id ('str'): Key ID
            key_value ('str'): Key value
            key_type ('str'): Key type
            key_enc_type ('str', optional): Key encryption type (default: 0)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            "ntp authentication-key {} {} {} {}".format(
                key_id, key_type, key_value, key_enc_type
            )
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring ntp authentication key "
            "on device {device}, "
            "Error: {e}".format(device=device.name, e=str(e))
        ) from e


def configure_ntp_authenticate(device):
    """ Configures ntp authenticate

        Args:
            device ('obj'): device to configure on
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("ntp authenticate")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring ntp authenticate "
            "on device {device}, "
            "Error: {e}".format(device=device.name, e=str(e))
        ) from e


def configure_ntp_trusted_key(device, key_id):
    """ Configures ntp trusted key

        Args:
            device ('obj'): device to configure on
            key_id ('str'): Key ID
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("ntp trusted-key {}".format(key_id))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring ntp trusted key "
            "on device {device}, "
            "Error: {e}".format(device=device.name, e=str(e))
        ) from e


def configure_ntp_server_with_auth(device, server_ip, key_id, vrf=None):
    """
    Configure ntp server with authentication
        Args:
            device ('obj'): device to configure on
            server_ip ('str'): Server IP address
            key_id ('str'): Key ID
            vrf ('str', optional): Optional VRF to be used during configuration (default: None)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        if vrf:
            device.configure("ntp server vrf {} {} key {}".format(vrf, server_ip, key_id))
        else:
            device.configure("ntp server {} key {}".format(server_ip, key_id))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring ntp server with authentication "
            "on device {device}, "
            "Error: {e}".format(device=device.name, e=str(e))
        ) from e


def configure_no_ntp(device):
    """
    Configure no ntp
        Args:
            device ('obj'): device to configure on
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("no ntp")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring no ntp "
            "on device {device}, "
            "Error: {e}".format(device=device.name, e=str(e))
        ) from e
