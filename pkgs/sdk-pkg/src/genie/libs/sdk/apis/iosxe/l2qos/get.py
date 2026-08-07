"""Common get info functions for l2 qos"""

# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_l2qos_max_queue_number(device):
    """
    Get max queue number supported by the device for l2 qos
    Note,
        Need configure wrr queue bandwith via configure_wrr_queue_bandwidth
        api before calling this api to get correct max queue number
    Args:
        device ('obj'): Device object
    Returns:
        Max queue number (int)
    """

    out = device.api.get_show_wrr_queue_bandwidth()
    max_queue_number = len(out.get('queues', {})) if out else 0
    log.debug(f'Get device l2 qos max queue number: {max_queue_number}')
    return max_queue_number


def get_show_wrr_queue_bandwidth(device):
    """
    Get l2 qos show wrr queue bandwidth on device
    Args:
        device ('obj'): Device object
    Returns:
        Dict of wrr queue bandwidth, or None if no result, e.g.
                {
                    'enabled': True,
                    'interface_type': 'Etherswitch NGWIC',
                    'queues': {
                        1: {'bandwidth': 1},
                        2: {'bandwidth': 2},
                        3: {'bandwidth': 3},
                        4: {'bandwidth': 6},
                    },
                }
            or when disabled, e.g.
                {
                    'enabled': False,
                }
    """

    try:
        return device.parse('show wrr-queue bandwidth')
    except SchemaEmptyParserError as e:
        log.debug('Could not get device wrr-queue bandwidth, '
                  f'Error: {e}')
        return None


def get_show_wrr_queue_cos_map(device):
    """
    Get l2 qos show wrr queue cos map bandwidth on device
    Args:
        device ('obj'): Device object
    Returns:
        Dict of wrr queue cos map, or None if no result, e.g.
                {
                    'interface_type': 'Etherswitch NGWIC',
                    'cos_map': {
                        0: {'priority_queue': 1},
                        1: {'priority_queue': 5},
                        2: {'priority_queue': 3},
                        3: {'priority_queue': 4},
                        4: {'priority_queue': 5},
                        5: {'priority_queue': 6},
                        6: {'priority_queue': 7},
                        7: {'priority_queue': 8},
                    },
                }
    """

    try:
        return device.parse('show wrr-queue cos-map')
    except SchemaEmptyParserError as e:
        log.debug('Could not get device wrr-queue cos-map, '
                  f'Error: {e}')
        return None
