'''IOSXE execute functions for platform'''

# Python
import re
import logging
import time

# pyATS
from pyats.utils.fileutils import FileUtils

# Genie
from genie.utils import Dq
from genie.harness.utils import connect_device
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import StateMachineError,SubCommandFailure


# Logger
log = logging.getLogger(__name__)


def execute_delete_boot_variable(device, boot_images=[], timeout=300):
    ''' Delete the boot variables
        Args:
            device ('obj'): Device object
            boot_images ('list', optional): List of strings of system images to delete as boot variable.default is an empty list
            timeout ('int'): Max time to delete boot vars in seconds
    '''

    if not boot_images:
        log.info("Removing boot variable on {device}".format(device=device))
        try:
            device.configure('no boot system')
        except SubCommandFailure as e:
            raise SubCommandFailure(
                "Could not removing boot variable on {device}. Error:\n{error}".format(device=device, error=e))
    else:
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
            boot_images ('list'): List of strings of system images to set as boot variable
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
                            install_timeout=660, reconnect_max_time=120,
                            reconnect_interval=30, _install=True, install_commit_sleep_time=None):
    """ Installs package
        Args:
            device ("obj"): Device object
            image_dir ("str"): Directory image is located in
            image ("str"): Image name
            save_system_config ("bool"): If config changed do we save it?
            install_timeout ("int"): Maximum time for install. Default 660
            reconnect_max_time ("int"): Maximum time for reconnect. Default 120
            reconnect_interval ("int"): Time between reconnect attempts. Default 30
            install_commit_sleep_time ("int"): Sleep time before install commit command
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
        device.execute(cmd, reply=dialog, timeout=install_timeout)
        device.enable()
    except StateMachineError:
        # this will be raised after 'Return to get started' is seen
        timeout = Timeout(reconnect_max_time, reconnect_interval)
        while timeout.iterate():
            device.destroy()
            try:
                connect_device(device)
            except Exception as e:
                connection_error = str(e)
                timeout.sleep()
                continue
            break
        else:
            raise Exception("Couldn't reconnect to the device. Error: {}"\
                            .format(connection_error))

    if _install:
        cmd = "install commit"
    else:
        cmd = """install commit
        install remove file {dir}{image}""".format(
            dir=image_dir, image=image
        )
    if install_commit_sleep_time:
        time.sleep(install_commit_sleep_time)
    device.execute(cmd, timeout=install_timeout)

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
                              timeout=660, install_commit_sleep_time=None):
    """ Uninstalls package
        Args:
            device ("obj"): Device object
            image_dir ("str"): Directory image is located in
            image ("str"): Image name
            save_system_config ("bool"): If config changed do we save it?
            timeout ("int"): maximum time for install
            install_commit_sleep_time ("int"): Sleep time before install commit command

        Raises:
            Exception

        Returns:
            True if install succeeded else False
    """
    return execute_install_package(
        device,
        image_dir,
        image,
        save_system_config,
        timeout,
        _install=False,
        install_commit_sleep_time=install_commit_sleep_time)


def delete_unprotected_files(device,
                             directory,
                             protected,
                             files_to_delete=None,
                             dir_output=None,
                             allow_failure=False):
    """delete all files not matching regex in the protected list
        Args:
            device ('obj'): Device object
            directory ('str'): working directory to perform the operation
            protected ('list'): list of file patterns that won't be deleted. If it begins
                                and ends with (), it will be considered as a regex
            files_to_delete('list') list of files that should be deleted unless they are not protected
            dir_output ('str'): output of dir command, if not provided execute the cmd on device to get the output
            allow_failure (bool, optional): Allow the deletion of a file to silently fail. Defaults to False.
        Returns:
            None
            """

    protected_set = set()
    fu_device = FileUtils.from_device(device)
    file_set = set(
        Dq(device.parse('dir {}'.format(directory),
                        output=dir_output)).get_values('files'))

    if isinstance(protected, str):
        protected = [protected]
    elif not isinstance(protected, (list, set)):
        raise TypeError("'{p}' must be a list")

    for pattern in protected:
        # it's a regex!
        if pattern.startswith('(') and pattern.endswith(')'):
            regexp = re.compile(pattern)
            protected_set.update(set(filter(regexp.match, file_set)))

        # just file names, exact match only
        elif pattern in file_set:
            protected_set.add(pattern)

    # if files_to_delete is given,updated protected files with the diff of file_set - files_to_delete
    # so that we only delete files that are in files_to_delete and NOT protected
    # in other words we remove the protected files from file_to_delete
    if files_to_delete:
        protected_set.update(file_set - set(files_to_delete))

    not_protected = file_set - protected_set
    error_messages = []

    if not_protected:
        log.info("The following files will be deleted:\n{}".format(
            '\n'.join(not_protected)))
        dont_delete_list = protected_set.intersection(files_to_delete)
        if dont_delete_list:
            log.info(
                "The following files will not be deleted because they are protected:\n{}"
                .format('\n'.join(dont_delete_list)))
        for file in not_protected:
            # it's a directory, dont delete
            if file.endswith('/'):
                continue
            log.info('Deleting the unprotected file "{}"'.format(file))
            try:
                fu_device.deletefile(file, device=device)
            except Exception as e:
                if allow_failure:
                    log.info('Failed to delete file "{}" but ignoring and moving '
                             'on due to "allow_failure=True".'.format(file))
                    continue

                error_messages.append('Failed to delete file "{}" due '
                                      'to :{}'.format(file, str(e)))
        if error_messages:
            raise Exception('\n'.join(error_messages))
    else:
        log.info(
            "No files will be deleted, the following files are protected:\n{}".
            format('\n'.join(protected_set)))
def execute_card_OIR(device, card_number, timeout=60):
    ''' Execute 'hw-module subslot <slot> oir power-cycle' on the device
        Args:
            device ('obj'): Device object
            card_number ('str'): Card number on which OIR has to be performed
            timeout ('int',optional): Max time for card oir execution to complete in seconds.Defaults to 60
    '''

    log.info("Executing 'hw-module subslot <slot> oir power-cycle' on the device")

    # Unicon Statement/Dialog
    dialog = Dialog([
             Statement(
             pattern=r"Proceed with power cycle of module? [confirm]",
             action='sendline()',
             loop_continue=True,
             continue_timer=False)
             ])
    command = 'hw-module subslot ' + card_number + ' oir power-cycle'

    try:
       output = device.execute(
                command,
                reply=dialog,
                timeout=timeout,
                append_error_pattern=['.*Command cannot be executed.*'])
    except Exception as err:
        log.error("Failed to execute 'hw-module subslot <slot> oir power-cycle': {err}".format(err=err))
        raise Exception(err)

    if output:
        log.info("Successfully executed 'hw-module subslot <slot> oir power-cycle'")
    else:
        raise Exception("Failed to execute 'hw-module subslot <slot> oir power-cycle'")


def execute_clear_platform_software_fed_active_acl_counters_hardware(device):
    """ clear platform software fed active acl counters hardware
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.execute("clear platform software fed active acl counters hardware")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not clear counters on {device}. Error:\n{e}")


def execute_clear_platform_software_fed_switch_acl_counters_hardware(device,switch_num):
    """ clear platform software fed switch acl counters hardware
        Args:
            device ('obj'): Device object
            switch_num ('int'): Switch number to clear acl counters
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.execute("clear platform software fed switch {switch_num} acl counters hardware".format(switch_num=switch_num))
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not clear counters on {device}. Error:\n{e}")

