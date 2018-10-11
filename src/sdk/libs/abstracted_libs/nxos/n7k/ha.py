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

        from_URL = '{protocol}://{address}/{debug_plugin}'.format(
            protocol=self.device.filetransfer_attributes['protocol'],
            address=self.device.filetransfer_attributes['server_address'],
            path=self.device.filetransfer_attributes['path'])

        to_URL = 'bootflash://'

        self.filetransfer.copyfile(device=self.device,
                                   from_file_url=from_URL,
                                   to_file_url=to_URL)

        location = 'bootflash:////'
        log.info('Copied debug plugin at : {l}'.format(l=location))
        return location

    def _copy_temp_debug_plugin(self, debug_plugin):
        self.device.execute('copy {dp} bootflash:debug_plugin.tmp'.format(\
                                                              dp=debug_plugin))

    def load_debug_plugin(self, debug_plugin):
        self._copy_temp_debug_plugin(debug_plugin)
        self.device.execute('load bootflash:debug_plugin.tmp', timeout=5)
