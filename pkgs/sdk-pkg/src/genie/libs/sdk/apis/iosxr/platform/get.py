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
    bytes_free = int(re.search(r'\d+', free_bytes[0]).group(0))

    if bytes_free:
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
    all_corefiles = []
    dirs = []
    stby_dirs = []

    if isinstance(default_dir, str):
        dirs = [default_dir]
    elif isinstance(default_dir, list):
        dirs = default_dir
    else:
        raise Exception(
            "'default_dir {dd} is not string or list".format(dd=default_dir))

    # check if device is HA
    if device.is_ha:
        log.info('Detected device is HA configuration.')
        log.info('Checking location for standby RP.')
        red_out = device.parse('show redundancy summary')
        standby_location = red_out.q.get_values('standby_node',
                                                0).split('(')[0]
        for storage in dirs:
            # if missing, adding `/`. harddisk:/dumper -> harddisk:/dumper/
            if storage[-1] != '/':
                storage += '/'
            stby_dirs.append('{dd} location {sl}'.format(dd=storage,
                                                         sl=standby_location))

    # add standby location `stby_dirs` to main `dirs`
    dirs.extend(stby_dirs)

    # convert from device name to device object
    if remote_device:
        if remote_device in device.testbed.devices:
            remote_device = device.testbed.devices[remote_device]
        else:
            raise Exception(
                'remote device {rd} was not found.'.format(rd=remote_device))

        # check connected_alias for remote_device
        remote_device_alias = [
            i for i in remote_device.api.get_connected_alias().keys()
        ]

    for storage in dirs:
        corefiles = []
        log.info('Checking on {s}'.format(s=storage))

        cmd = "dir {s}".format(s=storage)

        parsed = ''
        try:
            # sample output:
            # #dir harddisk:/dumper/
            # Fri Sep 15 18:14:57.449 UTC
            #
            # Directory of harddisk:/dumper
            #
            # 1769728     -rw-  2353427     Thu Sep 14 06:34:54 2017  first.dsc_174.by. wdsysmon.sparse.20170914-063449.node0_0_CPU0.x86.Z
            # 1769952     -rw-  7814        Thu Sep 14 06:34:54 2017  first.dsc_174.by. wdsysmon.sparse.20170914-063449.node0_0_CPU0.x86.txt
            # 1770176     -rw-  73415       Thu Sep 14 06:34:56 2017  first.dsc_174.by. wdsysmon.sparse.20170914-063449.node0_0_CPU0.x86.cpu_info.Z
            parsed = device.parse(cmd, output=output)
        except SchemaEmptyParserError:
            # empty is possible. so pass instead of exception
            pass

        if parsed:
            location_alias = parsed.q.get_values('dir_name', 0)
            for file in parsed.q.get_values('files'):
                for kw in keyword:
                    if kw in file:
                        # corefiles in current storage
                        log.debug('core file {f} is found'.format(f=file))
                        corefiles.append(file)
                        # corefiles in all storages
                        all_corefiles.append(file)

        # copy core file to remote device
        if remote_device:
            for corefile in corefiles:
                copy_success = False
                log.info('Copying {s} to remote device {rd}'.format(
                    s=corefile, rd=remote_device.name))

                if not (remote_device and remote_path):
                    log.warn(
                        '`remote_device` or/and `remote_path` are missing')
                    return len(dirs) if num_of_cores else dirs
                local_path = "{la}/{fn}".format(la=location_alias, fn=corefile)
                if not device.api.scp(local_path=local_path,
                                              remote_path=remote_path,
                                              remote_device=remote_device.name,
                                              remote_via=remote_via,
                                              vrf=vrf):
                    log.warn(
                        'SCP has failed to copy core file to remote device {rd}'
                        .format(rd=remote_device.name))
                    return len(dirs) if num_of_cores else dirs
                else:
                    copy_success = True

                # TODO: waiting for enhancement of decoder
                # # decode core file
                # if decode:

                #     # connect to remote_device if not connected
                #     if not remote_device_alias:
                #         # if no connected alias, connect
                #         try:
                #             remote_device.connect()
                #         except Exception as e:
                #             log.warn(
                #                 "Remote device {d} was not connected and failed to  connect   : {e}"
                #                 .format(d=remote_device.name, e=e))
                #             return len(dirs) if num_of_cores else dirs

                #     try:
                #         # archive decode output
                #         if archive:
                #             fullpath = corefile if remote_path in corefile else remote_path   + '/'+ corefile
                #             decode_output = remote_device.api.decode_core(
                #                 corefile="{fp}".format(fp=fullpath),
                #                 timeout=decode_timeout)
                #             with open(
                #                     '{folder}/{fn}'.format(
                #                         folder=runtime.directory,
                #                         fn='core_decode_{file}'.format(
                #                             file=corefile)), 'w') as f:
                #                 print(decode_output, file=f)
                #                 log.info(
                #                     'Saved decode output as archive: {folder}/{fn}'
                #                     .format(folder=runtime.directory,
                #                             fn='core_decode_{file}'.format(
                #                                 file=corefile)))
                #     except Exception as e:
                #         log.warning(
                #             'decode core file is failed : {e}'.format(e=e))

                # delete core files
                if delete_core and copy_success:
                    try:
                        log.info(
                            'Deleting copied file {lp}.'.format(lp=local_path))
                        device.execute(
                            'delete /noprompt {lp}'.format(lp=local_path))
                        log.info('{lp} was successfully deleted'.format(
                            lp=local_path))
                    except Exception as e:
                        log.warn(
                            'deleting core files on {s} failed. {e}'.format(
                                s=storage, e=e))
                        return []

    if num_of_cores:
        return len(all_corefiles)
    return all_corefiles


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
            # To get process id based on check_key
            # {
            #   (snip))
            #   "index": {
            #     "1": {
            #       "process": "sleep",
            #       (snip)
            #       "one_min_cpu": 0.0,
            indexes = parsed.q.contains_key_value(
                'process', ps_item, value_regex=True).get_values('index')
            for index in indexes:
                process = parsed.q.contains_key_value('index', index).get_values('process', 0)
                cpu_load_dict.update({
                    process:
                    parsed.q.contains_key_value('index',
                                                index).get_values(check_key, 0)
                })

    return cpu_load_dict


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
    regex_items = []
    memory_usage_dict = {}
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

    all_processes = parsed.q.get_values('process')
    if isinstance(processes, list):
        for item in processes:
            regex_items += parsed.q.contains_key_value(
                'process', item, value_regex=True).get_values('process')

    if regex_items:
        processes = regex_items
    if processes or all_processes:
        for ps_item in (sorted(processes) if isinstance(processes, list) else
                        processes) or (sorted(all_processes) if isinstance(
                            all_processes, list) else all_processes):
            memory_holding = 0
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
            memory_holding = 0
            for pid in pids:
                for dynamic in parsed.q.contains_key_value(
                        'jid', pid).get_values(check_key):
                    # accumulating because it's possible one pid returns multiple `holding`
                    memory_holding += device.api.unit_convert(dynamic)

            memory_usage = 0 if physical_total == 0 else memory_holding / physical_total
            memory_usage_dict.update({ps_item: memory_usage * 100})

    return memory_usage_dict


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
    # check keywords and create strings for `include` option
    kw = ''
    if isinstance(keywords, list):
        kw = '|'.join(keywords)
        kw = '"{kw}"'.format(kw=kw)

    try:
        if kw:
            parsed = device.parse('show logging | include {kw}'.format(kw=kw),
                                  output=output)
        else:
            parsed = device.parse('show logging', output=output)
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