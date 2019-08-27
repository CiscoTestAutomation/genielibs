# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils.timeout import Timeout

# REDUNDANCY
from genie.libs.sdk.apis.iosxe.redundancy.get import (
    get_redundancy_operational_state,
)

log = logging.getLogger(__name__)


def is_redundancy_state_in_state(
    device, expected_state, max_time=500, check_interval=5, output=""
):
    """ Verify if redundancy state is in state:
        Args:
            device ('obj'): Device object
            output ('dict'): Parsed output of show redundancy state
            expected_state ('str'): Expected state
            max_time ('int'): Max time in seconds to check redundancy state
            check_interval ('int'): Interval in seconds between each check
        Returns:
            True
            False
        Raises:
            None
    """

    if not output:
        redundancy_state = get_redundancy_operational_state(device=device)

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():

        if redundancy_state == expected_state:
            log.info(
                "Redundancy state on device {dev} is {state}".format(
                    dev=device.name, state=redundancy_state
                )
            )
            return True

        log.info(
            "Redundancy state in device {dev} is {state}.\n"
            "Expected {expected_state}".format(
                dev=device.name,
                state=redundancy_state,
                expected_state=expected_state,
            )
        )

        redundancy_state = get_redundancy_operational_state(device=device)

        timeout.sleep()

    log.error(
        "Redundancy state in device {dev} is {state}.\n"
        "Expected {expected_state}".format(
            dev=device.name,
            state=redundancy_state,
            expected_state=expected_state,
        )
    )

    return False
