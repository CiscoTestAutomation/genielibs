''' Common Execute functions for IOX / app-hosting '''

# Python
import logging
import re
import time

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure

# Import parser
from genie.utils.timeout import Timeout

log = logging.getLogger(__name__)

def execute_install_application_bootflash(device, app_id, package_name, timeout=60, wait_timer=10):
    """
        Performs install application from bootflash
        Args:
            device ('obj'): Device object
            app_id ('str'): Application id name
            package_name ('str'): Name of the Application package in bootflash to install 
            timeout ('int, optional'): Timeout value ( default 60)
            wait_timer ('int, optional'): Time to wait before sending the result ( default 10 )
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"app-hosting install appid {app_id} "
    
    #Package name 
    if package_name :
        cmd += f"package bootflash:{package_name}"
    log.info(f"Performing {cmd} on device {device.name}")

    try:   
        device.execute(cmd, timeout=timeout)       
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Error while executing {cmd} on {device.name}:\n {e}'
        )

    log.info(f"Waiting for {wait_timer} seconds ")
    time.sleep(wait_timer)


def execute_guestshell_enable(device, timeout=60):
    """
        Execute guestshell enable
        Args:
            device ('obj'): Device object
            timeout ('int'): timout in seconds
        Returns:
            None
        Raises:
            SubCommandFailure
        
    """
    cmd = 'guestshell enable'
    try:
        device.execute(cmd, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not execute guestshell enable. Error {e}")


def execute_app_hosting_appid(device, appid, action, package_path=None):
    """ Execute app-hosting appid
        Args:
            device ('obj'): device to use
            appid ('str') : appid to configure
            action ('str'): app-hosting action. Ex: start, install, etc
            package_path ('str', optional): package install file path. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f"app-hosting {action} appid {appid}{f' package {package_path}' if package_path else ''}"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not execute app-hosting appid. Error: {e}')
