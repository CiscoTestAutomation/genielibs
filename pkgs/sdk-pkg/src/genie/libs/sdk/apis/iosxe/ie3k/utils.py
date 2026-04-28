"""Utility type functions that do not fit into another category"""

# Python
import logging

# unicon
from unicon.core.errors import TimeoutError


log = logging.getLogger(__name__)


def password_recovery(device, console_activity_pattern='',
                      console_breakboot_char='', console_breakboot_telnet_break=False,
                      grub_activity_pattern='', grub_breakboot_char='',
                      break_count=10, timeout=60):
    '''Attempt to recover the device after failed login attempts using credentials provided in testbed.
    
    Similar to IOS-XE implementation but with the following differences:
        - Config register cannot be set in IE3k, hence related config/verification steps are removed.

    Steps:
        1. Powercycle the device
        2. Break boot and enter rommon state
        3. Execute reset command
        4. Bring the device to enable mode
        5. Init connection settings (term length, etc.)
        6. Configure the login credentials
        7. Execute write memory

    Args:
        device ('obj'): Device object
        console_activity_pattern (str): Pattern to send the break at
        console_breakboot_char (str): Character to send when console_activity_pattern is matched
        console_breakboot_telnet_break (bool): Use telnet `send break` to interrupt device boot
        grub_activity_pattern (str): Unused.
        grub_breakboot_char (str): Unused.
        break_count (int, optional): Number of break commands to send. Defaults to 10.
        timeout (int, optional): Recovery process timeout. Defaults to 60.

    Return:
        None

    Raise:
        Exception if:
            - Failure to power cycle the device
            - Timeout occurs on breaking boot and entering rommon state
    '''

    # step:1 Powercycle the device
    # Set the "destroy" option to false when performing a power cycle for password recovery
    log.info(f'Powercycle the device {device.name}')
    device.api.execute_power_cycle_device(destroy=False)

    # step:2 Break boot and enter rommon state
    log.info(f'Breakboot to reach rommon state on {device.name}')
    try:
        device.api.send_break_boot(console_activity_pattern=console_activity_pattern,
                                   console_breakboot_char=console_breakboot_char,
                                   console_breakboot_telnet_break=console_breakboot_telnet_break,
                                   grub_activity_pattern='',
                                   grub_breakboot_char='',
                                   break_count=break_count,
                                   timeout=timeout)
    except TimeoutError as e:
        raise Exception(
            f'Password recovery could not put device {device.name} into rommon mode and '
            f'manual recovery is needed. Error:\n{e}'
        )

    # step:3 Execute reset command
    log.info(f"Executing ROMMON reset for device {device.name}")
    device.api.execute_rommon_reset()

    # step:4 Bring the device to enable mode
    if device.is_ha:
        # designate handle method will bring the device to enable mode
        device.connection_provider.designate_handles()
    else:
        device.enable()

    # step:5 Init connection settings (term length, etc.)
    log.info('Initialize connection settings')
    device.connection_provider.init_connection()

    # step:6 Configure the login credentials
    log.info(f'Configure the login credentials {device.name}')
    device.api.configure_management_credentials()

    # step:7 Execute write memory
    log.info(f'Executing write memory {device.name}')
    device.api.execute_write_memory()
