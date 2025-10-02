# Python
import logging
import re

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Statement, Dialog
log = logging.getLogger(__name__)


def unconfig_trust_points(device):
    """Unconfigure trust points

    Args:
        device (`obj`): Device object
    """
    dialog = Dialog([
        Statement(
            pattern=r".*Clear all NBAR Protocol Discovery statistics\? \[yes\]",
            action="sendline(yes)",
            loop_continue=True,
            continue_timer=False,
        )
    ])
    try:
        device.execute(
            'clear ip nbar protocol-discovery',
            reply=dialog,
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear ip nbar protocol-discovery"
        )
