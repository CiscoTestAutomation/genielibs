from genie.libs.sdk.apis.iosxe.stack.utils import (
    free_up_disk_space as multi_rp_free_up_disk_space,
)


def free_up_disk_space(device, destination, required_size, skip_deletion,
    protected_files, compact=False, min_free_space_percent=None,
    dir_output=None, allow_deletion_failure=False):
    """Forward disk cleanup to the IOS-XE multi-RP implementation.

    Args:
        device ('obj'): Device object.
        destination ('str' or list): Destination or member destinations.
        required_size ('int'): Required free space in bytes.
        skip_deletion ('bool'): Only perform checks when True.
        protected_files ('list' or dict): Global or per-destination protection
            rules.
        compact ('bool'): Apply compact-image size estimation.
        min_free_space_percent ('int'): Minimum acceptable free-space percent.
        dir_output ('str' or dict): Captured directory output, optionally
            keyed by destination.
        allow_deletion_failure ('bool'): Ignore individual deletion failures.

    Returns:
        bool: Result from the multi-RP cleanup implementation.
    """
    return multi_rp_free_up_disk_space(
        device=device,
        destination=destination,
        required_size=required_size,
        skip_deletion=skip_deletion,
        protected_files=protected_files,
        compact=compact,
        min_free_space_percent=min_free_space_percent,
        dir_output=dir_output,
        allow_deletion_failure=allow_deletion_failure,
    )
