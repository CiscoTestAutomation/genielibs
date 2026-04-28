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

def configure_ignore_startup_config(device):
    """  To configure ignore startup config.
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to configure the device
    """

    try:
        # If the device state is in rommon configure rommon variable
        if device.state_machine.current_state == 'rommon':
            cmd = 'confreg 0x2142'
            device.execute(cmd)
        else:
            cmd = 'config-register 0x2142'
            device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ignore startup config on {device.name}. Error:\n{e}")