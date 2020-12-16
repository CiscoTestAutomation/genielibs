'''NXOS N9K Specific implementation of Restart process restart'''

import time
import logging

from pyats import aetest

from genie.utils.diff import Diff
from unicon.statemachine import State
from genie.utils.timeout import TempResult
from genie.harness.utils import connect_device, disconnect_device

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
        if not hasattr(self.device.custom, 'debug_plugin'):
            raise Exception('No debug plugin has been loaded on the device.')

        ha = self.abstract.sdk.libs.abstracted_libs.ha.HA(device=self.device,
                                                          filetransfer=self.device.filetransfer)
        # https://devxsupport.cisco.com/scp/tickets.php?id=39483
        State('config', r'Linux')
        State('exec', r'Linux')

        output = ha.load_debug_plugin(self.device.custom.debug_plugin)

        if 'Incompatible' in output:
            raise Exception("Incompatible debug plugin image\n")

        try:
            self.device.execute('kill -{cm} {p}\n'.\
                                format(p=self.previous_pid,
                                        cm=self.obj.crash_method),
                                timeout=10)
        except Exception as e:
            log.info('Exception raised is expected when running trigger '\
                'through management connection. Exception: {e}'.format(e=e))
            # Set pattern
            restore_state = State(name='config', pattern=r'^.(%N\(config\))#\s?')
            return

        self.device.instantiate()
        if 'vty' == self.device.connectionmgr.connections.cli.via:
            time.sleep(60)
            self.device.destroy()
            self.device.connect(via='vty')
        else:
            self.device.execute('exit', timeout=10)

        # Set pattern
        restore_state = State(name='config', pattern=r'^.(%N\(config\))#\s?')
