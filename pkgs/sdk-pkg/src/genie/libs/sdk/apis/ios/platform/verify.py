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
from genie.libs.sdk.apis.ios.platform.get import get_diffs_platform

# Logger
log = logging.getLogger(__name__)


def verify_file_exists(device, file, size=None, dir_output=None):
    '''Verify that the given file exist on device with the same name and size
        Args:
            device ('obj'): Device object
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
    try:
        dir_out = device.parse('dir {}'.format(directory), output=dir_output)
    except SchemaEmptyParserError:
        log.info(
            "Folder '{}' does not exist on {}"
            .format(directory, device.name))
        return False

    device_dir = dir_out.get('dir', {}).get('dir')

    # Check device directory
    if not device_dir:
        log.warning("Directory does not exist on {}".format(device.name))
        return False

    # Check if file exists
    exist = filename in dir_out.get('dir').get(device_dir, {}).get('files', {})

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

    if boot_images == device.api.get_boot_variables():
        log.info("Given boot images '{}' are set to 'BOOT' variable".\
                 format(boot_images))
        return True
    else:
        log.info("Given boot images '{}' are not set to 'BOOT' variable".\
                 format(boot_images))
        return False


def verify_show_boot_variable(device):
    ''' Verifies by issue 'show boot' on the device
        Args:
            None
        Return: the output
    '''
    log.info("Execute 'show boot' to verify boot variables and config-"
             "register'")
    try:
        out = device.execute('show boot')
    except Exception as e:
        log.error(str(e))

    return out
