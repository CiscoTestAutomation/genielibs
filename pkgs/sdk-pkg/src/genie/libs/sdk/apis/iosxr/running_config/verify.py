'''Common verify functions for running-config'''
# Python
import logging

# Genie
from genie.utils.timeout import Timeout

# running-config get
from genie.libs.sdk.apis.iosxr.running_config.get import \
        get_running_config_hostname

log = logging.getLogger(__name__)


def verify_hostname(device, expected_hostname, max_time=60, check_interval=20):
    ''' Verify hostname is matched with expected name

        Args:
            device (`obj`): Device object
            expected_hostname (`str`): Expected hostname
            max_time (`int`): Max time
            check_interval (`int`): Check interval
        Returns:
            result (`bool`): Verified result
    '''
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            name = get_running_config_hostname(device)
        except Exception as e:
            log.error(e)
            timeout.sleep()
            continue

        log.info("Device hostname is {}, expected value is {}"
            .format(name, expected_hostname))
        if name == expected_hostname:
            return True
        
        timeout.sleep()
    
    return False
