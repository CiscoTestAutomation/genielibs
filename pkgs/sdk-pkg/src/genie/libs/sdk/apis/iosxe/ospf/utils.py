"""Utility type functions for OSPF"""
# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement
log = logging.getLogger(__name__)


def clear_ip_ospf_process(device):
    """Clear Ip Ospf process
       Args:
            device('obj'): device object
       Returns:
            None
       Raises:
            SubCommandFailure
    """

    dialog = Dialog(
        [
            Statement(
                pattern=r".*Reset ALL OSPF processes\? \[no\]:.*",
                action=lambda spawn: spawn.sendline('yes'),
                loop_continue=False,
                continue_timer=False
            ),
            Statement(
                pattern=f".*{device.name}#$",
                action=None,
                loop_continue=False,
                continue_timer=False
            )
        ]
    )
    try:
        device.execute("clear ip ospf process", reply=dialog, timeout=60)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to clear IP OSPF Process\n{e}'
        )

def clear_ip_ospf_rib(device):
    """Clear Ip Ospf rib
       Args:
            device('obj'): device object
       Returns:
            None
       Raises:
            SubCommandFailure
    """
    try:
        device.execute("clear ip ospf rib")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to clear IP OSPF RIB\n{e}'
        )