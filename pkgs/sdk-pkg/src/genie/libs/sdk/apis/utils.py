"""Utility type functions that do not fit into another category"""

# Python
import os
import ast
import logging
import re
import json
import jinja2
import shlex
import subprocess
import time
import random
import copy
import operator
import psutil
import pathlib

from time import strptime
from datetime import datetime
from netaddr import IPAddress

# pyATS
from pyats.easypy import runtime
from pyats.utils.email import EmailMsg
from pyats.utils.fileutils import FileUtils
from pyats.utils.secret_strings import to_plaintext
from pyats.datastructures.logic import Not
from pyats.datastructures import ListDict
from pyats.aetest.utils.interaction import WebInteraction

# Genie
from genie.utils.config import Config
from genie.utils.diff import Diff
from genie.utils.timeout import Timeout
from genie.conf.base import Device
from genie.utils import Dq
from genie.libs.sdk.libs.utils.normalize import merge_dict
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.filetransferutils import FileServer

# unicon
from unicon.eal.dialogs import Dialog, Statement
from unicon.core.errors import ConnectionError
from unicon.plugins.generic.statements import default_statement_list
from unicon import Connection

log = logging.getLogger(__name__)


def _cli(device, cmd, timeout, prompt):
    """ Send command to device and get the output

        Args:
            device (`obj`): Device object
            cmd (`str`): Command
            timeout (`int`): Timeout in second
            prompt (`obj`): Unicon statement
        Returns:
            output (`obj`): Output
    """
    # Create a dialog
    state = device.state_machine.current_state
    pattern = device.state_machine.get_state(state).pattern

    device.send(cmd)
    statements = [prompt, Statement(pattern=pattern)]
    statements.extend(device.state_machine.default_dialog)
    statements.extend(default_statement_list)
    dialog = Dialog(statements)
    return dialog.process(device.spawn, timeout=timeout)


def tabber(device, cmd, expected, timeout=20):
    """ Verify if tab works as expected on device

        Args:
            device (`obj`): Device object
            cmd (`str`): Command
            expected (`str`): Expected output
            timeout (`int`): Timeout in second
        Returns:
            None
    """
    # Create a new state for prompt# cmd
    state = device.state_machine.current_state
    pattern = device.state_machine.get_state(state).pattern
    pattern_mark = "{b}{c}.*{e}".format(b=pattern[:-1], c=cmd, e=pattern[-1])

    prompt = Statement(
        pattern=pattern_mark,
        action="send(\x03)",
        args=None,
        loop_continue=True,
        continue_timer=False,
    )

    output = _cli(device, cmd + "\t", timeout, prompt)

    # Remove sent command
    output = output.match_output.replace(cmd, "", 1).replace("^C", "")
    output = escape_ansi(output)
    # Find location where command begins, and remove white space at the end
    trim_output = output.splitlines()[1]
    trim_output = trim_output[trim_output.find(cmd):].strip()

    if expected != trim_output:
        raise Exception("'{e}' is not in output".format(e=expected))


def question_mark(device, cmd, expected, timeout=20, state="enable"):
    """ Verify if ? works as expected on device

        Args:
            device (`obj`): Device object
            cmd (`str`): Command
            expected (`str`): Expected output
            timeout (`int`): Timeout in second
            state (`str`): Cli state
        Returns:
            None
    """
    output = question_mark_retrieve(device, cmd, timeout, state)

    # Find if expected exists in the output
    if expected not in output:
        raise Exception("'{e}' is not in output".format(e=expected))


def question_mark_retrieve(device, cmd, timeout=20, state="enable"):
    """ Retrieve output after pressing ? on device

        Args:
            device (`obj`): Device object
            cmd (`str`): Command
            timeout (`int`): Timeout in second
            state (`str`): Cli state
        Returns:
            output (`str`): Output
    """
    # Create a new state for prompt# cmd
    pattern = device.state_machine.get_state(state).pattern
    if state == "config":
        # then remove all except last line
        tmp_cmd = cmd.splitlines()[-1]
        pattern_mark = pattern[:-1] + tmp_cmd + pattern[-1]
    else:
        pattern_mark = pattern[:-1] + cmd + pattern[-1]

    prompt = Statement(
        pattern=pattern_mark,
        action="send(\x03)",
        args=None,
        loop_continue=True,
        continue_timer=False,
    )
    output = _cli(device, cmd + "?", timeout, prompt)

    # Remove sent command
    output = output.match_output.replace(cmd, "", 1).replace("^C", "")
    output = escape_ansi(output)
    return output


def escape_ansi(line):
    ansi_escape = re.compile(r"(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]")
    return ansi_escape.sub("", line)


def time_to_int(time):
    """ Cast time string to int in second

        Args:
            time(`str`): time string
        Returns:
            out(`int`): time in second
    """
    out = 0
    # support patterns like ['00:00:00', '2d10h', '1w2d']
    p = re.compile(r"^(?P<time>(\d+):(\d+):(\d+))?(?P<dh>(\d+)d(\d+)h)?"
                   r"(?P<wd>(\d+)w(\d)+d)?$")
    m = p.match(time)
    if m:
        group = m.groupdict()
        if group["time"]:
            out = (int(m.group(2)) * 3600 + int(m.group(3)) * 60 +
                   int(m.group(4)))
        elif group["dh"]:
            out = int(m.group(6)) * 3600 * 24 + int(m.group(7)) * 3600
        elif group["wd"]:
            out = (int(m.group(9)) * 3600 * 24 * 7 +
                   int(m.group(10)) * 3600 * 24)
    return out


def get_unconfig_line(config_dict, line):
    """ unconfigure specific line

        Args:
            config_dict (`str`): Config dict
            line (`str`): line to unconfig
        Returns:
            unconfig (`list`): list of unconfig strings
    """
    unconfig = []

    try:
        line_dict = config_dict[line]
    except Exception:
        raise Exception(
            "line '{}' is not in running config output".format(line))

    unconfig.append(line)
    for key in line_dict.keys():
        unconfig.append("no " + key)

    return unconfig


def get_config_dict(config):
    """ Cast config to Configuration dict

        Args:
            config ('str'): config string
        Returns:
            Configuration dict
    """
    cfg = Config(config)
    cfg.tree()
    return cfg.config


def compare_config_dicts(a, b, exclude=None):
    """ Compare two configuration dicts and return the differences

        Args:
            a (`dict`): Configuration dict
            b (`dict`): Configuration dict
            exclude (`list`): List of item to ignore. Supports Regex.
                              Regex must begins with ( )
        Returns:
            out (`str`): differences
    """
    excludes = [r"(^Load|Time|Build|Current|Using|exit|end)"]
    if exclude:
        excludes.extend(exclude)

    diff = Diff(a, b, exclude=excludes)
    diff.findDiff()

    return str(diff)


def copy_pcap_file(testbed, filename, command=None):
    """Copy pcap filename to runtime directory for analysis

        Args:
            testbed (`obj`): Testbed object
            filename (`str`): Pcap filename
            command ('str'): cli command to copy file from remote
                             server to local server
        Returns:
            None

        Raises:
            pyATS Results
    """
    if not command:
        if "port" in testbed.servers["scp"]["custom"]:
            command = ("sshpass -p {password} scp -P {port} {user}@{add}:"
                       "/{serv_loc}/{file} {loc}/{file}".format(
                           password=testbed.servers["scp"]["password"],
                           port=testbed.servers["scp"]["custom"]["port"],
                           user=testbed.servers["scp"]["username"],
                           add=testbed.servers["scp"]["address"],
                           serv_loc=testbed.servers["scp"]["custom"]["loc"],
                           file=filename,
                           loc=runtime.directory,
                       ))
        else:
            # In case of VIRL testbed where is no specific port
            # to connect to the server from
            command = ("sshpass -p {password} scp {user}@{add}:"
                       "/{serv_loc}/{file} {loc}/{file}".format(
                           password=testbed.servers["scp"]["password"],
                           user=testbed.servers["scp"]["username"],
                           add=testbed.servers["scp"]["address"],
                           serv_loc=testbed.servers["scp"]["custom"]["loc"],
                           file=filename,
                           loc=runtime.directory,
                       ))

    log.info("Copy pcap file '{file}' to '{loc}' for packet analysis".format(
        file=filename, loc=runtime.directory))

    args = shlex.split(command)
    try:
        subprocess.check_output(args)
    except Exception as e:
        log.error(e)
        raise Exception("Issue while copying pcap file to runtime directory"
                        " '{loc}'".format(loc=runtime.directory))

    return "{loc}/{file}".format(file=filename, loc=runtime.directory)


def get_neighbor_address(ip):
    """Get the neighbor address in a subnet /30

        Args:
            ip (`str`): Ip address to get the neighbor for

        Returns:
            None
    """

    # Get the neighbor IP address
    ip_list = ip.split(".")
    last = int(ip_list[-1])

    ip_list[-1] = str(last - 1) if last % 2 == 0 else str(last + 1)
    return ".".join(ip_list)


def has_configuration(configuration_dict, configuration):
    """ Verifies if configuration is present
        Args:
            configuration_dict ('dict'): Dictionary containing configuration
            configuration ('str'): Configuration to be verified
        Returns:
            True if configuration is found
    """

    for k, v in configuration_dict.items():
        if configuration in k:
            return True
        if isinstance(v, dict) and has_configuration(v, configuration):
            return True
    return False


def int_to_mask(mask_int):
    """ Convert int to mask
        Args:
            mask_int ('int'): prefix length is convert to mask
        Returns:
            mask value
    """
    bin_arr = ["0" for i in range(32)]
    for i in range(int(mask_int)):
        bin_arr[i] = "1"
    tmpmask = ["".join(bin_arr[i * 8:i * 8 + 8]) for i in range(4)]
    tmpmask = [str(int(tmpstr, 2)) for tmpstr in tmpmask]
    return ".".join(tmpmask)


def mask_to_int(mask):
    """ Convert mask to int
        Args:
            mask ('str'):  mask to int
        Returns:
            int value
    """
    return sum(bin(int(x)).count("1") for x in mask.split("."))


def copy_to_server(testbed,
                   protocol,
                   server,
                   local_path,
                   remote_path,
                   timeout=300,
                   fu_session=None,
                   quiet=False,
                   **kwargs):
    """ Copy file from directory to server

        Args:
            testbed ('obj'): Testbed object
            protocol ('str'): Transfer protocol
            server ('str'): Server name in testbed yaml or server ip address
            local_path ('str'): File to copy, including path
            remote_path ('str'): Where to save the file, including file name
            timeout('int'): timeout value in seconds, default 300
            fu_session ('obj'): existing FileUtils object to reuse
            quiet ('bool'): quiet mode -- does not print copy progress
        Returns:
            None

        Raises:
            Exception
    """

    if fu_session:
        _copy_to_server(protocol,
                        server,
                        local_path,
                        remote_path,
                        timeout=timeout,
                        fu_session=fu_session,
                        quiet=quiet,
                        **kwargs)

    else:
        with FileUtils(testbed=testbed) as fu:
            _copy_to_server(protocol,
                            server,
                            local_path,
                            remote_path,
                            timeout=timeout,
                            fu_session=fu,
                            quiet=quiet,
                            **kwargs)


def _copy_to_server(protocol,
                    server,
                    local_path,
                    remote_path,
                    timeout=300,
                    fu_session=None,
                    quiet=False,
                    **kwargs):
    remote = "{p}://{s}/{f}".format(p=protocol, s=server, f=remote_path)
    remote = fu_session.validate_and_update_url(remote)

    log.info("Copying {local_path} to {remote_path}".format(
        local_path=local_path, remote_path=remote))

    fu_session.copyfile(source=local_path,
                        destination=remote,
                        timeout_seconds=timeout,
                        quiet=quiet,
                        **kwargs)


def copy_file_from_tftp_ftp(testbed, filename, pro):
    """Copy file to runtime directory for analysis

        Args:
            testbed (`obj`): Testbed object
            filename (`str`): File name
            pro (`str`): Transfer protocol
        Returns:
            None
        Raises:
            pyATS Results
    """
    if "port" in testbed.servers[pro]["custom"]:
        command = ("sshpass -p {svr[password]} scp -P {svr[custom][port]} "
                   "{svr[username]}@{svr[address]}:"
                   "/{svr[custom][loc]}/{file} {loc}/{file}".format(
                       svr=testbed.servers[pro],
                       file=filename,
                       loc=runtime.directory))
    else:
        # In case of VIRL testbed where is no specific port
        # to connect to the server from
        command = (
            "sshpass -p {svr[password]} scp {svr[username]}@{svr[address]}:"
            "/{svr[custom][loc]}/{file} {loc}/{file}".format(
                svr=testbed.servers[pro], file=filename,
                loc=runtime.directory))

    log.info("Copy {pro} file '{file}' to '{loc}' for later analysis".format(
        pro=pro, file=filename, loc=runtime.directory))

    args = shlex.split(command)
    try:
        subprocess.check_output(args)
    except Exception as e:
        log.error(e)
        raise Exception("Issue while copying file to runtime directory"
                        " '{loc}'".format(loc=runtime.directory))

    return "{loc}/{file}".format(file=filename, loc=runtime.directory)


def load_jinja(
    path,
    file,
    vrf_name,
    bandwidth,
    packet_size,
    ref_packet_size,
    time_interval,
    ipp4_bps,
    ipp2_bw_percent,
    ipp0_bw_percent,
    interface,
):
    """Use Jinja templates to build the device configuration

        Args:
            device (`obj`): Device object
            vrf_name (`str`): Vrf name to be used in configuration
            bandwidth (`int`): In bps, bandwidth for traffic flow
            packet_size (`int`): Config packet size
            ref_packet_size (`int`): Refrenced packet size
            time_interval (`float`): In seconds, used for calculating bc
            ipp4_bps (`int`): In bps, bandwidth for IPP4 traffic
            ipp2_bw_percent (`int`): In percents, bandwidth for IPP2 traffic
            ipp0_bw_percent (`int`): In percents, bandwidth for IPP0 traffic
            interface (`str`): Where to apply the configured policies

        Returns:
            out
    """

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=path))

    template = env.get_template(file)
    return template.render(
        vrf_name=vrf_name,
        bandwidth=bandwidth,
        packet_size=packet_size,
        ref_packet_size=ref_packet_size,
        time_interval=time_interval,
        ipp4_bps=ipp4_bps,
        ipp2_bw_percent=ipp2_bw_percent,
        ipp0_bw_percent=ipp0_bw_percent,
        interface=interface,
    )


def get_time_source_from_output(output):
    """ Parse out 'Time Source' value from output
        Time source output example : 'Time source is NTP, 23:59:38.461 EST Thu Jun 27 2019'
                                     'Time source is NTP, *12:33:45.355 EST Fri Feb 7 2020'

        Args:
            output ('str'): Text output from command
        Returns:
            Datetime object
            Format : datetime(year, month, day, hour, minute, second, microseconds)
    """

    r1 = re.compile(
        r"Time\ssource\sis\sNTP\,\s\.*\*?(?P<hour>\d+)\:(?P<minute>\d+)\:"
        r"(?P<seconds>\d+)\.(?P<milliseconds>\d+)\s(?P<time_zone>"
        r"\S+)\s(?P<day_of_week>\S+)\s(?P<month>\S+)\s(?P<day>\d+)"
        r"\s(?P<year>\d+)")

    for line in output.splitlines():
        line = line.strip()

        result = r1.match(line)
        if result:
            group = result.groupdict()
            hour = int(group["hour"])
            minute = int(group["minute"])
            second = int(group["seconds"])
            milliseconds = int(group["milliseconds"])
            month = strptime(group["month"], "%b").tm_mon
            day = int(group["day"])
            year = int(group["year"])

            return datetime(year, month, day, hour, minute, second,
                            milliseconds * 1000)

    log.warning('Time source could not be found in output')


def get_delta_time_from_outputs(output_before, output_after):
    """ Get delta time from Time source of two outputs
        Time source example: 'Time source is NTP, 23:59:38.461 EST Thu Jun 27 2019'

        Args:
            output_before ('str'): Text output from show command
            output_after ('str'): Text output from show command
        Returns:
            Time delta in seconds
    """

    time_source_before = get_time_source_from_output(output_before)
    time_source_after = get_time_source_from_output(output_after)

    return (time_source_after - time_source_before).total_seconds()


def analyze_rate(rate):
    """ Get the traffic rate and the corresponding unit

        Args:
            rate (`str`): Passed rate as a string

        Returns:
            rate (`int`): Traffic rate
            rate_unit (`str`): Traffic rate unit
            original_rate (`str`): Original Traffic rate
    """

    no_unit = False

    if isinstance(rate, int):
        rate = str(rate)
        no_unit = True

    parse = re.compile(
        r"^(?P<original_rate>[0-9\.]+)(?P<rate_unit>[A-Za-z\%]+)?$")
    m = parse.match(rate)
    if not m:
        raise Exception("The provided rate is not in the correct "
                        "format in the trigger data file")

    parsed_rate = m.groupdict()["original_rate"]
    try:
        original_rate = int(parsed_rate)
    except BaseException:
        original_rate = float(parsed_rate)

    if m.groupdict()["rate_unit"]:
        rate_unit = m.groupdict()["rate_unit"]
        if "M" in rate_unit:
            rate_unit = "Mbps"
            rate = original_rate * 1000000
        elif "K" in rate_unit:
            rate_unit = "Kbps"
            rate = original_rate * 1000
        elif "G" in rate_unit:
            rate_unit = "Gbps"
            rate = original_rate * 1000000000
        elif "%" in rate_unit:
            rate = original_rate
    elif no_unit:
        # Case when recreating policy map on other interfaces
        # Bandwidth was already converetd before
        rate_unit = None
        rate = int(rate)
    else:
        rate_unit = None

    return rate, rate_unit, original_rate


def unit_convert(value, unit=None):
    """ Get value with given corresponding unit.
        If not unit is given, value will be converted to value without unit

        Args:
            value (`str`): value with unit like `10M`
            unit (`str`): unit type like `K`, `M`, `G`

        Returns:
            new_value (`float`): value after converting to given unit

        Examples:
            >>> dev.api.unit_convert('123K', 'M')
            0.123

            >>> dev.api.unit_convert('100M', 'K')
            100000.0

            >>> dev.api.unit_convert('100M')
            100000000.0
    """

    if unit not in ['K', 'M', 'G'] and unit is not None:
        raise Exception(
            'Provided unit `{u}` is incorrect. Please provide either `K`, `M` or `G`.'
            .format(u=unit))

    parse = re.compile(
        r"^(?P<original_value>[0-9\.]+)(?P<original_unit>[A-Za-z]+)?$")
    m = parse.match(value)
    if not m:
        raise Exception(
            "The provided value `{v}` is incorrect "
            "format. Please make sure the value is like `10M`.".format(
                v=value))

    parsed_rate = m.groupdict()["original_value"]
    try:
        original_value = int(parsed_rate)
    except BaseException:
        original_value = float(parsed_rate)

    new_value = None
    if m.groupdict()["original_unit"]:
        value_unit = m.groupdict()["original_unit"]
        if value_unit not in ['K', 'M', 'G']:
            raise Exception(
                'Unit with value `{v}` is incorrect. Please provide either `K`, `M` or `G`.'
                .format(v=value_unit))
        if value_unit == "G":
            new_value = original_value * 1000000000

        elif value_unit == "K":
            new_value = original_value * 1000
        elif value_unit == "M":
            new_value = original_value * 1000000
    if new_value:
        if unit == "G":
            new_value = new_value / 1000000000

        elif unit == "K":
            new_value = new_value / 1000
        elif unit == "M":
            new_value = new_value / 1000000
    return float(new_value)


def reconnect_device_with_new_credentials(
    device,
    testbed,
    username,
    password_tacacs,
    password_enable=None,
    password_line=None,
    connection_alias=None,
):
    """ Reconnect device
    Args:
        device ('obj'): Device object
        max_time ('int'): Max time in seconds trying to connect to device
        interval ('int'): Interval in seconds of checking connection
        sleep_disconnect ('int'): Waiting time after device disconnection
    Raise:
        ConnectionError
    Returns:
        N/A
    """
    device_name = device.name
    device.destroy()
    device = testbed.devices[device_name]
    device.tacacs.username = username
    device.passwords.tacacs = password_tacacs

    if password_enable:
        device.passwords.enable = password_enable

    if password_line:
        device.passwords.line = password_line

    if connection_alias:
        device.connect(via=connection_alias)
    else:
        device.connect()

    return device


def destroy_connection(device):
    """ Destroy connection device
        Args:
            device ('obj'): Device object

    """
    log.info("Destroying current connection")
    device.destroy_all()
    log.info("Connection destroyed")


def configure_device(device, config, config_timeout=150):
    """shut interface

        Args:
            device (`obj`): Device object
            config (`str`): Configuration to apply
            config_timeout ('int'): Timeout value in sec, Default Value is 150 sec
    """
    try:
        device.configure(config, timeout=config_timeout)
    except Exception as e:
        raise Exception("{}".format(e))
    return


def reconnect_device(device,
                     max_time=300,
                     interval=30,
                     sleep_disconnect=30,
                     via=None):
    """ Reconnect device
        Args:
            device ('obj'): Device object
            max_time ('int'): Max time in seconds trying to connect to device
            interval ('int'): Interval in seconds of checking connection
            sleep_disconnect ('int'): Waiting time after device disconnection
        Raise:
            ConnectionError
        Returns:
            N/A
    """
    destroy_connection(device=device)

    time.sleep(sleep_disconnect)
    timeout = Timeout(max_time=max_time, interval=interval)

    while timeout.iterate():
        try:
            if via:
                device.connect(via=via)
            else:
                device.connect()
        except Exception as e:
            log.info("Device {dev} is not connected".format(dev=device.name))
            destroy_connection(device=device)
            timeout.sleep()
            continue

        if device.is_connected():
            break

        timeout.sleep()

    if not device.is_connected():
        raise ConnectionError(
            "Could not reconnect to device {dev}".format(dev=device.name))

    log.info("Reconnected to device {dev}".format(dev=device.name))


def netmask_to_bits(net_mask):
    """ Convert netmask to bits
        Args:
            net_mask ('str'): Net mask IP address
            ex.) net_mask = '255.255.255.255'
        Raise:
            None
        Returns:
            Net mask bits
    """
    return IPAddress(net_mask).netmask_bits()


def bits_to_netmask(bits):
    """ Convert bits to netmask
        Args:
            bits ('int'): bits to converts
            ex.) bits = 32
        Raise:
            None
        Returns:
            Net mask
    """
    mask = (0xffffffff >> (32 - bits)) << (32 - bits)
    return (str((0xff000000 & mask) >> 24) + '.' +
            str((0x00ff0000 & mask) >> 16) + '.' +
            str((0x0000ff00 & mask) >> 8) + '.' + str((0x000000ff & mask)))


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
        local_path (str): local file path to copy to on the device (default: flash:)
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
        (str, None): console output if successful, None if not

    If the server is not specified, a HTTP server will be spawned
    on the local system and serve the directory of the file
    specified via remote_path and the copy operation will use http.

    If the device is connected via CLI proxy (unix jump host) and the proxy has
    'socat' installed, the transfer will be done via the proxy automatically.
    """
    local_path = local_path or 'flash:'

    if not fu:
        fu = FileUtils.from_device(device, protocol=protocol)

    if server:

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
        except Exception as e:
            log.info('Failed to copy file to device: {e}'.format(
                e = e
            ))
            
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

    mgmt_ip, mgmt_src_ip_addresses = device.api.get_mgmt_ip_and_mgmt_src_ip_addresses()

    mgmt_interface = device.api.get_mgmt_interface(mgmt_ip=mgmt_ip)

    # try figure out local IP address
    local_ip = device.api.get_local_ip()

    if local_ip in mgmt_src_ip_addresses:
        mgmt_src_ip = local_ip
    else:
        mgmt_src_ip = None

    remote_path_parent = str(pathlib.PurePath(remote_path).parent)

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

        if http_auth:
            username = fs.get('credentials', {}).get('http', {}).get('username', '')
            password = to_plaintext(fs.get('credentials', {}).get('http', {}).get('password', ''))
            source = 'http://{}:{}@'.format(username, password)
        else:
            source = 'http://'

        if mgmt_src_ip and proxy_port:
            source += '{}:{}/{}'.format(mgmt_src_ip, proxy_port, remote_path)
        elif mgmt_src_ip:
            source += '{}:{}/{}'.format(mgmt_src_ip, local_port, remote_path)
        else:
            log.error('Unable to determine management IP address to use to download file')
            return None

        try:
            fu.validate_and_update_url = lambda url, *args, **kwargs: url  # override to avoid url changes
            fu.get_server = lambda *args, **kwargs: None  # override to suppress log messages
            return fu.copyfile(source=source,
                        destination=local_path,
                        timeout_seconds=timeout,
                        device=device,
                        vrf=vrf,
                        interface=mgmt_interface)

        except Exception:
            log.error('Failed to transfer file', exc_info=True)
            return None


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
        remote_path (str): Path on the server (default: .) (optionally include filename)
        server (str): Server to copy file to (optional)
        protocol (str): Protocol to use to copy (default: http)
        vrf (str): VRF to use for copying (default: None)
        timeout('int'): timeout value in seconds, default 300
        timestamp (bool): include timestamp in filename (default: False)
        http_auth (bool): Use http authentication (default: True)

    Returns:
        (str, None): console output if successful, None if not

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

    fu = FileUtils.from_device(device, protocol=protocol)

    if server:

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

    mgmt_ip, mgmt_src_ip_addresses = device.api.get_mgmt_ip_and_mgmt_src_ip_addresses()

    mgmt_interface = device.api.get_mgmt_interface(mgmt_ip=mgmt_ip)

    # try figure out local IP address
    local_ip = device.api.get_local_ip()

    if local_ip in mgmt_src_ip_addresses:
        mgmt_src_ip = local_ip
    else:
        mgmt_src_ip = None

    if not filename:
        filename = pathlib.Path(os.path.basename(local_path.split(':')[-1]))
        if device.hostname not in str(filename):
            filename = '{}_{}'.format(device.hostname, slugify(filename.stem) + filename.suffix)
        else:
            filename = '{}'.format(slugify(filename.stem) + filename.suffix)

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

        if http_auth:
            username = fs.get('credentials', {}).get('http', {}).get('username', '')
            password = to_plaintext(fs.get('credentials', {}).get('http', {}).get('password', ''))
            destination = 'http://{}:{}@'.format(username, password)
        else:
            destination = 'http://'

        if mgmt_src_ip and proxy_port:
            destination += '{}:{}/{}'.format(mgmt_src_ip, proxy_port, filename)
        elif mgmt_src_ip:
            destination += '{}:{}/{}'.format(mgmt_src_ip, local_port, filename)
        else:
            log.error('Unable to determine management IP address to use to upload file')
            return None

        try:
            fu.validate_and_update_url = lambda url, *args, **kwargs: url  # override to avoid url changes
            fu.get_server = lambda *args, **kwargs: None  # override to suppress log messages
            return fu.copyfile(source=local_path,
                               destination=destination,
                               timeout_seconds=timeout,
                               device=device,
                               vrf=vrf,
                               interface=mgmt_interface)

        except Exception:
            log.error('Failed to transfer file', exc_info=True)
            return None



def get_file_size_from_server(device,
                              server,
                              path,
                              protocol,
                              timeout=300,
                              fu_session=None):
    """ Get file size from the server
    Args:
        device ('Obj'): Device object
        server ('str'): server address or hostname
        path ('str'): file path on server to check
        protocol ('srt'): protocol used to check file size
        timeout ('int'): check size timeout in seconds
        fu_session ('obj'): existing FileUtils object to reuse
    Returns:
         integer representation of file size in bytes
    """
    if fu_session:
        return _get_file_size_from_server(server,
                                          path,
                                          protocol,
                                          timeout=timeout,
                                          fu_session=fu_session)
    with FileUtils(testbed=device.testbed) as fu:
        return _get_file_size_from_server(server,
                                          path,
                                          protocol,
                                          timeout=timeout,
                                          fu_session=fu)


def _get_file_size_from_server(server,
                               path,
                               protocol,
                               timeout=300,
                               fu_session=None):
    """ Get file size from the server (works for sftp and ftp)
        Args:
            server ('str'): server address or hostname
            path ('str'): file path on server to check
            protocol ('srt'): protocol used to check file size
            timeout ('int'): check size timeout in seconds
            fu_session ('obj'): existing FileUtils object to reuse
        Returns:
             integer representation of file size in bytes
        """
    url = '{p}://{s}/{f}'.format(p=protocol, s=server, f=path)
    url = fu_session.validate_and_update_url(url)

    # get file size, and if failed, raise an exception
    try:
        return fu_session.stat(target=url, timeout_seconds=timeout).st_size
    except NotImplementedError as e:
        log.warning(
            'The protocol {} does not support file listing, unable to get file '
            'size.'.format(protocol))
        raise e from None
    except FileNotFoundError as e:
        log.error("Can not find file {} on server {}".format(path, server))
        raise e from None
    except Exception as e:
        if 'not found' in str(e):
            raise FileNotFoundError(str(e))
        raise Exception("Failed to get file size : {}".format(str(e)))


def modify_filename(device,
                    file,
                    directory,
                    protocol,
                    server=None,
                    append_hostname=False,
                    check_image_length=False,
                    limit=63,
                    unique_file_name=False,
                    unique_number=None,
                    new_name=None):
    """ Truncation is done such that protocol:/directory/image should not
        exceed the limited characters.
        This for older devices, where it does not allow netboot from rommon,
        if image length is more than provided limit (63 characters by default).
        Returns truncated image name, if protocol:/directory/image length
        exceeds limit, else image return without any change
        Args:
            device
            file ('str'): the file to be processed
            directory ('str'): the directory where the image will be copied
            protocol ('str'): the protocol used in the url
            server ('str'): server address used in calculation, if not provided then it
                            will take the longest server address from the testbed
            append_hostname ('bool'): option to append hostname to the end of the file
            check_image_length ('bool'): option to check the name length exceeds the limit
            limit ('int'): character limit of the url, default 63
            unique_file_name ('bool'): append a six digit random number to the end of
                                        file name to make it unique
            unique_number ('int'): provide a number to be used with unique_file_name
                                    instead of a random one
            new_name ('str'): replace original file name with new_name

        Raises:
            ValueError
        Returns:
            truncated image name
            """
    if not server:
        server = device.api.get_longest_server_address()

    if new_name:
        file = new_name

    image_name, image_ext = os.path.splitext(file)
    if check_image_length:
        log.info(
            'Checking if file length exceeds the limit of {}'.format(limit))
        url = ''.join([protocol, ':/', server, '//', directory])

        if not url.endswith('/'):
            url = url + '/'
        if len(url) + len(image_ext) + 1 > limit:
            raise ValueError('The length of the directory URL already exceeds'
                             ' {} characters.'.format(limit))

        length = len(url) + len(file)

        # counts hostname in length if provided
        if append_hostname:
            length += len(device.name) + 1

        # counts random number in length.  6 digits + underscore = 7
        if unique_file_name:
            length += 7

        # truncate image
        if length > limit:
            # always negative number
            diff = limit - length
            if abs(diff) > len(image_name):
                raise Exception('File name {} does not have enough '
                                'characters {} to truncate.'.format(
                                    image_name, abs(diff)))
            image_name = image_name[:diff]

    if append_hostname:
        image_name += '_' + device.name

    if unique_file_name:
        if unique_number:
            image_name += '_' + str(unique_number)
        else:
            rand_num = random.randint(100000, 999999)
            image_name += '_' + str(rand_num)

    new_name = ''.join([image_name, image_ext])
    if new_name != file:
        log.info('File name changed to {}'.format(new_name))

    return new_name


def get_longest_server_address(device):
    """
    get the longest server address from the devices's testbed
    Args:
        device ('obj'): Device object
    Returns:
        the longest address in the testbed
    """
    addresses = []
    for server in device.testbed.servers.values():
        addr = server.get('address', '')
        if isinstance(addr, list):
            addresses.extend(addr)
        else:
            addresses.append(addr)

    return max(addresses, key=len)


def delete_file_on_server(testbed,
                          server,
                          path,
                          protocol='sftp',
                          timeout=300,
                          fu_session=None):
    """ delete the file from server
    Args:
        testbed ('obj'): testbed object containing the server info
        server ('str"): server address or hostname
        path ('str'): file path on server
        protocol ('str'): protocol used for deletion, defaults to sftp
        timeout ('int'):  connection timeout
    Returns:
        None
    """
    if fu_session:
        return _delete_file_on_server(server,
                                      path,
                                      protocol=protocol,
                                      timeout=timeout,
                                      fu_session=fu_session)
    with FileUtils(testbed=testbed) as fu:
        return _delete_file_on_server(server,
                                      path,
                                      protocol=protocol,
                                      timeout=timeout,
                                      fu_session=fu)


def _delete_file_on_server(server,
                           path,
                           protocol='sftp',
                           timeout=300,
                           fu_session=None):

    url = '{p}://{s}/{f}'.format(p=protocol, s=server, f=path)
    url = fu_session.validate_and_update_url(url)

    try:
        return fu_session.deletefile(target=url, timeout_seconds=timeout)
    except Exception as e:
        raise Exception("Failed to delete file : {}".format(str(e)))


def convert_server_to_linux_device(device, server):
    """
    Args
        converts a server block to a device object
        device ('obj'): Device object
        server ('str'): server hostname

    Returns:
        A Device object that can be connected
    """
    with FileUtils(testbed=device.testbed) as fu:
        server_block = fu.get_server_block(server)
        hostname = fu.get_hostname(server)

    return Device(name=server,
                  os='linux',
                  credentials=server_block.credentials,
                  connections={'linux': {
                      'ip': hostname,
                      'protocol': 'ssh'
                  }},
                  custom={'abstraction': {
                      'order': ['os']
                  }},
                  type='linux',
                  testbed=device.testbed)


def get_username_password(device, username=None, password=None, creds=None):
    """ Gets the username and password to use to log into the device console.
    """
    if username is None or password is None:
        if hasattr(device, 'credentials') and device.credentials:
            if creds is not None:
                cred = creds[0] if isinstance(creds, list) else creds
            # only 1 credential, but not 'default'
            elif len(device.credentials) == 1:
                for name in device.credentials:
                    cred = name
            else:
                cred = 'default'
            username = device.credentials.get(cred, {}).get("username", "")
            password = to_plaintext(
                device.credentials.get(cred, {}).get("password", ""))
        else:
            username = device.tacacs.get("username", "")
            password = device.passwords.get("line", "")

    if not username or not password:
        raise Exception("No username or password was provided.")

    return username, password


def compared_with_running_config(device, config):
    """ Show difference between given config and current config
        Args:
            config ('dict'): Config to compare with
        Raise:
            None
        Returns:
            Diff
    """
    current = device.api.get_running_config_dict()
    diff = Diff(current, config)

    diff.findDiff()

    return diff


def diff_configuration(device, config1, config2):
    """ Show difference between two configurations
        Args:
            config1 ('str'): Configuration one
            config2 ('str'): Configuration two
        Raise:
            None
        Returns:
            Diff
    """
    configObject1 = Config(config1)
    configObject2 = Config(config2)
    configObject1.tree()
    configObject2.tree()

    diff = Diff(configObject1.config, configObject2.config)

    diff.findDiff()

    return diff


def dynamic_diff_parameterized_running_config(device,
                                              base_config,
                                              mapping,
                                              running_config=None):
    """ Parameterize device interface from the configuration and return the parameterized configuration
        with respect to the mapping.
        Args:
            base_config ('str'): Content of the base config
            mapping ('dict'): Interface to variable mapping
            ex.) {'Ethernet2/1-48': '{{ int_1 }}', 'Ethernet5': '{{ int_2 }}'}
            running_config ('str'): The running config. If set to None, running config will be retrieved
                from currently connected device
        Raise:
            None
        Returns:
            Templated Config ('str'): The config that is parameterized
    """
    if running_config is None:
        running_config = device.execute('show running-config')

    output = diff_configuration(device, base_config,
                                running_config).diff_string('+')
    converted_map = {}

    # Make sure each mapping is not in short form
    for interface, variable in mapping.items():
        full_info = device.execute(
            'show interface {}'.format(interface)).split(' ')
        if len(full_info) > 0:
            # Assume full interface name is first word of output
            converted_map.setdefault(full_info[0], variable)
        else:
            raise Exception("Invalid interface short form")

    for interface, variable in converted_map.items():
        output = output.replace(' {} '.format(interface),
                                ' {} '.format(variable))
        output = output.replace(' {}\n'.format(interface),
                                ' {}\n'.format(variable))

    # Remove the end markers that are not at the end of file
    # End of file end markers will have the pattern '\nend' or '\nend '
    output = output.replace('\nend \n', '\n')
    output = output.replace('\nend\n', '\n')

    return output


def dynamic_diff_create_running_config(device, mapping, template, base_config):
    """ Creates a merged running config from template dynamic diff with
        variables replaced by mapping and merged with base config
        Args:
            mapping ('dict'): Variable to interface mapping
            ex.) {'{{ int_1 }}': 'Ethernet2/1-48', '{{ int_2 }}': 'Ethernet5'}
            template ('str'): Content of the dynamic diff template
            base_config ('str'): Content of the base config
        Raise:
            None
        Returns:
            Config ('str'): The merged running config from template
    """
    for variable, value in mapping.items():
        template = template.replace(variable, value)

    # Remove all end markers if any
    template = template.replace('\nend \n', '\n')
    template = template.replace('\nend\n', '\n')
    if template.endswith('\nend'):
        template = template[:-4]
    if template.endswith('\nend '):
        template = template[:-5]

    return '{}{}'.format(template, base_config)


def save_info_to_file(filename, parameters, header=[], separator=','):
    """ save information to a file in runtime directory
        Args:
            filename ('str'): Log file name
            parameters ('list'): Parameters list
            header ('list'): Header list
            separator ('str'): Separator for the parameters

            example for traffic loss:
                parameters = ['TC1', 'PE1-PE2-1000pps', '0.0', 'PASSED']
                header = ['uid', 'flows', 'outage', 'result']
                save_info_to_file('logs.txt', parameters, header=header)

                - in logs.txt
                uid,flows,outage,result
                TC1,PE1-PE2-1000pps,0.0,PASSED

        Returns:
            None
    """
    log_file = runtime.directory + "/" + filename
    hasFile = os.path.isfile(log_file)

    params = [str(p) for p in parameters]
    with open(log_file, 'a+') as f:
        if not hasFile and header:
            f.write(separator.join(header) + '\n')
        f.write(separator.join(params) + '\n')


def string_to_number(word):
    """ Converts from number(string) to number(integer)
        Args:
            word (`str`): number (string)
        Raise:
            Exception
        Returns:
            ret_num ('int|float'): number (integer|float)

        Example:

        >>> dev.api.string_to_number('1')
        1

        >>> dev.api.string_to_number('1.1')
        1.1

    """
    try:
        ret_num = int(word)
    except Exception:
        try:
            ret_num = float(word)
        except Exception:
            raise Exception(
                "'{word}' could not be converted to number.".format(word=word))

    return ret_num


def number_to_string(number):
    """ Converts from number(integer|float) to number(string)
        Args:
            number (`int|float`): number (integer|float)
        Raise:
            Exception
        Returns:
            ret_str ('str'): number (string)

        Example:

        >>> dev.api.number_to_string(1)
        '1'

        >>> dev.api.number_to_string(1.1)
        '1.1'

        >>> dev.api.number_to_string('1')
        '1'

        >>> dev.api.number_to_string('1.1')
        '1.1'

    """
    # if string, try to convert to number(string)
    if isinstance(number, str):
        try:
            number = float(number) if '.' in number else int(number)
        except Exception:
            try:
                number = float(number)
            except Exception:
                raise Exception(
                    "'{number}' could not be converted to string from number.".
                    format(number=number))

    if not isinstance(number, (int, float)):
        raise Exception(
            "'{number}' could not be converted to string from number.".format(
                number=number))

    try:
        ret_str = str(number)
    except Exception:
        raise Exception(
            "'{number}' could not be converted to string from number.".format(
                number=number))
    return ret_str


def get_list_items(name, index, index_end='', to_num=False, to_str=False):
    """ Get one or any of list items
        Args:
            name (`list`): list data
            index (`int`): number of index for list to get
            index_end (`int`): end number of index for list to get
            to_num (`bool`): flag to change value from str to number
            to_str (`bool`): flag to change value from number to str
        Raise:
            Exception
        Returns:
            ret_item (`any`): one or any of list items

        Example:

        >>> dev.api.get_list_items([1,2,3], 0)
        1

        >>> dev.api.get_list_items([[1,4],2,3], 0)
        [1, 4]

        >>> dev.api.get_list_items([[1,4],2,3], 1, to_str=True)
        '2'

        >>> dev.api.get_list_items([[1,4],2,'3'], 2, to_str=True)
        '3'

        >>> dev.api.get_list_items([[1,4], 2, '3'], 2, to_num=True)
        3

        >>> dev.api.get_list_items([[1,4], 2, '3'], 1, 2)
        [2, '3']

    """

    if not isinstance(name, list):
        raise Exception("{name} was not list.".format(name=name))

    try:
        ret_item = name[index:index_end + 1] if index_end else name[index]
    except BaseException:
        raise Exception("Could not get the item from {name}".format(name=name))
    if to_num:
        ret_item = string_to_number(ret_item)
    elif to_str:
        ret_item = number_to_string(ret_item)
    return ret_item


def get_dict_items(name,
                   keys,
                   contains='',
                   to_num=False,
                   to_str=False,
                   headers=False,
                   regex=False):
    """ Get one or any of dict items
        Args:
            name (`dict`): dict data
            key (`str|int|list`): key in dict. one or any
            contains (`str`): filter with Dq by this keyword
            regex (`bool`): if use regex for contains
            to_num (`bool`): flag to change value from str to number
            to_str (`bool`): flag to change value from number to str
            headers (`bool`): if return contains headers, or not
        Raise:
            Exception
        Returns:
            ret_item (`any`): list of one or of dict key/value items

        Example:

            bgp = {
                'id': '65000',
                'shutdown': False,
                'address_family': {
                    'ipv4': {
                        'total_neighbor': 3,
                        'neighbors': {
                            '10.1.1.1': {
                                'status': 'up',
                                'routes': 10,
                            },
                            '10.2.2.2': {
                                'status': 'down',
                                'routes': '20',
                            },
                            '10.3.3.3': {
                                'status': 'up',
                                'routes': 30
                            }
                        }
                    }
                }
            }

            Some examples with above structure data.

            >>> dev.api.get_dict_items(bgp, 'neighbors')
            [['10.1.1.1'], ['10.2.2.2'], ['10.3.3.3']]

            >>> dev.api.get_dict_items(bgp, ['id', 'shutdown'])
            [['65000', False]]

            >>> dev.api.get_dict_items(bgp, ['neighbors', 'routes', 'status'])
            [['10.1.1.1', 10, 'up'], ['10.2.2.2', '20', 'down'], ['10.3.3.3', 30, 'up']]

            >>> dev.api.get_dict_items(bgp, ['neighbors', 'routes', 'status'], 'ipv4')
            [['10.1.1.1', 10, 'up'], ['10.2.2.2', '20', 'down'], ['10.3.3.3', 30, 'up']]

            >>> dev.api.get_dict_items(bgp, ['neighbors', 'routes', 'status'], '10.1.1.1')
            [['10.1.1.1', 10, 'up']]

            >>> dev.api.get_dict_items(bgp, ['neighbors', 'routes', 'status'], ['10.1.1.1', '10.2.2.2])
            [['10.1.1.1', 10, 'up'], ['10.2.2.2', '20', 'down']]

            >>> dev.api.get_dict_items(bgp, 'routes', ['10.1.1.1', '10.2.2.2'])
            [[10], ['20']]

            >>> dev.api.get_dict_items(bgp, 'routes', ['10.1.1.1', '10.2.2.2'], to_str=True)
            [['10'], ['20']]

            >>> dev.api.get_dict_items(bgp, 'routes', ['10.1.1.1', '10.2.2.2'], to_num=True)
            [[10], [20]]

            >>> dev.api.get_dict_items(bgp, ['neighbors', 'routes', 'status'], ['10.1.1.1', '10.2.2.2])
            [['10.1.1.1', 10, 'up'], ['10.2.2.2', '20', 'down']]

            (Speceial case) if only one item in list, it will return value without list.
            >>> dev.api.get_dict_items(bgp, 'routes', '10.1.1.1')
            10

    """

    ret_item = []

    if not isinstance(name, dict):
        raise Exception("{name} was not dict.".format(name=name))

    if contains:
        if isinstance(contains, list):
            name2 = {}
            for item in contains:
                name2 = merge_dict(
                    name2,
                    Dq(name).contains(item, regex=regex).reconstruct())
            name = name2
        else:
            name = Dq(name).contains(contains, regex=regex).reconstruct()
    if isinstance(keys, list):
        ret_item.append(keys)
        value_lists = []
        for key in keys:
            dq_list = Dq(name).get_values(key)
            if len(keys) != len(dq_list):
                dq_list = sorted(set(dq_list), key=dq_list.index)
            value_list = [value for value in dq_list]
            value_lists.append(value_list)
        for i in range(len(value_list)):
            item_row = [item_column[i] for item_column in value_lists]
            ret_item.append(item_row)
    else:
        ret_item.append([keys])
        # get values by Dq
        dq_list = Dq(name).get_values(keys)
        dq_list = sorted(set(dq_list), key=dq_list.index)
        for value in dq_list:
            if to_num:
                ret_item.append([string_to_number(value)])
            elif to_str:
                ret_item.append([number_to_string(value)])
            else:
                ret_item.append([value])
    if headers is False:
        ret_item.pop(0)
    # special case. if only one item, return just one without list for ease of
    # use
    if len(ret_item) == 1 and len(ret_item[0]) == 1:
        ret_item = ret_item[0][0]
    return ret_item


def get_interfaces(device, link_name=None, opposite=False, phy=False, num=0):
    """ Get current or opposite interface from topology section of testbed file

        Args:
            device ('obj'): Device object
            link_name ('str'): link name
            opposite ('bool'): find opposite device interface
            phy ('bool'): find only physical interface
            num ('int'): num of interface to return

        Returns:
            topology dictionary

        Raises:
            None

    """
    # Example topology section in testbed yaml file:
    #         topology:
    #             # D1:
    #             Device1:
    #                 interfaces:
    #                     ge-0/0/1.0:
    #                         alias: D1-D2-1
    #                         link: D1-D2-1
    #                         type: ethernet
    #             # D2:
    #             Device2:
    #                 interfaces:
    #                     ge-0/0/0.0:
    #                         alias: D1-D2-1
    #                         link: D1-D2-1
    #                         type: ethernet
    if link_name:
        try:
            link = device.testbed.find_links(
                interfaces__device__name=device.name, name=link_name).pop()
        except Exception as e:
            log.error(str(e))
            return None
        intf_list = link.find_interfaces(
            device__name=Not(device.name) if opposite else device.name)
    else:
        intf_list = device.find_interfaces()

    if intf_list:
        intf_list.sort()

        if num > 0 and num <= len(intf_list):
            return intf_list[num - 1]
        phy_intf_list = []
        if phy:
            for intf in intf_list:
                phy_intf = copy.copy(intf)
                phy_intf.name = phy_intf.name.split('.')[0]
                phy_intf_list.append(phy_intf)

        return phy_intf_list if phy else intf_list
    else:
        return {}


def get_interface_interfaces(device,
                             link_name=None,
                             opposite=False,
                             phy=False,
                             num=0):
    """ Get current or opposite interface from topology section of testbed file

        Args:
            device ('obj'): Device object
            link_name ('str'): link name
            opposite ('bool'): find opposite device interface
            phy ('bool'): find only physical interface
            num ('int'): num of interface to return

        Returns:
            topology dictionary

        Raises:
            None
    """
    return get_interfaces(device=device,
                          link_name=link_name,
                          opposite=opposite,
                          phy=phy,
                          num=num)


def verify_pcap_has_imcp_destination_unreachable(pcap_location,
                                                 msg_type=3,
                                                 msg_code=0):
    """ Verify that the pcap file has messages with imcp destination
        unreachable with type and code

        Args:
            pcap_location ('str'): location of pcap file
            msg_type ('int'): pcap message type
            msg_code ('int'): pcap message code
        Returns:
            Boolean if icmp destination reachable message in pcap
    """

    try:
        import scapy.all
        rdpcap = scapy.all.rdpcap
        ICMP = scapy.layers.inet.ICMP
        ICMPv6 = scapy.layers.inet6._ICMPv6
        ICMPv6DestUnreach = scapy.layers.inet6.ICMPv6DestUnreach
    except ImportError:
        raise ImportError(
            'scapy is not installed, please install it by running: '
            'pip install scapy') from None

    pcap_object = rdpcap(pcap_location)

    for packet in pcap_object:
        if (packet.haslayer(ICMP) and packet.getlayer(ICMP).type == msg_type
                and packet.getlayer(ICMP).code == msg_code):
            return True
    return False


def verify_pcap_has_imcpv6_destination_unreachable(pcap_location,
                                                   msg_type=1,
                                                   msg_code=3):
    """ Verify that the pcap file has messages with imcpv6 destination
        unreachable with type and code

        Args:
            pcap_location ('str'): location of pcap file
            msg_type ('int'): pcap message type
            msg_code ('int'): pcap message code
        Returns:
            Boolean if icmpv6 destination reachable message in pcap
    """

    try:
        import scapy.all
        rdpcap = scapy.all.rdpcap
        ICMP = scapy.layers.inet.ICMP
        ICMPv6 = scapy.layers.inet6._ICMPv6
        ICMPv6DestUnreach = scapy.layers.inet6.ICMPv6DestUnreach
    except ImportError:
        raise ImportError(
            'scapy is not installed, please install it by running: '
            'pip install scapy') from None

    pcap_object = rdpcap(pcap_location)

    for packet in pcap_object:
        if (packet.haslayer(ICMPv6DestUnreach)
                and packet.getlayer(ICMPv6DestUnreach).type == msg_type
                and packet.getlayer(ICMPv6DestUnreach).code == msg_code):
            return True
    return False


def slugify(word):
    """ update all special characters in string to underscore
        Args:
            word (`str`): string which you want to convert special characters in the word to underscore
        Raise:
            Exception
        Returns:
            word

        Example:

        >>> dev.api.slugify('Ethernet1/1.100')
        Ethernet1_1_100

        >>> dev.api.slugify('2020-05-26_14:15:36.555')
        2020_05_26_14_15_36_555

    """
    return re.sub(r'\W+', '_', word)


def repeat_command_save_output(device, command, command_interval,
                               command_count, report_file):
    """
        Execute the {command} on the device and store the output to file, can
        repeat the same command with {command_count} and a sleep interval with
        {command_interval}.

        Args:
            command ('str'): Command to run on device
            command_interval ('int'): Waiting between command calls
            command_count ('int'): Number of times to call command
            report_file ('str'): File name to store in archive

        Raises:
            Parser and python file exceptions

        Returns:
            None
    """
    command_output_data = ""

    for i in range(command_count):
        log.info("Iteration: {}".format(str(i)))
        command_output_data += "\nIteration {iteration} of \"{command}\":\n".format(
            iteration=i, command=command)
        try:
            command_output_data += device.execute(command)

        except Exception as e:
            raise Exception("Failed to execute command {} error: {}".format(
                command, str(e)))

        time.sleep(command_interval)
        log.info("Going to sleep for {command_interval}".format(
            command_interval=command_interval))
    path = "{}/{}.txt".format(runtime.directory, report_file)
    try:
        with open(path, "w") as report_file_object:
            report_file_object.write(command_output_data)

    except Exception as e:
        raise Exception("Failed to write file {} error: {}".format(
            path, str(e)))

    return path


def send_email(from_email,
               to_email,
               subject='',
               body='',
               attachments=None,
               html_email=False,
               html_body=''):
    """
        Send an email from execution server where pyATS runs.
        Plain or HTML email can be sent.

        Args:
            from_email (list/str): list or string-list of addresses to be used
                                   in the generated email's "From:" field.
            to_email(list/str): list or string-list of addresses to be used
                                in the generated email's "To:" field.
            subject (str): alternate subject for the report email
            body (string): message body in the email
            attachments (list): list of attachments paths
            html_email (bool): flag to enable alternative email format
            html_body (string): html content

        Raises:
            python file exceptions

        Returns:
            None
    """
    email = EmailMsg(from_email, to_email, subject, body, attachments,
                     html_email, html_body)
    email.send()


def get_tolerance_min_max(value, expected_tolerance):
    """
       Get minimum and maximum tolerance range

        Args:
            value(int): value to find minumum and maximum range
            expected_tolerance ('int'): Expected tolerance precentage

        Returns:
            minimum and maximum value of tolerance
    """
    # Convert it to int
    value = int(value)

    # Expected tolerance %
    tolerance = (value * expected_tolerance) / 100

    # Minimum tolerance value
    min_value = abs(value - tolerance)

    # Maximum tolerance value
    max_value = abs(value + tolerance)

    return (min_value, max_value)


def verify_mpls_experimental_bits(pcap_location, expected_dst_address,
                                  expected_bit_value):
    """ Verify the first packet to have expected_dst_address has the
        MPLS experiement bits set to expected_bit_value

    Args:
        pcap_location (obj): PCAP file location
        expected_dst_address (str): Destination IP address to search for
        expected_bit_value (int): Expected bit value to check
    """

    try:
        from scapy.contrib.mpls import MPLS
        from scapy.all import rdpcap, IP, Raw
    except ImportError:
        raise ImportError(
            'scapy is not installed, please install it by running: '
            'pip install scapy') from None

    pcap_object = rdpcap(pcap_location)

    for packet in pcap_object:
        if IP in packet and packet[IP].dst == expected_dst_address:
            if MPLS in packet:
                return expected_bit_value == packet[MPLS].cos
        else:
            mpls_ = MPLS(packet[Raw])
            if IP in packet and packet[IP].dst == expected_dst_address:
                if MPLS in packet:
                    return expected_bit_value == packet[MPLS].cos

    return False

def verify_pcap_dscp_bits(pcap_location, expected_bits, position=0, expected_protocol=None,
                          expected_protocol_message_type=None, expected_dst_port_number=None,
                          expected_src_address=None, expected_dst_address=None, check_all=True,
                          expected_src_port_number=None, port_and_or='and'):
    """Verifies the dscp bits of packets in a capture file

    Args:
        pcap_location (str): Location of pcap file
        expected_bits (str/int): Expeceted bits to find / Integer to be converted to bits
        position (int, optional): Which packet to check. Defaults to 0.
        expected_protocol (str, optional): Expected protocol to verify against. Defaults to None
        expected_protocol_message_type (str, optional): Expected protocol message type. Defaults to None
                                                        Eg.BGPOpen, BGPUpdate, BGPKeepAlive
        expected_dst_port_number (int, optional): Expected destination port number to verify again. Defaults to None
        expected_src_address (str, optional): Expected source IP address. Defaults to None
        expected_dst_address (str, optional): Expected destination IP address. Defaults to None
        check_all (bool, optional): Ignore position and check all packets until one is found that meets criteria. Defaults to False
        expected_src_port_number (int, optional): Expected source port number to verify again. Defaults to None
        port_and_or (str, optional): Whether to and/or the expected port number results. Defaults to 'and'

    Returns:
        bool: True or False
    """
    # Defines whether to check for one or both port numbers
    if port_and_or.lower() == 'and':
        port_and_or_op = operator.and_
    elif port_and_or.lower() == 'or':
        port_and_or_op = operator.or_
    else:
        raise Exception("port_and_or must be either 'and' or 'or'")

    # Converts int to bit string, IE, 56 == '111000'
    if isinstance(expected_bits, int):
        expected_bits = format(expected_bits, '#010b')[4:]

    # Converts CS# into bit string, IE, CS7 == '111000'
    dscp_options_ = {
        'cs' + str(num): format(num, '#010b')[7:]
        for num in range(8)
    }
    if expected_bits.lower() in dscp_options_:
        expected_bits = dscp_options_.get(expected_bits.lower())

    # Import modules from scapy
    try:
        from scapy.all import rdpcap, IP, IPv6, UDP, Raw, TCP, load_contrib
        from scapy.contrib.ospf import OSPF_Hdr, OSPF_Hello
        from scapy.contrib.bgp import BGPKeepAlive, BGPOpen, BGPUpdate, BGP
        from scapy.contrib.rsvp import RSVP
        load_contrib("mpls")

    except ImportError:
        log.info('scapy is not installed, please install it by running: '
                 'pip install scapy')
        return False

    # If expected_protocol is an int, convert it to its respective protocol string
    if isinstance(expected_protocol, int):
        protocols_ = {46: 'rsvp'}
        expected_protocol = protocols_.get(expected_protocol)
        if not expected_protocol:
            raise Exception(
                "Supplied protocol integer is not currently available, please supply string representation instead"
            )

    pcap_object = rdpcap(pcap_location)

    for packet in pcap_object:
        if not check_all:
            packet = pcap_object[position]
        bits_ = None
        if IP in packet:
            # Six bits 111000
            bits_ = bin(packet[0].tos)[2:8]
        elif IPv6 in packet:
            # Six bits 111000
            bits_ = bin(packet[0].tc)[2:8]

        # Handles looking for protocols
        try:
            if str(expected_protocol).lower(
            ) == 'ospf' and OSPF_Hello not in OSPF_Hdr(packet[Raw]):
                continue
        except Exception:
            pass

        if str(expected_protocol).lower() == 'rsvp' and RSVP not in packet:
            continue

        if str(expected_protocol).lower() == 'udp' and UDP not in packet:
            continue

        if str(expected_protocol).lower() == 'tcp' and TCP not in packet:
            continue

        if str(expected_protocol_message_type).lower() == 'bgpkeepalive' and BGPKeepAlive not in packet:
            continue

        if str(expected_protocol_message_type).lower() == 'bgpopen' and BGPOpen not in packet:
            continue

        if str(expected_protocol_message_type).lower() == 'bgpupdate' and BGPUpdate not in packet:
            continue

        # Handles port numbers
        if expected_dst_port_number and expected_src_port_number:
            if not port_and_or_op(expected_dst_port_number == packet.dport,
                                  expected_src_port_number == packet.sport):
                continue
        else:
            if expected_dst_port_number and expected_dst_port_number != packet.dport:
                continue

            if expected_src_port_number and expected_src_port_number != packet.sport:
                continue

        # Handles src IPv4/IPv6 addresses
        if expected_src_address:
            if IP in packet and packet[IP].src != expected_src_address.split(
                    '/')[0]:
                continue
            if IPv6 in packet and packet[
                    IPv6].src != expected_src_address.split('/')[0]:
                continue

        # Handles dst IPv4/IPv6 addresses
        if expected_dst_address:
            if IP in packet and packet[IP].dst != expected_dst_address.split('/')[0]:
                continue
            if IPv6 in packet and packet[IPv6].dst != expected_dst_address.split('/')[0]:
                continue

        if bits_ and bits_.startswith(str(expected_bits)):
            return True

        if not check_all:
            break

    return False


def verify_pcap_packet_type(pcap_location, expected_type, position=0):
    """Verifies expected type of a packet

    Args:
        pcap_location (`str`): Location of pcap file
        expected_type (`str`): Expected type
        position (`int`, optional): Which packet to check. Defaults to 0.

    Returns:
        bool: True or False
    """

    try:
        from scapy.all import rdpcap, IP
    except ImportError:
        log.info('scapy is not installed, please install it by running: '
                 'pip install scapy')
        return False

    pcap_object = rdpcap(pcap_location)
    packet = pcap_object[position]
    target_type_ = packet[IP].version

    if expected_type == target_type_:
        return True

    return False


def verify_pcap_packet_protocol(pcap_location, expected_protocol, position=0):
    """Verifies expected protocol of a packet

    Args:
        pcap_location (`str`): Location of pcap file
        expected_protocol (`str`): Expected protocol name
        position (`int`, optional): Which packet to check. Defaults to 0.

    Returns:
        bool: True or False
    """

    try:
        from scapy.all import rdpcap, IP
    except ImportError:
        log.info('scapy is not installed, please install it by running: '
                 'pip install scapy')
        return False

    pcap_object = rdpcap(pcap_location)
    packet = pcap_object[position]
    protocol_ = packet[IP].proto

    if expected_protocol == protocol_:
        return True

    return False


def verify_pcap_packet_source_port(pcap_location,
                                   expected_source_port,
                                   position=0):
    """Verifies expected source port of a packet

    Args:
        pcap_location (`str`): Location of pcap file
        expected_source_port (`str`): Expected source port
        position (`int`, optional): Which packet to check. Defaults to 0.

    Returns:
        bool: True or False
    """

    try:
        from scapy.all import rdpcap, IP
    except ImportError:
        log.info('scapy is not installed, please install it by running: '
                 'pip install scapy')
        return False

    pcap_object = rdpcap(pcap_location)
    packet = pcap_object[position]
    src_port_ = packet[IP].sport

    if expected_source_port == src_port_:
        return True

    return False


def verify_pcap_packet_destination_port(pcap_location,
                                        expected_destination_port,
                                        position=0):
    """Verifies expected destination port of a packet

    Args:
        pcap_location (`str`): Location of pcap file
        expected_destination_port (`str`): Expected destination port
        position (`int`, optional): Which packet to check. Defaults to 0.

    Returns:
        bool: True or False
    """

    try:
        from scapy.all import rdpcap, IP
    except ImportError:
        log.info('scapy is not installed, please install it by running: '
                 'pip install scapy')
        return False

    pcap_object = rdpcap(pcap_location)
    packet = pcap_object[position]
    dst_port_ = packet[IP].dport

    if expected_destination_port == dst_port_:
        return True

    return False

def verify_pcap_mpls_packet(pcap_location, expected_src_address=None, expected_dst_address=None,
    expected_src_port_number=None, expected_dst_port_number=None, port_and_or='and',
    expected_inner_exp_bits=None, expected_outer_exp_bits=None, expected_tos=None,
    expected_protocol_message_type=None, expected_mpls_label=None,
    check_all=False, ipv6_flag=False):
    """ Verify pcap mpls packets values

    Args:
        pcap_location (obj): PCAP file location
        expected_src_address (str): Source IP address to search for
        expected_dst_address (str): Destination IP address to search for
        expected_src_port_number(int): Expected source port number to verify again. Defaults to None
        expected_dst_port_number (int): Expected destination port number to verify again. Defaults to None
        port_and_or (str, optional): Whether to and/or the expected port number results. Defaults to 'and'
        expected_inner_exp_bits (int): Expected inner Exp bits
        expected_outer_exp_bits (int): Expected outer Exp bits
        expected_tos (int): Expected tos value
        expected_protocol_message_type (str, optional): Expected protocol message type. Defaults to None
                                                        Eg.BGPOpen, BGPUpdate, BGPKeepAlive
        expected_mpls_label (str): Expected mpls label
        check_all (bool): Check all matching packets

    Returns:
        bool: True or False
    """

    # Defines whether to check for one or both port numbers
    if port_and_or.lower() == 'and':
        port_and_or_op = operator.and_
    elif port_and_or.lower() == 'or':
        port_and_or_op = operator.or_
    else:
        raise Exception("port_and_or must be either 'and' or 'or'")

    try:
        from scapy.contrib.mpls import MPLS
        from scapy.all import rdpcap, IP, IPv6, load_contrib
        from scapy.contrib.bgp import BGPKeepAlive, BGPOpen, BGPUpdate
        load_contrib("mpls")
    except ImportError:
        raise ImportError(
            'scapy is not installed, please install it by running: '
            'pip install scapy') from None

    pcap_object = rdpcap(pcap_location)
    supported = [IP, MPLS, IPv6]
    ip_packet = None

    for packet in pcap_object:
        if any(i for i in supported if i in packet):
            if not ipv6_flag:
                ip_packet = packet.getlayer(IP)
            else:
                if IPv6 in packet:
                    ip_packet = packet.getlayer(IPv6)
                else:
                    continue

            if expected_dst_address:
                if not ip_packet:
                    continue
                dst = ip_packet.dst
                if dst != expected_dst_address:
                    continue

            if expected_src_address:
                if not ip_packet:
                    continue
                src = ip_packet.src
                if src != expected_src_address:
                    continue


            # Handles port numbers
            if expected_dst_port_number and expected_src_port_number:
                if getattr(packet, "sport", None) and getattr(packet, "dport", None):
                    if not port_and_or_op(
                            expected_dst_port_number == packet.dport,
                            expected_src_port_number == packet.sport):
                        continue
            else:
                # To check the destination port. Here "continue" helps in checking all the packets with
                # destination port, If port is matched it returns True at the end of loop. If none of the
                # port matches, it goes out of loop and return False at the end of api.
                if expected_dst_port_number:
                    if getattr(packet, "dport", None):
                        if expected_dst_port_number != packet.dport:
                            continue
                    else:
                        continue

                #To check the source port
                if expected_src_port_number:
                    if getattr(packet, "sport", None):
                         if expected_src_port_number != packet.sport:
                            continue
                    else:
                        continue


            # Handles looking for protocol message types
            if str(expected_protocol_message_type).lower() == 'bgpkeepalive' and BGPKeepAlive not in packet:
                continue

            if str(expected_protocol_message_type).lower() == 'bgpopen' and BGPOpen not in packet:
                continue

            if str(expected_protocol_message_type).lower() == 'bgpupdate' and BGPUpdate not in packet:
                continue

            if expected_outer_exp_bits:
                if not packet.haslayer(MPLS):
                    continue
                mpls_layer = packet.getlayer(MPLS)
                mpls_outer = mpls_layer[0]
                mpls_outer_cos = mpls_outer.cos
                if bin(mpls_outer_cos) != bin(expected_outer_exp_bits):
                    if check_all:
                        return False
                    continue

            if expected_mpls_label:
                if not packet.haslayer(MPLS):
                    continue
                mpls_layer = packet.getlayer(MPLS)
                mpls_outer = mpls_layer[0]
                mpls_outer_label = mpls_outer.label
                if bin(mpls_outer_label) != bin(expected_mpls_label):
                    if check_all:
                        return False
                    continue

            if expected_inner_exp_bits:
                if not packet.haslayer(MPLS):
                    continue
                mpls_layer = packet.getlayer(MPLS)
                mpls_inner = mpls_layer[1]
                mpls_inner_cos = mpls_inner.cos
                if bin(mpls_inner_cos) != bin(expected_inner_exp_bits):
                    if check_all:
                        return False
                    continue

            if expected_tos is not None:
                # If it is an IPv6 packet, use .tc to get tos value
                # otherwise use .tos
                if not ip_packet:
                    continue
                ip_tos = ip_packet.tc if IPv6 in ip_packet else ip_packet.tos
                if not bin(ip_tos).startswith(bin(expected_tos)):
                    if check_all:
                        return False
                    continue
            return True

    return False


def verify_no_mpls_header(pcap_location, expected_dst_address=None):
    """ Verify no mpls header

    Args:
        pcap_location (obj): PCAP file location
        expected_dst_address (str): Destination IP address to search for

    Returns:
        bool: True or False

    """
    try:
        from scapy.contrib.mpls import MPLS
        from scapy.all import rdpcap, IP, load_contrib
        load_contrib("mpls")
    except ImportError:
        raise ImportError(
            'scapy is not installed, please install it by running: '
            'pip install scapy') from None

    pcap_object = rdpcap(pcap_location)
    for packet in pcap_object:
        if IP in packet:

            ip_packet = packet.getlayer(IP)

            if expected_dst_address:

                dst = ip_packet.dst
                if dst == expected_dst_address and MPLS not in packet:
                    return True

    return False


def save_dict_to_json_file(data, filename):
    """ merge a list of Python dictionaries into one dictionary
        and save the dictionary to a JSON file
        If same key exists in data(dicts) which will be merged,
        the key will be overridden.

        Args:
            data (`list`): list of dictionaries
            filename (`string`): filename to save
        Raise:
            Exception
        Returns:
            output (`dict`): Python dictionary

        Example:

        >>> dev.api.save_dict_to_file(data=[dict1, dict2], 'merged_dict')
        {
            'a': {        # came from `dict1`
                'b': 1,
            },
            'c': {        # came from `dict2`
                'd': 2,
            }
        }

    """
    if isinstance(data, list):
        output = {}
        for dict_ in data:
            if isinstance(dict_, dict):
                output.update(dict_)
            else:
                raise Exception(
                    '{dict_} is not dictionary.'.format(dict_=dict_))
        with open(filename, 'w+') as f:
            f.write(json.dumps(output))
    else:
        raise Exception('`data` {data} is not list.'.format(data=data))

    return output


def load_dict_from_json_file(filename):
    """ load python dictionary from a JSON file
        Args:
            filename (`string`): JSON file name
        Raise:
            Exception
        Returns:
            output (`dict`): Python dictionary

        Example:

        >>> dev.api.load_dict_from_json_file('merged_dict')
        {
            'a': {
                'b': 1,
            },
            'c': {
                'd': 2,
            }
        }

    """
    with open(filename, 'r') as f:
        output = json.loads(f.read())

    return output


def verify_pcap_packet(pcap_location,
                       expected_src_address=None,
                       expected_dst_address=None,
                       expected_protocol=None,
                       expected_dst_port_number=None,
                       expected_tos=None,
                       expected_src_port_number=None,
                       expected_traffic_class=None,
                       expected_fragment_flag=None,
                       check_all=False):
    """ Verify pcap mpls packets values

    Args:
        pcap_location (obj): PCAP file location
        expected_src_address (str): Source IP address to search for
        expected_dst_address (str): Destination IP address to search for
        expected_protocol (str): Expected protocol in packet
        expected_dst_port_number (int): Expected destination port number
        expected_src_port_number (int): Expected source port number
        expected_tos (int): Expected type of service(tos) value
        expected_traffic_class (str): Expected traffic class
        expected_fragment_flag (bool): Expected Fragment flag
        check_all (bool): Check all matching packets

    Returns:
        bool: True or False
    """

    try:
        from scapy.contrib.mpls import MPLS
        from scapy.all import rdpcap, IP, load_contrib, IPv6, TCP, UDP
        load_contrib("mpls")
    except ImportError:
        raise ImportError(
            'scapy is not installed, please install it by running: '
            'pip install scapy') from None

    pcap_object = rdpcap(pcap_location)

    for packet in pcap_object:
        if IP in packet or IPv6 in packet:
            #To check the packet is IPv4 or Ipv6
            ip_packet = packet.getlayer(
                IP) if IP in packet else packet.getlayer(IPv6)

            #To check the expected destination address
            if expected_dst_address:
                dst = ip_packet.dst
                if dst != expected_dst_address:
                    continue

            # To check the expected source address
            if expected_src_address:
                src = ip_packet.src
                if src != expected_src_address:
                    continue

            #Type of Service
            if expected_tos is not None:
                if getattr(ip_packet, "tos", None):
                    ip_tos = ip_packet.tos
                    if not bin(ip_tos).startswith(bin(expected_tos)):
                        if check_all:
                            return False
                        continue
                else:
                    continue

            #To check the expected protocols eg: tcp, udp
            if expected_protocol and expected_protocol.lower(
            ) == 'tcp' and TCP not in packet:
                continue

            if expected_protocol and expected_protocol.lower(
            ) == 'udp' and UDP not in packet:
                continue

            #To check the destination port. Here "continue" helps in checking all the packets with
            #destination port, If port is matched it returns True at the end of loop. If none of the
            #port matches, it goes out of loop and return False at the end of api.
            if expected_dst_port_number:
                if getattr(packet, "dport", None):
                    if expected_dst_port_number != packet.dport:
                        continue
                else:
                    continue

            #To check the source port
            if expected_src_port_number:
                if getattr(packet, "sport", None):
                    if expected_src_port_number != packet.sport:
                        continue
                else:
                    continue

            #To check the Traffic class for IPv6
            if expected_traffic_class is not None:
                if IPv6 in packet and ip_packet.tc != expected_traffic_class:
                    continue

            #To check the fragmented packet
            if expected_fragment_flag is not None:
                if IP in packet:
                    #For fragment packet
                    # The More Fragments(MF) flag should be non zero.
                    if str(ip_packet.flags
                           ) != "MF" and ip_packet.flags.value == 0:
                        continue

                if IPv6 in packet:
                    #Here 44 denotes the IPv6 Fragment extension header
                    #https://www.iana.org/assignments/ipv6-parameters/ipv6-parameters.xhtml
                    next_header = ip_packet.fields.get('nh', None)
                    if next_header != 44:
                        continue
                log.info(f'The fragmented packet is {ip_packet.fields}')
            return True

    return False


def verify_login_with_credentials(device,
                                  hostname,
                                  username,
                                  password,
                                  start_cmd,
                                  learn_hostname=False,
                                  proxy_connections=None,
                                  invert=False):
    """
        Verify device is logged in with correct credentials and
        can not be logged in with wrong credentials when start command is given.

        Args:
            device('obj'): device to use
            hostname('str') : hostname
            username('str') : username
            password('str'): password
            start_cmd('list'): list of commands to execute
            learn_hostname('bool', optional): learn hostname. Default to False.
            proxy_connections('str', optional): proxy_connections. Default to None.
            invert ('bool', optional): True if device can't be logged in with wrong credentials. Default to False.

        Returns:
            Boolean
        Raises:
            N/A
    """

    op = operator.eq if not invert else operator.ne

    try:
        terminal = Connection(hostname=hostname,
                              learn_hostname=learn_hostname,
                              start=start_cmd,
                              credentials={
                                  'default': {
                                      'username': username,
                                      'password': password
                                  }
                              },
                              os=device.os,
                              timeout=300,
                              prompt_recovery=True,
                              proxy_connections=proxy_connections)
        terminal.connect()
    except Exception as ex:
        log.warning(
            f"Executing {start_cmd} with {username}(username) and {password}(password) "
            f"failed with error {ex}")

    return op(terminal.connected, True)


def get_connection(device,
                   hostname,
                   username,
                   password,
                   start_cmd,
                   learn_hostname=False,
                   proxy_connections=None):
    """
        Get connection object.

        Args:
            device('obj'): device to use
            hostname('str') : hostname
            username('str') : username
            password('str'): password
            start_cmd('list'): list of commands to execute
            learn_hostname('bool', optional): learn hostname. Default to False.
            proxy_connections('str', optional): proxy_connections. Default to None.

        Returns:
            Connection object
        Raises:
            N/A
    """

    try:
        terminal = Connection(hostname=hostname,
                              learn_hostname=learn_hostname,
                              start=start_cmd,
                              credentials={
                                  'default': {
                                      'username': username,
                                      'password': password
                                  }
                              },
                              os=device.os,
                              timeout=300,
                              prompt_recovery=True,
                              proxy_connections=proxy_connections)
    except Exception as ex:
        log.warning(
            f"Get connection object for {start_cmd} with {username}(username) and {password}(password) "
            f"failed with error {ex}")

    return terminal


def get_devices(testbed,
                os=None,
                regex=None,
                regex_key='os',
                pick_type='all',
                only_connected=False,
                with_os=False):
    """ Get devices from testbed object
        Args:
            testbed (`obj`): testbed object
            os (`str`): specify os to choose. Defaults to None
            regex (`str`): regex to chose devices based against regex_key
                           Defaults to None
            regex_key (`str`): specify key in testbed yaml where use regex
                               default to `os`
            pick_type (`str`) : specify how to pick up
                                default to `all`
                                choices:
                                  `all`: pick up all devices
                                         return device names as list
                                  `first_one`: pick up first one device
                                               return device name as string
                                  `random_one`: pick up one device randomly
                                                return device name as string
                                  `random_order`: randomize order of devices
                                                  return device names as list
            only_connected (`bool`) : check if device is connected and return 
                                      only connected ones. Default to False
            with_os (`bool`): return dict with device name and os as key/value pair
                              Defaults to False

        Raise:
            Exception
        Returns:
            picked_devices (`list` or `str`, or dict): list of device names
                                              device name as string in case of
                                              `first_one` or `random_one`
                                              if with_os is True, will return dict with os
                                              ex.)
                                              {
                                                  'R1_xe': 'iosxe',
                                                  'R2_xr': 'iosxr',
                                              }

        Example:

        >>> dev.api.get_devices(testbed)
        ['terminal_server',
         'internet-rtr01',
         'internet-host01',
         'edge-firewall01',
         'core-rtr01',
         'core-rtr02',
         'dist-rtr01',
         'dist-rtr02',
         'dist-sw01',
         'dist-sw02',
         'inside-host01',
         'edge-sw01',
         'inside-host02']

        >>> dev.api.get_devices(testbed, os='iosxe')
        ['internet-rtr01', 'dist-rtr01', 'dist-rtr02']

        >>> dev.api.get_devices(testbed, regex='iosxe')
        ['internet-rtr01', 'dist-rtr01', 'dist-rtr02']

        >>> dev.api.get_devices(testbed, regex='ios.*')
        ['internet-rtr01',
         'core-rtr01',
         'core-rtr02',
         'dist-rtr01',
         'dist-rtr02',
         'edge-sw01']

        >>> dev.api.get_devices(testbed, regex='iosxrv', regex_key='series')
        ['core-rtr01', 'core-rtr02']

        >>> dev.api.get_devices(testbed, os='iosxe', regex='.*n0.*', regex_key='command')
        ['internet-rtr01']

        >>> dev.api.get_devices(testbed, pick_type='first_one')
        'terminal_server'

        >>> dev.api.get_devices(testbed, os='nxos', pick_type='random_one')
        'dist-sw02'

        >>> dev.api.get_devices(testbed, os='iosxe', pick_type='random_order')
        ['internet-rtr01', 'dist-rtr01', 'dist-rtr02']

    """
    def _create_dict_with_os(testbed, picked_devices):
        dev_dict = {}
        for dev in picked_devices:
            os = Dq(testbed.raw_config).contains_key_value('devices',
                                                           dev).get_values(
                                                               'os', 0)
            dev_dict.update({dev: os})
        return dev_dict

    picked_devices = None
    if os:
        if regex and regex_key:
            picked_devices = Dq(testbed.raw_config).contains(
                os, level=-1).contains_key_value(
                    regex_key, regex, value_regex=True).get_values('devices')
        else:
            picked_devices = Dq(testbed.raw_config).contains_key_value(
                'os', os).get_values('devices')
    else:
        if regex and regex_key:
            picked_devices = Dq(testbed.raw_config).contains_key_value(
                regex_key, regex, value_regex=True).get_values('devices')
        else:
            picked_devices = Dq(testbed.raw_config).get_values('devices')

    # check if device is connected or not from picked_devices
    if only_connected:
        connected_devices = [
            dev for dev in picked_devices if testbed.devices[dev].connected
        ]
        # overwrite picked_devices by connected_devices
        picked_devices = connected_devices

    if picked_devices:
        if pick_type == 'first_one':
            return picked_devices[0]
        elif pick_type == 'random_one':
            return random.choice(picked_devices)
        elif pick_type == 'random_order':
            random.shuffle(picked_devices)
            if with_os:
                picked_devices = _create_dict_with_os(testbed, picked_devices)
            return picked_devices
        else:
            if with_os:
                picked_devices = _create_dict_with_os(testbed, picked_devices)
            return picked_devices
    else:
        if hasattr(runtime, 'testbed') and runtime.testbed != testbed:
            log.warning('testbed object is not same with runtime.testbed. Please make sure device is connected via runtime.testbed for easypy plugins.')
        if only_connected:
            raise Exception("Couldn't find any connected device from testbed object.")
        else:
            raise Exception("Couldn't find any device from testbed object.")


def get_interface_from_yaml(local, remote, value, testbed_topology, **kwargs):
    """ Get interface name from the testbed yaml file

        To be used within datafile

        Args:
            local (`str`): local device to get interface from
            remote (`str`): Remote device where the interface is connected to
            value (`str`): Either link name or a number and a link will be randomly chosen
            testbed_topology (`dict`): `testbed.topology` or `testbed`

        Raise:
            Exception
        Returns:
            Interface name

        Example:

            interface: "%CALLABLE{genie.libs.sdk.apis.utils.get_interface_from_yaml(uut,helper,0,%{testbed.topology})}"

            interface: "%CALLABLE{genie.libs.sdk.apis.utils.get_interface_from_yaml(uut,helper,r1_r4_1,%{testbed.topology})}"

            interface: "%CALLABLE{genie.libs.sdk.apis.utils.get_interface_from_yaml(alias,helper,0,%{testbed})}"
    """
    # Put it back as a dictionary

    if not isinstance(testbed_topology, dict):
        topology = ast.literal_eval(','.join(testbed_topology).lstrip())
    else:
        topology = testbed_topology
    data = Dq(topology)

    # Get all the links for local
    local_links = data.contains(local.strip()).get_values('link')
    if not local_links:
        local = data.contains(local.strip()).contains('devices')[0].path[1]
        local_links = data.contains(local.strip()).get_values('link')
    # Get all the links for remote
    remote_links = data.contains(remote.strip()).get_values('link')
    if not remote_links:
        remote = data.contains(remote.strip()).contains('devices')[0].path[1]
        remote_links = data.contains(remote.strip()).get_values('link')
    # Now find the one connected to the remote
    common_links = sorted(set(local_links).intersection(set(remote_links)))
    # if value is an int
    if isinstance(value, int) or value.isnumeric():
        try:
            value = common_links[int(value)]
        except Exception as e:
            raise Exception("Link '{n}' between '{l}' and "
                            "'{r}' does not exists; there is only '{m}' links "
                            "between them".format(n=value,
                                                  l=local,
                                                  r=remote,
                                                  m=len(common_links)))

    # Get interface related to it
    interface = data.contains(value).contains(local.strip()).get_values(
        'interfaces', 0)
    if isinstance(interface, list):
        raise Exception(
            "Could not find an interface for device '{d}'".format(d=local))
    return interface


def get_interface_type_from_yaml(local, remote, value, testbed_topology, **kwargs):
    """ Get interface type from the testbed yaml file

        To be used within datafile

        Args:
            local (`str`): local device to get interface from
            remote (`str`): Remote device where the interface is connected to
            value (`str`): Either link name or a number and a link will be randomly chosen
            testbed_topology (`dict`): `testbed.topology` or `testbed`

        Raise:
            N/A
        Returns:
            Interface type or `None` if not found

        Example:

            interface_type: "%CALLABLE{genie.libs.sdk.apis.utils.get_interface_type_from_yaml(uut,helper,0,%{testbed.topology})}"

            interface_type: "%CALLABLE{genie.libs.sdk.apis.utils.get_interface_type_from_yaml(uut,helper,r1_r4_1,%{testbed.topology})}"

            interface_type: "%CALLABLE{genie.libs.sdk.apis.utils.get_interface_type_from_yaml(alias,helper,0,%{testbed})}"
    """
    if not isinstance(testbed_topology, dict):
        topology = ast.literal_eval(','.join(testbed_topology).lstrip())
    else:
        topology = testbed_topology
    data = Dq(topology)

    # Get type related to the interface
    interface = get_interface_from_yaml(local, remote, value, testbed_topology)
    type = data.contains(interface).contains(local.strip()).get_values('type', 0)
    if isinstance(type, list):
        log.error("Could not find a type for device '{d}' interface '{i}'"
                  .format(d=local, i=interface))
        # Empty list is given if the type is not found. Return `None` instead.
        return None
    return type


def get_device_connections_info(device):
    """ Get connection information of a device from testbed file.
            Args:
                device (`obj`): device object
            Returns:
                device.connections (`dict`)
    """

    return device.connections


def get_running_config_all(device):
    """ Return raw running configuration

        Args:
            device ('obj')  : Device object to extract configuration
        Returns:
            Raw output
    """
    if device.os == 'junos':
        return device.execute("show configuration")

    try:
        return device.execute("show running-config all")
    except Exception:
        pass
    log.info("Device doesn't have 'show running-config all'...")
    return device.execute("show running-config")


def verify_pcap_as_path(
    pcap_location,
    layer,
    expected_as_path,
):
    """ Verify pcap AS path values
    Args:
        pcap_location (obj): PCAP file location
        layer (str): Given target route address
        expected_as_path (str): Expected AS path value

    Returns:
        bool: True of False
    """

    try:
        from scapy.all import rdpcap, IP, IPv6
        from scapy.contrib.bgp import BGPPathAttr, BGP
    except ImportError:
        log.info('scapy is not installed, please install it by running: '
                 'pip install scapy')
        return False

    pcap_packets = rdpcap(pcap_location)

    for i in range(len(pcap_packets)):
        packet = pcap_packets[i]

        # Determine IPv4 or IPv6
        if ':' in layer:
            try:
                packet_26 = IPv6(packet.load[26:])
                log.info(
                    f"IPv6(packet.load[26:]) is \n {packet_26.show()}\n\n")
                try:
                    packet_36 = IPv6(packet.load[36:])
                    log.info(
                        f"IPv6(packet.load[36:]) is \n {packet_36.show()}\n\n")
                except Exception:
                    continue
            except IndexError:
                log.info('Failed to load packets in IndexError')
                continue
        else:
            packet_26 = IP(packet.load[26:])
            packet_36 = IP(packet.load[36:])

            log.info(f"IP(packet.load[26:]) is \n {packet_26.show()}\n\n")
            log.info(f"IP(packet.load[36:]) is \n {packet_36.show()}\n\n")

        if BGPPathAttr in packet_26 or BGPPathAttr in packet_36:

            # ###[ UPDATE ]###
            #    withdrawn_routes_len= 0
            #    \withdrawn_routes\
            #    ...
            #    \nlri      \
            #     |###[ IPv4 NLRI ]###
            #     |  prefix    = 123.123.123.0/32 <------------
            try:
                # IPv6:
                # (Pdb) IPv6(pcap_packets[54].load[36:]).path_attr[-1].attribute.nlri[0].prefix
                # '2001:123::/64'
                if ':' in layer:

                    path_attr_lists_26 = packet_26.path_attr
                    for path_attr_item in path_attr_lists_26:
                        try:
                            if path_attr_item.attribute.nlri[
                                    0].prefix == layer:
                                if (expected_as_path).to_bytes(
                                        4, byteorder='big'
                                ) in pcap_packets[i].load:
                                    return True
                        except AttributeError:
                            continue

                    path_attr_lists_36 = packet_36.path_attr
                    for path_attr_item in path_attr_lists_36:
                        try:
                            if path_attr_item.attribute.nlri[
                                    0].prefix == layer:
                                if (expected_as_path).to_bytes(
                                        4, byteorder='big'
                                ) in pcap_packets[i].load:
                                    return True
                        except AttributeError:
                            continue
                # IPv4
                else:
                    if packet_26.nlri[0].prefix or packet_36.nlri[0].prefix:
                        if packet_26.nlri[0].prefix == layer or packet_36.nlri[
                                0].prefix == layer:
                            if (expected_as_path).to_bytes(
                                    4,
                                    byteorder='big') in pcap_packets[i].load:
                                return True

            except AttributeError:
                continue

    return False


def verify_pcap_capability(
    pcap_location,
    source,
    destination,
    expected_capability,
):
    """ Verify pcap AS path values
    Args:
        pcap_location (obj): PCAP file location
        source (str): Source address
        destination (str): Destination address
        expected_capability (str or int): Expected capability in string or integer

    Returns:
        bool: True of False
    """
    # verify code or name
    # reference: https://www.iana.org/assignments/capability-codes/capability-codes.xhtml
    capabilities_dict = {
        '0':
        'Reserved',
        '1':
        'Multiprotocol Extensions for BGP-4',
        '10-63':
        'Unassigned',
        '128':
        'Prestandard Route Refresh (deprecated)',
        '129':
        'Prestandard Outbound Route Filtering (deprecated), prestandard '
        'Routing Policy Distribution (deprecated)',
        '130':
        'Prestandard Outbound Route Filtering (deprecated)',
        '131':
        'Prestandard Multisession (deprecated)',
        '132-183':
        'Unassigned',
        '184':
        'Prestandard FQDN (deprecated)',
        '185':
        'Prestandard OPERATIONAL message (deprecated)',
        '186-238':
        'Unassigned',
        '2':
        'Route Refresh Capability for BGP-4',
        '239-254':
        'Reserved for Experimental Use',
        '255':
        'Reserved',
        '3':
        'Outbound Route Filtering Capability',
        '4':
        'Multiple routes to a destination capability (deprecated)',
        '5':
        'Extended Next Hop Encoding',
        '6':
        'BGP Extended Message',
        '64':
        'Graceful Restart Capability',
        '65':
        'Support for 4-octet AS number capability',
        '66':
        'Deprecated (2003-03-06)',
        '67':
        'Support for Dynamic Capability (capability specific)',
        '68':
        'Multisession BGP Capability',
        '69':
        'ADD-PATH Capability',
        '7':
        'BGPsec Capability',
        '70':
        'Enhanced Route Refresh Capability',
        '71':
        'Long-Lived Graceful Restart (LLGR) Capability',
        '72':
        'Routing Policy Distribution',
        '73':
        'FQDN Capability',
        '74-127':
        'Unassigned',
        '8':
        'Multiple Labels Capability',
        '9':
        'BGP Role (TEMPORARY - registered 2018-03-29, extension registered '
        '2020-03-20, expires 2021-03-29)'
    }

    try:
        from scapy.all import rdpcap, IP, IPv6
        from scapy.contrib.bgp import BGPPathAttr, BGP
    except ImportError:
        log.info('scapy is not installed, please install it by running: '
                 'pip install scapy')
        return False

    # read pcap file
    pcap_packets = rdpcap(pcap_location)

    for packet in pcap_packets:

        #    ###[ OPEN ]###
        #    version   = 4
        #    my_as     = 1
        #    hold_time = 90
        #    bgp_id    = 1.1.1.1
        #    opt_param_len= 30
        #    \opt_params\
        #     |###[ Optional parameter ]###
        #         |  param_type= Capabilities
        #         |  param_length= 6
        #         |  \param_value\
        #         |   |###[ Support for 4-octet AS number capability ]###
        #         |   |  code      = Support for 4-octet AS number capability
        #         |   |  length    = 4
        #         |   |  asn       = 1

        if ':' in source:
            try:
                packet_26 = IPv6(packet.load[26:])
                log.info(
                    f"IPv6(packet.load[26:]) is \n {packet_26.show()}\n\n")
                try:
                    packet_36 = IPv6(packet.load[36:])
                    log.info(
                        f"IPv6(packet.load[36:]) is \n {packet_36.show()}\n\n")
                except Exception:
                    continue
            except IndexError:
                continue
        else:
            packet_26 = IP(packet.load[26:])
            packet_36 = IP(packet.load[36:])

            log.info(f"IP(packet.load[26:]) is \n {packet_26.show()}\n\n")
            log.info(f"IP(packet.load[36:]) is \n {packet_36.show()}\n\n")

        try:
            # IPv6
            # (Pdb) IPv6(pcap_packets[449].load[36:]).show()
            if ':' in source:
                opt_params_lst = packet_26[IPv6].opt_params or packet_36[
                    IPv6].opt_params

            # IPv4:
            else:
                opt_params_lst = packet_26[IP].opt_params or packet_36[
                    IP].opt_params

            for opt_param in opt_params_lst:

                # Given capability code, find its context
                if type(expected_capability) == int:
                    expected_capability = capabilities_dict[str(
                        expected_capability)]

                # packet_26[IP].opt_params[0].param_value.name
                # -> 'Multiprotocol Extensions for BGP-4'
                if opt_param.param_value.name == expected_capability:
                    return True

        except AttributeError:
            continue

    return False


def get_connected_alias(device):
    """ Get connected alias from device object

        Args:
            device ('obj')  : Device object
        Returns:
            aliases (`dict`) : dict with alias key with value
                               which contains all related info
                               for the connection
    """
    aliases = {}
    connections = device.connectionmgr.connections

    for alias in connections.keys():
        aliases.setdefault(alias, connections[alias].__dict__)
    return aliases


def verify_keywords_in_output(device,
                              keywords,
                              output,
                              max_time=60,
                              check_interval=10,
                              invert=False):
    """
    Verify if keywords are in output

    Args:
        device(`obj`): device to use
        max_time (`int`): Maximum time to keep checking. Default to 60 secs
        check_interval (`int`): How often to check. Default to 10 secs
        keywords (`list`, `str`): list of keywords to find
        output (`str`): output of show command.
        invert (`bool`): invert result. (check all keywords not in log)
                         Default to False

    Returns:
        Boolean : if True, find the keywords in log
    Raises:
        N/A
    """

    if not isinstance(keywords, list):
        keywords = [str(keywords)]

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():

        # dictionary of information what found with keyword
        # {
        #     <keyword>: <the line where the keyword found>
        #}
        found = {}
        for line in output.splitlines():
            line = line.strip()
            for kw in keywords:
                if kw in line or re.match(kw, line):
                    found[kw] = line

        if not invert and len(found) == len(keywords) or invert and not found:
            return True
        elif not invert:
            timeout.sleep()
        else:
            # in case of revert=True, no need to retry
            return False

    return False


def get_structure_output(device,
                         command=None,
                         exclude=['!'],
                         negative_keyword='no',
                         output=None):
    """
    Get structure output from any test data. Data will be divided by space
    and generate structure data.

    Args:
        device (`obj`): device to use
        command (`str`): show command. Default to None
        exclude (`list`): patter to excute in text output
                          Default to ['!']
        negative_keyword (`str`): keyword to set value as False
                                  Default to 'no'
        output (`str`): text output

    Returns:
        Dict : structure data (python dictionary)
    Raises:
        N/A
    """

    if not output and not command:
        log.warn('output or/and command were not provided.')
        return {}

    base = []
    ld = ListDict()
    priv_line = ''
    priv_orig_line = ''
    priv_line_list = []

    if not output and command:
        output = device.execute(command)

    def _check_output(line, priv_orig_line, priv_line, config_flag, base):
        line_space = re.search(r'^\s+', line)
        if line_space:
            start, end = line_space.span()
            line_space = end
        else:
            line_space = 0
        priv_orig_line_space = re.search(r'^\s+', priv_orig_line)
        if priv_orig_line_space:
            start, end = priv_orig_line_space.span()
            priv_orig_line_space = end
        else:
            priv_orig_line_space = 0
        # check if same level(indentation)
        if line_space == priv_orig_line_space:
            # check if no indentation
            # (=global configuration)
            if line.split(' ').count('') == 0:
                base = []
            priv_line_list = priv_orig_line.strip().split(' ')
            # check if negative_keyword(default `no`) in output line
            # (mainly for iosxe/nxos)
            if priv_line.strip().split(' ')[0] == negative_keyword:
                priv_line_list = priv_line.strip().split(' ')
                priv_line_list.pop(0)
                priv_line = ' '.join(priv_line_list)
                config_flag = False
            # add base to priv_line_list. and then have complete priv_line
            # without config_flag
            if priv_orig_line_space != 0:
                priv_line = ' '.join(base) + ' ' + ' '.join(priv_line_list)
            priv_line_list = priv_line.split(' ')
            # if not only spaces, add priv_line_list to ld(ListDict)
            if priv_line.replace(' ', ''):
                ld.append(((tuple(priv_line_list)), config_flag))
                log.debug('append_ld_path: {}'.format(priv_line_list))
        else:
            # check if line is more deeper indentation comparing to priv_line
            # ex.)
            # interface GigabitEthernet1 # priv_line
            #   ip address 10.1.1.1      # line
            if line.split(' ').count('') > priv_line.split(' ').count(
                    '') and line.split(' ').count('') != len(base):
                base.append(priv_line.strip())
                priv_line = line
                priv_orig_line = orig_line
            # check if line is less deeper indentation comparing to priv_line
            # ex.)
            # interface GigabitEthernet1
            #   ip address 10.1.1.1      # priv_line
            # end                        # line
            if (line.split(' ').count('') < priv_line.split(' ').count('')
                    and priv_line != ''):
                diff_count = priv_line.split(' ').count('') - line.split(
                    ' ').count('')
                # check if line of indentation is not same with base
                if line.split(' ').count('') != len(base):
                    priv_line_list = priv_orig_line.strip().split(' ')
                    if priv_line.strip().split(' ')[0] == negative_keyword:
                        priv_line_list = re.sub(r'\s+', ' ',
                                                priv_line.strip()).split(' ')
                        priv_line_list.pop(0)
                        config_flag = False
                    # to add LD, add base
                    priv_line = ' '.join(base) + ' ' + ' '.join(priv_line_list)
                    priv_line_list = re.sub(r'\s+', ' ', priv_line).split(' ')
                    if priv_line.replace(' ', ''):
                        ld.append(((tuple(priv_line_list)), config_flag))
                        log.debug('append_ld_path: {}'.format(priv_line_list))
                    log.debug('diff_count: {}'.format(diff_count))
                    for _ in range(diff_count):
                        try:
                            base.pop()
                        except IndexError:
                            break
            line_list = line.split(' ')
            # check if negative_keyword(default `no`) in line
            if negative_keyword in line_list:
                line_list.remove(negative_keyword)
                config_flag = False
                line = ' '.join(line_list)
            if line not in base:
                line = ' '.join(base) + line
        line_list = line.split(' ')
        priv_line = line
        priv_orig_line = orig_line
        return priv_orig_line, priv_line, config_flag, base

    output = output.splitlines()

    while output:
        line = output.pop(0)
        line = line.rstrip()
        line = re.sub(r'\s+', ' ', line)
        # debug messages
        log.debug('-' * 50)
        log.debug('line: {}'.format(line))
        log.debug('base: {}'.format(base))
        log.debug('priv_line: {}'.format(priv_line))
        log.debug('priv_line_list: {}'.format(priv_line_list))
        orig_line = line
        # ignore empty line
        if not line or line.strip() in exclude:
            continue
        config_flag = True
        # check if global config
        priv_orig_line, priv_line, config_flag, base = _check_output(
            line, priv_orig_line, priv_line, config_flag, base)

    # handle last one
    config_flag = True
    # check if global config
    _check_output(line, priv_orig_line, priv_line, config_flag, base)

    # remove items which should be ignored because ignored ones prevent to build
    # dictionary

    # need sorting to check from longer ones to shorter ones
    ld.sort(reverse=True)
    # final config parse result
    ld_final = ListDict()
    # ignored items
    ld_final_ignored = ListDict()
    ld_final_paths = []
    match_flag = False
    for item in ld:
        if not ld_final_paths:
            ld_final_paths.append(item.path)
            ld_final.append(((tuple(item.path)), item.value))
            continue
        match_flag = False
        for each_final_path in ld_final_paths:
            # check shorter DictItem exists in longer DictItem
            # and move matched item to ld_final_ignored list
            if set(item.path) == (set(item.path) & set(each_final_path)):
                match_flag = True
                ld_final_ignored.append(((tuple(item.path)), item.value))
        # if item is unique and longer than other items, added to ld_final list
        if not match_flag:
            ld_final_paths.append(item.path)
            ld_final.append(((tuple(item.path)), item.value))

    log.debug(json.dumps(ld_final.reconstruct(), indent=2, sort_keys=True))
    if ld_final_ignored:
        log.debug('below DictItem are ignored:')
        for item in set(ld_final_ignored):
            log.debug(item)

    return ld_final.reconstruct()


def arithmetic_operations(operation=None, operands=None):
    """
    Perform arithmetic operations on operands.

    Args:
        operation (`str`): string indicating the calculation method.
                           'addition' is '+'
                           'subtraction' is '-'
                           'multiplication' is '*'
                           'division' is '/'
        operands (`list`): operands to be calculated.
                           example: [1, 2]

    Returns:
        Numerical : Calculation result
        None      : When an abnormality occurs during calculation
    Raises:
        N/A
    """
    # debug
    log.debug("operation: {}".format(operation))
    log.debug("operands: {}".format(operands))

    # Initialize
    result = None

    try:
        # check operands list
        if operands is None:
            log.error("'operands' is not set.")
            log.error("Please check 'operands' argument.")
            result = None
            return result

        if len(operands) != 2:
            log.error("Invalid argument: {}".format(operands))
            log.error("Please check 'operands' argument.")
            result = None
            return result

        # calculation
        if operation == '+':
            # addition
            result = operands[0] + operands[1]
        elif operation == '-':
            # subtraction
            result = operands[0] - operands[1]
        elif operation == '*':
            # multiplication
            result = operands[0] * operands[1]
        elif operation == '/':
            # division
            result = operands[0] / operands[1]
        else:
            log.error("Invalid argument: {}".format(operation))
            log.error("Please check 'operation' argument.")
            result = None

    except (ValueError, ZeroDivisionError, TypeError, IndexError) as e:
        # Calculation error
        log.error("Calculation error has occurred : {}".format(e))
        log.error("Please check 'operation' and 'operands' arguments.")
        result = None
    except Exception as e:
        # Unexpected error
        log.error("Unexpected error has occurred : {}".format(e))
        result = None
    finally:
        log.debug("Calculation result: {}".format(result))
        return result


def get_single_interface(device, link_name=None, opposite=False, phy=False):
    """"
    Returns the single interface and fails if multiple interfaces
    are found.

    Args:
        device (`obj`): device to use
        link_name ('str'): link name
        opposite ('bool'): find opposite device interface
        phy ('bool'): find only physical interface

    Raise:
        N/A

    Return:
        Interface Object
    """

    interface = device.api.get_interfaces(link_name=link_name,
                                          opposite=opposite,
                                          phy=phy)

    if interface == None:
        log.warning(
            "found no interface found on device {} with link {}".format(
                device.name, link_name))
        return None

    if len(interface) != 1:
        log.warning("{} interfaces on {} with link {} but expected 1".format(
            len(interface), device.name, link_name))
        return None

    interface = interface[0]

    try:
        interface_name = interface.name
    except AttributeError:
        log.error('Interface object does not have attribute "name"')
        return None

    log.info("found the interface {}".format(interface_name))

    return interface_name


def get_local_ip(device, alias=None):
    ''' Get the local IP address that is used to connect to devices.

    Looks up the IP address via the spawn process ID.

    Args:
        device (Device): device object
        alias (str): alias name of the connection

    Returns:
        IP address (str)
    '''
    if alias:
        conn = getattr(device, alias)
    else:
        conn = device
    p = psutil.Process(conn.spawn.pid)
    conns = p.connections()
    if conns:
        conn = conns[0]
        local_ip = conn.laddr[0]
        log.info('Local IP: {}'.format(local_ip))
        return local_ip


def get_bool(value=None):
    ''' Get boolean result against given value

        Use-case:
        %CALLABLE Markup doesn't support built-in function bool().
        This API can be used when you want to get boolean result via %CALLABLE
        or can directly calling this API with value in Blitz YAML or etc

    Args:
        device (Device): device object
        value (`any`): any such as string, integer, list, dict etc.

    Returns:
        Bool: True or False
    '''
    return bool(value)


def get_testcase_name(runtime=runtime, escape_regex_chars=False):
    ''' Get testcase name from runtime

    Args:
        runtime (`obj`, optional): easypy runtime object
        escape_regex_chars (`bool`): escapre regex special chars. Default to False

    Returns:
        str: testcase name
    '''
    try:
        testcase_name = runtime.reporter.client.get_section(
        )['idlist'][1].split('.')[0]
    except Exception:
        testcase_name = ''
        log.error("Couldn't get testcase name from easypy runtime object.")

    if escape_regex_chars:
        return re.escape(testcase_name)

    return testcase_name

def get_list_length(target_list):
    """"
    Returns length of target_list.

    Args:
        target_list (`list`): target list

    Raise:
        N/A

    Return:
        length of target list(int)
    """

    if type(target_list) != list:
        log.error("{} is not list".format(target_list))
        return None

    try:
        list_length = len(target_list)
    except AttributeError:
        log.error("cannot get length of {}".format(target_list))
        return None

    log.info("lentgh of {} is {}".format(target_list, list_length))

    return list_length


def web_interaction(subject, message, section_name, **kwargs):
    """
    Returns result of user choice after changes in physical world.

    Use-case:

    There are rare cases when a result must be manually determined by a human.
    Such as a test that relies upon changes that happen in the physical world.
    For these cases this utility that allows a user to decide the result.

    This api web_interaction can pause test execution and notify a user via email
    that input is required. This email has a link to a webpage hosted by WebInteraction
    that has a form for the user to submit to give a result.

    Args:
        subject (str) : A brief description of the interaction.
        message (str) : This is the message that describes to the
                        user what the test is and how they determine
                        the result.
        section_name (ref) : Reference to section or step that called interaction.
                        This provides the name of the test to the user,
                        as well as the APIs to return a test result.

        [optional args]
        from_address(str): The email address that the notification will be sent from.
                           Defaults to the user login.
        to_address(str): The email address that the notification will be sent to.
                         Defaults to the user login.

    Returns:
        result (str)
        Eg. aborted, blocked, errored, failed, passed, passx, skipped

    Note:
        You can apply additional arguments to webinteraction api.
        List of arguments for the api can be found at the link below:
        https://pubhub.devnetcloud.com/media/pyats/docs/aetest/results.html?highlight=webinteraction#interaction-results
        In this api, section_name is equal to section in the above docs.

    Blitz example:

        - api:
              function: web_interaction
              common_api: True
              alias: To wait, till manual work is done.
              arguments:
                subject: "Testing web interaction api"
                message: "Message for the user about how to assess this test"
                section_name: "%VARIABLES{section}"  #section ref can be passed like this.
                from_address: "example@cisco.com"
              result_status: "passx"
              include:
                  - "passx"
    """

    #To get the WebInteraction object
    web_int = WebInteraction(subject=subject,
                             message=message,
                             section=section_name,
                             **kwargs)

    # Set up any prerequisites for the interaction loop
    web_int._setup_interact()

    if not web_int.email_disabled:
        # Send an email notification
        web_int._send_email()

    # Instantiate empty results from interaction
    results = None

    # Calculate timeout target
    timeout_target = time.time() + web_int.timeout

    while not results:
        # Attempt to get results from interaction
        results = web_int._check_interact()

        # Check if timeout has passed. If timeout is 'inf', this will always
        # return false
        if time.time() > timeout_target:
            break

    #When Timelimit is exceeded the result is set to blocked.
    if web_int.timeout and results is None:
        results = {'choice': 'blocked'}
        log.warning('The time limit {} exceeded for the '
                    'web_interation api '.format(web_int.timeout))

    # Teardown any allocated resources
    web_int._teardown_interact()

    return results.get('choice', None)


def verify_pcap_ldp_packet(pcap_location,
                           expected_ldp_hello=None,
                           expected_ldp_keepalive=None):
    """Verifies expected type of a packet
    Args:
        pcap_location (str): Location of pcap file
        expected_ldp_hello (bool): Expected LDPHello
        expected_ldp_keepalive (bool): Expected LDPKeepAlive
    Returns:
        bool: True or False
    """

    try:
        from scapy.all import rdpcap, IP
        from scapy.contrib.ldp import LDP, LDPKeepAlive, LDPHello
    except ImportError:
        log.warning('scapy is not installed, please install it by running: '
                    'pip install scapy')
        return False

    # To check the params are given
    if not expected_ldp_hello and not expected_ldp_keepalive:
        log.warning(
            'expected_ldp_hello or expected_ldp_keepalive must be True')
        return False

    #Load pcap file
    pcap_object = rdpcap(pcap_location)

    for packet in pcap_object:

        #Check LDP layer in packet
        if LDP in packet:
            ldp_packet = packet.getlayer(LDP)
            ip_packet = packet.getlayer(IP)

            #To check the expected LDPHello packet
            if expected_ldp_hello:
                if LDPHello not in ldp_packet:
                    continue

            #To check the expected LDPKeepAlive packet
            if expected_ldp_keepalive:
                if LDPKeepAlive not in ldp_packet:
                    continue

            log.info(f'The matched LDP packet is {ldp_packet.fields}')
            log.info(f'The IP layer of matched packet is {ip_packet.fields}')
            return True

    log.warning(
        "No matching packets found in the Pcap file {}".format(pcap_location))
    return False
