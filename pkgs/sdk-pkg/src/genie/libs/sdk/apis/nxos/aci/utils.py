"""Base functions for NXOS ACI"""

# Python
import re
import logging

from genie.libs.filetransferutils import FileServer
from genie.libs.sdk.apis.utils import copy_to_device as generic_copy_to_device

from pyats.utils.fileutils import FileUtils

log = logging.getLogger(__name__)


def copy_to_device(device,
                   remote_path,
                   local_path,
                   server,
                   protocol,
                   vrf=None,
                   timeout=300,
                   compact=False,
                   use_kstack=False,
                   username=None,
                   password=None,
                   **kwargs):
    """
    Copy file from linux server to device
        Args:
            device ('Device'): Device object
            remote_path ('str'): remote file path on the server
            local_path ('str'): local file path to copy to on the device
            server ('str'): hostname or address of the server
            protocol('str'): file transfer protocol to be used
            vrf ('str'): vrf to use (optional)
            timeout('int'): timeout value in seconds, default 300
            compact('bool'): compress image option for n9k, defaults False
            username('str'): Username to be used during copy operation
            password('str'): Password to be used during copy operation
            use_kstack('bool'): Use faster version of copy, defaults False
                                Not supported with a file transfer protocol
                                prompting for a username and password
        Returns:
            None
    """
    # aci uses the linux implementation and fileutils doesnt support
    # os/platform abstraction
    setattr(device, 'os', 'linux')
    fu = FileUtils.from_device(device)
    setattr(device, 'os', 'nxos')

    generic_copy_to_device(device=device,
                           remote_path=remote_path,
                           local_path=local_path,
                           server=server,
                           protocol=protocol,
                           vrf=vrf,
                           timeout=timeout,
                           compact=compact,
                           use_kstack=use_kstack,
                           username=username,
                           password=password,
                           fu=fu,
                           **kwargs)


def copy_to_script_host(device,
                 filename,
                 local_path=None,
                 timeout=300):
    """
    Copy a file from the device to the local system where the script is running.
    Uses HTTP. Only supported via telnet or SSH sessions.

    Args:
        device (Device): device object
        filename (str): filename to copy
        local_path (str): local path to copy the file to, defaults to '.'
        timeout('int'): timeout value in seconds, default 300

    Returns:
        (boolean): True if successful, False if not

    The local IP adddress will be determined from the spawned telnet or ssh session.
    A temporary http server will be created and the show tech file will be sent
    to the host where the script is running.

    If the device is connected via proxy (unix jump host) and the proxy has
    'socat' installed, the upload will be done via the proxy automatically.
    """

    local_path = local_path or '.'

    output = device.execute('ifconfig eth0')

    #   inet addr:172.1.1.2  Bcast:172.1.1.255  Mask:255.255.255.0
    m = re.search(r'inet addr:(\S+)', output)
    if m:
        mgmt_ip = m.group(1)

    netstat_output = device.execute('netstat -an | grep {}:22'.format(mgmt_ip))
    # tcp        0      0 172.1.1.2:22        10.1.1.1:59905     ESTABLISHED -
    mgmt_src_ip_addresses = re.findall(r'\d+ +\S+:\d+ +(\S+):\d+ +ESTAB', netstat_output)
    if not mgmt_src_ip_addresses:
        log.error('Unable to find management session, unable to upload file')
        return False

    # try figure out local IP address
    local_ip = device.api.get_local_ip()

    if local_ip in mgmt_src_ip_addresses:
        mgmt_src_ip = local_ip
    else:
        mgmt_src_ip = None

    with FileServer(protocol='http',
                    address=local_ip,
                    path=local_path) as fs:

        local_port = fs.get('port')

        proxy_port = None
        # Check if we are connected via proxy device
        proxy = device.connections[device.via].get('proxy')
        if proxy and isinstance(proxy, str):
            log.info('Setting up port relay via proxy')
            proxy_dev = device.testbed.devices[proxy]
            proxy_dev.connect()
            proxy_port = proxy_dev.api.socat_relay(remote_ip=local_ip, remote_port=local_port)

            ifconfig_output = proxy_dev.execute('ifconfig')
            proxy_ip_addresses = re.findall(r'inet (?:addr:)?(\S+)', ifconfig_output)
            mgmt_src_ip = None
            for proxy_ip in proxy_ip_addresses:
                if proxy_ip in mgmt_src_ip_addresses:
                    mgmt_src_ip = proxy_ip
                    break

        try:
            if mgmt_src_ip and proxy_port:
                device.execute('curl --upload-file {} http://{}:{}'.format(
                               filename, mgmt_src_ip, proxy_port),
                               timeout=timeout)
            elif mgmt_src_ip:
                device.execute('curl --upload-file {} http://{}:{}'.format(
                               filename, local_ip, local_port),
                               timeout=timeout)
            else:
                log.error('Unable to determine management IP address to use to upload file')
                return False

        except Exception:
            log.error('Failed to transfer file', exc_info=True)
            return False

    return True
