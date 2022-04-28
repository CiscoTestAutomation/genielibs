"""IOSXE CAT9K specific clean stages"""

# Python
import logging
import time

from pyats.async_ import pcall

from genie.abstract import Lookup
from genie.libs import clean
from genie.libs.clean.recovery.recovery import _disconnect_reconnect

# Genie
from genie.libs.clean.stages.iosxe.stages import (
    ChangeBootVariable as IOSXEChangeBootVariable)
from genie.libs.clean.stages.iosxe.stages import (
    TftpBoot as IOSXETftpBoot)

# MetaParser
from genie.metaparser.util.schemaengine import Optional
from genie.libs.clean import BaseStage

from unicon.eal.dialogs import Statement, Dialog


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
        Optional('recovery_en_pasword'): str,
        Optional('save_system_config'): bool,
        Optional('timeout'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'delete_boot_variables',
        'write_memory',
        'enable_boot_manual',
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

    def enable_boot_manual(self, steps, device):
        # To enable the boot manual
        with steps.start("Enabling the boot manual on {}".\
                        format(device.name)) as step:
            try:
                device.api.configure_boot_manual()
            except Exception as e:
                step.failed("Failed to enable the boot manual {}".format(e))


class RommonBoot(BaseStage):
    """This stage boots an image onto the device through rommon. Using either
a local image or one from a tftp server.

Stage Schema
------------
rommon_boot:

    image (list): Image to boot with

    tftp (optional): If specified boot via tftp otherwise boot using local
        image.

        ip_address (list): Management ip address to configure to reach to the
            tftp server

        subnet_mask (str): Management subnet mask

        gateway (str): Management gateway

        tftp_server (str): Tftp server that is reachable with management interface

    save_system_config (bool, optional): Whether or not to save the
        system config if it was modified. Defaults to True.

    timeout (int, optional): Max time allowed for the booting process.
        Defaults to 600.

    config_reg_timeout (int, optional): Max time to set config-register.
        Defaults to 30.

Example
-------
rommon_boot:
    image:
      - /auto/some-location/that-this/image/stay-isr-image.bin
    tftp:
        ip_address: [10.1.7.126, 10.1.7.127]
        gateway: 10.1.7.1
        subnet_mask: 255.255.255.0
        tftp_server: 11.1.7.251
    save_system_config: False
    timeout: 600
    config_reg_timeout: 10

There is more than one ip address, one for each supervisor.
"""

    # =================
    # Argument Defaults
    # =================
    SAVE_SYSTEM_CONFIG = True
    TIMEOUT = 600

    # ============
    # Stage Schema
    # ============
    schema = {
        'image': list,
        Optional('tftp'): {
            'ip_address': list,
            'subnet_mask': str,
            'gateway': str,
            'tftp_server': str,
        },
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
        'rommon_boot',
        'reconnect',
    ]

    def delete_boot_variables(self, steps, device):
        with steps.start("Delete configured boot variables") as step:
            try:
                device.configure('no boot system')
            except Exception as e:
                step.failed("Failed to delete configured boot variables", from_exception=e)

    def write_memory(self, steps, device):
        with steps.start("Write memory") as step:

            try:
                device.api.execute_write_memory()
            except Exception as e:
                step.failed("Failed to write memory", from_exception=e)

    def go_to_rommon(self, steps, device, save_system_config=SAVE_SYSTEM_CONFIG):
        with steps.start("Bring device down to rommon mode"):

            reload_dialog = Dialog([
                Statement(pattern=r".*System configuration has been modified\. Save\? \[yes\/no\].*",
                          action='sendline(yes)' if save_system_config else 'sendline(no)',
                          loop_continue=True,
                          continue_timer=False),
                Statement(pattern=r".*Proceed with reload\? \[confirm\].*",
                          action='sendline()',
                          loop_continue=False,
                          continue_timer=False),
            ])

            # Using sendline, as we dont want unicon boot to kick in and send "boot"
            # to the device. Cannot use device.reload() directly as in case of HA,
            # we need both sup to do the commands
            device.sendline('reload')
            reload_dialog.process(device.spawn)

            if device.is_ha:
                def reload_check(device, target):
                    device.expect(['(.*Initializing Hardware.*|^(.*)((rommon(.*))+>|switch *:).*$)'],
                                  target=target, timeout=90)

                # check if device is a stack device(stack with 2 members is similar to HA devices)
                if len(device.subconnections) > 2:
                    pcall(reload_check,
                          cargs=(device,),
                          iargs=[[alias] for alias in device.connections.defaults.connections])
                else:
                    pcall(reload_check,
                          ckwargs={'device': device},
                          ikwargs=[{'target': 'active'},
                                   {'target': 'standby'}])
            else:
                device.expect(['(.*Initializing Hardware.*|^(.*)((rommon(.*))+>|switch *:).*$)'], timeout=60)

            log.info("Device is reloading")
            device.destroy_all()

    def rommon_boot(self, steps, device, image, tftp=None, timeout=TIMEOUT):

        with steps.start("Boot device from rommon") as step:

            # Need to instantiate to get the device.start
            # The device.start only works because of a|b
            device.instantiate(connection_timeout=timeout)

            try:
                abstract = Lookup.from_device(device, packages={'clean': clean})
            except Exception as e:
                step.failed("Abstraction lookup failed", from_exception=e)

            # device.start only gets filled with single rp devices
            # for multiple rp devices we need to use subconnections
            if device.is_ha and hasattr(device, 'subconnections'):
                start = [i.start[0] for i in device.subconnections]
            else:
                start = device.start

            common_kwargs = {
                'device': device,
                'timeout': timeout
            }

            if tftp:
                tftp.update({'image': image})
                common_kwargs.update({'tftp_boot': tftp})
            else:
                common_kwargs.update({'golden_image': image})

            try:
                pcall(
                    targets=abstract.clean.recovery.recovery.recovery_worker,
                    start=start,
                    ikwargs=[{'item': i} for i, _ in enumerate(start)],
                    ckwargs=common_kwargs
                )
            except Exception as e:
                step.failed("Failed to boot the device from rommon", from_exception=e)

    def reconnect(self, steps, device):
        with steps.start("Reconnect to device") as step:

            if hasattr(device, 'chassis_type') and device.chassis_type.lower() == 'stack':
                log.info("Sleep for 90 seconds in order to sync")
                time.sleep(90)

            if not _disconnect_reconnect(device):
                step.failed("Failed to reconnect")
