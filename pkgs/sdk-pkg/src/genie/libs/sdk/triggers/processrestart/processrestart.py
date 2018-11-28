'''Common implementation for ProcessRestart Cli trigger'''

import time
import logging

from ats import aetest

from genie.utils.diff import Diff
from genie.libs.sdk.triggers.template.processrestart import \
                       TriggerProcessRestart as ProcessRestartTemplate

log = logging.getLogger(__name__)

class TriggerProcessRestart(ProcessRestartTemplate):
    '''Trigger class for ProcessCliRestart action'''

    @aetest.setup
    def verify_prerequisite(self, uut, abstract, steps):
        '''Learn Ops object and verify the requirements.

           If the requirements are not satisfied, then skip to the next
           testcase.

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''

        self.lib = abstract.sdk.triggers.processrestart.\
                            libs.processrestart.ProcessRestartLib(\
                                            device=uut,
                                            process=self.process,
                                            abstract=abstract,
                                            verify_exclude=self.verify_exclude,
                                            obj=self)

        try:
            self.lib.process_information()
        except Exception as e:
            self.skipped("Issue getting information about '{p}' "
                         "process".format(p=self.process), from_exception=e,
                         goto=['next_tc'])

        self.print_local_verifications()

    @aetest.test
    def restart(self, uut, abstract, steps, repeat_restart=1, sleep_restart=0):
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

        try:
            if self.method == 'crash':
                if hasattr (self.lib, "crash_restart"):
                    output = self.lib.crash_restart()
                else:
                    self.skipped("ProcessCrashRestart is not supported on "
                                 "the device type: '{p}'".format(p=uut.type))
            elif self.method == 'cli':
                if hasattr (self.lib, "cli_restart"):
                    output = self.lib.cli_restart()
                else:
                    self.skipped("ProcessCliRestart is not supported on "
                                 "the device type: '{p}'".format(p=uut.type))
        except Exception as e:
            self.failed("Failed to restart '{p}' ".\
                        format(p=self.process), from_exception=e)

        if sleep_restart:
            log.info("Sleeping for {s} before next "
                     "restart".format(s=sleep_restart))
            time.sleep(0)

    @aetest.test
    def verify_restart(self, uut, abstract, steps, timeout, repeat_restart=1):
        '''Verify if the shut command shut the feature correctly and
           as expected

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''
        try:
            if self.method == 'crash':
                output = self.lib.verify_restart(repeat_restart=repeat_restart,
                                                 steps=steps, timeout=timeout)
            elif self.method == 'cli':
                output = self.lib.verify_restart(repeat_restart=repeat_restart,
                                                 steps=steps, timeout=timeout)
        except Exception as e:
            self.failed("Issue getting information about '{p}' "
                        "process".format(p=self.process), from_exception=e)
