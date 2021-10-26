'''
IOSXE SDWAN specific clean stages
'''

# Python
import re
import time
import logging

# pyATS
from pyats.async_ import pcall

# Genie
from genie.abstract import Lookup
from genie.libs import clean
from genie.libs.clean.utils import (_apply_configuration,
                                    handle_rommon_exception)
from genie.libs.clean.recovery.iosxe.sdwan.recovery import recovery_worker as sdwan_recovery_worker
from genie.metaparser.util.schemaengine import Optional, Or
from genie.utils.timeout import Timeout
from genie.libs.clean import BaseStage
from genie.libs.clean.stages.stages import Connect as CommonConnect
from genie.libs.clean.stages.iosxe.stages import ChangeBootVariable as XeChangeBootVariable

# Unicon
from unicon.eal.dialogs import Statement, Dialog

# Logger
log = logging.getLogger(__name__)


class Connect(CommonConnect):
    """This stage connects to the device that is being cleaned.

Stage Schema
------------
connect:

    via (str, optional): Which connection to use from the testbed file. Uses the
        default connection if not specified.

    timeout (int, optional): The timeout for the connection to complete in seconds.
        Defaults to 200.

    retry_timeout (int, optional): Overall timeout for retry mechanism in seconds.
        Defaults to 0 which means no retry.

    retry_interval (int, optional): Interval for retry mechanism in seconds. Defaults
        to 0 which means no retry.

Example
-------
connect:
    timeout: 60
"""

    # =================
    # Argument Defaults
    # =================
    VIA = None
    TIMEOUT = 200
    RETRY_TIMEOUT = 0
    RETRY_INTERVAL = 0
    INIT_EXEC_COMMANDS = ['pnpa service discovery stop', 'show version']
    INIT_CONFIG_COMMANDS = []

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('via'): str,
        Optional('timeout'): Or(str, int),
        Optional('retry_timeout'): Or(str, int, float),
        Optional('retry_interval'): Or(str, int, float),
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = ['connect']

    def connect(self,
                steps,
                device,
                via=VIA,
                timeout=TIMEOUT,
                retry_timeout=RETRY_TIMEOUT,
                retry_interval=RETRY_INTERVAL,
                init_exec_commands=INIT_EXEC_COMMANDS,
                init_config_commands=INIT_CONFIG_COMMANDS):

        with steps.start("Connecting to the device") as step:

            log.info('Checking connection to device: %s' % device.name)

            # Create a timeout that will loop
            retry_timeout = Timeout(float(retry_timeout),
                                    float(retry_interval))
            retry_timeout.one_more_time = True
            # Without this we see 'Performing the last attempt' even if retry
            # is not being used.
            retry_timeout.disable_log = True

            while retry_timeout.iterate():
                retry_timeout.disable_log = False

                # overwrite platform as iosxe
                device.platform = 'iosxe'

                # If the device is in rommon, just raise an exception
                device.instantiate(connection_timeout=timeout,
                                   learn_hostname=True,
                                   prompt_recovery=True,
                                   via=via,
                                   init_exec_commands=init_exec_commands,
                                   init_config_commands=init_config_commands)
                device.settings.HA_INIT_CONFIG_COMMANDS = []
                # ignore error for 'pnpa service discovery stop' in case device doesn't support
                device.settings.ERROR_PATTERN = []

                rommon = Statement(
                    pattern=r'^(.*)(rommon(.*)|loader(.*))+>.*$',
                    #action=lambda section: section.failed('Device is in rommon'),
                    action=handle_rommon_exception,
                    loop_continue=False,
                    continue_timer=False)

                autoinstall = Statement(
                    pattern=
                    r'Would you like to terminate autoinstall\? \[yes\]:',
                    action='sendline(yes)',
                    loop_continue=False,
                    continue_timer=False)

                config_dialog = Statement(
                    pattern=
                    r'Would you like to enter the initial configuration dialog\? \[yes/no\]:',
                    action='sendline(no)',
                    loop_continue=False,
                    continue_timer=False)

                device.connect_reply.append(rommon)
                device.connect_reply.append(autoinstall)
                device.connect_reply.append(config_dialog)

                try:
                    output = device.connect()
                    # need to set `sdwan` for config-register 0x0
                    if 'Controller-Managed' in output:
                        try:
                            device.destroy_all()
                        except Exception as e:
                            log.warning(f'{e}')
                        device.destroy_all()
                        device.platform = 'sdwan'
                        log.info(
                            "Router operating mode is Controller-Managed. so reconnecting as 'iosxe/sdwan' device."
                        )
                        device.instantiate(
                            connection_timeout=timeout,
                            learn_hostname=True,
                            prompt_recovery=True,
                            via=via,
                            init_exec_commands=init_exec_commands,
                            init_config_commands=init_config_commands)
                        device.settings.HA_INIT_CONFIG_COMMANDS = []
                except Exception:

                    try:
                        device.destroy_all()
                    except Exception as e:
                        log.warning(f'{e}')

                    device.platform = 'iosxe'
                    device.instantiate(
                        connection_timeout=timeout,
                        learn_hostname=True,
                        prompt_recovery=True,
                        via=via,
                        init_exec_commands=init_exec_commands,
                        init_config_commands=init_config_commands)
                    device.settings.HA_INIT_CONFIG_COMMANDS = []

                    _, password = device.api.get_username_password()

                    username_stmt = Statement(pattern=r'Username:',
                                              action='sendline(admin)',
                                              loop_continue=True,
                                              continue_timer=False)
                    password_stmt = Statement(pattern=r'Password:',
                                              action='sendline(admin)',
                                              loop_continue=True,
                                              continue_timer=False)
                    new_password_stmt = Statement(
                        pattern=r'Enter new password:',
                        action=f'sendline({password})',
                        loop_continue=True,
                        continue_timer=False)
                    confirm_password_stmt = Statement(
                        pattern=r'Confirm password:',
                        action=f'sendline({password})',
                        loop_continue=True,
                        continue_timer=False)

                    for stmt in [
                            username_stmt, password_stmt, new_password_stmt,
                            confirm_password_stmt
                    ]:
                        device.connect_reply.append(stmt)

                    try:
                        output = device.connect()

                        if 'Controller-Managed' in output:
                            try:
                                device.destroy_all()
                            except Exception as e:
                                log.warning(f'{e}')
                            device.destroy_all()
                            device.platform = 'sdwan'
                            log.info(
                                "Router operating mode is Controller-Managed. so reconnecting as 'iosxe/sdwan' device."
                            )
                            device.instantiate(
                                connection_timeout=timeout,
                                learn_hostname=True,
                                prompt_recovery=True,
                                via=via,
                                init_exec_commands=init_exec_commands,
                                init_config_commands=init_config_commands)
                            device.settings.HA_INIT_CONFIG_COMMANDS = []

                    except Exception:
                        log.error("Connection to the device failed",
                                  exc_info=True)
                        if device.connected:
                            device.destroy_all()
                    finally:
                        try:
                            device.connect_reply.remove(rommon)
                        except Exception as e:
                            log.warning(f'{e}')
                        step.passed("Successfully connected".format(
                            device.name))
                else:
                    if 'Controller-Managed' in output:

                        try:
                            device.destroy_all()
                        except Exception as e:
                            log.warning(f'{e}')

                        device.platform = 'sdwan'
                        log.info(
                            "Router operating mode is Controller-Managed. so reconnecting as 'iosxe/sdwan' device."
                        )
                        try:
                            device.connect()
                            log.info("connected as 'iosxe/sdwan'")
                        except Exception:
                            log.error("Connection to the device failed",
                                      exc_info=True)
                            device.destroy_all()
                        finally:
                            try:
                                device.connect_reply.remove(rommon)
                            except Exception:
                                pass
                    else:
                        log.info("Connected as 'iosxe'")

                    step.passed("Successfully connected".format(device.name))
                finally:
                    try:
                        device.connect_reply.remove(rommon)
                    except Exception as e:
                        log.warning(f'{e}')
                    step.passed("Successfully connected".format(device.name))

                retry_timeout.sleep()

            step.failed("Could not connect. Scroll up for tracebacks.")


class ApplyConfiguration(BaseStage):
    """Apply configuration on the device, either by providing a file or a
raw configuration.

Stage Schema
------------
apply_configuration:

    configuration (str, optional): String representation of the configuration to
        apply. Defaults to None.

    configuration_from_file (str, optional): A file that contains a configuration
        that will be read. The configuration contained will then be applied as
        if a string representation of the config was applied. Defaults to None.

    file (str, optional): A saved configuration file that will be used. The file
        will either be used in copy run start or configure replace based on the
        'configure_replace' argument. Defaults to None.

    configure_replace (bool, optional): When 'True' use 'configure replace' instead
        of 'copy run start'. Defaults to False.

    config_timeout (int, optional): Max time in seconds allowed for applying the
        configuration. Defaults to 60.

    config_stable_time (int, optional): Max time in seconds allowed for the
        configuration to stabilize. Defaults to 10.

    copy_vdc_all (bool, optional): If 'True' copy on all VDCs. Defaults to False.

    max_time (int, optional): Maximum time in seconds allowed for any
        verifications. Defaults to 300.

    check_interval (int, optional): How often in seconds to check. Defaults to 60.

    skip_copy_run_start (bool, optional): If 'True' do not copy the running config
        to the startup config. Defaults to False.

    copy_directly_to_startup (bool, optional): If 'True' copy the provided
        configuration directly to the startup config. Defaults to False.

Example
-------
apply_configuration:
    configuration: |
        interface ethernet2/1
        no shutdown
    config_timeout: 600
    config_stable_time: 10
    copy_vdc_all: True
    max_time: 300
    check_interval: 20
    copy_directly_to_startup: False

"""

    # =================
    # Argument Defaults
    # =================
    CONFIGURATION = None
    CONFIGURATION_FROM_FILE = None
    FILE = None
    CONFIG_TIMEOUT = 60
    CONFIG_STABLE_TIME = 10
    COPY_VDC_ALL = False
    MAX_TIME = 300
    CHECK_INTERVAL = 60
    CONFIGURE_REPLACE = False
    SKIP_COPY_RUN_START = False
    COPY_DIRECTLY_TO_STARTUP = False

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('configuration'): str,
        Optional('configuration_from_file'): str,
        Optional('file'): str,
        Optional('config_timeout'): int,
        Optional('config_stable_time'): int,
        Optional('configure_replace'): bool,
        Optional('copy_directly_to_startup'): bool,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = ['apply_configuration']

    def apply_configuration(self,
                            steps,
                            device,
                            configuration=CONFIGURATION,
                            configuration_from_file=CONFIGURATION_FROM_FILE,
                            file=FILE,
                            config_timeout=CONFIG_TIMEOUT,
                            config_stable_time=CONFIG_STABLE_TIME,
                            configure_replace=CONFIGURE_REPLACE,
                            copy_directly_to_startup=COPY_DIRECTLY_TO_STARTUP):

        log.info("Section steps:\n1- Copy/Apply configuration to/on the device"
                 "\n2- Copy running-config to startup-config"
                 "\n3- Sleep to stabilize configuration on the device")

        # User has provided raw output or configuration file to apply onto device
        with steps.start("Apply configuration to device {} after reload".\
                         format(device.name)) as step:
            try:
                _apply_configuration(
                    device=device,
                    configuration=configuration,
                    configuration_from_file=configuration_from_file,
                    file=file,
                    configure_replace=configure_replace,
                    timeout=config_timeout,
                    copy_directly_to_startup=copy_directly_to_startup)
            except Exception as e:
                step.failed("Error while applying configuration to device "
                            "{}\n{}".format(device.name, str(e)))
            else:
                step.passed(
                    "Successfully applied configuration to device {} ".format(
                        device.name))

        # Allow configuration to stabilize
        with steps.start("Allow configuration to stabilize on device {}".\
                         format(device.name)) as step:
            log.info("Sleeping for '{}' seconds".format(config_stable_time))
            time.sleep(config_stable_time)
            self.passed("Successfully applied configuration after reloading "
                        "device {}".format(device.name))


class TftpBoot(BaseStage):
    """This stage boots a new image onto your device using the tftp booting
    method.

Stage Schema
------------
tftp_boot:

    image (list): Image to boot with

    ip_address (list): Management ip address to configure to reach to the tftp server

    subnet_mask (str): Management subnet mask

    gateway (str): Management gateway

    tftp_server (str): Tftp server that is reachable with management interface

    device_managed_mode (str, optional): Specify mode 'controller' or 'autonomous'
        Defaults to 'autonomous'

    recovery_password (str, optional): Enable password for device
        required after bootup. Defaults to None.

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
    device_managed_mode: autonomous
    recovery_password: nbv_12345
    timeout: 600
    config_reg_timeout: 10

There is more than one ip address, one for each supervisor.
"""

    # =================
    # Argument Defaults
    # =================
    RECOVERY_PASSWORD = None
    TIMEOUT = 600
    CONFIG_REG_TIMEOUT = 30
    SAVE_SYSTEM_CONFIG = False
    DEVICE_MANAGED_MODE = 'autonomous'

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
        Optional('device_managed_mode'): str,
        Optional('timeout'): int,
        Optional('config_reg_timeout'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = ['tftp_boot']

    def tftp_boot(self,
                  steps,
                  device,
                  image,
                  ip_address,
                  subnet_mask,
                  gateway,
                  tftp_server,
                  recovery_password=RECOVERY_PASSWORD,
                  device_managed_mode=DEVICE_MANAGED_MODE,
                  save_system_config=SAVE_SYSTEM_CONFIG,
                  timeout=TIMEOUT,
                  config_reg_timeout=CONFIG_REG_TIMEOUT):

        log.info("Section steps:"
                 "\n1- Set config-register to 0x40"
                 "\n2- Bring device down to rommon> prompt prior to TFTP boot"
                 "\n3- Begin TFTP boot"
                 "\n4- Reconnect to device after TFTP boot"
                 "\n5- Reset config-register to 0x2101"
                 "\n6- Execute 'write memory'")

        # Set config-register to 0x0
        with steps.start("Set config-register to 0x40 on {}".format(
                device.name)) as step:
            try:
                # device.api.execute_set_config_register(config_register='0x0',
                #                                        timeout=config_reg_timeout)
                # going to rommon and not load config
                device.configure('config-register 0x40')
                if device.platform == 'sdwan':
                    log.info(
                        'changing unicon plugin to iosxe from iosxe/sdwan by reconnecting'
                    )
                    try:
                        device.destroy_all()
                    except Exception as e:
                        log.warning(f'{e}')

                    device.platform = 'iosxe'
                    log.info(
                        "Router operating mode is Controller-Managed. so reconnecting as 'iosxe/sdwan' device."
                    )
                    device.instantiate(learn_hostname=True,
                                       prompt_recovery=True,
                                       init_exec_commands=[],
                                       init_config_commands=[])
                    try:
                        device.connect()
                        log.info("connected as 'iosxe/sdwan'")
                    except Exception:
                        log.error("Re-connection to the device failed",
                                  exc_info=True)

            except Exception as e:
                step.failed(
                    "Unable to set config-register to 0x0 prior to TFTP"
                    " boot on {}".format(device.name), )

        # Bring the device down to rommon> prompt prior to TFTP boot
        with steps.start("Bring device {} down to rommon> prompt prior to TFTP boot".\
                            format(device.name)) as step:

            reload_dialog = Dialog([
                Statement(
                    pattern=
                    r".*System configuration has been modified\. Save\? \[yes\/no\].*",
                    action='sendline(yes)'
                    if save_system_config else 'sendline(no)',
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
                    device.expect(['.*Initializing Hardware.*'],
                                  target=target,
                                  timeout=60)

                pcall(reload_check,
                      ckwargs={'device': device},
                      ikwargs=[{
                          'target': 'active'
                      }, {
                          'target': 'standby'
                      }])
            else:
                device.expect(['.*Initializing Hardware.*'], timeout=120)

            log.info("Device is reloading")
            device.destroy_all()

        # Begin TFTP boot of device
        with steps.start("Begin TFTP boot of device {}".format(
                device.name)) as step:

            # Need to instantiate to get the device.start
            # The device.start only works because of a|b
            device.platform = 'iosxe'
            device.instantiate(connection_timeout=timeout)

            tftp_boot = {
                'ip_address': ip_address,
                'subnet_mask': subnet_mask,
                'gateway': gateway,
                'tftp_server': tftp_server,
                'image': image,
                'device_managed_mode': device_managed_mode
            }
            try:
                abstract = Lookup.from_device(device,
                                              packages={'clean': clean})
                # Item is needed to be able to know in which parallel child

                # device.start only gets filled with single rp devices
                # for multiple rp devices we need to use subconnections
                if device.is_ha and hasattr(device, 'subconnections'):
                    start = [i.start[0] for i in device.subconnections]
                else:
                    start = device.start

                result = pcall(sdwan_recovery_worker,
                               start=start,
                               ikwargs = [{'item': i} for i, _ in enumerate(start)],
                               ckwargs = \
                                    {'device': device,
                                     'timeout': timeout,
                                     'tftp_boot': tftp_boot,
                                     'break_count': 0,
                                     # Irrelevant as we will not use this pattern anyway
                                     # But needed for the recovery
                                     'console_activity_pattern': '\\.\\.\\.\\.',
                                     'golden_image': None,
                                     'recovery_password': recovery_password})
            except Exception as e:
                log.error(str(e))
                step.failed("Failed to TFTP boot the device '{}'".\
                               format(device.name), )
            else:
                log.info("Successfully performed TFTP boot on device '{}'".\
                         format(device.name))

        # Disconnect and reconnect to the device
        with steps.start("Reconnect to device {} after TFTP boot".\
                            format(device.name)) as step:

            try:
                device.destroy_all()
            except Exception as e:
                log.debug(f'error with destroy(): {e}')
                pass

            # need to be as `iosxe` at this point
            # if device.platform != 'iosxe':
            log.debug(f"device.platform : {device.platform}")
            log.debug("changing platform to iosxe...")
            device.platform = 'iosxe'
            log.debug(f"device.platform : {device.platform}")
            device.instantiate(learn_hostname=True,
                               prompt_recovery=True,
                               init_exec_commands=[],
                               init_config_commands=[])
            log.debug(f"device.platform : {device.platform}")
            device.settings.HA_INIT_CONFIG_COMMANDS = ['no logging console']
            try:
                device.connect()
            except Exception as e:
                # If that still doesn't work, Thats all we got
                step.failed(
                    f"Cannot reconnect to the device {device.name} after TFTP boot"
                )

            step.passed(
                f"Success - Have recovered and reconnected to device '{device.name}'"
            )

        # Reset config-register to 0x2101
        with steps.start("Reset config-register to 0x2101 on {}".\
                            format(device.name)) as step:
            try:
                device.api.execute_set_config_register(
                    config_register='0x2102', timeout=config_reg_timeout)
            except Exception as e:
                log.error(str(e))
                step.failed(
                    f"Unable to reset config-register to 0x2101 after TFTP boot on {device.name}"
                )

        # Execute 'write memory'
        with steps.start("Execute 'write memory' on {}".format(
                device.name)) as step:
            try:
                device.api.execute_write_memory()
            except Exception as e:
                log.error(str(e))
                step.failed(
                    f"Unable to execute 'write memory' after TFTP boot on {device.name}"
                )
            else:
                step.passed(
                    f"Successfully performed TFTP boot on device {device.name}"
                )


class ExpandImage(BaseStage):
    """Clear up old packages and expand image

Stage Schema
------------
expand_image:

    image (list, optional): Image to boot with

Example
-------
expand_image:
    image:
      - bootflash:stay-isr-image.bin
"""

    conf_file = 'bootflash:packages.conf'

    # =================
    # Argument Defaults
    # =================
    # N/A

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('image'): list,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'erase_config', 'clean_package', 'expand_image'
    ]

    def erase_config(self, steps, device):

        with steps.start("Deleting configuration.") as step:

            device.execute('write erase')
            device.execute('delete /force bootflash:ciscosdwan*.cfg')

    def clean_package(self, steps, device):

        with steps.start("Cleaning old package info") as step:

            clean_package_dialog = Dialog([
                Statement(pattern=r'Do you want to proceed\? \[y/n\]',
                          action='sendline(y)',
                          loop_continue=True,
                          continue_timer=False),
            ])

            device.execute('request platform software package clean',
                           reply=clean_package_dialog)

    def expand_image(self, steps, device, image):

        with steps.start("Expanding .bin image file.") as step:

            output = device.execute(
                f'request platform software package expand file {image[0]}')

            # Sample Outputs:
            #   WARNING: bootflash:asr1000-universalk9.17.06.01a.SPA.18.conf
            #   WARNING: packages.conf will replace the identical file that already exists in bootflash:
            m = re.search(r'.*\s+WARNING:\s+(?P<conf_file>\S+.conf)', output)
            if m:
                self.conf_file = m.groupdict()['conf_file']
                if ':' not in self.conf_file:
                    self.conf_file = 'bootflash:' + self.conf_file
                log.info(
                    f'config is saved as {self.conf_file}. This file will be saved as boot variable for boot.'
                )

            image_mapping = self.history['ExpandImage'].parameters.setdefault('image_mapping', {})
            image_mapping.update({image[0]: self.conf_file})


class SetControllerMode(BaseStage):
    """Set controller mode

Stage Schema
------------
set_controller_mode:

    mode (str, optional): `enable` or `disable`. Defaults to `enable`

    reload_timeout (int, optional): maximum time to wait for reload.
        Defaults to 600 secs

    configure_retry_interval (int, optional): interval of retry configure().
        Defaults to 60 secs

    delete_inactive_versions (bool, optional): delete non active version after
        changing image. Defaults to True

Example
-------
set_controller_mode:
    mode: enable
    reload_timeout: 600
    configure_retry_interval: 30
    delete_inactive_versions: True
"""

    # =================
    # Argument Defaults
    # =================
    MODE = 'enable'
    RELOAD_TIMEOUT = 600
    CONFIGURE_RETRY_INTERVAL = 30
    delete_inactive_versions = True

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('mode'): str,
        Optional('reload_timeout'): int,
        Optional('delete_inactive_versions'): bool,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'set_controller_mode', 'confirm_and_set_default',
        'delete_inactive_versions'
    ]

    def set_controller_mode(
        self,
        steps,
        device,
        mode=MODE,
        reload_timeout=RELOAD_TIMEOUT,
    ):

        with steps.start("setting controller mode") as step:

            if device.connected:
                device.destroy_all()

            device.platform = 'iosxe'
            device.connect()

            _, password = device.api.get_username_password()

            # Username: admin
            # Password:
            # Default admin password needs to be changed.
            #
            #
            # Enter new password:
            # Confirm password:
            #
            # Router# pnpa service discovery stop

            controller_mode_dialog = Dialog([
                Statement(pattern=r'Continue\? \[confirm\]',
                          action='sendline()',
                          loop_continue=True,
                          continue_timer=False),
                Statement(pattern=r'Do you want to abort\? \(yes/\[no\]\):',
                          action='sendline(no)',
                          loop_continue=True,
                          continue_timer=False),
                Statement(pattern=r'Username:',
                          action='sendline(admin)',
                          loop_continue=True,
                          continue_timer=False),
                Statement(pattern=r'Password:',
                          action='sendline(admin)',
                          loop_continue=True,
                          continue_timer=False),
                Statement(pattern=r'Enter new password:',
                          action=f'sendline({password})',
                          loop_continue=True,
                          continue_timer=False),
                Statement(pattern=r'Confirm password:',
                          action=f'sendline({password})',
                          loop_continue=True,
                          continue_timer=False),
                Statement(
                    pattern=
                    r'Would you like to enter basic management setup\? \[yes/no\]:',
                    action=f'sendline(no)',
                    loop_continue=True,
                    continue_timer=False),
            ])
            device.execute(f'controller-mode {mode}',
                           timeout=reload_timeout,
                           reply=controller_mode_dialog)

    def confirm_and_set_default(
            self,
            steps,
            device,
            configure_retry_interval=CONFIGURE_RETRY_INTERVAL):

        with steps.start("upgrade-confirm and set-default") as step:

            if device.connected:
                device.destroy_all()

            log.debug(f"device.platform : {device.platform}")
            log.debug('changing platform to sdwan...')
            device.platform = 'sdwan'
            log.debug(f"device.platform : {device.platform}")
            device.instantiate(learn_hostname=True,
                               prompt_recovery=True,
                               init_exec_commands=[
                                   'pnpa service discovery stop',
                                   'show version'
                               ],
                               init_config_commands=[])
            log.debug(f"device.platform : {device.platform}")
            self.output = device.connect()
            for attempt in range(5):
                log.info(f'Attempt#{attempt+1}:')
                try:
                    device.configure('no logging console')
                    break
                except Exception as e:
                    if attempt == 4:
                        raise Exception(
                            f"Couldn't enter to configuration mode: {e}")
                    else:
                        time.sleep(configure_retry_interval)

            parsed_output = device.parse('show sdwan software')
            active_version = parsed_output.q.contains_key_value(
                'active', 'true').get_values('version', 0)
            self.non_active_version = parsed_output.q.contains_key_value(
                'active', 'false').get_values('version')

            if active_version:
                commands = [
                    'request platform software sdwan software upgrade-confirm',
                    f'request platform software sdwan software set-default {active_version}',
                    'show sdwan software'
                ]
                device.execute(commands)
            else:
                step.failed('Active version was not confirmed.')

        with steps.start("Verify controller mode") as step:

            if 'Controller-Managed' in self.output:
                step.passed(
                    "Device booted up with controller-mode successfully.")
            else:
                step.failed("Device couldn't boot up with controller-mode")

    def delete_inactive_versions(
            self,
            steps,
            device,
            delete_inactive_versions=delete_inactive_versions):

        with steps.start("deleting non active version") as step:

            if delete_inactive_versions and self.non_active_version:
                for version in self.non_active_version:
                    device.execute(
                        f"request platform software sdwan software remove {version}"
                    )
                device.execute("show sdwan software")
                log.info(
                    f"Non active versions {self.non_active_version} are deleted."
                )


class ChangeBootVariable(XeChangeBootVariable):
    """This stage change boot variables of the device using the following steps:

    - Delete existing boot variables.
    - Configure boot variables using the provided 'images'.
    - Write memory.

Stage Schema
------------
change_boot_variable:

    images (list): Image files to use when configuring the boot variables.

    timeout (int, optional): Execute timeout in seconds. Defaults to 300.

Example
-------
change_boot_variable:
    timeout: 150
"""

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('images'): list,
        Optional('timeout'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'delete_boot_variable',
        'configure_boot_variable',
        'write_memory',
    ]
