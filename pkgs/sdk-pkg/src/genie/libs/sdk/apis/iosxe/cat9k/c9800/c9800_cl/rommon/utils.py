from genie.libs.sdk.apis.iosxe.cat9k.rommon.utils import (
    send_break_boot as cat9k_break_boot
)
from genie.libs.sdk.apis.iosxe.rommon.utils import (
    device_rommon_boot as xe_generic_rommon_boot
)


def device_rommon_boot(device, golden_image=None, tftp_boot=None,
                       error_pattern=[], grub_activity_pattern=None,
                       timeout=None, *, tftp_boot_state=None):
    """Boot C9800-CL using its configured GRUB golden-image entry.

    Prefer the configured golden image over recovery TFTP metadata. Without
    a golden image, use the generic IOS-XE recovery flow.

    Args:
        device (`obj`): Device object.
        golden_image (`list`, optional): GRUB menu entries. Defaults to
            device_recovery.golden_image.
        tftp_boot (`dict`, optional): TFTP options used when no golden image is
            configured. Defaults to device_recovery.tftp_boot.
        error_pattern (`list`, optional): Boot error patterns. Defaults to [].
        grub_activity_pattern (`str`, optional): Custom GRUB activity pattern.
            Defaults to None.
        timeout (`int`, optional): Boot timeout in seconds. Defaults to the
            device_recovery timeout or 2000 seconds.
        tftp_boot_state (`dict`, optional): Transport selection cache shared
            across retries. Defaults to None.

    Returns:
        None

    Raises:
        SchemaError: Invalid TFTP image metadata.
        SubCommandFailure: A ROMMON command fails.
        FailedToBootException: The device fails to boot.
    """
    recovery_info = device.api.get_recovery_details(golden_image, tftp_boot)
    return xe_generic_rommon_boot(
        device, golden_image=recovery_info['golden_image'],
        tftp_boot=tftp_boot, error_pattern=error_pattern,
        grub_activity_pattern=grub_activity_pattern, timeout=timeout,
        tftp_boot_state=tftp_boot_state)


def send_break_boot(device, console_activity_pattern=None,
                    console_breakboot_char=None,
                    console_breakboot_telnet_break=None,
                    grub_activity_pattern=None,
                    grub_breakboot_char=None,
                    break_count=2, timeout=60):
    """C9800-CL submodel-specific send_break_boot with GRUB defaults.

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
