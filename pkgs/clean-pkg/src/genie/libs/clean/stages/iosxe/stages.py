'''
IOSXE specific clean stages
'''

# Python
import logging
import time
# pyATS
from pyats.async_ import pcall

# Genie
from genie.abstract import Lookup
from genie.libs import clean
from genie.libs.clean.recovery.recovery import _disconnect_reconnect
from genie.metaparser.util.schemaengine import Optional, Any
from genie.utils.timeout import Timeout
from genie.libs.clean import BaseStage
from genie.libs.sdk.libs.abstracted_libs.iosxe.subsection import get_default_dir
from genie.libs.clean.utils import raise_

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure

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

    recovery_en_password (str): Enable password for device
        required after bootup. Defaults to None.

    recovery_username (str): Enable username for device
        required after bootup. Defaults to None.

    save_system_config (bool, optional): Whether or not to save the
        system config if it was modified. Defaults to True.

    timeout (int, optional): Max time during which tftp boot must
        complete. Defaults to 600.

    config_reg_timeout (int, optional): Max time to set config-register.
        Defaults to 30.

    image_length_limit(int, optinal): Maximum length of characters for image.
        Defaults to 110.

    ether_port(int, optional): port to set for tftp boot. Defaults to None.

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
    recovery_en_password: en
    save_system_config: False
    timeout: 600
    config_reg_timeout: 10
    image_length_limit: 90
    ether_port: 0

There is more than one ip address, one for each supervisor.
"""

    # =================
    # Argument Defaults
    # =================
    RECOVERY_PASSWORD = None
    RECOVERY_EN_PASSWORD=None
    RECOVERY_USERNAME = None
    SAVE_SYSTEM_CONFIG = False
    TIMEOUT = 1200
    CONFIG_REG_TIMEOUT = 30
    CONFIG_REG_ROMMON = '0x0'
    CONFIG_REG_NORMAL = '0x2101'
    IMAGE_LENGTH_LIMIT = 110
    ETHER_PORT = None
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
        Optional('recovery_en_password'): str,
        Optional('save_system_config'): bool,
        Optional('timeout'): int,
        Optional('config_reg_timeout'): int,
        Optional('image_length_limit'): int,
        Optional('ether_port') : int
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'check_image_length',
        'set_config_register',
        'go_to_rommon',
        'tftp_boot',
        'reconnect',
        'reset_config_register',
        'write_memory'
    ]

    def check_image_length(self ,steps, image, image_length_limit=IMAGE_LENGTH_LIMIT): 
        log.warning('The next release will REMOVE the following keys from the tftp_boot schema:\n'
                    'recovery_password, recovery_username, recovery_en_password, ether_port, save_system_config\n'
                    'Please update the clean YAML file accordingly.'
                )
        with steps.start("Check the length of image: {}".format(image[0])) as step:
            if len(image[0]) > image_length_limit:
                step.failed(f"The length of image path {image[0]} is more than the limit of"
                            f" {image_length_limit} characters.")
            else:
                step.passed(f"The length of image {image[0]} is within the {image_length_limit} character limit.")

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

                # check if device is a stack device(stack with 2 memebrs is similar to HA devices)
                if len(device.subconnections) > 2:
                    pcall(reload_check,
                          cargs= (device,),
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

    def tftp_boot(self, steps, device, ip_address, subnet_mask, gateway, tftp_server,
                  image, timeout=TIMEOUT, recovery_password=RECOVERY_PASSWORD,
                  recovery_username=RECOVERY_USERNAME,recovery_en_password=RECOVERY_EN_PASSWORD, ether_port=ETHER_PORT ):
        with steps.start("Begin TFTP boot of device {}".format(device.name)) as step:

            # Need to instantiate to get the device.start
            # The device.start only works because of a|b
            device.instantiate(connection_timeout=timeout)

            tftp_boot = {'ip_address': ip_address,
                         'subnet_mask': subnet_mask,
                         'gateway': gateway,
                         'tftp_server': tftp_server,
                         'image': image,
                         'ether_port':ether_port}
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
                                    'recovery_en_password':recovery_en_password,
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
            if hasattr(device, 'chassis_type') and device.chassis_type.lower() == 'stack':
                log.info("Sleep for 90 seconds in order to sync ")
                time.sleep(90)
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

    reload_service_args (optional):

        reload_creds (str, optional): The credential to use after the reload is
            complete. The credential name comes from the testbed yaml file.
            Defaults to the 'default' credential.

        prompt_recovery (bool, optional): Enable or disable the prompt recovery
            feature of unicon. Defaults to True.

        append_error_pattern (list, optional): List of regex strings to check for,
            to be appended to the default error pattern list. Default: [r"FAILED:.* ",]

        <Key>: <Value>
            Any other arguments that the Unicon reload service supports

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
    RELOAD_SERVICE_ARGS = {
        'reload_creds': 'default',
        'prompt_recovery': True,
        'append_error_pattern': [r"FAILED:.* ",],
    }
    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('images'): list,
        Optional('save_system_config'): bool,
        Optional('install_timeout'): int,
        Optional('reload_timeout'): int,
        Optional('reload_service_args'): {
            Optional('reload_creds'): str,
            Optional('prompt_recovery'): bool,
            Optional('append_error_pattern'): list,
            Any(): Any()
        }
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'delete_boot_variable',
        'set_boot_variable',
        'save_running_config',
        'verify_boot_variable',
        'install_image'
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
            output = device.parse('dir')
            directory = output['dir']['dir']
            files = output.get('dir', {}).get(directory, {}).get('files', {})

            if not files.get('packages.conf'):
                # create packages.conf, if it does not exist
                device.tclsh('puts [open "%spackages.conf" w+] {}' % directory)

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

    def install_image(self, steps, device, images,
                      save_system_config=SAVE_SYSTEM_CONFIG,
                      install_timeout=INSTALL_TIMEOUT,
                      reload_service_args=None):

        # Set default reload args
        reload_args = self.RELOAD_SERVICE_ARGS.copy()
        # If user provides custom values, update the default with the user
        # provided.
        if reload_service_args:
            reload_args.update(reload_service_args)

        with steps.start(f"Installing image '{images[0]}'") as step:
            current_image = device.api.get_running_image()
            if current_image == images[0]:
                step.skipped('Images is already installed on the device.')

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
                Statement(pattern=r".*Same Image File-No Change",
                          loop_continue=False,
                          continue_timer=False),
                Statement(pattern=r".*reload of the system\. "
                                  r"Do you want to proceed\? \[y\/n\]",
                          action='sendline(y)',
                          loop_continue=True,
                          continue_timer=False),
                Statement(pattern=r"FAILED:.* ",
                          action=None,
                          loop_continue=False,
                          continue_timer=False),
            ])

            try:
                reload_args.update({
                    'timeout': install_timeout,
                    'reply': install_add_one_shot_dialog
                })

                device.reload('install add file {} activate commit'.format(images[0]),
                              **reload_args)

            except Exception as e:
                step.failed("Failed to install the image", from_exception=e)

            image_mapping = self.history['InstallImage'].parameters.setdefault(
                'image_mapping', {})
            image_mapping.update({images[0]: self.new_boot_var})


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


class Reload(BaseStage):
    """ This stage reloads the device.

Stage Schema
------------
reload:

    reload_service_args (optional):

        timeout (int, optional): Maximum time in seconds allowed for the reload.
            Defaults to 800.

        reload_creds (str, optional): The credential to use after the reload is
            complete. The credential name comes from the testbed yaml file.
            Defaults to the 'default' credential.

        prompt_recovery (bool, optional): Enable or disable the prompt recovery
            feature of unicon. Defaults to True.

        <Key>: <Value>
            Any other arguments that the Unicon reload service supports

    check_modules:

        check (bool, optional): Enable the checking of modules after reload.
            Defaults to True.

        timeout (int, optional): Maximum time in seconds allowed for verifying
            the modules are in a stable state. Defaults to 180.

        interval (int, optional): How often to check the module states in
            seconds. Defaults to 30.

    reconnect_via (str, optional): Specify which connection to use after reloading.
        Defaults to the 'default' connection in the testbed yaml file.


Example
-------
reload:
    reload_service_args:
        timeout: 600
        reload_creds: clean_reload_creds
        prompt_recovery: True
        reconnect_sleep: 200 (Unicon NXOS reload service argument)
    check_modules:
        check: False
"""
    # =================
    # Argument Defaults
    # =================
    RELOAD_SERVICE_ARGS = {
        'timeout': 800,
        'reload_creds': 'default',
        'prompt_recovery': True
    }
    CHECK_MODULES = {
        'check': True,
        'timeout': 180,
        'interval': 30,
        'ignore_modules': None
    }
    RECONNECT_VIA = None

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('check_modules'): {
            Optional('check'): bool,
            Optional('timeout'): int,
            Optional('interval'): int,
            Optional('ignore_modules'): list
        },
        Optional('reload_service_args'): {
            Optional('timeout'): int,
            Optional('reload_creds'): str,
            Optional('prompt_recovery'): bool,
            Any(): Any()
        },
        Optional('reconnect_via'): str,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'reload',
        'disconnect_and_reconnect',
        'check_modules'
    ]

    def reload(self, steps, device, reload_service_args=None):

        if reload_service_args is None:
            # If user provides no custom values, take the defaults
            reload_service_args = self.RELOAD_SERVICE_ARGS
        else:
            # If user provides custom values, update the default with the user
            # provided. This is needed because if the user only provides 1 of
            # the many optional arguments, we still need to default the others.
            self.RELOAD_SERVICE_ARGS.update(reload_service_args)
            reload_service_args = self.RELOAD_SERVICE_ARGS

        with steps.start(f"Reload {device.name}") as step:

            try:
                device.reload(**reload_service_args)
            except Exception as e:
                step.failed(f"Failed to reload within {reload_service_args['timeout']} "
                            f"seconds.", from_exception=e)

    def disconnect_and_reconnect(self, steps, device, reload_service_args=None,
                                 reconnect_via=RECONNECT_VIA):

        if reload_service_args is None:
            # If user provides no custom values, take the defaults
            reload_service_args = self.RELOAD_SERVICE_ARGS
        else:
            # If user provides custom values, update the default with the user
            # provided. This is needed because if the user only provides 1 of
            # the many optional arguments, we still need to default the others.
            self.RELOAD_SERVICE_ARGS.update(reload_service_args)
            reload_service_args = self.RELOAD_SERVICE_ARGS

        with steps.start(f"Disconnect and Reconnect to {device.name}") as step:

            try:
                device.destroy()
            except Exception:
                log.warning("Failed to destroy the device connection but "
                            "attempting to continue", exc_info=True)
            connect_kwargs = {
                        'learn_hostname': True,
                        'prompt_recovery': reload_service_args['prompt_recovery']
                    }

            if reconnect_via:
                connect_kwargs.update({'via': reconnect_via})

            device.instantiate(**connect_kwargs)
            rommon_to_disable = None
            try:
                if device.is_ha and hasattr(device, 'subconnections'):
                    if isinstance(device.subconnections, list):
                        rommon_to_disable = device.subconnections[0].state_machine.get_path('rommon', 'disable')
                else:
                    rommon_to_disable = device.state_machine.get_path('rommon', 'disable')
            except ValueError:
                log.warning('There is no path between rommon and disable states.')
            except IndexError:
                log.warning('There is no connection in device.subconnections')
            if rommon_to_disable and hasattr(rommon_to_disable, 'command'):
                original_command = rommon_to_disable.command
                if device.is_ha:
                    index = device.subconnections[0].state_machine.paths.index(rommon_to_disable)
                    for subcon in device.subconnections:
                        subcon.state_machine.paths[index].command = lambda state,spawn,context: raise_(Exception(f'Device {device.name} is still '
                                                                    f'in rommon state after reload.'))
                else:
                    index = device.state_machine.paths.index(rommon_to_disable)
                    device.state_machine.paths[index].command = lambda state,spawn,context: raise_(Exception(f'Device {device.name} is still '
                                                                    f'in rommon state after reload.'))

            try:
                device.connect()
            except Exception as e:
                step.failed("Failed to reconnect", from_exception=e)
            if rommon_to_disable and hasattr(rommon_to_disable, 'command'):
                if device.is_ha:
                    index = device.subconnections[0].state_machine.paths.index(rommon_to_disable)
                    for subcon in device.subconnections:
                        subcon.state_machine.paths[index].command = original_command
                else:
                    index = device.state_machine.paths.index(rommon_to_disable)
                    device.state_machine.paths[index].command = original_command

    def check_modules(self, steps, device, check_modules=None):

        if check_modules is None:
            # If user provides no custom values, take the defaults
            check_modules = self.CHECK_MODULES
        else:
            # If user provides custom values, update the default with the user
            # provided. This is needed because if the user only provides 1 of
            # the many optional arguments, we still need to default the others.
            self.CHECK_MODULES.update(check_modules)
            check_modules = self.CHECK_MODULES

        if check_modules['check']:

            with steps.start(f"Checking the modules on '{device.name}' are in a "
                             f"stable state") as step:

                try:
                    device.api.verify_module_status(
                        timeout=check_modules['timeout'],
                        interval=check_modules['interval'],
                        ignore_modules=check_modules['ignore_modules'])
                except Exception as e:
                    step.failed("Modules are not in a stable state",
                                from_exception=e)

