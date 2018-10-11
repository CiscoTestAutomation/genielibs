'''HA useful function'''

# Python
import time

# unicon
from unicon.eal.dialogs import Statement, Dialog

from ..ha import HA as HA_iosxe


class HA(HA_iosxe):

    def _reloadLc(self, lc):
        """Do the reload LC action for c3850(edison) devices.

        Args:
          Mandatory:
            lc (`str`) : LC slot number need to reload.

        Raises:
            Unicon errors

        Example:
            >>> _reloadLc(lc='1')
        """
        # unicon
        dialog = Dialog([
            Statement(pattern=r'\[yes\/no\].*',
                                action='sendline(y)',
                                loop_continue=True,
                                continue_timer=False),
            Statement(pattern=r'\(y\/n\)\?.*',
                                action='sendline(y)',
                                loop_continue=True,
                                continue_timer=False)
        ])
        # # Execute command to reload LC
        self.device.execute('reload slot {}'.format(lc), reply=dialog)
        time.sleep(5)
