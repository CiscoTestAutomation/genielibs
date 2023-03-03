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
from unicon.core.errors import StateMachineError

# Logger

log = logging.getLogger(__name__)


def execute_delete_boot_variable(device, boot_images, timeout=300):
    ''' Delete the boot variables
        Args:
            device ('obj'): Device object
            boot_images ('list'): List of strings of system images to delete as boot variable
            timeout ('int', optional): Max time to delete boot vars in seconds
                            Default is 300
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
            boot_images ('list'): List of strings of system images to set as boot variable
            timeout ('int', optional): Max time to set boot vars in seconds
                             Default is 300
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
            timeout ('int', optional): Max time to set config-register in seconds
                            Default is 300
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
            timeout ('int', optional): Max time to for write erase to complete in seconds
                            Default is 300
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
            timeout ('int', optional): Max time for write memory to complete in seconds
                            Default is 300
    '''

    log.info("Executing 'write memory' on the device")

    dialog = Dialog([
        Statement(
            pattern=r'Continue\? \[no\]:\s*$',
            action='sendline(yes)',
            loop_continue=True)
    ])

    try:
        output = device.execute("write memory", reply=dialog, timeout=timeout)
    except Exception as err:
        log.error("Failed to execute 'write memory'\n{err}".format(err=err))
        raise Exception(err)

    if "[OK]" in output:
        log.info("Successfully executed 'write memory'")
    else:
        raise Exception("Failed to execute 'write memory'")


def delete_unprotected_files(device,
                             directory,
                             protected,
                             files_to_delete=None,
                             dir_output=None,
                             allow_failure=False,
                             destination=None):
    """delete all files not matching regex in the protected list
        Args:
            device ('obj'): Device object
            directory ('str'): working directory to perform the operation
            protected ('list'): list of file patterns that won't be deleted. If it begins
                                and ends with (), it will be considered as a regex
            files_to_delete('list') list of files that should be deleted unless they are not protected
            dir_output ('str'): output of dir command, if not provided execute the cmd on device to get the output
            allow_failure (bool, optional): Allow the deletion of a file to silently fail. Defaults to False.
            destination ('str') : Destination directory. default to None. i.e bootflash:/
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
            log.info(f'Deleting the unprotected file "{file}"')
            try:
                if destination:
                    fu_device.deletefile(f"{destination}{file}", device=device)
                else:
                    fu_device.deletefile(file, device=device)
            except Exception as e:
                if allow_failure:
                    log.info(
                        f'Failed to delete file "{file}" but ignoring and moving on due to "allow_failure=True".'
                    )
                    continue

                error_messages.append(f'Failed to delete file "{file}" due to :{str(e)}')
        if error_messages:
            raise Exception('\n'.join(error_messages))
    else:
        log.info(
            "No files will be deleted, the following files are protected:\n{}".
            format('\n'.join(protected_set)))

def execute_card_OIR(device, card_number):
    ''' Execute 'hw-module subslot <slot> oir power-cycle' on the device
        Args:
            device ('obj'): Device object
            card_number ('str'): Card number on which OIR has to be performed
    '''
    log.info("Executing 'hw-module subslot <slot> oir power-cycle' on the device")

    try:
        output = device.transmit('hw-module subslot {card_number} oir power-cycle'.format(card_number=card_number)) 
        device.transmit('\r')
        device.transmit('\r')
    except Exception as err:
        raise Exception(err)

    if 'True' in output:
        log.info("Successfully executed 'hw-module subslot <slot> oir power-cycle'")
    else:
        raise Exception("Failed to execute 'hw-module subslot <slot> oir power-cycle'")
