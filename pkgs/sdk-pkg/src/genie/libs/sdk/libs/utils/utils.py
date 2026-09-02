
import logging
from collections.abc import Mapping
from contextlib import contextmanager
import re
import time

from genie.utils.timeout import Timeout

from unicon.core.errors import UniconBackendDecodeError
from unicon.core.errors import ConnectionError


log = logging.getLogger(__name__)


def get_tftp_server_address(device):
    """Select a TFTP server address from the device testbed.

    TFTP services with an ``order`` value take precedence, with the lowest
    numeric order selected first. The function then falls back to an unordered
    TFTP service, a server using the legacy top-level ``protocol: tftp`` form,
    and finally the address of the legacy server named ``tftp``.

    Args:
        device (obj): Device whose testbed server data should be searched.

    Returns:
        str: Selected TFTP server address, or an empty string when unavailable.
    """
    servers = getattr(getattr(device, 'testbed', None), 'servers', {}) or {}
    if not isinstance(servers, Mapping):
        return ''

    ordered_servers = []
    unordered_servers = []
    legacy_servers = []

    for server in servers.values():
        address = server.get('address')
        if not address:
            continue

        tftp_services = [
            service for service in (server.get('services', {}) or {}).values()
            if service.get('protocol') == 'tftp'
        ]
        for service in tftp_services:
            order = service.get('order')
            if order is None:
                unordered_servers.append(address)
            else:
                ordered_servers.append((order, address))

        if not tftp_services and server.get('protocol') == 'tftp':
            legacy_servers.append(address)

    if ordered_servers:
        def order_key(server):
            order = server[0]
            try:
                return (0, float(order))
            except (TypeError, ValueError):
                return (1, str(order))

        ordered_servers.sort(key=order_key)
        return ordered_servers[0][1]

    if unordered_servers:
        return unordered_servers[0]

    if legacy_servers:
        return legacy_servers[0]

    return servers.get('tftp', {}).get('address', '')


def get_recovery_tftp_server(device):
    """Get the clean recovery TFTP server, falling back to testbed services.

    Args:
        device (obj): Device containing clean and testbed server data.

    Returns:
        str: Recovery TFTP server name or address, or an empty string when no
            TFTP server is available.
    """
    clean = getattr(device, 'clean', None)
    if not isinstance(clean, Mapping):
        clean = {}

    recovery = clean.get('device_recovery', {}) or {}
    if not isinstance(recovery, Mapping):
        recovery = {}

    tftp_boot = recovery.get('tftp_boot', {}) or {}
    if not isinstance(tftp_boot, Mapping):
        tftp_boot = {}

    tftp_server = tftp_boot.get('tftp_server', '')
    if tftp_server:
        log.info(
            'Using recovery TFTP server %s from clean data for device %s',
            tftp_server, device.name)
        return tftp_server

    log.warning(
        'No recovery TFTP server found in clean data for device %s; '
        'falling back to testbed services', device.name)
    return get_tftp_server_address(device)


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


def connect_to_device(device, timeout=30):
    """Connect to device
    Args:
        device('obj'): device object
        timeout('int'): connection timeout in seconds
    """
    try:
        log.info(f'Connecting to device {device.name}')
        device.connect(connection_timeout=timeout, settings=dict(GRACEFUL_DISCONNECT_WAIT_SEC=0, POST_DISCONNECT_WAIT_SEC=0))
        return True
    except Exception:
        return False

def verify_device_connection(device, timeout=60, interval=10, send_line_count=3):
    """Connect to device and if it fails, check the buffer for ASCII characters
    Args:
        device('obj'): device object
        timeout('int'): connection timeout in seconds
        interval('int'): interval in seconds to check the buffer
        send_line_count('int'): number of lines to send to device spawn
    """
    try:
        log.info(f'Connecting to device {device.name}')
        device.connect(connection_timeout=10, settings=dict(GRACEFUL_DISCONNECT_WAIT_SEC=0, POST_DISCONNECT_WAIT_SEC=0))
        return True
    except UniconBackendDecodeError as e:
        log.error(f'Could not connect to device {device.name} due to console speed mismatch.')
        device.destroy()
        raise e
    except Exception as e:
        # make sure to disconnect before try to setup connection 
        log.error(f'Could not connect to device {device.name} due to {e}.')
        log.info('Checking the buffer for ASCII characters')
        # if connection failed we need to destroy connection otherwise if we try to device.disconnect()
        # and setup_connection() we will get device is already connected.
        device.destroy()
        device.instantiate()
        device.setup_connection()
        timeout = Timeout(max_time=timeout, interval=interval, disable_log=True)
        while timeout.iterate():
            for _ in range(send_line_count):
                device.spawn.sendline()
            device.spawn.read_update_buffer()
            output = device.spawn.buffer
            # Strip telnet connection banner
            output = re.sub(r"Trying [\d\.]+.*?\s*", '', output)
            output = re.sub(r"Connected to [\d\.]+\.\r\r\nEscape character is '\^]'\.\r\r\n", '', output)
        
            # Reject if output looks like escape sequences (e.g., \x86\xfe)
            # Accept if it has readable text (letters, numbers, punctuation excluding backslash patterns)
            if output:
                # Filter ASCII chars and check for consecutive alphanumeric sequences (words)
                ascii_chars = ''.join(char for char in output if ord(char) < 128)
                # Look for at least 5 consecutive letters (a real word, not hex like "xfe")
                if ascii_chars and re.search(r'[a-zA-Z]{5,}', ascii_chars):
                    log.info(f'ASCII characters {ascii_chars} found in the buffer: {output}')
                    device.destroy()
                    return True
                else:
                    log.warning(f'Buffer contains non-ASCII or escape sequences: {output}')
                    timeout.sleep()
        device.destroy()
        raise ConnectionError(f'Could not connect to device {device.name} .')



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


_SYSLOG_MONTHS = {'jan', 'feb', 'mar', 'apr', 'may', 'jun',
                  'jul', 'aug', 'sep', 'oct', 'nov', 'dec'}


def _is_syslog_line(line):
    """Return True if line looks like a syslog message that should be stripped."""
    stripped = line.strip().lstrip('.*')
    parts = stripped.split()
    if len(parts) >= 1 and parts[0].lower() in _SYSLOG_MONTHS:
        return True
    if '%' in line and '-' in line:
        if re.search(r'%[A-Z_]+-\d+-[A-Z_]+:', line):
            return True
    return False
