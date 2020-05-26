# Python
import os
import logging

# Genie
from genie.utils import Dq
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# pyATS
from pyats.utils.objects import R, find

# PLATFORM
from genie.libs.sdk.apis.iosxe.platform.get import get_diffs_platform

# Logger
log = logging.getLogger(__name__)


def is_platform_slot_in_state(device, slot, state="ok, active", max_time=1200,
    interval=120):
    """ Verify if slot is in state

        Args:
            device ('obj'): Device object
            slot ('str'): Slot number
            state ('str'): State being checked
            max_time ('int'): Max time checking
            interval ('int'): Interval checking
        Return:
            True
            False
        Raises:
            None
    """
    log.info("Verifying state of slot {slot}".format(slot=slot))
    timeout = Timeout(max_time=max_time, interval=interval)

    rs = R(["slot", slot, "rp", "(?P<val2>.*)", "state", state])

    while timeout.iterate():
        try:
            output = device.parse("show platform")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        ret = find([output], rs, filter_=False, all_keys=True)
        if ret:
            log.info(
                "Slot {slot} reached state '{state}'".format(
                    slot=slot, state=state
                )
            )
            return True

        timeout.sleep()

    return False


def verify_changes_platform(device, platform_before, platform_after,
    max_time=1200, interval=120):
    """ Verify if there are changes between outputs from 'show platform'
        Args:
            device ('obj'): Device object
            platform_before ('str'): Parsed output from 'show platform'
            platform_after ('str'): Parsed output from 'show platform'
            max_time ('int'): Max time in seconds retrying
            interval ('int'): Interval of each retry
        Return:
            True
            False
        Raises:
            None
    """

    timeout = Timeout(max_time=max_time, interval=interval)
    while timeout.iterate():
        if get_diffs_platform(
            platform_before=platform_before, platform_after=platform_after
        ):
            return True
        else:
            try:
                platform_after = device.parse("show platform")
            except SchemaEmptyParserError:
                pass

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
    exist = filename in dir_out.get('dir').get(directory).get('files')

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
        log.warning("File '{}' exists, but could not verify the file size".\
                    format(file))
        return True


def verify_boot_variable(device, boot_images, output=None):
    ''' Verifies given boot_images are set to the next-reload BOOT vars
        Args:
            device ('obj'): Device object
            boot_images ('str'): System images
    '''

    if boot_images == device.api.get_boot_variables(boot_var='next', output=output):
        log.info("Given boot images '{}' are set to 'BOOT' variable".\
                 format(boot_images))
        return True
    else:
        log.info("Given boot images '{}' are not set to 'BOOT' variable".\
                 format(boot_images))
        return False


def verify_config_register(device, config_register, next_reload=False,
    output=None):
    ''' Check current config register value
        Args:
            device ('obj'): Device object
            config_reg ('str'): Hexadecimal value of config register
    '''

    # Get config-register
    value = device.api.get_config_register(next_reload=next_reload, output=output)
    if config_register == value:
        log.info("Configuration register has been correctly set to '{}'".\
                 format(config_register))
        return True
    else:
        log.error("Configuration register value '{}' is incorrect".\
                  format(value))
        return False


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

        # Check state for all slots
        failed_slots = Dq(output).contains('state').\
                            not_contains_key_value('state',
                                                   '.*ok.*|standby|ha-standby|Ready',
                                                   value_regex=True).\
                            get_values('slot')
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
