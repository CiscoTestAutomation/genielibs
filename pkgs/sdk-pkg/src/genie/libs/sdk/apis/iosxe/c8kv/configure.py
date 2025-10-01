from unicon.core.errors import SubCommandFailure

def configure_autoboot(device):
    """ Configure autoboot
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = 'config-reg 0x2102'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure Autoboot on c8kv device. Error:\n{e}')


def configure_no_boot_manual(device):
    """ Configure no boot
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    # Configuring no boot manual is not supported in c8kv
    # devices hence using config register
    return configure_autoboot(device=device)
