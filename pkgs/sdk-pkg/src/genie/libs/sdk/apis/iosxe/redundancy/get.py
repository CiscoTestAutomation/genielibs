# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_redundancy_operational_state(device):
    """ Get redundancy states of device
        Args:
            device ('obj'): Device object
        Returns:
            String: Redundancy state
            None
        Raises:
            None
    """

    try:
        output = device.parse("show redundancy states")
    except SchemaEmptyParserError:
        log.info(
            "Command 'show redundancy states' has " "not returned any results"
        )
        return None

    redundancy_state = output.get("redundancy_state", None)

    if redundancy_state:
        log.info(
            "Found redundancy state {state} on device {dev}".format(
                state=redundancy_state, dev=device.name
            )
        )
    else:
        log.info(
            "Could not find any redundancy state on device {dev}".format(
                dev=device.name
            )
        )

    return redundancy_state
