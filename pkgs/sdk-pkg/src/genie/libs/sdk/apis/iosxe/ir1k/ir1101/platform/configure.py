"""IOS XE IR1101 platform configuration APIs."""


def configure_no_boot_manual(device):
    """Configure autoboot on an IR1101 device.

    IR1101 does not support the generic ``no boot manual`` command. Delegate
    to ``configure_autoboot`` to use its supported config-register behavior.

    Args:
        device (`obj`): Device object.

    Returns:
        None

    Raises:
        SubCommandFailure: If autoboot cannot be configured.
    """
    return device.api.configure_autoboot()
