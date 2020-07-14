# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Logger
log = logging.getLogger(__name__)

def get_platform_default_dir(device, output=None):
    '''Get the default directory of this device

        Args:
            device (`obj`): Device object
            output (`str`): Output of `file list` command
        Returns:
            default_dir (`str`): Default directory of the system
    '''

    try:
        output = device.parse("file list", output=output)
    except SchemaEmptyParserError as e:
        raise Exception("Command 'file list' did not return any output") from e

    default_dir = output.q.get_values('dir', 0)

    return default_dir