from genie.libs.sdk.apis.iosxe.ie3k.utils import (
    password_recovery as ie3k_password_recovery
)


def password_recovery(device, console_activity_pattern='',
                      console_breakboot_char='', console_breakboot_telnet_break=False,
                      grub_activity_pattern='', grub_breakboot_char='',
                      break_count=10, timeout=60):
    '''Attempt to recover the device after failed login attempts using credentials provided in testbed.

    IE9k is similar to IE3k, hence reusing IE3k's implementation.

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
    ie3k_password_recovery(
        device=device,
        console_activity_pattern=console_activity_pattern,
        console_breakboot_char=console_breakboot_char,
        console_breakboot_telnet_break=console_breakboot_telnet_break,
        grub_activity_pattern=grub_activity_pattern,
        grub_breakboot_char=grub_breakboot_char,
        break_count=break_count,
        timeout=timeout
    )