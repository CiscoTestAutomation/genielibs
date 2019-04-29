
# python
import logging
log = logging.getLogger(__name__)


def save_device_information(device, **kwargs):
    """Show version to print information users interest

    Args:
      Mandatory:
        device (`obj`) : Device object.

    Returns:
        True: Result is PASSED


    Raises:
        None

    Example:
        >>> save_device_information(device=Device())
    """

    # bypass the section
    log.info('SONiC device does not have bootvar.')


def get_default_dir(device):
    """ Get the default directory of this device

        Args:
          Mandatory:
            device (`obj`) : Device object.

        Returns:
            default_dir (`str`): Default directory of the system

        Raises:
            None

        Example:
            >>> get_default_dir(device=device)
    """
    # bypass the section
    log.info('SONiC device does not have default directory.')
