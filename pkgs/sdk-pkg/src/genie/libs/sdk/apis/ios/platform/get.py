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
            output (`str`): Output of `dir` command
        Returns:
            default_dir (`str`): Default directory of the system
    '''

    try:
        output = device.parse("dir", output=output)
    except SchemaEmptyParserError as e:
        raise Exception("Command 'dir' did not return any output") from e

    default_dir = output.setdefault('dir', {}).get('dir', '').replace('/', '')

    return default_dir

def get_platform_core(device, default_dir, output=None, keyword=['.core.gz']):
    '''Get the default directory of this device

        Args:
            device      (`obj`) : Device object
            default_dir (`str`) : default directory on device
            output      (`str`) : Output of `dir` command
            keyword     (`list`): List of keywords to search
        Returns:
            corefiles (`list`): List of found core files
    '''

    cmd = "dir {default_dir}/core/".format(default_dir=default_dir)

    try:
        # sample output:
        # #dir bootflash:core
        # Directory of bootflash:/core/
        #
        # 64899  -rw-           501904  Aug 28 2015 10:16:28 +00:00  RP_0_vman_23519_1440756987.core.gz
        output = device.parse(cmd, output=output)
    except SchemaEmptyParserError:
        # empty is possible. so pass instead of exception
        pass

    corefiles = []
    if output:
        for file in output.q.get_values('files'):
            for kw in keyword:
                if kw in file:
                    corefiles.append('file')

    return corefiles