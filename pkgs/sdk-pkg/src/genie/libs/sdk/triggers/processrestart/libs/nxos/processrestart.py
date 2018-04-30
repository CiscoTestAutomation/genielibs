'''NXOS Specific implementation of Restart process restart'''

import time
import logging
import datetime

from ats import aetest

from genie.utils.diff import Diff
from genie.utils.timeout import TempResult
from genie.harness.utils import connect_device, disconnect_device

log = logging.getLogger(__name__)

class ProcessRestartLib(object):
    '''Trigger class for ProcessCliRestart action'''

    # Mention for which process do special actions
    # Process to reconnect after restarting
    reconnect = ["sysmgr", "mrib", "netstack", "urib"]

    # Process where show sysmgr does not work, must use show process
    expected_no_show_sysmgr = ['sysmgr']
    
    # Process to switchover after restarting
    switchover = ["sysmgr", "urib", "mrib"]

    # Process which does not generate a core
    no_core = [""]

    no_log_check = ['sysmgr', 'syslogd', 'confcheck']

    def __init__(self, device, process, abstract, obj, verify_exclude):
        '''Initialize library'''
        self.device = device
        self.process = process

        # Trigger object
        self.obj = obj
        self.abstract = abstract
        self.verify_exclude = verify_exclude

    def process_information(self):
        '''Use for gathering initial information on the process'''

        if self.process in self.expected_no_show_sysmgr:
            # Instead just use show process
            self.previous_pid, self.cmd = self._process_information_no_sysmgr()

            # TODO - get timestamp
            # TO BE TESTED WHEN SWITCH TO UNICON
            # self.previous_timestamp = self.get_process_timestamp(process=self.process)
            return

        output = self.abstract.parser.show_system.\
                      ShowSystemInternalSysmgrServiceName(device=self.device).\
                      parse(process=self.process)

        # TODO: Add log to say what we are checking
        if 'instance' not in output:
            raise Exception("No output for 'show system internal sysmgr "
                            "service name {p}'".format(p=self.process))

        self.previous_pid = None
        for instance, tags  in output['instance'].items():
            for tag, keys in tags['tag'].items():
                # Make sure pid exists, if so take this one to restart
                if 'pid' in keys:
                    self.previous_pid = keys['pid']
                    if 'restart_count' in keys:
                        self.previous_restart_count = keys['restart_count']
                    else:
                        self.previous_restart_count = 0
                    if 'last_restart_date' in keys:
                        self.last_restart_time = \
                                datetime.datetime.strptime(\
                                           keys['last_restart_date'],
                                           '%a %b %d %H:%M:%S %Y')
                    else:
                        self.last_restart_time = datetime.datetime.today()
                    break
                else:
                    continue
            else:
                continue
            # Didnt go in the else, this mean it has found a pid to use
            break

        if not self.previous_pid:
            raise Exception("Could not find a running process for '{p}' "
                            .format(p=self.process))

        self.cmd = 'restart ' + self.process
        if tag.lower() != 'n/a':
            self.cmd = '{p} {tag}'.format(p=self.cmd, tag=tag)

        # Store the tag
        self.tag =  tag
        self.instance = instance
        self.previous_output = output

    def _process_information_no_sysmgr(self):
        '''Get process information with show process'''
        output = self.abstract.parser.show_process.\
                      ShowProcesses(device=self.device).parse(process=self.process)
        # Get pid
        if 'process' in output and self.process in output['process'] and\
           output['process'][self.process]:
           previous_pid = list(output['process'][self.process]['pid'].keys())[0]
        self.cmd = 'restart ' + self.process
        return (previous_pid, self.cmd)

    def cli_restart(self):
        '''Send configuration to restart the process

           Args:

           Returns:
               None

           Raises:
               pyATS Results
        '''
        self.device.execute(self.cmd)

    def verify_restart(self, repeat_restart, steps, timeout):
        '''Verify if the shut command shut the feature correctly and
           as expected

           Args:
               uut (`obj`): Device object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''

        # reconnect if needed
        if self.process in self.reconnect:
            self._reconnect(steps, timeout)

        # Switchover if needed
        if self.process in self.switchover:
            # Do switchover
            self._switchover(steps, timeout)

        if self.obj.method == 'cli':
            return self.verify_process(repeat_restart=repeat_restart,
                                        steps=steps, timeout=timeout)

        if self.process in self.expected_no_show_sysmgr:
            try:
                self._verify_restart_no_sysmgr(repeat_restart, steps, timeout)
            except Exception as e:
                pass

        core_check = True if int(self.obj.crash_method) == 6 and\
                             self.process not in self.no_core else False
                             
        if core_check:
            with steps.start('Verify process restart has created a core', \
                             continue_=True) as step:
                filetransfer = self.device.filetransfer if hasattr(self.device, 'filetransfer') else None
                ha = self.abstract.sdk.libs.abstracted_libs.ha.HA(
                    device=self.device, filetransfer=filetransfer)
                cores = None
                exception = None
                while timeout.iterate():
                    try:
                        cores = ha.check_cores()
                    except Exception as e:
                        exception = e

                    # Check if core is the one wanted
                    for core in cores:
                        if int(core['pid']) == self.previous_pid:
                            break
                    else:
                        timeout.sleep()
                        # Didn't find, so keep going
                        continue

                    # Found core
                    step.passed("Core found for "
                                "'{p}' '{pp}'".format(p=self.process,
                                                      pp=self.previous_pid))
                    break
                else:
                    # No core!
                    step.failed("No core was found for "\
                                "'{p}' '{pp}'".format(p=self.process,
                                                      pp=self.previous_pid),
                                from_exception=exception)


            if self.process not in self.no_log_check:

                with steps.start('Verify information has been printed to log',
                                 continue_=True) as step:

                    msg = self.device.execute("show logging logfile | i '(core "
                                              "will be saved)' | i '(PID {pid})' |"
                                              "count".format(pid=self.previous_pid))

                    msg2 = self.device.execute("show logging logfile | "
                                               "i 'SYSMGR-2-SERVICE_CRASHED:' |"
                                               "i '(PID {pid})' | count".\
                                                format(pid=self.previous_pid))
                    # Make sure the count is not 0
                    if int(msg) == 0 or int(msg2) == 0:
                        # TOOD Better message?
                        step.failed('The PID should be restarted at least one time '
                                    'from the logging logfile, '
                                    'expected non-zero, but got count number 0')
                    else:
                        step.passed('Process has restarted this time '
                                    '- the cound number is non-zero from the logging logfile')                

            self._extra_core(steps)

        if self.process not in self.expected_no_show_sysmgr:
            return self.verify_process(repeat_restart=repeat_restart,
                                           steps=steps, timeout=timeout)

    def verify_process(self, repeat_restart, steps, timeout):
        '''Verify the process has been restarted

           Args:
               uut (`obj`): Device object.
               steps (`step obj`): aetest step object

           Returns:
               None
        '''

        with steps.start('Verify process has restarted correctly') as step:
            temp = TempResult(container=step)

            while timeout.iterate():
                output = self.abstract.parser.show_system.\
                             ShowSystemInternalSysmgrServiceName(device=\
                                        self.device).parse(process=self.process)

                if 'instance' not in output:
                    temp.failed("No output for 'show system internal sysmgr "
                               "service name {p}'".format(p=self.process))
                    timeout.sleep()
                    continue

                # Check the if the process has changed pid
                try:
                    pid = output['instance'][self.instance]['tag'][self.tag]['pid']
                    sap = output['instance'][self.instance]['tag'][self.tag]['sap']
                    restart_count = output['instance'][self.instance]['tag'][self.tag]['restart_count']
                    last_restart = output['instance'][self.instance]['tag'][self.tag]['last_restart_date']
                    last_restart_time = datetime.datetime.strptime(last_restart,
                                                                   '%a %b %d %H:%M:%S %Y')
                except Exception as e:
                    temp.failed("Issue retrieving information about "
                                "'{p}' process".format(p=self.process),
                                from_exception=e)

                # Make sure time has changed
                if not self.last_restart_time < last_restart_time:
                    temp.failed("The restart time has not changed for "
                                "process '{p}'".format(p=self.process))
                    timeout.sleep()
                    continue
              
                # Make sure the pid has changed
                if self.process not in self.reconnect and pid == self.previous_pid:
                    temp.failed("The pid has not changed for process '{p}'"
                                "\nprevious pid: {pp}"
                                "\ncurrent pid: "
                                "{cp}".format(p=self.process,
                                              pp=self.previous_pid,
                                              cp=pid))
                    timeout.sleep()
                    continue

                # Verify the restart_count has increased
                if self.process not in self.reconnect and\
                   self.previous_restart_count + repeat_restart != restart_count:
                    temp.failed('Restart count has not increased by {rr}'
                                '\nprevious count: {pc}'
                                '\ncurrent count: {cc}'.format(rr=repeat_restart,
                                                               pc=self.previous_restart_count,
                                                               cc=restart_count))
                    timeout.sleep()
                    continue

                # exclude sap when the value is not in range [0, 1023]
                if sap > 1023:
                    self.verify_exclude.append('sap')
          

                # Modify the original output so it does not fail the compare
                self.previous_output['instance'][self.instance]['tag'][self.tag]['restart_count'] =\
                              restart_count
                self.previous_output['instance'][self.instance]['tag'][self.tag]['pid'] =\
                              pid

                diff = Diff(self.previous_output, output, exclude=self.verify_exclude)
                diff.findDiff()

                if diff.diffs:
                    temp.failed("The device output has changed in an unexpected "
                                "way\n{d}".format(d=str(diff.diffs)))
                    timeout.sleep()
                    continue
                break
            else:
                temp.result()

    def _verify_restart_no_sysmgr(self, repeat_restart, steps, timeout):
        '''Verify with show process that the pid has changed'''

        # TODO
        # Verify if timestamps is increasing
        # TO BE TESTED WHEN SWITCH TO UNICON
        # with steps.start('Verify the timestamp "previous < current"',
        #                  continue_=True) as step:
        #     # get timestamp
        #     timestamp = self.get_process_timestamp(process=self.process)
        #     if timestamp <= self.previous_timestamp:
        #         temp.failed("The timestamp is not increasing after restart "
        #                     "process '{p}'".format(p=self.process))
        #     else:
        #         temp.passed('The timestamp incresaed')

        # Verify if the pid is not the same
        with steps.start('Verify if the pid is the same',
                         continue_=True) as step:
            temp = TempResult(container=step)
            while timeout.iterate():
                previous_pid, _ = self._process_information_no_sysmgr()
                # Make sure time has changed
                if not self.previous_pid != previous_pid:
                    temp.failed("The restart pid has changed for "
                                "process '{p}'".format(p=self.process))
                    timeout.sleep()
                temp.passed('The pid has not changed')
                break

    def _switchover(self, steps, timeout):
        '''Switchover the device if needed'''
        # Switchover
        with steps.start('Switchover',
                         continue_=True) as step:
            self.device.execute('system switchover')
            step.passed('switchvoer is executed')

        # reconnect
        self._reconnect(steps, timeout)



    def _reconnect(self, steps, timeout):
        '''Reconnect to the device if needed'''
        if self.process in self.reconnect:

            ha = self.abstract.sdk.libs.abstracted_libs.ha.HA(
                device=self.device)
            with steps.start('The device is reloading when restarting this process',
                             continue_=True) as step:
                disconnect_device(self.device)
                time.sleep(30)
                temp = TempResult(container=step)
                while timeout.iterate():
                    try:
                        connect_device(self.device)
                    except Exception as e:
                        temp.failed('Could not reconnect to the device',
                                    from_exception=e)
                        timeout.sleep()
                        continue
                    temp.passed('Reconnected to the device')
                    break
                temp.result()

            # check show module
            with steps.start('Check module status after reconnection',
                             continue_=True) as step:
                
                temp = TempResult(container=step)
                while timeout.iterate():
                    try:
                        ha.check_module()
                    except AttributeError as e:
                        temp.failed('Could not find mandatory information from show module',
                                    from_exception=e)
                        continue
                    except AssertionError as e:
                        temp.failed('Modules are not ready', from_exception=e)
                        timeout.sleep()
                        continue

                    temp.passed('Modules are ready')
                    break

                temp.result()

    def _extra_core(self, steps):
        with steps.start('Verify if no extra core has been generated',
                         continue_=True) as step:
            # Check if core of process is found
            ha = self.abstract.sdk.libs.abstracted_libs.ha.HA(
                device=self.device, filetransfer=self.device.filetransfer)
            temp = TempResult(container=step)
            cores = ha.check_cores()
            for core in cores:
                # Upload core of all the other core found
                if int(core['pid']) == self.previous_pid:
                    continue
                # Different core than the one expected!

                log.error("Process '{p}' with '{pp}' has created a core "\
                          "but should not have".\
                               format(p=core['process'],
                                      pp=core['pid']))
                temp.failed('More core than expected has been created')
                ha.upload_core_to_linux(core)

            # Clear cores
            ha.clear_cores()
            temp.result()

