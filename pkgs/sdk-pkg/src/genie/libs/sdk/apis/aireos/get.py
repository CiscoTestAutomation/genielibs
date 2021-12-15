
# Python
import os
import re
import logging

# pyATS
from pyats.easypy import runtime
from pyats.utils.objects import R, find

# Genie
from genie.utils import Dq
from genie.utils.diff import Diff
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import (SchemaEmptyParserError,
                                              SchemaMissingKeyError)
from genie.libs.parser.iosxe.show_logging import ShowLogging

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

def get_boot_variables(device, output=None):
    """Get current or info of boot variables on the device

        Args:
            device ('obj'): Device object
            output ('str'): Out from 'show boot' command

        Returns:
            return a tuple where first tuple is active image and second is backup
            ({'version': <version>, 'status': <status>}, {'version': <version>, 'status': <status>})
    """

    status = ()
    primary = {}
    backup = {}
    try:
        show_boot = device.parse('show boot', output=output)
    except SchemaEmptyParserError as e:
        log.error("Command 'show boot' did not return any output\n".format(str(e)))
    
    else:

        version_pri = show_boot.get('primary_boot_image').get("version_num")
        stat_pri = show_boot.get('primary_boot_image').get("status")
        primary.update({'version': version_pri})
        if stat_pri:
            primary.update({'status': stat_pri})

        version_bk = show_boot.get('backup_boot_image').get("version_num")
        backup.update({'version': version_bk})
        stat_bk = show_boot.get('backup_boot_image').get("status")
        if stat_bk:
            backup.update({'version': stat_bk})
        
        status = (primary,backup)

    return status
