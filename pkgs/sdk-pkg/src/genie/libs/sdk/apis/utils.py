"""Utility type functions that do not fit into another category"""

# Python
import os
import logging
import re
import jinja2
import shlex, subprocess
import time
import random
from time import strptime
from datetime import datetime
from netaddr import IPAddress

# pyATS
from pyats.easypy import runtime
from pyats.utils.fileutils import FileUtils
from pyats.utils.secret_strings import to_plaintext

# Genie
from genie.utils.config import Config
from genie.utils.diff import Diff
from genie.utils.timeout import Timeout
from genie.conf.base import Device
from genie.harness._commons_internal import _error_patterns

# unicon
from unicon.eal.dialogs import Dialog, Statement
from unicon.core.errors import ConnectionError
from unicon.plugins.generic.statements import default_statement_list

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
    statements = []
    statements.append(prompt)
    statements.append(Statement(pattern=pattern))
    statements.extend(device.state_machine.default_dialog)
    statements.extend(default_statement_list)
    dialog = Dialog(statements)
    output = dialog.process(device.spawn, timeout=timeout)

    return output


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
    trim_output = trim_output[trim_output.find(cmd) :].strip()

    if not expected == trim_output:
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
    p = re.compile(
        r"^(?P<time>(\d+):(\d+):(\d+))?(?P<dh>(\d+)d(\d+)h)?"
        "(?P<wd>(\d+)w(\d)+d)?$"
    )
    m = p.match(time)
    if m:
        group = m.groupdict()
        if group["time"]:
            out = (
                int(m.group(2)) * 3600 + int(m.group(3)) * 60 + int(m.group(4))
            )
        elif group["dh"]:
            out = int(m.group(6)) * 3600 * 24 + int(m.group(7)) * 3600
        elif group["wd"]:
            out = (
                int(m.group(9)) * 3600 * 24 * 7 + int(m.group(10)) * 3600 * 24
            )
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
            "line '{}' is not in running config output".format(line)
        )

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


def copy_pcap_file(testbed, filename):
    """Copy pcap filename to runtime directory for analysis

        Args:
            testbed (`obj`): Testbed object
            filename (`str`): Pcap filename

        Returns:
            None

        Raises:
            pyATS Results
    """

    if "port" in testbed.servers["scp"]["custom"]:
        command = (
            "sshpass -p {password} scp -P {port} {user}@{add}:"
            "/{serv_loc}/{file} {loc}/{file}".format(
                password=testbed.servers["scp"]["password"],
                port=testbed.servers["scp"]["custom"]["port"],
                user=testbed.servers["scp"]["username"],
                add=testbed.servers["scp"]["address"],
                serv_loc=testbed.servers["scp"]["custom"]["loc"],
                file=filename,
                loc=runtime.directory,
            )
        )
    else:
        # In case of VIRL testbed where is no specific port
        # to connect to the server from
        command = (
            "sshpass -p {password} scp {user}@{add}:"
            "/{serv_loc}/{file} {loc}/{file}".format(
                password=testbed.servers["scp"]["password"],
                user=testbed.servers["scp"]["username"],
                add=testbed.servers["scp"]["address"],
                serv_loc=testbed.servers["scp"]["custom"]["loc"],
                file=filename,
                loc=runtime.directory,
            )
        )

    log.info(
        "Copy pcap file '{file}' to '{loc}' for packet analysis".format(
            file=filename, loc=runtime.directory
        )
    )

    args = shlex.split(command)
    try:
        p = subprocess.check_output(args)
    except Exception as e:
        log.error(e)
        raise Exception(
            "Issue while copying pcap file to runtime directory"
            " '{loc}'".format(loc=runtime.directory)
        )

    pcap = "{loc}/{file}".format(file=filename, loc=runtime.directory)

    return pcap


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

    if last % 2 == 0:
        ip_list[-1] = str(last - 1)
    else:
        ip_list[-1] = str(last + 1)

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
        if isinstance(v, dict):
            if has_configuration(v, configuration):
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
    tmpmask = ["".join(bin_arr[i * 8 : i * 8 + 8]) for i in range(4)]
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


def copy_to_server(testbed, protocol, server, local_path, remote_path,
                   timeout=300, fu_session=None, quiet=False):
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
        _copy_to_server(protocol, server, local_path, remote_path,
                        timeout=timeout, fu_session=fu_session, quiet=quiet)

    else:
        with FileUtils(testbed=testbed) as fu:
            _copy_to_server(protocol, server, local_path, remote_path,
                            timeout=timeout, fu_session=fu, quiet=quiet)

def _copy_to_server(protocol, server, local_path, remote_path, timeout=300, fu_session=None, quiet=False):
    remote = "{p}://{s}/{f}".format(p=protocol, s=server, f=remote_path)

    log.info("Copying {local_path} to {remote_path}"
             .format(local_path=local_path,
                     remote_path=remote))

    fu_session.copyfile(source=local_path, destination=remote, timeout_seconds=timeout, quiet=quiet)


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
        command = (
            "sshpass -p {svr[password]} scp -P {svr[custom][port]} "
            "{svr[username]}@{svr[address]}:"
            "/{svr[custom][loc]}/{file} {loc}/{file}".format(
                svr=testbed.servers[pro], file=filename, loc=runtime.directory
            )
        )
    else:
        # In case of VIRL testbed where is no specific port
        # to connect to the server from
        command = (
            "sshpass -p {svr[password]} scp {svr[username]}@{svr[address]}:"
            "/{svr[custom][loc]}/{file} {loc}/{file}".format(
                svr=testbed.servers[pro], file=filename, loc=runtime.directory
            )
        )

    log.info(
        "Copy {pro} file '{file}' to '{loc}' for later analysis".format(
            pro=pro, file=filename, loc=runtime.directory
        )
    )

    args = shlex.split(command)
    try:
        p = subprocess.check_output(args)
    except Exception as e:
        log.error(e)
        raise Exception(
            "Issue while copying file to runtime directory"
            " '{loc}'".format(loc=runtime.directory)
        )

    path = "{loc}/{file}".format(file=filename, loc=runtime.directory)

    return path


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
    out = template.render(
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

    return out


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
        r"\s(?P<year>\d+)"
    )

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

            return datetime(
                year, month, day, hour, minute, second, milliseconds * 1000
            )

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
        r"^(?P<original_rate>[0-9\.]+)(?P<rate_unit>[A-Za-z\%]+)?$"
    )
    m = parse.match(rate)
    if m:
        parsed_rate = m.groupdict()["original_rate"]
        try:
            original_rate = int(parsed_rate)
        except:
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
    else:
        raise Exception(
            "The provided rate is not in the correct "
            "format in the trigger data file"
        )


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

    _error_patterns(device=device)
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


def reconnect_device(device, max_time=300, interval=30, sleep_disconnect=30, via=None):
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
            _error_patterns(device=device)
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
            "Could not reconnect to device {dev}".format(dev=device.name)
        )

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
    return (str( (0xff000000 & mask) >> 24)   + '.' +
          str( (0x00ff0000 & mask) >> 16)   + '.' +
          str( (0x0000ff00 & mask) >> 8)    + '.' +
          str( (0x000000ff & mask)))

def copy_to_device(device, remote_path, local_path, server, protocol, vrf=None,
    timeout=300, compact=False, use_kstack=False, **kwargs):
    """
    Copy file from linux server to device
        Args:
            device ('Device'): Device object
            remote_path ('str'): remote file path on the server
            local_path ('str'): local file path to copy to on the device
            server ('str'): hostname or address of the server
            protocol('str'): file transfer protocol to be used
            vrf ('str'): vrf to use (optional)
            timeout('int'): timeout value in seconds, default 300
            compact('bool'): compress image option for n9k, defaults False
            use_kstack('bool'): Use faster version of copy, defaults False
                                Not supported with a file transfer protocol
                                prompting for a username and password
        Returns:
            None
    """
    fu = FileUtils.from_device(device)

    # build the source address
    source = '{p}://{s}/{f}'.format(p=protocol, s=server, f=remote_path)
    try:
        if vrf:
            fu.copyfile(source=source, destination=local_path, device=device,
                        vrf=vrf, timeout_seconds=timeout, compact=compact,
                        use_kstack=use_kstack, **kwargs)
        else:
            fu.copyfile(source=source, destination=local_path, device=device,
                        timeout_seconds=timeout, compact=compact,
                        use_kstack=use_kstack, **kwargs)
    except Exception as e:
        if compact or use_kstack:
            log.info("Failed to copy with compact/use-kstack option, "
                     "retrying again without compact/use-kstack")
            fu.copyfile(source=source, destination=local_path, device=device,
                        vrf=vrf, timeout_seconds=timeout, **kwargs)
        else:
            raise

def copy_from_device(device, remote_path, local_path, server, protocol, vrf=None, timeout=300, **kwargs):
    """
    Copy file from device to linux server (Works for sftp and ftp)
        Args:
            device ('Device'): Device object
            remote_path ('str'): remote file path to copy to on the server
            local_path ('str'): local file path to copy from the device
            server ('str'): hostname or address of the server
            protocol('str'): file transfer protocol to be used
            vrf ('str'): vrf to use (optional)
            timeout('int'): timeout value in seconds, default 300
        Returns:
            None
    """

    fu = FileUtils.from_device(device)

    # build the source address
    destination = '{p}://{s}/{f}'.format(p=protocol, s=server, f=remote_path)
    if vrf:
        fu.copyfile(source=local_path, destination=destination, device=device, vrf=vrf, timeout_seconds=timeout, **kwargs)
    else:
        fu.copyfile(source=local_path, destination=destination, device=device, timeout_seconds=timeout, **kwargs)


def get_file_size_from_server(device, server, path, protocol, timeout=300,
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
        return _get_file_size_from_server(server, path, protocol, timeout=timeout,
                                          fu_session=fu_session)
    else:
        with FileUtils(testbed=device.testbed) as fu:
            return _get_file_size_from_server(server, path, protocol, timeout=timeout,
                                              fu_session=fu)

def _get_file_size_from_server(server, path, protocol, timeout=300,
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

    # get file size, and if failed, raise an exception
    try:
        return fu_session.stat(target=url, timeout_seconds=timeout).st_size
    except NotImplementedError as e:
        log.warning(
            'The protocol {} does not support file listing, unable to get file '
            'size.'.format(
                protocol))
        raise e from None
    except Exception as e:
        raise Exception("Failed to get file size : {}".format(str(e)))

def modify_filename(device, file, directory, protocol, server=None,
                    append_hostname=False, check_image_length=False,
                    limit=63, unique_file_name=False):
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
            unique_file_name（'bool'): append a six digit random number to the end of
                                        file name to make it unique
        Raises:
            ValueError
        Returns:
            truncated image name
            """
    if not server:
        server = device.api.get_longest_server_address()

    new_name = file
    image_name, image_ext = os.path.splitext(file)
    if check_image_length:
        log.info('Checking if file length exceeds the limit of {}'.format(limit))
        url = ''.join([protocol, ':/', server, '//', directory])

        if not url.endswith('/'):
            url = url + '/'
        if len(url) > limit:
            raise ValueError('The length of the directory URL already exceeds'
                             ' {} characters.'.format(limit))

        length = len(url) + len(file)

        # counts hostname in length if provided
        if append_hostname:
            length += len(device.name)+1

        # counts random number in length.  6 digits + underscore = 7
        if unique_file_name:
            length += 7

        # truncate image
        if length > limit:
            # always negative number
            diff = limit - length
            image_name = image_name[:diff]
        new_name = ''.join([image_name, image_ext])

    if append_hostname:
        image_name, image_ext = os.path.splitext(new_name)
        new_name = ''.join([image_name, '_', device.name, image_ext])

    if unique_file_name:
        image_name, image_ext = os.path.splitext(new_name)
        rand_num = random.randint(100000, 999999)
        new_name = ''.join([image_name, '_', str(rand_num), image_ext])

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
        addr = server.get('address','')
        if isinstance(addr, list):
            addresses.extend(addr)
        else:
            addresses.append(addr)

    return max(addresses, key=len)

def delete_file_on_server(testbed, server, path, protocol='sftp', timeout=300, fu_session=None):
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
        return _delete_file_on_server(server, path, protocol=protocol, timeout=timeout,
                               fu_session=fu_session)
    else:
        with FileUtils(testbed=testbed) as fu:
            return _delete_file_on_server(server, path, protocol=protocol,
                                          timeout=timeout,
                                          fu_session=fu)

def _delete_file_on_server(server, path, protocol='sftp', timeout=300, fu_session=None):

        url = '{p}://{s}/{f}'.format(p=protocol, s=server, f=path)

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

    device_obj = Device(name=server,
                        os='linux',
                        credentials=server_block.credentials,
                        connections={'linux': {
                            'ip': hostname,
                            'protocol': 'ssh'}},
                        custom={'abstraction':{
                            'order':['os']}},
                        type='linux',
                        testbed=device.testbed)

    return device_obj

def get_username_password(device, username=None, password=None, creds=None):
    """ Gets the username and password to use to log into the device console.
    """
    if username is None or password is None:
        if hasattr(device, 'credentials') and device.credentials:
            if creds is not None:
                cred = creds[0] if isinstance(creds, list) else creds
            else:
                cred='default'
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

def dynamic_diff_parameterized_running_config(device, base_config, mapping, running_config=None):
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
    
    output = diff_configuration(device, base_config, running_config).diff_string('+')

    for interface, variable in mapping.items():
        output = output.replace(' {} '.format(interface), ' {} '.format(variable))
        output = output.replace(' {}\n'.format(interface), ' {}\n'.format(variable))

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

    return '{}{}'.format(template, base_config)
