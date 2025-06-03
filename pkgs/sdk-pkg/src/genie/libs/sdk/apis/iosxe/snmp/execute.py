'''IOSXE execute functions for snmp'''

# Python
import logging

# Genie
from genie.utils import Dq

# Unicon
from genie.metaparser.util.exceptions import (SchemaEmptyParserError,
                                              SchemaMissingKeyError)
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

def configure_switch_priority(device, switch, priority):
    """ Configures priority for a switch
        Example : switch 2 priority 13

        Args:
            device ('obj'): device to use
            switch ('int'): Switch Number (1-16)
            priority ('int'): Switch Priority (1-15)
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Configures switch {switch} with priority {priority} on {device.name}')
    cmd = f'switch {switch} priority {priority}'
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to configure switch {switch} priority {priority} on {device.name}. Error:\n{e}'
        )

def execute_show_snmp(device, subcommand):
    """
    Executes a given 'show snmp' command on a device .

    Args:
        device ('obj'): device to execute the command on.
        subcommand ('str'): Subcommand to append after 'show snmp'.

    Returns:
        str: Output from the device.
    """
    cmd = f'show snmp {subcommand}'
    try:
        return device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to execute command {cmd} on {device.name}. Error:\n{e}'
        )