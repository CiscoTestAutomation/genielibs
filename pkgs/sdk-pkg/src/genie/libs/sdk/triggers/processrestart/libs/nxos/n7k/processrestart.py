'''NXOS N9K Specific implementation of Restart process restart'''

import time
from datetime import datetime
import logging

from ats import aetest

from genie.utils.diff import Diff
from genie.utils.timeout import TempResult
from genie.harness.utils import connect_device, disconnect_device
from unicon.statemachine import State

from ..processrestart import \
                      ProcessRestartLib as ProcessRestartLibNxos

log = logging.getLogger(__name__)

class ProcessRestartLib(ProcessRestartLibNxos):
    '''Trigger class for ProcessCliRestart action'''

    def crash_restart(self):
        '''Send configuration to shut

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''
        if not hasattr(self.device, 'debug_plugin'):
            raise Exception('No debug plugin has been loaded on the device.')

        ha = self.abstract.sdk.libs.abstracted_libs.ha.HA(device=self.device,
                                                        tftp=self.device.tftp)
        # https://devxsupport.cisco.com/scp/tickets.php?id=39483
        State('config', r'Linux')
        State('exec', r'Linux')

        ha.load_debug_plugin(self.device.debug_plugin)

        # Set pattern
        self.device.execute('kill -{cm} {p}\n'.\
                              format(p=self.previous_pid,
                                     cm=self.obj.crash_method),
                            timeout=10)
        self.device.execute('exit', timeout=10)

        restore_state =  State(name='config', pattern=r'^.(%N\(config\))#\s?')
