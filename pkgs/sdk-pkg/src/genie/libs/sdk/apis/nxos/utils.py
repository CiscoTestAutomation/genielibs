"""Utility type functions that do not fit into another category"""

# Python
import logging
import re

# Genie
from genie.libs.sdk.apis.utils import get_config_dict
from genie.libs.parser.nxos.ping import Ping
from genie.libs.filetransferutils import FileServer
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# unicon
from unicon.eal.dialogs import Dialog, Statement
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def scp(device,
        local_path,
        remote_path,
        remote_device,
        remote_user=None,
        remote_pass=None,
        remote_via=None,
        vrf=None,
        return_filename=False):
    """ copy files from local device to remote device via scp
        Args:
            device (`obj`) : Device object (local device)
            local_path (`str`): path with file on local device
            remote_device (`str`): remote device name
            remote_path (`str`): path with/without file on remote device
            remote_user (`str`): use given username to scp
                                 Default to None
            remote_pass (`str`): use given password to scp
                                 Default to None
            remote_via (`str`) : specify connection to get ip
                                 Default to None
            vrf (`str`): use vrf where scp find route to remote device
                                 Default to None
            return_filename (`bool`): if True, will return list of copied files
        Returns:
            result (`bool` or `tuple`): True if scp successfully done 
                                        if return_filename is True, return list of copied filename

    """
    return_filenames = []

    # convert from device name to device object
    remote_device = device.testbed.devices[remote_device]
    # set credential for remote device
    username, password = remote_device.api.get_username_password()
    if remote_user:
        username = remote_user
    if remote_pass:
        password = remote_pass

    # find ip for remote server from testbed yaml
    if remote_via:
        if remote_via in remote_device.connections:
            remote_device_ip = str(remote_device.connections[remote_via]['ip'])
        else:
            log.warn(
                'remote_via {rv} for device {d} is not defined in testbed.yaml.'
                .format(rv=remote_via, d=remote_device.name))
            return return_filenames if return_filename else False
    else:
        remote_device_ip = str(
            remote_device.connections[remote_device.via]['ip'])

    # complete remote_path with credential and ip
    if remote_path[-1] != '/':
        remote_path += '/'
    remote_path = "scp://{id}@{ip}/{rp}".format(id=username,
                                                ip=remote_device_ip,
                                                rp=remote_path)

    s1 = Statement(pattern=r".*Are you sure you want to continue connecting",
                   action="sendline(yes)",
                   args=None,
                   loop_continue=True,
                   continue_timer=False)
    s2 = Statement(pattern=r".*password:",
                   action="sendline({pw})".format(pw=password),
                   args=None,
                   loop_continue=True,
                   continue_timer=False)
    dialog = Dialog([s1, s2])

    try:
        if vrf:
            out = device.execute("copy {lp} {rp} vrf {vrf}".format(
                lp=local_path, rp=remote_path, vrf=vrf),
                                 reply=dialog)

            # 1612443652_0x1b01_bgp_log.4609.tar.gz
            p = re.compile(
                r'^(?P<fn>(?!{username})\S+\.\S+)'.format(username=username))
            for line in out.splitlines():
                m = p.match(line)
                if m:
                    fn = m.groupdict()['fn']
                    if fn not in return_filenames:
                        return_filenames.append(fn)

        else:
            out = device.execute("copy {lp} {rp}".format(lp=local_path,
                                                         rp=remote_path),
                                 reply=dialog)
    except Exception as e:
        log.warn("Failed to copy from {lp} to {rp} via scp: {e}".format(
            lp=local_path, rp=remote_path, e=e))
        return False

    if return_filename:
        return return_filenames
    else:
        # return True/False depending on result
        return 'Copy complete.' in out

def get_md5_hash_of_file(device, file, timeout=60):
    """ Return the MD5 hash of a given file.

    Args:
        device (obj): Device to execute on
        file (str): File to calculate the MD5 on
        timeout (int, optional): Max time in seconds allowed for calculation.
            Defaults to 60.

    Returns:
        MD5 hash (str), or None if something went wrong
    """
    # show file test_file.bin md5sum
    # f9e90a6ca1a911a5e89a1bbac088bfec
    try:
        return device.execute('show file {} md5sum'.format(file),
                              timeout=timeout)
    except Exception as e:
        log.warning(e)
        return None

def ping(device,
         address,
         ttl=None,
         timeout=None,
         tos=None,
         dscp=None,
         size=None,
         count=None,
         source=None,
         rapid=False,
         do_not_fragment=False,
         validate=False,
         vrf=None,
         command=None,
         output=None):
    """ execute ping and parse ping result and return structure data

    Args:
        device ('obj'): Device object
        address ('str'): Address value
        tos ('int'): Not supported. type of service value
        dscp (`str`): Not supported. DSCP value
        size ('str'): data bytes expected
        ttl ('int'): Not supported
        timeout ('int'): timeout interval
        count ('int'): repeat count
        source ('str'): source address or interface, default: None
        rapid ('bool'): Not supported
        do_not_fragment ('bool'): enable do not fragment bit in IP header, default: False
        validate (`bool`): Not supported. validate reply data, default: False
        vrf ('str'): VRF name
        command (`str`): ping command. This will ignore all other arguments
        output (`str`): ping command output. no parser call involved
    Returns:
        Boolean
    Raises:
        None

    """
    try:
        obj = Ping(device=device)
        return obj.parse(addr=address,
                         vrf=vrf,
                         tos=tos,
                         dscp=dscp,
                         size=size,
                         ttl=ttl,
                         timeout=timeout,
                         count=count,
                         source=source,
                         rapid=rapid,
                         do_not_fragment=do_not_fragment,
                         validate=validate,
                         command=command,
                         output=output)
    except SchemaEmptyParserError:
        log.info('parsed_output was empty')
        return {}
    except Exception as e:
        log.warning(e)
        return {}


def copy_to_script_host(device,
                 filename,
                 local_path=None,
                 timeout=300,
                 vrf='management'):
    """
    Copy a file from the device to the local system where the script is running.
    Uses HTTP. Only supported via telnet or SSH sessions.

    Args:
        device (Device): device object
        filename (str): filename to copy
        local_path (str): local path to copy the file to, defaults to '.'
        timeout('int'): timeout value in seconds, default 300
        vrf (str): vrf name to use (default: management)

    Returns:
        (boolean): True if successful, False if not

    The local IP adddress will be determined from the spawned telnet or ssh session.
    A temporary http server will be created and the show tech file will be sent
    to the host where the script is running.

    If the device is connected via proxy (unix jump host) and the proxy has
    'socat' installed, the upload will be done via the proxy automatically.
    """
    local_path = local_path or '.'

    # Can only retrieve the file if this is a VTY connection
    if not device.api.is_connected_via_vty():
        log.error('Not on VTY terminal, cannot retrieve show tech file')
        return False

    # tcp      ESTABLISHED  0         5.25.25.5(23)
    #          management   0         5.25.24.1(54062)
    show_sockets_output = device.execute('show sockets connection tcp')
    mgmt_src_ip_addresses = re.findall(r'management +\d+ +(\S+)\(\d+\)', show_sockets_output)

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

        copy_dialog = Dialog([
            [r'Address or name of remote host', 'sendline()', None, True, False],
            [r'Destination filename', 'sendline()', None, True, False],
        ])

        try:
            if mgmt_src_ip and proxy_port:
                device.execute('copy {} http://{}:{} vrf {}'.format(
                            filename, mgmt_src_ip, proxy_port, vrf),
                            reply=copy_dialog, timeout=timeout,
                            append_error_pattern=[r'%\s*Error', r'%\s*Invalid'])
            elif mgmt_src_ip:
                device.execute('copy {} http://{}:{} vrf {}'.format(
                            filename, mgmt_src_ip, local_port, vrf),
                            reply=copy_dialog, timeout=timeout,
                            append_error_pattern=[r'%\s*Error', r'%\s*Invalid'])
            else:
                log.error('Unable to determine management IP address to use to upload file')
                return False

        except Exception:
            log.error('Failed to transfer file', exc_info=True)
            return False

    return True
