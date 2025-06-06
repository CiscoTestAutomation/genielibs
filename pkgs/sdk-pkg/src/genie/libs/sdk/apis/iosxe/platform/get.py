# Python
import os
import re
import logging
import time

# pyATS
from pyats.easypy import runtime
from pyats.utils.objects import R, find

# Genie
from genie.utils import Dq
from genie.utils.diff import Diff
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import (SchemaEmptyParserError,
                                              SchemaMissingKeyError)
from genie.libs.parser.iosxe.show_logging import ShowLogging
from datetime import datetime, timedelta, timezone

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

def get_platform_standby_rp(device, max_time=1200, interval=120):
    """ Get standby router slot on device
        Args:
            device ('obj'): Device object
            max_time ('int'): Max time in seconds retrieving router information
            interval ('int'): Interval in seconds retrieving router information
        Raise:
            None
        Return:
            Integer: Number of RP
    """

    log.info("Getting standby slot")

    rs = R(
        ["slot", "(?P<val1>.*)", "rp", "(?P<val2>.*)", "state", "ok, standby"]
    )

    timeout = Timeout(max_time=max_time, interval=interval)
    while timeout.iterate():
        try:
            output = device.parse("show platform")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        ret = find([output], rs, filter_=False, all_keys=True)
        if ret:
            standby_rp = ret[0][1][1]
            srp = re.search(r"(?P<srp>(\d))", standby_rp).groupdict()["srp"]
            if srp:
                log.info(
                    "Standby RP on '{dev}' is: '{standby_rp}'".format(
                        dev=device.name, standby_rp=standby_rp
                    )
                )
                return srp

        timeout.sleep()

    return None


def get_diffs_platform(platform_before, platform_after):
    """ Check differences between two parsed outputs from 'show platform'

        Args:
            platform_before ('str'): Parsed output from 'show platform'
            platform_after ('str'): Parsed output from 'show platform'
        Return:
            True
            False
        Raises:
            None
    """

    dd = Diff(platform_before, platform_after, exclude=["insert_time"])
    dd.findDiff()

    for slot in platform_after["slot"]:
        for rp_lc in platform_after["slot"][slot]:
            for type_ in platform_after["slot"][slot][rp_lc]:
                state_after = platform_after["slot"][slot][rp_lc][type_][
                    "state"
                ]

                state_before = (
                    platform_before["slot"]
                    .get(slot, {})
                    .get(rp_lc, {})
                    .get(type_, {})
                    .get("state", False)
                )

                if not state_before:
                    log.info(
                        "Found differences between outputs:\n{out}".format(
                            out=dd
                        )
                    )
                    return False

                for subslot in platform_before["slot"][slot][rp_lc].get(
                    "subslot", []
                ):

                    subslot_state = (
                        platform_after["slot"][slot][rp_lc]
                        .get(subslot, {})
                        .get("state", False)
                    )

                    if not subslot_state:
                        log.info(
                            "Found differences between outputs:\n{out}".format(
                                out=dd
                            )
                        )

                if state_after == state_before or ("ok" in state_after and "ok" in state_before):
                    continue
                else:
                    log.info(
                        "Found differences between outputs:\n{out}".format(
                            out=dd
                        )
                    )
                    return False
    return True


def get_file_size(device, file, output=None):
    """Get file size on the device
        Args:
            device (`obj`): Device object
            file (`str`): File name
            output ('str'): Output of 'dir' command
                            if not provided, executes the cmd on device
        Returns:
            file size in `int` type or None if file size is not available
    """

    directory = ''.join([os.path.dirname(file), '/'])
    filename = os.path.basename(file)
    try:
        dir_output = device.parse('dir {}'.format(directory), output=output)
    except Exception as e:
        log.error("Failed to parse the directory listing due to: {}".\
                  format(str(e)))
        return None

    size = Dq(dir_output).contains(filename).get_values('size')
    if size:
        return int(size[0])
    else:
        log.error("File '{}' is not found on device".format(file))


def get_running_image(device):
    """Get running image on the device
        Args:
            device (`obj`): Device object
        Returns:
            Image or None
    """

    output = {}
    try:
        # Execute 'show version'
        output = device.parse("show version")
    except SchemaEmptyParserError as e:
        log.error("Command 'show version' did not return any results: {e}".format(e=e))
    except SchemaMissingKeyError as e:
        log.error("Missing key while parsing 'show version': {e}".format(e=e))
    except Exception as e:
        log.error("Failed to parse 'show version': {e}".format(e=e))

    if not output:
        return None

    system_image = output.get('version', {}).get('system_image')

    if 'packages.conf' in system_image:
        directory = system_image.split(":")[0]

        try:
            output = device.execute("more {}".format(system_image))
        except Exception as e:
            log.error("Failed to check contents of {}".format(system_image))
            return None

        # more bootflash:packages.conf
        # #! /usr/binos/bin/packages_conf.sh
        #
        # sha1sum: e4de49179e2b7fbd772888d0d8ce7fc57f830b80
        # boot  rp 0 0   rp_boot       csr1000v-rpboot.16.12.01a.SPA.pkg
        #
        # iso   rp 0 0   rp_base       csr1000v-mono-universalk9.16.12.01a.SPA.pkg

        for line in output.splitlines():
            if line.startswith("boot"):
                system_image = line.split()[-1]
                system_image = directory + ":" + system_image
                break

    return system_image


def get_available_space(device, directory='', output=None):
    """Gets available space on a given directory
        Args:
            device ('str'): Device object
            directory ('str'): Directory to check space
                               If not provided, checks current working directory
                               i.e. media:/path/to/my/dir
            output ('str'): Output of 'dir' command
                            if not provided, executes the cmd on device
        Returns:
            space available in bytes in `int` type or 
            None if failed to retrieve available space
    """

    try:
        dir_output = device.parse('dir {}'.format(directory), output=output)
    except Exception as e:
        log.error("Failed to parse the directory listing due to: {}".\
                  format(str(e)))
        return None

    bytes_free = Dq(dir_output).get_values(key='bytes_free')
    if bytes_free:
        return int(bytes_free[0])
    else:
        log.error("Failed to get available space for {}".format(directory))


def get_total_space(device, directory='', output=None):
    """Gets total space on a given directory
        Args:
            device ('str'): Device object
            directory ('str'): Directory to check space
                               If not provided, checks current working directory
                               i.e. media:/path/to/my/dir
            output ('str'): Output of 'dir' command
                            if not provided, executes the cmd on device
        Returns:
            space available in bytes in `int` type or 
            None if failed to retrieve available space
    """

    try:
        dir_output = device.parse('dir {}'.format(directory), output=output)
    except Exception as e:
        log.error("Failed to parse the directory listing due to: {}".\
                  format(str(e)))
        return None
    else:
        return int(Dq(dir_output).get_values('bytes_total')[0])


def get_boot_variables(device, boot_var, output=None):
    """Get current or next-reload boot variables on the device
        Args:
            device (`obj`): Device object
            boot_var (`str`): Type of boot variable to return to caller
            output (`str`): output from show boot
        Returns:
            List of boot images or []
    """

    # Check type
    assert boot_var in ['current', 'next']

    boot_images = []
    try:
        boot_out = device.parse("show bootvar", output=output)
    except SchemaEmptyParserError as e:
        log.error("Command 'show bootvar' did not return any output\n{}".\
                  format(str(e)))
    else:
        # Get current or next
        if boot_var == 'current':
            boot_variables = boot_out.get("active", {}).get("boot_variable")
        else:
            boot_variables = boot_out.get("next_reload_boot_variable")

        # Trim
        if boot_variables:
            for item in boot_variables.split(';'):
                if not item:
                    continue
                if ',' in item:
                    item, num = item.split(',')
                if " " in item:
                    item, discard = item.split(" ")
                boot_images.append(item)

    return boot_images


def get_config_register(device, next_reload=False, output=None):
    """Get current config-register setting on the device
        Args:
            device (`obj`): Device object
            next_reload (`bool`): Determine if returning next-reload value
        Returns:
            config-register value or None
    """

    try:
        boot_out = device.parse("show bootvar", output=output)
    except SchemaEmptyParserError as e:
        log.error("Command 'show bootvar' did not return any output\n{}".\
                  format(str(e)))
        return None

    # Set keys
    nr_key = 'next_reload_configuration_register'
    # Check if next_reload is set
    if next_reload and nr_key in boot_out.get('active'):
        return boot_out.get('active').get(nr_key)
    else:
        cr_key = 'configuration_register'
        return boot_out.get('active').get(cr_key)

def get_platform_default_dir(device, output=None):
    """Get the default directory of this device

        Args:
            device (`obj`): Device object
            output (`str`): Output of `dir` command
        Returns:
            default_dir (`str`): Default directory of the system
    """

    try:
        output = device.parse("dir", output=output)
    except SchemaEmptyParserError as e:
        raise Exception("Command 'dir' did not return any output") from e

    return output.setdefault('dir', {}).get('dir', '').replace('/', '')


def get_platform_core(device,
                      default_dir,
                      output=None,
                      keyword=['.core.gz', '.tar.gz'],
                      num_of_cores=False,
                      decode=False,
                      decode_timeout=300,
                      remote_device=None,
                      remote_path=None,
                      remote_via=None,
                      vrf=None,
                      archive=False,
                      delete_core=False):
    """Get the default directory of this device

        Args:
            device      (`obj`) : Device object
            default_dir (`str` or `list`) : default directory where core or 
                                            system-report is generated on device
                                            ex.) `bootflash:/core/`
            output      (`str`) : Output of `dir` command
            keyword     (`list`): List of keywords to search
            num_of_cores (`bool`): flag to return number of core files
                                   Default to False
            remote_device (`str`): remote device in testbed yaml
                                   Default to None
            remote_path (`str`): path with/without file on remote device
                                 Default to None
            remote_via (`str`) : specify connection to get ip
                                 Default to None
            vrf (`str`): use vrf where scp find route to remote device
                                 Default to None
            archive     (`bool`): flag to save the decode output as file in archive
                                  Defaults to False
            delete_core (`bool`): flag to delete core files only when copying to
                                  remove_device is successfully done
                                  Defaults to False

            ### CISCO INTERNAL ###
            decode      (`bool`): flag to enable for decoding core
                                  copy core file to remote_server and decode on remote_server
            decode_timeout (`int`): timeout to execute decode script
                                    Default to 300

        Returns:
            all_corefiles (`list`, `int`): List of found core files
                                           or number of core files if num_of_cores=True
    """
    return device.api.health_core(default_dir, output, keyword, num_of_cores,
                                  decode, decode_timeout, remote_device,
                                  remote_path, remote_via, vrf, archive,
                                  delete_core, health=False)


def get_platform_logging(device,
                         command='show logging',
                         files=None,
                         keywords=None,
                         output=None,
                         num_of_logs=False):
    """Get logging messages

        Args:
            device    (`obj`): Device object
            command   (`str`): N/A
            files    (`list`): Not applicable on this platform
            keywords (`list`): List of keywords to match
            output    (`str`): Output of show command
            num_of_logs (`bool`): flag to return number of log messages
                                  Default to False
        Returns:
            logs     (`list` or `int`): list of logging messages
                                        OR or number of core files if num_of_logs=True
    """
    return device.api.health_logging(command, files, keywords, output, num_of_logs, health=False)

def get_platform_cpu_load(device,
                          command='show processes cpu',
                          processes=None,
                          check_key='five_sec_cpu',
                          output=None):
    """Get cpu load on device

        Args:
            device     (`obj`): Device object
            command    (`str`): Override show command
                                Default to `show processes cpu`
            processes (`list`): List of processes to check
            check_key  (`str`): Key to check in parsed output
                                Default to `five_sec_cpu`
            output     (`str`): Output of show command
        Returns:
            cpu_load   (`int`): Cpu load (5 secs average by default) on the device (percentage)
                                If multiple processes are given, returns average.
    """
    cpu_load = 0

    try:
        parsed = device.parse(command, output=output)
    except SchemaEmptyParserError as e:
        log.error("Command '{cmd}' did not return any output\n{msg}".\
                  format(cmd=command, msg=str(e)))
        return None

    if processes:
        count = 0
        for ps_item in processes:
            # To get process id based on check_key
            # {
            #   (snip))
            #   "sort": {
            #     "1": {
            #       "process": "Chunk Manager",
            #       (snip)
            #       "five_sec_cpu": 0.0,
            pids = parsed.q.contains_key_value(
                'process', ps_item, value_regex=True).get_values('sort')
            count = len(pids)
            for pid in pids:
                cpu_load += parsed.q.contains_key_value('sort',
                                                        pid).get_values(
                                                            check_key, 0)
        if count == 0:
            cpu_load = 0
        else:
            cpu_load /= count
    else:
        cpu_load = float(parsed['five_sec_cpu_total'])

    return cpu_load


def get_platform_cpu_load_detail(device,
                                 command='show processes cpu',
                                 processes=None,
                                 check_key='five_sec_cpu',
                                 check_key_total='five_sec_cpu_total',
                                 output=None):
    """Get cpu load on device

        Args:
            device     (`obj`): Device object
            command    (`str`): Override show command
                                Default to `show processes cpu`
            processes (`list`): List of processes to check
                                if not specified, will return one ALL_PROCESSES 
                                with total cpu load
            check_key  (`str`): Key to check in parsed output
                                Default to `five_sec_cpu`
            check_key_total (`str`): Key to check in parsed output for Total
                                     Default to `five_sec_cpu_total`
            output     (`str`): Output of show command
        Returns:
            cpu_load_dict  (`dict`): Cpu load dictionary on the device
                                     example:
                                     {
                                         'OMP': 0.0,
                                         'NAT-ROUTE': 0.0,
                                     }
    """
    return device.api.health_cpu(command,
                                 processes,
                                 check_key,
                                 check_key_total,
                                 output,
                                 health=False)


def get_platform_memory_usage(device,
                              command='show processes memory',
                              processes=None,
                              check_key='processor_pool',
                              output=None):
    """Get memory usage on device

        Args:
            device         (`obj`): Device object
            command        (`str`): Override show command
                                    Default to `show processes memory`
            processes     (`list`): List of processes to check
                                    If both processes and check_key are given,
                                    processes are preferred.
            check_key      (`str`): Key to check in parsed output
                                    Default to `processor_pool`
            output         (`str`): Output of show command
        Returns:
            memory_usage (`float`): memory usage on the device (percentage)
                                    If multiple processes are given, returns average.
    """

    memory_usage = 0
    try:
        parsed = device.parse(command, output=output)
    except SchemaEmptyParserError as e:
        log.error("Command '{cmd}' did not return any output\n{msg}".\
                  format(cmd=command, msg=str(e)))
        return None

    if processes:
        count = 0
        memory_holding = 0
        for ps_item in processes:
            # To get process id based on check_key
            # {
            #   "processor_pool": {
            #     "total": 735981852,
            #     "used": 272743032,
            #     "free": 463238820
            #   },
            #   (snip)
            #   "pid": {
            #     "0": {
            #       "index": {
            #         "1": {
            #           "pid": 0,
            #           "tty": 0,
            #           "allocated": 256940960,
            #           "freed": 73576632,
            #           "holding": 158001024,
            #           "getbufs": 392,
            #           "retbufs": 12905093,
            #           "process": "*Init*"
            #         },
            pids = parsed.q.contains_key_value(
                'process', ps_item, value_regex=True).get_values('pid')
            count = len(pids)
            for pid in pids:
                # use `sum` because it's possible one pid returns multiple `holding`
                memory_holding += sum(
                    parsed.q.contains_key_value('pid',
                                                pid).get_values('holding'))
        if parsed.get(check_key, {}).get('total', 0) == 0:
            memory_usage = 0
        else:
            memory_usage = memory_holding / parsed[check_key]['total']
        process_names = parsed.q.contains_key_value(
            'process', ps_item, value_regex=True).get_values('process')
    else:
        if parsed.get(check_key, {}).get('total', 0) == 0:
            memory_usage = 0
        else:
            memory_usage = parsed[check_key]['used'] / parsed[check_key][
                'total']
        process_names = []

    memory_usage *= 100

    return memory_usage


def get_platform_memory_usage_detail(device,
                                     command='show processes memory',
                                     processes=None,
                                     check_key='processor_pool',
                                     output=None):
    return device.api.health_memory(command,
                                    processes,
                                    check_key,
                                    output,
                                    health=False)


def get_stack_size(device):
    """Get switch stack size

    Args:
        device (obj): Device object

    Returns:
        int: Size of stack as int
    """

    switch_out = None
    module_out = None
    try:
        switch_out = device.parse('show switch detail')
    except Exception:
        try:
            module_out = device.parse('show module')
        except Exception:
            log.info('Failed to get stack size')
            return None

    if switch_out:
        return len(switch_out.q.get_values('stack'))

    if module_out:
        return len(module_out.get('switch', {}))

    return None

def get_slot_model(device, slot=None):
    """Gets the model name of one or all modules

    Args:
        device (obj): Device object
        slot (str, optional): Module slot to get. Defaults to None.

    Returns:
        dict: Dictionary mapped from slot number to model
    """

    try:
        out = device.parse('show module')
    except Exception:
        log.info('Failed to get slot model')
        return None

    if slot:
        model = out.get('switch', {}).get(str(slot), {}).get('model', None)
        return {str(slot): model}

    return {key: val.get('model', None) for key, val in out.get('switch').items()}

def get_chassis_type(device):
    """Get the chassis type of the device

    Args:
        device (obj): Device object

    Return:
        str: Device chassis
    """

    try:
        out = device.parse('show version')
    except SubCommandFailure:
        log.info('Could not get device version information')
        return None

    return out.q.get_values('chassis', 0)

def get_chassis_sn(device):
    """Get the chassis SN of the device

    Args:
        device (obj): Device object

    Return:
        str: Device chassis SN
    """

    try:
        out = device.parse('show version')
    except SubCommandFailure:
        log.info('Could not get device version information')
        return None

    return out.q.get_values('chassis_sn', 0)

def get_platform_type(device):
    """Get platform type of device

    Args:
        device (obj): Device object

    Return:
        str: Device platform type
    """

    try:
        out = device.parse('show version')
    except SubCommandFailure:
        log.info('Could not get device version information')
        return None

    return out.q.contains('platform').get_values('name', 0)

def get_slice_id_of_interface(device,interface):
    """Get the slice id of the interface

    Args:
        device (obj): Device object
        interface ('str'): interface name

    Return:
        str: Slice ID that the interface belongs to
    """

    try:
        out = device.parse('show platform software fed active ifm mappings')
    except SubCommandFailure:
        log.error('Could not get ifm mappings')
        return None

    slice_id = out['interface'][interface]['Core']

    return slice_id


def get_total_asics_cores(device, switch = None):
    """Get the total number of asics and cores

    Args:   
        device (obj): Device object
        switch ('str'): switch to get info

    Return: 
        total_asics: Number of asics
        total_cores: Number of cores
    """
    
    if switch is None:
        try:    
            output = device.parse('show platform software fed active ifm mappings')
        except SubCommandFailure:
            log.error('Could not get ifm mappings')
            return None

    else:
        try:
            output = device.parse('show platform software fed switch active ifm mappings')
        except SubCommandFailure:
            log.error('Could not get ifm mappings')
            return None

    asic = output.q.get_values('asic')
    core = output.q.get_values('core')
    total_asics = set(asic)
    total_asics = list(total_asics)
    total_cores = set(core)
    total_cores = list(total_cores)

    return total_asics, total_cores 

def get_platform_model_number(device):
    """Get platform model number or chassis type of device

    Args:
        device (obj): Device object

    Return:
        str: Device model number or chassis type
    """

    try:
        out_inventory = device.parse('show inventory').q.contains('chassis').get_values('pid', 0)
        output_detail=out_inventory
    except SubCommandFailure:
        log.info('Could not get device chassis type from inventory information')
        return None

    try:
        out_version = device.parse('show version').q.contains('version').get_values('chassis', 0)
    except SubCommandFailure:
        log.info('Could not get device chassis type from version information')
        return None

    if out_inventory == out_version:
        return output_detail
    else:
        log.info(
            'Could not get device "platform model number", mismatch in chassis type in "inventory" and "version" information'
        )
        return None

def get_number_of_interfaces(device):
    """ Gets the device number of interfaces
        Args:
            device (`obj`): Device object
        Returns:
            number of interfaces
            False if None
    """
    
    try:
        # Execute 'show version'
        out = device.parse("show version")
    except SchemaEmptyParserError as e:
        log.error("Command 'show version' did not return any results: {e}".format(e=e))
    except SchemaMissingKeyError as e:
        log.error("Missing key while parsing 'show version': {e}".format(e=e))
    except Exception as e:
        log.error("Failed to parse 'show version': {e}".format(e=e))
    else:        
        return out['version']['number_of_intfs']

    return False

def get_device_uptime(device):
    """ Gets the device uptime
        Args:
            device (`obj`): Device object
        Returns:
            uptime
            False if None
    """
    
    try:
        # Execute 'show version'
        out = device.parse("show version")
    except SchemaEmptyParserError as e:
        log.error("Command 'show version' did not return any results: {e}".format(e=e))
    except SchemaMissingKeyError as e:
        log.error("Missing key while parsing 'show version': {e}".format(e=e))
    except Exception as e:
        log.error("Failed to parse 'show version': {e}".format(e=e))
    else:
        return out.q.contains('version').get_values('uptime', 0)

    return False
    
def get_dscp_cos_qos_queue_stats(
    device,
    interface,
    cos=None,
    dscp=None,
    switch_type=None,
    switch_num=None,
    switch=None):

    """ Gets the ingress or egress dscp and cos stats
        Args:
            device (`obj`): Device object
            interface ('str'): Device interface
            cos ('str',optional): Ingress COS0 or Egress COS7
            dscp ('str',optional): Ingress DSCP0 or Egress DSCP43
            switch ('str',optional): switch to get info
            switch_type ('str',optional): switch_type active or standby to get info
            switch_num ('str',optional): switch_num 1 or 2 or 3 to get info
        Returns:
            heading,frames and bytes
            If condition not matched it will return None
    """
    try:
        if switch:
            if switch_num:
                output=device.parse("show platform hardware fed switch {switch_num} qos dscp-cos counters interface {interface}".format(switch_num=switch_num,switch=switch,interface=interface))
            elif switch_type:
                output=device.parse("show platform hardware fed switch {switch_type} qos dscp-cos counters interface {interface}".format(switch_type=switch_type,switch=switch,interface=interface))        
        else:
            output=device.parse("show platform hardware fed {switch_type} qos dscp-cos counters interface {interface}".format(interface=interface,switch_type=switch_type))
    except SubCommandFailure:
        log.error('Could not get dscp or cos qos queue stats')
        return None

    heading = output['@heading']
    if dscp and cos:
        dscp_frames = output['traffictype'][dscp]['frames']
        cos_frames = output['traffictype'][cos]['frames']
        return heading,dscp_frames,cos_frames
    elif dscp:
        dscp_frames = output['traffictype'][dscp]['frames']
        dscp_bytes = output['traffictype'][dscp]['bytes']
        return heading,dscp_frames,dscp_bytes
    elif cos:
        cos_frames = output['traffictype'][cos]['frames']
        cos_bytes = output['traffictype'][cos]['bytes']
        return heading,cos_frames,cos_bytes
    else:
        return None

def get_boot_time(device):
    """
    Extracts the boot time of the device.

    Args:
        device (`obj`): Device object.

    Returns:
        tuple: Boot time in Unix timestamp format and its range.
    """
    try:
        # Parse the 'show version' command output
        out_ver = device.parse('show version')
        
        # Extract the compiled date and uptime string
        compiled_date_str = out_ver['version']['compiled_date']
        uptime_str = out_ver['version']['uptime']

        # Parse the 'show clock' command output to get the timezone
        out_clock = device.parse('show clock')
        timezone_str = out_clock.get('timezone')

        # Define the format of the date string
        date_format = '%a %d-%b-%y %H:%M'

        # Parse the compiled date string
        parsed_compiled_date = datetime.strptime(compiled_date_str, date_format)

        # Define timezone offset dictionary
        timezone_offsets = {
            'PST': -8, 'IST': 5.5, 'UTC': 0,  # Fill in more timezones as needed
            'PDT': -7, 'MST': -7, 'MDT': -6,
            'CST': -6, 'CDT': -5, 'EST': -5,
            'EDT': -4
        }

        # Get timezone offset from dictionary
        timezone_offset = timezone_offsets.get(timezone_str)

        if timezone_offset is None:
            raise ValueError(f"Unsupported timezone: {timezone_str}")

        # Create timezone object
        boot_timezone = timezone(timedelta(hours=timezone_offset))

        # Adjust the datetime object based on the timezone
        parsed_compiled_date = parsed_compiled_date.replace(tzinfo=boot_timezone)

        # Extract hours and minutes from the uptime string
        uptime_parts = uptime_str.split(', ')

        # Initialize hours and minutes
        hours = 0
        minutes = 0

        for part in uptime_parts:
            if 'hour' in part:
                hours = int(part.split(' ')[0])
            elif 'minute' in part:
                minutes = int(part.split(' ')[0])

        # Convert uptime to seconds
        uptime_seconds = hours * 3600 + minutes * 60

        # Calculate boot time
        boot_time = parsed_compiled_date - timedelta(seconds=uptime_seconds)
        boot_time_timeticks = int(boot_time.timestamp())

        # Define boot time range (e.g., +/- 100000 seconds)
        range_seconds = 1000000
        
        return boot_time_timeticks, (boot_time_timeticks - range_seconds, boot_time_timeticks + range_seconds)
    
    except Exception as e:
        log.error("Error parsing command output: {e}".format(e=e))
        return None

def get_memory_utilization_status(device):
    """
    Gets the memory utilization status of processes based on parsed outputs of 'show process memory'
    and 'show platform software status control-processor brief' commands.

    Args:
        device (obj): Device object

    Returns:
        dict: Dictionary containing PID and memory utilization status
    """
    try:
        # Execute 'show process memory' command
        process_memory_output = device.parse("show process memory")

        # Execute 'show platform software status control-processor brief' command
        control_processor_output = device.parse("show platform software status control-processor brief")
        
        # Get the total memory from 'show platform software status control-processor brief'
        total_memory = None
        for slot in control_processor_output['slot'].values():
            total_memory = slot['memory']['total'] * 1024
            break
        
        if total_memory is None:
            raise ValueError("Failed to retrieve total memory")

        # Get PID and memory utilization status
        pid_list = []
        utilization_status_list = []

        for pid, details in process_memory_output['pid'].items():
            if pid != 0:
                # Find the index dynamically
                index = next(iter(details['index'].keys()))
                holding_memory = details['index'][index]['holding']
                utilization = (holding_memory / total_memory) * 100
                status = 1 if utilization > 0.5 else 0
                pid_list.append(pid)
                utilization_status_list.append(status)

        return {'pid': pid_list, 'memory_utilization_status': utilization_status_list}

    except Exception as e:
        # Handle any exceptions and log errors
        log.error(f"Failed to retrieve memory utilization status: {e}")
        return {}

def get_port_speed_info(device):
    """
    Extracts port speed information from the parsed output of 'show interfaces status'.

    Args:
        device (`obj`): Device object.

    Returns:
        dict: A dictionary containing lists of interfaces and their corresponding port speeds.
    """
    # Define the OpenConfig prefix
    OPENCONFIG_PREFIX = 'openconfig-if-ethernet:'
    
    try:
        # Parse the command output
        out = device.parse('show interfaces status')
    except SchemaEmptyParserError as e:
        log.error(f"Command 'show interfaces status' did not return any results: {e}")
        return None

    interfaces = out.get('interfaces', {})
    interface_list = []
    port_speed_list = []

    # Extracting port speed information from the parser output
    for interface, details in interfaces.items():
        # Exclude interfaces starting with 'Ap'
        if not interface.startswith('Ap'):
            port_speed = details.get('port_speed')
            openconfig_speed = None

            # Handling port speed mappings
            if port_speed == '1000' or port_speed == 'a-1000':
                openconfig_speed = 'SPEED_1GB'
            elif port_speed == 'auto':
                openconfig_speed = 'SPEED_UNKNOWN'
            elif port_speed.startswith('a-'):
                openconfig_speed = f'SPEED_{port_speed[2:-1]}GB'
            elif port_speed.endswith('G'):
                openconfig_speed = f'SPEED_{port_speed[:-1]}GB'
            elif port_speed.isdigit():
                if port_speed == '5000':
                    openconfig_speed = 'SPEED_5GB'
                else:
                    openconfig_speed = f'SPEED_{port_speed}MB'
            
            if openconfig_speed:
                interface_list.append(interface)
                port_speed_list.append(OPENCONFIG_PREFIX + openconfig_speed)

    return {'interface': interface_list, 'port_speed': port_speed_list}

def get_cpu_instant_interval(device):
    """
    Extracts summary information from the platform status parser output.
    Args:
        device (`obj`): Device object.
    Returns:
        dict: A dictionary containing slot information including CPU utilization
        instant and interval.
    """
    try:
        # Parse the command output
        out = device.parse('show platform software status control-processor brief')
    except SchemaEmptyParserError as e:
        log.error("Command 'show platform software status control-processor brief' did not return any results: {e}".format(e=e))
        return None

    slot_info = {
        'slot': [],
        'instant': [],
        'interval': []
    }

    # Extracting slot information from the parser output
    slots = out.get('slot', {})
    total_cpus = 0
    total_idle = 0

    for slot, details in slots.items():
        # Adjust slot name format
        if '-' in slot:
            adjusted_slot = "Switch" + slot.split('-')[0]
        elif slot.startswith("rp"):
            adjusted_slot = "slot R" + slot[2:]
        else:
            adjusted_slot = slot

        # Extracting CPU details for each slot
        cpu_info = details.get('cpu', {})
        for cpu, stats in cpu_info.items():
            total_cpus += 1
            total_idle += stats.get('idle')

        # Calculate instant CPU utilization
        instant = ((total_cpus * 100) - total_idle) / total_cpus

        # Round off the instant value to the nearest integer
        instant = int(round(instant))

        # Default interval
        interval = 300000000000

        # Append values to corresponding lists in slot_info dictionary
        slot_info['slot'].append(adjusted_slot)
        slot_info['instant'].append(instant)
        slot_info['interval'].append(interval)

    return slot_info

def get_cpu_min_max_avg(device):
    """
    Extracts minimum, maximum, and average CPU utilization values.
    Args:
        device (`obj`): Device object.
    Returns:
        dict: A dictionary containing minimum, maximum, and average CPU utilization values.
    """
    instant_values = []
    slot_info = None
    for _ in range(5):
        try:
            platform_cpu_status = get_cpu_instant_interval(device)
            instant_values.extend(platform_cpu_status['instant'])  # Extend the list instead of appending
            if slot_info is None:
                slot_info = platform_cpu_status
        except Exception as e:
            log.error("Error getting CPU instant interval: {e}".format(e=e))
        time.sleep(5)  # Sleep for 5 seconds before the next iteration

    # Calculate minimum, maximum, and average based on 5 sets of instant values
    cpu_min = [min(instant_values)]
    cpu_max = [max(instant_values)]
    cpu_avg = [sum(instant_values) / len(instant_values)]

    # Append slot information to the result dictionary
    result = {'min': cpu_min, 'max': cpu_max, 'avg': cpu_avg}
    if slot_info:
        result['slot'] = slot_info['slot']

    return result

def get_platform_component_type_id_info(device):
    """
    Extracts platform component and transceiver information.
    
    Args:
        device (`obj`): Device object.
        
    Returns:
        dict: A dictionary containing platform component and transceiver information.
    """
    output = {}
    
    try:
        # Parse the command outputs
        platform_component_output = device.parse('test platform software database get-n all ios_oper/platform_component')
        transceiver_output = device.parse('test platform software database get-n all ios_oper/transceiver')

    except SchemaEmptyParserError as e:
        # Log an error message if any of the command outputs are empty
        log.error("Command output is empty: {e}".format(e=e))
        return None

    # Extract platform component information
    for index, info in platform_component_output.get('table_record_index', {}).items():
        name = info.get('cname', '')
        type_ = info.get('type', '')
        platform_info = {
            'type': type_, 
            'id': info.get('id', '')
        }
        output[name] = platform_info

    # Modify platform_info for transceivers
    for index, info in transceiver_output.get('table_record_index', {}).items():
        name = info.get('name', '')
        if name in output:
            output[name]['type'] = 'TRANSCEIVER'

    # Process type list to append appropriate prefixes
    for name, platform_info in output.items():
        type_ = platform_info['type']
        if type_ == 'CONTAINER':
            platform_info['type'] = 'cisco-xe-openconfig-platform-ext:' + type_
        elif type_ == 'MODULE':
            platform_info['type'] = 'openconfig-platform-types:' + 'FRU'
        else:
            platform_info['type'] = 'openconfig-platform-types:' + type_

    return output

def get_platform_component_temp_info(device):

    try:
        # Parse the command output
        platform_component_info = device.parse('test platform software database get-n all ios_oper/platform_component')
    except SchemaEmptyParserError as e:
        # Log an error message if the command output is empty
        log.error("Command 'test platform software database get-n all ios_oper/platform_component' did not return any results: {e}".format(e=e))
        return None

    # Transform the parsed output
    output = {}

    records = platform_component_info.get('table_record_index', {})

    for record_id, record_data in records.items():
        # Check if any of the temperature fields are present and not equal to zero
        temperature_fields = ['temp_instant', 'temp_avg', 'temp_max', 'temp_min', 'temp_interval']
        if any(record_data.get(field) and record_data.get(field) != 0 for field in temperature_fields):
            # Process severity and interval  
            severity = 'openconfig-alarm-types:' + record_data['severity'].split('OC_')[1]
            interval = int(record_data['temp_interval']) * 60000000000
            temp_avg = round(float(record_data['temp_avg']))

            cname = record_data.get('cname')
            temp_instant = record_data.get('temp_instant')

            if cname:
                output[cname] = {
                    'alarm_severity': severity,
                    'alarm_status': record_data.get('alarm_status'),
                    'alarm_threshold': record_data.get('alarm_threshold'),
                    'temp_avg': temp_avg,
                    'temp_instant': temp_instant,
                    'temp_interval': interval,
                    'temp_max': record_data.get('temp_max'),
                    'temp_min': record_data.get('temp_min')
                }

    return output

def get_platform_component_firmware_info(device):
    """
    Extracts firmware version information for platform components.
    Args:
        device (`obj`): Device object.
    Returns:
        dict: A dictionary containing platform component names and firmware version information.
    """
    output = {}

    try:
        # Parse the CLI command output
        platform_component_output = device.parse('test platform software database get-n all ios_oper/platform_component')

    except SchemaEmptyParserError as e:
        # Log an error message if the command output is empty
        log.error("Command output is empty: {e}".format(e=e))
        return None

    # Extract firmware version information from the parsed output
    for index, info in platform_component_output.get('table_record_index', {}).items():
        name = info.get('cname', '')
        firmware_ver = info.get('firmware_ver', 'NULL')
        output[name] = {
            'firmware_version': firmware_ver,
        }

    return output

def show_tech_support_platform_interface(device, file_name, interface=None, port_id=None):
    """
    Redirect the interface-specific information from the command output to a file
    Args:
        device (`obj`): Device object
        file_name (`str`): name of file to save the output in bootflash
        interface ('str`, Optional): Interface name
        port_id (`int`, Optional): Port ID of the port-channel interface
    Returns:
        Device output or None
    """
    try:
        if not interface and not port_id:
            raise ValueError("Either interface or port_id must be provided")
        elif port_id and not interface:
            device.execute(f"show tech-support platform interface port-channel {port_id} | redirect bootflash:{file_name}")
        elif interface and not port_id:
            device.execute(f"show tech-support platform interface {interface} | redirect bootflash:{file_name}")
        else:
            raise ValueError("Both interface and port_id cannot be provided")
        return None
    except SchemaEmptyParserError as e:
        log.error("Command 'show tech-support platform interface {interface}' did not return any results: {e}".format(e=e))
        return None

def show_tech_support_platform_monitor(device, file_name, session_id):
    """redirect show tech-support platform monitor for a specific session ID to a specific file in device bootflash

        Args:
            device    (`obj`): Device object
            file_name (`str`): name of file to save the output in bootflash
            session_id(`int`): <1-66>  SPAN session id
        Returns:
            None
    """
    
    log.debug(f"Redirecting the output to bootflash:{file_name}")
    try:
        device.execute(f"show tech-support platform monitor {session_id} | redirect bootflash:{file_name}")
    except SubCommandFailure as e:
        log.error(f"Failed to redirect the output to bootflash: {e}")

def get_logging_message_time(device, message):
    """ Get message time from log message using regex
        Args:
            device ('obj'): device to run on
            message ('str'): Line from show logging command
            regex ('str'): Regex to extract time from line
        Returns:
            datetime: Time extracted from message or None if parsing fails
    """    
    # Apr  8 04:18:45.753
    p0 = re.compile(r"(\*?)\s*(?P<month>\S+)\s+(?P<day>\d{1,2})\s+(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})\.(?P<millisecond>\d{3})")

    # Apr  8 04:18:45.753
    m = p0.match(message)
    if m:
        group = m.groupdict()
        hour = int(group["hour"])
        minute = int(group["minute"])
        second = int(group["second"])
        milliseconds = int(group["millisecond"])
        month = datetime.strptime(group["month"], "%b").month
        day = int(group["day"])
        year = int(group.get("year", datetime.now().year))

        return datetime(year, month, day, hour, minute, second, milliseconds)
    else:
        log.info(f"Regex did not match message: {message}")

    return None
