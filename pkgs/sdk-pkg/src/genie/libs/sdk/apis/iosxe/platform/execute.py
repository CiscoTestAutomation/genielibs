'''IOSXE execute functions for platform'''

# Python
import logging

# Genie
from genie.harness.utils import connect_device
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import StateMachineError

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

    # Add permisson denied to error pattern
    origin = list(device.execute.error_pattern)
    error_pattern = ['.*[Pp]ermission denied.*']
    error_pattern.extend(origin)

    try:
        output = device.execute("write erase", reply=Dialog([write_erase]),
                                timeout=timeout, error_pattern=error_pattern)
    except Exception as err:
        log.error("Failed to write erase: {err}".format(err=err))
        raise Exception(err)
    finally:
        # restore original error pattern
        device.execute.error_pattern = origin

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

def execute_install_package(device, image_dir, image, save_system_config=True,
                            timeout=660, _install=True):
    """ Installs package
        Args:
            device ("obj"): Device object
            image_dir ("str"): Directory image is located in
            image ("str"): Image name
            save_system_config ("bool"): If config changed do we save it?
            timeout ("int"): maximum time for install

            _install ("bool"): True to install, False to uninstall.
                Not meant to be changed manually.

        Raises:
            Exception

        Returns:
            True if install succeeded else False
    """
    dialog = Dialog([
        Statement(pattern=r".*Press Quit\(q\) to exit, you may save "
                          r"configuration and re-enter the command\. "
                          r"\[y\/n\/q\]",
                  action='sendline(y)' if save_system_config else 'sendline(n)',
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r".*This operation may require a reload of the "
                          r"system\. Do you want to proceed\? \[y\/n\]",
                  action='sendline(y)',
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r"^.*RETURN to get started",
                  action='sendline()',
                  loop_continue=False,
                  continue_timer=False)
    ])

    if _install:
        cmd = """install add file {dir}{image}
        install activate file {dir}{image}""".format(
            dir=image_dir, image=image
        )
    else:
        cmd = "install deactivate file {dir}{image}".format(
            dir=image_dir, image=image
        )

    try:
        device.execute(cmd, reply=dialog, timeout=timeout)
    except StateMachineError:
        # this will be raised after 'Return to get started' is seen
        device.destroy()
        timeout = Timeout(90, 30)
        while timeout.iterate():
            try:
                connect_device(device)
            except Exception:
                timeout.sleep()
                continue
            break
        else:
            raise Exception("Couldnt reconnect to the device")

    if _install:
        cmd = "install commit"
    else:
        cmd = """install commit
        install remove file {dir}{image}""".format(
            dir=image_dir, image=image
        )

    device.execute(cmd)

    try:
        out = device.parse("show install summary")
    except SchemaEmptyParserError:
        out = {}

    for location in out.get("location"):
        for pkg in out['location'][location]['pkg_state']:
            pkg = out['location'][location]['pkg_state'][pkg]
            if (_install and
                    image in pkg['filename_version'] and
                    'C' == pkg['state']):
                # the image should exist; it was just installed
                return True
            elif (not _install and
                    image in pkg['filename_version']):
                # the image should not exist; it was just uninstalled.
                return False

    return False if _install else True

def execute_uninstall_package(device, image_dir, image, save_system_config=True,
                              timeout=660):
    """ Uninstalls package
        Args:
            device ("obj"): Device object
            image_dir ("str"): Directory image is located in
            image ("str"): Image name
            save_system_config ("bool"): If config changed do we save it?
            timeout ("int"): maximum time for install

        Raises:
            Exception

        Returns:
            True if install succeeded else False
    """
    return execute_install_package(
        device, image_dir, image, save_system_config, timeout, _install=False)