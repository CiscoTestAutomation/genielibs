''' Common Config functions for IOX / app-hosting '''

import logging
import time

log = logging.getLogger(__name__)

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.utils.timeout import Timeout


def enable_usb_ssd(device, timeout=30):
    ''' 
    Configure - no platform usb disable
    Enables connected SSDs on c9300
    Args:
        device ('obj') : Device object
        timeout ('int'): timeout arg for Unicon configure for this CLI
    Returns:
        None
    '''
    
    try:
        output = device.configure("no platform usb disable" , timeout=timeout)
        
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable USB SSD - Error:\n{error}".format(error=e)
        )
        
def disable_usb_ssd(device, timeout=30):
    ''' 
    Configure - platform usb disable
    Disables connected SSDs on c9300
    Args:
        device ('obj') : Device object
        timeout ('int'): timeout arg for Unicon configure for this CLI
    Returns:
        None
    '''
    
    try:
        output = device.configure("platform usb disable" , timeout=timeout)
        
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disable USB SSD - Error:\n{error}".format(error=e)
        )

def clear_iox(device, max_time=120, interval=10, disable_iox_then_clear=False,wait_timer=30,timeout=30):
    ''' 
    Execute clear iox
    Uses disable_iox
    Args:
        device ('obj') : Device object
        max_time ('int') : max time to wait
        interval ('int') : interval timer
        disable_iox_then_clear ('boolean') : Disable IOX then clear
        wait_timer ('int') : wait timer after disable IOX if disable_iox_then_clear
        timeout ('int'): timeout arg for Unicon execute for this CLI
    Returns:
        True
        False
    Raises:
        None    
    '''
    
    time_out = Timeout(max_time=max_time, interval=interval)
    while time_out.iterate():
        try:
            output = device.execute("clear iox" , timeout=timeout)
            if 'IOX cleanup successfully completed' in output:
                return True        
            elif 'IOX is configured/UP. IOX must be disabled before invoking this command' in output:
                if disable_iox_then_clear:                
                    log.info("User requested unconfigure IOX then clear IOX")
                    device.api.disable_iox()
                    log.info('Wait %s seconds after Disable IOX' % wait_timer)
                    time.sleep(wait_timer)            
        except SubCommandFailure as e:
            raise SubCommandFailure(
                "Could not clear IOX - Error:\n{error}".format(error=e)
            )
    return False

def enable_iox(device):
    ''' 
    Configure iox    
    Args:
        device ('obj') : Device object
    Returns:
        None
    '''
    try:
        device.configure("iox")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable IOX - Error:\n{error}".format(error=e)
        )
    
def disable_iox(device):
    ''' 
    Configure no iox    
    Args:
        device ('obj') : Device object
    Returns:
        None
    '''
    try:
        device.configure("no iox")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disable IOX - Error:\n{error}".format(error=e)
        )
