"""Common configure functions for system"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure


log = logging.getLogger(__name__)


def config_license(device, license):
    """ Config license on Device

        Args:
            device (`obj`): Device object
            license (`str`): License name
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """

    try:
        device.configure("license boot level {license}".format(license=license))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure license {license}, Error: {error}'.format(
                license=license, error=e)
        )

def configure_boot_level_licence(device, nw_advantage=False, nw_essentials=False,
        nw_premier=False, addon=False, adventerprise=False, advipservices=False,
        ipbase=False):
    """ Config boot level license on Device
    Args:
        device ('obj'): Device object
        network-advantage ('bool'): boot level network-advantage
        network-essentials ('bool'): boot level network-essentials
        network-premier ('bool'): boot level network-premier
        addon ('bool'): addon option for license
        adventerprise ('bool'): boot level adventerprise
        advipservices ('bool'): boot level advipservices
        ipbase ('bool'): boot level ipbase
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring boot level license
    """
    log.info(f"Configure boot level license")

    cmd = "license boot level"
    if adventerprise:
        cmd += " adventerprise"
    elif advipservices:
        cmd += " advipservices"
    elif ipbase:
        cmd += " ipbase"
    elif nw_advantage:
        cmd += " network-advantage"
        if addon:
             cmd += " addon dna-advantage"
    elif nw_essentials:
        cmd += " network-essentials"
        if addon:
            cmd += " addon dna-essentials"
    elif nw_premier:
        cmd += " network-premier"
        if addon:
            cmd += " addon dna-premier"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
                raise SubCommandFailure(
            f"Failed to configure boot level license Error, Error:\n{e}"
        )

def configure_terminal_settings(device, length=24, width=80, **kwargs):
    '''
    Configure terminal length/width

    Args:
        device ('obj'): Device object
        length ('int'): Terminal length of the device (Default: 24)
        width ('int'): Terminal width of the device (Default: 80)
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to configure terminal setting
    '''

    cmd = [
        f"terminal length {length}",
        f"terminal width {width}"
    ]
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure terminal settings, Error:\n{e}"
        )