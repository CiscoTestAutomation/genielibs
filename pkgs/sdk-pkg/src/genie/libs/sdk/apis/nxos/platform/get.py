"""Common get info functions for platform"""

# Python
import os
import logging

# pyATS
from genie.metaparser.util.exceptions import SchemaEmptyParserError, SchemaMissingKeyError

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
    except Exception as e:
        log.error("Failed to parse the directory listing due to: {}".format(str(e)))
        return None

    filename = os.path.basename(file)
    size = out.get('files',{}).get(filename, {}).get('size')
    if size:
        return int(size)
    else:
        log.error("File '{}' is not found on device".format(file))


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
            return [kickstart.replace('///', '/'), system.replace('///', '/')]
        else:
            return [system.replace('///', '/')]
    except SchemaEmptyParserError as e:
        log.error("Command 'show version' did not return any results: {e}".format(e=e))
    except SchemaMissingKeyError as e:
        log.error("Missing key while parsing 'show version': {e}".format(e=e))
    except Exception as e:
        log.error("Failed to parse 'show version': {e}".format(e=e))
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

    free_space = dir_output.get('disk_free_space')
    if free_space:
        return int(free_space)
    else:
        log.error("Failed to get available space for {}".format(directory))


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