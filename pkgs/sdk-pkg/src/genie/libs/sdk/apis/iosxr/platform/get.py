'''Common get info functions for platform'''
# Python
import re
import logging
import os

# pyATS
from pyats.easypy import runtime

# Genie
from genie.utils import Dq
from genie.metaparser.util.exceptions import SchemaEmptyParserError,\
                                             SchemaMissingKeyError

log = logging.getLogger(__name__)

def get_module_info(device, module, key='sn'):
    ''' Get a module's information

        Args:
            device (`obj`): Device object
            module (`str`): Module name
            key (`str`): Key name
        Returns:
            field (`str`): Field value
    '''
    log.info("Getting module '{}' key '{}' from {}".format(
             module, key, device.name))
    try:
        out = device.parse('show inventory')
    except Exception as e:
        log.error("Failed to parse 'show inventory' on {}:\n{}"
            .format(device.name, e))
        raise Exception from e

    if module in out['module_name']:
        if key in out['module_name'][module]:
            return out['module_name'][module][key]
        else:
            raise Exception("module '{}' doesn't have a key named '{}'"
                    .format(module, key))
    else:
        raise Exception("Can not find a module name '{}' on device {}"
                .format(module, device.name))

def get_running_image(device):
    '''Get running image on the device
        Args:
            device (`obj`): Device object
        Returns:
            Image or None
    '''

    try:
        # Execute 'show version'
        output = device.parse("show version")
    except SchemaEmptyParserError as e:
        log.error("Command 'show version' did not return any results: {e}".format(e=e))
    except SchemaMissingKeyError as e:
        log.error("Missing key while parsing 'show version': {e}".format(e=e))
    except Exception as e:
        log.error("Failed to parse 'show version': {e}".format(e=e))
    else:
        return output.get('image')
    return None

def get_config_register(device):
    '''Get config-regsiter on the device
        Args:
            device (`obj`): Device object
        Returns:
            config-register or None
    '''

    try:
        # Execute 'show version'
        output = device.parse("show version")
    except SchemaEmptyParserError as e:
        log.error("Command 'show version' did not return any results: {e}".format(e=e))
    except SchemaMissingKeyError as e:
        log.error("Missing key while parsing 'show version': {e}".format(e=e))
    except Exception as e:
        log.error("Failed to parse 'show version': {e}".format(e=e))
    else:
        return output.get('config_register')
    return None

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
    except SchemaEmptyParserError as e:
        log.error("Command 'dir {}' did not return any results: {e}".format(directory,e=e))
    except SchemaMissingKeyError as e:
        log.error("Missing key while parsing 'dir {}': {e}".format(directory,e=e))
    except Exception as e:
        log.error("Failed to parse the directory listing due to: {}".\
                  format(str(e)))
        return None

    size = Dq(dir_output).contains(filename).get_values('size')
    if size:
        return int(size[0])
    else:
        log.error("File '{}' is not found on device".format(file))

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
    except SchemaEmptyParserError as e:
        log.error(
            "Command 'dir {}' did not return any results: {e}".format(directory, e=e))
    except SchemaMissingKeyError as e:
        log.error("Missing key while parsing 'dir {}': {e}".format(directory, e=e))
    except Exception as e:
        log.error("Failed to parse the directory listing due to: {}".\
                  format(str(e)))
        return None

    free_bytes = Dq(dir_output).get_values(key='total_free_bytes')
    reg = re.search(r'(\d+)\s*(\S+)?', free_bytes[0])
    
    if reg:
        if len(reg.groups()) == 2:
            if reg.group(2) == 'kbytes':
                bytes_free = int(reg.group(1))*1000
            else:
                bytes_free = reg.group(1)
        else:
            bytes_free = reg.group(1)
        return bytes_free
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
        bytes_in_total = Dq(dir_output).get_values(key='total_bytes')
        total_bytes = int(re.search(r'\d+', bytes_in_total[0]).group(0))
        return total_bytes

def get_current_active_pies(device):

    '''Gets the current active pies on a device

        Args:
            device (`obj`): Device object

        Returns:
            List of active pies on the device
    '''

    log.info("Getting current active pies on device {}".format(device.name))

    try:
        out = device.parse("show install active summary")
    except SchemaEmptyParserError:
        out = {}

    # Trim out mini package as thats the image, not the pie
    regex = re.compile(r'.*mini.*')

    return [i for i in out.get('active_packages', []) if not regex.match(i)]

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

    default_dir = output.setdefault('dir', {}).get('dir_name', '')

    return default_dir


def get_platform_core(device,
                      default_dir,
                      output=None,
                      keyword=['.x86.'],
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
            default_dir (`str` or `list`) : default directory where core is generated 
                                            on device
                                            ex.) `harddisk:/dumper`
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
    return device.api.health_core(default_dir,
                                  output,
                                  keyword,
                                  num_of_cores,
                                  decode,
                                  decode_timeout,
                                  remote_device,
                                  remote_path,
                                  remote_via,
                                  vrf,
                                  archive,
                                  delete_core,
                                  health=False)


def get_platform_cpu_load(device,
                          command='show processes cpu',
                          processes=None,
                          check_key='one_min_cpu',
                          output=None):
    '''Get cpu load on device

        Args:
            device     (`obj`): Device object
            command    (`str`): Override show command
                                Default to `show processes cpu`
            processes (`list`): List of processes to check
                                Default to None
            check_key  (`str`): Key to check in parsed output
                                Default to `one_min_cpu`
            output     (`str`): Output of show command
                                Default to None
        Returns:
            cpu_load   (`int`): Cpu load (5 mins average by default) on the device (percentage)
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
            #   "index": {
            #     "1": {
            #       "process": "sleep",
            #       (snip)
            #       "one_min_cpu": 0.0,
            pids = parsed.q.contains_key_value(
                'process', ps_item, value_regex=True).get_values('index')
            count = len(pids)
            for pid in pids:
                cpu_load += parsed.q.contains_key_value('index',
                                                        pid).get_values(
                                                            check_key, 0)
        if count == 0:
            cpu_load = 0
        else:
            cpu_load /= count
    else:
        for location in parsed['location']:
            cpu_load = float(parsed['location'][location][check_key])

    return float(cpu_load)


def get_platform_cpu_load_detail(device,
                                 command='show processes cpu',
                                 processes=None,
                                 check_key='one_min_cpu',
                                 output=None):
    '''Get cpu load on device

        Args:
            device     (`obj`): Device object
            command    (`str`): Override show command
                                Default to `show processes cpu`
            processes (`list`): List of processes to check
                                Default to None
            check_key  (`str`): Key to check in parsed output
                                Default to `one_min_cpu`
            output     (`str`): Output of show command
                                Default to None
        Returns:
            cpu_load_dict  (`dict`): Cpu load dictionary on the device
                                     example:
                                     {
                                         'netconf': 0.0,
                                         'bgp': 0.0,
                                     }
    '''
    return device.api.health_cpu(command, processes, check_key, output, health=False)


def get_platform_memory_usage(device,
                              command='show processes memory detail',
                              processes=None,
                              check_key='dynamic',
                              output=None):
    '''Get memory usage on device

        Args:
            device         (`obj`): Device object
            command        (`str`): Override show command
                                    Default to `show processes memory`
            processes     (`list`): List of processes to check
                                    If both processes and check_key are given,
                                    processes are preferred.
                                    Default to None
            check_key      (`str`): Key to check in parsed output
                                    Default to 'dynamic'
            output         (`str`): Output of show command
                                    Default to None
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

    # get all `phy_tot` and calculate the total
    physical_total = 0
    for phy_tot in parsed.q.get_values('phy_tot'):
        physical_total += device.api.unit_convert(phy_tot)

    if processes:
        count = 0
        memory_holding = 0
        for ps_item in processes:
            # To get job id based on check_key
            # {
            #   "jid": {
            #     "1114": {
            #       "index": {
            #         "1": {
            #           "jid": 1114,
            #           "text": "10M",
            #           "data": "1059M",
            #           "stack": "136K",
            #           "dynamic": "44M",
            #           "dyn_limit": "2048M",
            #           "shm_tot": "132M",
            #           "phy_tot": "197M",
            #           "process": "emsd"
            #         }
            #       }
            #     },
            pids = parsed.q.contains_key_value(
                'process', ps_item, value_regex=True).get_values('jid')
            count = len(pids)
            for pid in pids:
                for dynamic in parsed.q.contains_key_value(
                        'jid', pid).get_values(check_key):
                    # accumulating because it's possible one pid returns multiple `holding`
                    memory_holding += device.api.unit_convert(dynamic)

        memory_usage = 0 if physical_total == 0 else memory_holding / physical_total
    else:
        dynamic_total = 0
        # get all `dynamic` and calculate the total
        for dynamic in parsed.q.get_values(check_key):
            dynamic_total += device.api.unit_convert(dynamic)
        memory_usage = dynamic_total / physical_total

    return float(memory_usage * 100)


def get_platform_memory_usage_detail(device,
                                     command='show processes memory detail',
                                     processes=None,
                                     check_key='dynamic',
                                     output=None):
    '''Get memory usage on device

        Args:
            device         (`obj`): Device object
            command        (`str`): Override show command
                                    Default to `show processes memory`
            processes     (`list`): List of processes to check
                                    If both processes and check_key are given,
                                    processes are preferred.
                                    Default to None
            check_key      (`str`): Key to check in parsed output
                                    Default to `dynamic`
            output         (`str`): Output of show command
                                    Deault to None
        Returns:
            memory_usage_dict (`dict`): memory usage dict on the device (percentage)
                                        example:
                                        {
                                            'OMP': 0.0012294695662956926,
                                            'NAT-ROUTE': 0.0012294695662956926,
                                        }
    '''
    return device.api.health_memory(command, processes, check_key, output, health=False)


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