"""Common clear functions"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def clear_access_list_counters(device, option=''):
    """ clear access-list counters
        Args:
            device (`obj`):           Device object
            option ('str', Optional): Which data to clear. Default will clear all access-list counters or 
                                      can give access-list name(eg:input_packet) or number(eg:100)
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("clear access-list counters on {device}".format(device=device))

    try:
        device.execute('clear access-list counters {option}'.format(option=option))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear access-list counters on {device}. Error:\n{error}".format(device=device, error=e)
        )

