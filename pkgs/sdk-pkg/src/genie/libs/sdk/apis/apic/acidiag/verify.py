""" Verify type APIs for APIC """

import logging

from genie.utils.timeout import Timeout

log = logging.getLogger(__name__)


def verify_aci_registered_nodes_in_state(device, node_ids, state, max_time=90,
                                         check_interval=15):
    """ Verifies that a provided list of Node IDs are in the provided state.

    Args:
        device (obj): Device to execute on
        node_ids (list): List of node IDs to verify
        state (str): State of nodes to match
        max_time (int, optional): Max time to verify. Defaults to 90.
        check_interval (int, optional): How often to recheck. Defaults to 15.

    Returns:
        (bool): True if all nodes provided are in the correct state
                False if some nodes provided are in the wrong state

    Raises:
        N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():

        nodes_in_state = device.api.get_aci_registered_nodes_in_state(state=state)
        if not nodes_in_state:
            log.info("No nodes are in '{state}' state".format(state=state))
            timeout.sleep()
            continue

        if set(node_ids).issubset(set(nodes_in_state)):
            return True

        log.warning("The following node IDs are not in '{state}': {nodes}".format(
            state=state, nodes=set(node_ids)-set(nodes_in_state)))

        timeout.sleep()
        continue

    return False

