'''IOSXE execute functions for platform'''

# Python
import logging

# Unicon
from unicon.eal.dialogs import Statement, Dialog

# Logger
log = logging.getLogger(__name__)


def execute_delete_boot_variable(device, boot_images, timeout=300):
    ''' Set the boot variables
        Args:
            device ('obj'): Device object
            boot_images ('str'): System image to delete as boot variable
            timeout ('int'): Max time to delete boot vars in seconds
    '''

    for image in boot_images:
        try:
            device.configure("no boot system {}".format(image), timeout=timeout)
        except Exception as e:
            raise Exception("Failed to delete boot variables on '{}'\n{}".\
                            format(device.name, str(e)))
        else:
            log.info("Deleted '{}' from BOOT variable".format(image))


def execute_set_boot_variable(device, boot_images, timeout=300):
    ''' Set the boot variables
        Args:
            device ('obj'): Device object
            boot_images ('str'): System image to set as boot variable
            timeout ('int'): Max time to set boot vars in seconds
    '''

    for image in boot_images:
        try:
            device.configure("boot system {}".format(image), timeout=timeout)
        except Exception as e:
            raise Exception("Failed to set boot variables on '{}'\n{}".\
                            format(device.name, str(e)))
        else:
            log.info("Added '{}' to BOOT variable".format(image))


def execute_set_config_register(device, config_register, timeout=300):
    '''Set config register to load image in boot variable
        Args:
            device ('obj'): Device object
            config_reg ('str'): Hexadecimal value to set the config register to
            timeout ('int'): Max time to set config-register in seconds
    '''

    try:
        device.configure("config-register {}".format(config_register),
                         timeout=timeout)
    except Exception as e:
        raise Exception("Failed to set config register for '{d}'\n{e}".\
                        format(d=device.name, e=str(e)))
    else:
        log.info("Set config-register to '{}'".format(config_register))


def execute_write_erase(device, timeout=300):
    ''' Execute 'write erase' on the device
        Args:
            device ('obj'): Device object
            timeout ('int'): Max time to for write erase to complete in seconds
    '''

    log.info("Executing 'write erase' on the device")

    # Unicon Statement/Dialog
    write_erase = Statement(
        pattern=r".*remove all configuration files\! Continue\? \[confirm\]",
        action='sendline()',
        loop_continue=True,
        continue_timer=False)

    try:
        output = device.execute("write erase", reply=Dialog([write_erase]),
                                timeout=timeout)
    except Exception as err:
        log.error("Failed to write erase: {err}".format(err=err))
        raise Exception(err)

    if "[OK]" in output:
        log.info("Successfully executed 'write erase'")
    else:
        raise Exception("Failed to execute 'write erase'")


def execute_write_memory(device, timeout=300):
    ''' Execute 'write memory' on the device
        Args:
            device ('obj'): Device object
            timeout ('int'): Max time to for write memory to complete in seconds
    '''

    log.info("Executing 'write memory' on the device")

    try:
        output = device.execute("write memory", timeout=timeout)
    except Exception as err:
        log.error("Failed to execute 'write memory'\n{err}".format(err=err))
        raise Exception(err)

    if "[OK]" in output:
        log.info("Successfully executed 'write memory'")
    else:
        raise Exception("Failed to execute 'write memory'")
