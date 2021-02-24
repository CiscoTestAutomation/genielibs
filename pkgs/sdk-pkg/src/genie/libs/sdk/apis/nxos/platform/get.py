"""Common get info functions for platform"""

# Python
import os
import logging

# pyATS
from pyats.easypy import runtime

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError, SchemaMissingKeyError
from genie.utils import Dq

# Unicon
from unicon.core.errors import SubCommandFailure

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


def get_platform_core(device,
                      default_dir=None,
                      output=None,
                      keyword=['_core.'],
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
            default_dir (`str` or `list`) : N/A. location will be identified
                                            from show cores command
            output      (`str`) : Output of `dir` command. Default to None
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
    # store found core file name
    all_corefiles = []
    # store core file name which is successfully copied
    copied_files = []
    # store found core file location
    dirs = []

    parsed = {}
    try:
        parsed = device.parse('show cores', output=output)
        # example:
        # {
        #     "date": {
        #         "2020-08-20 05:49:09": {
        #             "pid": {
        #                 18234: {
        #                     "instance": 1,
        #                     "module": 1,
        #                     "process_name": "bgp-65000",
        #                     "vdc": 1
        #                 }
        #             }
        #         }
        #     }
        # }
    except SchemaEmptyParserError:
        # empty is possible. so pass instead of exception
        pass

    if parsed:
        for entry in parsed['date']:
            for pid in parsed['date'][entry]['pid'].keys():
                loc = '{module}/{pid}/{instance}'.format(
                    module=str(parsed['date'][entry]['pid'][pid]['module']),
                    pid=str(pid),
                    instance=str(
                        parsed['date'][entry]['pid'][pid]['instance']))
                dirs.append(loc)

    log.debug('dirs: {dirs}'.format(dirs=dirs))

    if remote_device:
        # convert from device name to device object
        if remote_device in device.testbed.devices:
            remote_device = device.testbed.devices[remote_device]
        else:
            log.warn(
                'remote device {rd} was not found.'.format(rd=remote_device))
            return len(dirs) if num_of_cores else dirs
        # check connected_alias for remote_device
        remote_device_alias = [
            i for i in remote_device.api.get_connected_alias().keys()
        ]

    corefiles = []

    # copy core file to remote device
    for corefile in dirs:
        log.info('Copying {s} to remote device {rd}'.format(s=corefile,
                                                            rd=remote_device))
        if not (remote_device and remote_path):
            log.warn('`remote_device` or/and `remote_path` are missing')
            return len(dirs) if num_of_cores else dirs
        local_path = "core://{cf}".format(cf=corefile)
        copied_files = device.api.scp(local_path=local_path,
                                      remote_path=remote_path,
                                      remote_device=remote_device.name,
                                      remote_via=remote_via,
                                      vrf=vrf,
                                      return_filename=True)
        if not copied_files:
            log.warn('SCP has failed to copy core file to remote device {rd}'.
                     format(rd=remote_device.name))
            return len(dirs) if num_of_cores else dirs
        # decode core file
        if decode:
            # connect to remote_device if not connected
            if not remote_device_alias:
                # if no connected alias, connect
                try:
                    remote_device.connect()
                except Exception as e:
                    log.warn(
                        "Remote device {d} was not connected and failed to connect : {e}"
                        .format(d=remote_device.name, e=e))
                    return len(dirs) if num_of_cores else dirs
            for core in copied_files:
                try:
                    fullpath = "{rp}/{core}".format(rp=remote_path, core=core)
                    decode_output = remote_device.api.analyze_core_by_ucd(
                        core_file="{fp}".format(fp=fullpath),
                        timeout=decode_timeout)
                    # archive decode output
                    if archive:
                        with open(
                                '{folder}/{fn}'.format(
                                    folder=runtime.directory,
                                    fn='core_decode_{file}'.format(file=core)),
                                'w') as f:
                            print(decode_output, file=f)
                            log.info(
                                'Saved decode output as archive: {folder}/{fn}'
                                .format(
                                    folder=runtime.directory,
                                    fn='core_decode_{file}'.format(file=core)))
                except Exception as e:
                    log.warning('decode core file is failed : {e}'.format(e=e))
        # delete core files
        if delete_core:
            for corefile in dirs:
                module = corefile.split('/')[0]
                try:
                    log.info(
                        'Deleting copied file on module-{m}.'.format(m=module))
                    device.execute(
                        'delete logflash://module-{m}/core/* no-prompt'.format(
                            m=module))
                    log.info(
                        'Core files on module-{m} was successfully deleted'.
                        format(m=module))
                except Exception as e:
                    log.warn(
                        'deleting core files on module-{m} failed. {e}'.format(
                            m=module, e=e))
                    return []

    # clear show cores history
    if copied_files:
        try:
            device.execute('clear cores')
        except Exception as e:
            log.warn('Failed to execute `clear cores`.'.format(
                rd=remote_device.name))
            return len(dirs) if num_of_cores else dirs
    else:
        log.info('No core file was copied. So `clear cores` was not executed.')

    if num_of_cores:
        return len(dirs)
    return dirs


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


def get_slot_model(device):
    """Gets the model name of all modules

    Args:
        device (obj): Device object
        slot (str, optional): Module slot to get. Defaults to None.

    Returns:
        dict: Dictionary mapped from slot number to model
    """

    try:
        out = device.parse('show module')
    except SubCommandFailure as e:
        log.info('Failed to get slot model: {e}'.format(e=e))
        return None

    return {key: Dq(val).get_values('model', 0) for key, val in out.get('slot', {}).get('rp', {}).items()}

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


def get_platform_logging(device,
                         command='show logging logfile',
                         files=None,
                         keywords=None,
                         output=None,
                         num_of_logs=False):
    '''Get logging messages
        Args:
            device    (`obj`): Device object
            command   (`str`): show command. Default to 'show logging logfile'
            files    (`list`): Not applicable on this platform
            keywords (`list`): List of keywords to match. Default to None
            output    (`str`): Output of show command. Default to None
            num_of_logs (`bool`): flag to return number of log messages
                                  Default to False
        Returns:
            logs     (`list` or `int`): list of logging messages
                                        OR or number of core files if num_of_logs=True
    '''

    # check keywords and create strings for `include` option
    kw = ''
    if isinstance(keywords, list):
        kw = '|'.join(keywords)

    try:
        parsed = device.parse(command, include=kw)
    except SchemaEmptyParserError:
        if num_of_logs:
            return 0
        else:
            return []

    # Get value of 'logs' if it exists else '[]'
    logs = parsed.setdefault('logs', [])

    if num_of_logs:
        return len(logs)

    return logs
