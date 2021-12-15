"""Utility type functions that do not fit into another category"""

# Python
import re
import logging
import subprocess
import time
from pyats.async_ import Pcall

# Genie
from genie.libs.sdk.apis.utils import get_config_dict
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils.timeout import Timeout
from genie.libs.parser.iosxe.ping import Ping

# unicon
from unicon.eal.dialogs import Dialog, Statement
from unicon.core.errors import SubCommandFailure
from ats.log.utils import banner


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
    device, capture_name=None, interface=None, direction='both', capture_command=None
):
    """Start packet capture

        Args:
            device (`obj`): Device object
            capture_name (`str`): Packet capture name
            interface (`str`): Interface to capture the packets on
            capture_command (`str`): Monitor command
            direction ('str'): direction of the capture pkts. Default is both direction

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
            "{direction} match any".format(
                capture_name=capture_name, interface=interface, direction=direction
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
        log.warn("Failed to copy from {lp} to {rp} via scp: {e}".format(
            lp=local_path, rp=remote_path, e=e))
        return False

    # return True/False depending on result
    return 'bytes copied in' in out


def delete_files(device, locations, filenames):
    """ Delete local file

        Args:
            device (`obj`): Device object
            locations (`list`): list of locations
                                  ex.) bootflash:/core/
            filenames (`list`): file name. regular expression is supported
        Returns:
            deleted_files (`list`): list of deleted files
    """
    deleted_files = []

    # loop by given locations
    for location in locations:
        log.info('Checking {location}...'.format(location=location))
        parsed = device.parse('dir {location}'.format(location=location))

        # loop by given filenames
        for filename in filenames:

            # find target files by using Dq with regex
            matched_files = parsed.q.contains_key_value(
                'files', filename, value_regex=True).get_values('files')
            log.debug('Matched files to delete: {matched_files}'.format(
                matched_files=matched_files))
            # delete files which were found
            for file in matched_files:
                if location[-1] != '/':
                    location += '/'
                device.execute('delete /force {location}{file}'.format(
                    location=location, file=file))
                # build up list for return
                deleted_files.append('{location}{file}'.format(
                    location=location, file=file))

    return deleted_files


def verify_ping(
    device, address, expected_max_success_rate=100, expected_min_success_rate=0,
    count=None, source=None, vrf=None, max_time=60, check_interval=10,
):
    """Verify ping

    Args:
            device ('obj'): Device object
            address ('str'): Address value
            expected_max_success_rate (int): Expected maximum success rate
            expected_min_success_rate (int): Expected minimum success rate
            count ('int'): Count value for ping command
            source ('str'): Source IP address, default: None
            vrf (`str`): vrf id
            max_time (`int`): Max time, default: 30
            check_interval (`int`): Check interval, default: 10
    """

    p = re.compile(r"Success +rate +is +(?P<rate>\d+) +percent.*")

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if address and count and source:
            cmd = 'ping {address} source {source} repeat {count}'.format(
                    address=address,
                    source=source,
                    count=count)
        elif address and count:
            cmd = 'ping {address} repeat {count}'.format(
                    address=address,
                    count=count)
        elif address and source:
            cmd = 'ping {address} source {source}'.format(
                    address=address,
                    source=source)
        elif address and not vrf:
            cmd = 'ping {address}'.format(address=address)
        elif vrf:
            cmd = "ping vrf {vrf} {address}".format(vrf=vrf,address=address)
        else:
            log.info('Need to pass address as argument')
            return False
        try:
            out = device.execute(cmd, error_pattern=['% No valid source address for destination'])
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
    # verify /md5 bootflash:test_file.bin
    # ....................................
    # ....................................Done!
    # verify /md5 (bootflash:test1.bin) = 2c9bf2c64bee6fb22277fc89bd1c8ff0
    try:
        output = device.execute('verify /md5 {}'.format(file), timeout=timeout)
        m = re.search(r' = (\S+)', output)
        if m:
            hash_value = m.group(1)
            return hash_value
        else:
            log.error('Could not find MD5 hash in output')
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
        tos ('int'): type of service value
        dscp (`str`): DSCP value
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


def get_mgmt_src_ip_addresses(device):
    """ Get the source IP addresses connected via SSH or telnet to the device.

    Returns:
        List of IP addresses or []
    """
    tcp_output = device.execute('show tcp brief | inc .22 |.23 ')
    # 0160C06C  5.25.26.9.22                5.25.24.1.51363             ESTAB
    mgmt_src_ip_addresses = set(re.findall(r'\w+ +\S+\.(?:22|23) +(\S+)\.\d+ +ESTAB', tcp_output))
    if not mgmt_src_ip_addresses:
        log.error('Unable to find management session, cannot determine management IP addresses')
        return []

    return mgmt_src_ip_addresses


def get_mgmt_ip(device):
    """ Get the management IP address of the device.

    Returns:
        IP address string or None
    """
    tcp_output = device.execute('show tcp brief | inc .22 |.23 ')
    # 0160C06C  5.25.26.9.22                5.25.24.1.51363             ESTAB
    m = re.search(r'\w+ +(\S+)\.(22|23) +\S+\.\d+ +ESTAB', tcp_output)
    if m:
        mgmt_ip = m.group(1)
    else:
        log.error('Unable to find management session, cannot determine IP address')
        return None

    return mgmt_ip


def get_mgmt_ip_and_mgmt_src_ip_addresses(device):
    """ Get the management IP address and management source addresses.

    Returns:
        Tuple of mgmt_ip and list of IP address (mgmt_ip, [mgmt_src_addrs]) or None
    """
    tcp_output = device.execute('show tcp brief | inc .22 |.23 ')

    # 0160C06C  5.25.26.9.22                5.25.24.1.51363             ESTAB
    mgmt_src_ip_addresses = set(re.findall(r'\w+ +\S+\.(?:22|23) +(\S+)\.\d+ +ESTAB', tcp_output))
    if not mgmt_src_ip_addresses:
        log.error('Unable to find management session, cannot determine management IP addresses')

    m = re.search(r'\w+ +(\S+)\.(22|23) +\S+\.\d+ +ESTAB', tcp_output)
    if m:
        mgmt_ip = m.group(1)
    else:
        log.error('Unable to find management session, cannot determine IP address')
        mgmt_ip = None

    if not mgmt_ip or not mgmt_src_ip_addresses:
        return None

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


def get_show_output_line_count(device, command, filter, output=None):
    """ Count number of lines from show command.

        The command string is created using "{command} | count {filter}"

        Args:
            device (`obj`): Device object
            command (`str`): show command
            filter (`str`): filter expression
            output (`str`): output of show command. (optional) Default to None
        Returns:
            line_count (`int`): number of lines based on show command output
        Raises:
            N/A
    """
    command += ' | count {}'.format(filter)
    if output is None:
        output = device.execute(command)

    p = re.compile(r'^Number of lines which match regexp = (?P<line_count>\d+)')

    for line in output.splitlines():
        line = line.strip()

        m = p.match(line)
        if m:
            return int(m.groupdict()['line_count'])

    log.warn("Couldn't get line count properly.")
    return 0


def clear_counters(device):
    """ clear logging
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("clear counters on {device}".format(device=device))

    dialog = Dialog([Statement(pattern=r'\[confirm\].*', action='sendline(\r)',loop_continue=True,continue_timer=False)])

    try:
        device.execute("clear counters", reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear counters on {device}. Error:\n{error}".format(device=device, error=e)
        )


def clear_logging(device):
    """ clear logging
        Args:
            device ('obj'): Device object
        Returns:
            output ('str'): Output of execution
        Raises:
            SubCommandFailure
    """
    dialog = Dialog([Statement(pattern=r'\[confirm\].*', action='sendline(\r)',loop_continue=True,continue_timer=False)])

    try:
        output = device.execute("clear logging", reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear logging on {device}. Error:\n{error}".format(device=device, error=e)
        )

    return output

def get_show_output_include(device, command, filter, output=None):
    """ Find the lines which are match from show command.
        Args:
            device (`obj`): Device object
            command (`str`): show command
            filter (`str`): filter expression
            output (`str`): output of show command. (optional) Default to None
        Returns:
            bool,output('str') : True/False, include command output based on the output
        Raises:
            N/A
    """
    command += ' | include {}'.format(filter)
    result = True

    try:
        output= device.execute(command)
        if output == "":
            log.error('No match found')
            result = False
    except:
        log.info("In valid command")
        result = False

    return [result,output]


def decrypt_tacacs_pcap(filename, key, filepath):
    """Decrypt and Converting the tacacs pcap file to tacacs txt file
        Args:
            filename: taacs pcap filename
            key: tacacs server key
            filepath: tacacs pcap file path

        Returns:
            True : Decrypted and copied to pcap txt file
            False: No data in pcap text file
    """

    decrypted_pcap_file = filename.replace("pcap", "txt")
    log.info("Decoding {0} file and saving the decrypted data to {1} file".
                format(filename, decrypted_pcap_file))
    cmd = 'tshark -r {path} -V -o tacplus.key:{key}>{decrypted_pcap_file}'.format(
        path=filepath, key=key, decrypted_pcap_file=decrypted_pcap_file)
    log.info(cmd)
    try:
        subprocess.getoutput(cmd)
        with open(decrypted_pcap_file, encoding="utf8", errors='ignore') as file:
            fdata = file.readlines()
        if fdata:
            log.info("Data copied from {0} to {1}".format(
                filename, decrypted_pcap_file))
            log.info("Decrypted pcap txt file saved in script location ")
            return decrypted_pcap_file
        else:
            log.info("No Data in {0}".format(decrypted_pcap_file))
            return False
    except Exception as error:
        log.error("Failed to decode tacacs pcap file using tshark {0}".format(error))
        return False


def parse_tacacs_packet(decrypted_pcap_file):
    """ Parsing tacacs pcap file data
        Args:
            decrypted_pcap_file: txt file having tacacs packet data
        Returns:
            tacacs_json_dict: dict contains tacacs data as
            json format

    """
    log.info(banner("start analysing the packet"))

    tacacs_json_dict = {}
    typedict = {}
    seqdict = {}
    aaadict = {}
    aaa_type = ""
    seqno = ''
    packetno = 1

    # Different patterns of tacacs packet
    # common pattern for all key-value data
    p = re.compile(r'(.*):\s*(.*)')

    # Patterns of Tacacs Header
    # Frame 1: 60 bytes on wire (480 bits), 60 bytes captured (480 bits)
    # on interface 0
    p0 = re.compile(r'\s*Frame.*')

    # TACACS+
    p1 = re.compile(r'(^TACACS[+]$)')

    # Type: Authentication(1)
    p2 = re.compile(r'\s*Type\:\s+(.*)\s*\(\d+\)')

    # Sequence number: 1
    p3 = re.compile(r'\s*(Sequence\s*number)\:\s*(\d+)')

    # .... .0.. = Single Connection: Not set
    p4 = re.compile(r'.*\=\s*(Single\s*Connection)\:\s*(.*)')

    # .... ...0 = Unencrypted: Not set
    p5 = re.compile(r'.*\=\s*(Unencrypted)\:\s*(.*)')

    # Session ID: 3305082361
    p6 = re.compile(r'.*\=\s*(Session\s*ID)\:\s*(.*)')

    # Decrypted Request
    p7 = re.compile(r'\s*Decrypted\s*(.*)')

    # Server message: Password:
    p8 = re.compile(r'\s*Server\s*message\:\s*(.*)')

    # authorization command
    # Arg[0] length: 13
    p9 = re.compile(r'\s*Arg\[(\d+)\]\s*length\:\s*(\d+)')

    # Arg[0] value: service=shell
    p10 = re.compile(r'Arg\[(\d+)\]\s*value\:\s*(.*)')

    # accounting commands
    # .... ...0 = More: Not set
    # .... ..0. = Start: Not set
    # .... .1.. = Stop: Set
    #   .... 0... = Watchdog: Not set
    p11 = re.compile(r'.*\=\s*(.*)\:\s*(.*)')

    with open(decrypted_pcap_file, encoding="utf8", errors='ignore') as file:
        fdata = file.readlines()
        if fdata:
            data = iter(list(fdata))
            for i in data:
                # TACACS+
                res = p1.match(i)
                if res:
                    for j in range(100):
                        ndata = next(data)
                        n = ndata.strip()

                        # Frame 1: 60 bytes on wire (480 bits), 60 bytes captured (480
                        # bits) on interface 0
                        if p0.match(n):
                            break

                        # Type: Authentication(1)
                        res = p2.match(n)
                        if res:
                            aaa_type = "".join(res.group(1).split(" "))
                            typedict = tacacs_json_dict.setdefault(aaa_type, {})
                            continue

                        # Sequence number: 1
                        res = p3.match(n)
                        if res:
                            seqno = "".join(res.group(2).split(" "))
                            if seqno == '1':
                                aaa_p = aaa_type[:6] + 'packet' + str(packetno)
                                aaadict = typedict.setdefault(aaa_p, {})
                                packetno += 1
                            seqdict = aaadict.setdefault(seqno, {})
                            continue

                        if seqno != '':
                            # .... .0.. = Single Connection: Not set
                            res = p4.match(n)
                            if res:
                                single_connection = res.group(2)
                                seqdict["single_connection"] = single_connection
                                continue

                            # .... ...0 = Unencrypted: Not set
                            res = p5.match(n)
                            if res:
                                unencrypted = res.group(2)
                                seqdict["unencrypted"] = unencrypted
                                continue

                            # Session ID: 3305082361
                            res = p6.match(n)
                            if res:
                                seesion_id = res.group(2)
                                seqdict["seesion_id"] = seesion_id
                                continue

                            # Decrypted Request
                            res = p7.match(n)
                            if res:
                                msgtype = res.group(1)
                                seqdict["msgtype"] = msgtype
                                continue

                        if aaa_type == 'Authentication':
                            # Server message: Password:
                            res = p8.match(n)
                            if res:
                                server_message = res.group(1)
                                seqdict["server_message"] = server_message
                                continue
                            # common pattern for all key-value data
                            res = p.match(n)
                            if res:
                                key = res.group(1).lower().replace(" ", "_")
                                value = res.group(2)
                                seqdict[key] = value
                                continue

                        if aaa_type == 'Authorization':
                            # Arg[0] length: 13
                            arg_len = p9.match(n)
                            if arg_len:
                                key = "arg_len" + arg_len.group(1)
                                seqdict[key] = arg_len.group(2)
                                continue

                            # Arg[0] value: service=shell
                            arg_value = p10.match(n)
                            if arg_value:
                                key = "arg_value" + arg_value.group(1)
                                seqdict[key] = arg_value.group(2)
                                continue

                            # common pattern for all key-value data
                            res = p.match(n)
                            if res:
                                key = res.group(1).lower().replace(" ", "_")
                                value = res.group(2)
                                seqdict[key] = value
                                continue

                        if aaa_type == 'Accounting':
                            # Arg[0] length: 13
                            arg_len = p9.match(n)
                            if arg_len:
                                key = "arg_len" + str(arg_len.group(1))
                                seqdict[key] = arg_len.group(2)
                                continue
                            # Arg[0] value: service=shell
                            arg_value = p10.match(n)
                            if arg_value:
                                key = "arg_value" + arg_value.group(1)
                                seqdict[key] = arg_value.group(2)
                                continue

                            # .... ...0 = More: Not set
                            # .... ..0. = Start: Not set
                            # .... .1.. = Stop: Set
                            #   .... 0... = Watchdog: Not set
                            arg_value = p11.match(n)
                            res = p11.match(n)
                            if res:
                                flag_name = res.group(1).lower()
                                flags = res.group(2)
                                seqdict[flag_name] = flags
                                continue
                            # common pattern for all key-value data
                            res = p.match(n)
                            if res:
                                key = res.group(1).lower().replace(" ", "_")
                                value = res.group(2)
                                seqdict[key] = value
                                continue
                    continue
            return tacacs_json_dict
        else:
            log.info("No data in {0} to parse".format(decrypted_pcap_file))
            return False


def verify_tacacs_packet(tacacs_json_dict, verfifydict):
    """Validating Authentication, Authorization and Accounting json data
    with the verifydict data
        Args:
            tacacs_json_dict: parsed tacacs packet data
            verfifydict:  dict having authentication or accounting or
                        authorization attributes to verify
        Returns:
            final_verify: dict contains authentication or accounting or
            authorization bool values
    """
    final_verify = {}
    for i in verfifydict:
        type = i
        count = 0
        for type_dict in verfifydict[i]:
            count += 1
            final_verify[type + str(count)] = False
            seq_dict = {}
            aaapackets = tacacs_json_dict[type].keys()
            for i in aaapackets:
                seq_dict.setdefault(i, {})
                seq = tacacs_json_dict[type][i].keys()
                for e in type_dict.keys():
                    seq_dict.setdefault(i, {}).setdefault(e, {})
                    if e in seq:
                        aaa_flag = {}
                        seqfields = tacacs_json_dict[type][i][e]
                        for f in type_dict[e].keys():
                            if f in seqfields.keys():
                                if type_dict[e][f] == seqfields[f]:
                                    aaa_flag[f] = True
                                else:
                                    aaa_flag[f] = False
                            else:
                                aaa_flag[f] = False
                    if all(aaa_flag.values()):
                        seq_dict[i][e] = True
                    else:
                        seq_dict[i][e] = False
            for v in seq_dict.keys():
                if all(seq_dict[v].values()) is True:
                    log.info("{0} packet found {1} {2}".format(type, v,
                                                                  type_dict))
                    final_verify[type + str(count)] = True
    return final_verify


def perform_ssh(device, testbed, enable_pass, timeout=60):
    """
    Restore config from local file using copy function
        Args:
            device (`obj`): Device object
            testbed (`str`): Testbed object
            enable_pass (`str`): Enable password
            timeout (int): Optional timeout value
                           default value 60
        Returns:
            None
    """
    hostname = testbed.devices['uut'].name
    username = testbed.custom['username']
    password = testbed.custom['password']
    ip_address = testbed.devices['uut'].custom['int_ipaddress']

    ssh_dict = {
                'pass_timeout_expire_flag': False,
                'ssh_pass_case_flag': False,
                'enable_pass_flag': False
                }

    def pass_timeout_expire():
        ssh_dict['pass_timeout_expire_flag'] = True

    def send_pass(spawn):
        if ssh_dict['enable_pass_flag']:
            spawn.sendline(enable_pass)
            ssh_dict['enable_pass_flag'] = False
        else:
            spawn.sendline(password)

    def ssh_pass_case(spawn):
        ssh_dict['ssh_pass_case_flag'] = True
        spawn.sendline(' exit')

    def send_enable(spawn):
        ssh_dict['enable_pass_flag'] = True
        spawn.sendline('enable')

    dialog = Dialog([

            Statement(pattern=r"Password:\s*timeout expired!",
                      action=pass_timeout_expire,
                      loop_continue=False),
            Statement(pattern=r"Password:",
                      action=send_pass,
                      loop_continue=True),
            Statement(pattern=r""+hostname+">",
                      action=send_enable,
                      loop_continue=True),
            Statement(pattern=r""+hostname+"#",
                      action=ssh_pass_case,
                      loop_continue=True),

    ])
    try:
        device.execute('ssh -l {u} {i}'.format(u=username, i=ip_address),
                       reply=dialog,
                       prompt_recovery=True,
                       timeout=timeout)
    except Exception as e:
        log.info(f"Error occurred while performing ssh : {e}")

    if ssh_dict['pass_timeout_expire_flag']:
        return False
    if ssh_dict['ssh_pass_case_flag']:
        return True


def concurrent_ssh_sessions(concurrent_sessions, iteration_times, device, testbed,
                            enable_pass):
    """
    Generates multiple ssh sessions
        Args:
            device (`obj`): Device object
            testbed (`str`): Testbed object
            enable_pass (`str`): enable password
            concurrent_sessions (`int`): count of ssh session to generate
            iteration_times (`int`): count of concurrent_sessions to repeat
        Returns:
            None
    """
    for iteration in range(iteration_times):
        log.info(f"generating sessions for iteration {iteration + 1}")

        p = Pcall(perform_ssh, device=[device]*concurrent_sessions,
                  testbed=[testbed]*concurrent_sessions,
                  enable_pass=[enable_pass]*concurrent_sessions)

        # start all child processes
        p.start()
        # wait for everything to finish
        p.join()

        time.sleep(2)


def get_radius_packets(pcap_or_packet):
    """
    returns radius packets from pcap file/packet
        Args:
            pcap_or_packet (`str/obj`): path of pcap file or packet object obtained
                                        from scapy module
        Returns:
            List contains radius packets
    """
    try:
        from scapy.all import rdpcap
        from scapy.layers.radius import Radius
    except ImportError:
        raise ImportError('scapy is not installed, please install it by running: '
                          'pip install scapy') from None

    # Read the pcap file if path is provided
    if isinstance(pcap_or_packet, str):
        pcap_or_packet = rdpcap(pcap_or_packet)

    return pcap_or_packet.getlayer(Radius)


def get_packet_attributes_scapy(packet):
    """
    returns attributes and their values of a packet
        Args:
            packet (`obj`): packet object obtained from scapy module
        Returns:
            dict with attributes and their values
    example:
        {
            "User-Name": {"value": "'6c8bd38ec702'", "len": "14"},
            "User-Password": {"value": "b392032ba377baacffb4cacf3a8d9b04", "len": "18"},
            "Service-Type": {"value": "Call Check", "len": "6"},
            "Framed-MTU": {"value": "1468", "len": "6"},
            "Message-Authenticator": {"value": "d215599321f88dca2cacb5e0e793f354", "len": "18"},
            "EAP-Key-Name": {"value": "''", "len": "2"},
            "NAS-IP-Address": {"value": "10.106.26.213", "len": "6"},
            "NAS-Port-Id": {"value": "'TenGigabitEthernet1/0/11'", "len": "26"},
            "NAS-Port-Type": {"value": "Ethernet", "len": "6"},
            "NAS-Port": {"value": "50111", "len": "6"},
            "Calling-Station-Id": {"value": "'6C-8B-D3-8E-C7-02'", "len": "19"},
            "NAS-Identifier": {"value": "'Switch-9500'", "len": "13"},
            "Called-Station-Id": {"value": "'D0-EC-35-92-C9-8B'", "len": "19"},
        }
    """
    try:
        from scapy.layers.radius import Radius
    except ImportError:
        raise ImportError('scapy is not installed, please install it by running: '
                          'pip install scapy') from None

    attr_dict = {}
    for i in range(0, len(packet.attributes)):
        attribute = packet.attributes[i]
        attr_type = attribute.get_field('type').i2repr(attribute, attribute.type)
        type_dict = attr_dict.setdefault(attr_type, {})
        type_dict.update({'value': attribute.get_field('value').i2repr(
                        attribute, attribute.value)})
        type_dict.update({'len': attribute.get_field('len').i2repr(
                        attribute, attribute.len)})

        if 'Vendor-Specific' in attr_type:
            av_pair = attribute.get_field('value').i2repr(attribute, attribute.value)
            vender_type = type_dict.setdefault(av_pair, {})
            vender_type.update({'vendor_type': attribute.get_field(
                            'vendor_type').i2repr(attribute, attribute.vendor_type)})
            vender_type.update({'vender_id': attribute.get_field('vendor_id').i2repr(
                            attribute, attribute.vendor_id)})
            vender_type.update({'vendor_len': attribute.get_field('vendor_len').i2repr(
                            attribute, attribute.vendor_len)})

    return attr_dict


def get_packet_info_field(packet):
    """
    returns packets info
        Args:
            packet (`obj`): packet object obtained from scapy module
        Returns:
            returns packets info
    """

    return packet.get_field('code').i2repr(packet, packet.code)


def get_ip_packet_scapy(packet):
    """
    returns IP layer from packet
        Args:
            packet (`obj`): packet object obtained from scapy module
        Returns:
            ip packet
    """
    try:
        from scapy.layers.inet import IP
    except ImportError:
        raise ImportError('scapy is not installed, please install it by running: '
                          'pip install scapy') from None

    return packet.getlayer(IP)


def get_packet_ip_tos_field(packet):
    """
    returns types of services field from packet
        Args:
            packet (`obj`): packet object obtained from scapy module
        Returns:
            returns types of services field
    """

    return packet.get_field('tos').i2repr(packet, packet.tos)


def clear_ip_nat_translation_all(device):
    """ clear ip nat translation *
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Delete all dynamic translations on {device}".format(device=device))

    try:
        device.execute('clear ip nat translation *')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Delete all dynamic translations on {device}. Error:\n{error}".format(device=device, error=e)
        )


def clear_ip_mroute_all(device):
    """ clear ip mroute *
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Clearing ip mroute on {device}".format(device=device))

    try:
        device.execute("clear ip mroute *")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clearing ip mroute on {device}. Error:\n{error}".format(device=device, error=e)
        )


def get_show_output_section(device, command, filter):
    """ Display the lines which are match from section 
        Args:
            device (`obj`): Device object
            command (`str`): show command
            filter (`str`): filter expression
        Returns:
            bool,output('str') : True/False, section command output based on the output
        Raises:
            SubCommandFailure
    """
    command += ' | section {}'.format(filter)
    result = True

    try:
        output = device.execute(command)
        if not output:
            log.error('No match found')
            result = False
    except SubCommandFailure as e:
        raise SubCommandFailure("No match found or Invalid command executed on {device}. Error:\n{e}")

    return (result,output)
