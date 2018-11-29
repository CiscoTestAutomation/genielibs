
# python
import re
import logging

# pyats
from ats import aetest

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

    out = re.search('(\/\S+)', device.execute('file list'))
    if out:
        default_dir = out.groups()[0]
    else:
        default_dir = ''
    

    # Return default_dir to caller
    log.info("Default directory on '{d}' is '{dir}'".format(d=device.name,
                                                            dir=default_dir))
    return default_dir
