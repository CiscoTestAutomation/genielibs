"""Common health functions for platform"""

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


def health_cpu(device,
               command='show processes cpu',
               processes=None,
               check_key='one_sec',
               output=None,
               health=True):
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
                                            "health_data": [
                                                {
                                                    "process": "OMP",
                                                    "value": 0.0,
                                                },
                                                {
                                                    "process": "NAT-ROUTE",
                                                    "value": 0.0,
                                                }
                                            ]
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
            indexes = parsed.q.contains_key_value(
                'process', ps_item, value_regex=True).get_values('index')
            for index in indexes:
                process = parsed.q.contains_key_value('index',
                                                      index).get_values(
                                                          'process', 0)
                cpu_load_dict.update({
                    process:
                    parsed.q.contains_key_value('index', index).get_values(
                        check_key, 0)
                })

    # if health is True, change the dict
    # from:
    # cpu_load_dict = {
    #   "OMP": 0.0,
    #   "NAT-ROUTE": 0.0,
    # }
    # to:
    # cpu_load_dict = {
    #   "health_data": [
    #     {
    #       "process": "OMP",
    #       "value": 0.0,
    #     },
    #     {
    #       "process": "NAT-ROUTE",
    #       "value": 0.0,
    #     }
    #   ]
    # }
    if health:
        health_data = {}
        health_data.setdefault('health_data', [])
        for k, v in cpu_load_dict.items():
            health_data['health_data'].append({'process': k, 'value': v})
        cpu_load_dict = health_data

    return cpu_load_dict


def health_memory(device,
                  command='show processes memory',
                  processes=None,
                  check_key='all_mem_alloc',
                  output=None,
                  health=True):
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
                                            "health_data": [
                                                {
                                                    "process": "libvirtd",
                                                    "value": 0.0012294695662956926,
                                                },
                                                {
                                                    "process": "inotifywait",
                                                    "value": 0.0012294695662956926,
                                                }
                                            ]
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
            regex_items += parsed.q.contains_key_value(
                'process', item, value_regex=True).get_values('process')

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

            memory_usage_dict.update({ps_item: memory_usage * 100})

    # if health is True, change the dict
    # from:
    # memory_usage_dict = {
    #   "libvirtd": 0.0012294695662956926,
    #   "inotifywait": 0.0012294695662956926,
    # }
    # to:
    # memory_usage_dict = {
    #   "health_data": [
    #     {
    #       "process": "libvirtd",
    #       "value": 0.0012294695662956926,
    #     },
    #     {
    #       "process": "inotifywait",
    #       "value": 0.0012294695662956926,
    #     }
    #   ]
    # }
    if health:
        health_data = {}
        health_data.setdefault('health_data', [])
        for k, v in memory_usage_dict.items():
            health_data['health_data'].append({'process': k, 'value': v})
        memory_usage_dict = health_data

    return memory_usage_dict


def health_logging(device,
                   command='show logging logfile',
                   files=None,
                   keywords=None,
                   output=None,
                   num_of_logs=False,
                   health=True):
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
            logs     (`dict`): return health_data format.
                               ex.)
                                {
                                    "health_data": {
                                        "num_of_logs": 1,
                                        "logs": [
                                            {
                                                "line": "-Traceback= D667B8 D66F04 41463C 40FFF8 411834 423A6C A6E428 A64EF8 (EEHYP_CS_801-1)",
                                                "decode": "<decode output>" # Optional
                                            }
                                        ]
                                    }
                                }
    '''

    # check keywords and create strings for `include` option
    kw = ''
    if isinstance(keywords, list):
        kw = '|'.join(keywords)

    try:
        parsed = device.parse(command, include=kw)
    except SchemaEmptyParserError:
        parsed = {}

    # Get value of 'logs' if it exists else '[]'
    logs = parsed.setdefault('logs', [])

    if health:
        health_data = {}
        health_data.setdefault('health_data', {})
        health_data['health_data'].setdefault('num_of_logs', len(logs))
        health_logs = health_data['health_data'].setdefault('logs', [])
        for item in logs:
            health_logs.append({'line': item})
        return health_data

    if num_of_logs:
        return len(logs)

    return logs


def health_core(device,
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
                delete_core=False,
                health=True):
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
            all_corefiles (`dict`): return health_data format.
                                    ex.)
                                    {
                                        "health_data": {
                                            "num_of_cores": 1,
                                            "core_files": [
                                                {
                                                    "filename": "asr-MIB-1_RP_1_nginx_23178_20210317-175351-UTC.core.gz",
                                                    "decode": """
                                                        <decode output>
                                                    """
                                                }
                                            ]
                                        }
                                    }
    '''
    # store found core file name
    all_corefiles = []
    # store core file name which is successfully copied
    copied_files = []
    # store found core file location
    dirs = []
    health_data = {}
    health_corefiles = {}
    remote_device_alias = []

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
                if health:
                    health_corefiles.setdefault(loc, {})

    log.debug('dirs: {dirs}'.format(dirs=dirs))

    if remote_device:
        # convert from device name to device object
        if remote_device in device.testbed.devices:
            remote_device = device.testbed.devices[remote_device]
            # check connected_alias for remote_device
            remote_device_alias = [
                i for i in remote_device.api.get_connected_alias().keys()
            ]
        else:
            log.warn(
                'remote device {rd} was not found.'.format(rd=remote_device))

    corefiles = []

    # initialize health_corefiles again to store with core file name
    if health:
        health_corefiles = {}
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
            log.warn('SCP has failed to copy core file to remote device {rd}.'.
                     format(rd=remote_device.name))
        if health:
            health_corefiles.setdefault(copied_files[0], {})
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
                    if health:
                        health_corefiles[core].setdefault('decode', decode_output)
                    # archive decode output
                    if archive:
                        with open(
                                '{folder}/{fn}'.format(
                                    folder=runtime.directory,
                                    fn='core_decode_{file}'.format(file=core)),
                                'w') as f:
                            print(decode_output, file=f)
                            log.info(
                                'Saved decode output as archive:{folder}/{fn}'
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

    if health:
        health_data.setdefault('health_data', {})
        health_data['health_data'].setdefault('num_of_cores', len(dirs))
        health_data['health_data'].setdefault('corefiles', [])
        for filename in health_corefiles:
            if 'decode' in health_corefiles[filename]:
                health_data['health_data']['corefiles'].append({'filename': filename, 'decode': health_corefiles[filename]['decode']})
            else:
                health_data['health_data']['corefiles'].append({'filename': filename})
        return health_data

    if num_of_cores:
        return len(dirs)
    return dirs