"""Common get info functions for platform"""

# Python
import os
import logging

# pyATS
from genie.metaparser.util.exceptions import SchemaEmptyParserError, SchemaMissingKeyError

log = logging.getLogger(__name__)

def get_file_size(device, file):

    '''
        Get file size on the device
        Args:
            device (`obj`): Device object
            file (`str`): File name
        Returns:
            file size in `int` type or None if file size is not available
    '''

    directory = ''.join([os.path.dirname(file), '/'])
    try:
        out = device.parse("dir {}".format(directory))
    except Exception as e:
        log.error("Failed to parse the directory listing due to: {}".format(str(e)))
        return None

    filename = os.path.basename(file)
    size = out.get('files',{}).get(filename, {}).get('size')
    if size:
        return int(size)
    else:
        log.error("File '{}' is not found on device".format(file))


def get_running_image(device):

    '''
        Get running image on the device
        Args:
            device (`obj`): Device object
        Returns:
            kickstart (`str`): Kickstart image
            system (`str`): System image
    '''

    try:
        out = device.parse("show version")
        kickstart = out.get('platform').get('software').get('kickstart_image_file', None)
        system = out.get('platform').get('software').get('system_image_file')
        if kickstart:
            return [kickstart.replace('///', '/'), system.replace('///', '/')]
        else:
            return [system.replace('///', '/')]
    except SchemaEmptyParserError as e:
        log.error("Command 'show version' did not return any results: {e}".format(e=e))
    except SchemaMissingKeyError as e:
        log.error("Missing key while parsing 'show version': {e}".format(e=e))
    except Exception as e:
        log.error("Failed to parse 'show version': {e}".format(e=e))
    return None


def get_available_space(device, directory='', output=None):
    """Gets available space on a given directory
        Args:
            device ('str'): Device object
            directory ('str'): directory to check spaces, if not provided it will check the
            current working directory. i.e. media:/path/to/my/dir
            output ('str'): output of dir command, if not provided execute the cmd on device to get the output
        Returns:
            space available in bytes in `int` type or None if failed to retrieve available space
    """
    try:
        dir_output = device.parse('dir {}'.format(directory), output=output)
    except Exception as e:
        log.error("Failed to parse the directory listing due to: {}".format(str(e)))
        return None

    free_space = dir_output.get('disk_free_space')
    if free_space:
        return int(free_space)
    else:
        log.error("Failed to get available space for {}".format(directory))


def get_total_space(device, directory='', output=None):
    """Gets total space on a given directory
        Args:
            device ('str'): Device object
            directory ('str'): directory to check spaces, if not provided it will check the
            current working directory. i.e. media:/path/to/my/dir
            output ('str'): output of dir command, if not provided execute the cmd on device to get the output
        Returns:
            space available in bytes in `int` type or None if failed to retrieve available space
    """
    try:
        dir_output = device.parse('dir {}'.format(directory), output=output)
    except Exception as e:
        log.error("Failed to parse the directory listing due to: {}".format(str(e)))
        return None

    return int(dir_output.get('disk_total_space'))

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

    return output.get('dir', '')

def get_platform_core(device, default_dir, output=None, keyword=['_core.']):
    '''Get the default directory of this device

        Args:
            device      (`obj`) : Device object
            default_dir (`str`) : default directory on device
            output      (`str`) : Output of `dir` command
            keyword     (`list`): List of keywords to search
        Returns:
            corefiles (`list`): List of found core files
    '''

    cmd = "dir {default_dir}//sup-active/core/".format(default_dir=default_dir)

    try:
        # sample output:
        # # dir logflash://sup-active/core/
        #   119173734    May 25 00:09:00 2017  0x101_vsh.bin_core.27380.gz
        output = device.parse(cmd, output=output)
    except SchemaEmptyParserError:
        # empty is possible. so pass instead of exception
        pass

    corefiles = []
    if output:
        for file in output.q.get_values('files'):
            for kw in keyword:
                if kw in file:
                    corefiles.append('file')

    return corefiles

def get_platform_cpu_load(device,
                         command='show processes cpu',
                         processes=None,
                         check_key='one_sec',
                         output=None):
    '''Get cpu load on device

        Args:
            device     (`obj`): Device object
            command    (`str`): Override show command
                                Default to `show processes cpu`
            processes (`list`): List of processes to check
            check_key  (`str`): Key to check in parsed output
                                Default to `one_sec`
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
            # To get process id
            # {
            #   (snip))
            #   "index": {
            #     1: {
            #       "process": "init",
            #       (snip)
            #       "one_sec": 0.0,
            pids = parsed.q.contains_key_value('process', ps_item, value_regex=True).get_values('index')
            count = len(pids)
            for pid in pids:
                cpu_load += parsed.q.contains_key_value('index', pid).get_values(check_key, 0)
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
                         check_key='one_sec',
                         output=None):
    '''Get cpu load on device

        Args:
            device     (`obj`): Device object
            command    (`str`): Override show command
                                Default to `show processes cpu`
            processes (`list`): List of processes to check
            check_key  (`str`): Key to check in parsed output
                                Default to `one_sec`
            output     (`str`): Output of show command
        Returns:
            cpu_load_dict  (`dict`): Cpu load dictionary on the device
                                     example:
                                     {
                                         'OMP': 0.0,
                                         'NAT-ROUTE': 0.0,
                                     }
    '''

    cpu_load_dict = {}

    try:
        parsed = device.parse(command, output=output)
    except SchemaEmptyParserError as e:
        log.error("Command '{cmd}' did not return any output\n{msg}".\
                  format(cmd=command, msg=str(e)))
        return None

    all_processes = parsed.q.get_values('process')

    if processes or all_processes:
        for ps_item in processes or all_processes:
            # To get process id
            # {
            #   (snip))
            #   "index": {
            #     1: {
            #       "process": "init",
            #       (snip)
            #       "one_sec": 0.0,
            indexes = parsed.q.contains_key_value('process', ps_item, value_regex=True).get_values('index')
            for index in indexes:
                process = parsed.q.contains_key_value('index', index).get_values('process', 0)
                cpu_load_dict.update({process: parsed.q.contains_key_value('index', index).get_values(check_key, 0)})

    return cpu_load_dict

def get_platform_memory_usage(device,
                              command='show processes memory',
                              processes=None,
                              check_key='all_mem_alloc',
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
                                    Default to `all_mem_alloc`
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

    memory_holding = 0
    if processes:
        for ps_item in processes:
            # To get process id
            # {
            #   'all_mem_alloc': 4646178816,
            #   'pid': {
            #     1: {
            #       'index': {
            #         1: {
            #           'mem_alloc': 188416,
            #           'mem_limit': 0,
            #           'mem_used': 4308992,
            #           'pid': 1,
            #           'process': 'init',
            #           'stack_base_ptr': 'ffffffff/ffffffff'
            #           (snip)
            pids = parsed.q.contains_key_value(
                'process', ps_item, value_regex=True).get_values('pid')
            for pid in pids:
                # use `sum` because it's possible one pid returns multiple `holding`
                memory_holding += sum(
                    parsed.q.contains_key_value('pid',
                                                pid).get_values('mem_alloc'))
        if parsed.get(check_key, 0) == 0:
            memory_usage = 0
        else:
            memory_usage = memory_holding / parsed[check_key]
    else:
        if parsed.get(check_key, 0) == 0:
            memory_usage = 0
        else:
            memory_holding += sum(parsed.q.get_values('mem_alloc'))
            memory_usage = memory_holding / parsed[check_key]

    return memory_usage * 100

def get_platform_memory_usage_detail(device,
                              command='show processes memory',
                              processes=None,
                              check_key='all_mem_alloc',
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
                                    Default to `all_mem_alloc`
            output         (`str`): Output of show command
        Returns:
            memory_usage_dict (`dict`): memory usage dict on the device (percentage)
                                        example:
                                        {
                                            'libvirtd': 0.0012294695662956926,
                                            'inotifywait': 0.0012294695662956926,
                                        }
    '''

    process = ''
    regex_items = []
    memory_usage_dict = {}
    try:
        parsed = device.parse(command, output=output)
    except SchemaEmptyParserError as e:
        log.error("Command '{cmd}' did not return any output\n{msg}".\
                  format(cmd=command, msg=str(e)))
        return None

    all_processes = parsed.q.get_values('process')
    if isinstance(processes, list):
        for item in processes:
            regex_items += parsed.q.contains_key_value('process', item, value_regex=True).get_values('process')

    if regex_items:
        processes = regex_items

    if processes or all_processes:
        for ps_item in processes or all_processes:
            # To get process id
            # {
            #   'all_mem_alloc': 4646178816,
            #   'pid': {
            #     1: {
            #       'index': {
            #         1: {
            #           'mem_alloc': 188416,
            #           'mem_limit': 0,
            #           'mem_used': 4308992,
            #           'pid': 1,
            #           'process': 'init',
            #           'stack_base_ptr': 'ffffffff/ffffffff'
            #           (snip)
            pids = parsed.q.contains_key_value(
                'process', ps_item, value_regex=True).get_values('pid')
            memory_holding = 0
            for pid in pids:
                # use `sum` because it's possible one pid returns multiple `holding`
                memory_holding += sum(
                    parsed.q.contains_key_value('pid',
                                                pid).get_values('mem_alloc'))

            if parsed.get(check_key, 0) == 0:
                memory_usage = 0
            else:
                memory_usage = memory_holding / parsed[check_key]

            memory_usage_dict.update({ps_item: memory_usage*100})
 
    return memory_usage_dict