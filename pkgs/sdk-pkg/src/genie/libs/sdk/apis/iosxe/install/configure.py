# Python
import logging
import re
import time

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def install_remove_version(device, version=None, timeout=60, connect_timeout = 10):
    """
    Performs install remove for the version provided on the device
    Args:
        device ('obj'): Device object
        version ('str, optional'): Base Version to remove
        timeout ('int, optional'): Timeout value
        connect_timeout ('int, optional'): Time to wait before sending the promt
                                            (when pattern "SUCCESS: install_remove"
                                             matches)
    Returns:
        True if install remove is successful
        False if install remove is not successful
    Raises:
        SubCommandFailure
    """

    log.info(f"Performing install remove for version {version} on {device.name}")

    def slow_sendline(spawn):
            time.sleep(connect_timeout)
            spawn.sendline('')

    dialog = Dialog([
        Statement(pattern=r".*\[y/n\]",
                  action="sendline(y)",
                  args=None,
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r".*Nothing to clean\.",
                  action=None,
                  args=None,
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r"%s#" % device.name,
                  action=None,
                  args=None,
                  loop_continue=False,
                  continue_timer=False),
        Statement(pattern=r".*SUCCESS\: install_remove.*",
                  action=slow_sendline,
                  args=None,
                  loop_continue=False,
                  continue_timer=False),
    ])
    
    if version:
        cmd = f"install remove version {version}"

        try:
            output = device.execute(cmd, reply=dialog, timeout=timeout)
        except Exception as e:
            log.error(f"Error while executing {cmd} on {device.name}: {e}")
            return False

        match = re.search(r"FAILED: install_remove.*", output)
        if not match:
            log.info(f"install remove version passed on {device.name}")
            return True
        else:
            log.info(f"install remove version failed on {device.name}")
            return False

    return False

def install_autoupgrade(device):
    """ Perform install upgrade on the device
    Args:
        device ('obj'): Device object

    Returns:
        None
    Raises:
        SubCommandFailure
    """
    
    cmd = "install autoupgrade"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to install upgrade on the device. Error:\n{e}")
