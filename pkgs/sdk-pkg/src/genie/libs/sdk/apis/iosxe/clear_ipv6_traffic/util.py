# Python
import logging
# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)
LOG = log

def clear_ipv6_traffic(device):
    """
        clear ipv6 traffic
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubcommandFailure: Failed executing command
    """

    log.debug("clear ipv6 traffic")

    try:
        device.execute("clear ipv6 traffic")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear ipv6 traffic on {device}. Error:\n{error}".format(device=device, error=e
            )
        ) 