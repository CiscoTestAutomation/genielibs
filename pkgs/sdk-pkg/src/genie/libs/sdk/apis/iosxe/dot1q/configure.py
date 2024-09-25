import logging
import re
from genie.libs.parser.utils.common import Common
from unicon.eal.dialogs import Dialog, Statement
from unicon.core.errors import (
    SubCommandFailure,
    StateMachineError,
    TimeoutError,
    ConnectionError,
)

log = logging.getLogger(__name__)

def configure_vlan_dot1q_tag_native(device):
    """ configure vlan dot1q tag native
        Args:
            device ('obj')    : device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f'configure vlan dot1q tag native on {device}')
    cmd = ["vlan dot1q tag native"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure vlan dot1q tag native on {device}.Error:\n{e}')

def unconfigure_vlan_dot1q_tag_native(device):
    """ unconfigure vlan dot1q tag native
        Args:
            device ('obj')    : device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f'unconfigure vlan dot1q tag native on {device}')
    cmd = ["no vlan dot1q tag native"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not unconfigure vlan dot1q tag native on {device}.Error:\n{e}')            
            