
# python
import re
import logging
from genie.utils import Dq
# pyats
from pyats import aetest

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
    log.info('Junos device does not have bootvar.')


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
    try:
        out = device.parse('file list')
        default_dir = Dq(out).get_values('dir', 0)
    except Exception as e:
        log.error(str(e))
        default_dir = ''
    # Return default_dir to caller
    log.info("Default directory on '{d}' is '{dir}'".format(d=device.name,
                                                            dir=default_dir))
    return default_dir


def configure_replace(device, file_location, timeout=60, file_name=None):
    """Configure replace on device

       Args:
           device (`obj`): Device object
           file_location (`str`): File location
           timeout (`int`): Timeout value in seconds
           file_name (`str`): File name

       Returns:
           None

       Raises:
           pyATS Results
    """
    if file_name:
        file_location = '/{}/:{}'.format(
            file_location,
            file_name)
    device.configure('load override {}'.format(file_location), timeout=timeout)
