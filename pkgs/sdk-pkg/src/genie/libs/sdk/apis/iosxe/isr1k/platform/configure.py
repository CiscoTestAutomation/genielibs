"""IOS XE ISR 1000 Series platform configuration APIs."""


def configure_no_boot_manual(device):
    """Configure normal autoboot on an ISR 1000 Series device.

    Uses the config-register API to set register ``0x2102``. That API selects
    ``config-register`` in IOS XE and ``confreg`` in ROMMON.

    Args:
        device (`obj`): Device object.

    Returns:
        None
    """
    return device.api.configure_autoboot()
