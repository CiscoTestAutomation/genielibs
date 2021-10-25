"""Common health functions for platform"""

# Python
import re
import logging

# pyATS
from pyats.easypy import runtime

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


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
                i for i in remote_device.api.get_connected_alias().keys()
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
                log.info('Copying {s}  via FileUtils'.format(
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
                                                             vrf=vrf,
                                                             use_kstack=True,
                                                             timeout=600)
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