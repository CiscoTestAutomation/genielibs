
from genie.libs.sdk.apis.iosxe.rommon.utils import send_break_boot as xe_generic_break_boot


def send_break_boot(device, console_activity_pattern=None,
                    console_breakboot_char=None, console_breakboot_telnet_break=None,
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
    console_activity_pattern = console_activity_pattern or r'\[.*Ctrl-C.*\]'
    console_breakboot_char = console_breakboot_char or '\x03'

    xe_generic_break_boot(device, console_activity_pattern=console_activity_pattern,
                    console_breakboot_char=console_breakboot_char, console_breakboot_telnet_break=console_breakboot_telnet_break,
                    grub_activity_pattern=grub_activity_pattern, grub_breakboot_char=grub_breakboot_char,
                    break_count=break_count, timeout=timeout)