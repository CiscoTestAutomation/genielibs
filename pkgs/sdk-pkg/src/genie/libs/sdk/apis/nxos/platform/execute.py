'''NXOS execute functions for platform'''

# Python
import re
import logging

# pyATS
from pyats.utils.fileutils import FileUtils

# Unicon
from unicon.eal.dialogs import Statement, Dialog

# Logger
log = logging.getLogger(__name__)


def execute_change_boot_variable(device, system, kickstart=None, timeout=300):

    ''' Set the boot variables
        Args:
            device ('obj'): Device object
            system ('str'): System image
            kickstart ('str'): Kickstart image
            timeout ('int'): Timeout in seconds
    '''

    try:
        # Make sure device.configure contain the following
        # configure fail patterns "can not open|not supported |failed | fail| Abort"
        if kickstart:
            device.configure('boot kickstart {i}'.format(i=kickstart),
                timeout=timeout)
            device.configure('boot system {i}'.format(i=system),
                timeout=timeout)
        else:
            # N9K
            device.configure('boot nxos {i}'.format(i=system),
                timeout=timeout)
    except Exception as e:
        raise Exception("Failed to set boot variables "
                        "for '{d}': {e}".format(d=device.name, e=e))

    # Make sure current variables are as expected
    device.api.is_current_boot_variable_as_expected(system, kickstart)


def execute_write_erase(device, timeout=300):

    ''' Execute write erase on the device
        Args:
            device ('obj'): Device object
    '''

    log.info("Executing Write Erase")
    write_erase = Statement(
        pattern=r'.*Do you wish to proceed anyway\? \(y\/n\)\s*\[n\]',
        action='sendline(y)',
        loop_continue=True,
        continue_timer=False)

    # Add permisson denied to error pattern
    origin = list(device.execute.error_pattern)
    error_pattern = ['.*[Pp]ermission denied.*']
    error_pattern.extend(origin)

    try:
        device.execute("write erase", reply=Dialog([write_erase]),
                       timeout=timeout, error_pattern=error_pattern)
    except Exception as err:
        log.error("Failed to write erase: {err}".format(err=err))
        raise Exception(err)
    finally:
        # restore original error pattern
        device.execute.error_pattern = origin

def execute_write_erase_boot(device, timeout=300):
    ''' Execute write erase on the device
        Args:
            device ('obj'): Device object
    '''

    log.info("Executing Write Erase Boot")
    write_erase = Statement(
        pattern=r'.*Do you wish to proceed anyway\? \(y\/n\)\s*\[n\]',
        action='sendline(y)',
        loop_continue=True,
        continue_timer=False)

    try:
        device.execute("write erase boot", reply=Dialog([write_erase]),
                       timeout=timeout)
    except Exception as err:
        log.error("Failed to write erase boot: {err}".format(err=err))
        raise Exception(err)


def delete_unprotected_files(device, directory, protected, files_to_delete=None, dir_output=None):
    """delete all files not matching regex in the protected list
        Args:
            device ('obj'): Device object
            directory ('str'): working directory to perform the operation
            protected ('list'): list of file patterns that won't be deleted. If it begins
                                and ends with (), it will be considered as a regex
            files_to_delete('list') list of files that should be deleted unless they are not protected
            dir_output ('str'): output of dir command, if not provided execute the cmd on device to get the output
        Returns:
            None
            """

    protected_set = set()
    fu_device = FileUtils.from_device(device)
    file_set = set(device.parse('dir {}'.format(directory), output=dir_output).get('files',{}).keys())

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
    log.debug("protected patterns : {}".format(protected))
    log.debug("found files : {}".format(file_set))
    log.debug("protected files : {}".format(protected_set))
    log.debug("non-protected files : {}".format(not_protected))
    if not_protected:
        log.info("The following files will be deleted:\n{}".format(
            '\n'.join(not_protected)))
        dont_delete_list = protected_set.intersection(files_to_delete)
        if dont_delete_list:
            log.info("The following files will not be deleted because they are protected:\n{}".format(
                '\n'.join(dont_delete_list)))
        for file in not_protected:
            # it's a directory, dont delete
            if file.endswith('/'):
                continue
            log.info('Deleting the unprotected file "{}"'.format(file))
            try:
                fu_device.deletefile(directory+file, device=device)
            except Exception as e:
                error_messages.append('Failed to delete file "{}" due '
                                      'to :{}'.format(file, str(e)))
        if error_messages:
            raise Exception('\n'.join(error_messages))
    else:
        log.info("No files will be deleted, the following files are protected:\n{}".format(
            '\n'.join(protected_set)))
