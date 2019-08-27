"""Common get functions for VIRL STD"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.utils.timeout import Timeout
from genie.libs.sdk.apis.virl.std.get import get_node_summary, get_simulations

log = logging.getLogger(__name__)


def verify_node_reachable(
    device, simulation_name, node_name=None, max_time=300, check_interval=15
):
    """Verify node reachable

        Args:
            device (`obj`): Device object
            simulation_name ('str'): simulation name
            node_name ('str'): node name
            max_time (`int`): maximum wait time in seconds. Default: 300
            check_interval (`int`): Wait time between iterations when looping\
                 is needed in secnods. Default: 15

        Returns:
            boolean: True/False
        
        Raise:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        nodes = []
        if node_name:
            nodes.append(node_name)
        else:
            nodes = get_node_summary(device, simulation_name)
        for node in nodes:
            if nodes[node]["state"] != "reachable":
                break
        else:
            return True
        timeout.sleep()
    return False


def verify_node_state(
    device,
    simulation_name,
    node_name=None,
    max_time=300,
    check_interval=15,
    state="ACTIVE",
):
    """Verify node reachable

        Args:
            device (`obj`): Device object
            simulation_name ('str'): simulation name
            node_name ('str'): node name
            max_time (`int`): maximum wait time in seconds. Default: 300
            check_interval (`int`): Wait time between iterations when looping\
                 is needed in secnods. Default: 15
            state (`str`): state to verify

        Returns:
            state ('str'): node state
        
        Raise:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        nodes = []
        if node_name:
            nodes.append(node_name)
        else:
            nodes = get_node_summary(device, simulation_name)
        for node in nodes:
            if nodes[node]["state"] != state:
                break
        else:
            return True
        timeout.sleep()
    return False


def verify_simulation(
    device, simulation_name, max_time=60, check_interval=10, exist=True
):
    """Verify if simulation exists

        Args:
            device (`obj`): Device object
            simulation_name (`str`): simulation name
            max_time (`int`): maximum wait time in seconds. Default: 60
            check_interval (`int`): Wait time between iterations when looping\
                 is needed in secnods. Default: 10
            exist (`Bool`): True if simulation exists. False for opposite check.

        Returns:
            Bool: True/False
        Raise:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        simulations = get_simulations(device)
        if exist:
            if simulation_name in simulations:
                return True
        else:
            if simulation_name not in simulations:
                return True
        timeout.sleep()
    return False
