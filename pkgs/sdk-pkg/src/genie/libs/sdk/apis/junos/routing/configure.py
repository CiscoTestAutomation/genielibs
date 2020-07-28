"""Common configure functions for routing"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def restart_routing(device):
    """API for restarting routing

    Args:
        device (obj): Restarts routing process

    Returns:
        None
    """

    try:
        device.execute('restart routing')
    except SubCommandFailure as e:
        log.info("Sub command error when restarting routing {e}".format(e=e))
        raise
    except Exception as e:
        log.info("General error when restarting routing {e}".format(e=e))
        raise