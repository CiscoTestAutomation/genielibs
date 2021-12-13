"""IOSXE CAT9500 specific clean stages"""

# Python
import logging

# Genie
from genie.libs.clean.stages.iosxe.stages import (
    ChangeBootVariable as IOSXEChangeBootVariable)

# MetaParser
from genie.metaparser.util.schemaengine import Optional

# Logger
log = logging.getLogger(__name__)


class ChangeBootVariable(IOSXEChangeBootVariable):
    """This stage configures boot variables of the device using the following steps:

    - Delete existing boot variables.
    - Configure boot variables using the provided 'images'.
    - Write memory.
    - Verify the boot variables are as expected.

Stage Schema
------------
change_boot_variable:

    images (list): Image files to use when configuring the boot variables.

    timeout (int, optional): Execute timeout in seconds. Defaults to 300.

    current_running_image (bool, optional): Set the boot variable to the currently
        running image from the show version command instead of the image provided.
        Defaults to False.

Example
-------
change_boot_variable:
    images:
        - harddisk:/image.bin
    timeout: 150
"""

    # =================
    # Argument Defaults
    # =================
    TIMEOUT = 300
    CURRENT_RUNNING_IMAGE = False

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('images'): list,
        Optional('timeout'): int,
        Optional('current_running_image'): bool,

        # Deprecated
        Optional('check_interval'): int,
        Optional('max_time'): int,
        Optional('write_memory'): bool,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'delete_boot_variable',
        'configure_boot_variable',
        'write_memory',
        'verify_boot_variable'
    ]

