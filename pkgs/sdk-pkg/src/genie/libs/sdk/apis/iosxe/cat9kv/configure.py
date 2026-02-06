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
        raise SubCommandFailure(
            "Could not configure autoboot on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_boot_manual(device):
    """ boot manual
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure('boot manual')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not config boot manual on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_no_boot_manual(device):
    """ no boot manual
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure('no boot manual')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not remove boot manual config on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )
