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

#pyats
from pyats.utils.secret_strings import to_plaintext

# Logger
log = logging.getLogger(__name__)

def recovery_worker(start, device, console_activity_pattern=None,
                    console_breakboot_char=None, console_breakboot_telnet_break=None,
                    grub_activity_pattern=None, grub_breakboot_char=None,
                    break_count=10, timeout=600,
                    *args, **kwargs):
    """ Starts a Spawn and processes device dialogs during recovery of a device

        Args:
            start (obj): Start method under device object
            device (obj): Device object
            console_activity_pattern (str): Pattern to send the break at
            console_breakboot_char (str): Character to send when console_activity_pattern is matched
            console_breakboot_telnet_break (bool): Use telnet `send break` to interrupt device boot
            grub_activity_pattern (str): Break pattern on the device for grub boot mode
            grub_breakboot_char (str): Character to send when grub_activity_pattern is matched
            break_count (int, optional): Number of break commands to send. Defaults to 10.
            timeout (int, optional): Recovery process timeout. Defaults to 600.

        Returns:
            None
    """

    device.api.send_break_boot(
        console_activity_pattern=console_activity_pattern,
        console_breakboot_char=console_breakboot_char,
        console_breakboot_telnet_break=console_breakboot_telnet_break,
        grub_activity_pattern=grub_activity_pattern,
        grub_breakboot_char=grub_breakboot_char,
        break_count=break_count,
        timeout=timeout)

    spawn = device.spawn
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
    device = spawn.device
    credentials = device.credentials
    dialog = RommonDialog()
    dialog.dialog.process(
        spawn,
        timeout=timeout,
        context={'boot_image': golden_image[0],
                 'password': to_plaintext(credentials.get('default',{}).get('password')),
                 'username': to_plaintext(credentials.get('default',{}).get('username')),
                 'en_password': to_plaintext(credentials.get('enable',{}).get('password')),
                 'pass_login':1},
        prompt_recovery=True)


def tftp_device_recovery(spawn, timeout, device, tftp_boot, item, recovery_password=None
                        ,recovery_username=None,recovery_en_password=None, **kwargs):
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
                 'username': recovery_username,
                 'en_password': recovery_en_password,
                 'subnet_mask': tftp_boot['subnet_mask'],
                 'gateway': tftp_boot['gateway'],
                 'image': tftp_boot['image'],
                 'tftp_server': tftp_boot['tftp_server'],
                 'ether_port': tftp_boot['ether_port'],
                 'hostname': device.hostname,
                 'pass_login':1})

