""" Verify type APIs for APIC """

import logging

from genie.utils.timeout import Timeout

log = logging.getLogger(__name__)

def verify_firmware_upgrade_status(device, status, firmware_group=None, max_time=90, check_interval=30):
    """ Verifies that all nodes are in the provided status.

    Args:
        device (obj): Device to execute on
        status (str): Expected status
        firmware_group (str, optional): group to filter by. Defaults to None.
        max_time (int, optional): Max time to verify. Defaults to 90.
        check_interval (int, optional): How often to recheck. Defaults to 15.

    Returns:
        (bool): True if all nodes in the expected status
                False if some nodes are not in the expected status

    Raises:
        N/A

    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():

        output = device.api.get_firmware_upgrade_status(firmware_group=firmware_group)
        if not output:
            log.warning("No upgrade information available")
            timeout.sleep()
            continue

        nodes_not_as_expected = []
        for node_id, node_status in output:
            if status.lower() != node_status.lower():
                nodes_not_as_expected.append((node_id, node_status))

        if nodes_not_as_expected:
            log.warning("These nodes are not in the expected status of "
                        "'{status}': {nodes}"
                        .format(status=status,
                                nodes=nodes_not_as_expected))
            timeout.sleep()
            continue

        return True

    return False
