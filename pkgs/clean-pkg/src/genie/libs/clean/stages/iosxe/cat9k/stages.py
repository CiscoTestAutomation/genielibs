"""IOSXE CAT9K specific clean stages"""

# Python
import logging

# Genie
from genie.libs.clean.stages.iosxe.stages import (
    ChangeBootVariable as IOSXEChangeBootVariable)
from genie.libs.clean.stages.iosxe.stages import (
    TftpBoot as IOSXETftpBoot)


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
class TftpBoot(IOSXETftpBoot):
    """This stage boots a new image onto your device using the tftp booting
method.

Stage Schema
------------
tftp_boot:

    image (list): Image to boot with

    ip_address (list): Management ip address to configure to reach to the
        tftp server

    subnet_mask (str): Management subnet mask

    gateway (str): Management gateway

    tftp_server (str): Tftp server that is reachable with management interface

    recovery_password (str): Enable password for device
        required after bootup. Defaults to None.

    recovery_username (str): Enable username for device
        required after bootup. Defaults to None.

    save_system_config (bool, optional): Whether or not to save the
        system config if it was modified. Defaults to True.

    timeout (int, optional): Max time during which tftp boot must
        complete. Defaults to 1000 seconds.

Example
-------
tftp_boot:
    image:
      - /auto/some-location/that-this/image/stay-isr-image.bin
    ip_address: [10.1.7.126, 10.1.7.127]
    gateway: 10.1.7.1
    subnet_mask: 255.255.255.0
    tftp_server: 11.1.7.251
    recovery_password: nbv_12345
    recovery_username: user_123
    save_system_config: False
    timeout: 1000

There is more than one ip address, one for each supervisor.
"""

    # =================
    # Argument Defaults
    # =================
    # =================
    RECOVERY_PASSWORD = None
    RECOVERY_USERNAME = None
    SAVE_SYSTEM_CONFIG = True
    TIMEOUT = 1000


    # ============
    # Stage Schema
    # ============
    schema = {
        'image': list,
        'ip_address': list,
        'subnet_mask': str,
        'gateway': str,
        'tftp_server': str,
        'recovery_password': str,
        'recovery_username': str,
        Optional('save_system_config'): bool,
        Optional('timeout'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'delete_boot_variables',
        'write_memory',
        'go_to_rommon',
        'tftp_boot',
        'reconnect',
    ]

    def delete_boot_variables(self, steps, device, timeout=30):

        # Delete any previously configured boot variables
        with steps.start("Delete any previously configured boot variables on {}".\
                        format(device.name)) as step:
            try:
                device.configure('no boot system', timeout=timeout)
            except Exception as e:
                step.failed("Failed to delete the boot variables because of {}".format(e))            


