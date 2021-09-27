'''NXOS N7K specific recovery functions'''

# Python
import re
import logging

# Unicon
from unicon.eal.expect import Spawn
from unicon.eal.dialogs import Statement

# Genie
from genie.libs.clean.recovery.nxos.recovery import sendbrk_handler
from genie.libs.clean.recovery.nxos.dialogs import BreakBootDialog, RommonDialog

# Logger
log = logging.getLogger(__name__)

def recovery_worker(*args, **kwargs):

    if kwargs.get('golden_image'):
        return device_recovery(*args, **kwargs)
    elif kwargs.get('tftp_boot'):
        raise Exception('tftp_boot is not supported for N7k')

def device_recovery(start, device, console_activity_pattern, golden_image=None,
                           break_count=10, timeout=600, recovery_password=None,
                           tftp_boot=None, item=None, **kwargs):

    ''' A method for starting Spawns and handling the device statements during recovery
        Args:
            device ('obj'): Device object
            start ('obj'): Start method under device object
            console_activity_pattern ('str'): Pattern to send the break at
            golden_image ('str'): Image to load the device with
            break_count ('int'): Number of sending break times
            timeout ('int'): Recovery process timeout
            recovery_password ('str'): Device password after recovery
        Returns:
            None
    '''

    # Set a target for each recovery session
    # so it's easier to distinguish expect debug logs on the console.
    device.instantiate(connection_timeout=timeout)

    # Get device console port information
    last_word_in_start_match = re.match('.*\s(\S+)$', start)
    last_word_in_start = last_word_in_start_match.group(1) \
        if last_word_in_start_match else ""

    # Set target
    target = "{}_{}".format(device.hostname, last_word_in_start)

    logfile = log.handlers[1].logfile if len(log.handlers) >=2 else None
    spawn = Spawn(start,
                  settings=device.cli.settings,
                  target=target,
                  log=log,
                  logfile=logfile)

    break_dialog = BreakBootDialog()
    break_dialog.add_statement(Statement(pattern=console_activity_pattern,
                                         action=sendbrk_handler,
                                         args={'break_count': break_count},
                                         loop_continue=True,
                                         continue_timer=False),
                               pos=0)
    break_dialog.dialog.process(spawn, timeout=timeout)

    if 'kickstart' not in golden_image or 'system' not in golden_image:
        raise Exception("Either Kickstart or System image has not been provided "
                        "in the 'device_recovery' section of clean YAML")

    dialog = RommonDialog()
    dialog.dialog.process(spawn,
                          context={
                              'kick': golden_image.get('kickstart'),
                              'sys': golden_image.get('system'),
                              'password': recovery_password
                          },
                          timeout=timeout)
    spawn.close()
