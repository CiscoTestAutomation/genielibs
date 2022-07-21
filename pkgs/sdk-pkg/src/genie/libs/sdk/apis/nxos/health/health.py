"""Common health functions for nxos"""

# Python
import re
import logging

# pyATS
from pyats.easypy import runtime

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def health_cpu(device,
               command='show processes cpu',
               processes=None,
               check_key='one_sec',
               check_key_total=None,
               output=None,
               add_total=False,
               timeout=None,
               health=True):
    '''Get cpu load on device

        Args:
            device     (`obj`): Device object
            command    (`str`): Override show command
                                Default to `show processes cpu`
            processes (`list`): List of processes to check
            check_key  (`str`): Key to check in parsed output
                                Default to `one_sec`
            check_key_total (`str`): N/A
            add_total (`bool`): If True, add total cpu load
            output     (`str`): Output of show command
            timeout    (`int`): Timeout(secs). Defaults to None
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
        parsed = device.parse(command, output=output, timeout=timeout)
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
        health_data['health_data'].append({
            'process': 'ALL_PROCESSES',
            'value': float(parsed['user_percent']+parsed['kernel_percent'])
        })
        for k, v in cpu_load_dict.items():
            health_data['health_data'].append({'process': k, 'value': v})
        return health_data

    if add_total:
        cpu_load_dict = {'ALL_PROCESSES': float(parsed['user_percent']+parsed['kernel_percent'])}

    return cpu_load_dict


def health_memory(device,
                  command='top -n 1',
                  processes=None,
                  check_key=None,
                  check_key_total=None,
                  output=None,
                  add_total=False,
                  timeout=None,
                  threshold=None,
                  health=True):
    '''Get memory usage on device

        Args:
            device         (`obj`): Device object
            command        (`str`): Override show command
                                    Default to `show processes memory`
            processes     (`list`): List of processes to check
                                    If both processes and check_key are given,
                                    processes are preferred.
            check_key      (`str`): N/A. not used for NXOS
            check_key_total (`str`): N/A. not used for NXOS
            add_total    (`bool`): If True, add total memory usage
            output         (`str`): Output of show command
            timeout        (`int`): Timeout(secs). Defaults to None
            threshold      (`int`): N/A
        Returns:
            memory_usage_dict (`dict`): memory usage dict on the device (percentage)
                                        example:
                                        {
                                            "health_data": [
                                                {
                                                    "process": "/opt/mtx/bin/grpc -i 2626 -I",
                                                    "value": 0.0,
                                                },
                                                {
                                                    "process": "/sbin/klogd -2 -x -c 1",
                                                    "value": 0.0,
                                                }
                                            ]
                                        }
    '''

    regex_items = []
    memory_usage_dict = {}
    try:
        parsed = device.parse(command, output=output, timeout=timeout)
    except SchemaEmptyParserError as e:
        log.error("Command '{cmd}' did not return any output\n{msg}".\
                  format(cmd=command, msg=str(e)))
        return None

    total_res = sum(parsed.q.get_values('res'))

    all_processes = parsed.q.get_values('command')

    total_memory_usage = 0
    if processes or all_processes:
        for ps_item in processes or all_processes:
            # To get process(command)
            # {
            #   'pid': {
            #     7329: {
            #       'stat': 'Ssl',
            #       'majflt': 157,
            #       'trs': 0,
            #       'rss': 217428,
            #       'vsz': 1052196,
            #       'mem_percent': 3.7,
            #       'command': '/opt/mtx/bin/grpc -i 2626 -I',
            #       'tty': '?',
            #       'time': '00:01:43'
            #     }
            pids = parsed.q.contains_key_value(
                'command', ps_item, value_regex=True).get_values('pids')
            process_total_res = 0
            process_total_shr = 0
            for pid in pids:
                process_total_res += parsed['pids'][pid]['res']
                process_total_shr += parsed['pids'][pid]['shr']
            memory_usage_percent = ((process_total_res - process_total_shr) / total_res) * 100
            memory_usage_dict[ps_item] = memory_usage_percent
            total_memory_usage += memory_usage_percent

    # if health is True, change the dict
    # from:
    # memory_usage_dict = {
    #   "/opt/mtx/bin/grpc -i 2626 -I": 0.0,
    #   "/sbin/klogd -2 -x -c 1": 0.0,
    # }
    # to:
    # memory_usage_dict = {
    #   "health_data": [
    #     {
    #       "process": "/opt/mtx/bin/grpc -i 2626 -I",
    #       "value": 0.0,
    #     },
    #     {
    #       "process": "/sbin/klogd -2 -x -c 1",
    #       "value": 0.0,
    #     }
    #   ]
    # }
    if health:
        health_data = {}
        health_data.setdefault('health_data', [])
        health_data['health_data'].append({
            'process': 'ALL_PROCESSES',
            'value': total_memory_usage
        })
        for k, v in memory_usage_dict.items():
            health_data['health_data'].append({'process': k, 'value': v})
        return health_data

    if add_total:
        memory_usage_dict.update({'ALL_PROCESSES': total_memory_usage})

    return memory_usage_dict


def health_logging(device,
                   command='show logging logfile',
                   files=None,
                   keywords=['traceback', 'Traceback', 'TRACEBACK'],
                   output=None,
                   num_of_logs=False,
                   clear_log=False,
                   health=True):
    '''Get logging messages
        Args:
            device    (`obj`): Device object
            command   (`str`): show command. Default to 'show logging logfile'
            files    (`list`): Not applicable on this platform
            keywords (`list`): List of keywords to match.
                               Default to ['traceback', 'Traceback', 'TRACEBACK']
            output    (`str`): Output of show command. Default to None
            num_of_logs (`bool`): flag to return number of log messages
                                  Default to False
            clear_log (`bool`): flag to clear logging message
                                Default to False
            health (`bool`): wheather return health_data format or not
                             Default to True
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
    if clear_log:
        device.api.clear_logging()

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
                protocol='scp',
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
            protocol (`str`): protocol for copy. Default to scp
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
    # store core file name which is successfully copied
    copied_files = []
    # store found core file location
    dirs = []
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

    # convert from device name to device object
    fileutils = False
    if remote_device and protocol != 'http':
        if remote_device in device.testbed.testbed.servers:
            fileutils = True
        elif remote_device in device.testbed.devices:
            remote_device = device.testbed.devices[remote_device]
            # check connected_alias for remote_device
            remote_device_alias = [
                device_alias for device_alias in
                remote_device.api.get_connected_alias().keys()
            ]
        else:
            log.warn(
                'remote device {rd} was not found.'.format(rd=remote_device))

    # initialize health_corefiles again to store with core file name
    if health:
        health_corefiles = {}

    # in case of HTTP, will use FileUtils
    if protocol == 'http':
        fileutils = True

    # copy core file to remote device
    if remote_device or protocol == 'http':
        for corefile in dirs:
            if fileutils:
                log.info('Copying {s} via FileUtils'.format(
                    s=corefile))
            else:
                log.info('Copying {s} to remote device {rd} via API'.format(
                    s=corefile, rd=remote_device.name))

            if not fileutils and not (remote_device and remote_path):
                log.warn('`remote_device` or/and `remote_path` are missing')
                return len(dirs) if num_of_cores else dirs
            local_path = "core://{cf}".format(cf=corefile)
            # execute by FileUtils
            if fileutils:
                try:
                    # if protocol is 'http', will use FileUtils only with local_path
                    # proxy of device will be detected automatically. if proxy,
                    # proxy will be used as remote_device
                    if protocol == 'http':
                        output = device.api.copy_from_device(protocol=protocol,
                                                             remote_path=remote_path,
                                                             local_path=local_path,
                                                             vrf=vrf)
                    else:
                        output = device.api.copy_from_device(protocol=protocol,
                                                             server=remote_device,
                                                             remote_path=remote_path,
                                                             local_path=local_path,
                                                             vrf=vrf)
                    copied_files = list(
                        set(
                            re.findall(
                                r"(?P<filename>\d\S+)\s+\d+%\s+\d+\S+\s+\d+\.\d+\S+\s+",
                                output)))
                    # cannot see filename with FTP, so use local_path
                    if not copied_files:
                        copied_files = [local_path]
                except Exception as e:
                    log.exception(
                        '{p} has failed to copy core file to remote device {rd}: {e}'
                        .format(p=protocol, rd=remote_device, e=e))
            # execute by API
            if not fileutils and (remote_device and remote_path):
                if protocol == 'scp':
                    copied_files = device.api.scp(local_path=local_path,
                                                  remote_path=remote_path,
                                                  remote_device=remote_device.name,
                                                  remote_via=remote_via,
                                                  vrf=vrf,
                                                  return_filename=True)
                    if not copied_files:
                        log.warn(
                            'SCP has failed to copy core file to remote device {rd}.'
                            .format(rd=remote_device.name))
                else:
                    log.error('protocol {p} is not implemented by API'.format(
                        p=protocol))

            if health:
                health_corefiles.setdefault(copied_files[0], {})
            # decode core file
            if decode:
                if protocol != 'http':
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
                                health_corefiles[core].setdefault(
                                    'decode', decode_output)
                            # archive decode output
                            if archive:
                                with open(
                                        '{folder}/{fn}'.format(
                                            folder=runtime.directory,
                                            fn='core_decode_{file}'.format(file=core)),
                                        'w') as f:
                                    print(decode_output, file=f)
                                    log.info(
                                        'Saved decode output as archive:{folder}/{fn}'.
                                        format(
                                            folder=runtime.directory,
                                            fn='core_decode_{file}'.format(file=core)))
                        except Exception as e:
                            log.warning('decode core file is failed : {e}'.format(e=e))
                else:
                    # decode is not supported by http because http transfer output
                    # doesn't have file name. so don't know file name
                    log.warning('decode is not supported with protocol `http`.')
            # delete core files
            if delete_core:
                module = corefile.split('/')[0]
                pid = corefile.split('/')[1]
                try:
                    log.info(
                        'Deleting copied file on module-{m}/core/*{p}*.'.format(
                            m=module, p=pid))
                    device.execute(
                        'delete logflash://module-{m}/core/*{p}* no-prompt'.format(
                            m=module, p=pid))
                    log.info(
                        'Core files on module-{m}/core/*{p}* was successfully deleted'
                        .format(m=module, p=pid))
                except Exception as e:
                    log.warn(
                        'deleting core files on module-{m}/core/*{p} failed. {e}'.
                        format(m=module, p=pid, e=e))
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
        health_data = {}
        health_data.setdefault('health_data', {})
        health_data['health_data'].setdefault('num_of_cores', len(dirs))
        health_data['health_data'].setdefault('corefiles', [])
        for filename in health_corefiles:
            if 'decode' in health_corefiles[filename]:
                health_data['health_data']['corefiles'].append({
                    'filename':
                    filename,
                    'decode':
                    health_corefiles[filename]['decode']
                })
            else:
                health_data['health_data']['corefiles'].append(
                    {'filename': filename})
        return health_data

    if num_of_cores:
        return len(dirs)
    return dirs
