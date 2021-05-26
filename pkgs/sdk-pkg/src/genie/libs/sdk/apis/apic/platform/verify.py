
import os
import logging

log = logging.getLogger(__name__)


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
    dir_out = device.parse('ls -l {}'.format(directory), output=dir_output)
    exist = filename in dir_out.get('files', {})

    # size not provided, just check if file exists
    if not exist:
        log.info("File '{}' does not exist.".format(file))
        return exist
    elif not size:
        log.info("File name '{}' exists".format(file))
        return exist

    # File exists and check size
    file_size = int(dir_out.get('files', {}).get(filename, {}).get('size', -1))
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