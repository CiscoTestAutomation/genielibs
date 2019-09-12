"""Utility type functions that do not fit into another category"""

# Python
import logging
import re
import jinja2
import shlex, subprocess
import time
from time import strptime
from datetime import datetime
from netaddr import IPAddress

# pyATS
from pyats.easypy import runtime

# Genie
from genie.utils.config import Config
from genie.utils.diff import Diff
from genie.libs.parser.utils.common import Common
from genie.utils.timeout import Timeout

# unicon
from unicon.eal.dialogs import Dialog, Statement
from unicon.core.errors import ConnectionError
from unicon.plugins.generic.statements import default_statement_list
from unicon.core.errors import SubCommandFailure

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

        Args:
            output ('str'): Text output from command
        Returns:
            Datetime object
            Format : datetime(year, month, day, hour, minute, second, microseconds)
    """

    r1 = re.compile(
        r"Time\ssource\sis\sNTP\,\s\.*(?P<hour>\d+)\:(?P<minute>\d+)\:"
        "(?P<seconds>\d+)\.(?P<milliseconds>\d+)\s(?P<time_zone>"
        "\S+)\s(?P<day_of_week>\S+)\s(?P<month>\S+)\s(?P<day>\d+)"
        "\s(?P<year>\d+)"
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

    return device


def destroy_connection(device):
    """ Destroy connection device
        Args:
            device ('obj'): Device object

    """
    log.info("Destroying current connection")
    device.destroy_all()
    log.info("Connection destroyed")


def configure_device(device, config):
    """shut interface

        Args:
            device (`obj`): Device object
            config (`str`): Configuration to apply
    """
    try:
        device.configure(config)
    except Exception as e:
        raise Exception("{}".format(e))
    return


def reconnect_device(device, max_time=300, interval=30, sleep_disconnect=30):
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