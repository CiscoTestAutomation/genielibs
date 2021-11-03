"""Common clear functions"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def clear_ipv6_mfib_vrf_counters(device, vrf_name=''):
    """ clear ipv6 mfib vrf * counters
        Args:
            device (`obj`):             Device object
            vrf_name ('str', optional): VRF name. Default will clear all vrf counters
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Clearing ipv6 mfib vrf counters on {device}".format(device=device))

    try:
        if not vrf_name:
            device.execute("clear ipv6 mfib vrf * counters")
        else:
            device.execute("clear ipv6 mfib vrf {vrf_name} counters".format(vrf_name=vrf_name))

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear ipv6 mfib vrf counters on {device}. Error:\n{error}".format(device=device, error=e)
        )
       
def clear_ipv6_mld_group(device):
    """ clear ipv6 mld group
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Clear ipv6 mld group on {device}".format(device=device))

    try:
        device.execute('clear ipv6 mld group')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear ipv6 mld group on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )
