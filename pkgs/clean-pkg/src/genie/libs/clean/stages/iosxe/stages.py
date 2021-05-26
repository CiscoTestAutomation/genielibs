'''
IOSXE specific clean stages
'''

# Python
import logging

# pyATS
from pyats import aetest
from pyats.async_ import pcall

# Genie
from genie.abstract import Lookup
from genie.libs import clean
from genie.libs.clean.utils import clean_schema
from genie.libs.clean.recovery.recovery import _disconnect_reconnect
from genie.metaparser.util.schemaengine import Optional
from genie.utils.timeout import Timeout

from genie.libs.sdk.libs.abstracted_libs.iosxe.subsection import get_default_dir

# Unicon
from unicon.eal.dialogs import Statement, Dialog

# Logger
log = logging.getLogger(__name__)


@clean_schema({
    Optional('images'): list,
    Optional('timeout'): int,
    Optional('max_time'): int,
    Optional('check_interval'): int,
    Optional('config_register'): str,
    Optional('write_memory'): bool,
})
@aetest.test
def change_boot_variable(section, steps, device, images, timeout=300,
    max_time=300, check_interval=30, config_register='0x2102',
    write_memory=False):
    """ This stage configures the boot variables to the provided image in
    preparation for the next device reload.

    Stage Schema
    ------------
    change_boot_variable:
        images (list): Images to copy

        timeout (int, optional): Execute timeout in seconds. Defaults to 300.

        max_time (int, optional): Maximum time to wait while saving
            running-config to startup-config in seconds. Defaults to 300.

        check_interval (int, optional): Time interval while checking save
            running config to startup-config completed in seconds. Defaults to 30.

        write_memory (bool, optional): Execute 'write memory' after
            setting BOOT var. Defaults to False.

        config_register (str, optional): Value to set config-register for
            reload. Defaults to 0x2102.

    Example
    -------
    change_boot_variable:
        images:
            - harddisk:/Genie-12351822-iedge-asr-uut
        timeout: 150
        max_time: 300
        check_interval: 20

    """

    log.info("Section steps:\n1- Delete any previously configured boot variables"
             "\n2- (Optional) Write to memory"
             "\n3- Set boot variables to images provided"
             "\n4- Set config-register to boot new image"
             "\n5- Write to memory or save running-config to startup-configuration"
             "\n6- Verify next reload boot variables are set correctly"
             "\n7- Verify config-register to boot new image is set correctly")


    # Delete any previously configured boot variables
    with steps.start("Delete any previously configured boot variables on {}".\
                     format(device.name)) as step:

        # Get list of existing boot images if any
        try:
            curr_boot_images = device.api.get_boot_variables(boot_var='next')
        except Exception as e:
            step.failed("Unable to check existing boot images on {}:\n{}".\
                        format(device.name, str(e)))

        if not curr_boot_images:
            step.passed("Device {} does not have any previously configured "
                        "boot variables".format(device.name))
        else:
            try:
                device.api.\
                    execute_delete_boot_variable(boot_images=curr_boot_images,
                                                 timeout=timeout)
            except Exception as e:
                step.failed("Failed to delete previously configured boot "
                            "variable on {}\n{}".format(device.name, str(e)))
            else:
                step.passed("Succesfully deleted previously configured boot "
                            "variables on {}".format(device.name))

    # Write to memory
    if write_memory:
        with steps.start("Execute 'write memory' on {}".format(device.name)) \
                as step:
            try:
                device.api.execute_write_memory(timeout=timeout)
            except Exception as e:
                log.error(str(e))
                step.failed("Failed to execute 'write memory' after setting "
                               "BOOT variables on device {}".format(device.name),
                               )
            else:
                step.passed("Succesfully executed 'write memory'")


    # Setting boot variable to image specified
    with steps.start("Set boot variable to images provided on {}".\
                     format(device.name)) as step:
        try:
            device.api.execute_set_boot_variable(boot_images=images,
                                                 timeout=timeout)
        except Exception as e:
            log.error(str(e))
            step.failed("Failed to set boot variables to images specified "
                           "on device {}\n".format(device.name), )
        else:
            step.passed("Succesfully set boot variables to image provided: {}".\
                        format(images))


    # Set config register as needed
    with steps.start("Set config register to boot new image on {}".\
                     format(device.name)) as step:
        try:
            device.api.\
                execute_set_config_register(config_register=config_register,
                                            timeout=timeout)
        except Exception as e:
            log.error(str(e))
            step.failed("Failed to set config-register correctly on device "
                           "{}".format(device.name), )
        else:
            step.passed("Succesfully set config register to {}".\
                        format(config_register))


    # Save configuration changes before reloading device
    if write_memory:
        with steps.start("Execute 'write memory' on {}".format(device.name)) \
                as step:
            try:
                device.api.execute_write_memory(timeout=timeout)
            except Exception as e:
                log.error(str(e))
                step.failed("Failed to execute 'write memory' after setting "
                               "BOOT variables on device {}".format(device.name),
                               )
            else:
                step.passed("Succesfully executed 'write memory'")

    else:
        with steps.start("Save running-configuration to startup-configuration "
                         "on {}".format(device.name)) as step:
            try:
                device.api.\
                    execute_copy_run_to_start(max_time=max_time,
                                              check_interval=check_interval)
            except Exception as e:
                log.error(str(e))
                step.failed("Failed to copy running-config to "
                               "startup-config on device {}".\
                               format(device.name), )
            else:
                step.passed("Successully saved running-config to startup-config"
                            " on {}".format(device.name))


    # Execute 'show bootvar' for verifying 'BOOT' and 'config register'
    log.info("Execute 'show bootvar' to verify boot variables and config-"
             "register'")
    show_bootvar_output = device.execute('show bootvar')


    # Verify next reload boot variables are correctly set
    with steps.start("Verify next reload boot variables are correctly set "
                     "on {}".format(device.name)) as step:
        if not device.api.verify_boot_variable(boot_images=images,
                                               output=show_bootvar_output):
            step.failed("Boot variables are not correctly set to {} prior "
                           "to reloading device {}".format(images, device.name),
                           )
        else:
            step.passed("Verified boot variables are correctly set on {}".\
                        format(device.name))


    # Verify config-register is correct set for next reload
    with steps.start("Verify config-register is correct set for next reload "
                     "on {}".format(device.name)) as step:
        if not device.api.\
                    verify_config_register(config_register=config_register,
                                           output=show_bootvar_output,
                                           next_reload=True):
            step.failed("Config-register not correctly set for next reload "
                           "on device {}".format(device.name), )
        else:
            section.passed("Verified config-register is correctly set on {}".\
                           format(device.name))

@clean_schema({
    'image': list,
    'ip_address': list,
    'subnet_mask': str,
    'gateway': str,
    'tftp_server': str,
    'recovery_password': str,
    Optional('save_system_config'): bool,
    Optional('timeout'): int,
    Optional('config_reg_timeout'): int,
})
@aetest.test
def tftp_boot(section, steps, device, ip_address, subnet_mask, gateway,
              tftp_server, image, recovery_password=None, save_system_config=True, timeout=600,
              config_reg_timeout=30):
    """ This stage boots a new image onto your device using the tftp booting
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

        recovery_password (str, optional): Enable password for device
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
        save_system_config: False
        timeout: 600
        config_reg_timeout: 10

    There is more than one ip address, one for each supervisor.

    """

    log.info("Section steps:"
             "\n1- Set config-register to 0x0"
             "\n2- Bring device down to rommon> prompt prior to TFTP boot"
             "\n3- Begin TFTP boot"
             "\n4- Reconnect to device after TFTP boot"
             "\n5- Reset config-register to 0x2101"
             "\n6- Execute 'write memory'")

    # Set config-register to 0x0
    with steps.start("Set config-register to 0x0 on {}".format(device.name)) as step:
        try:
            device.api.execute_set_config_register(config_register='0x0',
                                                   timeout=config_reg_timeout)
        except Exception as e:
            step.failed("Unable to set config-register to 0x0 prior to TFTP"
                           " boot on {}".format(device.name), )

    # Bring the device down to rommon> prompt prior to TFTP boot
    with steps.start("Bring device {} down to rommon> prompt prior to TFTP boot".\
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
                device.expect(['.*Initializing Hardware.*'],
                              target=target, timeout=60)

            pcall(reload_check,
                  ckwargs={'device': device},
                  ikwargs=[{'target': 'active'},
                           {'target': 'standby'}])
        else:
            device.expect(['.*Initializing Hardware.*'], timeout=60)

        log.info("Device is reloading")
        device.destroy_all()

    # Begin TFTP boot of device
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
        if not _disconnect_reconnect(device):
            # If that still doesnt work, Thats all we got
            step.failed("Cannot reconnect to the device {d} after TFTP boot".
                            format(d=device.name), )
        else:
            log.info("Success - Have recovered and reconnected to device '{}'".\
                     format(device.name))

    # Reset config-register to 0x2101
    with steps.start("Reset config-register to 0x2101 on {}".\
                        format(device.name)) as step:
        try:
            device.api.execute_set_config_register(config_register='0x2102',
                                                   timeout=config_reg_timeout)
        except Exception as e:
            log.error(str(e))
            step.failed("Unable to reset config-register to 0x2101 after TFTP"
                           " boot on {}".format(device.name), )

    # Execute 'write memory'
    with steps.start("Execute 'write memory' on {}".format(device.name)) as step:
        try:
            device.api.execute_write_memory()
        except Exception as e:
            log.error(str(e))
            step.failed("Unable to execute 'write memory' after TFTP boot "
                           "on {}".format(device.name), )
        else:
            section.passed("Successfully performed TFTP boot on device {}".\
                            format(device.name))

@clean_schema({
    Optional('timeout'): int
})
@aetest.test
def install_remove_inactive(section, steps, device, timeout=180):
    """ This stage removes partially installed packages/images left
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

    with steps.start("Removing inactive packages") as step:

        install_remove_inactive_dialog = Dialog([
            Statement(pattern=r".*Do you want to remove the above files\? \[y\/n\]",
                      action='sendline(y)',
                      loop_continue=False,
                      continue_timer=False),
        ])

        try:
            device.execute('install remove inactive',
                           reply=install_remove_inactive_dialog,
                           timeout=timeout)
        except Exception as e:
            step.failed("Remove inactive packages failed. Error: {e}".format(e=str(e)))

@clean_schema({
    Optional('images'): list,
    Optional('save_system_config'): bool,
    Optional('install_timeout'): int,
    Optional('reload_timeout'): int,
})
@aetest.test
def install_image(section, steps, device, images, save_system_config=False,
                  install_timeout=500, reload_timeout=800):
    """ This stage installs a provided image onto the device using the install
    CLI. It also handles the automatic reloading of your device after the
    install is complete.

    Stage Schema
    ------------
    install_image:
        images (list): Image to install

        save_system_config (bool, optional): Whether or not to save the system
            config if it was modified. Defaults to False.

        install_timeout (int, optional): Maximum time to wait for install
            process to finish. Defaults to 500.

        reload_timeout (int, optional): Maximum time to wait for reload process
            to finish. Defaults to 800.

    Example
    -------
    install_image:
        images:
          - /auto/some-location/that-this/image/stay-isr-image.bin
        save_system_config: True
        install_timeout: 1000
        reload_timeout: 1000

    """

    # Need to get directory that the image would be unpacked to
    # This is the same directory the image is in
    with steps.start("Learning the default directory where packages.conf will be unpacked to") as step:
        directory = get_default_dir(device=device)

    # packages.conf is hardcoded because it is required to set
    # the boot variable to packages.conf for 'install mode'
    # ----------------------------------------------------------
    # 'Bundle mode' is when we set the boot var to the image.bin
    new_boot_var = directory+'packages.conf'

    with steps.start("Configure boot variables for 'install mode' on '{dev}'".format(dev=device.hostname)) as step:
        with step.start("Delete all boot variables") as substep:
            # Get list of existing boot variables
            try:
                curr_boot_images = device.api.get_boot_variables(boot_var='current')
            except Exception as e:
                substep.failed("Unable to retrieve boot variables\nError: {e}".format(e=str(e)))

            if not curr_boot_images:
                substep.passed("No boot variables are configured")

            # delete the existing boot variables
            try:
                device.api.execute_delete_boot_variable(
                    boot_images=curr_boot_images, timeout=60)
            except Exception as e:
                substep.failed("Failed to delete all boot variables\nError: {e}".format(e=str(e)))
            else:
                substep.passed("Deleted all boot variables")

        with step.start("Configure boot system variable to '{boot_var}'".format(boot_var=new_boot_var)) as substep:
            try:
                device.api.execute_set_boot_variable(
                    boot_images=[new_boot_var], timeout=60)
            except Exception as e:
                substep.failed("Failed to configure new boot variables\nError: {e}".format(e=str(e)))
            else:
                substep.passed("Configured boot system variable")

        with step.start("Copy running-configuration to startup-configuration") as substep:
            try:
                device.api.execute_copy_run_to_start(
                    max_time=60, check_interval=30)
            except Exception as e:
                substep.failed("Failed to copy running-config to startup-config\nError: {e}".format(e=str(e)))
            else:
                substep.passed("Copied running-config to startup-config")

        # Verify next reload boot variables are correctly set
        with step.start("Verify next reload boot variables are correctly set") as substep:
            if not device.api.verify_boot_variable(boot_images=[new_boot_var]):
                substep.failed("Boot variables are not correctly set to {}"
                               .format([new_boot_var]))
            else:
                substep.passed("Boot variables are correctly set".format(device.name))

    with steps.start("Installing image '{img}' onto {dev}".format(
            img=images[0], dev=device.hostname)) as step:

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
                           error_pattern=['FAILED:'],
                           timeout=install_timeout)
        except Exception as e:
            step.failed("Installing image '{img}' failed. Error: {e}"
                        .format(img=images[0], e=str(e)))

    with steps.start("Waiting for {dev} to reload".format(dev=device.hostname)) as step:

        timeout = Timeout(reload_timeout, 60)
        while timeout.iterate():
            timeout.sleep()
            device.destroy()

            try:
                device.connect(learn_hostname=True)
            except Exception:
                log.info("{dev} is not reloaded".format(dev=device.hostname))
            else:
                step.passed("{dev} has successfully reloaded".format(dev=device.hostname))

        step.failed("{dev} failed to reboot".format(dev=device.hostname))

    image_mapping = section.history['install_image'].parameters.setdefault(
        'image_mapping', {})
    image_mapping.update({images[0]: new_boot_var})

@clean_schema({
    'packages': list,
    Optional('save_system_config'): bool,
    Optional('install_timeout'): int,
})
@aetest.test
def install_packages(section, steps, device, packages, save_system_config=False,
                     install_timeout=300):
    """ This stage installs the provided packages using the install CLI.

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
                device.execute('install add file {} activate commit'.format(pkg),
                               reply=install_add_one_shot_dialog,
                               error_pattern=['FAILED:'],
                               timeout=install_timeout)
            except Exception as e:
                step.failed("Installing package '{pkg}' failed. Error: {e}"
                            .format(pkg=pkg, e=str(e)))
