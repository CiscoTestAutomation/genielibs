'''IOSXE specific recovery functions'''

# Python
import re
import time
import logging

# Unicon
from unicon.eal.expect import Spawn
from unicon.eal.dialogs import Statement

# Genie
from genie.libs.clean.utils import print_message
from genie.libs.clean.recovery.iosxe.dialogs import (
    BreakBootDialog,
    RommonDialog,
    TftpRommonDialog)

# Logger
log = logging.getLogger(__name__)

def recovery_worker(start, device, console_activity_pattern=None,
                    console_breakboot_char=None, grub_activity_pattern=None,
                    grub_breakboot_char=None, break_count=10, timeout=600,
                    *args, **kwargs):
    """ Starts a Spawn and processes device dialogs during recovery of a device

        Args:
            start (obj): Start method under device object
            device (obj): Device object
            console_activity_pattern (str): Pattern to send the break at
            console_breakboot_char (str): Character to send when console_activity_pattern is matched
            grub_activity_pattern (str): Break pattern on the device for grub boot mode
            grub_breakboot_char (str): Character to send when grub_activity_pattern is matched
            break_count (int, optional): Number of break commands to send. Defaults to 10.
            timeout (int, optional): Recovery process timeout. Defaults to 600.

        Returns:
            None
    """

    def console_breakboot(spawn, break_count, break_char):
        """ Breaks the booting process on a device

            Args:
                spawn (obj): Spawn connection object
                break_count (int): Number of break commands to send
                break_char (str): Char to send

            Returns:
                None
        """

        log.info(f"Found the console_activity_pattern! Breaking the boot process.")

        for _ in range(break_count):
            log.info(f"Sending {repr(break_char)}")
            spawn.send(break_char)
            time.sleep(1)

    def grub_breakboot(spawn, break_char):
        """ Breaks the booting process on a device

            Args:
                spawn (obj): Spawn connection object
                break_char (str): Char to send

            Returns:
                None
        """

        log.info(f"Found the grub_activity_pattern! Breaking the boot process "
                 f"by sending {repr(break_char)}")

        spawn.send(break_char)

    # Set a target for each recovery session
    # so it's easier to distinguish expect debug logs on the console.
    device.instantiate(connection_timeout=timeout)

    # Get device console port information
    last_word_in_start_match = re.match('.*\s(\S+)$', start)
    last_word_in_start = last_word_in_start_match.group(1) \
        if last_word_in_start_match else ""

    # Set target
    target = "{}_{}".format(device.hostname, last_word_in_start)

    if len(log.handlers) >= 2:
        logfile= log.handlers[1].logfile
    else:
        logfile = None

    spawn = Spawn(spawn_command=start,
                  settings=device.cli.settings,
                  target=target,
                  log=log,
                  logfile=logfile)

    # Stop the device from booting
    break_dialog = BreakBootDialog()
    if console_activity_pattern and console_breakboot_char:
        break_dialog.add_statement(
            Statement(pattern=console_activity_pattern,
                      action=console_breakboot,
                      args={'break_count': break_count,
                            'break_char': console_breakboot_char},
                      loop_continue=True,
                      continue_timer=False), pos=0)

    if grub_activity_pattern and grub_breakboot_char:
        break_dialog.add_statement(
            Statement(pattern=grub_activity_pattern,
                      action=grub_breakboot,
                      args={'break_char': grub_breakboot_char},
                      loop_continue=True,
                      continue_timer=False), pos=0)

    break_dialog.dialog.process(spawn, timeout=timeout)

    # Recover the device using the specified method
    if kwargs.get('golden_image'):
        device_recovery(spawn, timeout, *args, **kwargs)
    elif kwargs.get('tftp_boot'):
        tftp_device_recovery(spawn, timeout, device, *args, **kwargs)

    spawn.close()

def device_recovery(spawn, timeout, golden_image, recovery_password=None, **kwargs):
    """ A method for processing a dialog that loads a local image onto a device

        Args:
            spawn (obj): Spawn connection object
            golden_image (dict): Information to load golden image on the device
            timeout (int): Recovery process timeout
            recovery_password (str, optional): Device password after recovery

        Returns:
            None
    """

    dialog = RommonDialog()
    dialog.dialog.process(
        spawn,
        timeout=timeout,
        context={'boot_image': golden_image[0],
                 'password': recovery_password})


def tftp_device_recovery(spawn, timeout, device, tftp_boot, item, recovery_password=None, **kwargs):
    """ A method for processing a dialog that loads a remote image onto a device

        Args:
            spawn (obj): Spawn connection object
            device ('obj'): Device object
            tftp_boot ('dict'): Tftp boot information
            timeout ('int'): Recovery process timeout
            recovery_password ('str'): Device password after recovery
            item (int): Index of device connection

        Returns:
            None
    """

    dialog = TftpRommonDialog()

    # Add a statement to the dialog which will match the device hostname
    dialog.add_statement(
        Statement(pattern=r'^(.*?)({hostname}|Router|Switch|ios|switch)(\\(standby\\))?(-stby)?(\\(boot\\))?(>)'
                          r''.format(hostname=device.hostname),
                  action=print_message,
                  args={'message': 'Device has reached privileged exec prompt'}))

    dialog.dialog.process(
        spawn,
        timeout=timeout,
        context={'device_name': device.name,
                 'ip': tftp_boot['ip_address'][item],
                 'password': recovery_password,
                 'subnet_mask': tftp_boot['subnet_mask'],
                 'gateway': tftp_boot['gateway'],
                 'image': tftp_boot['image'],
                 'tftp_server': tftp_boot['tftp_server'],
                 'hostname': device.hostname})

