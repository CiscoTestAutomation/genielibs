"""Utility type functions that do not fit into another category"""

# Python
import logging
import re

# Genie
from genie.libs.sdk.apis.utils import get_config_dict
from genie.utils.timeout import Timeout

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
