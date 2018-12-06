'''HA Main function'''

# Python
import time
import logging

# genie
from genie.utils.timeout import TempResult
from genie.harness.utils import connect_device, disconnect_device

# unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Statement, Dialog

# module logger
log = logging.getLogger(__name__)


class HA(object):
    """Class to handle HA related actions"""

    def __init__(self, device=None, filetransfer=None):
        """built-in __init__

        instantiates each HA.

        Arguments
        ---------
            device (`obj`): Device object
            filetransfer (`obj`): filetransferutils object
        """
        self.device = device
        self.filetransfer = filetransfer

    def get_debug_plugin(self, debug_plugin):
        pass

    def switchover(self, steps, timeout):
        """Do the switchover action and reconnect to router after switchover.

        Args:
          Mandatory:
            steps (`obj`) : Step object to represent each step taken.
            timeout (`obj`) : 
                max_time (int): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (int): Wait time between iterations when looping is needed,
                                in second. Default: 15

        Returns:
            AETEST Step Result


        Raises:
            None

        Example:
            >>> switchover(steps=ats.aetest.Steps(),
                           timeout=genie.utils.timeout.Timeout(
                              max_time=180,
                              interval=15))
        """
        with steps.start('Switchover', continue_=True) as step:
            try:
                self._switchover()
            except SubCommandFailure:
                pass
            except Exception as e:
                raise Exception(str(e))
            
        self._reconnect(steps=steps, timeout=timeout)

    def reload(self, steps, timeout):
        """Do the reload the whole box action and
        reconnect to router after reload.

        Args:
          Mandatory:
            steps (`obj`) : Step object to represent each step taken.
            timeout (`obj`) : 
                max_time (int): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (int): Wait time between iterations when looping is needed,
                                in second. Default: 15

        Returns:
            AETEST Step Result


        Raises:
            None

        Example:
            >>> reload(steps=ats.aetest.Steps(),
                       timeout=genie.utils.timeout.Timeout(
                          max_time=180,
                          interval=15))
        """
        with steps.start('Reloading the device {}'.format(self.device.name),
                         continue_=True) as step:
            # unicon
            dialog = Dialog([
                Statement(pattern=r'\(y\/n\) +\[n\].*',
                                    action='sendline(y)',
                                    loop_continue=True,
                                    continue_timer=False),
                Statement(pattern=r'Save\? *\[yes\/no\]:.*',
                                    action='sendline(y)',
                                    loop_continue=True,
                                    continue_timer=False)
            ])

            # store original error pattern
            origin_err_pat = self.device.settings.ERROR_PATTERN.copy()

            # TODO - update more with issues when seeing
            # update the error pattern
            self.device.settings.ERROR_PATTERN.append("Write failed: Broken pipe")
            try:
                self.device.reload(dialog=dialog)
            except SubCommandFailure:
                # read the capture setting errors
                try:
                    out = self.device.spawn.read()
                except Exception:
                    out = getattr(getattr(self.device, 'spawn', None), 'buffer', None)

                if 'Write failed' in str(out):
                    log.warning('Please Notice failures during reload: %s' % str(out))
            except Exception as e:
                raise Exception(str(e))

        # revert the error pattern
        self.device.settings.ERROR_PATTERN = origin_err_pat.copy()
            
        self._reconnect(steps=steps, timeout=timeout)

    def reloadLc(self, steps, timeout, lc):
        """Do the reload the LC action and reconnect to router
        after reload if lost connection.

        Args:
          Mandatory:
            steps (`obj`) : Step object to represent each step taken.
            timeout (`obj`) : 
                max_time (int): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (int): Wait time between iterations when looping is needed,
                                in second. Default: 15
            lc (`str`) : LC slot number need to reload.

        Returns:
            AETEST Step Result


        Raises:
            None

        Example:
            >>> reloadLc(steps=ats.aetest.Steps(),
                         timeout=genie.utils.timeout.Timeout(
                            max_time=180,
                            interval=15),
                         lc = '27')
        """

        with steps.start('Reload LC {}'.format(lc), continue_=True) as step:
            try:
                self._reloadLc(lc=lc)
            except SubCommandFailure:
                pass
            except Exception as e:
                raise Exception(str(e))

        # check if reload the active supervisor LC
        # if so, need reconnection
        try:
            self.device.execute('show clock')
        except:
            self._reconnect(steps=steps, timeout=timeout)

    def prepare_issu(self, steps, upgrade_image):
        """Prepare the device to be ready to perform ISSU.

        Args:
          Mandatory:
            steps (`obj`) : Step object to represent each step taken.
            timeout (`obj`) :
                max_time (int): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (int): Wait time between iterations when looping is needed,
                                in second. Default: 15

        Returns:
            AETEST Step Result

        Raises:
            None

        Example:
            >>> prepare_issu(steps=ats.aetest.Steps(),
                             timeout=genie.utils.timeout.Timeout(
                             max_time=180,
                             interval=15))
        """

        with steps.start('Prepare device for ISSU', continue_=True) as step:
            try:
                self._prepare_issu(steps=steps, upgrade_image=upgrade_image)
            except SubCommandFailure:
                pass
            except Exception as e:
                raise Exception(str(e))

    def perform_issu(self, steps, upgrade_image):
        """Perform all the ISSU steps in sequence and reconnect to the device

        Args:
          Mandatory:
            steps (`obj`) : Step object to represent each step taken.
            timeout (`obj`) :
                max_time (int): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (int): Wait time between iterations when looping is needed,
                                in second. Default: 15

        Returns:
            AETEST Step Result

        Raises:
            None

        Example:
            >>> perform_issu(steps=ats.aetest.Steps(),
                             timeout=genie.utils.timeout.Timeout(
                             max_time=180,
                             interval=15))
        """

        with steps.start('Perform ISSU', continue_=True) as step:
            try:
                self._perform_issu(steps=steps, upgrade_image=upgrade_image)
            except Exception as e:
                raise Exception(str(e))

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
        with steps.start('Disconnecting device {}'.format(self.device.name),
                         continue_=True) as step:
            disconnect_device(self.device)
            time.sleep(sleep_disconnect)

        with steps.start('Reconnecting to device {}'.format(self.device.name),
                         continue_=True) as step:
            temp = TempResult(container=step)
            while timeout.iterate():
                try:
                    connect_device(self.device)
                except Exception as e:
                    temp.failed('Could not reconnect to the device',
                                from_exception=e)
                    # incase console is existed but cannot enable the device.
                    # conf mode is not active when standby RP is coming up
                    try:
                        disconnect_device(self.device)
                    except:
                        pass
                    timeout.sleep()
                    continue
                temp.passed('Reconnected to the device')
                break
            temp.result()
