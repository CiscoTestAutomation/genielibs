
import logging
import os

from genie.libs.sdk.apis.iosxe.stack.utils import free_up_disk_space as multi_rp_free_up_disk_space

log = logging.getLogger(__name__)

def free_up_disk_space(device, destination, required_size, skip_deletion,
    protected_files, compact=False, min_free_space_percent=None,
    dir_output=None, allow_deletion_failure=False):

    '''Delete files to create space on device except protected files
    Args:
        device ('Obj') : Device object
        destination ('str or list') : Destination , i.e bootflash:/
        required_size ('int') : Check if enough space to fit given size in bytes.
                                If this number is negative it will be assumed
                                the required size is not available.
        skip_deletion ('bool') : Only performs checks, no deletion
        protected_files ('list or dict') : List of file patterns that wont be deleted
                          or dictionary wiht the key being the destination and value being the 
                          List of file patterns that wont be deleted that not being deleted for 
                          that destination
        compact ('bool'): Compact option for n9k, used for size estimation,
                          default False
        min_free_space_percent ('int'): Minimum acceptable free disk space %.
                                        Optional,
        dir_output ('str'): Output of 'dir' command
                            if not provided, executes the cmd on device
        allow_deletion_failure (bool, optional): Allow the deletion of a file to silently fail. Defaults to False
    Returns:
         True if there is enough space after the operation, False otherwise
    '''
    return multi_rp_free_up_disk_space(device, destination, required_size, skip_deletion,
                                protected_files, compact=False, min_free_space_percent=None,
                                dir_output=None, allow_deletion_failure=False)