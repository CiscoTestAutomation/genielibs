# Python
import re
import logging

# pyATS
from pyats.easypy import runtime

# Genie
from genie.metaparser.util.exceptions import (SchemaEmptyParserError,
                                              InvalidCommandError)
from genie.libs.parser.iosxe.show_logging import ShowLogging
from genie.utils import Dq


# Logger
log = logging.getLogger(__name__)


def health_cpu(device,
               command=['show processes cpu sorted | exclude 0.00%', 'show processes cpu platform sorted | exclude 0%'],
               processes=None,
               check_key='five_sec_cpu',
               check_key_total='five_sec_cpu_total',
               output=None,
               add_total=False,
               timeout=None,
               health=True):
    '''Get cpu load on device

        Args:
            device     (`obj`): Device object
            command    (`str`) or list(`str`): Override show commands
                                Default to `show processes cpu sorted` and `show processes cpu platform sorted`
            processes (`list`): List of processes to check
                                if not specified, will return one ALL_PROCESSES
                                with total cpu load
            check_key  (`str`): Key to check in parsed output
                                Default to `five_sec_cpu`
            check_key_total (`str`): Key to check in parsed output for Total
                                     Default to `five_sec_cpu_total`
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
    parsed_output = []
    # Check if the command is a list if its not make it a list
    if not isinstance(command, list):
        command = [command]
    # loop through the list of commands and add the parsed output to parsed_output
    for cmd in command:
        try:
            parsed = device.parse(cmd, output=output, timeout=timeout)
            parsed_output.append(parsed)
        except SchemaEmptyParserError as e:
            log.error(f"Command '{cmd}' did not return any output\n{e}")
        except InvalidCommandError as e:
            log.warning(f"Command '{cmd}' is not supported on the device {device.name}")
    if not parsed_output:
        return None

    if processes:
        for ps_item in processes:
            for output in parsed_output:
            # To get process id based on check_key
            # {
            #   (snip))
            #   "sort": {
            #     "1": {
            #       "process": "Chunk Manager",
            #       (snip)
            #       "five_sec_cpu": 0.0,
                indexes = Dq(output).contains_key_value(
                    'process', ps_item, value_regex=True).get_values('sort')
                for index in indexes:
                    if output['sort'][index]['process'] not in cpu_load_dict:
                        process = output['sort'][index]['process']
                    else:
                        process = output['sort'][index]['process'] + '_1'
                    cpu_load_dict.update({
                        process:
                        output['sort'][index][check_key]
                    })
    # if health is True, change the dict
    # from:
    # cpu_load_dict = {
    #   "BGP": 10.0,
    #   "OSPF": 20.0,
    # }
    # to:
    # cpu_load_dict = {
    #   "health_data": [
    #     {
    #       "process": "BGP",
    #       "value": 10.0,
    #     },
    #     {
    #       "process": "OSPF",
    #       "value": 20.0,
    #     }
    #   ]
    # }
    # if we have more than one parser we use the one with biggest value of the the 2 commands for the check_key_total
    if len(parsed_output) == 2 and parsed_output[1].get('cpu_utilization', {}).get(check_key_total):
        total = max(float(parsed_output[0][check_key_total]), float(parsed_output[1]['cpu_utilization'][check_key_total]))
    else:
        total = float(parsed_output[0][check_key_total])
    if health:
        health_data = {}
        health_data.setdefault('health_data', [])
        if add_total:
            health_data['health_data'].append({
                'process':
                'ALL_PROCESSES',
                'value':
                total
            })
        for k, v in cpu_load_dict.items():
            health_data['health_data'].append({'process': k, 'value': v})
        return health_data

    if add_total:
        cpu_load_dict.update({'ALL_PROCESSES': total})

    return cpu_load_dict


def health_memory(device,
                  command='show processes memory | section ^Processor',
                  processes=None,
                  check_key='processor_pool',
                  output=None,
                  add_total=False,
                  timeout=None,
                  threshold=90,
                  health=True):
    '''Get memory usage on device. Threshold can be passed as argument.
       Check memory usage from header of show command first, then in case
       the usage exceeds threshold, capture all the show output for detail.

        Args:
            device         (`obj`): Device object
            command        (`str`): Override show command
                                    Default to `show processes memory`
            processes     (`list`): List of processes to check
                                    If both processes and check_key are given,
                                    processes are preferred.
            check_key      (`str`): Key to check in parsed output
                                    Default to `processor_pool`
            add_total    (`bool`): If True, add total memory usage
            output         (`str`): Output of show command
            timeout       (`int`): Timeout(secs). Defaults to None
            threshold     (`int`): Threshold(%) of memory usage
                                   Defaults to 90
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
    threshold_exceed = False

    try:
        parsed = device.parse(command, output=output, timeout=timeout)
    except SchemaEmptyParserError as e:
        log.error("Command '{cmd}' did not return any output\n{msg}".\
                  format(cmd=command, msg=str(e)))
        return None

    # default command
    default_command = 'show processes memory | section ^Processor'

    # check if total usage exceeds threshold or not
    if command == default_command and (parsed[check_key]['used'] / parsed[check_key]['total'])*100 > threshold:
        threshold_exceed = True

    # get each of processes usage only when exceeding threshold
    if threshold_exceed or command != default_command:

        try:
            parsed = device.parse("show processes memory", output=output, timeout=timeout)
        except SchemaEmptyParserError as e:
            log.error("Command '{cmd}' did not return any output\n{msg}".\
                      format(cmd=command, msg=str(e)))
            return None

        if isinstance(processes, list):
            for item in processes:
                regex_items += parsed.q.contains_key_value(
                    'process', item, value_regex=True).get_values('process')

        if regex_items:
            processes = regex_items

        if processes:
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
                pids = []
                p = re.compile(ps_item.replace('*', r'\*'))
                if 'pid' in parsed:
                    for pid, pid_value in parsed['pid'].items():
                        for index_value in pid_value['index'].values():
                            m = p.match(index_value['process'])
                            if m and index_value['process'] == ps_item:
                                pids.append(pid)

                    memory_holding = 0
                    for pid in pids:
                        # use `sum` because it's possible one pid returns multiple `holding`
                        for idx in parsed['pid'][pid]['index']:
                            if parsed['pid'][pid]['index'][idx]['process'] == ps_item:
                                memory_holding += parsed['pid'][pid]['index'][idx][
                                    'holding']

                if parsed.get(check_key, {}).get('total', 0) == 0:
                    memory_usage = 0
                else:
                    try:
                        memory_usage = memory_holding / parsed[check_key]['total']
                    except Exception:
                        memory_usage = parsed[check_key]['used'] / parsed[check_key]['total']

                memory_usage_dict.update({ps_item: memory_usage * 100})

    # if health is True, change the dict
    # from:
    # memory_usage_dict = {
    #   "BGP": 10.0,
    #   "OSPF": 20.0,
    # }
    # to:
    # memory_usage_dict = {
    #   "health_data": [
    #     {
    #       "process": "BGP",
    #       "value": 10.0,
    #     },
    #     {
    #       "process": "OSPF",
    #       "value": 20.0,
    #     }
    #   ]
    # }
    if health:
        health_data = {}
        health_data.setdefault('health_data', [])
        if add_total:
            health_data['health_data'].append({
                'process': 'ALL_PROCESSES',
                'value': (parsed[check_key]['used'] / parsed[check_key]['total']) * 100
            })
        for k, v in memory_usage_dict.items():
            health_data['health_data'].append({'process': k, 'value': v})
        return health_data

    if add_total:
        memory_usage_dict.update({
            'ALL_PROCESSES':
            (parsed[check_key]['used'] / parsed[check_key]['total']) * 100
        })

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
                                       "lines": [
                                            "-Traceback= D667B8 D66F04 41463C 40FFF8 411834 423A6C A6E428 A64EF8 (EEHYP_CS_801-1)",
                                       ]
                                   }
                               }
    '''
    # check keywords and create strings for `include` option
    kw = ''
    if isinstance(keywords, list):
        kw = '|'.join(keywords)

    obj = ShowLogging(device=device)

    try:
        parsed = obj.parse(include=kw, output=output)
    except SchemaEmptyParserError:
        parsed = {}
    if clear_log:
        device.api.clear_logging()

    # Get value of 'logs' if it exists else '[]'
    logs = parsed.setdefault('logs', [])

    if health:
        if hasattr(runtime, 'health_data') and runtime.health_data is not None:
            log.debug(f'runtime health data {runtime.health_data}')
            runtime.health_data.setdefault(device.name, runtime.synchro.dict())
            runtime.health_data[device.name].setdefault('logging', {})
            runtime_health_data = runtime.health_data[device.name]['logging']
        else:
            runtime_health_data = {}

        existing_log_count = runtime_health_data.get('num_of_logs') or 0
        log_count = len(logs)

        if log_count > 0 and log_count >= existing_log_count:
            new_log_count = log_count - existing_log_count
        elif log_count:
            new_log_count = log_count
        else:
            new_log_count = 0

        runtime_health_data['num_of_logs'] = new_log_count
        runtime_health_data.setdefault('lines', logs)
        if new_log_count:
            log.warning(f'Found {new_log_count} new log messages')

        if hasattr(runtime, 'health_data'):
            runtime.health_data[device.name].setdefault('logging', {})
            runtime.health_data[device.name]['logging'] = runtime_health_data
            log.debug(f'runtime health data {runtime.health_data}')
        return {'health_data': runtime_health_data}

    if num_of_logs:
        return len(logs)

    return logs

def health_core(device,
                default_dir=['bootflash:/core/', 'harddisk:/core/'],
                output=None,
                keyword=['.core.gz', '.tar.gz'],
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
                health=True,
                **kwargs):
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
            protocol (`str`): protocol for copy. Default to scp
            vrf (`str`): use vrf where scp find route to remote device
                                 Default to None
            archive     (`bool`): flag to save the decode output as file in archive
                                  Defaults to False
            delete_core (`bool`): flag to delete core files only when copying to
                                  remove_device is successfully done
                                  Defaults to False
            health (`bool`): wheather return health_data format or not
                             Default to True
            ### CISCO INTERNAL ###
            decode      (`bool`): flag to enable for decoding core
                                  copy core file to remote_server and decode on remote_server
            decode_timeout (`int`): timeout to execute decode script
                                    Default to 300

        Returns:
            health_data (`dict`): return health_data format.
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
        for storage in dirs:
            stby_dirs.append('stby-{dd}'.format(dd=storage))

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
        log.info('Checking on {storage}'.format(storage=storage))

        # if missing, adding `/`. bootflash:/core -> bootflash:/core/
        if storage[-1] != '/':
            storage += '/'
        cmd = "dir {storage}".format(storage=storage)

        parsed = ''
        try:
            # sample output:
            # #dir bootflash:core
            # Directory of bootflash:/core/
            #
            # 64899  -rw-           501904  Aug 28 2015 10:16:28 +00:00  RP_0_vman_23519_1440756987.core.gz
            parsed = device.parse(cmd, output=output)
        except SchemaEmptyParserError:
            # empty is possible and so pass instead of exception
            pass
        except InvalidCommandError as e:
            if health != True:
                raise InvalidCommandError(e)
        if parsed:
            for file in parsed.q.get_values('files'):
                for kw in keyword:
                    if kw in file:
                        # corefiles in current storage
                        log.debug(
                            'core file {file} is found'.format(file=file))
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
                    log.info('Copying {corefile} via FileUtils'.format(
                        corefile=corefile))
                else:
                    log.info(
                        'Copying {corefile} to remote device {rd} via API'.
                        format(corefile=corefile, rd=remote_device.name))
                if not fileutils and (not remote_device or not remote_path):
                    log.warn(
                        '`remote_device` or/and `remote_path` are missing')
                local_path = "{lp}{fn}".format(lp=storage, fn=corefile)
                # execute by FileUtils
                if fileutils:
                    try:
                        # if protocol is 'http', will use FileUtils only with local_path
                        # proxy of device will be detected automatically. if proxy,
                        # proxy will be used as remote_device
                        if protocol == 'http':
                            device.api.copy_from_device(local_path)
                        else:
                            device.api.copy_from_device(protocol=protocol,
                                                        server=remote_device,
                                                        remote_path=remote_path,
                                                        local_path=local_path,
                                                        vrf=vrf)

                        copy_success = True
                    except Exception as e:
                        log.warn(
                            '{protocol} has failed to copy core file to remote device {rd}: {e}'
                            .format(protocol=protocol, rd=remote_device, e=e))
                # execute by API
                if not fileutils and (remote_device and remote_path):
                    if protocol == 'scp':
                        if not device.api.scp(local_path=local_path,
                                              remote_path=remote_path,
                                              remote_device=remote_device.name,
                                              remote_via=remote_via,
                                              vrf=vrf):
                            log.warn(
                                'scp has failed to copy core file to remote device {rd}'
                                .format(rd=remote_device.name))
                        else:
                            copy_success = True
                    else:
                        log.error(
                            'protocol {protocol} is not implemented by API'.
                            format(protocol=protocol))

                # decode core file
                if decode and copy_success:

                    cores = []

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

                    # extract system-report
                    if '.tar.gz' in corefile:
                        extracted_files = remote_device.api.extract_tar_gz(
                            path=remote_path, files=[corefile])
                        # find core file in extracted files from system report
                        cores = [
                            extracted_file
                            for extracted_file in extracted_files
                            if '.core.gz' in extracted_file
                        ]
                        if not cores:
                            log.warning(
                                'No core file was found in system-report {sr}'.
                                format(sr=corefile))

                    if not cores and '.tar.gz' not in corefile:
                        cores = [corefile]

                    for core in cores:
                        try:
                            # archive decode output
                            if archive:
                                fullpath = core if remote_path in core else remote_path + '/' + core
                                decode_output = remote_device.api.decode_core(
                                    corefile="{fp}".format(fp=fullpath),
                                    timeout=decode_timeout)
                                with open(
                                        '{folder}/{fn}'.format(
                                            folder=runtime.directory,
                                            fn='core_decode_{file}'.format(
                                                file=corefile)), 'w') as f:
                                    print(decode_output, file=f)
                                    log.info(
                                        'Saved decode output as archive: {folder}/{fn}'
                                        .format(folder=runtime.directory,
                                                fn='core_decode_{file}'.format(
                                                    file=corefile)))
                                    if health:
                                        health_corefiles[corefile].setdefault(
                                            'decode', decode_output)
                        except Exception as e:
                            log.warning(
                                'decode core file is failed : {e}'.format(e=e))

                    if 'tar.gz' in corefile:
                        # delete folder for extracting .tar.gz
                        extracted_dir = remote_path + '/' + corefile.split(
                            '.')[0]
                        log.info(
                            'Deleting folder {dir} where system-report was extracted.'
                            .format(dir=extracted_dir))
                        remote_device.api.execute(
                            'rm -rf {dir}'.format(dir=extracted_dir))

                # delete core files
                if delete_core and copy_success:
                    try:
                        log.info(
                            'Deleting copied file {lp}.'.format(lp=local_path))
                        device.execute(
                            'delete /force {lp}'.format(lp=local_path))
                        log.info('{lp} was successfully deleted'.format(
                            lp=local_path))
                    except Exception as e:
                        log.warn('deleting core files on s failed. {e}'.format(
                            s=storage, e=e))
                        return []

    if health:
        if hasattr(runtime, 'health_data') and runtime.health_data is not None:
            log.debug(f'runtime health data {runtime.health_data}')
            runtime.health_data.setdefault(device.name, runtime.synchro.dict())
            runtime.health_data[device.name].setdefault('core', {})
            runtime_health_data = runtime.health_data[device.name]['core']
        else:
            runtime_health_data = {}

        runtime_health_data.setdefault('corefiles', [])
        # get existing core files from health data
        existing_core_files = [hf.get('filename') for hf in runtime_health_data.get('corefiles', [])]
        if existing_core_files:
            log.info(f'Existing core files: {existing_core_files}')

        # create list of new core files
        new_core_files = [cf for cf in health_corefiles if cf not in existing_core_files]

        # init health_data
        health_data = {'health_data': {}}
        health_data['health_data'].setdefault('num_of_cores', len(new_core_files))
        health_data['health_data'].setdefault('corefiles', [])

        # process core files, add to existing health data
        for filename in new_core_files:
            file_data = {'filename': filename}
            if 'decode' in health_corefiles[filename]:
                file_data.update({'decode': health_corefiles[filename]['decode']})

            log.info(f'Adding file {filename} to health core info for device {device.name}')
            health_data['health_data']['corefiles'].append(file_data)
            runtime_health_data['corefiles'].append(file_data)

        if hasattr(runtime, 'health_data'):
            runtime.health_data[device.name]['core'] = runtime_health_data
            log.debug(f'runtime health data {runtime.health_data}')
        return health_data

    if num_of_cores:
        return len(all_corefiles)
    return all_corefiles
