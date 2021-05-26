
import logging

log = logging.getLogger(__name__)


def get_available_space(device, directory, output=None):
    """Gets available space on a given directory
        Args:
            device ('str'): Device object
            directory ('str'): directory to check spaces, i.e. media:/path/to/my/dir
            output ('str'): output of dir command, if not provided execute the cmd on device to get the output
        Returns:
            space available in bytes in `int` type or None if failed to retrieve available space
    """
    try:
        dir_output = device.parse('df {}'.format(directory), output=output)
    except Exception as e:
        log.error("Failed to parse the directory listing due to: {}".format(str(e)))
        return None

    dir_df_info = dir_output['directory'].values()
    if dir_df_info:
        dir_df_info = list(dir_df_info)[0]
        free_space = dir_df_info.get('available')
        return int(free_space)
    else:
        log.error("Failed to get available space for {}".format(directory))
