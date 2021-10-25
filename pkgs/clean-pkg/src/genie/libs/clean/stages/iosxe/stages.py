'''
IOSXE specific clean stages
'''

# Python
import logging

# pyATS
from pyats.async_ import pcall

# Genie
from genie.abstract import Lookup
from genie.libs import clean
from genie.libs.clean.recovery.recovery import _disconnect_reconnect
from genie.metaparser.util.schemaengine import Optional
from genie.utils.timeout import Timeout
from genie.libs.clean import BaseStage
from genie.libs.sdk.libs.abstracted_libs.iosxe.subsection import get_default_dir

# Unicon
from unicon.eal.dialogs import Statement, Dialog

# Logger
log = logging.getLogger(__name__)


class ChangeBootVariable(BaseStage):
    """This stage configures boot variables of the device using the following steps:

    - Delete existing boot variables.
    - Configure boot variables using the provided 'images'.
    - Set the configuration-register using the provided 'config_register'.
    - Write memory.
    - Verify the boot variables are as expected.
    - Verify the configuration-register is as expected.

Stage Schema
------------
change_boot_variable:

    images (list): Image files to use when configuring the boot variables.

    timeout (int, optional): Execute timeout in seconds. Defaults to 300.

    config_register (str, optional): Value to set config-register for
        reload. Defaults to 0x2102.

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
    CONFIG_REGISTER = '0x2102'
    CURRENT_RUNNING_IMAGE = False

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('images'): list,
        Optional('timeout'): int,
        Optional('config_register'): str,
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
        'set_configuration_register',
        'write_memory',
        'verify_boot_variable',
        'verify_configuration_register'
    ]

    def delete_boot_variable(self, steps, device):
        with steps.start("Delete any configured boot variables on {}".format(
                device.name)) as step:

            try:
                device.configure('no boot system')
            except Exception as e:
                step.failed("Failed to delete configured boot variables",
                            from_exception=e)
            else:
                step.passed("Successfully deleted configured boot variables")

    def configure_boot_variable(self, steps, device, images, timeout=TIMEOUT,
                                current_running_image=CURRENT_RUNNING_IMAGE):

        with steps.start("Set boot variable to images provided for {}".format(
                device.name)) as step:

            if current_running_image:
                log.info("Retrieving and using the running image due to "
                         "'current_running_image: True'")

                try:
                    output = device.parse('show version')
                    images = [output['version']['system_image']]
                except Exception as e:
                    step.failed("Failed to retrieve the running image. Cannot "
                                "set boot variables",
                                from_exception=e)

            try:
                device.api.execute_set_boot_variable(
                    boot_images=images, timeout=timeout)
            except Exception as e:
                step.failed("Failed to set boot variables to images provided",
                            from_exception=e)
            else:
                step.passed("Successfully set boot variables to images provided")

    def set_configuration_register(self, steps, device,
                                   config_register=CONFIG_REGISTER, timeout=TIMEOUT):
        with steps.start("Set config register to boot new image on {}".format(
                device.name)) as step:

            try:
                device.api.execute_set_config_register(
                    config_register=config_register, timeout=timeout)
            except Exception as e:
                step.failed("Failed to set config-register",
                            from_exception=e)
            else:
                step.passed("Successfully set config register")

    def write_memory(self, steps, device, timeout=TIMEOUT):
        with steps.start("Execute 'write memory' on {}".format(device.name)) as step:
            try:
                device.api.execute_write_memory(timeout=timeout)
            except Exception as e:
                step.failed("Failed to execute 'write memory'",
                            from_exception=e)
            else:
                step.passed("Successfully executed 'write memory'")

    def verify_boot_variable(self, steps, device, images):
        with steps.start("Verify next reload boot variables are correctly set "
                         "on {}".format(device.name)) as step:

            if not device.api.verify_boot_variable(boot_images=images):
                step.failed("Boot variables are NOT correctly set")
            else:
                step.passed("Boot variables are correctly set")

    def verify_configuration_register(self, steps, device,
                                      config_register=CONFIG_REGISTER):
        with steps.start("Verify config-register is as expected on {}".format(
                device.name)) as step:

            if not device.api.verify_config_register(
                    config_register=config_register, next_reload=True):
                step.failed("Config-register is not as expected")
            else:
                step.passed("Config-register is as expected")


class TftpBoot(BaseStage):
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
        complete. Defaults to 600.

    config_reg_timeout (int, optional): Max time to set config-register.
        Defaults to 30.

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
    recovery_username: user_12345
    save_system_config: False
    timeout: 600
    config_reg_timeout: 10

There is more than one ip address, one for each supervisor.
"""

    # =================
    # Argument Defaults
    # =================
    RECOVERY_PASSWORD = None
    RECOVERY_USERNAME = None
    SAVE_SYSTEM_CONFIG = True
    TIMEOUT = 600
    CONFIG_REG_TIMEOUT = 30
    CONFIG_REG_ROMMON = '0x0'
    CONFIG_REG_NORMAL = '0x2101'

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
        Optional('config_reg_timeout'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'set_config_register',
        'go_to_rommon',
        'tftp_boot',
        'reconnect',
        'reset_config_register',
        'write_memory'
    ]

    def set_config_register(self, steps, device, config_reg_rommon=CONFIG_REG_ROMMON,
                            config_reg_timeout=CONFIG_REG_TIMEOUT):
        with steps.start("Set config-register to 0x0 on {}".format(device.name)) as step:
            try:
                device.api.execute_set_config_register(
                    config_register=config_reg_rommon, timeout=config_reg_timeout)
            except Exception as e:
                step.failed("Unable to set config-register to 0x0 prior to TFTP"
                            " boot on {}".format(device.name), )

    def go_to_rommon(self, steps, device, save_system_config=SAVE_SYSTEM_CONFIG):
        with steps.start("Bring device {} down to rommon> prompt prior to TFTP boot". \
                                 format(device.name)) as step:

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

                pcall(reload_check,
                      ckwargs={'device': device},
                      ikwargs=[{'target': 'active'},
                               {'target': 'standby'}])
            else:
                device.expect(['(.*Initializing Hardware.*|^(.*)((rommon(.*))+>|switch *:).*$)'], timeout=60)

            log.info("Device is reloading")
            device.destroy_all()

    def tftp_boot(self, steps, device, ip_address, subnet_mask, gateway, tftp_server,
                  image, timeout=TIMEOUT, recovery_password=RECOVERY_PASSWORD,
                  recovery_username=RECOVERY_USERNAME):
        with steps.start("Begin TFTP boot of device {}".format(device.name)) as step:

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

                # device.start only gets filled with single rp devices
                # for multiple rp devices we need to use subconnections
                if device.is_ha and hasattr(device, 'subconnections'):
                    start = [i.start[0] for i in device.subconnections]
                else:
                    start = device.start

                result = pcall(abstract.clean.recovery.recovery.recovery_worker,
                               start=start,
                               ikwargs=[{'item': i} for i, _ in enumerate(start)],
                               ckwargs= \
                                   {'device': device,
                                    'timeout': timeout,
                                    'tftp_boot': tftp_boot,
                                    'break_count': 0,
                                    # Irrelevant as we will not use this pattern anyway
                                    # But needed for the recovery
                                    'console_activity_pattern': '\\.\\.\\.\\.',
                                    'golden_image': None,
                                    'recovery_username': recovery_username,
                                    'recovery_password': recovery_password})
            except Exception as e:
                log.error(str(e))
                step.failed("Failed to TFTP boot the device '{}'". \
                            format(device.name), )
            else:
                log.info("Successfully performed TFTP boot on device '{}'". \
                         format(device.name))

    def reconnect(self, steps, device):
        with steps.start("Reconnect to device {} after TFTP boot". \
                                 format(device.name)) as step:
            if not _disconnect_reconnect(device):
                # If that still doesnt work, Thats all we got
                step.failed("Cannot reconnect to the device {d} after TFTP boot".
                            format(d=device.name), )
            else:
                log.info("Success - Have recovered and reconnected to device '{}'". \
                         format(device.name))

    def reset_config_register(self, steps, device,
                              config_reg_timeout=CONFIG_REG_TIMEOUT,
                              config_reg_normal=CONFIG_REG_NORMAL):
        with steps.start("Reset config-register to 0x2101 on {}". \
                                 format(device.name)) as step:
            try:
                device.api.execute_set_config_register(
                    config_register=config_reg_normal, timeout=config_reg_timeout)
            except Exception as e:
                log.error(str(e))
                step.failed("Unable to reset config-register to 0x2101 after TFTP"
                            " boot on {}".format(device.name), )

    def write_memory(self, steps, device):
        with steps.start("Execute 'write memory' on {}".format(device.name)) as step:
            try:
                device.api.execute_write_memory()
            except Exception as e:
                log.error(str(e))
                step.failed("Unable to execute 'write memory' after TFTP boot "
                            "on {}".format(device.name), )
            else:
                step.passed("Successfully performed TFTP boot on device {}". \
                               format(device.name))


class InstallRemoveInactive(BaseStage):
    """This stage removes partially installed packages/images left
on the device. If a super package is left partially installed,
we cannot attempt to install another until it is removed.

Stage Schema
------------
install_image:
    timeout (int, optional): Maximum time to wait for remove process to
        finish. Defaults to 180.

Example
-------
install_remove_inactive:
    timeout: 180

"""

    # =================
    # Argument Defaults
    # =================
    TIMEOUT = 180

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('timeout'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'remove_inactive_pkgs'
    ]

    def remove_inactive_pkgs(self, steps, device, timeout=TIMEOUT):
        with steps.start("Removing inactive packages") as step:
            install_remove_inactive_dialog = Dialog([
                Statement(
                    pattern=r".*Do you want to remove the above files\? \[y\/n\]",
                    action='sendline(y)',
                    loop_continue=False,
                    continue_timer=False),
            ])

            try:
                device.execute('install remove inactive',
                               reply=install_remove_inactive_dialog,
                               timeout=timeout)
            except Exception as e:
                step.failed("Failed to remove inactive packages",
                            from_exception=e)


class InstallImage(BaseStage):
    """This stage installs a provided image onto the device using the install
CLI. It also handles the automatic reloading of your device after the
install is complete.

Stage Schema
------------
install_image:
    images (list): Image to install

    save_system_config (bool, optional): Whether or not to save the system
        config if it was modified. Defaults to False.

    install_timeout (int, optional): Maximum time in seconds to wait for install
        process to finish. Defaults to 500.

    reload_timeout (int, optional): Maximum time in seconds to wait for reload
        process to finish. Defaults to 800.

Example
-------
install_image:
    images:
      - /auto/some-location/that-this/image/stay-isr-image.bin
    save_system_config: True
    install_timeout: 1000
    reload_timeout: 1000

"""
    # =================
    # Argument Defaults
    # =================
    SAVE_SYSTEM_CONFIG = False
    INSTALL_TIMEOUT = 500
    RELOAD_TIMEOUT = 800

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('images'): list,
        Optional('save_system_config'): bool,
        Optional('install_timeout'): int,
        Optional('reload_timeout'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'delete_boot_variable',
        'set_boot_variable',
        'save_running_config',
        'verify_boot_variable',
        'install_image',
        'wait_for_reload'
    ]

    def delete_boot_variable(self, steps, device,):
        with steps.start("Delete all boot variables") as step:
            try:
                device.configure('no boot system')
            except Exception as e:
                step.failed("Failed to delete configured boot variables",
                            from_exception=e)

    def set_boot_variable(self, steps, device):
        with steps.start("Configure system boot variable for 'install mode'") as step:
            # Figure out the directory that the image files get unpacked to
            directory = get_default_dir(device=device)

            # packages.conf is hardcoded because install mode boots using an
            # unpacked packages.conf file
            self.new_boot_var = directory+'packages.conf'

            try:
                device.api.execute_set_boot_variable(
                    boot_images=[self.new_boot_var], timeout=60)
            except Exception as e:
                step.failed("Failed to configure the boot variable",
                            from_exception=e)

    def save_running_config(self, steps, device):
        with steps.start("Save the running config to the startup config") as step:
            try:
                device.api.execute_copy_run_to_start(
                    max_time=60, check_interval=30)
            except Exception as e:
                step.failed("Failed to save the running config",
                            from_exception=e)

    def verify_boot_variable(self, steps, device):
        # Verify next reload boot variables are correctly set
        with steps.start("Verify next reload boot variables are correctly set") as step:
            if not device.api.verify_boot_variable(boot_images=[self.new_boot_var]):
                step.failed(f"Boot variables are not correctly set to "
                            f"{self.new_boot_var}")

    def install_image(self, steps, device, images, save_system_config=SAVE_SYSTEM_CONFIG,
                      install_timeout=INSTALL_TIMEOUT):
        with steps.start(f"Installing image '{images[0]}'") as step:

            install_add_one_shot_dialog = Dialog([
                Statement(pattern=r".*Press Quit\(q\) to exit, you may save "
                                  r"configuration and re-enter the command\. "
                                  r"\[y\/n\/q\]",
                          action='sendline(y)' if save_system_config else 'sendline(n)',
                          loop_continue=True,
                          continue_timer=False),
                Statement(pattern=r".*Please confirm you have changed boot config "
                                  r"to \S+ \[y\/n\]",
                          action='sendline(y)',
                          loop_continue=True,
                          continue_timer=False),
                Statement(pattern=r".*reload of the system\. "
                                  r"Do you want to proceed\? \[y\/n\]",
                          action='sendline(y)',
                          loop_continue=True,
                          continue_timer=False),
            ])

            try:
                device.execute('install add file {} activate commit'.format(images[0]),
                               reply=install_add_one_shot_dialog,
                               append_error_pattern=['FAILED:'],
                               timeout=install_timeout)
            except Exception as e:
                step.failed("Failed to install the iamge", from_exception=e)

            image_mapping = self.history['InstallImage'].parameters.setdefault(
                'image_mapping', {})
            image_mapping.update({images[0]: self.new_boot_var})

    def wait_for_reload(self, steps, device, reload_timeout=RELOAD_TIMEOUT):
        with steps.start(f"Waiting for {device.hostname} to reload") as step:

            timeout = Timeout(reload_timeout, 60)
            while timeout.iterate():
                timeout.sleep()
                device.destroy()

                try:
                    device.connect(learn_hostname=True)
                except Exception as e:
                    connect_exception = e
                    log.info("The device is not ready")
                else:
                    step.passed("The device has successfully reloaded")

            step.failed("Failed to reload", from_exception=connect_exception)


class InstallPackages(BaseStage):
    """This stage installs the provided packages using the install CLI.

Stage Schema
------------
install_packages:
    packages (list): Packages to install.

    save_system_config (bool, optional): Whether or not to save the system
        config if it was modified. Defaults to False.

    install_timeout (int, optional): Maximum time to wait for install
        process to finish. Defaults to 300.

Example
-------
install_packages:
    packages:
      - /auto/some-location/that-this/image/stay-isr-image.bin
    save_system_config: True
    install_timeout: 1000

"""
    # =================
    # Argument Defaults
    # =================
    SAVE_SYSTEM_CONFIG = False
    INSTALL_TIMEOUT = 300

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('packages'): list,
        Optional('save_system_config'): bool,
        Optional('install_timeout'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'install_package'
    ]

    def install_package(self, steps, device, packages,
                        save_system_config=SAVE_SYSTEM_CONFIG,
                        install_timeout=INSTALL_TIMEOUT):

        install_add_one_shot_dialog = Dialog([
            Statement(pattern=r".*Press Quit\(q\) to exit, you may save "
                              r"configuration and re-enter the command\. "
                              r"\[y\/n\/q\]",
                      action='sendline(y)' if save_system_config else 'sendline(n)',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r".*Please confirm you have changed boot config "
                              r"to \S+ \[y\/n\]",
                      action='sendline(y)',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r".*This operation may require a reload of the "
                              r"system\. Do you want to proceed\? \[y\/n\]",
                      action='sendline(y)',
                      loop_continue=True,
                      continue_timer=False),
        ])

        for pkg in packages:
            with steps.start("Installing package '{pkg}' onto {dev}".format(
                    pkg=pkg, dev=device.hostname)) as step:

                try:
                    device.execute(
                        'install add file {} activate commit'.format(pkg),
                        reply=install_add_one_shot_dialog,
                        error_pattern=['FAILED:'],
                        timeout=install_timeout
                    )
                except Exception as e:
                    step.failed("Failed to install the package",
                                from_exception=e)