'''Common verify functions for platform'''

# Python
import logging
import os
import re
import time

# Genie
from genie.utils import Dq
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def is_next_reload_boot_variable_as_expected(device, system, kickstart=None):

    ''' Check next boot variables
        Args:
            device ('obj'): Device object
            system ('str'): System image
            kickstart ('str'): Kickstart image
    '''

    try:
        _is_boot_variable_as_expected(device=device, system=system,
            boot_variable='next_reload_boot_variable', kickstart=kickstart)
        log.info("Successfully verified next reload boot variables")
    except Exception as e:
        log.error("Could not verify next reload boot variables due to: {e}".format(
            e=e))

def is_current_boot_variable_as_expected(device, system, kickstart=None):

    ''' Check current boot variables
        Args:
            device ('obj'): Device object
            system ('str'): System image
            kickstart ('str'): Kickstart image
    '''

    try:
        _is_boot_variable_as_expected(device=device, system=system,
            boot_variable='current_boot_variable', kickstart=kickstart)
        log.info("Successfully verified current reload boot variables")
    except Exception as e:
        raise Exception("Could not verify current reload boot variables due to: {e}".format(
            e=e))

def _is_boot_variable_as_expected(device, system, boot_variable, kickstart=None):

    ''' Check boot variables
        Args:
            device ('obj'): Device object
            system ('str'): System image
            kickstart ('str'): Kickstart image
            boot_variable ('str'): Next or current boot variables
    '''

    # Check boot variable
    try:
        output = device.parse('show boot')
    except SchemaEmptyParserError:
        raise Exception("No boot variables found on the device '{d}' "
            "to verify boot variables set".format(d=device.name))

    if 'system_variable' in output[boot_variable]:
        # case for no supervisor
        if kickstart:
            actual_kickstart = output.get(boot_variable, {}).get('kickstart_variable', None)
            if kickstart != actual_kickstart:
                raise Exception("Next reload kickstart boot variable ({a}) is not as expected ({e}) "
                                "for '{d}'".format(a=actual_kickstart, e=kickstart, d=device.name))
        actual_system = output.get(boot_variable, {}).get('system_variable', None)
        if system != actual_system:
            raise Exception("Next reload system boot variable ({a}) is not as expected ({e}) "
                            "for '{d}'".format(a=actual_system, e=system, d=device.name))
    else:
        # if there are supervisors, check if all of the boot var are changed
        for sup in output[boot_variable]['sup_number']:
            actual_kickstart = output.get(boot_variable, None).\
                                   get('sup_number', None).\
                                   get(sup, None).\
                                   get('kickstart_variable', None)
            actual_system = output.get(boot_variable, None).\
                                     get('sup_number', None).\
                                     get(sup, None).\
                                     get('system_variable', None)
            if kickstart:
                if kickstart != actual_kickstart:
                    raise Exception("Next reload kickstart boot variable ({a}) is not as expected ({e}) "
                                "for '{d}', supervisor '{s}'".format(a=actual_kickstart, e=kickstart, d=device.name, s=sup))
            if system != actual_system:
                raise Exception("Next reload system boot variable ({a}) is not as expected ({e}) "
                                "for '{d}', supervisor '{s}'".format(a=actual_system, e=system, d=device.name, s=sup))

def verify_file_exists(device, file, size=None, dir_output=None):
    """verify that the given file exist on device with the same name and size
        Args:
            device (`obj`): Device object
            file ('str'): file path on the device, i.e. bootflash:/path/to/file
            size('int'): expected file size (Optional)
            dir_output ('str'): output of dir command, if not provided execute the cmd on device to get the output
        Returns:
            Boolean value of whether file exists or not
            """

    filename = os.path.basename(file)
    directory = ''.join([os.path.dirname(file), '/'])
    dir_out = device.parse('dir {}'.format(directory), output=dir_output)
    exist = filename in dir_out.get('files',{})

    # size not provided, just check if file exists
    if not exist:
        log.info("File '{}' does not exist.".format(file))
        return exist
    elif not size:
        log.info("File name '{}' exists".format(file))
        return exist

    # File exists and check size
    file_size = int(dir_out.get('files',{}).get(filename, {}).get('size', -1))
    log.info(
        "Expected size: {} bytes, Actual size : {} bytes".format(
            size if size > -1 else 'Unknown',
            file_size if file_size > -1 else 'Unknown'))

    if size > -1 and file_size > -1:
        return size == file_size
    else:
        log.warning("File name '{}' exists, but could not verify the file size".format(
            file))
        return True

def verify_file_size_stable(device, file, max_tries=3, delay_seconds=2):
    """
    Args
        Verify if the file size is stable, not changing
        device ('obj'): Device Object
        file ('str'): file path to check the size
        max_tries('int'): number of tries to check file stability, defaults 3
        delay_seconds ('int'): time delay between tries in seconds, defaults 2
    Returns
        True if file size is stable, false otherwise
    """
    num_consecutive_equal_length_tries = 0
    result = None
    prev_result = None
    for _try in range(max_tries):
        try:
            result = int(device.api.get_file_size(file))
            if not result:
                log.warning("Failed to get file size for file :'{file}'".format(file=file))
                return False
        except Exception as exc:
            log.warning("Failed to get file size for file '{file}'"
                        " due to: {exc}".format(file=file, exc=exc))
            result = None
            prev_result = None
        else:
            # Check if first time, prev_result will be none
            # if so, then just do a +1
            # If not empty verify current result with prev result and
            # make sure they are equal
            if prev_result and result == prev_result:
                num_consecutive_equal_length_tries += 1
            else:
                num_consecutive_equal_length_tries = 1
            prev_result = result

        time.sleep(delay_seconds)

    # Verify that the last two matches
    if num_consecutive_equal_length_tries < 2:
        log.warning("The length of file {} is not stable.".format(file))
        return False
    return True

def verify_files_copied_on_standby(device, max_time=300, check_interval=20):

    '''
        Verify files transfered successfully to the standby
        Args:
            device (`obj`): Device object
            max_time ('int'): Maximum time in seconds, Default Value is 300 sec
            check_interval ('int'): Check interval in seconds, Default Value is 20 sec
        Returns:
            None
    '''

    timeout = Timeout(max_time, check_interval)

    pattern = "No file currently being auto-copied"

    while timeout.iterate():
        output = device.execute("show boot auto-copy list", prompt_recovery=True)
        if re.search(pattern, output):
            log.info("Copy Sync Completed on Standby")
            break

        timeout.sleep()
    else:
        raise Exception("Auto-Copy on standby is not yet completed")

    return

def verify_module_status(device, timeout=180, interval=30):
    ''' Check status of slot using 'show module'
        Args:
            device ('obj'): Device object
            timeout ('int'): Max timeout to re-check module status
            interval ('int'): Max interval to re-check module status
    '''

    timeout = Timeout(max_time=timeout, interval=interval)
    while timeout.iterate():
        # Reset
        failed_slots = []
        try:
            output = device.parse("show module")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Check state for all slots
        failed_slots = Dq(output).contains('status').\
                            not_contains_key_value('status',
                                                   '.*ok.*|active|standby|ha-standby|Ready',
                                                   value_regex=True).\
                            get_values('lc')
        failed_slots.extend(Dq(output).contains('status').\
                            not_contains_key_value('status',
                                                   '.*ok.*|active|standby|ha-standby|Ready',
                                                   value_regex=True).\
                            get_values('rp'))
        if not failed_slots:
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
