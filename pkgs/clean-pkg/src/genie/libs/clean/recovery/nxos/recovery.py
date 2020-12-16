'''NXOS specific recovery functions'''

# Python
import time
import logging

# Logger
log = logging.getLogger(__name__)

# Power Cycler handlers
def sendbrk_handler(spawn, break_count):
    ''' Send break while rebooting device
        Args:
            spawn ('obj'): Spawn connection object
            break_count ('int'): Number of sending break times
        Returns:
            None
    '''

    count = 1
    while count < break_count:
        log.debug('Sending break')
        # `\x03` is Ctrl-C 
        spawn.sendline("\x03")
        time.sleep(1)
        count += 1
