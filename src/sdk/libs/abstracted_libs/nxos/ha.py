'''HA NXOS implement function'''

# Python
import os
import time
import logging
from datetime import datetime

# unicon
from unicon.eal.dialogs import Statement, Dialog

# Parsergen
from genie.parsergen import oper_fill_tabular

# parser
from genie.libs.parser.nxos.show_platform import ShowModule

# module logger
log = logging.getLogger(__name__)

from ..ha import HA as HA_main


class HA(HA_main):

    def __init__(self, device=None, filetransfer=None):
       self.device = device
       self.filetransfer = filetransfer

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
        header = [ "VDC", "Module", "Instance",
                    "Process-name", "PID", "Date\(Year-Month-Day Time\)" ]
        output = oper_fill_tabular(device = self.device,
                                   show_command = 'show cores vdc-all',
                                   header_fields = header, index = [5])
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
            core_info = dict(module = row['Module'],
                             pid = row['PID'],
                             instance = row['Instance'],
                             process = row['Process-name'],
                             date = date.replace(" ", "_"))
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
                                   from_file_url=from_URL,
                                   to_file_url=to_URL)

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
            pid = '{pid}/{instance}'.format(pid = pid, instance = instance)
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
