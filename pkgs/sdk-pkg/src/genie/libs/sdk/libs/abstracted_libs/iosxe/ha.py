'''HA IOSXE implement function'''

# unicon
from unicon.eal.dialogs import Statement, Dialog

from ..ha import HA as HA_main


class HA(HA_main):

    def _switchover(self, timeout=700):
        """Do the switchover action for IOSXE devices.

        Raises:
            Unicon errors

        Example:
            >>> _switchover()
        """
        # unicon
        dialog = Dialog([
            Statement(pattern=r'Save\? *\[yes\/no\]:.*',
                      action='sendline(y)',
                      loop_continue=True,
                      continue_timer=False)
        ])
        out = self.device.switchover(
            'redundancy force-switchover', reply=dialog, timeout=timeout
        )
        if not out:
            raise NotImplementedError
