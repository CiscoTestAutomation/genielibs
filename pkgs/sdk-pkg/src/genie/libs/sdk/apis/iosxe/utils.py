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


def delete_local_file(device, path, file):
    """ Delete local file

        Args:
            device (`obj`): Device object
            path (`str`): directory
            file (`str`): file name
        Returns:
            None
    """
    try:
        device.execute("delete {path}{file}".format(path=path, file=file))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not delete file {file} from device "
            "{device}".format(file=file, device=device.name)
        )


def get_config_from_file(device, disk, filename):
    """ Get configuration from a file in disk

        Args:
            device ('obj'): Device object
            disk ('str'): Disk name
            filename ('str'): File name
        Raises:
            SubCommandFailure
        Returns:
            Dictionary: Configuration 
    """

    try:
        config = device.execute(
            "more {disk}{filename}".format(disk=disk, filename=filename)
        )
    except SubCommandFailure as e:
        log.error(
            "Could not retrieve configuration information from "
            "file {filename}".format(filename=filename)
        )
        return None

    return get_config_dict(config)


def start_packet_capture(
    device, capture_name=None, interface=None, capture_command=None
):
    """Start packet capture

        Args:
            device (`obj`): Device object
            capture_name (`str`): Packet capture name
            interface (`str`): Interface to capture the packets on
            capture_command (`str`): Monitor command

        Returns:
            None

        Raises:
            pyATS Results
    """

    log.info("Start the packet capture")
    log.info("Clear packet buffer")
    # Making sure packet buffers are empty the next
    # time when capturing packets
    try:
        device.execute("no monitor capture {cn}".format(cn=capture_name))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in no monitor capture, Error: {}".format(str(e))
        ) from e
    # Set default
    monitor_command = capture_command
    if not capture_command:
        # User provided own command, use that one instead
        monitor_command = (
            "monitor capture {capture_name} interface {interface} "
            "out match any".format(
                capture_name=capture_name, interface=interface
            )
        )

    # Send capture command
    device.execute(monitor_command)

    # Start capture of packets
    # TODO: Karim - What if it fails
    try:
        device.execute(
            "monitor capture {capture_name} start".format(
                capture_name=capture_name
            )
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in monitor capture, Error: {}".format(str(e))
        ) from e


def stop_packet_capture(device, capture_name):

    """Stop the packet capture

        Args:
            device (`obj`): Device object
            capture_name (`str`): Packet capture name

        Returns:
            None

        Raises:
            pyATS Results
    """

    log.info("Stop the packet capture")
    try:
        device.execute(
            "monitor capture {capture_name} stop".format(
                capture_name=capture_name
            )
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in monitor capture, Error: {}".format(str(e))
        ) from e


def export_packet_capture(device, testbed, filename, capture_name, protocol='tftp',
                          path='', username='', password=''):

    """Export the packet capture to a pcap file

        Args:
            device (`obj`): Device object
            testbed (`obj`): Testbed object
            filename (`str`): Filename to save
            capture_name (`str`): Packet capture name
            protocol (`str`): Protocol name
            path (`str`): Path to export
            username (`str`): user name
            password (`str`): password


        Returns:
            pcap_file_name or None

        Raises:
            pyATS Results
    """

    if protocol in testbed.servers and "server" in testbed.servers[protocol]:
        execution_server = testbed.servers[protocol]["server"]
    else:
        raise Exception("{pro} server is missing from the testbed yaml file".format(pro=protocol))

    pcap_file_name = filename.replace(".", "_") + ".pcap"

    credential = ''
    if username and password:
        credential = '{}:{}@'.format(username, password)

    export_to = '{pro}://{credential}{server}/{path}/{pcap_file_name}'.format(
                pro=protocol, path=path,
                credential=credential,
                server=execution_server,
                pcap_file_name=pcap_file_name)

    cmd = "monitor capture {capture_name} export {export_to}".format(
            capture_name=capture_name, export_to=export_to)

    log.info("Export the capture to {p}".format(p=pcap_file_name))
    try:
        out = device.execute(cmd, error_pattern=["Failed to Export"])
    except SubCommandFailure:
        log.error("Invalid command: Failed to Export packet capture")
        return None

    except Exception as e:
        log.error("Failed to export pcap file: {e}".format(e=e))
        return None

    # Making sure packet buffers are empty the next
    # time when capturing packets
    clear_packet_buffer(device, capture_name)

    return pcap_file_name


def clear_packet_buffer(device, capture_name):
    """Clear packet buffer

        Args:
            device (`obj`): Device object

        Returns:
            None

        Raises:
            pyATS Results
    """
    # Making sure packet buffers are empty the next
    # time when capturing packets
    try:
        device.execute(
            "no monitor capture {capture_name}".format(
                capture_name=capture_name
            )
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in no monitor capture, Error: {}".format(str(e))
        ) from e


def ping_interface_success_rate(device, ips, success_rate, **kwargs):
    """ Ping interfaces and verify success rate
        Args:
            device (`obj`): Device object
            ips (`list`): IP list to ping
            ips (`str`): Single IP address to ping
            success_rate (`int`): Ping success rate
        Returns:
            None
    """
    if isinstance(ips, str):
        log.info("Pinging '{ip}'".format(ip=ips))
        try:
            out = device.ping(addr=ips, **kwargs)
        except Exception as e:
            raise Exception("Failed in ping, Error: {}".format(str(e))) from e
        p = re.compile(r"Success +rate +is +(?P<rate>\d+) +percent.*")
        m = p.search(out)
        if not m or int(m.groupdict()["rate"]) < int(success_rate):
            raise Exception(
                "Ping success rate was lower than '{s}'".format(s=success_rate)
            )
    else:
        for ip in ips:
            log.info("Pinging '{ip}'".format(ip=ip))
            try:
                out = device.ping(addr=ip, **kwargs)
            except Exception as e:
                raise Exception(
                    "Failed in ping, Error: {}".format(str(e))
                ) from e
            p = re.compile(r"Success +rate +is +(?P<rate>\d+) +percent.*")
            m = p.search(out)
            if not m or int(m.groupdict()["rate"]) < int(success_rate):
                raise Exception(
                    "Ping success rate was lower than '{s}'".format(
                        s=success_rate
                    )
                )


def change_hostname(device, name):
    """ Change the hostname on device

        Args:
            device('obj'): device to change hostname on
            name('str'): name to change hostname to

        Returns:
            N/A
    """
    log.info('Changing hostname to "{}".'.format(name))

    device.state_machine.hostname = name
    try:
        device.configure("hostname {}".format(name))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in changing hostname on device"
            " {device}, Error: {e}".format(device=device.name, e=str(e))
        ) from e


def save_running_config_configuration(device):
    """Save configuration on the device after configure action

        Args:
            device (`obj`): Device object

        Returns:
            None
    """

    try:
        device.execute("write memory")
    except Exception as e:
        raise Exception("{}".format(e))


def set_clock(device, datetime):
    """ Set clock date and time on device

        Args:
            device ('obj')        : Device object to update clock
            datetime ('str') : Date and time value
                ex.)
                    datetime = '23:55:00 20 Dec 2019'
        Returns:
            None
    """
    try:
        device.execute("clock set {}".format(datetime))
    except Exception as e:
        raise Exception("{}".format(e))


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
    remote_path = "scp://{id}@{ip}/{rp}".format(id=username,
                                                ip=remote_device_ip,
                                                rp=remote_path)

    s1 = Statement(pattern=r".*Address or name of remote host",
                   action="sendline()",
                   args=None,
                   loop_continue=True,
                   continue_timer=False)
    s2 = Statement(pattern=r".*Destination username",
                   action="sendline()",
                   args=None,
                   loop_continue=True,
                   continue_timer=False)
    s3 = Statement(pattern=r".*Destination filename",
                   action="sendline()",
                   args=None,
                   loop_continue=True,
                   continue_timer=False)
    s4 = Statement(pattern=r".*Password:",
                   action="sendline({pw})".format(pw=password),
                   args=None,
                   loop_continue=True,
                   continue_timer=False)
    dialog = Dialog([s1, s2, s3, s4])

    try:
        if vrf:
            out = device.execute("copy {lp} {rp} vrf {vrf}".format(
                lp=local_path, rp=remote_path, vrf=vrf),
                                 reply=dialog)
        else:
            out = device.execute("copy {lp} {rp}".format(lp=local_path,
                                                         rp=remote_path),
                                 reply=dialog)
    except Exception as e:
        raise Exception("{}".format(e))

    # return True/False depending on result
    return 'bytes copied in' in out
