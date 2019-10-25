'''HA useful function'''

# Python
import os
import time
import logging
from datetime import datetime

# genie
from genie.utils.timeout import TempResult
from genie.harness.utils import connect_device, disconnect_device

from ..ha import HA as HA_nxos
from unicon.eal.dialogs import Statement, Dialog

# module logger
log = logging.getLogger(__name__)


class HA(HA_nxos):

    def get_debug_plugin(self, debug_plugin):

        if not self.device.filetransfer_attributes['protocol']:
            raise Exception("Unable to get debug plugin, file transfer "
                "'protocol' is missing. Check the testbed yaml file and the "
                "provided arguments.")

        # Case when user pass multiple debug plugins, path as an argument
        # in the job file and the actual plugins in the testbed yaml file
        if hasattr(self.device.custom, 'debug_plugin'):
            from_URL = '{protocol}://{address}/{debug_plugin_path}/{debug_plugin}'.format(
                protocol=self.device.filetransfer_attributes['protocol'],
                address=self.device.filetransfer_attributes['server_address'],
                debug_plugin_path=debug_plugin, debug_plugin=self.device.custom.debug_plugin)

            to_URL = 'bootflash:{}'.format(self.device.custom.debug_plugin)
        else:
            # Case when user pass one debug plugin as an argument in
            # in the job file
            from_URL = '{protocol}://{address}/{debug_plugin}'.format(
                protocol=self.device.filetransfer_attributes['protocol'],
                address=self.device.filetransfer_attributes['server_address'],
                debug_plugin=debug_plugin)

            to_URL = 'bootflash:{}'.format(debug_plugin.split('/')[-1])

        self.filetransfer.copyfile(device=self.device,
                                   source=from_URL,
                                   destination=to_URL)

        log.info('Copied debug plugin at : {l}'.format(l=to_URL))
        return to_URL

    def _copy_temp_debug_plugin(self, debug_plugin):
        self.device.execute('copy {dp} bootflash:debug_plugin.tmp'.format(\
                                                              dp=debug_plugin))

    def _delete_debug_plugin(self, debug_plugin):
        dialog = Dialog([
            Statement(pattern=r'.*Do you want to delete.*',
                      action='sendline(y)',
                      loop_continue=True,
                      continue_timer=False)])
        self.device.execute('delete {dp}'.format(dp=debug_plugin), reply=dialog)

    def load_debug_plugin(self, debug_plugin):
        try:
            self._copy_temp_debug_plugin(debug_plugin)
        except:
            raise Exception("Couldn't copy debug plugin to \
            'bootflash:debug_plugin.tmp'")

        try:
            self._delete_debug_plugin(debug_plugin)
        except:
            raise Exception("Couldn't delete the debug plugin from 'bootflash'")

        self.device.state_machine.get_state('enable').add_state_pattern(
            [r'^(.*)Linux\(debug\)#\s?$'])
        self.device.execute('load bootflash:debug_plugin.tmp', timeout=5)

    def _reconnect(self, steps, timeout, sleep_disconnect=30):
        """Disconnect and reconnect to router within given timeout.

        Args:
          Mandatory:
            steps (`obj`) : Step object to represent each step taken.
            timeout (`obj`) :
                max_time (int): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (int): Wait time between iterations when looping is needed,
                                in second. Default: 15
          Optional:
            sleep_disconnect (`int`) : Break between issue the command and the
                                       HA action really take place,
                                       in second. Default: 30

        Returns:
            AETEST Step Result


        Raises:
            None

        Example:
            >>> _reconnect(steps=ats.aetest.Steps(),
                           timeout=genie.utils.timeout.Timeout(
                             max_time=180,
                             interval=15))
        """

        if hasattr(self.device.custom, 'vdcs'):
            devices = [self.device]
            for vdc in self.device.custom['vdcs']:
                devices.append(self.device.testbed.devices[vdc])
        else:
            devices = [self.device]

        for device in devices:
            with steps.start('Disconnecting device {}'.format(device.name),
                             continue_=True) as step:
                disconnect_device(device)
                time.sleep(sleep_disconnect)

            with steps.start('Reconnecting to device {}'.format(device.name),
                             continue_=True) as step:
                temp = TempResult(container=step)
                while timeout.iterate():
                    try:
                        connect_device(device)
                    except Exception as e:
                        temp.failed('Could not reconnect to the device',
                                    from_exception=e)
                        # incase console is existed but cannot enable the device.
                        # conf mode is not active when standby RP is coming up
                        try:
                            disconnect_device(device)
                        except:
                            pass
                        timeout.sleep()
                        continue
                    temp.passed('Reconnected to the device')
                    break
                temp.result()