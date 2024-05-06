"""Common clear functions for GETVPN"""

# Python
from unicon.eal.dialogs import Statement, Dialog
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def clear_crypto_gkm(device,
                     group='',
                     timeout=30):
    """ clear_crypto_gkm
        Args:
            device (`obj`): Device object
            group ('str', optional): Name for the GetVpn Gdoi group
            timeout('int', optional): timeout for exec command execution, default is 30
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    dialog = Dialog([
                Statement(pattern=r'^.*Are you sure you want to proceed.*\[yes\/no\].*$',
                    action=f'sendline(yes)',
                    loop_continue=True,
                    continue_timer=False)
            ])

    log.info("clear crypto gkm")
    
    cmd = []

    if not group:
        cmd = f"clear crypto gkm"
    else:
        cmd = f"clear crypto gkm group {group}"

    try:    
        device.execute(cmd, 
            reply=dialog, 
            timeout=timeout)
    
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear crypto gkm on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )
