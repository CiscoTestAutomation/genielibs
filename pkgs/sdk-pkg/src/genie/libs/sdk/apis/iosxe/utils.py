"""Utility type functions that do not fit into another category"""

# Python
import logging
import re
import jinja2
import shlex, subprocess
import time
from time import strptime
from datetime import datetime

# pyATS
from pyats.easypy import runtime

# Genie
from genie.utils.config import Config
from genie.utils.diff import Diff
from genie.libs.parser.utils.common import Common
from genie.utils.timeout import Timeout
from genie.libs.sdk.apis.utils import _cli, get_config_dict

# unicon
from unicon.eal.dialogs import Dialog, Statement
from unicon.core.errors import ConnectionError
from unicon.plugins.generic.statements import default_statement_list
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

    config_dict = get_config_dict(config)

    return config_dict


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


def export_packet_capture(device, testbed, filename, capture_name):
    """Export the packet capture to a pcap file

        Args:
            device (`obj`): Device object
            testbed (`obj`): Testbed object
            filename (`str`): Filename to save
            capture_name (`str`): Packet capture name

        Returns:
            pcap_file_name or None

        Raises:
            pyATS Results
    """

    if "tftp" in testbed.servers and "server" in testbed.servers["tftp"]:
        execution_server = testbed.servers["tftp"]["server"]
    else:
        raise Exception("Tftp server is missing from the testbed yaml file")

    pcap_file_name = filename.replace(".", "_") + ".pcap"
    log.info("Export the capture to {p}".format(p=pcap_file_name))

    try:
        out = device.execute(
            "monitor capture {capture_name} export tftp://{server}/"
            "{pcap_file_name}".format(
                capture_name=capture_name,
                server=execution_server,
                pcap_file_name=pcap_file_name,
            ),
            error_pattern=["Failed to Export"],
        )
    except SubCommandFailure:
        log.error("Invalid command: Failed to Export packet capture")
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
