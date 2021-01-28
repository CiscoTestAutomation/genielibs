""" Get type APIs for APIC """

import logging

from genie.metaparser.util.exceptions import SchemaEmptyParserError

from unicon.core.errors import TimeoutError

log = logging.getLogger(__name__)

def get_aci_registered_nodes_in_state(device, state):
    """ Returns a list of node IDs that are in the provided state.

    Args:
        device (obj): Device to execute on
        state (str): State of nodes to match

    Returns:
        (list): of nodes that are in the provided state

    Raises:
        N/A
    """

    try:
        out = device.parse('acidiag fnvread')
    except (SchemaEmptyParserError, TimeoutError):
        log.warning("'acidiag fnvread' parser returned nothing")
        return []

    nodes = []

    for id_ in out['id']:
        if state == out['id'][id_].get('state', ''):
            nodes.append(id_)

    return nodes

