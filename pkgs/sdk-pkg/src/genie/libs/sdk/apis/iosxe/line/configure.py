"""Common configure functions for line """
import logging
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement
log = logging.getLogger(__name__)

def configure_line(device, async_line, async_speed, async_parity, async_stopbits, async_databits):
    """ configure speed, parity, stopbits, databits on serial line.

        Args:
            device (`obj`): Device object of router on which serial async line is to be configured.
            async_line (`str`): Async line on router, for example 'line 0/3/0'.
            async_speed ('int'): Transmit and receive speeds to be configured on async line like 9600, 115200.
            async_parity ('str'): Parity of even, odd, none, space and mark of async line.
            async_stopbits ('int'): Stopbits supported on async line like one stop and two stop.
            async_databits ('int'): Number of data bits for transmit and receive on async line.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configure async line")
    cmd =[f"line {async_line}", f"speed {async_speed}", f"parity {async_parity}",f"stopbits {async_stopbits}",f"databits {async_databits}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure speed, parity, stopbits, databits on serial line, Error:\n{e}"
        )

def unconfigure_line(device, async_line, async_speed, async_parity, async_stopbits, async_databits):
    """ unconfigure speed, parity, stopbits, databits on serial line.
        Args:
            device (`obj`): Device object of router on which serial async line is to be unconfigured.
            async_line (`str`): Async line on router, for example line 0/3/0.
            async_speed ('int'): Transmit and receive speeds to be unconfigured on async line like 9600.
            async_parity ('str'): Parity of even, odd, none, space and mark of async line.
            async_stopbits ('int'): Stopbits supported on async line like one stop and two stop.
            async_databits ('int'): Number of data bits for transmit and receive on async line.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Unconfigure line")
    cmd =[f"line {async_line}", f"no speed {async_speed}", f"no parity {async_parity}",f"no stopbits {async_stopbits}",f"no databits {async_databits}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure speed, parity, stopbits, databits on serial line, Error:\n{e}"
        )

def configure_line_raw_socket_tcp_server(device, async_line, rawtcp_server_ip, rawtcp_server_port):
    """ configure raw-socket tcp server on serial line
        Args:
            device (`obj`): Router on which raw socket tcp server is to be configured.
            async_line (`str`):  Async line on router, for example line 0/3/0.
            rawtcp_server_port ('int'): Port number of raw tcp server on async line.
            rawtcp_server_ip ('str'): IP address of raw tcp server on async line.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configure raw-tcp server on serial line")
    cmd =[f"line {async_line}", f"raw-socket tcp server {rawtcp_server_port} {rawtcp_server_ip}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure raw socket tcp server on serial line,  Error:\n{e}"
        )

def unconfigure_line_raw_socket_tcp_server(device, async_line, rawtcp_server_ip, rawtcp_server_port):
    """ unconfigure raw-socket tcp server on serial async line
        Args:
            device (`obj`): Router on which raw socket tcp server is to be unconfigured.
            async_line (`str`):  Async line on router, for example line 0/3/0.
            rawtcp_server_port ('int'): Port number of raw tcp server on async line.
            rawtcp_server_ip ('str'): IP address of raw tcp server on asyc line.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Unconfigure raw-tcp server on serial line")
    cmd =[f"line {async_line}", f"no raw-socket tcp server {rawtcp_server_port} {rawtcp_server_ip}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure raw socket tcp server on serial line, Error:\n{e}"
        )
    
def configure_line_raw_socket_tcp_client(device, async_line, rawtcp_server_ip, rawtcp_server_port, rawtcp_client_port, rawtcp_client_ip):
    """ configure raw-socket tcp client on serial async line
        Args:
            device (`obj`): Router on which raw socket tcp server is to be configured.
            async_line (`str`):  Async line on router example line 0/3/0.
            rawtcp_server_port ('int'): Port number of raw tcp server to which client must connect.
            rawtcp_server_ip ('str'): IP address of raw tcp server to which client must connect.
            rawtcp_client_port ('int'): Port number of raw tcp client on async line.
            rawtcp_client_ip ('str'): IP address of raw tcp client on asyc line.
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Configure raw-tcp client")
    cmd =[f"line {async_line}", f"raw-socket tcp client {rawtcp_server_ip} {rawtcp_server_port} {rawtcp_client_port} {rawtcp_client_ip}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure tcp client on serial line, Error:\n{e}"
        )
    
def unconfigure_line_raw_socket_tcp_client(device, async_line, rawtcp_server_ip, rawtcp_server_port, rawtcp_client_port, rawtcp_client_ip):
    """ unconfigure raw-socket tcp client on serial async line
        Args:
            device (`obj`): Router on which raw socket tcp server is to be configured.
            async_line (`str`):  Async line on router example line 0/3/0.
            rawtcp_server_port ('int'): Port number of raw tcp server to which client must connect.
            rawtcp_server_ip ('str'): IP address of raw tcp server to which client must connect.
            rawtcp_client_port ('int'): Port number of raw tcp client on async line.
            rawtcp_client_ip ('str'): IP address of raw tcp client on asyc line.
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Unconfigure raw-tcp client")
    cmd =[f"line {async_line}", f"no raw-socket tcp client {rawtcp_server_ip} {rawtcp_server_port} {rawtcp_client_port} {rawtcp_client_ip}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure tcp client on serial line, Error:\n{e}"
        )
