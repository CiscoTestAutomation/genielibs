'''IOSXE specific recovery functions'''

# Python
import logging
import time
from concurrent.futures import ThreadPoolExecutor, wait as wait_futures, ALL_COMPLETED

#unicon
from unicon.eal.dialogs import Dialog, Statement
from unicon.plugins.iosxe.statements import grub_prompt_handler

# Genie
from genie.libs.clean.exception import FailedToBootException

# Logger
log = logging.getLogger(__name__)

def recovery_worker(device, console_activity_pattern=None,
                    console_breakboot_char=None, console_breakboot_telnet_break=None,
                    grub_activity_pattern=None, grub_breakboot_char=None,
                    break_count=10, timeout=600,
                    *args, **kwargs):
    """ Starts a Spawn and processes device dialogs during recovery of a device

        Args:
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
    log.info('Breaking out of auto boot!')
    device.api.send_break_boot(
        console_activity_pattern=console_activity_pattern,
        console_breakboot_char=console_breakboot_char,
        console_breakboot_telnet_break=console_breakboot_telnet_break,
        grub_activity_pattern=grub_activity_pattern,
        grub_breakboot_char=grub_breakboot_char,
        break_count=break_count,
        timeout=timeout)
    if device.is_ha and hasattr(device, 'subconnections'):
        conn_list = device.subconnections
    else:
        conn_list = [device.default]
    
    for con in conn_list:
        if con.state_machine.current_state != 'rommon':
            raise Exception(f'Device {device.name} is not in rommon state could not recover the device.')
        else:
            log.info('Device is in rommon, Booting the device!')

    # if there is golden image in the recovery info we should boot each connection using 
    # golden image for that we need to boot each subconnetion in a separate process.
    if golden_image:=kwargs.get('golden_image'):
        futures = []
        executor = ThreadPoolExecutor(max_workers=len(conn_list))
        for con in conn_list:
            futures.append(executor.submit(
                device_recovery,
                con,
                timeout,
                golden_image,
                grub_activity_pattern
            ))
        wait_futures(futures, timeout=timeout, return_when=ALL_COMPLETED)
    elif kwargs.get('tftp_boot'):
        tftp_boot = kwargs.get('tftp_boot')

        # Retry for TFTP rommon boot if clean stage provides retry parameters
        max_attempts = kwargs.get('tftp_boot_max_attempts', 1)
        sleep_interval = kwargs.get('tftp_boot_sleep_interval', 30)

        retry_count = 0
        while retry_count < max_attempts:
            try:
                log.info(f"TFTP rommon boot attempt {retry_count + 1}/{max_attempts}")
                device.api.device_rommon_boot(tftp_boot=tftp_boot)
                log.info(f"TFTP rommon boot successful on attempt {retry_count + 1}")
                break
            except FailedToBootException as e:
                retry_count += 1
                if retry_count < max_attempts:
                    log.warning(
                        f"TFTP rommon boot failed on attempt {retry_count}/{max_attempts}. "
                        f"Error: {str(e)}. Retrying in {sleep_interval} seconds..."
                    )
                    time.sleep(sleep_interval)
                else:
                    log.error(
                        f"TFTP rommon boot failed after {max_attempts} attempts. "
                        f"Last error: {str(e)}"
                    )
                    raise


def device_recovery(con, timeout, golden_image, grub_activity_pattern):
    """ A method for processing a dialog that loads a local image onto a device

        Args:
            con (obj): connection object
            timeout (int, optional): Recovery process timeout. Defaults to 600.
            golden_image (dict): Information to load golden image on the device
            grub_activity_pattern (str): Grub activity pattern
        Returns:
            None
    """
    # if we have grup activity pattern then we need to update the context with grub boot image
    if grub_activity_pattern:
        grub_image_to_boot = con.context.get('grub_boot_image')
        con.context['grub_boot_image'] = golden_image[0]
    # check for image to boot if we have a value store it and replace it with the golden image
    image_to_boot = con.context.get('image_to_boot')
    con.context['image_to_boot'] = golden_image[0]
    # check for login creds and update the cred list 
    login_creds = con.context.get('login_creds')
    if login_creds:
        con.context['cred_list'] = login_creds
    
    # these statments needed for booting from grub menu  
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

    con.state_machine.go_to('enable',
                            con.spawn,
                            timeout=timeout,
                            context=con.context,
                            dialog = dialog,
                            prompt_recovery=True)

    # we need to set the value of grub_boot_image and image_to_boot to original value 
    if grub_activity_pattern:
         con.context['grub_boot_image'] = grub_image_to_boot
    con.context['image_to_boot'] = image_to_boot

