# Python
import logging
from unicon.eal.dialogs import Statement, Dialog

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_logging_console(device):
    """ logging console
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure('logging console')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure logging console on {device}. Error:\n{error}".format(device=device, error=e))


def unconfigure_logging_console(device):
    """ no logging console
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure('no logging console')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure logging console on {device}. Error:\n{error}".format(device=device, error=e))


def configure_logging_host(device, server_ip):
    """ Configure logging host 
        Args:
            device ('obj'): Device object
            server_ip ('str'):  IP address of the syslog server

        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring logging host transport tcp port
    """
    cmd = f'logging host {server_ip}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure logging. Error:\n{e}")

def unconfigure_logging_host(device, server_ip):
    """ Configure logging host
        Args:
            device ('obj'): Device object
            server_ip ('str'):  IP address of the syslog server

        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring logging host transport tcp port
    """
    cmd = f'no logging host {server_ip}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure logging. Error:\n{e}")
        

def configure_logging_source_interface(device, interface):
    """ Configure logging host
        Args:
            device ('obj'): Device object
            interface ('str'):  Logging source interface

        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring logging host transport tcp port
    """
    cmd = f'logging source-interface {interface}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure logging source interface. Error:\n{e}")

def unconfigure_logging_source_interface(device, interface):
    """ Configure logging host
        Args:
            device ('obj'): Device object
            interface ('str'):  Logging source interface

        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring logging host transport tcp port
    """
    cmd = f'no logging source-interface {interface}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure logging source interface. Error:\n{e}")

        
           
def configure_logging_monitor(device):
    """ logging monitor
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure('logging monitor')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure logging monitor on {device}. Error:\n{error}".format(device=device, error=e))


def unconfigure_logging_monitor(device):
    """ no logging monitor
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure('no logging monitor')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure logging monitor on {device}. Error:\n{error}".format(device=device, error=e))


def configure_terminal_length(device, line_num):
    """ terminal length 0
        Args:
            device (`obj`): Device object
            line_num ('int'): Number of lines on screen (0 for no pausing)
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Configure terminal length on {device}".format(device=device))

    try:
        device.execute('terminal length {line_num}'.format(line_num=line_num))
    except SubCommandFailure as e:
        raise SubCommandFailure(
             "Could not configure terminal length on {device}. Error:\n{error}".format(device=device, error=e))


def configure_terminal_width(device, char_num):
    """ terminal width 0
        Args:
            device (`obj`): Device object
            char_num ('int'): Number of characters on a screen line
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Configure terminal width on {device}".format(device=device))

    try:
        device.execute('terminal width {char_num}'.format(char_num=char_num))
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not configure terminal width on {device}. Error:\n{error}".format(device=device, error=e))

def configure_terminal_exec_prompt_timestamp(device):
    """ terminal exec prompt timestamp
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configure terminal exec prompt timestamp on {device}".format(device=device))

    try:
        device.execute('terminal exec prompt timestamp')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not terminal exec prompt timestamp on {device}. Error:\n{error}".format(device=device, error=e))


def configure_logging_buffer_size(device, buffer_size):
    """ logging buffered <4096-2147483647>
        Args:
            device (`obj`): Device object
            buffer_size ('int'): Size of the buffer
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Configure logging buffer on {device}".format(device=device))

    try:
        device.configure('logging buffer {buffer_size}'.format(buffer_size=buffer_size))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not logging buffer on {device}. Error:\n{error}".format(device=device, error=e))

def configure_logging_buffered_errors(device):
    """ Confgiure logging buffered errors
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Configure logging buffered errors on {device}".format(device=device))
    
    try:
        device.configure('logging buffered errors')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure logging buffered errors on {device}. Error:\n{error}"
                .format(device=device, error=e))

def unconfigure_logging_buffered_errors(device):
    """ Unconfgiure logging buffered errors
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Unconfigure logging buffered errors on {device}".format(device=device))
    
    try:
        device.configure('no logging buffered errors')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure logging buffered errors on {device}. Error:\n{error}"
                .format(device=device, error=e))

def configure_logging_console_errors(device):
    """ Confgiure logging console errors
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Configure logging console errors on {device}".format(device=device))
    
    try:
        device.configure('logging console errors')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure logging console errors on {device}. Error:\n{error}"
                .format(device=device, error=e))

def unconfigure_logging_console_errors(device):
    """ Unconfgiure logging console errors
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Unconfigure logging console errors on {device}".format(device=device))
    
    try:
        device.configure('no logging console errors')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure logging console errors on {device}. Error:\n{error}"
                .format(device=device, error=e))


def configure_lineconsole_exectimeout(device,console_num,timeout):
    """ Configure line console exec timeout
        Args:
            device (`obj`): Device object
            console_num ('int'): Line console number
            timeout ('mins'): timeout in mins
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Configure line console exec timeout on {device}".format(device=device))

    try:
        device.configure(
            [
                "line console {console_num}".format(console_num=console_num),
                "exec-timeout {timeout}".format(timeout=timeout),
            ]
        )

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure line console exec timeout on {device}. Error:\n{error}"
                .format(device=device, error=e))


def configure_logging_monitor_debugging(device):
    """ logging monitor debugging
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure('logging monitor debugging')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure logging monitor debugging on {device}. Error:\n{error}".format(device=device, error=e))

def configure_logging_buffered_debugging(device):
    """ Confgiure logging buffered debugging
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Configure logging buffered debugging on {device}".format(device=device))
    
    try:
        device.configure('logging buffered debugging')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure logging buffered debugging on {device}. Error:\n{error}"
                .format(device=device, error=e))

def unconfigure_logging_buffered(device, log_type=None):
    """ Unconfigure logging buffered
        Args:
            device ('obj'): Device object
            log_type ('str', optional) : unconfigure log type. Ex: alerts, critical, etc. Default is None. 
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug(f"Unconfigure logging buffered on {device}")
    config = f"no logging buffered {log_type if log_type else ''}"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure logging console errors on {device}. Error:\n{e}")


def unconfigure_logging_monitor_debugging(device):
    """ Unconfigure logging monitor debugging
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = 'no logging monitor debugging'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure logging monitor debugging on {device}. Error:\n{e}")


def configure_logging_facility(device, facility):
    """ Configure logging facility
        Args:
            device ('obj'): Device object
            facility ('str'): Name of facility (eg. local7)
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring logging facility
    """
    cmd = f'logging facility {facility}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure logging facility on device {device}. Error:\n{e}"
            )


def configure_login_log(device, login_attempt, periodicity_num=''):
    """ Configure login log on switch
        Args:
            device ('obj'): Device object
            login_attempt ('str'):  Set options for login attempt (eg. on-failure/on-success)
            periodicity_num ('int'): Periodicity number (1-65535)
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring login log
    """
    cmd = f'login {login_attempt} log'
    if periodicity_num:
        cmd += f' every {periodicity_num}'        
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure login log on device {device}. Error:\n{e}")


def configure_logging_host_transport_tcp_port(device, server_ip, port_num):
    """ Configure logging host transport tcp port
        Args:
            device ('obj'): Device object
            server_ip ('str'):  IP address of the syslog server
            port_num ('int'): Port number (1-65535)
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring logging host transport tcp port
    """	
    cmd = f'logging host {server_ip} transport tcp port {port_num}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure logging host transport tcp port on device {device}. Error:\n{e}")


def configure_logging(device, mode, severity=None):
    """ Configure logging 
        Args:
            device ('obj'): Device object
            mode ('str'): logging mode. Ex: monitor, history, hostname, on
            severity ('str', optional): logging severity. Ex: alrets, debugging, critical, 7. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = f'logging {mode}{f" {severity}" if severity else ""}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure logging {mode} on {device}. Error:\n{e}")


def unconfigure_logging(device, mode, severity=None):
    """ Unconfigure logging 
        Args:
            device ('obj'): Device object
            mode ('str'): logging mode. Ex: monitor, history, hostname, on
            severity ('str', optional): logging severity. Ex: alrets, debugging, critical, 7. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = f'no logging {mode}{f" {severity}" if severity else ""}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not unconfigure logging {mode} on {device}. Error:\n{e}")
