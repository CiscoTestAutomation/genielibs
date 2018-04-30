'''HA IOSXR implement function'''

# import python
import time

# Genie Libs
from ..ha import HA as HA_main

# unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure


class HA(HA_main):

    def _switchover(self):
        """Do the switchover action for IOSXR devices.

        Raises:
            Unicon errors

        Example:
            >>> _switchover()
        """
        # unicon
        self.device.execute('redundancy switchover')

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

        Raises:
            Exception

        Example:
            >>> reload(steps=ats.aetest.Steps(),
                       timeout=genie.utils.timeout.Timeout(
                          max_time=180,
                          interval=15))
        """
        with steps.start('Reloading the device {}'.format(self.device.name),
                         continue_=True) as step:
            try:
                self.device.execute('admin reload location all')
            except SubCommandFailure:
                pass
            except Exception as e:
                raise Exception(str(e))
            
        self._reconnect(steps=steps, timeout=timeout)

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
        self.device.execute('admin reload location {}'.format(lc), reply=dialog)
        time.sleep(5)
