"""Utility type functions that do not fit into another category"""

# Python
import logging
import re
import yaml

# Genie
from genie.libs.sdk.apis.utils import get_config_dict
from genie.libs.parser.nxos.ping import Ping
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


def get_mgmt_src_ip_addresses(device):
    """ Get the source IP addresses connected via SSH to the device.

    Returns:
        List of IP addresses or []
    """
    # tcp      ESTABLISHED  0         5.25.25.5(23)
    #          management   0         5.25.24.1(54062)
    show_sockets_output = device.execute('show sockets connection tcp')
    mgmt_src_ip_addresses = set(re.findall(
        r'tcp\s+ESTABLISHED\s+0\s+\S+\((?:22|23)\).+management +\d+ +(\S+)\(\d+\)',
        show_sockets_output, re.S))
    if not mgmt_src_ip_addresses:
        log.error('Unable to find management session, cannot determine management IP addresses')
        return []

    log.info('Device management source IP addresses: {}'.format(mgmt_src_ip_addresses))

    return mgmt_src_ip_addresses


def get_mgmt_ip_and_mgmt_src_ip_addresses(device):
    """ Get the management IP and source IP addresses connected via SSH to the device.

    Returns:
        List of IP addresses or []
    """
    # tcp      ESTABLISHED  0         5.25.25.5(23)
    #          management   0         5.25.24.1(54062)
    show_sockets_output = device.execute('show sockets connection tcp')
    mgmt_addresses = re.findall(
        r'tcp\s+ESTABLISHED\s+0\s+(\S+)\((?:22|23)\).+management +\d+ +(\S+)\(\d+\)',
        show_sockets_output, re.S)
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
    """ Get the management interface name.
    """
    return 'mgmt0'


def check_if_device_in_testbed_yaml(device_name, yaml_file):
    """ Check if the given device name is part of the devices yaml file

        Args:
            device_name ('str'): Name of the device to be found as a string
            yaml_file ('str'): Name(path) of the yaml file where the device
                       is to be found as a string
        Return value:
            Boolean. True, if found. False, if error/not found

    """
    try:
        with open(yaml_file, 'r') as myYamlFile:
            data = yaml.load(myYamlFile, Loader=yaml.FullLoader)
        for devices in data:
            if device_name in data[devices]:
                return True
    except Exception as e:
        log.warning("Failed to open/read {f}. Error: {e}".format(f=yaml_file, e=e))
    return False


def add_device_to_testbed_yaml_file(device_name, device_ip, yaml_file):
    """ Add device details to the devices yaml file

        Args:
            device_name ('str'): Name of the device to be added as a string
            device_ip ('str'): IP address of the device to be added as a string
            yaml_file ('str'): Name(path) of the yaml file where the device
                       is to be added as a string
        Return value:
            None

    """
    try:
        with open(yaml_file, 'r') as myYamlFile:
            data = yaml.safe_load(myYamlFile)
    except Exception as e:
        log.warning("Failed to open/read {f}. Error: {e}".format(f=yaml_file, e=e))
        return

    if "devices" in data:
        dict_contents = {'type': 'router', 'os': 'nxos', 'platform': 'n9k', 'alias': device_name, 'credentials': {'default': {'username': 'admin', 'password': 'insieme'}},
            'connections': {'cli': {'protocol': 'telnet', 'ip': device_ip}}}
        data['devices'][device_name] = dict_contents

    try:
        with open(yaml_file, 'w+') as write_file:
            yaml.safe_dump(data, write_file)
    except Exception as e:
        log.warning("Failed to open/write {f}. Error: {e}".format(f=yaml_file, e=e))
    return

def clear_logging(device):
    """ clear logging
        Args:
            device ('obj'): Device object
        Returns:
            output ('str'): Output of execution
        Raises:
            SubCommandFailure
    """

    try:
        output = device.execute("clear logging logfile")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear logging on {device}. Error:\n{error}".format(device=device, error=e)
        )

    return output