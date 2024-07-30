''' Utility functions for rommon'''

import time
import logging
log = logging.getLogger(__name__)
from pyats.log.utils import banner
# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Statement, Dialog
# Genie
from genie.libs.clean.utils import print_message


def device_rommon_boot(device, golden_image=None, tftp_boot=None, error_pattern=[]):
    '''Boot device using golden image or using tftp image
        Args:
            device: device object
            golden_image(`list`): Golden image to boot the device.
            tftp_boot:
                image(`list`): Image to boot.
                tftp_server('str'): tftp server information.

        Return:
            None
        Raise:
            Exception
    '''

    log.info(f'Get the recovery details from clean for device {device.name}')
    try:
        recovery_info = device.clean.get('device_recovery', {})
    except AttributeError:
        log.warning(f'There is no recovery info for device {device.name}')
        recovery_info = {}

    # golden_image info from device recovery
    if not golden_image:
        golden_image = recovery_info.get('golden_image', [])

    # tftp info from device recovery
    tftp_boot = tftp_boot or recovery_info.get('tftp_boot', {})
    # get the image and tftp server info
    image = tftp_boot.get('image', [])
    tftp_server = tftp_boot.get('tftp_server', "")


    # To boot using golden image
    if golden_image:
        log.info(banner("Booting device '{}' with the Golden images".\
                        format(device.name)))
        log.info("Golden image information found:\n{}".format(golden_image))
        golden_image = golden_image[0]
        cmd = f"{golden_image}"

    # To boot using tftp information
    elif tftp_server and image:
        log.info(banner("Booting device '{}' with the Tftp images".\
                        format(device.name)))
        log.info("Tftp boot information found:\n{}".format(tftp_boot))

        # To process the image path
        if image[0][0] != '/':
            image[0] = '/' + image[0]

        # To build the tftp command
        cmd_info = ("tftp://", tftp_server, image[0])
        cmd = ''.join(cmd_info)

    # To boot using tftp rommon variable
    # In this case, we assume the rommon variable TFTP_FILE is set already
    # and booting it using the "boot tftp:" command
    elif getattr(device.clean, 'images', []):
        log.warning('Assuming the rommon variable TFTP_FILE is set and boot using "boot tftp:" command')
        cmd = "tftp:"

    else:
        raise Exception('Global recovery only support golden image and tftp '
                         'boot recovery and neither was provided')

    # Timeout for device to reload
    timeout = device.clean.get('device_recovery', {}).get('timeout', 900)

    try:
        # To boot the image from rommon
        device.reload(image_to_boot=cmd, error_pattern=error_pattern, timeout=timeout)
    except Exception as e:
        log.error(str(e))
        raise Exception(f"Failed to boot the device {device.name}", from_exception=e)
    else:
        log.info(f"Successfully boot the device {device.name}")


def send_break_boot(device, console_activity_pattern='\[.*Ctrl-C.*\]',
                    console_breakboot_char='\x03', console_breakboot_telnet_break=None,
                    grub_activity_pattern=None, grub_breakboot_char=None,
                    break_count=2, timeout=60):
    """ Connects to the device, waits for the (console or grub) activity pattern and
        sends break boot character to interrupt boot. Device is expected to reach rommon state.

        Args:
            device ('obj'): Device object
            console_activity_pattern (str): Pattern to send the break at. Default to match
                                            this boot statement - Preparing to autoboot. [Press Ctrl-C to interrupt]
            console_breakboot_char (str): Character to send when console_activity_pattern is matched. Default to '\x03'.
            console_breakboot_telnet_break (bool): Use telnet `send break` to interrupt device boot. 
            grub_activity_pattern (str): Break pattern on the device for grub boot mode
            grub_breakboot_char (str): Character to send when grub_activity_pattern is matched
            break_count (int, optional): Number of break commands to send. Defaults to 2.
            timeout (int, optional): Break boot process timeout. Defaults to 60.
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    if console_activity_pattern is None and grub_activity_pattern is None:
        log.error('console_activity_pattern and grub_activity_pattern are empty, the break boot will not be effective')
    
    def telnet_breakboot(spawn, break_count):
        """ Breaks the booting process on a device using telnet `send break`

            Args:
                spawn (obj): Spawn connection object
                break_count (int): Number of break commands to send

            Returns:
                None
        """

        log.info(f"Found the console_activity_pattern! Breaking the boot process using telnet break.")

        for _ in range(break_count):
            log.info(f"Using telnet break")
            spawn.send('\x1d')
            spawn.expect(r'telnet>\s*$')
            spawn.sendline('send break')
            spawn.expect('.+')
            time.sleep(2)

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

    # setup the device connection
    device.setup_connection()

    # Get the spawn object
    spawn = device.spawn

    # connection dialog to handle the booting process
    connection_dialog = device.connection_provider.get_connection_dialog()

    # Either use break character or telnet escape break
    # break character is ctrl-c by default
    if console_activity_pattern and console_breakboot_char and not console_breakboot_telnet_break:
        connection_dialog.append(
            Statement(pattern=console_activity_pattern,
                      action=console_breakboot,
                      args={'break_count': break_count,
                            'break_char': console_breakboot_char},
                      loop_continue=True,
                      continue_timer=False))

    # telnet escape is used only if user specified
    if console_activity_pattern and console_breakboot_telnet_break:
        connection_dialog.append(
            Statement(pattern=console_activity_pattern,
                      action=telnet_breakboot,
                      args={'break_count': break_count},
                      loop_continue=True,
                      continue_timer=False))

    # grub_activity_pattern is used only if user specified
    if grub_activity_pattern and grub_breakboot_char:
        connection_dialog.append(
            Statement(pattern=grub_activity_pattern,
                      action=grub_breakboot,
                      args={'break_char': grub_breakboot_char},
                      loop_continue=True,
                      continue_timer=False))

    # Rommon >
    connection_dialog.append(
        Statement(pattern=r'^(.*)((rommon(.*))+>|switch *:).*$',
                  action=print_message,
                  args={'message': 'Device reached rommon prompt in break boot stage'},
                  trim_buffer=False))

    # grub>
    connection_dialog.append(
        Statement(pattern=r'.*grub *>.*',
                  action=print_message,
                  args={'message': 'Device reached grub prompt in break boot stage'},
                  trim_buffer=False))

    # To process the break boot dialogs
    connection_dialog.process(spawn, timeout=timeout)

    # Check the device state after breaking the boot process
    device.sendline()
    device.state_machine.go_to('any', spawn=device.spawn, context=device.default.context)
    if not device.state_machine.current_state == 'rommon':
        log.warning(f"The device {device.name} is not in rommon")
