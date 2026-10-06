"""Common verify functions for running-config"""

# Python
import logging


log = logging.getLogger(__name__)


def verify_show_running_config_section(
        device, section=None, expect_list=None, unexpect_list=None
    ):
    '''
    Verify running config section
    Args:
        device ('obj'): device to use
        section ('str', optional): only show the configuration with 'section'
            string included. Like a filtering. Default to None.
        expect_list ('list', optional): List of expected lines in show running
            output. Default to None
        unexpect_list ('list', optional): List of unexpected lines in show
            running output. Default to None
    Returns:
        a bool value: True or False.
    '''
    if section is None:
        res = device.execute('show running-config')
    else:
        res = device.execute(f'show running-config | section {section}')
    lines = res.splitlines()
    lines = [line.strip() for line in lines]
    if expect_list is not None:
        for expect_line in expect_list:
            if expect_line not in lines:
                log.debug(f"Not found the expected '{expect_line}' "
                          "in running config section")
                return False
    if unexpect_list is not None:
        for unexpect_line in unexpect_list:
            if unexpect_line in lines:
                log.debug(f"Found the unexpected '{unexpect_line}' "
                          "in running config section")
                return False
    return True
