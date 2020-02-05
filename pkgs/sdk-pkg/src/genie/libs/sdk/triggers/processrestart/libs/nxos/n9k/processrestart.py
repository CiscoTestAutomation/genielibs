'''NXOS N9K Specific implementation of Restart process restart'''

import time
import logging

from pyats import aetest

from genie.utils.diff import Diff
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
        # enable bash feature
        self.device.configure('feature bash')

        # check if Unicon
        if hasattr(self.device, 'connection_provider') and \
           'unicon' in str(self.device.connection_provider):
            try:
                self.device.shellexec(['sudo kill -{cm} {p}'.format(
                                p=self.previous_pid,
                                cm=self.obj.crash_method)])
            except Exception as e:
                if self.process not in self.reconnect:
                    raise Exception(str(e))
        else:
            # print message
            log.warning('Skip linux handle, Please use UNICON')

   
    # TO BE TESTED WHEN SWITCH TO UNICON
    def get_process_timestamp(self, process):
        # enable bash
        self.device.configure('feature bash')

        # unicon
        # 'ls -l /var/run/sysmgr.pid\r\n-rw-r--r-- 1 root root 5 Jan 29 14:14 /var/run/sysmgr.pid\r\nbash-4.2$'
        output = self.device.shellexec(['ls -l /var/run/{}.pid\nexit'.format(process)])

        # get timestamp
        # 14:14
        timestamp = output.splitlines()[1].split()[7]
        timestamp = timestamp.split(':')
        timestamp = int(timestamp[0]) * 60 + int(timestamp[1])
        return(timestamp)
