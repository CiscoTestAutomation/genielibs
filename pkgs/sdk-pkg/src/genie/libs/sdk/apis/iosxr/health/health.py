'''Common get info functions for iosxr'''
# Python
import logging

# pyATS
from pyats.easypy import runtime

# Genie
from genie.metaparser.util.exceptions import (SchemaEmptyParserError,
                                              InvalidCommandError)

log = logging.getLogger(__name__)


def health_cpu(device,
               command='show processes cpu',
               processes=None,
               check_key='one_min_cpu',
               check_key_total='one_min_cpu',
               output=None,
               add_total=False,
               health=True):
    '''Get cpu load on device

        Args:
            device     (`obj`): Device object
            command    (`str`): Override show command
                                Default to `show processes cpu`
            processes (`list`): List of processes to check
                                Default to None
            check_key  (`str`): Key to check in parsed output
                                Default to `one_min_cpu`
            check_key_total (`str`): Key to check in parsed output
                                     for Total. Default to `one_min_cpu`
            add_total    (`bool`): If True, add total cpu load
            output     (`str`): Output of show command
                                Default to None
        Returns:
            cpu_load_dict  (`dict`): Cpu load dictionary on the device
                                     Example:
                                        {
                                            "health_data": [
                                                {
                                                    "process": "netconf",
                                                    "value": 0.0,
                                                },
                                                {
                                                    "process": "bgp",
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

    if (processes or all_processes):
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
    #   "netconf": 0.0,
    #   "bgp": 0.0,
    # }
    # to:
    # cpu_load_dict = {
    #   "health_data": [
    #     {
    #       "process": "netconf",
    #       "value": 0.0,
    #     },
    #     {
    #       "process": "bgp",
    #       "value": 0.0,
    #     }
    #   ]
    # }
    total_load = float(
        parsed.q.not_contains('index').get_values(check_key_total, 0))
    if health:
        health_data = {}
        health_data.setdefault('health_data', [])
        if add_total:
            health_data['health_data'].append({
                'process': 'ALL_PROCESSES',
                'value': total_load
            })
        for k, v in cpu_load_dict.items():
            health_data['health_data'].append({'process': k, 'value': v})
        return health_data

    if add_total:
        cpu_load_dict.update({'ALL_PROCESSES': total_load})

    return cpu_load_dict


def health_memory(device,
                  command='show processes memory detail',
                  processes=None,
                  check_key='dynamic',
                  output=None,
                  add_total=False,
                  health=True):
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
            add_total    (`bool`): If True, add total memory usage
            output         (`str`): Output of show command
                                    Deault to None
        Returns:
            memory_usage_dict (`dict`): memory usage dict on the device (percentage)
                                        example:
                                        {
                                            "health_data": [
                                                {
                                                    "process": "OMP",
                                                    "value": 0.0012294695662956926,
                                                },
                                                {
                                                    "process": "NAT-ROUTE",
                                                    "value": 0.0012294695662956926,
                                                }
                                            ]
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
    physical_total = sum(
        device.api.unit_convert(phy_tot)
        for phy_tot in parsed.q.get_values('phy_tot'))

    all_processes = parsed.q.get_values('process')
    if isinstance(processes, list):
        for item in processes:
            regex_items += parsed.q.contains_key_value(
                'process', item, value_regex=True).get_values('process')

    if regex_items:
        processes = regex_items

    total_memory_usage = 0
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
            memory_usage_percent = memory_usage * 100
            memory_usage_dict.update({ps_item: memory_usage_percent})
            if add_total:
                total_memory_usage += memory_usage_percent

    # if health is True, change the dict
    # from:
    # memory_usage_dict = {
    #   "OMP": 0.0012294695662956926,
    #   "NAT-ROUTE": 0.0012294695662956926,
    # }
    # to:
    # memory_usage_dict = {
    #   "health_data": [
    #     {
    #       "process": "OMP",
    #       "value": 0.0012294695662956926,
    #     },
    #     {
    #       "process": "NAT-ROUTE",
    #       "value": 0.0012294695662956926,
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
                   command='show logging',
                   files=None,
                   keywords=['traceback', 'Traceback', 'TRACEBACK'],
                   output=None,
                   num_of_logs=False,
                   clear_log=False,
                   health=True):
    '''Get logging messages

        Args:
            device    (`obj`): Device object
            command   (`str`): N/A
            files    (`list`): Not applicable on this platform
            keywords (`list`): List of keywords to match
                               Default to ['traceback', 'Traceback', 'TRACEBACK']
            output    (`str`): Output of show command
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
                                                "decode": "<decode output>", # Optional
                                            }
                                        ]
                                    }
                                }
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
                default_dir=['/misc/scratch/core', 'harddisk:/dumper/'],
                output=None,
                keyword=['.x86.', '.core.'],
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
    all_corefiles = []
    dirs = []
    stby_dirs = []
    health_corefiles = {}

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
    fileutils = False
    if remote_device:
        if remote_device in device.testbed.testbed.servers:
            fileutils = True
        elif remote_device in device.testbed.devices:
            remote_device = device.testbed.devices[remote_device]
        else:
            raise Exception(
                'remote device {rd} was not found.'.format(rd=remote_device))

        # check connected_alias for remote_device
        if not fileutils:
            remote_device_alias = [
                device_alias for device_alias in
                remote_device.api.get_connected_alias().keys()
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
        except InvalidCommandError as e:
            if health != True:
                raise InvalidCommandError(e)
        if parsed:
            location_alias = parsed.q.get_values('dir_name', 0)
            for file in parsed.q.get_values('files'):
                for kw in keyword:
                    if kw in file and file not in all_corefiles:
                        # corefiles in current storage
                        log.debug('core file {f} is found'.format(f=file))
                        corefiles.append(file)
                        # corefiles in all storages
                        all_corefiles.append(file)
                        # add health_corefiles for health_data
                        if health:
                            health_corefiles.setdefault(file, {})

        # in case of HTTP, will use FileUtils
        if protocol == 'http':
            fileutils = True

        # copy core file to remote device
        if remote_device or protocol == 'http':
            for corefile in corefiles:
                copy_success = False
                if fileutils:
                    log.info('Copying {s} via FileUtils'.
                             format(s=corefile))
                else:
                    log.info(
                        'Copying {s} to remote device {rd} via API'.format(
                            s=corefile, rd=remote_device.name))

                if not fileutils and (not remote_device or not remote_path):
                    log.warn(
                        '`remote_device` or/and `remote_path` are missing')
                local_path = "{la}/{fn}".format(la=location_alias, fn=corefile)
                # execute by FileUtils
                if fileutils:
                    try:
                        # if protocol is 'http', will use FileUtils only with local_path
                        # proxy of device will be detected automatically. if proxy,
                        # proxy will be used as remote_device
                        if protocol == 'http':
                            device.api.copy_from_device(local_path, vrf=vrf)
                        else:
                            device.api.copy_from_device(protocol=protocol,
                                                        server=remote_device,
                                                        remote_path=remote_path,
                                                        local_path=local_path,
                                                        vrf=vrf)
                        copy_success = True
                    except Exception as e:
                        log.warn(
                            '{p} has failed to copy core file to remote device {rd}: {e}'
                            .format(p=protocol, rd=remote_device, e=e))
                # execute by API
                if not fileutils and (remote_device and remote_path):
                    if protocol == 'scp':
                        if not device.api.scp(local_path=local_path,
                                              remote_path=remote_path,
                                              remote_device=remote_device.name,
                                              remote_via=remote_via,
                                              vrf=vrf):
                            log.warn(
                                'SCP has failed to copy core file to remote device {rd}'
                                .format(rd=remote_device.name))
                        else:
                            copy_success = True
                    else:
                        log.error(
                            'protocol {p} is not implemented by API'.format(
                                p=protocol))

                # TODO: waiting for enhancement of decoder
                # # decode core file
                # if decode and copy_success:

                #     # connect to remote_device if not connected
                #     if not remote_device_alias:
                #         # if no connected alias, connect
                #         try:
                #             remote_device.connect()
                #         except Exception as e:
                #             log.warn(
                #                 "Remote device {d} was not connected and failed to connect : {e}"
                #                 .format(d=remote_device.name, e=e))
                #             return len(dirs) if num_of_cores else dirs

                #     try:
                #         # archive decode output
                #         if archive:
                #             fullpath = corefile if remote_path in corefile else remote_path + '/'+ corefile
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

    if health:
        health_data = {}
        health_data.setdefault('health_data', {})
        health_data['health_data'].setdefault('num_of_cores',
                                              len(all_corefiles))
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
        return len(all_corefiles)
    return all_corefiles
