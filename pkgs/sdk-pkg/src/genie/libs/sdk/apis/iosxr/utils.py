"""Utility type functions that do not fit into another category"""

# Python
import logging
import re

# Genie
from genie.libs.sdk.apis.utils import get_config_dict
from genie.utils.timeout import Timeout
from genie.libs.parser.iosxr.ping import Ping
from genie.libs.filetransferutils import FileServer
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# unicon
from unicon.eal.dialogs import Dialog, Statement
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def verify_ping(
    device, address, expected_max_success_rate=100, expected_min_success_rate=0,
    count=None, source=None, max_time=60, check_interval=10,
):
    """Verify ping

    Args:
            device ('obj'): Device object
            address ('str'): Address value
            expected_max_success_rate (int): Expected maximum success rate
            expected_min_success_rate (int): Expected minimum success rate
            count ('int'): Count value for ping command
            source ('str'): Source IP address, default: None
            max_time (`int`): Max time, default: 30
            check_interval (`int`): Check interval, default: 10
    """

    p = re.compile(r"Success +rate +is +(?P<rate>\d+) +percent.*")

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if address and count and source:
            cmd = 'ping {address} source {source} count {count}'.format(
                    address=address,
                    source=source,
                    count=count)
        elif address and count:
            cmd = 'ping {address} count {count}'.format(
                    address=address,
                    count=count)
        elif address and source:
            cmd = 'ping {address} source {source}'.format(
                    address=address,
                    source=source)
        elif address:
            cmd = 'ping {address}'.format(address=address)
        else:
            log.info('Need to pass address as argument')
            return False
        try:
            out = device.execute(cmd)
        except SubCommandFailure as e:
            timeout.sleep()
            continue

        rate = int(p.search(out).groupdict().get('rate', 0))

        if expected_max_success_rate >= rate >= expected_min_success_rate:
            return True

        timeout.sleep()
    return False

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
    # show md5 file test_file.bin
    # Sat Feb  6 21:38:34.001 UTC
    # 69c394d85d37fc15d445ae83155495e2
    try:
        return device.execute('show md5 file {}'.format(file),
                              timeout=timeout).split()[-1]
    except Exception as e:
        log.warning(e)
        return None

def scp(device,
        local_path,
        remote_path,
        remote_device,
        remote_user=None,
        remote_pass=None,
        remote_via=None,
        vrf=None):
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
        Returns:
            result (`bool`): True if scp successfully done 
    """
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
        remote_device_ip = str(remote_device.connections[remote_via]['ip'])
    else:
        remote_device_ip = str(
            remote_device.connections[remote_device.via]['ip'])

    # complete remote_path with credential and ip
    if remote_path[-1] != '/':
        remote_path += '/'
    remote_path = "{id}@{ip}:/{rp}".format(id=username,
                                                ip=remote_device_ip,
                                                rp=remote_path)

    s1 = Statement(pattern=r".*Password:",
                   action="sendline({pw})".format(pw=password),
                   args=None,
                   loop_continue=True,
                   continue_timer=False)
    dialog = Dialog([s1])

    try:
        if vrf:
            out = device.execute("scp {lp} {rp} vrf {vrf}".format(
                lp=local_path, rp=remote_path, vrf=vrf),
                                 reply=dialog)
        else:
            out = device.execute("scp {lp} {rp}".format(lp=local_path,
                                                         rp=remote_path),
                                 reply=dialog)
    except Exception as e:
        log.warn("Failed to copy from {lp} to {rp} via scp: {e}".format(
            lp=local_path, rp=remote_path, e=e))
        return False

    # return True/False depending on result
    return 'Transferred' in out

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
        validate (`bool`): validate reply data, default: False
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

    # Can only retrieve the file if this is a VTY connection
    if not device.api.is_connected_via_vty():
        log.error('Not on VTY terminal, cannot retrieve file')
        return False

    # 0x00007f2fbc01b4b8 0x60000000      0     32  127.1.1.2:23       127.1.1.1:54860    ESTAB
    show_tcp_output = device.execute('show tcp brief | inc ":22|:23"')
    mgmt_src_ip_addresses = re.findall(r' +(\S+):\d+ +ESTAB', show_tcp_output)

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
                device.execute('copy {} http://{}:{}'.format(
                            filename, mgmt_src_ip, proxy_port),
                            reply=copy_dialog, timeout=timeout, append_error_pattern=[r'%Error'])
            elif mgmt_src_ip:
                device.execute('copy {} http://{}:{}'.format(
                            filename, mgmt_src_ip, local_port),
                            reply=copy_dialog, timeout=timeout, append_error_pattern=[r'%Error'])
            else:
                log.error('Unable to determine management IP address to use to upload file')
                return False

        except Exception:
            log.error('Failed to transfer file', exc_info=True)
            return False

    return True
