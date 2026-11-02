from genie.libs.sdk.apis.iosxe.rommon.utils import (
    send_break_boot as xe_generic_break_boot,
)


def send_break_boot(device, console_activity_pattern=None,
                    console_breakboot_char=None,
                    console_breakboot_telnet_break=None,
                    grub_activity_pattern=None, grub_breakboot_char=None,
                    break_count=2, timeout=60):
    """Interrupt Cat8k boot and leave the device at the ROMMON prompt.

    Cat8k platforms require a Telnet BREAK after the system bootstrap banner.
    The remaining arguments are passed to the generic IOS XE implementation.
    Exceptions raised by that implementation are propagated unchanged.

    Args:
        device ('obj'): Device object.
        console_activity_pattern (str): Pattern that marks when to interrupt
            boot. Defaults to the system bootstrap banner.
        console_breakboot_char (str): Console break character.
        console_breakboot_telnet_break (bool): Ignored for Cat8k; Telnet BREAK
            is always used.
        grub_activity_pattern (str): GRUB activity pattern.
        grub_breakboot_char (str): Character used to interrupt GRUB.
        break_count (int): Number of Telnet BREAK commands. Defaults to 2.
        timeout (int): Break boot timeout in seconds. Defaults to 60.

    Returns:
        None: This API does not return a value.

    Raises:
        SubCommandFailure: If the generic IOS XE break-boot operation fails.
    """
    console_activity_pattern = (
        console_activity_pattern or r'.*System Bootstrap, Version.*'
    )

    xe_generic_break_boot(
        device,
        console_activity_pattern=console_activity_pattern,
        console_breakboot_char=console_breakboot_char,
        console_breakboot_telnet_break=True,
        grub_activity_pattern=grub_activity_pattern,
        grub_breakboot_char=grub_breakboot_char,
        break_count=break_count,
        timeout=timeout,
    )
