"""Common clear functions"""
# Python
import logging
import time

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

# Logger
log = logging.getLogger(__name__)

def clear_platform_software_fed_switch_active_access_security_table_counters(device,switch="active"):
    """ clear platform software fed switch active access-security table counters
        Args:
            device ('obj'): Device object
            switch ('str'): switch state is active or standby
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.execute("clear platform software fed switch {switch} access-security table counters".format(switch=switch))
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not clear active access-security table counters on device")

def clear_platform_software_fed_switch_active_access_security_auth_acl_counters(device,switch="active"):
    """ clear platform software fed switch active access-security auth-acl counters
        Args:
            device ('obj'): Device object
            switch ('str'): switch state is active or standby
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.execute("clear platform software fed switch {switch} access-security auth-acl counters".format(switch=switch))
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not clear active access-security auth-acl counters on device")
