''' Common Config functions for asr1k'''

# Unicon
from unicon.core.errors import SubCommandFailure


def configure_boot_manual(device):
    """ Configure autoboot
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = 'config-reg 0x0'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure manual boot on device {device.name}. Error:\n{e}')
