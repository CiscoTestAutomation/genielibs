"""Common clear functions"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement
log = logging.getLogger(__name__)
LOG = log

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


def clear_ipv6_pim_topology(device):
    """ clear ipv6 mld group
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug(f"Clear ipv6 pim topology on {device}")

    try:
        device.execute('clear ipv6 pim topology')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not clear ipv6 pim topology on {device}. Error:\n{e}"
        )

def clear_ipv6_ospf_process(device):
    """
        clear ipv6 ospf process
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubcommandFailure: Failed executing command
    """

    log.debug("Clearing ipv6 ospf process")
    dialog = Dialog([
            Statement(
            pattern=r'.*Reset selected OSPFv3 processes\?\s\[no\]\:', 
            action="sendline({val})".format(val='yes'),
            loop_continue=False,
            continue_timer=False)])
    try:
        device.execute("clear ipv6 ospf process", reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear ipv6 ospf process on {device}. Error:\n{error}".format(
                device=device, error=e
            )
        )

def clear_ipv6_neighbors(device):
    """
        clear ipv6 neighbors
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubcommandFailure: Failed executing command
    """
    log.debug("Clearing ipv6 neighbors")
    try:
        device.execute("clear ipv6 neighbors")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to clear ipv6 neighbors on {device}. Error:\n{e}")