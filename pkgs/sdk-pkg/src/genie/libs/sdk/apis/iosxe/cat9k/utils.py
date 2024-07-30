''' Utility functions for iosxe/cat9k'''

import logging
log = logging.getLogger(__name__)

# unicon
from unicon.core.errors import TimeoutError

def password_recovery(device, console_activity_pattern=None,
                      console_breakboot_char=None, console_breakboot_telnet_break=None,
                      grub_activity_pattern=None, grub_breakboot_char=None,
                      break_count=10, timeout=60):
    '''Recover the device by power cycling, breaking boot to reach rommon state,
       set variable to ignoring the startup configuration and boot device,
       re-configures credentials and saves the configuration.

       Args:
            device ('obj'): Device object
            console_activity_pattern (str): Pattern to send the break at
            console_breakboot_char (str): Character to send when console_activity_pattern is matched
            console_breakboot_telnet_break (bool): Use telnet `send break` to interrupt device boot
            grub_activity_pattern (str): Break pattern on the device for grub boot mode
            grub_breakboot_char (str): Character to send when grub_activity_pattern is matched
            break_count (int, optional): Number of break commands to send. Defaults to 10.
            timeout (int, optional): Recovery process timeout. Defaults to 60.
        Return:
            None
        Raise:
            Exception
    '''

    # step:1 Powercycle the device
    log.info(f'Powercycle the device {device.name}')
    device.api.execute_power_cycle_device()

    # step:2 Break boot and enter rommon state
    log.info(f'Breakboot to reach rommon state on {device.name}')
    try:
        device.api.send_break_boot(console_activity_pattern=console_activity_pattern,
                                console_breakboot_char=console_breakboot_char,
                                console_breakboot_telnet_break=console_breakboot_telnet_break,
                                grub_activity_pattern=grub_activity_pattern,
                                grub_breakboot_char=grub_breakboot_char,
                                break_count=break_count,
                                timeout=timeout)
    except TimeoutError as e:
        raise Exception(
            f'Password recovery could not put device {device.name} into rommon mode and '
            f'manual recovery is needed. Error:\n{e}'
            )

    # Device is assumed to be in rommon mode
    # step:3 Configure the ignore startup config
    log.info(f'Configure the ignore startup config on the device {device.name}')
    device.api.configure_ignore_startup_config()

    # step:4 Bring the device to enable mode
    device.enable()

    # step:5 Configure the login credentials
    log.info(f'Configure the login credentials {device.name}')
    device.api.configure_management_credentials()

    # step:6 Unconfigure the ignore startup config
    log.info(f'Unconfigure the ignore startup config')
    device.api.unconfigure_ignore_startup_config()

    # step:7 verify the rommon variable
    log.info(f'verify the ignore startup config')
    if not device.api.verify_ignore_startup_config():
        raise Exception(f"Failed to unconfigure the ignore startup config on {device.name}")

    # step:8 Execute write memory
    log.info(f'Executing write memory')
    device.api.execute_write_memory()
