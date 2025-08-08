''' Utility functions for rommon'''

import time
import logging

from pyats.log.utils import banner
from pyats.utils.secret_strings import to_plaintext

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Statement, Dialog
from concurrent.futures import ThreadPoolExecutor, wait as wait_futures, ALL_COMPLETED
from unicon.plugins.iosxe.statements import grub_prompt_handler, please_reset_handler, rommon_prompt_handler

# Genie
from genie.libs.clean.utils import print_message

log = logging.getLogger(__name__)

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

        # If the length of the TFTP path is greater than the
        # imposed limit on IOSXE, boot from TFTP_FILE instead
        if len(cmd) > 199:
            log.info(f"TFTP path `{cmd}` is too long, will boot from TFTP_FILE instead")
            cmd = "tftp:"

            # Set ROMMON variables
            log.info('Setting the rommon variables for TFTP boot (device_rommon_boot)')
            try:
                if device.is_ha and hasattr(device, 'subconnections'):
                    device.api.configure_rommon_tftp_ha()
                else:
                    device.api.configure_rommon_tftp()
            except Exception as e:
                log.warning(f'Failed to set the rommon variables for device {device.name}')

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
    timeout = device.clean.get('device_recovery', {}).get('timeout', 2000)

    # Collect all connections to process
    conn_list = getattr(device, 'subconnections', None) or [device.default]

    def task(conn, cmd, timeout):
        """
        Sets the image to boot in the connection's context and transitions
        the connection's state machine to 'enable' mode.
        This function is designed to be executed concurrently for multiple connections and
        handles the necessary steps to boot the device with that image.
        """

        # statments to handle grub menu.
        def _grub_boot_device(spawn, session, context):
            # '\033' == <ESC>
            spawn.send('\033')
            time.sleep(0.5)

        grub_prompt_stmt = \
            Statement(pattern=r'.*grub *>.*',
                    action=_grub_boot_device,
                    args=None,
                    loop_continue=True,
                    continue_timer=False)

        grub_boot_stmt = \
            Statement(pattern=r'.*Use the UP and DOWN arrow keys to select.*',
                    action=grub_prompt_handler,
                    args=None,
                    loop_continue=True,
                    continue_timer=False)

        dialog = Dialog([grub_boot_stmt, grub_prompt_stmt])

        # set image to boot
        conn.context['image_to_boot'] = cmd
        conn.context['grub_boot_image'] = cmd

        # Execute config register in rommon state
        conn.device.api.execute_set_config_register(config_register='0x0')
        # Execute reset command, supported platforms: asr1k, isr4k
        conn.device.api.execute_rommon_reset()

        # bring rommon to enable state
        conn.state_machine.go_to('enable',
                            conn.spawn,
                            timeout=timeout,
                            context=conn.context,
                            dialog=dialog,
                            prompt_recovery=True)

    try:
        futures = []
        executor = ThreadPoolExecutor(max_workers=len(conn_list))
        for conn in conn_list:
            # Submit each connection's task to the executor.
            futures.append(executor.submit(
                task,
                conn,
                cmd,
                timeout,
            ))
        wait_futures(futures, timeout=timeout, return_when=ALL_COMPLETED)
    except Exception as e:
        log.error(str(e))
        raise Exception(f"Failed to boot the device {device.name}")
    else:
        log.info(f"Successfully boot the device {device.name}")

def send_break_boot(device, console_activity_pattern= None,
                    console_breakboot_char=None, console_breakboot_telnet_break=None,
                    grub_activity_pattern=None, grub_breakboot_char=None,
                    break_count=2, timeout=60):
    """ Connects to the device, waits for the (console or grub) activity pattern and
        sends break boot character to interrupt boot. Device is expected to reach rommon state.

        Args:
            device ('obj'): Device object
            console_activity_pattern (str): Pattern to send the break at. Default to match
                                            this boot statement: "...."
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

    console_activity_pattern = console_activity_pattern or r'\.\.\.\.'
    console_breakboot_char = console_breakboot_char or '\x03'

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

        log.info("Found the console_activity_pattern! Breaking the boot process.")

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
    if (device.is_ha and not getattr(device, "subconnections", None)) or \
            (not device.is_ha and not getattr(device, "spawn", None)):
        device.instantiate(connection_timeout=timeout)

    if not device.connected:
        # setup the device connection
        device.setup_connection()

    # To process the break boot dialogs
    credentials = device.credentials

    if device.is_ha and hasattr(device, 'subconnections'):
        conn_list = device.subconnections
    else:
        conn_list = [device.default]

    def get_connection_dialog(device, conn):

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

        # add the pattern for all the states for the device to connection_dialog
        for state in conn.state_machine.states:
            connection_dialog.append(
                Statement(
                    state.pattern,
                    action=print_message,
                    args={'message': f'Device reached {state} state in break boot stage'},
                )
            )

        return connection_dialog

    def task(device, con):

        dialog = get_connection_dialog(device, con)

        # check for login creds and update the cred list 
        login_creds = con.context.get('login_creds')
        if login_creds:
            con.context['cred_list'] = login_creds
        # set the buffer for each subconnection to an empty string 
        con.spawn.buffer = '' 
        
        dialog.process(
            con.spawn,
            timeout=timeout,
            context=con.context,
            prompt_recovery=True
        )

        # Check the device state after breaking the boot process
        con.sendline()
        con.state_machine.go_to('any', spawn=con.spawn, context=con.context)

        if not con.state_machine.current_state == 'rommon':
            log.warning(f"The device {device.name} is not in rommon")

        # send a new line in order to catch the buffer output in recovery process
        con.sendline()

    futures = []
    executor = ThreadPoolExecutor(max_workers=len(conn_list))

    for con in conn_list:
        futures.append(executor.submit(
            task,
            device,
            con
        ))
    wait_futures(futures, timeout=timeout, return_when=ALL_COMPLETED)
