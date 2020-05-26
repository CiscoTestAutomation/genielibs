'''IOSXR verify functions for platform'''

# Python
import logging

# Genie
from genie.utils.timeout import Timeout

# Logger
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
            sn = device.api.get_module_info(module, key='sn')
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


def verify_installed_pies(device, installed_packages, max_time=300,
    check_interval=60):

    ''' Verify module serial number is matched with expected number

        Args:
            device (`obj`): Device object
            installed_packages (`list`): List of packages to verify that exist
            max_time (`int`): Maximum time to wait while checking for pies installed
                              Default 300 seconds (Optional)
          check_interval (`int`): Time interval while checking for pies installed
                                  Default 30 seconds (Optional)

        Returns:
            result (`bool`): Verified result
    '''

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():

        active_packages = device.api.get_current_active_pies()

        # Trim out active_packages
        if active_packages:
            active_packages = [item.split(":")[1] for item in active_packages]

        if set(installed_packages).intersection(active_packages):
            log.info("Installed packages {} present under 'Active Packages'".\
                    format(installed_packages))
            return True

        log.warning("Installed packages {} *not* present in 'Active Packages'"
                    "\nRe-checking after {} seconds...".\
                    format(installed_packages, check_interval))
        timeout.sleep()

    return False
