'''Common verify functions for platform'''
# Python
import logging

# Genie
from genie.utils.timeout import Timeout

# Platform get
from genie.libs.sdk.apis.iosxr.platform.get import get_module_info

log = logging.getLogger(__name__)


def verify_module_serial_num(device, module, expected_serial_num, 
                             max_time=60, check_interval=20):
    ''' Verify module serial number is matched with expected number

        Args:
            device (`obj`): Device object
            module (`str`): Module name
            expected_serial_num (`str`): Expected serial number
            max_time (`int`): Max time
            check_interval (`int`): Check interval
        Returns:
            result (`bool`): Verified result
    '''
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            sn = get_module_info(device, module, key='sn')
        except Exception as e:
            log.error(e)
            timeout.sleep()
            continue

        log.info("Module {} serial number is {}, expected value is {}"
            .format(module, sn, expected_serial_num))
        if sn == expected_serial_num:
            return True
        
        timeout.sleep()
    
    return False
