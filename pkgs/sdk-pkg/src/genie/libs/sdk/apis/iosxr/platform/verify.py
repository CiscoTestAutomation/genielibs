'''Common verify functions for platform IOSXR'''
# Python
import logging
import os

# Genie
from genie.utils import Dq
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Logger
log = logging.getLogger()


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
            sn = device.api.get_module_info(device, module, key='sn')
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


def verify_file_exists(device, file, size=None, dir_output=None):
    '''Verify that the given file exist on device with the same name and size
        Args:
            device (`obj`): Device object
            file ('str'): File path on the device, i.e. bootflash:/path/to/file
            size('int'): Expected file size (Optional)
            dir_output ('str'): Output of 'dir' command
                            if not provided, executes the cmd on device
        Returns:
            Boolean value of whether file exists or not
    '''
    filename = os.path.basename(file)
    directory = ''.join([os.path.dirname(file), '/'])

    # 'dir' output
    dir_out = device.parse('dir {}'.format(directory), output=dir_output)

    # Check if file exists
    exist = filename in dir_out.get('dir').get('files')

    if not exist:
        log.info("File '{}' does not exist on {}".format(file, device.name))
        return exist
    elif not size:
        # Size not provided, just check if file exists
        log.info("File name '{}' exists on {}".format(file, device.name))
        return exist

    # Get filesize from output
    file_size = device.api.get_file_size(file=file, output=dir_output)

    # Check expected vs actual size
    log.info("Expected size: {} bytes, Actual size : {} bytes".format(
             size if size > -1 else 'Unknown',
             file_size if file_size > -1 else 'Unknown'))

    # Check file sizes match
    if size > -1 and file_size > -1:
        return size == file_size
    else:
        log.warning("File '{}' exists, but could not verify the file size".
                    format(file))
        return True

def verify_module_status(device, timeout=180, interval=30):
    ''' Check status of slot using 'show platform'
        Args:
            device ('obj'): Device object
            timeout ('int'): Max timeout to re-check slot status
            interval ('int'): Max interval to re-check slot status
    '''

    timeout = Timeout(max_time=timeout, interval=interval)
    while timeout.iterate():
        # Reset
        failed_slots = []
        try:
            output = device.parse("show platform")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        failed_slots = Dq(output).\
                    contains_key_value('state','IOS XR RUN', value_regex=True)

        if failed_slots:
            log.info("All modules on '{}' are in stable state".\
                     format(device.name))
            break
        else:
            log.warning("The following modules are not in stable state {}".\
                        format(failed_slots))
            log.warning("Sleeping {} seconds before rechecking".format(interval))
            timeout.sleep()
            continue
    else:
        raise Exception("Modules on '{}' are not in stable state".\
                        format(device.name))

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
