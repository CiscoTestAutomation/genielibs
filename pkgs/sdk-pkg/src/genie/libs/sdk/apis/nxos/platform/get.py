"""Common get info functions for platform"""

# Python
import logging
import os

# pyATS
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def get_file_size(device, file):

    '''
        Get file size on the device
        Args:
            device (`obj`): Device object
            file (`str`): File name
        Returns:
            file size in `int` type or None if file size is not available
    '''

    directory = ''.join([os.path.dirname(file), '/'])
    try:
        out = device.parse("dir {}".format(directory))
    except SchemaEmptyParserError as e:
        log.error("Command 'dir' did not return any results")
    else:
        filename = os.path.basename(file)
        return int(out.get('files',{}).get(filename, {}).get('size', -1))
    return None

def get_running_image(device):

    '''
        Get running image on the device
        Args:
            device (`obj`): Device object
        Returns:
            kickstart (`str`): Kickstart image
            system (`str`): System image
    '''

    try:
        out = device.parse("show version")
        kickstart = out.get('platform').get('software').get('kickstart_image_file', None)
        system = out.get('platform').get('software').get('system_image_file')
        if kickstart:
            return [kickstart.split('/')[-1], system.split('/')[-1]]
        else:
            return [system.split('/')[-1]]
    except SchemaEmptyParserError as e:
        log.error("Command 'show version' did not return any results")
    return None

def get_available_space(device, directory='', output=None):
    """Gets available space on a given directory
        Args:
            device ('str'): Device object
            directory ('str'): directory to check spaces, if not provided it will check the
            current working directory. i.e. media:/path/to/my/dir
            output ('str'): output of dir command, if not provided execute the cmd on device to get the output
        Returns:
            space available in bytes in `int` type or None if failed to retrieve available space
    """
    try:
        dir_output = device.parse('dir {}'.format(directory), output=output)
    except Exception as e:
        log.error("Failed to parse the directory listing due to: {}".format(str(e)))
        return None

    return int(dir_output.get('disk_free_space'))


def get_total_space(device, directory='', output=None):
    """Gets total space on a given directory
        Args:
            device ('str'): Device object
            directory ('str'): directory to check spaces, if not provided it will check the
            current working directory. i.e. media:/path/to/my/dir
            output ('str'): output of dir command, if not provided execute the cmd on device to get the output
        Returns:
            space available in bytes in `int` type or None if failed to retrieve available space
    """
    try:
        dir_output = device.parse('dir {}'.format(directory), output=output)
    except Exception as e:
        log.error("Failed to parse the directory listing due to: {}".format(str(e)))
        return None

    return int(dir_output.get('disk_total_space'))