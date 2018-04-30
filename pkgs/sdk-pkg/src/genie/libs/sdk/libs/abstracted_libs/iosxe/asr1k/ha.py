'''HA useful function'''

# Python
import time

# unicon
from unicon.eal.dialogs import Statement, Dialog

from ..ha import HA as HA_iosxe


class HA(HA_iosxe):

    def _reloadLc(self, lc):
        """Do the reload LC action for asr1k devices.

        Args:
          Mandatory:
            lc (`str`) : LC slot number need to reload.

        Raises:
            Unicon errors

        Example:
            >>> _reloadLc(lc='R0')
        """
        # unicon
        dialog = Dialog([
            Statement(pattern=r'\(y\/n\)\?.*',
                                action='sendline(y)',
                                loop_continue=True,
                                continue_timer=False)
        ])
        # Execute command to reload LC
        self.device.execute('hw-module slot {} reload'.format(lc), reply=dialog)
        time.sleep(5)
