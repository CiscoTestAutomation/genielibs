
import logging

log = logging.getLogger(__name__)


def get_available_space(device, directory, output=None):
    """Get the available space for an APIC directory.

    Args:
        device ('obj'): Device object.
        directory ('str'): Directory to check, such as /data/log.
        output ('str'): Optional captured output of the 'df' command.

    Returns:
        int or None: Available space, or None when it cannot be verified.
    """
    try:
        parsed_output = device.parse(f'df {directory}', output=output)
    except Exception as error:
        log.error('Failed to parse the directory listing: %s', error)
        return None

    if not isinstance(parsed_output, dict):
        log.error('Failed to get available space for %s', directory)
        return None

    directory_data = parsed_output.get('directory', {})
    if not isinstance(directory_data, dict):
        log.error('Failed to get available space for %s', directory)
        return None

    filesystem_info = next(iter(directory_data.values()), None)
    available_space = filesystem_info.get('available') if isinstance(filesystem_info, dict) else None
    if available_space is not None:
        try:
            return int(available_space)
        except (TypeError, ValueError):
            pass

    log.error('Failed to get available space for %s', directory)
    return None
