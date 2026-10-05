import logging
import re
import time

from pyats.utils.fileutils import FileUtils

from genie.libs.sdk.apis.execute import (
    _DiskCleanupStrategy,
    _get_disk_cleanup_operation_timeout,
    _run_disk_cleanup_with_strategy,
)

log = logging.getLogger(__name__)


def _classify_apic_disk_cleanup_entry(entry_name, file_details):
    """Return the APIC filesystem entry type from mode metadata."""
    entry_details = file_details.get(entry_name)
    if not isinstance(entry_details, dict):
        return None

    mode = str(entry_details.get('mode', ''))
    if mode.startswith('-'):
        return 'file'
    if mode.startswith('d'):
        return 'directory'
    return None


def _delete_apic_disk_cleanup_batch(device, destination, protected_files,
                                    candidate_batch, directory_output,
                                    deadline, **_kwargs):
    """Delete an APIC batch of validated regular files."""
    return device.api.delete_unprotected_files(
        directory=destination,
        protected=protected_files,
        files_to_delete=[candidate.path for candidate in candidate_batch],
        dir_output=directory_output,
        deadline=deadline,
    )


def _get_apic_disk_cleanup_space(device, destination):
    """Return available space through the APIC platform API."""
    return device.api.get_available_space(directory=destination)


_APIC_DISK_CLEANUP_STRATEGY = _DiskCleanupStrategy(
    classify_entry=_classify_apic_disk_cleanup_entry,
    delete_batch=_delete_apic_disk_cleanup_batch,
    get_available_space=_get_apic_disk_cleanup_space,
)


def _protected_and_unprotected_files(file_set, protected, files_to_delete=None):
    protected_set = set()
    protected = protected or []
    if isinstance(protected, str):
        protected = [protected]
    elif not isinstance(protected, (list, set)):
        raise TypeError("'{p}' must be a list")

    for pattern in protected:
        # Preserve APIC's existing behavior: patterns containing an opening
        # parenthesis are treated as regular expressions.
        if '(' in pattern:
            regexp = re.compile(pattern)
            protected_set.update(set(filter(regexp.match, file_set)))

        # Plain file names use exact matching.
        elif pattern in file_set:
            protected_set.add(pattern)

    # Restrict deletion to the explicitly requested subset when supplied.
    if files_to_delete:
        protected_set.update(file_set - set(files_to_delete))

    unprotected_files = file_set - protected_set
    return protected_set, unprotected_files


def delete_unprotected_files(device,
                             directory,
                             protected,
                             files_to_delete=None,
                             dir_output=None,
                             destination=None,
                             deadline=None):
    """Delete regular files that do not match the protection rules.

    Args:
        device ('obj'): Device object.
        directory ('str'): Directory in which to delete files.
        protected ('list'): File patterns that must not be deleted.
        files_to_delete ('list'): Optional subset of files to delete.
        dir_output ('str'): Optional captured output of the 'ls -l' command.
        destination ('str'): Destination retained for API compatibility.
        deadline ('float'): Optional monotonic cleanup deadline.

    Returns:
        bool or None: True when the deadline is reached; otherwise None.
    """

    try:
        parsed_output = device.parse(f'ls -l {directory}', output=dir_output)
    except Exception as error:
        log.error('Unable to identify safe cleanup candidates: %s', error)
        return None

    if not isinstance(parsed_output, dict):
        log.error('Unable to identify safe cleanup candidates')
        return None

    file_details = parsed_output.get('files', {})
    if not isinstance(file_details, dict):
        log.error('Unable to identify safe cleanup candidates')
        return None
    file_set = set(file_details)

    protected_set, unprotected_files = _protected_and_unprotected_files(file_set, protected, files_to_delete)
    error_messages = []

    # Only entries explicitly identified as regular files are safe to delete.
    unprotected_files = {
        file_name for file_name in unprotected_files
        if (isinstance(file_details.get(file_name), dict) and
            str(file_details[file_name].get('mode', '')).startswith('-'))
    }

    if unprotected_files:
        fu_device = FileUtils.from_device(device)
        if files_to_delete:
            unprotected_files = [file_name for file_name in files_to_delete if file_name in unprotected_files]
        else:
            unprotected_files = sorted(unprotected_files)
        log.info('The following files will be deleted:\n%s', '\n'.join(unprotected_files))
        protected_requested_files = protected_set.intersection(files_to_delete or [])
        if protected_requested_files:
            log.info(
                'The following files will not be deleted because they are '
                'protected:\n%s',
                '\n'.join(sorted(protected_requested_files)))
        for file_name in unprotected_files:
            if deadline is not None and time.monotonic() >= deadline:
                return True
            log.info('Deleting the unprotected file "%s"', file_name)
            try:
                delete_timeout = _get_disk_cleanup_operation_timeout(deadline)
                fu_device.deletefile(file_name, timeout_seconds=delete_timeout, device=device)
            except Exception as error:
                error_messages.append(f'Failed to delete file "{file_name}" due to: {error}')
        if error_messages:
            raise Exception('\n'.join(error_messages))
    else:
        log.info('No files will be deleted, the following files are protected:\n%s', '\n'.join(sorted(protected_set)))


def free_up_disk_space(device, destination, required_size, skip_deletion,
                       protected_files=None,
                       min_free_space_percent=None,
                       dir_output=None):

    """Delete unprotected APIC files until enough space is available.

    Args:
        device ('Obj'): Device object.
        destination ('str'): Destination directory.
        required_size ('int'): Required free space in bytes.
        skip_deletion ('bool'): Only perform checks when True.
        protected_files ('list'): File patterns that must not be deleted.
        min_free_space_percent ('int'): Minimum acceptable free-space percent.
        dir_output ('str'): Optional captured output of the 'df' command.

    Returns:
        bool: True when enough space is verified, otherwise False.
    """
    if not destination:
        log.warning('No destination provided, cannot verify available space')
        return False
    protected_files = protected_files or []
    try:
        parsed_output = device.parse(f'df {destination}', output=dir_output)
        directory_data = parsed_output.get('directory', {})
        filesystem_info = next(iter(directory_data.values()), None)
        available_space = filesystem_info.get('available') if filesystem_info else None
    except Exception as error:
        log.error('Unable to determine available space: %s', error)
        return False

    if available_space is None:
        log.error('Unable to determine available space')
        return False
    try:
        available_space = int(available_space)
    except (TypeError, ValueError):
        log.error('Unable to determine available space')
        return False

    if min_free_space_percent:
        total_space = filesystem_info.get('total')
        if total_space is None:
            log.error('Unable to determine total disk space')
            return False
        try:
            total_space = int(total_space)
        except (TypeError, ValueError):
            log.error('Unable to determine total disk space')
            return False
        if total_space <= 0:
            log.error('Unable to determine total disk space')
            return False

        use_percentage = filesystem_info.get('use_percentage')
        if use_percentage is None:
            log.error('Unable to determine disk use percentage')
            return False
        try:
            available_percent = 100 - float(use_percentage)
        except (TypeError, ValueError):
            log.error('Unable to determine disk use percentage')
            return False

        comparison = 'less' if available_percent < min_free_space_percent else 'greater'
        log.info(
            'There is %s %% of free space on the disk, which is %s than the '
            'target of %s %%.',
            round(available_percent, 2), comparison, min_free_space_percent)

        required_size = round(max(required_size, min_free_space_percent * 0.01 * total_space))

    if available_space > required_size:
        log.info('APIC: enough free space available: %s', available_space)
        return True

    log.warning('APIC: not enough free space, required: %s, available: %s', required_size, available_space)

    if skip_deletion:
        log.error("'skip_deletion' is set to True and there isn't enough space on the device, files cannot be deleted.")
        return False

    try:
        ls_output = device.execute(f'ls -l {destination}')
        parsed_listing = device.parse(f'ls -l {destination}', output=ls_output)
    except Exception as error:
        log.error('Unable to identify cleanup candidates: %s', error)
        return False
    if not isinstance(parsed_listing, dict):
        log.error('Unable to identify cleanup candidates')
        return False
    file_entries = parsed_listing.get('files', {})
    if not isinstance(file_entries, dict):
        log.error('Unable to identify cleanup candidates')
        return False
    return _run_disk_cleanup_with_strategy(
        device=device,
        destination=destination,
        required_size=required_size,
        file_details=file_entries,
        protected_files=protected_files,
        directory_output=ls_output,
        allow_deletion_failure=False,
        recursive=False,
        cleanup_strategy=_APIC_DISK_CLEANUP_STRATEGY,
    )
