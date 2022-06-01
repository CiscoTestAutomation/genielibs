"""Base functions for NXOS ACI"""

# Python
import os
import re
import pathlib
import logging
from datetime import datetime

from unicon.eal.dialogs import Dialog

from pyats.utils.fileutils import FileUtils
from pyats.utils.secret_strings import to_plaintext

from genie.libs.sdk.apis.utils import slugify
from genie.libs.filetransferutils import FileServer


log = logging.getLogger(__name__)


def copy_to_device(device,
                   remote_path,
                   local_path=None,
                   server=None,
                   protocol='http',
                   vrf=None,
                   timeout=300,
                   compact=False,
                   use_kstack=False,
                   fu=None,
                   http_auth=True,
                   **kwargs):
    """
    Copy file from linux server to the device.

    Args:
        device (Device): Device object
        remote_path (str): remote file path on the server
        local_path (str): local file to copy to on the device (default: None)
        server (str): hostname or address of the server (default: None)
        protocol(str): file transfer protocol to be used (default: http)
        vrf (str): vrf to use (optional)
        timeout(int): timeout value in seconds, default 300
        compact(bool): compress image option for n9k, defaults False
        fu(obj): FileUtils object to use instead of creating one. Defaults to None.
        use_kstack(bool): Use faster version of copy, defaults False
                            Not supported with a file transfer protocol
                            prompting for a username and password
        http_auth (bool): Use http authentication (default: True)

    Returns:
        None

    If the server is not specified, a HTTP server will be spawned
    on the local system and serve the directory of the file
    specified via remote_path and the copy operation will use http.

    If the device is connected via CLI proxy (unix jump host) and the proxy has
    'socat' installed, the transfer will be done via the proxy automatically.
    """

    if server:

        if not fu:
            fu = FileUtils.from_device(device)

        if vrf is not None:
            server = fu.get_hostname(server, device, vrf=vrf)
        else:
            server = fu.get_hostname(server, device)

        # build the source address
        source = '{p}://{s}/{f}'.format(p=protocol, s=server, f=remote_path)
        try:
            if vrf is not None:
                return fu.copyfile(source=source,
                                   destination=local_path,
                                   device=device,
                                   vrf=vrf,
                                   timeout_seconds=timeout,
                                   compact=compact,
                                   use_kstack=use_kstack,
                                   protocol=protocol,
                                   **kwargs)
            else:
                return fu.copyfile(source=source,
                                   destination=local_path,
                                   device=device,
                                   timeout_seconds=timeout,
                                   compact=compact,
                                   use_kstack=use_kstack,
                                   protocol=protocol,
                                   **kwargs)
        except Exception:
            if compact or use_kstack:
                log.info("Failed to copy with compact/use-kstack option, "
                         "retrying again without compact/use-kstack")
                return fu.copyfile(source=source,
                                   destination=local_path,
                                   device=device,
                                   vrf=vrf,
                                   timeout_seconds=timeout,
                                   protocol=protocol,
                                   **kwargs)
            else:
                raise

    remote_path_parent = str(pathlib.PurePath(remote_path).parent)
    remote_filename = pathlib.PurePath(remote_path).name

    mgmt_src_ip_addresses = device.api.get_mgmt_src_ip_addresses()

    # try figure out local IP address
    local_ip = device.api.get_local_ip()

    if local_ip in mgmt_src_ip_addresses:
        mgmt_src_ip = local_ip
    else:
        mgmt_src_ip = None

    with FileServer(protocol='http',
                    address=local_ip,
                    path=remote_path_parent,
                    http_auth=http_auth) as fs:

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

        copy_dialog = Dialog([
            [r'Address or name of remote host', 'sendline()', None, True, False],
            [r'Destination filename', 'sendline()', None, True, False],
        ])

        cmd = 'curl'

        if http_auth:
            username = fs.get('credentials', {}).get('http', {}).get('username', '')
            password = to_plaintext(fs.get('credentials', {}).get('http', {}).get('password', ''))
            cmd += ' -u {}:{}'.format(username, password)

        if mgmt_src_ip and proxy_port:
            cmd += ' http://{}:{}/{}'.format(mgmt_src_ip, proxy_port, remote_filename)
        elif mgmt_src_ip:
            cmd += ' http://{}:{}/{}'.format(mgmt_src_ip, local_port, remote_filename)
        else:
            log.error('Unable to determine management IP address to use to download file')
            return False

        if local_path:
            cmd += ' -o {}'.format(local_path)
        else:
            cmd += ' -O'

        if vrf:
            cmd += ' vrf {}'.format(vrf)

        try:
            device.execute(cmd, reply=copy_dialog, timeout=timeout, append_error_pattern=[r'%\s*Error', r'%\s*Invalid'])
        except Exception:
            log.error('Failed to transfer file', exc_info=True)
            return False

    return True


def copy_from_device(device,
                     local_path,
                     remote_path=None,
                     server=None,
                     protocol='http',
                     vrf=None,
                     timeout=300,
                     timestamp=False,
                     http_auth=True,
                     **kwargs):
    """
    Copy a file from the device to the server or local system (where the script is running).
    Local system copy uses HTTP and is only supported via telnet or SSH sessions.

    Args:
        device (Device): device object
        local_path (str): local path from the device (path including filename)
        remote_path (str): Path on the server (default: .)
        server (str): Server to copy file to (optional)
        protocol (str): Protocol to use to copy (default: http)
        vrf (str): VRF to use for copying (default: None)
        timeout('int'): timeout value in seconds, default 300
        timestamp (bool): include timestamp in filename (default: False)
        http_auth (bool): Use http authentication (default: True)

    Returns:
        (boolean): True if successful, False if not

    If the server is not specified, below logic applies.

    If no filename is specified, the filename will be based on the device hostname
    and slugified name of the file determined from the local_path.

    The local IP adddress will be determined from the spawned telnet or ssh session.
    A temporary http server will be created and the show tech file will be sent
    to the host where the script is running.

    If the device is connected via proxy (unix jump host) and the proxy has
    'socat' installed, the upload will be done via the proxy automatically.

    Note: if the file already exists, it will be overwritten.
    """

    if server:

        fu = FileUtils.from_device(device)

        # build the source address
        destination = '{p}://{s}/{f}'.format(p=protocol, s=server, f=remote_path)
        if vrf is not None:
            return fu.copyfile(source=local_path,
                               destination=destination,
                               device=device,
                               vrf=vrf,
                               timeout_seconds=timeout,
                               **kwargs)
        else:
            return fu.copyfile(source=local_path,
                               destination=destination,
                               device=device,
                               timeout_seconds=timeout,
                               **kwargs)

    remote_path = remote_path or '.'

    if not pathlib.Path(remote_path).is_dir():
        filename = pathlib.PurePath(remote_path).name
        remote_path = pathlib.Path(remote_path).parent
    else:
        filename = None

    mgmt_src_ip_addresses = device.api.get_mgmt_src_ip_addresses()

    # try figure out local IP address
    local_ip = device.api.get_local_ip()

    if local_ip in mgmt_src_ip_addresses:
        mgmt_src_ip = local_ip
    else:
        mgmt_src_ip = None

    if not filename:
        filename = pathlib.Path(os.path.basename(local_path.split(':')[-1]))
        filename = '{}_{}'.format(device.hostname, slugify(filename.stem) + filename.suffix)

    if timestamp:
        ts = datetime.utcnow().strftime('%Y%m%dT%H%M%S%f')[:-3]
        filename = '{}_{}'.format(filename, ts)

    with FileServer(protocol='http',
                    address=local_ip,
                    path=remote_path,
                    http_auth=http_auth) as fs:

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

        copy_dialog = Dialog([
            [r'Address or name of remote host', 'sendline()', None, True, False],
            [r'Destination filename', 'sendline()', None, True, False],
        ])

        cmd = 'curl --upload-file {} '.format(local_path)

        if http_auth:
            username = fs.get('credentials', {}).get('http', {}).get('username', '')
            password = to_plaintext(fs.get('credentials', {}).get('http', {}).get('password', ''))
            cmd += '-u {}:{} '.format(username, password)

        if mgmt_src_ip and proxy_port:
            cmd += 'http://{}:{}/{}'.format(
                    mgmt_src_ip, proxy_port, filename)
        elif mgmt_src_ip:
            cmd += 'http://{}:{}/{}'.format(
                    mgmt_src_ip, local_port, filename)
        else:
            log.error('Unable to determine management IP address to use to upload file')
            return False

        if vrf:
            cmd += ' vrf {}'.format(vrf)

        try:
            device.execute(cmd, reply=copy_dialog, timeout=timeout, append_error_pattern=[r'%\s*Error', r'%\s*Invalid'])
        except Exception:
            log.error('Failed to transfer file', exc_info=True)
            return False

    return True


def get_mgmt_src_ip_addresses(device):
    """ Get the source IP addresses connected via SSH to the device.

    Returns:
        List of IP addresses or []
    """
    output = device.execute('ifconfig eth0')

    #   inet addr:172.1.1.2  Bcast:172.1.1.255  Mask:255.255.255.0
    m = re.search(r'inet addr:(\S+)', output)
    if m:
        mgmt_ip = m.group(1)

    netstat_output = device.execute('netstat -an | grep {}:22'.format(mgmt_ip))
    # tcp        0      0 172.1.1.2:22        10.1.1.1:59905     ESTABLISHED -
    mgmt_src_ip_addresses = re.findall(r'\d+ +\S+:\d+ +(\S+):\d+ +ESTAB', netstat_output)
    if not mgmt_src_ip_addresses:
        log.error('Unable to find management session, cannot determine management IP addresses')
        return []

    return mgmt_src_ip_addresses


def delete_files(device, locations, filenames):
    """ Delete local file

        Args:
            device (`obj`): Device object
            locations (`list`): list of locations
                                  ex.) bootflash:/core/
            filenames (`list`): file name. regular expression is supported
        Returns:
            deleted_files (`list`): list of deleted files
    """
    deleted_files = []

    # loop by given locations
    for location in locations:
        if location[-1] != '/':
            location += '/'

        log.info('Checking {location}...'.format(location=location))
        parsed = device.parse('ls -l {location}'.format(location=location))

        # loop by given filenames
        for filename in filenames:

            # find target files by using Dq with regex
            matched_files = parsed.q.contains_key_value(
                'files', filename, value_regex=True).get_values('files')
            log.debug('Matched files to delete: {matched_files}'.format(
                matched_files=matched_files))
            # delete files which were found
            for file in matched_files:
                device.execute('rm -f {location}{file}'.format(
                    location=location, file=file))
                # build up list for return
                deleted_files.append('{location}{file}'.format(
                    location=location, file=file))

    return deleted_files
