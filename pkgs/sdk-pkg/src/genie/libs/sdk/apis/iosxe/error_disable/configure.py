''' Common Config functions for IOX / app-hosting '''

import logging
import time

log = logging.getLogger(__name__)

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.utils.timeout import Timeout


def configure_errdisable(device, recovery_cause='loopdetect', recovery_interval=60):
    ''' 
    Configures errdisable recovery cause and errdisable recovery interval
    e.g.
    errdisable recovery cause loopdetect
    errdisable recovery interval 60
    Args:
        device ('obj') : Device object
        recovery_cause ('str'): error disable recovery cause
        recovery_interval ('int'): errdisable recovery interval integer in seconds
    Returns:
        None
    '''

    try:
        output = device.configure("errdisable recovery cause {cause}".format(cause=recovery_cause))
        output = device.configure("errdisable recovery interval {interval}".format(interval=str(recovery_interval)))
        
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Configure errdisable recovery  - Error:\n{error}".format(error=e)
        )

def unconfigure_errdisable(device, recovery_cause='loopdetect'):
    ''' 
    UnConfigures errdisable recovery cause and errdisable recovery interval
    e.g.
    e.g.
    no errdisable recovery cause loopdetect
    no errdisable recovery interval
    Args:
        device ('obj') : Device object
        recovery_cause ('str'): error disable recovery cause
        recovery_interval ('int'): errdisable recovery interval integer in seconds
    Returns:
        None
    '''
    
    try:
        output = device.configure("no errdisable recovery cause {cause}".format(cause=recovery_cause))
        output = device.configure("no errdisable recovery interval")
        
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not UnConfigure errdisable recovery  - Error:\n{error}".format(error=e)
        )