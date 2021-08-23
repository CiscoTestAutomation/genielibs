'''
NXOS specific clean stages
'''

# Python
import time
import logging

# pyATS
from pyats.async_ import pcall

# Genie
from genie.libs import clean
from genie.abstract import Lookup
from genie.libs.clean.recovery.recovery import _disconnect_reconnect
from genie.libs.clean import BaseStage

# MetaParser
from genie.metaparser.util.schemaengine import Optional

# Logger
log = logging.getLogger(__name__)


class ChangeBootVariable(BaseStage):
    """This stage configures boot variables of the device using the following steps:

    - Delete existing boot variables.
    - Configure boot variables using the provided 'images'.
    - Write memory.
    - Verify the boot variables are as expected.

Stage Schema
------------
change_boot_variable:

    images:

        kickstart (list, optional): The kickstart image file

        system (list): The system image file

    copy_vdc_all (bool, optional): If True copy onto all VDCs. Defaults to False.

    timeout (int, optional): Execute timeout in seconds. Defaults to 300.

    max_time (int, optional): Maximum time in seconds allowed for verifications.
        Defaults to 300.

    check_interval (int, optional): How often to check verifications in seconds.
        Defaults to 60.

    standby_copy_max_time (int, optional): Maximum time in seconds allowed for
        copying to standby RP. Defaults to 300.

    standby_copy_check_interval (int, optional): How often to check if the copy
        to the standby RP is complete. Defaults to 20.

    current_running_image (bool, optional): Set the boot variable to the currently
        running image from the show version command instead of the image provided.
        Defaults to False.

Example
-------
change_boot_variable:
    images:
        kickstart: bootflash:/kisckstart.gbin
        system: bootflash:/system.gbin
    copy_vdc_all: True
    timeout: 150
    max_time: 300
    check_interval: 20
    standby_copy_max_time: 100
    standby_copy_check_interval: 10
"""

    # =================
    # Argument Defaults
    # =================
    COPY_VDC_ALL = False
    TIMEOUT = 300
    MAX_TIME = 300
    CHECK_INTERVAL = 60
    STANDBY_COPY_MAX_TIME = 300
    STANDBY_COPY_CHECK_INTERVAL = 20
    CURRENT_RUNNING_IMAGE = False

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('images'): {
            'system': list,
            Optional('kickstart'): list
        },
        Optional('copy_vdc_all'): bool,
        Optional('timeout'): int,
        Optional('max_time'): int,
        Optional('check_interval'): int,
        Optional('standby_copy_max_time'): int,
        Optional('standby_copy_check_interval'): int,
        Optional('current_running_image'): bool,

        # Deprecated
        Optional('stabilize_time'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'delete_boot_variable',
        'configure_boot_variable',
        'save_running_config',
        'verify_boot_variable',
        'verify_ha_file_transfer'
    ]

    def delete_boot_variable(self, steps, device, timeout=TIMEOUT):
        with steps.start("Delete any previously configured boot variables on "
                         "{}".format(device.name)) as step:

            try:
                device.api.execute_delete_boot_variable(device=device, timeout=timeout)
            except Exception as e:
                step.failed('Failed to delete the boot variables',
                            from_exception=e)

    def configure_boot_variable(self, steps, device, images, timeout=TIMEOUT,
                                current_running_image=CURRENT_RUNNING_IMAGE):

        with steps.start("Set boot variable to images provided for {}".format(
                device.name)) as step:

            if current_running_image:
                log.info("Retrieving and using the running image due to "
                         "'current_running_image: True'")

                try:
                    output = device.parse('show version')
                    kickstart = output['platform']['software'].get('kickstart_image_file', None)
                    system = output['platform']['software'].get('system_image_file')
                    system = system.replace(':///', ':/')
                except Exception as e:
                    step.failed("Failed to retrieve the running image. Cannot "
                                "set boot variables",
                                from_exception=e)

            else:
                kickstart = images.get('kickstart')
                kickstart = kickstart[0] if kickstart else None

                system = images.get('system')
                system = system[0] if system else None

            try:
                device.api.execute_change_boot_variable(
                    kickstart=kickstart, system=system, timeout=timeout)
            except Exception as e:
                step.failed("Failed to set the boot variables",
                            from_exception=e)

    def save_running_config(self, steps, device, copy_vdc_all=COPY_VDC_ALL,
                            timeout=TIMEOUT, max_time=MAX_TIME,
                            check_interval=CHECK_INTERVAL):

        with steps.start("Save running configuration to startup configuration") as step:
            try:
                device.api.execute_copy_run_to_start(
                    copy_vdc_all=copy_vdc_all,
                    command_timeout=timeout,
                    max_time=max_time,
                    check_interval=check_interval)
            except Exception as e:
                step.failed('Failed to save the running configuration',
                            from_exception=e)

    def verify_boot_variable(self, steps, device, images):

        kickstart = images.get('kickstart')
        kickstart = kickstart[0] if kickstart else None

        system = images.get('system')
        system = system[0] if system else None

        with steps.start("Verify next boot variables") as step:
            try:
                device.api.is_next_reload_boot_variable_as_expected(
                    kickstart=kickstart,
                    system=system)
            except Exception as e:
                step.failed("Failed to verify the boot variables",
                            from_exception=e)

    def verify_ha_file_transfer(self, steps, device,
                                standby_copy_max_time=STANDBY_COPY_MAX_TIME,
                                standby_copy_check_interval=STANDBY_COPY_CHECK_INTERVAL):

        if device.is_ha:
            with steps.start("Verify the files transferred successfully to "
                             "the standby") as step:

                try:
                    device.api.verify_files_copied_on_standby(
                        max_time=standby_copy_max_time,
                        check_interval=standby_copy_check_interval)
                except Exception as e:
                    step.failed("Failed to verify the files copied to standby",
                                from_exception=e)


class TftpBoot(BaseStage):
    """This stage boots a new image onto your device using the tftp booting method.

Stage Schema
------------
tftp_boot:

    image (str): Image to boot the device with

    ip_address (str): The management IP address that will be configured in order
        to reach the TFTP server.

    subnet_mask (str): The management subnet mask that will be configured in
        order to reach the TFTP server.

    gateway (str): The management gateway that will be configured in order
        to reach the TFTP server.

    tftp_server (str): The TFTP server that is reachable through the management
        interface.

    timeout (int): The maximum time allowed in seconds to complete the tftp
        booting process.

    reboot_delay (int, optional): Time in seconds to sleep after sending the
        reboot command. Defaults to 20.

    reconnect_delay (int, optional): Time is seconds to sleep before reconnecting
        after the device has come up. Defaults to 60.

Example:
--------
tftp_boot:
    image:
      - /auto/some-location/that-this/image/stay-isr-image.bin
    ip_address: [10.1.7.126, 10.1.7.127]
    gateway: 10.1.7.1
    subnet_mask: 255.255.255.0
    tftp_server: 11.1.7.251

There is more than one ip address, one for each supervisor.
"""

    # =================
    # Argument Defaults
    # =================
    REBOOT_DELAY = 20
    RECONNECT_DELAY = 60

    # ============
    # Stage Schema
    # ============
    schema = {
        'image': list,
        'ip_address': list,
        'subnet_mask': str,
        'gateway': str,
        'tftp_server': str,
        'timeout': int,
        Optional('reboot_delay'): int,
        Optional('reconnect_delay'): int
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'tftp_boot'
    ]

    def tftp_boot(self, device, ip_address, subnet_mask, gateway, tftp_server,
                  image, timeout, reconnect_delay=RECONNECT_DELAY,
                  reboot_delay=REBOOT_DELAY):
        device.api.execute_write_erase_boot()
        # Using sendline, as we dont want unicon boot to kick in and send "boot" to
        # the device
        # Cannot use .reload as in case of HA, we need both sup to do the commands
        device.sendline('reload')
        device.sendline('y')
        device.sendline()
        log.info('** Rebooting the device **')

        # We now want to overwrite the statemachine
        device.destroy_all()
        # Sleep to make sure the device is reloading
        time.sleep(reboot_delay)

        # Need to instantiate to get the device.start
        # The device.start only works because of a|b
        device.instantiate(connection_timeout=timeout)

        tftp_boot = {'ip_address': ip_address,
                     'subnet_mask': subnet_mask,
                     'gateway': gateway,
                     'tftp_server': tftp_server,
                     'image': image}
        try:
            abstract = Lookup.from_device(device, packages={'clean': clean})
            # Item is needed to be able to know in which parallel child
            # we are

            # device.start only gets filled with single rp devices
            # for multiple rp devices we need to use subconnections
            if device.is_ha and hasattr(device, 'subconnections'):
                start = [i.start[0] for i in device.subconnections]
            else:
                start = device.start

            result = pcall(abstract.clean.recovery.recovery.recovery_worker,
                           start=start,
                           ikwargs = [{'item': i} for i, _ in enumerate(start)],
                           ckwargs = \
                                {'device': device,
                                 'timeout': timeout,
                                 'tftp_boot': tftp_boot,
                                 # Irrelevant as we will not use this pattern anyway
                                 # But needed for the recovery
                                 'break_count': 0,
                                 'console_activity_pattern': '\\.\\.\\.\\.',
                                 'golden_image': None,
                                 'recovery_password': None})
        except Exception as e:
            log.error(str(e))
            self.failed("Failed to recover the device '{}'".\
                            format(device.name))
        else:
            log.info("Successfully recovered the device '{}'".\
                     format(device.name))

        log.info('Sleeping for {r} before reconnection'.format(r=reconnect_delay))
        time.sleep(reconnect_delay)

        # Disconnect and reconnect to the device
        if not _disconnect_reconnect(device):
            # If that still doesnt work, Thats all we got
            self.failed("Cannot reconnect to the device {d}".
                            format(d=device.name))
        else:
            log.info("Success - Have recovered and reconnected to device '{}'".\
                     format(device.name))

        log.info('Set the boot variables')
        output = device.api.get_running_image()
        if not output:
            self.failed('Could not retrieved the running image')
        image = output[0].rsplit('/', 1)[1]
        device.api.execute_change_boot_variable(system='bootflash:/{image}'
                                                      .format(image=image))
        device.api.execute_copy_run_to_start()