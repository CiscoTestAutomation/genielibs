
import logging
from contextlib import contextmanager
log = logging.getLogger(__name__)

@contextmanager
def ensure_connection(device):
    connected = False
    try:
        if len(device.connections):
            # ensure connections are defined, otherwise cannot connect
            # instantiate device connection object
            try:
                device.connect()
                connected = True
                yield device
            except Exception:
                log.error(f'Unable to connect to {device}')
                yield
    finally:
        if connected:
            try:
                device.disconnect()
            except Exception as e:
                log.debug(e)


def connect_to_device(device):
    """Connect to device
    Args:
        device('obj'): device object
    """
    try:
        log.info(f'Connecting to device {device.name}')
        device.connect(connection_timeout=30, settings=dict(GRACEFUL_DISCONNECT_WAIT_SEC=0, POST_DISCONNECT_WAIT_SEC=0))
        return True
    except Exception:
        return False


def get_terminal_server(device):
    """Get terminal server info from testbed
    Args:
        device('obj'): device object
    return:
        terminal_server_info('dict'): dictionary of terminal servers info
    """
    if hasattr(device, 'peripherals') and 'terminal_server' in device.peripherals:
        return device.peripherals['terminal_server']
    else:
        return {}


def get_lines(terminal_server_lines):
    """Get lines from terminal server info
    Args:
       terminal_server_info('dict'): dictionary of terminal servers info
    return:
        lines('list'): list of line numbers
    """
    lines = []
    for line in terminal_server_lines:
        if isinstance(line, dict) and line.get('line'):
            lines.append(line['line'])
        else:
            lines.append(line)
    return lines


def get_speed(terminal_servers):
    """Get speed from terminal server info
    Args:
       terminal_server_info('dict'): dictionary of terminal servers info
    return:
        speed(int): speed defined in the testbed for the terminal serve line
    """
    for terminal_server, terminal_server_lines in terminal_servers.items():
        for line in terminal_server_lines:
            if isinstance(line, dict) and line.get('speed'):
                return line['speed']
 
 
def device_connection_provider_connect(device):
    """ Connect to device
    Args:
        device('obj'): device object
    """
    device.sendline()
    device.connection_provider.connect()
