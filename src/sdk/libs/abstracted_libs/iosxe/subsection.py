# Python
import logging
from os import path

# unicon
from unicon.eal.dialogs import Statement, Dialog

# Abstract
from genie.abstract import Lookup

# Parser
from genie.libs import parser
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def save_device_information(device):
    """Save running-configuration to startup-config.
    This is for general IOSXE devices.

    Args:
      Mandatory:
        device (`obj`) : Device object.

    Raises:
        None

    Example:
        >>> save_device_information(device=Device())
    """
    # configure config-register
    device.configure('config-register 0x2102')

    # save all configuration to startup for all slots        
    dialog = Dialog([
        Statement(pattern=r'Destination +filename +\[.*\].*',
                            action='sendline()',
                            loop_continue=True,
                            continue_timer=False)
    ])
    device.execute('copy running-config nvram:startup-config',
                        reply=dialog)
    device.execute('write memory')

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
        default_dir = parsed_dict['dir']['dir'].replace('/', '')
    except SchemaEmptyParserError as e:
        raise Exception("No output when executing 'dir' command") from e
    except Exception as e:
        raise Exception("Unable to execute or parse 'dir' command") from e

    # Return default_dir to caller
    log.info("Default directory on '{d}' is '{dir}'".format(d=device.name,
                                                            dir=default_dir))
    return default_dir