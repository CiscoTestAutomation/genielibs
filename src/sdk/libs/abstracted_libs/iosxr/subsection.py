# Python
import logging
from os import path

# Abstract
from genie.abstract import Lookup

# Parser
from genie.libs import parser
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def save_device_information(device, **kwargs):
    """Install the commit packages. This is for IOSXR devices.

    Args:
      Mandatory:
        device (`obj`) : Device object.

    Returns:
        True: Result is PASSED
        False: Result is PASSX


    Raises:
        None

    Example:
        >>> save_device_information(device=Device())
    """

    # Checking the config-register has 0x2
    # if not configure 0x2
    # RP/0/RSP1/CPU0:PE1#admin config-register 0x2


    if device.is_ha:
        conn = device.active
    else:
        conn = device

    # go to admin prompt
    conn.state_machine.go_to('admin', conn.spawn)

    # Install commit ( when thre are package to bring up features)
    out = conn.execute('install commit')

    # go back to enable prompt
    conn.state_machine.go_to('enable', conn.spawn)


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
        if ":" in parsed_dict['dir']['dir_name']:
            default_dir = parsed_dict['dir']['dir_name']
        else:
            default_dir = ''
    except SchemaEmptyParserError as e:
        raise Exception("No output when executing 'dir' command") from e
    except Exception as e:
        raise Exception("Unable to execute 'dir' command") from e

    # Return default_dir to caller
    log.info("Default directory on '{d}' is '{dir}'".format(d=device.name,
                                                            dir=default_dir))
    return default_dir