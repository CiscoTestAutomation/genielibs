# Python
import os
import re
import logging

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
    '''Get file size on the device
        Args:
            device (`obj`): Device object
            file (`str`): File name
            output ('str'): Output of 'dir' command
                            if not provided, executes the cmd on device
        Returns:
            file size in `int` type or None if file size is not available
    '''

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
    '''Get running image on the device
        Args:
            device (`obj`): Device object
        Returns:
            Image or None
    '''

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
    '''Gets available space on a given directory
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
    '''

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
    '''Gets total space on a given directory
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
    '''

    try:
        dir_output = device.parse('dir {}'.format(directory), output=output)
    except Exception as e:
        log.error("Failed to parse the directory listing due to: {}".\
                  format(str(e)))
        return None
    else:
        return int(Dq(dir_output).get_values('bytes_total')[0])


def get_boot_variables(device, boot_var, output=None):
    '''Get current or next-reload boot variables on the device
        Args:
            device (`obj`): Device object
            boot_var (`str`): Type of boot variable to return to caller
            output (`str`): output from show boot
        Returns:
            List of boot images or []
    '''

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
    '''Get current config-register setting on the device
        Args:
            device (`obj`): Device object
            next_reload (`bool`): Determine if returning next-reload value
        Returns:
            config-register value or None
    '''

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
    '''Get the default directory of this device

        Args:
            device (`obj`): Device object
            output (`str`): Output of `dir` command
        Returns:
            default_dir (`str`): Default directory of the system
    '''

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
    '''Get the default directory of this device

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
    '''
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
    '''Get logging messages

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
    '''
    return device.api.health_logging(command, files, keywords, output, num_of_logs, health=False)

def get_platform_cpu_load(device,
                          command='show processes cpu',
                          processes=None,
                          check_key='five_sec_cpu',
                          output=None):
    '''Get cpu load on device

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
    '''
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
    '''Get cpu load on device

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
    '''
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
    '''Get memory usage on device

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
    '''

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
