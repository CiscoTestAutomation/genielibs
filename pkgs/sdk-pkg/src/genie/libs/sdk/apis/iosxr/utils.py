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
from genie.libs.sdk.apis.utils import (
    copy_to_device as generic_copy_to_device)

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



def copy_to_device(device,
                   remote_path,
                   local_path='harddisk:',
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
        local_path (str): local file path to copy to on the device (default: harddisk:)
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
    return generic_copy_to_device(device=device,
                                  remote_path=remote_path,
                                  local_path=local_path,
                                  server=server,
                                  protocol=protocol,
                                  vrf=vrf,
                                  timeout=timeout,
                                  compact=compact,
                                  use_kstack=use_kstack,
                                  fu=fu,
                                  http_auth=http_auth,
                                  **kwargs)


def get_mgmt_src_ip_addresses(device):
    """ Get the source IP addresses connected via SSH or telnet to the device.

    Returns:
        List of IP addresses or []
    """
    # 0x00007f2fbc01b4b8 0x60000000      0     32  127.1.1.2:23       127.1.1.1:54860    ESTAB
    show_tcp_output = device.execute('show tcp brief | inc ":22|:23"')
    mgmt_src_ip_addresses = re.findall(r' +(\S+):\d+ +ESTAB', show_tcp_output)
    if not mgmt_src_ip_addresses:
        log.error('Unable to find management session, cannot determine management IP addresses')
        return []

    return mgmt_src_ip_addresses


def get_mgmt_ip_and_mgmt_src_ip_addresses(device):
    """ Get the management IP address and management source addresses.

    Returns:
        Tuple of mgmt_ip and list of IP address (mgmt_ip, [mgmt_src_addrs]) or None
    """
    tcp_output = device.execute('show tcp brief | inc ":22|:23"')

    # 0x00007f2fbc01b4b8 0x60000000      0     32  127.1.1.2:23       127.1.1.1:54860    ESTAB
    mgmt_addresses = re.findall(r'\w+ +(\S+):(?:22|23) +(\S+):\d+ +ESTAB', tcp_output)
    if mgmt_addresses:
        mgmt_ip = [m[0] for m in mgmt_addresses][0]
        mgmt_src_ip_addresses = set([m[1] for m in mgmt_addresses])
    else:
        log.error('Unable to find management session, cannot determine management IP addresses')
        return []

    log.info('Device management IP: {}'.format(mgmt_ip))
    log.info('Device management source IP addresses: {}'.format(mgmt_src_ip_addresses))

    return (mgmt_ip, mgmt_src_ip_addresses)


def get_mgmt_interface(device, mgmt_ip=None):
    """ Get the name of the management interface.

    if the mgmt_ip is provided, will use that for the lookup. If not, will
    call the get_mgmt_ip API to get the IP.

    Args:
        mgmt_ip: (str) IP address of the management interface (optional)

    Returns:
        String with interface name
    """
    mgmt_ip = mgmt_ip or device.api.get_mgmt_ip()
    out = device.parse('show ip interface brief')
    result = out.q.contains_key_value(key='ip_address', value=mgmt_ip).get_values('interface')
    if result:
        return result[0]

def clear_logging(device):
    """ clear logging
        Args:
            device ('obj'): Device object
        Returns:
            output ('str'): Output of execution
        Raises:
            SubCommandFailure
    """
    dialog = Dialog([Statement(pattern=r'Clear logging buffer \[confirm\] \[y/n\] :.*', action='sendline(y)',loop_continue=True,continue_timer=False)])

    try:
        output = device.execute("clear logging", reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear logging on {device}. Error:\n{error}".format(device=device, error=e)
        )

    return output
