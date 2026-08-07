"""Common verify functions for l2 qos"""

# Python
import logging

log = logging.getLogger(__name__)


def verify_wrr_queue_enabled(device, wrr_queue_enabled=False):
    """
    Verify l2 qos wrr queue enabled
    Args:
        device ('obj'): Device object
        wrr_queue_enabled ('bool'): Expect wrr queue status, True or False
    Returns:
        True/False
    """

    res = device.api.get_show_wrr_queue_bandwidth()
    if res is None:
        return False
    if res.get('enabled') != wrr_queue_enabled:
        return False
    return True


def verify_wrr_queue_bandwidth(device, wrr_queue_id, bandwidth):
    """
    Verify l2 qos wrr queue bandwidth
    Args:
        device ('obj'): Device object
        wrr_queue_id ('int'): Wrr queue id to verify
        bandwidth ('int'): Expect wrr queue bandwidth of the queue id
    Returns:
        True/False
    """

    res = device.api.get_show_wrr_queue_bandwidth()
    if res is None:
        return False
    if res.get('enabled') is False:
        return False
    actual_bandwidth = res.get('queues', {}).get(wrr_queue_id, {}).get(
        'bandwidth')
    if actual_bandwidth != bandwidth:
        log.debug(f'wrr queue id {wrr_queue_id} bandwidth expect '
                  f'{bandwidth} got {actual_bandwidth}')
        return False
    return True


def verify_wrr_queue_cos_map(device, cos_value, queue_id):
    """
    Verify l2 qos wrr queue cos map
    Args:
        device ('obj'): Device object
        cos_value ('int'): Cos value, 0..7
        queue_id ('int'): Expect queue id to map
    Returns:
        True/False
    """

    res = device.api.get_show_wrr_queue_cos_map()
    if res is None:
        return False
    actual_queue_id = res.get('cos_map', {}).get(cos_value, {}).get(
        'priority_queue')
    if actual_queue_id != queue_id:
        log.debug(f'wrr cos value {cos_value} expect map to queue '
                  f'{queue_id} got {actual_queue_id}')
        return False
    return True
