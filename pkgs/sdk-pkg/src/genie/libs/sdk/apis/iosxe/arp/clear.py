# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

log = logging.getLogger(__name__)

def clear_ip_arp_inspection_stats(device):
    """ clear ip arp inspection statistics
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("clear ip arp inspection statistics on {device}".format(device=device))

    dialog = Dialog([Statement(pattern=r'\[confirm\].*', action='sendline(\r)',loop_continue=True,continue_timer=False)])

    try:
        device.execute("clear ip arp inspection statistics", reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear ip arp inspection statistics on {device}. Error:\n{error}".format(device=device, error=e)
        )

