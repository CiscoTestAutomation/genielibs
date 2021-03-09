"""Utility type functions that do not fit into another category"""

# Python
import logging
import re

# Genie
from genie.libs.sdk.apis.utils import get_config_dict

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
