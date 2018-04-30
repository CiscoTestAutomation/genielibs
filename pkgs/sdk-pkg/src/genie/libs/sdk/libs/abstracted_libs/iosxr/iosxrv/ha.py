'''HA IOSXRv implement function'''

# Genie Libs
from ..ha import HA as HA_main

# unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure


class HA(HA_main):

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
        # unicon
        dialog = Dialog([
            Statement(pattern=r'\[no,yes\].*',
                                action='sendline(y)',
                                loop_continue=True,
                                continue_timer=False),
            Statement(pattern=r'\(y\/n\)\?.*',
                                action='sendline(y)',
                                loop_continue=True,
                                continue_timer=False)
        ])
        with steps.start('Reloading the device {}'.format(self.device.name),
                         continue_=True) as step:
            try:
                self.device.execute('admin reload location 0/RP0 all', reply=dialog)
            except SubCommandFailure:
                pass
            except Exception as e:
                raise Exception(str(e))
            
        self._reconnect(steps=steps, timeout=timeout)




