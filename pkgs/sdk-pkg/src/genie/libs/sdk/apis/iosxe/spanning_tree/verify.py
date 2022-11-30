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

def verify_spanning_tree_root_inc(device, vlan_id, interface):
    '''
    Verify spanning tree root inconsistancy is enabled on interface
    Args:
        device ('obj'): device object     
        vlan_id ('str'): Vlan id on the interface
        interface ('str'): interface to check

    Returns:
        result(bool): True if enabled else false
    Raises:
            SubCommandFailure: If command not executed raises subcommand failure error
    '''

    log.info('Verify spanning tree root inconsistancy')
    cmd = f'show spanning-tree vlan {vlan_id} interface {interface} inconsistency'

    try:
        sh_root_inc = device.execute(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure('Could not execute CLI on {device}. Error: {error}'.format(device = device, error = e))

    inconsistancy = re.search('Root', sh_root_inc)
    if inconsistancy:
        log.info('Root inconsistancy is enabled on interface {}'.format(interface))
        return True
    else:
        log.info('Root inconsistancy is not enabled in interface {}'.format(interface))
        return False

def verify_spanning_tree_loop_inc(device, vlan_id, interface):
    '''
    Verify spanning tree loop inconsistancy is enabled on interface
    Args:
        device ('obj'): device object     
        vlan_id ('str'): Vlan id on the interface
        interface ('str'): interface to check
    Returns:
        result(bool): True if enabled else false
    Raises:
            SubCommandFailure: If command not executed raises subcommand failure error
    '''

    log.info('Verify spanning tree loop inconsistancy')
    cmd = f'show spanning-tree vlan {vlan_id} interface {interface} inconsistency'

    try:
        sh_loop_inc = device.execute(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure('Could not execute CLI on {device}. Error: {error}'.format(device = device, error = e))

    inconsistancy = re.search('Loop', sh_loop_inc)
    if inconsistancy:
        log.info('Loop inconsistancy is enabled on interface {}'.format(interface))
        return True
    else:
        log.info('Loop inconsistancy is not enabled in interface {}'.format(interface))
        return False

