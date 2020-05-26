# Python
import logging

# Abstract
from genie.abstract import Lookup

# Parser
from genie.libs import parser
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def save_device_information(device, **kwargs):
    '''Save running configuration to startup configuration'''

    # Check if device is VDC
    try:
        output = device.parse('show vdc current-vdc')
    except Exception as e:
        raise Exception("Unable to execute 'show vdc current-vdc' to check "
                        "if device is VDC") from e

    # Check if device is VDC
    if 'current_vdc' in output and output['current_vdc']['id'] != '1':
        cmd = 'copy running-config startup-config'
    else:
        cmd = 'copy running-config startup-config vdc-all'

    # Copy boot variables
    try:
        device.execute(cmd)
    except Exception as e:
        raise Exception(
            "Unable to save running-config to startup-config") from e


def get_default_dir(device):
    """ Get the default directory of this device

        Args:
          Mandatory:
            device (`obj`) : Device object.

        Returns:
            default_dir (`str`): Default directory of the system

        Raises:
            Exception

        Example:
            >>> get_default_dir(device=device)
    """

    try:
        lookup = Lookup.from_device(device)
        parsed_dict = lookup.parser.show_platform.Dir(device=device).parse()
        default_dir = parsed_dict['dir']
    except SchemaEmptyParserError as e:
        raise Exception("No output when executing 'dir' command") from e
    except Exception as e:
        raise Exception("Unable to execute 'dir' command") from e

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
        file_location = '{}{}'.format(
            file_location,
            file_name)
    device.execute(
        'configure replace {}'.format(file_location),
        timeout=timeout)
