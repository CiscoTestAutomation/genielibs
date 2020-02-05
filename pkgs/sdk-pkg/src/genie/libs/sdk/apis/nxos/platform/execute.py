'''NXOS execute functions for platform'''

# Python
import re
import logging

# pyATS
from pyats.utils.fileutils import FileUtils

# Unicon
from unicon.eal.dialogs import Statement, Dialog

# Logger
log = logging.getLogger(__name__)


def execute_write_erase(device):

    ''' Execute write erase on the device
        Args:
            device ('obj'): Device object
    '''

    log.info("Executing Write Erase")
    write_erase = Statement(
        pattern=r'.*Do you wish to proceed anyway\? \(y\/n\)\s*\[n\]',
        action='sendline(y)',
        loop_continue=True,
        continue_timer=False)

    try:
        device.execute("write erase", reply=Dialog([write_erase]))
    except Exception as err:
        log.error("Failed to write erase: {err}".format(err=err))
        raise Exception(err)
