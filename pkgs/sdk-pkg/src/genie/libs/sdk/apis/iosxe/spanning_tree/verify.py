import logging
import re

log = logging.getLogger(__name__)

# Unicon
from unicon.core.errors import SubCommandFailure

def verify_portfast_state(device, interface):
    '''
    Verify portfast is enabled or not on interface
    Args:
        device ('obj'): device object
        interface ('str'): interface to check
    Returns:
        result(bool): True if enabled else false
    Raises:
            SubCommandFailure: If command not executed raises subcommand failure error
    '''

    log.info('Verify portfast state')
    cmd = f'show spanning-tree interface {interface} portfast'

    try:
        sh_spanint_portfast = device.execute(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure('Could not execute CLI on {device}. Error: {error}'.format(device = device, error = e))

    state = re.search('enabled', sh_spanint_portfast)
    if state:
        log.info('Portfast is enabled on interface {}'.format(interface))
        return True
    else:
        log.info('Portfast is not enabled in interface {}'.format(interface))
        return False

