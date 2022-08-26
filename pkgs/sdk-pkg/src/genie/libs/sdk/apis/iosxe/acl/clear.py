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

def clear_ip_reflexive_list(device, option='*'):
    """ #clear ip reflexive-list ?
            *     Delete all reflexive ACLs
            WORD  Delete a specific reflexive ACL
        Args:
            device (`obj`):           Device object
            option ('str'): Which data to clear. By Default will clear all reflexive-list. 
                                      For WORD need to pass reflexive-list name(eg:REF1) to delete particular reflexive-list.
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("clear ip reflexive-list on {device}".format(device=device))

    try:
        device.execute('clear ip reflexive-list {option}'.format(option=option))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear reflexive-list on {device}. Error:\n{error}".format(device=device, error=e)
        )        


def platform_software_fed_fnf_sw_stats_clear(device, switch):
    """ clear software fed fnf switch statistics
        Args:
            device (`obj`): Device object
            switch('str'): option to include switch in the CLI
        Returns: 
            None
        Raises: 
            SubCommandFailure
    """
    log.debug(" executing show platform software fed switch active fnf sw-stats-clear on device")

    if switch == '1':
      
        try:
           device.execute('show platform software fed switch active fnf sw-stats-clear'.format(device=device))

        except SubCommandFailure as e:
            raise SubCommandFailure(
            "Could not clear software fed fnf switch statistic on {device}. Error:\n{error}".format(device=device, error=e)
        )
    else:
        try:
            device.execute('show platform software fed active fnf sw-stats-clear'.format(device=device))

        except SubCommandFailure as e:
            raise SubCommandFailure(
            "Could not clear software fed fnf switch statistic on {device}. Error:\n{error}".format(device=device, error=e)
        )
