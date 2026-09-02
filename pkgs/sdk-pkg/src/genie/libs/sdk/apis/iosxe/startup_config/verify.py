# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

logger = logging.getLogger(__name__)


def verify_ignore_startup_config(device):
    """ To verify ignore startup config
        Args:
            device (`obj`): Device object
        Returns:
            True or False
        Raises:
            SubCommandFailure : Failed to verify ignore startup config on the device
            ValueError : Invalid config register value
    """
    cmd = 'show version'
    
    try:
        output = device.parse(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not verify the ignore startup config on {device.name}. Error:\n{e}")
    # first check the next config register if its not there check the current config register
    config_reg = output['version'].get('next_config_register') or output['version'].get('curr_config_register')

    try:
        config_reg = int(config_reg, 16)
    except ValueError as e:
        raise ValueError(
            f"Could not convert config register value '{config_reg}' to a "
            f"hexadecimal integer. Error:\n{e}"
        )
    return config_reg & 0x40 != 0


def verify_show_startup_config_section(
        device, section=None, expect_list=None, unexpect_list=None
    ):
    '''
    Verify startup config section
    Args:
        device ('obj'): device to use
        expect_list ('list'): List of expected lines in startup config section
        unexpect_list ('list'): List of unexpected lines
                                in startup config section
    '''
    if section is None:
        res = device.execute('show startup-config')
    else:
        res = device.execute(f'show startup-config | section {section}')
    lines = res.splitlines()
    lines = [line.strip() for line in lines]
    if expect_list is not None:
        for expect_line in expect_list:
            if expect_line not in lines:
                logger.error(f"Expect '{expect_line}' "
                             "found in startup config section")
                return False
    if unexpect_list is not None:
        for unexpect_line in unexpect_list:
            if unexpect_line in lines:
                logger.error(f"Expect '{unexpect_line}' not found "
                             "in startup config section")
                return False
    return True
