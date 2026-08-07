from genie.libs.sdk.apis.iosxe.cat9k.rommon.utils import (
    send_break_boot as cat9k_break_boot
)


def send_break_boot(device, console_activity_pattern=None,
                    console_breakboot_char=None,
                    console_breakboot_telnet_break=None,
                    grub_activity_pattern=None,
                    grub_breakboot_char=None,
                    break_count=2, timeout=60):
    """C9800-CL (vWLC) specific send_break_boot with GRUB defaults.

    C9800-CL uses GRUB bootloader instead of traditional ROMMON.
    This sets appropriate defaults for GRUB boot interruption:
    - grub_activity_pattern: matches the GRUB autoboot countdown message
    - grub_breakboot_char: 'c' to enter GRUB command line

    Args:
        device ('obj'): Device object
        console_activity_pattern (str): Pattern for normal console boot mode
        console_breakboot_char (str): Character for normal console boot mode
        console_breakboot_telnet_break (bool): Use telnet `send break`
        grub_activity_pattern (str): Pattern for GRUB boot mode.
            Defaults to 'The highlighted entry will be
            (?:booted|executed) automatically'
        grub_breakboot_char (str): Character for GRUB boot mode.
            Defaults to 'c'
        break_count (int, optional): Number of break commands.
            Defaults to 2.
        timeout (int, optional): Break boot timeout. Defaults to 60.
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    grub_activity_pattern = (
        grub_activity_pattern
        or 'The highlighted entry will be (?:booted|executed) automatically'
    )
    grub_breakboot_char = grub_breakboot_char or 'c'

    cat9k_break_boot(
        device,
        console_activity_pattern=console_activity_pattern,
        console_breakboot_char=console_breakboot_char,
        console_breakboot_telnet_break=console_breakboot_telnet_break,
        grub_activity_pattern=grub_activity_pattern,
        grub_breakboot_char=grub_breakboot_char,
        break_count=break_count,
        timeout=timeout
    )
