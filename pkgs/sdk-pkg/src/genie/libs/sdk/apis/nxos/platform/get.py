"""Common get info functions for platform"""

# Python
import os
import logging
import re

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
    return device.api.health_core(default_dir=default_dir,
                                  output=output,
                                  keyword=keyword,
                                  num_of_cores=num_of_cores,
                                  decode=decode,
                                  decode_timeout=decode_timeout,
                                  remote_device=remote_device,
                                  remote_path=remote_path,
                                  remote_via=remote_via,
                                  vrf=vrf,
                                  archive=archive,
                                  delete_core=delete_core,
                                  health=False)


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
    return device.api.health_cpu(command=command,
                                 processes=processes,
                                 check_key=check_key,
                                 output=output,
                                 health=False)


def get_platform_memory_usage(device,
                              command='show processes memory',
                              processes=None,
                              check_key=None,
                              output=None):
    '''Get memory usage on device

        Args:
            device         (`obj`): Device object
            command        (`str`): Override show command
                                    Default to `show processes memory`
            processes     (`list`): List of processes to check
                                    If both processes and check_key are given,
                                    processes are preferred.
            check_key      (`str`): N/A. Not used for NXOS
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
                                     check_key=None,
                                     output=None):
    '''Get memory usage on device

        Args:
            device         (`obj`): Device object
            command        (`str`): Override show command
                                    Default to `show processes memory`
            processes     (`list`): List of processes to check
                                    If both processes and check_key are given,
                                    processes are preferred.
            check_key      (`str`): N/A. Not used for NXOS
            output         (`str`): Output of show command
        Returns:
            memory_usage_dict (`dict`): memory usage dict on the device (percentage)
                                        example:
                                        {
                                            'libvirtd': 0.0012294695662956926,
                                            'inotifywait': 0.0012294695662956926,
                                        }
    '''
    return device.api.health_memory(command=command,
                                    processes=processes,
                                    check_key=check_key,
                                    output=output,
                                    health=False)


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
    return device.api.health_logging(command=command,
                                     files=files,
                                     keywords=keywords,
                                     output=output,
                                     num_of_logs=num_of_logs,
                                     health=False)


def get_software_version(device, return_tuple:bool=False):
    """Get software version of device

    Args:
        device (obj): Device object
        return_tuple (bool, optional): Should the return be a tuple.
            Defaults to False.

    Returns:
        (str, tuple): Device software version as a str or tuple
    """
    try:
        out = device.parse('show version')
    except SubCommandFailure:
        log.error('Could not get device version information')
        return None

    # Version is the first token of software/system_version when split with ' '
    ver:str = out.q.contains('software').get_values('system_version', 0) \
        .split(' ')[0]
    if return_tuple :
        # Tokenize system version into a list with delimiters '.', '(' and ')'
        ver:list = [ch for ch in re.split(r'\.|\(|\)', ver) if ch != '']
        # Convert to int whereever possible
        for i in range(len(ver)):
            try:
                ver[i] = int(ver[i])
            except ValueError:
                pass
        return tuple(ver)
    else:
        return ver

def get_standby_supervisor_slot(device):
    """Gets the standby supervisor slot number
    Args:
        device (obj): Device object
    Returns:
        int: standby supervisor slot number if present and in ha-standby state, 0 otherwise 
    """
    try:
        out = device.parse('show module')
    except SubCommandFailure as e:
        log.info('Failed to get slot model: {e}'.format(e=e))
        return None
 
    return out.q.contains('.*Supervisor Module', 
                          regex=True).\
                    contains_key_value('status', 
                                       'ha-standby', 
                                       value_regex=True).\
                    get_values('rp')


def get_active_supervisor_slot(device):
    """Gets the active supervisor slot number
    Args:
        device (obj): Device object
    Returns:
        int: active supervisor slot number 
    """

    try:
        out = device.parse('show module')
    except SubCommandFailure as e:
        log.info('Failed to get slot model: {e}'.format(e=e))
        return None
 
    return out.q.contains('.*Supervisor Module', 
                          regex=True).\
                    contains_key_value('status', 
                                       'active', 
                                       value_regex=True).\
                    get_values('rp')


def get_slots_by_state(device, status='ok|active|ha-standby'):
    """Gets the module list which match the given state/status
    Args:
        device (obj): Device object
        status (str): Module status to get the slot/module number. Default to ok|active|ha-standby state
    Returns:
        dict: Dictionary mapped with slot number to state/status
    """
        
    try:
        out = device.parse('show module')
    except SubCommandFailure as e:
        log.info('Failed to get slot model: {e}'.format(e=e))
        return None
    
    slots = Dq(out).contains('status').\
                            contains_key_value('status',
                                                   status,
                                                   value_regex=True).\
                            get_values('lc')
    
    slots.extend(Dq(out).contains('status').\
                            contains_key_value('status',
                                                   status,
                                                   value_regex=True).\
                            get_values('rp'))
    
    slots.extend(Dq(out).contains('status').\
                            contains_key_value('status',
                                                   status,
                                                   value_regex=True).\
                            get_values('lem'))
    
    return slots 
    

def get_fm_slots(device, status='ok'):
    """Gets the list of fabric slot which are in given state
    Args:
        device (obj): Device object
        status (str): FM status to get the fm list. Default to 'ok'
    Returns:
        list: Fabric Module list which matches the given state/status
    """

    try:
        out = device.parse('show module')
    except SubCommandFailure as e:
        log.info('Failed to get slot model: {e}'.format(e=e))
        return None
    
    return out.q.contains('.* Fabric Module', 
                          regex=True, level=-1).\
                    contains_key_value('status', 
                                   status,
                                   value_regex=True).\
                    get_values('lc')


def get_lc_slots(device, status='ok'):
    """Gets the list of line card slots (but not Fabric/Supervisor/controller) which are in given state
    Args:
        device (obj): Device object
        status (str): Linde card state to retrive. Default to 'ok'
    Returns:
        list: Line Module list which matches the given state/status
    """
    slots = []
    try:
        out = device.parse('show module')
    except SubCommandFailure as e:
        log.info('Failed to get slot model: {e}'.format(e=e))
        return None
 
    slots = out.q.not_contains('.* Fabric Module', 
                          regex=True, level=2).\
                    contains_key_value('status', 
                                   status,
                                   value_regex=True).\
                    get_values('lc')
    
    slots.extend(Dq(out).contains('status').\
                            contains_key_value('status',
                                               status,value_regex=True).\
                            get_values('lem')) 


    return slots 


def get_current_boot_image(device):
    """Gets the current boot image name from show boot cli
    Args:
        device (obj): Device object
        
    Returns:
        str: current boot image name or empty
    """
    try:
        out = device.parse('show boot')
    except SubCommandFailure as e:
        log.info('Failed to get slot model: {e}'.format(e=e))
        return None
 
    image = out.q.contains('current_boot_variable').get_values('system_variable')[0]
    
    return image.strip('bootflash:/') if image else ''

def get_next_reload_boot_image(device):
    """Gets the next reload boot image from show boot cli
    Args:
        device (obj): Device object
        
    Returns:
        str: next reload boot image or empty
    """
    try:
        out = device.parse('show boot')
    except SubCommandFailure as e:
        log.info('Failed to get slot model: {e}'.format(e=e))
        return None
 
    image = out.q.contains('next_reload_boot_variable').get_values('system_variable')[0]
    
    return image.strip('bootflash:/') if image else ''

def get_standby_systemcontroller_slot(device):
    """Gets the standby systemcontroller slot number
    Args:
        device (obj): Device object
    Returns:
        int: standby systemcontroller slot number if present and in ha-standby state, 0 otherwise
    """
    try:
        out = device.parse('show module')
    except SubCommandFailure as e:
        log.error('Failed to get slot model: {e}'.format(e=e))
        raise Exception("Failed to get slot model") from e

    return out.q.contains('.*System Controller',
                          regex=True).\
                    contains_key_value('status',
                                       'standby',
                                       value_regex=True).\
                    get_values('lc')


def get_active_systemcontroller_slot(device):
    """Gets the active systemcontroller slot number
    Args:
        device (obj): Device object
    Returns:
        int: active systemcontroller slot number
    """

    try:
        out = device.parse('show module')
    except SubCommandFailure as e:
        log.error('Failed to get slot model: {e}'.format(e=e))
        raise Exception("Failed to get slot model") from e

    return out.q.contains('.*System Controller',
                          regex=True).\
                    contains_key_value('status',
                                       'active',
                                       value_regex=True).\
                    get_values('lc')