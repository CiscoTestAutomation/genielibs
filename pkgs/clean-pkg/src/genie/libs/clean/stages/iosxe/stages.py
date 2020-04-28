'''
IOSXE specific clean stages
'''

# Python
import time
import logging

# pyATS
from pyats import aetest
from pyats.async_ import pcall
from pyats.log.utils import banner
from pyats.utils.fileutils import FileUtils

# Unicon
from unicon.eal.dialogs import Statement, Dialog

# Genie
from genie.libs import clean
from genie.abstract import Lookup
from .recovery import tftp_recover_from_rommon
from ..recovery import _disconnect_reconnect
from genie.libs.clean.utils import clean_schema

# MetaParser
from genie.metaparser.util.schemaengine import Optional

# Logger
log = logging.getLogger()


#===============================================================================
#                       stage: change_boot_variable
#===============================================================================

@clean_schema({
    'images': list,
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

    '''
    Clean yaml file schema:
    -----------------------
    devices:
      <device>:
        change_boot_variable:
          images ('list'): List of images to copy (Mandatory)
          timeout ('int'): Execute timeout in seconds
                           Default 300 (Optional)
          max_time ('int'): Maximum time to wait while saving running-config
                            to startup-config in seconds.
                            Default 300 (Optional)
          check_interval ('int'): Time interval while checking save running
                                  config to startup-config completed in seconds.
                                  Default 30 (Optional)
          write_memory ('bool'): Execute 'write memory' after setting BOOT var
                                 Default False (Optional)
          config_register ('str'): Value to set config-register for reload
                                   Default '0x2102' (Optional)

    Example:
    --------
    devices:
      N95_1:
        change_boot_variable:
          images:
            - harddisk:/Genie-12351822-iedge-asr-uut
          timeout: 150
          max_time: 300
          check_interval: 20

    Flow:
    -----
    before:
      copy_to_device (Optional, If images to set as boot variable is not already on device)
    after:
      write_erase (Optional, user wants to reload with current running configuration or not)
    '''

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
            curr_boot_images = device.api.get_boot_variables()
        except Exception as e:
            section.failed("Unable to check existing boot images on {}:\n{}".\
                           format(device.name, str(e)), goto=['exit'])

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
                            "variable on {}".format(device.name))
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
                log.error(banner("*** Terminating Genie Clean ***"))
                section.failed("Failed to execute 'write memory' after setting "
                               "BOOT variables on device {}".format(device.name),
                               goto=['exit'])
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
            log.error(banner("*** Terminating Genie Clean ***"))
            section.failed("Failed to set boot variables to images specified "
                           "on device {}\n".format(device.name), goto=['exit'])
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
            log.error(banner("*** Terminating Genie Clean ***"))
            section.failed("Failed to set config-register correctly on device "
                           "{}".format(device.name), goto=['exit'])
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
                log.error(banner("*** Terminating Genie Clean ***"))
                section.failed("Failed to execute 'write memory' after setting "
                               "BOOT variables on device {}".format(device.name),
                               goto=['exit'])
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
                log.error(banner("*** Terminating Genie Clean ***"))
                section.failed("Failed to set copy running-config to "
                               "startup-config on device {}".\
                               format(device.name), goto=['exit'])
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
            log.error(banner("*** Terminating Genie Clean ***"))
            section.failed("Boot variables not correctly set for reloading "
                           "device {}".format(device.name), goto=['exit'])
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
            log.error(banner("*** Terminating Genie Clean ***"))
            section.failed("Config-register not correctly set for next reload "
                           "on device {}".format(device.name), goto=['exit'])
        else:
            step.passed("Verified config-register is correctly set on {}".\
                        format(device.name))


#===============================================================================
#                       stage: tftp_boot
#===============================================================================


@clean_schema({
    'image': list,
    'ip_address': list,
    'subnet_mask': str,
    'gateway': str,
    'tftp_server': str,
    'timeout': int
})
@aetest.test
def tftp_boot(section, steps, device, ip_address, subnet_mask, gateway,
              tftp_server, image, timeout=120):
    '''
    Clean yaml file schema:
    -----------------------
        tftp_boot:
            image: <Image to boot with `str`> (Mandatory)
            ip_address: <Management ip address to configure to reach to the TFTP server `str`> (Mandatory)
            subnet_mask: <Management subnet mask `str`> (Mandatory)
            gateway: <Management gateway `str`> (Mandatory)
            tftp_server: <tftp server is reachable with management interface> (Mandatory)

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

    Flow:
    -----
        Before:
            Any
        After:
            Connect
    '''

    # If the tftp boot has already ran - recovery
    # Then do not run it again and skip this section
    if section.parameters['common_data'].get('device_tftp_booted'):
        section.skipped('The global recovery has already booted the device with'
                        ' the provided tftp image - no need to do it again')

    device.api.execute_set_config_register(config_register='0x0', timeout='60')
    # Using sendline, as we dont want unicon boot to kick in and send "boot" to
    # the device
    # Cannot use .reload as in case of HA, we need both sup to do the commands
    device.sendline('reload')
    device.sendline('yes')
    device.sendline()
    log.info('** Rebooting the device **')

    # We now want to overwrite the statemachine
    device.destroy_all()
    # Sleep to make sure the device is reloading
    time.sleep(20)

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
        result = pcall(abstract.clean.stages.recovery.recovery_worker,
                       start=device.start,
                       ikwargs = [{'item': i} for i, _ in enumerate(device.start)],
                       ckwargs = \
                            {'device': device,
                             'timeout': timeout,
                             'tftp_boot': tftp_boot,
                             'break_count': 0,
                             # Irrelevant as we will not use this pattern anyway
                             # But needed for the recovery
                             'console_activity_pattern': '\\.\\.\\.\\.',
                             'golden_image': None,
                             'recovery_password': None})
    except Exception as e:
        log.error(str(e))
        section.failed("Failed to recover the device '{}'".\
                        format(device.name))
    else:
        log.info("Successfully recovered the device '{}'".\
                 format(device.name))

    # Disconnect and reconnect to the device
    if not _disconnect_reconnect(device):
        # If that still doesnt work, Thats all we got
        section.failed("Cannot reconnect to the device {d}".
                        format(d=device.name))
    else:
        log.info("Success - Have recovered and reconnected to device '{}'".\
                 format(device.name))

    device.api.execute_set_config_register(config_register='0x2102', timeout='60')
    device.api.execute_write_memory()
