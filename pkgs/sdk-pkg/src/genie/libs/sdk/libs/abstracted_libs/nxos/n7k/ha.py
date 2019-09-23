'''HA useful function'''

# Python
import os
import time
import logging
from datetime import datetime

from ..ha import HA as HA_nxos

# module logger
log = logging.getLogger(__name__)


class HA(HA_nxos):

    def get_debug_plugin(self, debug_plugin):

        if not self.device.filetransfer_attributes['protocol']:
            raise Exception("Unable to get debug plugin, file transfer "
                "'protocol' is missing. Check the testbed yaml file and the "
                "provided arguments.")

        # Case when user pass one debug plugin as an argument in
        # in the job file
        if os.path.isfile(debug_plugin):
            from_URL = '{protocol}://{address}/{debug_plugin}'.format(
                protocol=self.device.filetransfer_attributes['protocol'],
                address=self.device.filetransfer_attributes['server_address'],
                debug_plugin=debug_plugin)

            to_URL = 'bootflash:{}'.format(debug_plugin.split('/')[-1])
        elif hasattr(self.device.custom, 'debug_plugin'):
            # Case when user pass multiple debug plugins, path as an argument
            # in the job file and the actual plugins in the testbed yaml file
            from_URL = '{protocol}://{address}/{debug_plugin_path}/{debug_plugin}'.format(
                protocol=self.device.filetransfer_attributes['protocol'],
                address=self.device.filetransfer_attributes['server_address'],
                debug_plugin_path=debug_plugin, debug_plugin=self.device.custom.debug_plugin)

            to_URL = 'bootflash:{}'.format(self.device.custom.debug_plugin)
        else:
            raise Exception("Debug plugin is missing from the \
                testbed yaml file.\ndevices:\n   'device_name':\n\
                        custom:\n            \debug_plugin:'debug_plugin_image'")

        self.filetransfer.copyfile(device=self.device,
                                   source=from_URL,
                                   destination=to_URL)

        log.info('Copied debug plugin at : {l}'.format(l=to_URL))
        return to_URL

    def _copy_temp_debug_plugin(self, debug_plugin):
        self.device.execute('copy {dp} bootflash:debug_plugin.tmp'.format(\
                                                              dp=debug_plugin))

    def load_debug_plugin(self, debug_plugin):
        self._copy_temp_debug_plugin(debug_plugin)
        self.device.state_machine.get_state('enable').add_state_pattern(
            [r'^(.*)Linux\(debug\)#\s?$'])
        self.device.execute('load bootflash:debug_plugin.tmp', timeout=5)
        #self.device.sendline('exit')