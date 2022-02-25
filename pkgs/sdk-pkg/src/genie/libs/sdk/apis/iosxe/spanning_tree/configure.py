''' Common Config functions for IOX / app-hosting '''

import logging
import time

log = logging.getLogger(__name__)

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.utils.timeout import Timeout

def configure_spanning_tree(device, vlan_range='1-4093'):
    ''' 
    Configures spanning-tree vlan with input vlan or vlan range
    e.g.
    spanning-tree vlan 666
    spanning-tree vlan 1-999
    Args:
        device ('obj') : Device object
        vlan_range ('str'): vlan or vlan range
    Returns:
        None
    '''

    try:
        output = device.configure("spanning-tree vlan {vlan}".format(vlan=vlan_range))
        
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Configure Spanning Tree - Error:\n{error}".format(error=e)
        )

def unconfigure_spanning_tree(device, vlan_range='1-4093'):
    ''' 
    UnConfigures spanning-tree vlan with input vlan or vlan range
    e.g.
    no spanning-tree vlan 666
    no spanning-tree vlan 1-999
    Args:
        device ('obj') : Device object
        vlan_range ('str'): vlan or vlan range
    Returns:
        None
    '''

    try:
        output = device.configure("no spanning-tree vlan {vlan}".format(vlan=vlan_range))
        
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not UnConfigure Spanning Tree - Error:\n{error}".format(error=e)
        )


def configure_spanning_tree_priority(device, vlan, priority):
    '''
    Configures spanning-tree vlan with priority
    e.g.
    spanning-tree vlan 666 priority 4096
    Args:
        device ('obj') : Device object
        vlan ('str'): vlan
        priority ('int'): priority to be configured

    Returns:
        None
        
    Raise:
        SubCommandFailure: Failed configuring spanning-tree vlan with priority
    '''

    try:
        output = device.configure(f"spanning-tree vlan {vlan} priority {priority}")

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Configure Spanning Tree with priority- Error:\n{error}".format(error=e)
        )


def unconfigure_spanning_tree_priority(device, vlan, priority):
    '''
    Unconfigures spanning-tree vlan with priority
    e.g.
    no spanning-tree vlan 666 priority 4096
    Args:
        device ('obj') : Device object
        vlan ('str'): vlan
        priority ('int'): priority to be configured

    Returns:
        None
        
    Raise:
        SubCommandFailure: Failed unconfiguring spanning-tree vlan with priority
    '''

    try:
        output = device.configure(f"no spanning-tree vlan {vlan} priority {priority}")

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Unconfigure Spanning Tree with priority- Error:\n{error}".format(error=e)
        )
