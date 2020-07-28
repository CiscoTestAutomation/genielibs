'''
IOSXE CAT9K specific clean stages
'''

# Python
import logging

# pyATS
from pyats import aetest
from pyats.log.utils import banner
from pyats.utils.fileutils import FileUtils

# Genie
from genie.libs.clean.utils import clean_schema

# MetaParser
from genie.metaparser.util.schemaengine import Optional

# Logger
log = logging.getLogger(__name__)


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
             "\n5- Write to memory or save running-config to startup-configuration"
             "\n6- Verify next reload boot variables are set correctly")


    # Delete any previously configured boot variables
    with steps.start("Delete any previously configured boot variables on {}".\
                     format(device.name)) as step:

        # Get list of existing boot images if any
        try:
            curr_boot_images = device.api.get_boot_variables(boot_var='current')
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


    # Verify next reload boot variables are correctly set
    with steps.start("Verify next reload boot variables are correctly set "
                     "on {}".format(device.name)) as step:
        if not device.api.verify_boot_variable(boot_images=images):
            log.error(banner("*** Terminating Genie Clean ***"))
            section.failed("Boot variables are not correctly set to {} prior "
                           "to reloading device {}".format(images, device.name),
                           goto=['exit'])
        else:
            section.passed("Successfully verified boot variables are correctly "
                           "set on {}".format(device.name))
