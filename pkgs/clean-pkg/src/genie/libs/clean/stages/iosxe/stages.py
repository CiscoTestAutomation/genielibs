"""
IOSXE specific clean stages
"""

# Python
import re
import copy
import json
import time
import os.path
import logging
from textwrap import dedent
from ipaddress import IPv4Address, IPv6Address, IPv4Interface, IPv6Interface

# pyATS
from pyats.async_ import pcall
from pyats.utils.fileutils import FileUtils

# Genie
from genie.abstract import Lookup
from genie.libs import clean
from genie.libs.clean.recovery.recovery import _disconnect_reconnect
from genie.utils import Dq
from genie.utils.config import Config
from genie.metaparser.util.schemaengine import Optional, Required, Any, Or, ListOf
from genie.utils.timeout import Timeout
from genie.libs.clean import BaseStage
from genie.libs.sdk.libs.abstracted_libs.iosxe.subsection import get_default_dir
from genie.libs.clean.utils import (
    find_clean_variable,
    verify_num_images_provided,
    remove_string_from_image,
    raise_,
)

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure
from unicon.plugins.generic.statements import GenericStatements
from unicon.core.errors import UniconAuthenticationError, UniconBackendDecodeError

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
    CONFIG_REGISTER = "0x2102"
    CURRENT_RUNNING_IMAGE = False

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional("images"): list,
        Optional("timeout"): int,
        Optional("config_register"): str,
        Optional("current_running_image"): bool,
        # Deprecated
        Optional("check_interval"): int,
        Optional("max_time"): int,
        Optional("write_memory"): bool,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        "delete_boot_variable",
        "configure_boot_variable",
        "set_configuration_register",
        "write_memory",
        "verify_boot_variable",
        "verify_configuration_register",
    ]

    def delete_boot_variable(self, steps, device):
        with steps.start(
            "Delete any configured boot variables on {}".format(device.name)
        ) as step:

            try:
                device.configure("no boot system")
            except Exception as e:
                step.failed(
                    "Failed to delete configured boot variables", from_exception=e
                )
            else:
                step.passed("Successfully deleted configured boot variables")

    def configure_boot_variable(
        self,
        steps,
        device,
        images,
        timeout=TIMEOUT,
        current_running_image=CURRENT_RUNNING_IMAGE,
    ):

        with steps.start(
            "Set boot variable to images provided for {}".format(device.name)
        ) as step:

            if current_running_image:
                log.info(
                    "Retrieving and using the running image due to "
                    "'current_running_image: True'"
                )

                try:
                    output = device.parse("show version")
                    images = self.running_images = [output["version"]["system_image"]]
                except Exception as e:
                    step.failed(
                        "Failed to retrieve the running image. Cannot "
                        "set boot variables",
                        from_exception=e,
                    )

            try:
                device.api.execute_set_boot_variable(
                    boot_images=images, timeout=timeout
                )
            except Exception as e:
                step.failed(
                    "Failed to set boot variables to images provided", from_exception=e
                )
            else:
                step.passed("Successfully set boot variables to images provided")

    def set_configuration_register(
        self, steps, device, config_register=CONFIG_REGISTER, timeout=TIMEOUT
    ):
        with steps.start(
            "Set config register to boot new image on {}".format(device.name)
        ) as step:

            try:
                device.api.execute_set_config_register(
                    config_register=config_register, timeout=timeout
                )
            except Exception as e:
                step.failed("Failed to set config-register", from_exception=e)
            else:
                step.passed("Successfully set config register")

    def write_memory(self, steps, device, timeout=TIMEOUT):
        with steps.start("Execute 'write memory' on {}".format(device.name)) as step:
            try:
                device.api.execute_write_memory(timeout=timeout)
            except Exception as e:
                step.failed("Failed to execute 'write memory'", from_exception=e)
            else:
                step.passed("Successfully executed 'write memory'")

    def verify_boot_variable(
        self, steps, device, images, current_running_image=CURRENT_RUNNING_IMAGE
    ):
        with steps.start(
            "Verify next reload boot variables are correctly set "
            "on {}".format(device.name)
        ) as step:

            if current_running_image:
                log.info(
                    "Verifying next reload boot variables Using the running image due to "
                    "'current_running_image: True'"
                )
                images = self.running_images

            if current_running_image:
                log.info("Verifying next reload boot variables Using the running image due to "
                         "'current_running_image: True'")
                images = self.running_images

            if not device.api.verify_boot_variable(boot_images=images):
                step.failed("Boot variables are NOT correctly set")
            else:
                step.passed("Boot variables are correctly set")

    def verify_configuration_register(
        self, steps, device, config_register=CONFIG_REGISTER
    ):
        with steps.start(
            "Verify config-register is as expected on {}".format(device.name)
        ) as step:

            if not device.api.verify_config_register(
                config_register=config_register, next_reload=True
            ):
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

        image_length_limit(int, optional): Maximum length of characters for image.
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
    RECOVERY_EN_PASSWORD = None
    RECOVERY_USERNAME = None
    SAVE_SYSTEM_CONFIG = False
    TIMEOUT = 1200
    CONFIG_REG_TIMEOUT = 30
    CONFIG_REG_ROMMON = "0x0"
    CONFIG_REG_NORMAL = "0x2101"
    IMAGE_LENGTH_LIMIT = 110
    ETHER_PORT = None
    # ============
    # Stage Schema
    # ============
    schema = {
        "image": list,
        "ip_address": list,
        "subnet_mask": str,
        "gateway": str,
        "tftp_server": str,
        "recovery_password": str,
        "recovery_username": str,
        Optional("recovery_en_password"): str,
        Optional("save_system_config"): bool,
        Optional("timeout"): int,
        Optional("config_reg_timeout"): int,
        Optional("image_length_limit"): int,
        Optional("ether_port"): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        "check_image_length",
        "set_config_register",
        "go_to_rommon",
        "tftp_boot",
        "reconnect",
        "reset_config_register",
        "write_memory",
    ]

    def check_image_length(self, steps, image, image_length_limit=IMAGE_LENGTH_LIMIT):
        log.warning(
            "The next release will REMOVE the following keys from the tftp_boot schema:\n"
            "recovery_password, recovery_username, recovery_en_password, ether_port, save_system_config\n"
            "Please update the clean YAML file accordingly."
        )
        with steps.start("Check the length of image: {}".format(image[0])) as step:
            if len(image[0]) > image_length_limit:
                step.failed(
                    f"The length of image path {image[0]} is more than the limit of"
                    f" {image_length_limit} characters."
                )
            else:
                step.passed(
                    f"The length of image {image[0]} is within the {image_length_limit} character limit."
                )

    def set_config_register(
        self,
        steps,
        device,
        config_reg_rommon=CONFIG_REG_ROMMON,
        config_reg_timeout=CONFIG_REG_TIMEOUT,
    ):
        with steps.start(
            "Set config-register to 0x0 on {}".format(device.name)
        ) as step:
            try:
                device.api.execute_set_config_register(
                    config_register=config_reg_rommon, timeout=config_reg_timeout
                )
            except Exception as e:
                step.failed(
                    "Unable to set config-register to 0x0 prior to TFTP"
                    " boot on {}".format(device.name),
                )

    def go_to_rommon(self, steps, device, save_system_config=SAVE_SYSTEM_CONFIG):
        with steps.start(
            "Bring device {} down to rommon> prompt prior to TFTP boot".format(
                device.name
            )
        ) as step:

            reload_dialog = Dialog(
                [
                    Statement(
                        pattern=r".*System configuration has been modified\. Save\? \[yes\/no\].*",
                        action=(
                            "sendline(yes)" if save_system_config else "sendline(no)"
                        ),
                        loop_continue=True,
                        continue_timer=False,
                    ),
                    Statement(
                        pattern=r".*Proceed with reload\? \[confirm\].*",
                        action="sendline()",
                        loop_continue=False,
                        continue_timer=False,
                    ),
                    Statement(
                        pattern=r".*Continue to reload\? \(yes\/\[no\]\)\:.*",
                        action="sendline(yes)",
                        loop_continue=False,
                        continue_timer=False,
                    ),
                    Statement(
                        pattern=r".*(Proceed|Continue) (with|to) reload\? (\[confirm\]|\(yes\/\[no\]\)\:).*",
                        action="sendline()",
                        loop_continue=False,
                        continue_timer=False,
                    ),
                ]
            )

            # Using sendline, as we dont want unicon boot to kick in and send "boot"
            # to the device. Cannot use device.reload() directly as in case of HA,
            # we need both sup to do the commands
            device.sendline("reload")
            reload_dialog.process(device.spawn)

            if device.is_ha:

                def reload_check(device, target):
                    device.expect(
                        [
                            "(.*Initializing Hardware.*|^(.*)((rommon(.*))+>|switch *:).*$)"
                        ],
                        target=target,
                        timeout=90,
                    )

                # check if device is a stack device(stack with 2 memebrs is similar to HA devices)
                if len(device.subconnections) > 2:
                    pcall(
                        reload_check,
                        cargs=(device,),
                        iargs=[
                            [alias] for alias in device.connections.defaults.connections
                        ],
                    )
                else:
                    pcall(
                        reload_check,
                        ckwargs={"device": device},
                        ikwargs=[{"target": "active"}, {"target": "standby"}],
                    )
            else:
                device.expect(
                    ["(.*Initializing Hardware.*|^(.*)((rommon(.*))+>|switch *:).*$)"],
                    timeout=60,
                )

            log.info("Device is reloading")
            device.destroy_all()

    def tftp_boot(
        self,
        steps,
        device,
        ip_address,
        subnet_mask,
        gateway,
        tftp_server,
        image,
        timeout=TIMEOUT,
        recovery_password=RECOVERY_PASSWORD,
        recovery_username=RECOVERY_USERNAME,
        recovery_en_password=RECOVERY_EN_PASSWORD,
        ether_port=ETHER_PORT,
    ):
        with steps.start("Begin TFTP boot of device {}".format(device.name)) as step:

            # Need to instantiate to get the device.start
            # The device.start only works because of a|b
            device.instantiate(connection_timeout=timeout)

            tftp_boot = {
                "ip_address": ip_address,
                "subnet_mask": subnet_mask,
                "gateway": gateway,
                "tftp_server": tftp_server,
                "image": image,
                "ether_port": ether_port,
            }
            try:
                abstract = Lookup.from_device(device, package=clean)
                # Item is needed to be able to know in which parallel child

                # device.start only gets filled with single rp devices
                # for multiple rp devices we need to use subconnections
                if device.is_ha and hasattr(device, "subconnections"):
                    start = [i.start[0] for i in device.subconnections]
                else:
                    start = device.start

                result = pcall(
                    abstract.recovery.recovery.recovery_worker,
                    start=start,
                    ikwargs=[{"item": i} for i, _ in enumerate(start)],
                    ckwargs={
                        "device": device,
                        "timeout": timeout,
                        "tftp_boot": tftp_boot,
                        "break_count": 0,
                        # Irrelevant as we will not use this pattern anyway
                        # But needed for the recovery
                        "console_activity_pattern": "\\.\\.\\.\\.",
                        "golden_image": None,
                        "recovery_username": recovery_username,
                        "recovery_en_password": recovery_en_password,
                        "recovery_password": recovery_password,
                    },
                )
            except Exception as e:
                log.error(str(e))
                step.failed(
                    "Failed to TFTP boot the device '{}'".format(device.name),
                )
            else:
                log.info(
                    "Successfully performed TFTP boot on device '{}'".format(
                        device.name
                    )
                )

    def reconnect(self, steps, device):
        with steps.start(
            "Reconnect to device {} after TFTP boot".format(device.name)
        ) as step:
            if (
                getattr(device, "chassis_type", None)
                and device.chassis_type.lower() == "stack"
            ):
                log.info("Sleep for 90 seconds in order to sync ")
                time.sleep(90)
            if not _disconnect_reconnect(device):
                # If that still doesnt work, Thats all we got
                step.failed(
                    "Cannot reconnect to the device {d} after TFTP boot".format(
                        d=device.name
                    ),
                )
            else:
                log.info(
                    "Success - Have recovered and reconnected to device '{}'".format(
                        device.name
                    )
                )

    def reset_config_register(
        self,
        steps,
        device,
        config_reg_timeout=CONFIG_REG_TIMEOUT,
        config_reg_normal=CONFIG_REG_NORMAL,
    ):
        with steps.start(
            "Reset config-register to 0x2101 on {}".format(device.name)
        ) as step:
            try:
                device.api.execute_set_config_register(
                    config_register=config_reg_normal, timeout=config_reg_timeout
                )
            except Exception as e:
                log.error(str(e))
                step.failed(
                    "Unable to reset config-register to 0x2101 after TFTP"
                    " boot on {}".format(device.name),
                )

    def write_memory(self, steps, device):
        with steps.start("Execute 'write memory' on {}".format(device.name)) as step:
            try:
                device.api.execute_write_memory()
            except Exception as e:
                log.error(str(e))
                step.failed(
                    "Unable to execute 'write memory' after TFTP boot "
                    "on {}".format(device.name),
                )
            else:
                step.passed(
                    "Successfully performed TFTP boot on device {}".format(device.name)
                )


class InstallRemoveInactive(BaseStage):
    """This stage removes partially installed packages/images left
    on the device. If a super package is left partially installed,
    we cannot attempt to install another until it is removed.

    Stage Schema
    ------------
    install_remove_inactive:
        images (list, optional):
            image to not removed by stage.

        timeout (int, optional): Maximum time to wait for remove process to
            finish. Defaults to 180.

        force_remove (bool, optional): Whether or not to remove the inactive
            package irrespective of availability of passed image. Defaults to True.

    Example
    -------
    install_remove_inactive:
        timeout: 180

    """

    # =================
    # Argument Defaults
    # =================
    TIMEOUT = 180
    FORCE_REMOVE = True

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional("images"): list,
        Optional("timeout"): int,
        Optional("force_remove"): bool,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = ["remove_inactive_pkgs"]

    def remove_inactive_pkgs(
        self, steps, device, images, timeout=TIMEOUT, force_remove=FORCE_REMOVE
    ):
        with steps.start("Removing inactive packages") as step:

            def _check_for_system_image(spawn, system_image=None, force_remove=None):
                if force_remove is True:
                    log.warning(
                        f"Sending yes to delete files without checking {system_image} in among the files to be deleted."
                    )
                    spawn.sendline("y")
                    return

                if system_image and re.search(f"{system_image}\r", spawn.buffer):
                    log.debug(
                        f"{system_image} is among the files to be deleted. send no so the {system_image} is not deleted. "
                    )
                    spawn.sendline("n")
                else:
                    log.debug(
                        f"{system_image} is not among the files to be deleted. Hence, send yes to delete files."
                    )
                    spawn.sendline("y")

            # split the image on the [:/] and pick up the image name
            image = re.split(r"[:/]", images[0])[-1]

            install_remove_inactive_dialog = Dialog(
                [
                    Statement(
                        pattern=r".*Do you want to remove the above files\? \[y\/n\]",
                        action=_check_for_system_image,
                        args={"system_image": image, "force_remove": force_remove},
                        loop_continue=False,
                        continue_timer=False,
                    ),
                ]
            )

            try:
                device.execute(
                    "install remove inactive",
                    service_dialog=install_remove_inactive_dialog,
                    timeout=timeout,
                )
            except Exception as e:
                step.failed("Failed to remove inactive packages", from_exception=e)


class InstallImage(BaseStage):
    """This stage installs a provided image onto the device using the install
    CLI. It also handles the automatic reloading of your device after the
    install is complete.

    Stage Schema
    ------------
    install_image:
        images (list): Image to install

        directory (str): directory where packages.conf is created


        save_system_config (bool, optional): Whether or not to save the system
            config if it was modified. Defaults to False.

        skip_save_running_config (bool, optional): Skip the step to save the the running
                                            configuration to the startup config.

        install_timeout (int, optional): Maximum time in seconds to wait for install
            process to finish. Defaults to 500.

        reload_timeout (int, optional): Maximum time in seconds to wait for reload
            process to finish. Defaults to 800.

        verify_running_image (bool, optional): Compare the image filename with the running
            image version on device. If a match is found, the stage will be skipped.
            Defaults to True.

        reload_service_args (optional):

            reload_creds (str, optional): The credential to use after the reload is
                complete. The credential name comes from the testbed yaml file.
                Defaults to the 'default' credential.

            prompt_recovery (bool, optional): Enable or disable the prompt recovery
                feature of unicon. Defaults to True.

            error_pattern (list, optional): List of regex strings to check for errors.
                Default: [r"FAILED:.*?$",]

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
        "reload_creds": "default",
        "prompt_recovery": True,
        "error_pattern": [
            r"FAILED:.*?$",
        ],
    }
    ISSU = False
    SKIP_BOOT_VARIABLE = False
    SKIP_SAVE_RUNNING_CONFIG = False
    VERIFY_RUNNING_IMAGE = True

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional("images"): list,
        Optional("directory"): str,
        Optional("save_system_config"): bool,
        Optional("install_timeout"): int,
        Optional("reload_timeout"): int,
        Optional("issu"): bool,
        Optional("skip_boot_variable"): bool,
        Optional("skip_save_running_config"): bool,
        Optional(
            "verify_running_image",
            description="Compare the image filename with the running image version on device. If a match is found, the stage will be skipped",
            default=VERIFY_RUNNING_IMAGE,
        ): bool,
        Optional("reload_service_args"): {
            Optional("reload_creds"): str,
            Optional("prompt_recovery"): bool,
            Optional("error_pattern"): list,
            Any(): Any(),
        },
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        "verify_running_image",
        "delete_boot_variable",
        "set_boot_variable",
        "save_running_config",
        "verify_boot_variable",
        "install_image",
    ]

    def verify_running_image(
        self, steps, device, images, verify_running_image=VERIFY_RUNNING_IMAGE
    ):
        # Check the running image
        if verify_running_image:
            # Verify the image running in the device
            with steps.start("Verify the image running in the device") as step:
                try:
                    out = device.parse("show version")
                except Exception as e:
                    step.failed("Failed to verify the running image")

                # if the device is in bundle mode this step will not be executed.
                if "BUNDLE" in Dq(out).get_values("mode"):
                    step.skipped(
                        f"The device is in bundle mode. Skipping the verify running image check."
                    )
                else:
                    # Match the build_label if present, otherwise the xe_version
                    # If neither is found, fail to match the image
                    xe_version = out.get("version", {}).get("xe_version", "")
                    build_label = out.get("version", {}).get("build_label", "")
                    image_version = build_label or xe_version
                    image_match = re.search(image_version, images[0])
                    if image_match and image_match.group():
                        image_mapping = self.history[
                            "InstallImage"
                        ].parameters.setdefault("image_mapping", {})
                        system_image = device.api.get_running_image()
                        image_mapping.update({images[0]: system_image})
                        self.skipped(
                            f"The image file provided is same as the current running image {image_version} on the device.\n\
                                    Skipping the install image stage."
                        )

    def delete_boot_variable(
        self, steps, device, issu=ISSU, skip_boot_variable=SKIP_BOOT_VARIABLE
    ):
        with steps.start("Delete all boot variables") as step:
            if issu or skip_boot_variable:
                step.skipped()
            else:
                try:
                    device.configure("no boot system")
                except Exception as e:
                    step.failed(
                        "Failed to delete configured boot variables", from_exception=e
                    )

    def set_boot_variable(
        self,
        steps,
        device,
        directory=None,
        issu=ISSU,
        skip_boot_variable=SKIP_BOOT_VARIABLE,
    ):
        with steps.start("Configure system boot variable for 'install mode'") as step:
            if issu or skip_boot_variable:
                step.skipped()
            else:
                # Figure out the directory that the image files get unpacked to
                if not directory:
                    output = device.parse(f"dir")
                    directory = output["dir"]["dir"]
                    output = device.parse("dir")
                else:
                    output = device.parse(f"dir {directory}")
                files = output.get("dir", {}).get(directory, {}).get("files", {})

                if not files.get("packages.conf"):
                    # create packages.conf, if it does not exist
                    device.tclsh('puts [open "%spackages.conf" w+] {}' % directory)

                # packages.conf is hardcoded because install mode boots using an
                # unpacked packages.conf file
                self.new_boot_var = directory + "packages.conf"

                try:
                    device.api.execute_set_boot_variable(
                        boot_images=[self.new_boot_var], timeout=60
                    )
                except Exception as e:
                    step.failed(
                        "Failed to configure the boot variable", from_exception=e
                    )

                log.info(f'Unconfigure the ignore startup config on {device.name}')
                try:
                   device.api.unconfigure_ignore_startup_config()
                except Exception as e:
                    step.failed(f"Failed to unconfigure ignore startup config on the device {device.name}",
                            from_exception=e)

    def save_running_config(self, steps, device, skip_save_running_config=SKIP_SAVE_RUNNING_CONFIG):
        with steps.start("Save the running config to the startup config") as step:
            if skip_save_running_config:
                step.skipped()
                return
            try:
                device.api.execute_copy_run_to_start(max_time=60, check_interval=30)
            except Exception as e:
                step.failed("Failed to save the running config", from_exception=e)


    def verify_boot_variable(self, steps, device, issu=ISSU, skip_boot_variable=SKIP_BOOT_VARIABLE):
        # Verify next reload boot variables are correctly set
        with steps.start("Verify next reload boot variables are correctly set") as step:
            if issu or skip_boot_variable:
                step.skipped()
            else:
                if not device.api.verify_boot_variable(boot_images=[self.new_boot_var]):
                    step.failed(f"Boot variables are not correctly set to "
                                f"{self.new_boot_var}")
            log.info(f'verify the ignore startup config')
            if not device.api.verify_ignore_startup_config():
                step.failed(f"Failed to verify unconfigure the ignore startup config on {device.name}")

    def install_image(
        self,
        steps,
        device,
        images,
        save_system_config=SAVE_SYSTEM_CONFIG,
        install_timeout=INSTALL_TIMEOUT,
        reload_service_args=None,
        issu=ISSU,
    ):

        # Set default reload args
        reload_args = self.RELOAD_SERVICE_ARGS.copy()
        # Disable device recovery for reload
        reload_args.update({"device_recovery": False})
        # If user provides custom values, update the default with the user
        # provided.
        if reload_service_args:
            reload_args.update(reload_service_args)

        with steps.start(f"Installing image '{images[0]}'") as step:
            current_image = device.api.get_running_image()
            if current_image == images[0]:
                step.skipped("Images is already installed on the device.")

            install_add_one_shot_dialog = Dialog(
                [
                    Statement(
                        pattern=r".*Press Quit\(q\) to exit, you may save "
                        r"configuration and re-enter the command\. "
                        r"\[y\/n\/q\]",
                        action="sendline(y)" if save_system_config else "sendline(n)",
                        loop_continue=True,
                        continue_timer=False,
                    ),
                    Statement(
                        pattern=r".*Please confirm you have changed boot config "
                        r"to \S+ \[y\/n\]",
                        action="sendline(y)",
                        loop_continue=True,
                        continue_timer=False,
                    ),
                    Statement(
                        pattern=r".*Same Image File-No Change",
                        loop_continue=False,
                        continue_timer=False,
                    ),
                    Statement(
                        pattern=r".*reload of the system\. "
                        r"Do you want to proceed\? \[y\/n\]",
                        action="sendline(y)",
                        loop_continue=True,
                        continue_timer=False,
                    ),
                    Statement(
                        pattern=r"FAILED:.*?$",
                        action=None,
                        loop_continue=False,
                        continue_timer=False,
                    ),
                ]
            )

            try:
                reload_args.update(
                    {"timeout": install_timeout, "reply": install_add_one_shot_dialog}
                )
                if issu:
                    device.reload(
                        "install add file {} activate issu commit prompt-level none".format(
                            images[0]
                        ),
                        **reload_args,
                    )
                else:
                    device.reload(
                        "install add file {} activate commit prompt-level none".format(
                            images[0]
                        ),
                        **reload_args,
                    )

                device.execute("install commit")

            except Exception as e:
                step.failed("Failed to install the image", from_exception=e)

            image_mapping = self.history["InstallImage"].parameters.setdefault(
                "image_mapping", {}
            )
            if hasattr(self, "new_boot_var"):
                image_mapping.update({images[0]: self.new_boot_var})


class InstallRemoveSmu(BaseStage):
    """This stage removes smu images from the device.
    If the SMU is installed, it will be de-activated first.

    Stage Schema
    ------------
    install_remove_smu:

        timeout (int, optional): Maximum time to wait for remove process to
            finish. Defaults to 180.

        force_remove (bool, optional): Whether or not to remove the inactive
            package irrespective of availability of passed image. Defaults to True.

    Example
    -------
    install_remove_smu:
        timeout: 180

    """

    # =================
    # Argument Defaults
    # =================
    TIMEOUT = 180
    FORCE_REMOVE = True
    RELOAD_TIMEOUT = 800
    RELOAD_SERVICE_ARGS = {
        "reload_creds": "default",
        "prompt_recovery": True,
        "error_pattern": [
            r"FAILED:.*?$",
        ],
    }

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional("timeout"): int,
        Optional("force_remove"): bool,
        Optional("reload_timeout"): int,
        Optional("reload_service_args"): {
            Optional("reload_creds"): str,
            Optional("prompt_recovery"): bool,
            Optional("error_pattern"): list,
            Any(): Any(),
        },
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = ["remove_smu_image"]

    def remove_smu_image(
        self,
        steps,
        device,
        reload_timeout=RELOAD_TIMEOUT,
        timeout=TIMEOUT,
        reload_service_args=None,
        force_remove=FORCE_REMOVE,
    ):

        with steps.start("Removing SMU image") as step:

            def _check_for_system_image(
                spawn, system_image=None, force_remove=None
                ):
                    if force_remove is True:
                        log.warning(
                            f"Sending yes to delete files without checking {system_image} in among the files to be deleted."
                        )
                        spawn.sendline("y")
                        return

                    if system_image and re.search(f"{system_image}\r", spawn.buffer):
                        log.debug(
                            f"{system_image} is among the files to be deleted. send no so the {system_image} is not deleted. "
                        )
                        spawn.sendline("n")
                    else:
                        log.debug(
                            f"{system_image} is not among the files to be deleted. Hence, send yes to delete files."
                        )
                        spawn.sendline("y")

            # Set default reload args
            reload_args = self.RELOAD_SERVICE_ARGS.copy()
            # Disable device recovery for reload
            reload_args.update({"device_recovery": False})
            # If user provides custom values, update the default with the user
            # provided.
            if reload_service_args:
                reload_args.update(reload_service_args)

            with steps.start("Checking status of SMU image") as step:
                try:
                    output = device.parse("show install summary")
                    location = list(output.get("location").keys())[0]
                    for pkg in output.get("location").get(location).get("pkg_state"):
                        file_state = output["location"][location]["pkg_state"][pkg][
                            "state"
                        ]
                        file_type = output["location"][location]["pkg_state"][pkg][
                            "type"
                        ]
                        image = output["location"][location]["pkg_state"][pkg][
                                "filename_version"
                        ]
                        if file_state == "C" and file_type == "SMU":
                            log.info("The installed SMU image is in committed state")
                            break
                        elif file_state == "D" and file_type == "SMU":
                            log.info("The installed SMU image is in deactivated state")
                            break
                except Exception as e:
                    step.failed("Failed to check status of smu image", from_exception=e)
                else:
                    if file_state == "C" and file_type == "IMG":
                        step.skipped("No smu image to remove")

                if file_state == "C" and file_type == "SMU":
                    with steps.start(f"Deactivate the smu image '{image}'") as step:
                        try:
                            install_smu_dialog = Dialog(
                                [
                                    Statement(
                                        pattern=r".*reload of the system\. "
                                        r"Do you want to proceed\? \[y\/n\]",
                                        action="sendline(y)",
                                        loop_continue=True,
                                        continue_timer=False,
                                    ),
                                    Statement(
                                        pattern=r"FAILED:.*?$",
                                        action=None,
                                        loop_continue=False,
                                        continue_timer=False,
                                    ),
                                    Statement(
                                        pattern=r"^.*RETURN to get started",
                                        action="sendline()",
                                        loop_continue=False,
                                        continue_timer=False,
                                    ),
                                ]
                            )

                            reload_args.update(
                                {"timeout": reload_timeout, "reply": install_smu_dialog}
                            )
                            device.reload(
                                f"install deactivate file {image}", **reload_args
                            )
                            device.parse("show install summary")
                        except Exception as e:
                            step.failed(
                                "Failed to deactivate SMU image", from_exception=e
                            )

                    with steps.start("commit the smu image") as step:
                        try:
                            output = device.parse("show install summary")
                            location = list(output.get("location").keys())[0]
                            for pkg in (
                                output.get("location").get(location).get("pkg_state")
                            ):
                                file_state = output["location"][location]["pkg_state"][
                                    pkg
                                ]["state"]
                                if file_state == "D":
                                    device.execute("install commit")
                                    device.execute("show install summary")
                                    log.info("The image is in inactivate state")
                        except Exception as e:
                            step.failed("Failed to commit SMU image", from_exception=e)

                    with steps.start("Remove inactive smu image") as step:
                        try:
                            install_remove_smu_inactive_dialog = Dialog(
                                [
                                    Statement(
                                        pattern=r".*Do you want to remove the above files\? \[y\/n\]",
                                        action=_check_for_system_image,
                                        args={"system_image": image, "force_remove": force_remove},
                                        loop_continue=False,
                                        continue_timer=False,
                                    ),
                                ]
                            )
                            device.execute(
                                "install remove inactive",
                                service_dialog=install_remove_smu_inactive_dialog,
                                timeout=timeout,
                            )
                        except Exception as e:
                            step.failed("Failed to remove inactive smu image", from_exception=e)

                elif file_state == "D" and file_type == "SMU":
                    with steps.start("commit the smu image") as step:
                        try:
                            device.execute("install commit")
                            device.execute("show install summary")
                            log.info("The image is in inactivate state")
                        except Exception as e:
                            step.failed("Failed to commit SMU image", from_exception=e)

                    with steps.start("Remove inactive smu image") as step:
                        try:
                            install_remove_smu_inactive_dialog = Dialog(
                                [
                                    Statement(
                                        pattern=r".*Do you want to remove the above files\? \[y\/n\]",
                                        action=_check_for_system_image,
                                        args={"system_image": image, "force_remove": force_remove},
                                        loop_continue=False,
                                        continue_timer=False,
                                    ),
                                ]
                            )
                            device.execute(
                                "install remove inactive",
                                service_dialog=install_remove_smu_inactive_dialog,
                                timeout=timeout,
                            )
                        except Exception as e:
                            step.failed("Failed to remove inactive packages", from_exception=e)
                else:
                    step.skipped("SMU image is in inactive state")


class InstallSmu(BaseStage):
    """This stage installs a provided smu image onto the device using the install
    CLI. It also handles the automatic reloading of your device after the
    install is complete.

    Stage Schema
    ------------
    install_smu:
        images (list): Image to install

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

            error_pattern (list, optional): List of regex strings to check for errors.
                Default: [r"FAILED:.*?$",]

            <Key>: <Value>
                Any other arguments that the Unicon reload service supports

    Example
    -------
    install_smu:
        images:
          - /auto/some-location/that-this/image/smu-image.bin
        install_timeout: 1000
        reload_timeout: 1000

    """

    # =================
    # Argument Defaults
    # =================
    SKIP_SAVE_RUNNING_CONFIG = False
    INSTALL_TIMEOUT = 500
    RELOAD_TIMEOUT = 800
    RELOAD_SERVICE_ARGS = {
        "reload_creds": "default",
        "prompt_recovery": True,
        "error_pattern": [
            r"FAILED:.*?$",
        ],
    }

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional("images"): list,
        Optional("install_timeout"): int,
        Optional("reload_timeout"): int,
        Optional("reload_service_args"): {
            Optional("reload_creds"): str,
            Optional("prompt_recovery"): bool,
            Optional("error_pattern"): list,
            Any(): Any(),
        },
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = ["save_running_config", "install_smu"]

    def save_running_config(
        self, steps, device, skip_save_running_config=SKIP_SAVE_RUNNING_CONFIG
    ):
        with steps.start("Save the running config to the startup config") as step:
            if skip_save_running_config:
                step.skipped()
                return
            try:
                device.api.execute_copy_run_to_start(max_time=60, check_interval=30)
            except Exception as e:
                step.failed("Failed to save the running config", from_exception=e)

    def install_smu(
        self,
        steps,
        device,
        images,
        install_timeout=INSTALL_TIMEOUT,
        reload_service_args=None,
    ):

        with steps.start("Installing smu image") as step:

            if not images:
                step.skipped("No smu image provided, skipping install_smu stage")
            if "smu" not in images[0]:
                step.skipped("No smu image provided, skipping install_smu stage")

            # Set default reload args
            reload_args = self.RELOAD_SERVICE_ARGS.copy()
            # Disable device recovery for reload
            reload_args.update({"device_recovery": False})

            # If user provides custom values, update the default with the user
            # provided.
            if reload_service_args:
                reload_args.update(reload_service_args)

            install_smu_dialog = Dialog(
                [
                    Statement(
                        pattern=r".*reload of the system\. "
                        r"Do you want to proceed\? \[y\/n\]",
                        action="sendline(y)",
                        loop_continue=True,
                        continue_timer=False,
                    ),
                    Statement(
                        pattern=r"FAILED:.*?$",
                        action=None,
                        loop_continue=False,
                        continue_timer=False,
                    ),
                    Statement(
                        pattern=r"^.*RETURN to get started",
                        action="sendline()",
                        loop_continue=False,
                        continue_timer=False,
                    ),
                ]
            )

            with steps.start(f"Add SMU image : '{images[0]}'") as step:
                try:
                    device.execute("install add file {}".format(images[0]))
                except Exception as e:
                    step.failed("Failed to add SMU image", from_exception=e)

            with steps.start("Verify SMU image is added successfully") as step:
                try:
                    output = device.parse("show install summary")
                    location = list(output.get("location").keys())[0]
                    for pkg in output.get("location").get(location).get("pkg_state"):
                        file_state = output["location"][location]["pkg_state"][pkg][
                            "state"
                        ]
                        file_type = output["location"][location]["pkg_state"][pkg][
                            "type"
                        ]
                        try:
                            if file_state == "I" and file_type == "SMU":
                                log.info("The installed SMU image is in inactive state")
                        except Exception as e:
                            step.failed("Failed to add the SMU image", from_exception=e)
                except Exception as e:
                    step.failed("Failed to verify SMU image", from_exception=e)

            with steps.start(f"Activate the SMU file with image '{images[0]}'") as step:
                try:
                    reload_args.update(
                        {"timeout": install_timeout, "reply": install_smu_dialog}
                    )
                    device.reload(
                        "install activate file {}".format(images[0]), **reload_args
                    )
                    device.execute("show version")
                    device.execute("show install summary")
                except Exception as e:
                    step.failed("Failed to activate SMU image", from_exception=e)

            with steps.start("Commit the SMU file with image") as step:
                try:
                    output = device.parse("show install active")
                    location = list(output.get("location").keys())[0]
                    for pkg in output.get("location").get(location).get("pkg_state"):
                        file_state = output["location"][location]["pkg_state"][pkg][
                            "state"
                        ]
                        if file_state == "U":
                            device.execute("install commit")
                            log.info("The image is activated and uncommitted")
                except Exception as e:
                    step.failed("Failed to activate SMU image", from_exception=e)

            with steps.start("Check if SMU is applied succesfully") as step:
                try:
                    output = device.parse("show install summary")
                    for pkg in output.get("location").get(location).get("pkg_state"):
                        file_state = output["location"][location]["pkg_state"][pkg][
                            "state"
                        ]
                        if file_state == "C":
                            log.info("Applied SMU successfully")

                except Exception as e:
                    step.failed("Failed to apply SMU image", from_exception=e)


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
        Optional("packages"): list,
        Optional("save_system_config"): bool,
        Optional("install_timeout"): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = ["install_package"]

    def install_package(
        self,
        steps,
        device,
        packages,
        save_system_config=SAVE_SYSTEM_CONFIG,
        install_timeout=INSTALL_TIMEOUT,
    ):

        install_add_one_shot_dialog = Dialog(
            [
                Statement(
                    pattern=r".*Press Quit\(q\) to exit, you may save "
                    r"configuration and re-enter the command\. "
                    r"\[y\/n\/q\]",
                    action="sendline(y)" if save_system_config else "sendline(n)",
                    loop_continue=True,
                    continue_timer=False,
                ),
                Statement(
                    pattern=r".*Please confirm you have changed boot config "
                    r"to \S+ \[y\/n\]",
                    action="sendline(y)",
                    loop_continue=True,
                    continue_timer=False,
                ),
                Statement(
                    pattern=r".*This operation may require a reload of the "
                    r"system\. Do you want to proceed\? \[y\/n\]",
                    action="sendline(y)",
                    loop_continue=True,
                    continue_timer=False,
                ),
            ]
        )

        for pkg in packages:
            with steps.start(
                "Installing package '{pkg}' onto {dev}".format(
                    pkg=pkg, dev=device.hostname
                )
            ) as step:

                try:
                    device.execute(
                        "install add file {} activate commit".format(pkg),
                        reply=install_add_one_shot_dialog,
                        error_pattern=["FAILED:"],
                        timeout=install_timeout,
                    )
                except Exception as e:
                    step.failed("Failed to install the package", from_exception=e)


class Reload(BaseStage):
    """This stage reloads the device.

    Stage Schema
    ------------
    reload:
        license: (optional)
            check: (bool, optional): Enable the checking license inconsistency and fix

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

        attempt_manual_boot (bool, optional): Enable to attempt manual boot when reload fails.
            Defaults to True.

    Example
    -------
    reload:
        reload_service_args:
            timeout: 600
            reload_creds: clean_reload_creds
            prompt_recovery: True
        check_modules:
            check: False
    """

    # =================
    # Argument Defaults
    # =================
    LICENSE = {"check": False}
    RELOAD_SERVICE_ARGS = {
        "timeout": 800,
        "reload_creds": "default",
        "prompt_recovery": True,
    }
    CHECK_MODULES = {
        "check": True,
        "timeout": 180,
        "interval": 30,
        "ignore_modules": None,
    }
    RECONNECT_VIA = None
    ATTEMPT_MANUAL_BOOT = True

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional("license"): {Optional("check"): bool},
        Optional("check_modules"): {
            Optional("check"): bool,
            Optional("timeout"): int,
            Optional("interval"): int,
            Optional("ignore_modules"): list,
        },
        Optional("reload_service_args"): {
            Optional("timeout"): int,
            Optional("reload_creds"): str,
            Optional("prompt_recovery"): bool,
            Any(): Any(),
        },
        Optional("reconnect_via"): str,
        Optional("attempt_manual_boot"): bool,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = ["reload", "license", "disconnect_and_reconnect", "check_modules"]

    def reload(
        self,
        steps,
        device,
        reload_service_args=None,
        attempt_manual_boot=ATTEMPT_MANUAL_BOOT,
    ):

        if reload_service_args is None:
            # If user provides no custom values, take the defaults
            self.reload_service_args = self.RELOAD_SERVICE_ARGS
        else:
            # If user provides custom values, update the default with the user
            # provided. This is needed because if the user only provides 1 of
            # the many optional arguments, we still need to default the others.
            self.RELOAD_SERVICE_ARGS.update(reload_service_args)
            self.reload_service_args = self.RELOAD_SERVICE_ARGS

        # custom exception for reload
        class ReloadError(BaseException):
            """Exception raised for errors that are specific to reload."""

            pass

        def break_reload(device):
            """Breaks the reload process on a device"""
            log.info(f"Boot variable does not exist!!! Breaking the reload process.")
            # Send No to exit from reload process
            device.sendline("N")

            # Throw custom reload error from base exception.
            raise ReloadError("Exiting the reload process.")

        # Disable device_recovey for reload in unicon
        self.reload_service_args.update({"device_recovery": False})
        reload_dialog = Dialog(
            [
                Statement(
                    pattern=r".*Do you wish to proceed with reload anyway\[confirm\].*",
                    action="sendline(y)",
                    loop_continue=True,
                    continue_timer=False,
                )
            ]
        )

        if attempt_manual_boot:
            reload_dialog.append(
                Statement(
                    pattern=r".*Boot variable either does not exist or buffer is too small.*",
                    action=break_reload,
                    args={"device": device},
                    loop_continue=False,
                    continue_timer=False,
                ),
            )

        self.reload_service_args.update({"reply": reload_dialog})

        with steps.start(f"Reload {device.name}") as step:

            try:
                device.reload(**self.reload_service_args)
            except ReloadError as e:
                # Get the current system image
                try:
                    output = device.parse("show version")
                    system_image = output["version"]["system_image"]
                except Exception as e:
                    log.exception(
                        f"Failed to get the system image from device {device.name}, Error: {e}"
                    )

                config_reg = None
                # capture the current boot settings to restore it on later stage
                try:
                    output = device.parse("show boot")
                    config_reg = output.get("active", {}).get("configuration_register")
                except Exception as e:
                    log.exception(
                        f"Failed to get the boot information for {device.name}, Error: {e}"
                    )

                # Bring the device state to rommon
                device.rommon()

                # If the device is HA then update context for standy rp
                cmd = f"boot {system_image}"
                if device.is_ha and hasattr(device, "subconnections"):
                    for con in device.subconnections:
                        if con.role == "standby":
                            con.context["boot_cmd"] = cmd

                with steps.start(f"Reload using manual boot for {device.name}") as step:
                    try:
                        device.reload(reload_command=cmd)
                    except Exception as e:
                        step.failed(
                            f"Failed to reload within {self.reload_service_args['timeout']} "
                            f"seconds.",
                            from_exception=e,
                        )

                # Restore the boot settings
                if config_reg:
                    device.api.execute_set_config_register(config_register=config_reg)

            except Exception as e:
                step.failed(
                    f"Failed to reload within {self.reload_service_args['timeout']} "
                    f"seconds.",
                    from_exception=e,
                )

    def license(self, steps, device, license=None):

        if license is None:
            license = self.LICENSE

        with steps.start(f"Check license inconsistency on {device.name}") as step:

            if license["check"]:
                out = device.parse("show version")
                if out.q.get_values("license_level", 0) == out.q.get_values(
                    "next_reload_license_level", 0
                ):
                    step.passed("No license inconsistency.")
                else:
                    try:
                        device.reload(**self.reload_service_args)
                    except Exception as e:
                        step.failed(
                            f"Failed to reload within {self.reload_service_args['timeout']} "
                            f"seconds.",
                            from_exception=e,
                        )
            else:
                step.skipped("License check is not enabled.")

    def disconnect_and_reconnect(
        self, steps, device, reload_service_args=None, reconnect_via=RECONNECT_VIA
    ):

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
                log.warning(
                    "Failed to destroy the device connection but "
                    "attempting to continue",
                    exc_info=True,
                )
            connect_kwargs = {
                "learn_hostname": True,
                "prompt_recovery": reload_service_args["prompt_recovery"],
            }

            if reconnect_via:
                connect_kwargs.update({"via": reconnect_via})

            device.instantiate(**connect_kwargs)
            rommon_to_disable = None
            try:
                if device.is_ha and hasattr(device, "subconnections"):
                    if isinstance(device.subconnections, list):
                        rommon_to_disable = device.subconnections[
                            0
                        ].state_machine.get_path("rommon", "disable")
                else:
                    rommon_to_disable = device.state_machine.get_path(
                        "rommon", "disable"
                    )
            except ValueError:
                log.warning("There is no path between rommon and disable states.")
            except IndexError:
                log.warning("There is no connection in device.subconnections")
            if rommon_to_disable and hasattr(rommon_to_disable, "command"):
                original_command = rommon_to_disable.command
                if device.is_ha:
                    index = device.subconnections[0].state_machine.paths.index(
                        rommon_to_disable
                    )
                    for subcon in device.subconnections:
                        subcon.state_machine.paths[index].command = (
                            lambda state, spawn, context: raise_(
                                Exception(
                                    f"Device {device.name} is still "
                                    f"in rommon state after reload."
                                )
                            )
                        )
                else:
                    index = device.state_machine.paths.index(rommon_to_disable)
                    device.state_machine.paths[index].command = (
                        lambda state, spawn, context: raise_(
                            Exception(
                                f"Device {device.name} is still "
                                f"in rommon state after reload."
                            )
                        )
                    )

            try:
                device.connect()
            except Exception as e:
                step.failed("Failed to reconnect", from_exception=e)
            if hasattr(device, "platform") and device.platform != "sdwan":
                if rommon_to_disable and hasattr(rommon_to_disable, "command"):
                    if device.is_ha:
                        index = device.subconnections[0].state_machine.paths.index(
                            rommon_to_disable
                        )
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

        if check_modules["check"]:

            with steps.start(
                f"Checking the modules on '{device.name}' are in a " f"stable state"
            ) as step:

                try:
                    device.api.verify_module_status(
                        timeout=check_modules["timeout"],
                        interval=check_modules["interval"],
                        ignore_modules=check_modules["ignore_modules"],
                    )
                except Exception as e:
                    step.failed("Modules are not in a stable state", from_exception=e)


class RommonBoot(BaseStage):
    """This stage boots an image onto the device through rommon. Using either
    a local image or one from a tftp server.

    Stage Schema
    ------------
    rommon_boot:

        image (list): Image to boot with

        tftp (optional): If specified boot via tftp otherwise boot using local
            image.

            ip_address (list, optional): Management ip address to configure to reach to the
                tftp server

            subnet_mask (str, optional): Management subnet mask

            gateway (str, optional): Management gateway

            tftp_server (str, optional): Tftp server that is reachable with management interface


        recovery_password (str): Enable password for device
            required after bootup. Defaults to None.

        recovery_enable_password (str): Enable password for device
            required after bootup. Defaults to None.

        recovery_username (str): Enable username for device
            required after bootup. Defaults to None.

        save_system_config (bool, optional): Whether or not to save the
            system config if it was modified. Defaults to True.

        timeout (int, optional): Max time allowed for the booting process.
            Defaults to 600.

        config_reg_timeout (int, optional): Max time to set config-register.
            Defaults to 30.

        config_register (str, optional): Specify a custom config register for rommon booting.
            Defaults to 0x0.

        rommon_timeout (int, optional): Timeout after bringing the device to rommon. Default to 15 sec.

        reconnect_timeout (int, optional): Timeout to reconnect the device after booting. Default to 90 sec.

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
        recovery_password: nbv_12345
        recovery_username: user_12345
        recovery_enable_password: en
        save_system_config: False
        timeout: 600
        config_reg_timeout: 10
        config_register: 0x0

    There is more than one ip address, one for each supervisor.

    To pass tftp information and tftp server ip from the testbed, refer the example below

    config_register (str, optional): Specify a custom config register for rommon booting.
        Defaults to 0x0.

    testbed:
      name:
      name:
      passwords:
        tacacs: test
        enable: test
      servers:
        tftp:
        tftp:
            address: 10.x.x.x
            credentials:
                default:
                    username: user
                    password: 1234
    devices:
        uut1:
            management:
                address:
                    ipv4: '10.1.1.1/16'
                gateway:
                    ipv4: '10.1.0.1'

    """

    # =================
    # Argument Defaults
    # =================
    RECOVERY_PASSWORD = None
    RECOVERY_ENABLE_PASSWORD = None
    RECOVERY_USERNAME = None
    SAVE_SYSTEM_CONFIG = True
    TIMEOUT = 600
    ETHER_PORT = 0
    ROMMON_TIMEOUT = 15
    RECONNECT_TIMEOUT = 90
    CONFIG_REGISTER = "0x0"

    # ============
    # Stage Schema
    # ============
    schema = {
        "image": list,
        Optional("tftp"): {
            Optional("ip_address"): list,
            Optional("subnet_mask"): str,
            Optional("gateway"): str,
            Optional("tftp_server"): str,
        },
        Optional("save_system_config"): bool,
        Optional("recovery_password"): str,
        Optional("recovery_username"): str,
        Optional("recovery_enable_password"): str,
        Optional("timeout"): int,
        Optional("ether_port"): int,
        Optional("rommon_timeout"): int,
        Optional("config_register"): str,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        "delete_boot_variables",
        "write_memory",
        "go_to_rommon",
        "rommon_boot",
        "reconnect",
        "enable_device_autoboot",
    ]

    def delete_boot_variables(self, steps, device):
        with steps.start("Delete configured boot variables") as step:
            try:
                device.configure("no boot system")
            except Exception as e:
                step.failed(
                    "Failed to delete configured boot variables", from_exception=e
                )

    def write_memory(self, steps, device):
        with steps.start("Write memory") as step:
            try:
                device.api.execute_write_memory()
            except Exception as e:
                step.failed("Failed to write memory", from_exception=e)

    def go_to_rommon(
        self,
        steps,
        device,
        config_register=CONFIG_REGISTER,
        rommon_timeout=ROMMON_TIMEOUT,
    ):
        with steps.start("Bring device down to rommon mode") as step:
            try:
                device.rommon(config_register=config_register)
            except Exception as e:
                step.failed("Failed to bring device to rommon!", from_exception=e)

            log.info("Device is reloading")
            device.destroy_all()

    def rommon_boot(
        self,
        steps,
        device,
        image,
        tftp=None,
        timeout=TIMEOUT,
        recovery_password=RECOVERY_PASSWORD,
        recovery_username=RECOVERY_USERNAME,
        recovery_enable_password=RECOVERY_ENABLE_PASSWORD,
        ether_port=ETHER_PORT,
    ):
        with steps.start("Boot device from rommon") as step:
            if tftp is not None:
                # Check if management attribute in device object, if not set to empty dict
                if not hasattr(device, "management"):
                    setattr(device, "management", {})

                # Getting the tftp information, if the info not provided by user, it takes from testbed
                address = device.management.get("address", {}).get("ipv4", "")
                if isinstance(address, IPv4Interface):
                    ip_address = [str(address.ip)]
                    subnet_mask = str(address.netmask)
                elif isinstance(address, IPv6Interface):
                    ip_address = [str(address.ip)]
                    subnet_mask = str(address.netmask)
                tftp.setdefault("ip_address", ip_address)
                tftp.setdefault("subnet_mask", subnet_mask)
                tftp.setdefault(
                    "gateway", str(device.management.get("gateway", {}).get("ipv4"))
                )
                tftp.setdefault(
                    "tftp_server", device.testbed.servers.get("tftp", {}).get("address")
                )

            log.info("checking if all the tftp information is given by the user")
            if tftp and not all(tftp.values()):
                log.warning(f"Some TFTP information is missing: {tftp}")
                # setting tftp empty if ttfp information is missing
                tftp = {}

            # Need to instantiate to get the device.start
            # The device.start only works because of a|b
            device.instantiate(connection_timeout=timeout)

            try:
                abstract = Lookup.from_device(device, packages={"clean": clean})
            except Exception as e:
                step.failed("Abstraction lookup failed", from_exception=e)

            # device.start only gets filled with single rp devices
            # for multiple rp devices we need to use subconnections
            if device.is_ha and hasattr(device, "subconnections"):
                start = [i.start[0] for i in device.subconnections]
            else:
                start = device.start

            common_kwargs = {"device": device, "timeout": timeout}

            if tftp:
                tftp.update({"image": image, "ether_port": ether_port})
                common_kwargs.update({"tftp_boot": tftp})
            else:
                common_kwargs.update({"golden_image": image})

            # Update recovery username and password
            common_kwargs.update(
                {
                    "recovery_username": recovery_username,
                    "recovery_en_password": recovery_enable_password,
                    "recovery_password": recovery_password,
                }
            )

            try:
                pcall(
                    targets=abstract.clean.recovery.recovery.recovery_worker,
                    start=start,
                    ikwargs=[{"item": i} for i, _ in enumerate(start)],
                    ckwargs=common_kwargs,
                )
            except Exception as e:
                step.failed("Failed to boot the device from rommon", from_exception=e)

    def reconnect(self, steps, device, reconnect_timeout=RECONNECT_TIMEOUT):
        with steps.start("Reconnect to device") as step:

            if (
                getattr(device, "chassis_type", None)
                and device.chassis_type.lower() == "stack"
            ):
                log.info(f"Sleep for {reconnect_timeout} seconds in order to sync")
                time.sleep(reconnect_timeout)

            if not _disconnect_reconnect(device):
                step.failed("Failed to reconnect")

    def enable_device_autoboot(self, steps, device):
        with steps.start("Enable autoboot after reconnect") as step:

            if hasattr(device.api, "configure_autoboot"):
                try:
                    device.api.configure_autoboot()
                except Exception as e:
                    step.failed(
                        "Failed to configure autoboot on the device", from_exception=e
                    )
            else:
                step.skipped("No autoboot API available")


class CopyToDevice(BaseStage):
    """This stage will copy an image to a device from a networked location.

    Stage Schema
    ------------
    copy_to_device:

        origin:

            files (list): Image files location on the server.

            hostname (str): Hostname or address of the server.

        destination:

            directory (str): Directory on the device to copy the images to.

            standby_directory (str, optional): Standby directory on the device
                to copy the images to. Defaults to None.

        protocol (str): Protocol used for copy operation.

        connection_alias (str): Connection alias to use

        verify_num_images (bool, optional): Verify number of images provided by
            user for clean is correct. Defaults to True.

        verify_running_image (bool, optional): Compare the image filename with the running
            image version on device. If a match is found, the copy stage will be skipped.
            Defaults to True.

        expected_num_images (int, optional): Number of images expected to be
            provided by user for clean. Defaults to 1.

        vrf (str, optional): Vrf used to copy. Defaults to an empty string.

        timeout (int, optional): Copy operation timeout in seconds. Defaults to 300.

        compact (bool, optional): Compact copy mode if supported by the device.
            Defaults to False.

        protected_files (list, optional): File patterns that should not be deleted.
            Defaults to None.

        overwrite (bool, optional): Overwrite the file if a file with the same
            name already exists. Defaults to False.

        skip_deletion (bool, optional): Do not delete any files even if there isn't
            any space on device. Defaults to False.

        copy_attempts (int, optional): Number of times to attempt copying image
            files. Defaults to 1 (no retry).

        copy_attempts_sleep (int, optional): Number of seconds to sleep between
            copy_attempts. Defaults to 30.

        check_file_stability (bool, optional): Verifies that the file size is not
            changing. This ensures the image is not actively being copied.
            Defaults to False.

        stability_check_tries (int, optional): Max number of checks that can be
            done when checking file stability. Defaults to 3.

        stability_check_delay (int, optional): Delay between tries when checking
            file stability in seconds. Defaults to 2.

        min_free_space_percent ('int', optional) : Percentage of total disk space
            that must be free. If specified the percentage is not free then the
            stage will attempt to delete unprotected files to reach the minimum
            percentage. Defaults to None.

        use_kstack (bool, optional): Use faster version of copy with limited options.
            Defaults to False.

        interface (str, optional): The interface to use for file transfers, may be needed
            for copying files on some IOSXE platforms, such as ASR1K when using a VRF
            Defaults to None

        unique_file_name (bool, optional): Appends a random six-digit number to
            the end of the image name. Defaults to False.

        unique_number: (int, optional): Appends the provided number to the end of
            the image name. Defaults to None. Requires unique_file_name is True
            to be applied.

        rename_images: (str, optional): Rename the image to the provided name.
            If multiple files exist then an incrementing number is also appended.
            Defaults to None

        prompt_recovery(bool, optional): Enable the prompt recovery when the  execution
            command timeout. Defaults to False.

    Example
    -------
    copy_to_device:
        origin:
            hostname: server-1
            files:
                - /home/cisco/asr1k.bin
        destination:
            directory: harddisk:/
        protocol: sftp
        timeout: 300
    """

    # =================
    # Argument Defaults
    # =================
    VERIFY_NUM_IMAGES = True
    VERIFY_RUNNING_IMAGE = True
    EXPECTED_NUM_IMAGES = 1
    # must be '' instead of None to prevent NXOS from
    # defaulting to 'management'
    VRF = ""
    TIMEOUT = 300
    COMPACT = False
    USE_KSTACK = False
    PROTECTED_FILES = None
    OVERWRITE = False
    SKIP_DELETION = False
    COPY_ATTEMPTS = 1
    COPY_ATTEMPTS_SLEEP = 30
    CHECK_FILE_STABILITY = False
    STABILITY_CHECK_TRIES = 3
    STABILITY_CHECK_DELAY = 2
    MIN_FREE_SPACE_PERCENT = None
    INTERFACE = None
    UNIQUE_FILE_NAME = False
    UNIQUE_NUMBER = None
    RENAME_IMAGES = None
    PROMPT_RECOVERY = False
    PROTOCOL = "http"
    CONNECTION_ALIAS = "default"

    # ============
    # Stage Schema
    # ============
    schema = {
        "origin": {
            Optional("files", description="Image files location on the server."): list,
            Optional("hostname", description="Hostname or address of the server."): str,
        },
        "destination": {
            Required(
                "directory",
                description="Directory on the device to copy the images to.",
            ): str,
            Optional(
                "standby_directory",
                description="Standby directory on the device to copy the images to",
            ): str,
            Optional(
                "stack_directory",
                description="Stack directories on the device to copy the images to",
            ): list,
        },
        Optional(
            "protocol",
            description="Protocol used for copy operation.",
            default=PROTOCOL,
        ): str,
        Optional(
            "connection_alias", description="Connection alias to use", default="default"
        ): str,
        Optional(
            "verify_num_images",
            description="Verify number of images provided by user for clean is correct.",
            default=VERIFY_NUM_IMAGES,
        ): bool,
        Optional(
            "verify_running_image",
            description="Compare the image filename with the running image version on device. If a match is found, the copy stage will be skipped",
            default=VERIFY_RUNNING_IMAGE,
        ): bool,
        Optional(
            "expected_num_images",
            description="Number of images expected to be provided by user for clean.",
            default=EXPECTED_NUM_IMAGES,
        ): int,
        Optional(
            "vrf",
            description="Vrf used to copy. Defaults to an empty string.",
            default=VRF,
        ): str,
        Optional(
            "timeout", description="Copy operation timeout in seconds.", default=TIMEOUT
        ): int,
        Optional(
            "compact",
            description="Compact copy mode if supported by the device.",
            default=COMPACT,
        ): bool,
        Optional(
            "use_kstack",
            description="Use faster version of copy with limited options.",
            default=USE_KSTACK,
        ): bool,
        Optional(
            "protected_files",
            description="File patterns that should not be deleted.",
            default=PROTECTED_FILES,
        ): list,
        Optional(
            "overwrite",
            description="Overwrite the file if a file with the same name already exists.",
            default=OVERWRITE,
        ): bool,
        Optional(
            "skip_deletion",
            description="Do not delete any files even if there isn't any space on device.",
            default=SKIP_DELETION,
        ): bool,
        Optional(
            "copy_attempts",
            description="Number of times to attempt copying image files.",
            default=COPY_ATTEMPTS,
        ): int,
        Optional(
            "copy_attempts_sleep",
            description="Number of seconds to sleep between copy_attempts.",
            default=COPY_ATTEMPTS_SLEEP,
        ): int,
        Optional(
            "check_file_stability",
            description="Verifies that the file size is not changing. This ensures the image is not actively being copied.",
            default=CHECK_FILE_STABILITY,
        ): bool,
        Optional(
            "stability_check_tries",
            description="Max number of checks that can be done when checking file stability.",
            default=STABILITY_CHECK_TRIES,
        ): int,
        Optional(
            "stability_check_delay",
            description="Delay between tries when checking file stability in seconds.",
            default=STABILITY_CHECK_DELAY,
        ): int,
        Optional(
            "min_free_space_percent",
            description="Percentage of total disk space that must be free. If specified the percentage is not free then the stage will attempt to delete unprotected files to reach the minimum percentage.",
            default=MIN_FREE_SPACE_PERCENT,
        ): int,
        Optional(
            "interface",
            description="The interface to use for file transfers, may be needed for copying files on some IOSXE platforms, such as ASR1K when using a VRF.",
            default=INTERFACE,
        ): str,
        Optional(
            "unique_file_name",
            description="Appends a random six-digit number to the end of the image name.",
            default=UNIQUE_FILE_NAME,
        ): bool,
        Optional(
            "unique_number",
            description="Appends the provided number to the end of the image name. Requires unique_file_name is True to be applied.",
            default=UNIQUE_NUMBER,
        ): int,
        Optional(
            "rename_images",
            description="Rename the image to the provided name. If multiple files exist then an incrementing number is also appended.",
            default=RENAME_IMAGES,
        ): str,
        Optional(
            "prompt_recovery",
            description="Enable the prompt recovery when the  execution command timeout.",
            default=PROMPT_RECOVERY,
        ): bool,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = ["copy_to_device"]

    def copy_to_device(
        self,
        steps,
        device,
        origin,
        destination,
        protocol=PROTOCOL,
        connection_alias=CONNECTION_ALIAS,
        verify_num_images=VERIFY_NUM_IMAGES,
        expected_num_images=EXPECTED_NUM_IMAGES,
        vrf=VRF,
        timeout=TIMEOUT,
        compact=COMPACT,
        use_kstack=USE_KSTACK,
        protected_files=PROTECTED_FILES,
        overwrite=OVERWRITE,
        skip_deletion=SKIP_DELETION,
        copy_attempts=COPY_ATTEMPTS,
        copy_attempts_sleep=COPY_ATTEMPTS_SLEEP,
        check_file_stability=CHECK_FILE_STABILITY,
        stability_check_tries=STABILITY_CHECK_TRIES,
        stability_check_delay=STABILITY_CHECK_DELAY,
        min_free_space_percent=MIN_FREE_SPACE_PERCENT,
        interface=INTERFACE,
        unique_file_name=UNIQUE_FILE_NAME,
        unique_number=UNIQUE_NUMBER,
        rename_images=RENAME_IMAGES,
        prompt_recovery=PROMPT_RECOVERY,
        verify_running_image=VERIFY_RUNNING_IMAGE,
        **kwargs,
    ):
        log.info(
            "Section steps:\n1- Verify correct number of images provided"
            "\n2- Get filesize of image files"
            "\n3- Check if image files already exist on device"
            "\n4- (Optional) Verify stability of image files"
            "\n5- Verify free space on device else delete unprotected files"
            "\n6- Copy image files to device"
            "\n7- Verify copied image files are present on device"
        )

        if connection_alias:
            log.info(f"Using connection alias {connection_alias}")

        with device.temp_default_alias(connection_alias):

            # list of destination directories
            destinations = []

            # Establish FileUtils session for all FileUtils operations
            file_utils = FileUtils(testbed=device.testbed)

            # Get args
            server = origin.get("hostname")

            image_files = origin["files"]

            if server:
                # Check remote server info present in testbed YAML
                if not file_utils.get_server_block(server):
                    self.failed(
                        "Server '{}' was provided in the clean yaml file but "
                        "doesn't exist in the testbed file.\n".format(server)
                    )

                string_to_remove = file_utils.get_server_block(server).get("path", "")
                image_files = remove_string_from_image(
                    images=origin["files"], string=string_to_remove
                )

            # Set active node destination directory
            destination_act = destination["directory"]

            # Set standby node destination directory
            if "standby_directory" in destination:
                destination_stby = destination["standby_directory"]
                destinations = [destination_stby, destination_act]
            else:
                destination_stby = None
                destinations = [destination_act]

            if "stack_directory" in destination:
                destination_stack = destination["stack_directory"]
                for member_dir in destination_stack:
                    destinations.append(member_dir)

            # update the expected images to 2 if SMU image is given
            # else defaults to 1
            for image in image_files:
                if "smu" in image:
                    expected_num_images = len(image_files)
                    break

            # Check image files provided
            if verify_num_images:
                # Verify correct number of images provided
                with steps.start("Verify correct number of images provided") as step:
                    if not verify_num_images_provided(
                        image_list=image_files, expected_images=expected_num_images
                    ):
                        step.failed(
                            "Incorrect number of images provided. Please "
                            "provide {} expected image(s) under destination"
                            ".path in clean yaml file.\n".format(expected_num_images)
                        )
                    else:
                        step.passed("Correct number of images provided")

            # Loop over all image files provided by user
            for index, file in enumerate(image_files):
                # Init
                files_to_copy = {}
                unknown_size = False

                file_size = None

                # Check the running image
                if verify_running_image:
                    # Verify the image running in the device
                    with steps.start("Verify the image running in the device") as step:
                        try:
                            out = device.parse("show version")
                        except Exception as e:
                            step.failed("Failed to verify the running image")

                        # To get the system image
                        dest_file_path = out.get("version", {}).get("system_image", "")

                        # if the device is in bundle mode and user passed install_image stage this step will not be executed.

                        if "BUNDLE" in Dq(out).get_values(
                            "mode"
                        ) and "install_image" in device.clean.get("order", []):
                            step.skipped(
                                f"The device is in bundle mode and install_image stage is passed in clean file. Skipping the verify running image check."
                            )
                        elif "packages.conf" in dest_file_path and any(
                            "change_boot_variable" in order_name
                            for order_name in device.clean.get("order", [])
                        ):
                            step.passed(
                                f"The device is in install mode and change_boot_variable stage is passed in clean file. Continuing with the copy process."
                            )
                        else:
                            # Match the build_label if present, otherwise the xe_version
                            # If neither is found, fail to match the image
                            xe_version = out.get("version", {}).get("xe_version", "")
                            build_label = out.get("version", {}).get("build_label", "")
                            image_version = build_label or xe_version
                            image_match = re.search(image_version, file)
                            if image_match and image_match.group():
                                # update image mapping 'as-if' we had copied the file
                                for dest in destinations:
                                    dest_file_path = os.path.join(
                                        dest, os.path.basename(file)
                                    )
                                    image_mapping = self.history[
                                        "CopyToDevice"
                                    ].parameters.setdefault("image_mapping", {})
                                    image_mapping.update(
                                        {origin["files"][index]: dest_file_path}
                                    )

                                self.skipped(
                                    f"The image file provided is same as the current running image {image_version} on the device.\n\
                                             Setting the destination image to {dest_file_path}. Skipping the copy process."
                                )

                # try to get file size from file directly
                with steps.start(f"Get filesize of '{file}'") as step:
                    try:
                        file_size = os.stat(file).st_size
                    except Exception:
                        step.passx("Failed to get file size")

                if not file_size and server:
                    # Get filesize of image files on remote server
                    with steps.start(
                        "Get filesize of '{}' on remote server '{}'".format(
                            file, server
                        )
                    ) as step:
                        try:
                            file_size = device.api.get_file_size_from_server(
                                server=file_utils.get_hostname(server),
                                path=file,
                                protocol=protocol,
                                timeout=timeout,
                                fu_session=file_utils,
                            )
                        except FileNotFoundError:
                            step.failed(
                                "Can not find file {} on server {}. Terminating clean".format(
                                    file, server
                                )
                            )
                        except Exception as e:
                            log.warning(str(e))
                            # Something went wrong, set file_size to -1
                            file_size = -1
                            unknown_size = True
                            err_msg = (
                                "\nUnable to get filesize for file '{}' on "
                                "remote server {}".format(file, server)
                            )
                            if overwrite:
                                err_msg += " - will copy file to device"
                            step.passx(err_msg)
                        else:
                            step.passed(
                                "Verified filesize of file '{}' to be "
                                "{} bytes".format(file, file_size)
                            )
                else:
                    log.info(f"Local file has size {file_size}")

                for dest in destinations:

                    # Check if file with same name and size exists on device
                    dest_file_path = os.path.join(dest, os.path.basename(file))
                    image_mapping = self.history["CopyToDevice"].parameters.setdefault(
                        "image_mapping", {}
                    )
                    image_mapping.update({origin["files"][index]: dest_file_path})
                    with steps.start(
                        "Check if file '{}' exists on device {} {}".format(
                            dest_file_path, device.name, dest
                        )
                    ) as step:
                        # Execute 'dir' before copying image files
                        dir_before = device.execute("dir {}".format(dest))

                        # Check if file exists
                        try:
                            exist = device.api.verify_file_exists(
                                file=dest_file_path,
                                size=file_size,
                                dir_output=dir_before,
                            )
                        except Exception as e:
                            exist = False
                            log.warning(
                                "Unable to check if image '{}' exists on device {} {}."
                                "Error: {}".format(
                                    dest_file_path, device.name, dest, str(e)
                                )
                            )

                        if (
                            (not exist)
                            or (exist and overwrite)
                            or (
                                exist
                                and (unique_file_name or unique_number or rename_images)
                            )
                        ):
                            # Update list of files to copy
                            file_copy_info = {
                                file: {
                                    "size": file_size,
                                    "dest_path": dest_file_path,
                                    "exist": exist,
                                }
                            }
                            files_to_copy.update(file_copy_info)
                            # Print message to user
                            step.passed(
                                "Proceeding with copying image {} to device {}".format(
                                    dest_file_path, device.name
                                )
                            )
                        else:
                            step.passed(
                                "Image '{}' already exists on device {} {}, "
                                "skipping copy".format(file, device.name, dest)
                            )

                    # Check if any file copy is in progress
                    if check_file_stability:
                        for file in files_to_copy:
                            with steps.start(
                                "Verify stability of file '{}'".format(file)
                            ) as step:
                                # Check file stability
                                try:
                                    stable = (
                                        device.api.verify_file_size_stable_on_server(
                                            file=file,
                                            server=file_utils.get_hostname(server),
                                            protocol=protocol,
                                            fu_session=file_utils,
                                            delay=stability_check_delay,
                                            max_tries=stability_check_tries,
                                        )
                                    )

                                    if not stable:
                                        step.failed(
                                            "The size of file '{}' on server is not "
                                            "stable\n".format(file),
                                        )
                                    else:
                                        step.passed(
                                            "Size of file '{}' is stable".format(file)
                                        )
                                except NotImplementedError:
                                    # cannot check using tftp
                                    step.passx(
                                        "Unable to check file stability over {protocol}".format(
                                            protocol=protocol
                                        )
                                    )
                                except Exception as e:
                                    log.error(str(e))
                                    step.failed(
                                        "Error while verifying file stability on "
                                        "server\n"
                                    )

                    # Verify available space on the device is sufficient for image copy, delete
                    # unprotected files if needed, copy file to the device
                    # unless overwrite: False
                    if files_to_copy:
                        with steps.start(
                            "Verify sufficient free space on device '{}' '{}' or delete"
                            " unprotected files".format(device.name, dest)
                        ) as step:

                            if unknown_size:
                                total_size = -1
                                log.warning(
                                    "Amount of space required cannot be confirmed, "
                                    "copying the files on the device '{}' '{}' may fail".format(
                                        device.name, dest
                                    )
                                )

                            if not protected_files:
                                protected_files = []

                            # Try to free up disk space if skip_deletion is not set to True
                            if not skip_deletion:
                                # TODO: add golden images, config to protected files once we have golden section
                                golden_config = find_clean_variable(
                                    self, "golden_config"
                                )
                                golden_image = find_clean_variable(self, "golden_image")

                                if golden_config:
                                    protected_files.extend(golden_config)
                                if golden_image:
                                    protected_files.extend(golden_image)

                                # Only calculate size of file being copied
                                total_size = sum(
                                    0 if file_data["exist"] else file_data["size"]
                                    for file_data in files_to_copy.values()
                                )

                                try:
                                    free_space = device.api.free_up_disk_space(
                                        destination=dest,
                                        required_size=total_size,
                                        skip_deletion=skip_deletion,
                                        protected_files=protected_files,
                                        min_free_space_percent=min_free_space_percent,
                                        dir_output=dir_before,
                                        allow_deletion_failure=True,
                                    )
                                    if not free_space:
                                        step.failed(
                                            "Unable to create enough space for "
                                            "image on device {} {}".format(
                                                device.name, dest
                                            )
                                        )
                                    else:
                                        step.passed(
                                            "Device {} {} has sufficient space to "
                                            "copy images".format(device.name, dest)
                                        )
                                except Exception as e:
                                    log.error(str(e))
                                    step.failed(
                                        "Error while creating free space for "
                                        "image on device {} {}".format(
                                            device.name, dest
                                        )
                                    )

                    # Copy the file to the devices
                    for file, file_data in files_to_copy.items():
                        with steps.start(
                            "Copying image file {} to device {} {}".format(
                                file, device.name, dest
                            )
                        ) as step:

                            # Copy file unless overwrite is False
                            if (
                                not overwrite
                                and file_data["exist"]
                                and not (
                                    unique_file_name or unique_number or rename_images
                                )
                            ):
                                step.skipped(
                                    "File with the same name size exists on "
                                    "the device {} {}, skipped copying".format(
                                        device.name, dest
                                    )
                                )

                            for i in range(1, copy_attempts + 1):
                                if unique_file_name or unique_number or rename_images:

                                    log.info("renaming files for copying")
                                    if rename_images:
                                        rename_images = rename_images + "_" + str(index)

                                    try:
                                        new_name = device.api.modify_filename(
                                            file=os.path.basename(file),
                                            directory=destination_act,
                                            server=server,
                                            protocol=protocol,
                                            unique_file_name=unique_file_name,
                                            unique_number=unique_number,
                                            new_name=rename_images,
                                        )
                                    except Exception as e:
                                        step.failed(
                                            "Can not change file name. Terminating clean:\n{e}".format(
                                                e=e
                                            )
                                        )

                                    log.info(
                                        f"Renamed {os.path.basename(file)} to {new_name}"
                                    )

                                    renamed_local_path = os.path.join(dest, new_name)

                                    renamed_file_data = {
                                        x: y for x, y in file_data.items()
                                    }
                                    renamed_file_data["dest_path"] = renamed_local_path

                                    self.history["CopyToDevice"].parameters[
                                        "image_mapping"
                                    ][file] = renamed_local_path

                                    try:
                                        res = device.api.copy_to_device(
                                            protocol=protocol,
                                            server=(
                                                file_utils.get_hostname(server)
                                                if server
                                                else None
                                            ),
                                            remote_path=file,
                                            local_path=renamed_local_path,
                                            vrf=vrf,
                                            timeout=timeout,
                                            compact=compact,
                                            use_kstack=use_kstack,
                                            interface=interface,
                                            overwrite=overwrite,
                                            prompt_recovery=prompt_recovery,
                                            **kwargs,
                                        )
                                        if not res:
                                            raise Exception(
                                                "Failed to copy file to device"
                                            )
                                    except Exception as e:
                                        # Retry attempt if user specified
                                        if i < copy_attempts:
                                            log.warning(
                                                "Attempt #{}: Unable to copy {} to '{} {}' due to:\n{}".format(
                                                    i, file, device.name, dest, e
                                                )
                                            )
                                            log.info(
                                                "Sleeping for {} seconds before retrying".format(
                                                    copy_attempts_sleep
                                                )
                                            )
                                            time.sleep(copy_attempts_sleep)
                                            continue
                                        else:
                                            log.error(str(e))
                                            step.failed(
                                                "Failed to copy image '{}' to '{}' on device"
                                                " '{}'\n".format(
                                                    file, dest, device.name
                                                ),
                                            )
                                else:
                                    try:
                                        res = device.api.copy_to_device(
                                            protocol=protocol,
                                            server=(
                                                file_utils.get_hostname(server)
                                                if server
                                                else None
                                            ),
                                            remote_path=file,
                                            local_path=file_data["dest_path"],
                                            vrf=vrf,
                                            timeout=timeout,
                                            compact=compact,
                                            use_kstack=use_kstack,
                                            interface=interface,
                                            overwrite=overwrite,
                                            prompt_recovery=prompt_recovery,
                                            **kwargs,
                                        )
                                        if not res:
                                            raise Exception(
                                                "Failed to copy file to device"
                                            )
                                    except Exception as e:
                                        # Retry attempt if user specified
                                        if i < copy_attempts:
                                            log.warning(
                                                "Attempt #{}: Unable to copy {} to '{} {}' due to:\n{}".format(
                                                    i, file, device.name, dest, e
                                                )
                                            )
                                            log.info(
                                                "Sleeping for {} seconds before retrying".format(
                                                    copy_attempts_sleep
                                                )
                                            )
                                            time.sleep(copy_attempts_sleep)
                                            continue
                                        else:
                                            log.error(str(e))
                                            step.failed(
                                                "Failed to copy image '{}' to '{}' on device"
                                                " '{}'\n".format(
                                                    file, dest, device.name
                                                ),
                                            )

                                log.info(
                                    "File {} has been copied to {} on device {}"
                                    " successfully".format(file, dest, device.name)
                                )
                                success_copy_ha = True
                                break

                            # Save the file copied path and size info for future use
                            history = self.history[
                                "CopyToDevice"
                            ].parameters.setdefault("files_copied", {})

                            if unique_file_name or unique_number or rename_images:
                                history.update({file: renamed_file_data})
                            else:
                                history.update({file: file_data})

                    with steps.start("Verify images successfully copied") as step:
                        # If nothing copied don't need to verify, skip
                        if (
                            "files_copied"
                            not in self.history["CopyToDevice"].parameters
                        ):
                            step.skipped(
                                "Image files were not copied for {} {} in previous steps, "
                                "skipping verification steps".format(device.name, dest)
                            )

                        # Execute 'dir' after copying image files
                        dir_after = device.execute("dir {}".format(dest))

                        for name, image_data in (
                            self.history["CopyToDevice"]
                            .parameters["files_copied"]
                            .items()
                        ):
                            with step.start(
                                "Verify image '{}' copied to {} on device {}".format(
                                    image_data["dest_path"], dest, device.name
                                )
                            ) as substep:
                                # if size is -1 it means it failed to get the size
                                if not device.api.verify_file_exists(
                                    file=image_data["dest_path"],
                                    size=image_data["size"],
                                    dir_output=dir_after,
                                ):
                                    substep.failed(
                                        "Either the file failed to copy OR the local file size is different "
                                        "than the origin file size on the device {}.".format(
                                            device.name
                                        )
                                    )
                                else:
                                    file_name = os.path.basename(file)
                                    if file_name not in protected_files:
                                        protected_files.append(file_name)
                                    log.info(
                                        "{file_name} added to protected list".format(
                                            file_name=file_name
                                        )
                                    )
                                    if image_data["size"] != -1:
                                        substep.passed(
                                            "File was successfully copied to device {}. "
                                            "Local file size is the same as the origin file size.".format(
                                                device.name
                                            )
                                        )
                                    else:
                                        substep.skipped(
                                            "File has been copied to device {}.Cannot verify integrity as "
                                            "the original file size is unknown.".format(
                                                device.name
                                            )
                                        )


class ConfigureReplace(BaseStage):
    """This stage does a configure replace on the device."""

    # =================
    # Argument Defaults
    # =================
    CONFIG_REPLACE_OPTIONS = ""
    TIMEOUT = 60
    KNOWN_WARNINGS = None

    # ============
    # Stage Schema
    # ============
    schema = {
        "path": str,
        "file": str,
        Optional("config_replace_options"): str,
        Optional("known_warnings"): list,
        Optional("timeout"): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        "configure_replace",
    ]

    def configure_replace(
        self,
        steps,
        device,
        path,
        file,
        config_replace_options=CONFIG_REPLACE_OPTIONS,
        known_warnings=KNOWN_WARNINGS,
        timeout=TIMEOUT,
    ):
        """This step does a configure replace on the device."""

        if known_warnings is None:
            known_warnings = []

        with steps.start(f"Configure replace on '{device.name}'") as step:
            try:
                output = device.api.configure_replace(
                    path=path,
                    file=file,
                    config_replace_options=config_replace_options,
                    timeout=timeout,
                )
                pattern = (
                    r"\*+\n*!List of Rollback Commands:(?P<rejected_cmds>.*?)end\n\*+"
                )
                if re.search(pattern, output, re.DOTALL):
                    rejected_cmds = (
                        re.search(pattern, output, re.DOTALL)
                        .group("rejected_cmds")
                        .strip()
                        .split("\n")
                    )
                else:
                    rejected_cmds = []
                if rejected_cmds:
                    if set(rejected_cmds).issubset(set(known_warnings)):
                        step.passx("Configure replace warnings are expected")
                    else:
                        log.warning(f"Rejected commands: {rejected_cmds}")
                        log.warning(
                            f"Unexpected warnings: {set(rejected_cmds) - set(known_warnings)}"
                        )
                        step.failed("Configure replace warnings are not expected")
                else:
                    step.passed("Configure replace passed without rejection")

            except Exception as e:
                step.failed("Configure replace failed", from_exception=e)


class Connect(BaseStage):
    """This stage connects to the device that is being cleaned.
    Stage Schema
    ------------
    connect:
        via (str, optional): Which connection to use from the testbed file. Uses the
            default connection if not specified.
        alias (str, optional): Which connection alias to use from the testbed file.
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
    ALIAS = None
    TIMEOUT = 200
    RETRY_TIMEOUT = 0
    RETRY_INTERVAL = 0

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional(
            "via",
            description="Which connection to use from the testbed file. Uses the default connection if not specified.",
        ): str,
        Optional("alias", description="Which connection alias to use."): str,
        Optional(
            "timeout",
            description=f"The timeout for the connection to complete in seconds. Defaults to {TIMEOUT}.",
            default=TIMEOUT,
        ): Or(str, int),
        Optional(
            "retry_timeout",
            description=f"Overall timeout for retry mechanism in seconds. Defaults to {RETRY_TIMEOUT} which means no retry.",
            default=RETRY_TIMEOUT,
        ): Or(str, int, float),
        Optional(
            "retry_interval",
            description=f"Interval for retry mechanism in seconds. Defaults to {RETRY_INTERVAL} which means no retry.",
            default=RETRY_INTERVAL,
        ): Or(str, int, float),
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = ["connect"]

    def connect(
        self,
        steps,
        device,
        via=VIA,
        alias=ALIAS,
        timeout=TIMEOUT,
        retry_timeout=RETRY_TIMEOUT,
        retry_interval=RETRY_INTERVAL,
    ):

        with steps.start("Connecting to the device") as step:

            log.info("Checking connection to device: %s" % device.name)
            # Create a timeout that will loop
            retry_timeout = Timeout(float(retry_timeout), float(retry_interval))
            retry_timeout.one_more_time = True
            # Without this we see 'Performing the last attempt' even if retry
            # is not being used.
            retry_timeout.disable_log = True

            while retry_timeout.iterate():
                retry_timeout.disable_log = False

                # mit=True is used to make sure we do not initialize the connection
                # and we can check if the device is in rommon.
                device.instantiate(
                    connection_timeout=timeout,
                    learn_hostname=True,
                    prompt_recovery=True,
                    via=via,
                    alias=alias,
                    mit=True,
                )

                try:
                    if alias:
                        getattr(device, alias).connect()
                    else:
                        device.connect()
                except UniconBackendDecodeError:
                    log.info("Console speed mismatch. Trying to recover")
                    device.destroy_all()
                    device.api.configure_management_console()
                    step.passed("Successfully connected".format(device.name))
                except UniconAuthenticationError as e:
                    log.info(f"Could not connect to device because of {e}")
                    log.info("Starting device password recovery.")
                    try:
                        device.api.password_recovery(timeout=timeout)
                    except Exception as e:
                        log.error("Password recovery failed", exc_info=True)
                    else:
                        step.passed("Successfully connected".format(device.name))
                        # Don't loop
                except Exception:
                    log.error("Connection to the device failed", exc_info=True)
                    device.destroy_all()
                    # Loop
                else:
                    step.passed("Successfully connected".format(device.name))
                    # Don't loop

                retry_timeout.sleep()

            step.failed("Could not connect. Scroll up for tracebacks.")

        with steps.start(
            f"Checking the current state of the device: {device.name}"
        ) as step:

            log.info(f"Checking the current state of the device: {device.name}")

            state = ""
            try:
                # To check the state for HA devices
                if device.is_ha and hasattr(device, "subconnections"):
                    # To allocate handles for HA devices
                    if isinstance(device.subconnections, list):
                        states = list(
                            set(
                                [
                                    con.state_machine.current_state
                                    for con in device.subconnections
                                ]
                            )
                        )
                        if "rommon" in states:
                            # To get the subconnections and designate handles
                            state = "rommon"
                            subcons = list(device._subconnections.items())
                            if len(subcons) > 1:
                                subcon1_alias, subcon1 = subcons[0]
                                subcon2_alias, subcon2 = subcons[1]
                                device._set_active_alias(subcon1_alias)
                                device._set_standby_alias(subcon2_alias)
                                device.default._handles_designated = True
                            else:
                                log.warning(
                                    f"There is only one subconnection in the HA device"
                                )
                else:
                    # To check the state for single rp device
                    state = device.state_machine.current_state
            except Exception as e:
                log.warning(f"There is no connection in device.subconnections: {e}")

        if state == "rommon":

            with steps.start("Setting the rommon variables") as step:

                log.info("Setting the rommon variables for TFTP boot")

                try:
                    if device.is_ha and hasattr(device, "subconnections"):
                        device.api.configure_rommon_tftp_ha()
                    else:
                        device.api.configure_rommon_tftp()
                except Exception as e:
                    step.passx(f"Failed to set rommon variables. {e}")
                else:
                    log.info("Successfully set the rommon variables")

            with steps.start("Configuring the manual boot") as step:

                log.info("Configuring the manual boot")

                try:

                    if device.is_ha and hasattr(device, "subconnections"):
                        states_list = []
                        # Switch to enable mode if one of the rps are disable mode.
                        for con in device.subconnections:
                            if con.state_machine.current_state == "disable":
                                con.state_machine.go_to("enable", con.spawn)
                            states_list.append(con.state_machine.current_state)

                        # if one rp in enable mode and another rp in rommon set boot manual on enable rp.
                        if "enable" in states_list and "rommon" in states_list:
                            device.subconnections[
                                states_list.index("enable")
                            ].configure("boot manual")
                        else:
                            log.info(
                                "Both rps are in rommon mode. Skipping the manual boot configuration"
                            )
                except Exception as e:
                    step.passx(f"Failed to configure manual boot. {e}")
                else:
                    log.info("Successfully configured manual boot")

            with steps.start("Booting the device from rommon") as step:

                log.info("Booting the device from rommon")

                try:
                    # Gets the recovery details from clean yaml
                    device.api.device_rommon_boot()
                except Exception as e:
                    step.passx(f"Failed to boot device from rommon. {e}")
                else:
                    log.info("Successfully booted the device from rommon.")

        # set mit to False to initialize the connection
        device.default.mit = False
        device.default.learn_hostname = False
        with steps.start("Initialize the device connection") as step:

            try:
                device.connection_provider.init_connection()
            except Exception as e:
                step.failed(f"Failed to initialize the connection. {e}")
            else:
                step.passed("Successfully connected to the device")


class ResetConfiguration(BaseStage):
    """Reset device configuration by using config replace operation with a minimal configuration.

        This clean stage generates a minimal configuration from the running config and stores
        it in the base_config.txt file on bootflash. Then uses configure replace command to
        override the running configuration.

        If the file `base_config.txt` exists on flash, the contents will be overwritten.

    Stage Schema
    ------------
    reset_configuration:
        timeout (int, optional): The timeout for device configuration to complete in seconds.
            Defaults to 120.

    Example:

        reset_configuration:

        order:
            - connect
            - reset_configuration
    """

    # =================
    # Argument Defaults
    # =================
    TIMEOUT = 120

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional(
            "timeout",
            description="Timeout for device configuration. Default: 120 seconds.",
        ): int,
    }

    exec_order = ["create_config_file", "reset_configuration", "show_running_config"]

    def _recurse_config_dict_to_text(self, config_dict, level=0, indent=1):
        output = ""
        for key, value in config_dict.items():
            if not value:
                # special handling for 'quit' statements in crypto config
                if key == "quit":
                    output = "\n  \tquit"
                else:
                    output += "\n" + " " * level * indent + key
            else:
                output += (
                    "\n"
                    + " " * level * indent
                    + key
                    + self._recurse_config_dict_to_text(value, level + 1)
                )
        return output

    def _generate_config_text(self, config_dict):
        return self._recurse_config_dict_to_text(config_dict, level=0)

    def _filter_config_dict(self, config_dict, new_config_dict, KEEP):
        for k in config_dict:
            for key in KEEP:
                if re.search(key, k) and not KEEP[key]:
                    # keep everything in the section
                    break
                elif re.search(key, k) and KEEP[key]:
                    # filter in section
                    self._filter_config_dict(
                        config_dict[k], new_config_dict[k], KEEP[key]
                    )
                    break
            else:
                new_config_dict.pop(k, None)

    def _generate_default_config(self, device, config_dict):

        DEFAULTS = dedent(
            """\
            !
            ! Last configuration change
            !
            hostname {device.name}
            no logging console
            service timestamps debug datetime msec
            service timestamps log datetime msec
            """.format(
                device=device
            )
        )

        KEEP = {
            "^interface GigabitEthernet0(/0)?$": {
                "^vrf forwarding": {},
                "^negotiation auto": {},
            },
            "^vrf definition Mgmt-(intf|vrf)": {},
            "^switch 1 provision": {},
            "^stackwise-virtual": {},
            "^platform hardware throughput level": {},
            "^ignition": {},
            "^canbus baudrate": {},
            "^crypto pki trustpoint": {},
            "^crypto pki certificate chain": {},
            "^license udi": {},
            "^license boot level": {},
            "^class-map match-any system": {},
            "^policy-map system": {},
            "^interface Vlan1$": {"^no ip address": {}, "^shutdown": {}},
            "^transceiver type all": {},
            "^redundancy": {},
            "^control-plane": {},
            "^spanning-tree extend system-id": {},
            "^spanning-tree mode rapid-pvst": {},
            "^diagnostic bootup level minimal": {},
            "^memory free low-watermark processor": {},
            "^boot system": {},
            "^aaa new-model": {},
            "^class-map match-any non-client-nrt-class": {},
            "^aaa session-id common": {},
            "^username": {},
            "^login on-success log": {},
            "^interface Async": {},
            "^ip forward-protocol nd": {},
            "^ip ssh bulk-mode": {},
            "^line con": {"^speed": {}},
            "^line vty": {"^transport input": {}},
            "^ip http server": {},
            "^ip http secure-server": {},
        }

        new_config_dict = copy.deepcopy(config_dict)

        self._filter_config_dict(config_dict, new_config_dict, KEEP)

        config_text = self._generate_config_text(new_config_dict)

        config_text = DEFAULTS + config_text + "\nend"

        return config_text

    def create_config_file(self, steps, device, timeout=TIMEOUT):
        with steps.start("Getting current config") as step:
            # Use lstrip to avoid stripping trailing whitespace from config lines,
            # this is required for config replace to work with pki certs.
            config_dict = device.api.get_running_config_dict(lstrip=True)
            log.debug(json.dumps(config_dict, indent=4))

        with steps.start("Creating minimal configuration file") as step:
            config_text = self._generate_default_config(device, config_dict)
            config_lines = config_text.splitlines()

            # Write the configuration into a file on the device using TCL shell.
            device.tclsh()
            lines = (
                [
                    'puts [open "base_config.txt" w+] {',
                ]
                + config_lines
                + ["}"]
            )
            for line in lines:
                device.sendline(line)
                # Instead of waiting for each line to be processed, just keep
                # reading the buffer. This is a lot faster and testing has shown
                # this to work fine. This could be changed using a bulk approach
                # like unicon configure() service if needed.
                device.spawn.read_update_buffer()
            # Wait until all config data has been processed by the device
            device.expect(
                device.state_machine.get_state(
                    device.state_machine.current_state
                ).pattern,
                timeout,
            )

            device.enable()

    def reset_configuration(self, steps, device, timeout=TIMEOUT):
        dialog = Dialog(
            [
                [
                    r".*?Enter Y if you are sure you want to proceed. \? \[no]:\s*$",
                    "sendline(y)",
                    None,
                    True,
                    False,
                ],
                [
                    r".*?Overwriting with a file sized 50% or less than running config\'s. Proceed\? \[no]:\s*$",
                    "sendline(yes)",
                    None,
                    True,
                    False,
                ],
            ]
        )

        # Configure the hostname explicitly
        device.configure(f"hostname {device.name}")

        with steps.start("Resetting configuration using config replace") as step:
            output = device.execute(
                "config replace bootflash:base_config.txt",
                reply=dialog,
                timeout=timeout,
            )
            if "Rollback aborted" in output:
                step.passx("Rollback aborted")

    def show_running_config(self, steps, device):
        with steps.start("Capturing running config") as step:
            device.execute("show running-config")


class SetControllerMode(BaseStage):
    """Set controller mode

    Stage Schema
    ------------
    set_controller_mode:

        mode (str, optional): `enable` or `disable`. Defaults to `enable`

        reload_timeout (int, optional): maximum time to wait for reload.
            Defaults to 600 secs

        delete_inactive_versions (bool, optional): delete non active version after
            changing image. Defaults to True

    Example
    -------
    set_controller_mode:
        mode: enable
        reload_timeout: 600
        delete_inactive_versions: True
    """

    # =================
    # Argument Defaults
    # =================
    MODE = "enable"
    RELOAD_TIMEOUT = 600
    DELETE_INACTIVE_VERSIONS = True

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional("mode"): str,
        Optional("reload_timeout"): int,
        Optional("delete_inactive_versions"): bool,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        "set_controller_mode",
        "confirm_and_set_default",
        "delete_inactive_versions",
    ]

    def set_controller_mode(
        self, steps, device, mode=MODE, reload_timeout=RELOAD_TIMEOUT
    ):

        # Check if we're already in the desired mode
        version_data = device.parse("show version")

        # For those versions of IOSXE where version is a str
        try:
            router_operating_mode = version_data.get("version", {}).get(
                "router_operating_mode"
            )
        except AttributeError:
            router_operating_mode = None

        if router_operating_mode == "Autonomous" and mode == "disable":
            self.skipped("Router already in Autonomous mode")
        elif router_operating_mode == "Controller-Managed" and mode == "enable":
            self.skipped("Router already in Controller-Managed mode")

        with steps.start("setting controller mode") as step:

            if device.connected:
                device.destroy_all()

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
            generic_statments = GenericStatements()

            controller_mode_dialog = Dialog(
                [
                    Statement(
                        pattern=r"Continue\? \[confirm\]",
                        action="sendline()",
                        loop_continue=True,
                        continue_timer=False,
                    ),
                    Statement(
                        pattern=r"Do you want to abort\? \(yes/\[no\]\):",
                        action="sendline(no)",
                        loop_continue=True,
                        continue_timer=False,
                    ),
                    Statement(
                        pattern=r"Username:",
                        action="sendline(admin)",
                        loop_continue=True,
                        continue_timer=False,
                    ),
                    Statement(
                        pattern=r"Password:",
                        action="sendline(admin)",
                        loop_continue=True,
                        continue_timer=False,
                    ),
                    Statement(
                        pattern=r"Enter new password:",
                        action=f"sendline({password})",
                        loop_continue=True,
                        continue_timer=False,
                    ),
                    Statement(
                        pattern=r"Confirm password:",
                        action=f"sendline({password})",
                        loop_continue=True,
                        continue_timer=False,
                    ),
                    Statement(
                        pattern=r"Press RETURN to get started.*",
                        action=f"sendline()",
                        loop_continue=True,
                        continue_timer=False,
                    ),
                    Statement(
                        pattern=r"(.*?)Would you like to enter the initial configuration dialog\? \[yes/no\]:\s*",
                        action=f"sendline(no)",
                        loop_continue=True,
                        continue_timer=False,
                    ),
                    Statement(
                        pattern=r"(.*?)Would you like to enter the initial configuration dialog\? \[yes/no\]:\s*",
                        action=f"sendline(no)",
                        loop_continue=True,
                        continue_timer=False,
                    ),
                    generic_statments.syslog_msg_stmt,
                    generic_statments.enable_secret_stmt,
                    generic_statments.enter_your_selection_stmt,
                ]
            )

            try:
                device.execute(
                    f"controller-mode {mode}",
                    timeout=reload_timeout,
                    service_dialog=controller_mode_dialog,
                    allow_state_change=True,
                )
            except SubCommandFailure:
                self.skipped(
                    "Unable to configure controller-mode. Is it a "
                    "feature of this device?"
                )

    def confirm_and_set_default(self, steps, device, mode=MODE):

        with steps.start("upgrade-confirm and set-default") as step:
            if device.connected:
                device.destroy_all()
            if mode == "disable":
                self.output = device.connect(
                    learn_tokens=True, overwrite_testbed_tokens=True
                )
            else:
                self.output = device.connect()

                parsed_output = device.parse("show sdwan software")
                active_version = parsed_output.q.contains_key_value(
                    "active", "true"
                ).get_values("version", 0)
                self.non_active_version = parsed_output.q.contains_key_value(
                    "active", "false"
                ).get_values("version")

                if active_version:
                    commands = [
                        "request platform software sdwan software upgrade-confirm",
                        f"request platform software sdwan software set-default {active_version}",
                        "show sdwan software",
                    ]
                    device.execute(commands)
                else:
                    step.failed("Active version was not confirmed.")

        with steps.start("Verify controller mode") as step:
            if "Controller-Managed" in self.output and mode == "enable":
                step.passed("Device booted up with controller-mode successfully.")
            elif "Autonomous" in self.output and mode == "disable":
                step.passed("Device booted up with autonomous-mode successfully.")
            elif "Controller-Managed" in self.output and mode == "disable":
                step.failed("Device couldn't boot up with autonomous-mode")
            elif "Autonomous" in self.output and mode == "enable":
                step.failed("Device couldn't boot up with controller-mode")
            else:
                step.failed(
                    f"Something went wrong configuring `controller-mode {mode}`"
                )

    def delete_inactive_versions(
        self,
        steps,
        device,
        delete_inactive_versions=DELETE_INACTIVE_VERSIONS,
        mode=MODE,
    ):

        with steps.start("deleting non active version") as step:

            if mode == "disable":
                step.skipped(
                    "Disabling the controller mode skipping the step as not needed. "
                )

            else:
                if delete_inactive_versions and self.non_active_version:
                    for version in self.non_active_version:
                        device.execute(
                            f"request platform software sdwan software remove {version}"
                        )
                    device.execute("show sdwan software")
                    log.info(
                        f"Non active versions {self.non_active_version} are deleted."
                    )
