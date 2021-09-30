'''HA NXOS implement function'''

# Parser
from genie.abstract import Lookup
from genie.libs import parser

from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Statement, Dialog
from os.path import basename, getsize
from datetime import datetime
import re
import logging
import time
import os
import stat
from ..ha import HA as HA_main

# genie
from genie.libs.sdk.libs.utils.common import set_filetransfer_attributes
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk import apis
from genie.libs.sdk.apis.execute import execute_copy_run_to_start
from genie.libs.sdk.apis.utils import compare_config_dicts, get_config_dict

# pyats
from pyats.utils.objects import R, find
from pyats.utils.fileutils import FileUtils
from pyats.easypy import runtime

# unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.plugins.generic.statements import authentication_statement_list

# Parsergen
from genie.parsergen import oper_fill_tabular

# platform parser
from genie.libs.parser.nxos.show_platform import ShowModule, Dir

run_path = runtime.directory
os.chmod(run_path, os.stat(run_path)[stat.ST_MODE] | stat.S_IWOTH)

log = logging.getLogger(__name__)


class HA(HA_main):

    def capture_core(self):
        """Verify if any core on the device and
        upload the core file to linux if there is any

        Example:
            >>> capture_core()
        """
        cores = self.check_and_upload_cores()
        self.upload_to_server(device=self.device, cores=cores)

    def check_cores(self):
        """Verify if any core on the device.

        Returns:
            Core files name

        Example:
            >>> check_cores()
        """

        cores = []
        # Execute command to check for cores
        header = ["VDC", "Module", "Instance",
                  "Process-name", "PID", "Date\(Year-Month-Day Time\)"]

        if self.device.alias == 'uut':
            # In case of restarting process on a the main VDC
            output = oper_fill_tabular(device=self.device,
                                       show_command='show cores vdc-all',
                                       header_fields=header, index=[5])
        else:
            # In case of restarting process on a sub-VDC
            self.device.disconnect()
            output = oper_fill_tabular(device=self.device,
                                       show_command='show cores',
                                       header_fields=header, index=[5])

        if not output.entries:
            log.info('No core found')
            return []

        # Parse through output to collect core information (if any)
        for k in sorted(output.entries.keys(), reverse=True):
            row = output.entries[k]
            date = row.get("Date\(Year-Month-Day Time\)", None)
            if not date:
                continue
            date_ = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

            # Save core info
            core_info = dict(module=row['Module'],
                             pid=row['PID'],
                             instance=row['Instance'],
                             process=row['Process-name'],
                             date=date.replace(" ", "_"))
            cores.append(core_info)

        return cores

    def upload_core_to_linux(self, core):
        """Upload core files to composed path.

        Args:
          Mandatory:
            core (`str`) : Core file

        Example:
            >>> upload_core_to_linux(core='RP_0_bt_logger_13899_20180112-184444-EST.core.gz')
        """

        # if the setup was not done because the configure subsection did
        # not run, then we do the setup here
        if not hasattr(self.device, 'filetransfer_attributes'):
            filetransfer = FileUtils.from_device(self.device)
            set_filetransfer_attributes(self, self.device, filetransfer)

        filename, core = self.get_upload_cmd(**core)
        message = "Core dump upload attempt: {}".format(filename)

        from_URL = 'core:{core}'.format(
            core=core)

        to_URL = '{protocol}://{address}/{path}/{filename}'.format(
            protocol=self.device.filetransfer_attributes['protocol'],
            address=self.device.filetransfer_attributes['server_address'],
            path=self.device.filetransfer_attributes['path'],
            filename=filename)

        self.filetransfer.copyfile(device=self.device,
                                   source=from_URL,
                                   destination=to_URL)

    def get_upload_cmd(self, module, pid, instance, date, process):
        """Compose the cores upload location

        Args:
          Mandatory:
            module (`str`) : Module number
            pid (`str`) : Process id number
            instance (`str`) : Instance number
            date (`str`) : Date time
            process (`str`) : Process name

        Returns:
            Tuple of path and core information

        Example:
            >>> get_upload_cmd(module='27', pid='12345', instance='1',
                               date='Dec 12 2017', process='bgp')
        """
        path = 'core_{pid}_{process}_{date}_{time}'.format(
            pid=pid,
            process=process,
            date=date,
            time=time.time())

        if instance:
            pid = '{pid}/{instance}'.format(pid=pid, instance=instance)
        core = '//{module}/{pid}'.format(module=module, pid=pid)
        return (path, core)

    def clear_cores(self):
        """Clear cores.

        Raises:
            Unicon errors

        Example:
            >>> clear_cores()
        """
        # Execute command to delete cores
        self.device.execute('clear cores')

    def check_module(self):
        """Check if all modules are ready with command "show module".

        Raises:
            AttributeError: No information from "show module"
            AssertionError: Modules are not in status from 
                            'ok', 'active', 'standby', 'ha-standby'

        Example:
            >>> check_module()
        """

        show_module = ShowModule(device=self.device)

        rp_expected_status = ['active', 'ha-standby']
        lc_expected_status = ['ok', 'active', 'standby']

        # get output
        output = show_module.parse()

        if 'slot' not in output:
            raise AttributeError('Could not find slot for show module')

        if 'rp' not in output['slot'] or 'lc' not in output['slot']:
            raise AttributeError('Could not find rp or lc for show module')

        for rp in output['slot']['rp']:
            (module_type, value), = output['slot']['rp'][rp].items()
            status = value['status']
            assert status in rp_expected_status, \
                'Module "{0}" has state "{1}" instead of expected state "{2}"'\
                .format(rp, status, rp_expected_status)

        for lc in output['slot']['lc']:
            (module_type, value), = output['slot']['lc'][lc].items()
            status = value['status']
            assert status in lc_expected_status, \
                'Module "{0}" has state "{1}" instead of expected state "{2}"'\
                .format(lc, status, lc_expected_status)

    def _switchover(self):
        """Do the switchover action for NXOS devices.

        Raises:
            Unicon errors

        Example:
            >>> _switchover()
        """
        # Execute command to switchover
        self.device.execute('system switchover')

    def _reloadLc(self, lc):
        """Do the reload LC action for asr1k devices.

        Args:
          Mandatory:
            lc (`str`) : LC slot number need to reload.

        Raises:
            Unicon errors

        Example:
            >>> _reloadLc(lc='27')
        """
        # unicon
        dialog = Dialog([
            Statement(pattern=r'Proceed\[y\/n\]\?.*',
                      action='sendline(y)',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'\(y\/n\)\?.*',
                      action='sendline(y)',
                      loop_continue=True,
                      continue_timer=False)
        ])
        # Execute command to reload LC
        self.device.execute('reload module {}'.format(lc), reply=dialog)
        time.sleep(5)

    def _reloadFabric(self, fabric):
        """Do the poweroff/no poweroff action for NXOS n7k devices.

        Raises:
            Unicon errors

        Example:
            >>> _reloadFabric()
        """

        # Execute command to poweroff/on
        self.device.configure(
            'poweroff xbar {}\nno poweroff xbar {}'.format(fabric, fabric))

    ########################################################################
    #                               ISSU                                   #
    ########################################################################

    def _prepare_issu(self, steps, upgrade_image):
        """Prepare the device for ISSU:

            1. Check currect image version and upgrade image version
            2. Copy upgrade image to standby RP

            NXOS:
            1. Copy image onto the device

        Raises:
            Unicon errors
            Exception

        Example:
            >>> _prepare_issu(steps=steps, upgrade_image='someimage')
        """

        # # Init
        device = self.device

        if not hasattr(self.device, 'filetransfer_attributes'):
            filetransfer = FileUtils.from_device(self.device)
            set_filetransfer_attributes(self, self.device, filetransfer)

        disk = "bootflash:"
        timeout_seconds = 600

        with steps.start('Check available diskspace') as step:
            dir_output = filetransfer.parsed_dir(disk, timeout_seconds, Dir)

            if int(dir_output['disk_free_space']) < 4500000000:
                step.failed(
                    "Not enough free space available to copy over the image.Free up atleast 4.5GB of space on {}".format(disk))

        with steps.start('Copy over the issu image') as step:
            # Copy ISSU upgrade image to disk

            from_url = '{protocol}://{address}/{upgrade_image}'.format(
                protocol=device.filetransfer_attributes['protocol'],
                address=device.filetransfer_attributes['server_address'],
                upgrade_image=upgrade_image)
            filetransfer.copyfile(source=from_url, destination=disk,
                                  device=device, vrf='management', timeout_seconds=600)

            # Verify location:<filename> exists
            output = device.execute('dir {disk}{image}'.format(disk=disk,
                                                               image=basename(upgrade_image)))

            if 'No such file or directory' not in output:
                log.info("Copied ISSU image to '{}'".format(disk))
            else:
                step.failed('Required ISSU image {} not found on disk. Transfer failed.'.format(
                    basename(upgrade_image)))

    def _perform_issu(self, steps, upgrade_image, timeout=300):
        """Perform the ND-ISSU on NXOS device:

            NXOS:
            1. execute install all <> non-disruptive

        Raises:
            Unicon errors
            Exception

        Example:
            >>> _perform_issu(steps=steps, upgrade_image='someimage')
        """

        # Init
        lookup = Lookup.from_device(self.device)
        filetransfer = FileUtils.from_device(self.device)

        statement_list = authentication_statement_list + \
            [Statement(pattern=r'.*Do you want to continue with the installation\s*\(y/n\)\?\s*\[n\]',
                       action='sendline(y)', loop_continue=True, continue_timer=False)] + \
            [Statement(pattern=r'.*Do you want to overwrite\s*\(yes/no\)\?\s* \[no\]',
                       action='sendline(yes)', loop_continue=True, continue_timer=False)]
        dialog = Dialog(statement_list)

        ctrlplane_downtime = self.parameters.get('ctrlplane_downtime')
        user_boot_mode = self.parameters.get('mode')
        issu_timeout = self.parameters.get('issu_timeout')
        cfg_transfer = self.parameters.get('cfg_transfer')
        cfg_timeout = self.parameters.get('cfg_timeout')
        with steps.start("Check boot mode on {}".format(self.device.hostname)) as step:
            invalid_cmd = False
            out = self.device.execute('show boot mode')
            # p1 matches line "Current mode is <native/lxc>."
            p1 = re.compile(
                r'^Current\smode\sis\s(?P<mode>\w+)\.$')
            # p2 matches line "% Invalid command at '^' marker."
            p2 = re.compile(r'.*?\'\^ \'\smarker\.')
            for line in out.splitlines():
                line = line.strip()
                m = p1.match(line)
                if m:
                    sys_boot_mode = m.groupdict()['mode']
                    break
                m = p2.match(line)
                if m:
                    invalid_cmd = True
                    break
            if sys_boot_mode.lower() != user_boot_mode.lower():
                step.failed(
                    "System boot mode {} does not match user expected boot mode {}".format(sys_boot_mode, user_boot_mode))
            elif invalid_cmd and user_boot_mode.lower() != 'lxc':
                step.failed("System only supports lxc mode. Invalid user expected boot mode input {}".format(
                    user_boot_mode))
            else:
                step.passed(
                    "System boot mode {} matches user expected boot mode {}".format(sys_boot_mode, user_boot_mode))

        with steps.start("Take a running-config snapshot pre trigger on {}".format(self.device.hostname)):
            if cfg_transfer:
                self.device.execute('show run > {}_pre_issu_trig.cfg'.format(self.device.hostname),
                                    timeout=cfg_timeout, reply=dialog)
                to_url = '{protocol}://{address}/{path}'.format(
                    protocol=self.device.filetransfer_attributes['protocol'],
                    address=self.device.filetransfer_attributes['server_address'],
                    path=runtime.directory)
                filetransfer.copyfile(source='bootflash:/{}_pre_issu_trig.cfg'.format(self.device.hostname), destination=to_url,
                                      device=self.device, vrf='management', timeout_seconds=600)
                try:
                    with open("{}/{}_pre_issu_trig.cfg".format(runtime.directory, self.device.hostname), "r") as pre_trig_file:
                        pre_cfg_str = pre_trig_file.read()
                except IOError:
                    step.failed(
                        "file not found.Please check path/content of the file")
                pre_trig_config = get_config_dict(pre_cfg_str)
            else:
                pre_trig_config = self.device.api.get_running_config_dict()
        with steps.start("Perform copy run start on {}".format(self.device.hostname)):
            execute_copy_run_to_start(self.device)
        with steps.start("Performing non disruptive issu on the device {}".format(self.device.hostname)):
            image_name = basename(upgrade_image)
            self.device.execute(
                'install all nxos bootflash:{} non-disruptive'.format(image_name), timeout=issu_timeout, reply=dialog)

        with steps.start("Reconnect back to device {} after ISSU".format(self.device.hostname)):
            reconnect_timeout = Timeout(max_time=1200, interval=120)
            self._reconnect(steps=steps, timeout=reconnect_timeout)

        with steps.start("Verify image version on device {} after ISSU".format(self.device.hostname)):
            version_dict = lookup.parser.show_platform.\
                ShowVersion(device=self.device).parse()
            # version check
            rs = R(['platform', 'software', 'system_image_file',
                    'bootflash:///{}'.format(image_name)])
            ret = find([version_dict], rs, filter_=False, all_keys=True)
            if not ret:
                raise Exception(
                    "Image version mismatch after ISSU on device {}".format(self.device.hostname))

        with steps.start("Verify module status and config load status on device {} after ISSU".format(self.device.hostname)):
            self.device.api.verify_module_status()
            config_timeout = Timeout(max_time=180, interval=30)
            while config_timeout.iterate():
                try:
                    parsed = self.device.parse(
                        "show logging logfile | include 'System ready'")
                except SchemaEmptyParserError as e:
                    log.info(
                        "command did not return any output\n{}".format(str(e)))
                    config_timeout.sleep()
                    continue
                if parsed is not None:
                    log.info("{}".format(parsed.q.get_values('logs', -1)))
                    break
                config_timeout.sleep()

        with steps.start("Check CP downtime after on {} after ISSU".format(self.device.hostname)) as step:
            if user_boot_mode.lower() == 'lxc':
                step.passed(
                    "show install all time-stats detail unsupported on lxc mode and cp downtime is minimal")
            else:
                out = self.device.execute('show install all time-stats detail')
                output_error = False
                cp_downtime = None
                for line in out.splitlines():
                    line = line.rstrip()
                    p1 = re.compile(r'^ERROR:.*$')
                    m = p1.match(line)
                    if m:
                        output_error = True
                        break
                    p2 = re.compile(
                        r'^Total\s+.*?:\s(?P<cp_downtime>\d+)\s+seconds$')
                    m = p2.match(line)
                    if m:
                        cp_downtime = m.groupdict()['cp_downtime']
                        continue
                if output_error:
                    step.failed(
                        "The output shows reset-reason as disruptive. ND ISSU was not performed properly.")
                elif cp_downtime is None:
                    step.failed(
                        "garbled output for show install all time-stats detail so cp_downtime was not calculated properly.")
                elif int(cp_downtime) > int(ctrlplane_downtime):
                    step.failed(
                        "Control plane was down for {} seconds which is longer than user expected at {} seconds".format(cp_downtime,    ctrlplane_downtime))
                else:
                    step.passed(
                        "Control plane was down for {} seconds which is within an user acceptable range of {} seconds".format(cp_downtime,    ctrlplane_downtime))

        with steps.start("Compare post-trigger config with pre trigger config snapshot on {}".format(self.device.hostname)) as step:
            if cfg_transfer:
                self.device.execute('show run > {}_post_issu_trig.cfg'.format(self.device.hostname),
                                    timeout=cfg_timeout, reply=dialog)
                to_url = '{protocol}://{address}/{path}'.format(
                    protocol=self.device.filetransfer_attributes['protocol'],
                    address=self.device.filetransfer_attributes['server_address'],
                    path=runtime.directory)
                filetransfer.copyfile(source='bootflash:/{}_post_issu_trig.cfg'.format(self.device.hostname), destination=to_url,
                                      device=self.device, vrf='management', timeout_seconds=600)
                try:
                    with open("{}/{}_post_issu_trig.cfg".format(runtime.directory, self.device.hostname), "r") as post_trig_file:
                        post_cfg_str = post_trig_file.read()
                except IOError:
                    step.failed(
                        "file not found. Please check path/content of the file")
                post_trig_config = get_config_dict(post_cfg_str)
            else:
                post_trig_config = self.device.api.get_running_config_dict()
            output = compare_config_dicts(
                pre_trig_config, post_trig_config, [r'(boot|version)'])
            if output:
                step.failed(
                    "Inconsistencies in running config post trigger:{}".format(output))
