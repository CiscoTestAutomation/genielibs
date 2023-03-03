
import re
import logging
from genie.utils import Dq
from pyats.utils.fileutils import FileUtils

log = logging.getLogger(__name__)


def _protected_and_unprotected_files(file_set, protected, files_to_delete=None):
    protected_set = set()
    if isinstance(protected, str):
        protected = [protected]
    elif not isinstance(protected, (list, set)):
        raise TypeError("'{p}' must be a list")

    for pattern in protected:
        # it's a regex!
        if '(' in pattern:
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

    return protected_set, not_protected


def delete_unprotected_files(device,
                             directory,
                             protected,
                             files_to_delete=None,
                             dir_output=None,
                             destination=None):
    """delete all files not matching regex in the protected list
        Args:
            device ('obj'): Device object
            directory ('str'): working directory to perform the operation
            protected ('list'): list of file patterns that won't be deleted. If it begins
                                and ends with (), it will be considered as a regex
            files_to_delete('list') list of files that should be deleted unless they are not protected
            dir_output ('str'): output of dir command, if not provided execute the cmd on device to get the output
            destination ('str') : Destination directory. default to None. i.e bootflash:/
        Returns:
            None
            """

    fu_device = FileUtils.from_device(device)
    file_set = set(
        Dq(device.parse('ls -l {}'.format(directory),
                        output=dir_output)).get_values('files'))

    protected_set, not_protected = _protected_and_unprotected_files(file_set, protected, files_to_delete)
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
                error_messages.append('Failed to delete file "{}" due '
                                      'to :{}'.format(file, str(e)))
        if error_messages:
            raise Exception('\n'.join(error_messages))
    else:
        log.info(
            "No files will be deleted, the following files are protected:\n{}".
            format('\n'.join(protected_set)))


def free_up_disk_space(device, destination, required_size, skip_deletion,
                       protected_files=None,
                       min_free_space_percent=None,
                       dir_output=None):

    '''Delete files to create space on device except protected files
    Args:
        device ('Obj') : Device object
        destination ('str') : Destination directory, i.e bootflash:/
        required_size ('int') : Check if enough space to fit given size in bytes.
                                If this number is negative it will be assumed
                                the required size is not available.
        skip_deletion ('bool') : Only performs checks, no deletion
        protected_files ('list') : List of file patterns that wont be deleted.
        min_free_space_percent ('int'): Minimum acceptable free disk space %.
                                        Optional,
        dir_output ('str'): Output of 'dir' command
                            if not provided, executes the cmd on device
    Returns:
         True if there is enough space after the operation, False otherwise
    '''
    if not destination:
        log.warning('No destination provided, cannot verify available space')
        return True
    df_info = device.parse('df {}'.format(destination), output=dir_output)

    dir_df_info = df_info['directory'].values()
    if dir_df_info:
        dir_df_info = list(dir_df_info)[0]
        free_space = dir_df_info.get('available')

    if not dir_df_info or not free_space:
        log.error('Unable to determine available space')
        return True

    # Check if available space is sufficient
    if min_free_space_percent:

        # Get total space
        total_space = dir_df_info.get('total')

        # Get current available space in %
        avail_percent = 100 - dir_df_info.get('use_percentage')

        log.info("There is {avail} % of free space on the disk, which is "
                 "{compare} than the target of {target} %.".
                 format(avail=round(avail_percent, 2), compare='less' if
                        avail_percent < min_free_space_percent else 'greater',
                        target=min_free_space_percent))

        # get bigger of required_space or min_free_space_percent
        required_size = round(
            max(required_size, min_free_space_percent * .01 * total_space))

    if free_space > required_size:
        log.info('APIC: enough free space available: {}'.format(free_space))
        return True

    log.warning('APIC: not enough free space, required: {}, available: {}'.format(
        required_size, free_space
    ))

    ls_output = device.execute('ls -l {}'.format(destination))
    file_info = device.parse('ls -l {}'.format(destination), output=ls_output)
    dq = Dq(file_info)

    # turn parsed dir output to a list of files for sorting
    # Large files are given priority when deleting
    file_list = []
    for file in dq.get_values('files'):
        file_list.append((file, int(dq.contains(file).get_values('size')[0])))

    file_list.sort(key=lambda x: x[1], reverse=True)

    # create lis of filenames
    files_to_be_deleted = set(x[0] for x in file_list)
    # filter list and get list of unprotected files
    _, unprotected_files = _protected_and_unprotected_files(files_to_be_deleted, protected_files)

    # create ordered list of unprotected files
    to_be_deleted = [x[0] for x in file_list if x[0] in unprotected_files]
    log.info('Files to be deleted: {}'.format(to_be_deleted))

    for file, size in file_list:
        device.api.delete_unprotected_files(directory=destination,
                                            protected=protected_files,
                                            files_to_delete=[file],
                                            dir_output=ls_output)

        if device.api.verify_enough_disk_space(required_size, destination):
            log.info("Verified there is enough space on the device after "
                     "deleting unprotected files.")
            return True

    # Exhausted list of files - still not enough space
    log.error('There is still not enough space on the device after '
              'deleting unprotected files.')
    return False
