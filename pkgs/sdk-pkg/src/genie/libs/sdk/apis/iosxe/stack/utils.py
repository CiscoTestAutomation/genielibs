import logging

from genie.libs.sdk.apis.execute import _free_up_disk_space_with_strategy
from genie.libs.sdk.apis.iosxe.utils import _IOSXE_DISK_CLEANUP_STRATEGY


log = logging.getLogger(__name__)


def free_up_disk_space(device, destination, required_size, skip_deletion,
    protected_files, compact=False, min_free_space_percent=None,
    dir_output=None, allow_deletion_failure=False):
    """Delete unprotected files on every IOS-XE stack destination.

    Stack-specific handling is limited to selecting the per-member destination,
    protection list, and optional captured directory output. The cleanup policy
    and orchestration live in the shared implementation.

    Args:
        device ('Obj'): Device object.
        destination ('str' or list): Destination(s), for example bootflash:/.
        required_size ('int'): Required free space in bytes.
        skip_deletion ('bool'): Only perform checks when True.
        protected_files ('list' or dict): Global or per-destination protection
            rules.
        compact ('bool'): Apply compact-image size estimation.
        min_free_space_percent ('int'): Minimum acceptable free-space percent.
        dir_output ('str' or dict): Captured directory output, optionally keyed
            by destination.
        allow_deletion_failure ('bool'): Ignore individual deletion failures.

    Returns:
        bool: True only when every destination has sufficient verified space.
    """
    destinations = destination if isinstance(destination, list) else [destination]

    for member_destination in destinations:
        if isinstance(protected_files, dict):
            member_protected_files = protected_files.get(member_destination, [])
        else:
            member_protected_files = protected_files

        if isinstance(dir_output, dict):
            member_dir_output = dir_output.get(member_destination)
        else:
            member_dir_output = dir_output

        if not _free_up_disk_space_with_strategy(
                device=device,
                destination=member_destination,
                required_size=required_size,
                skip_deletion=skip_deletion,
                protected_files=member_protected_files,
                compact=compact,
                min_free_space_percent=min_free_space_percent,
                dir_output=member_dir_output,
                allow_deletion_failure=allow_deletion_failure,
                recursive=True,
                cleanup_strategy=_IOSXE_DISK_CLEANUP_STRATEGY):
            return False

    log.info('Sufficient space available on all members')
    return True
