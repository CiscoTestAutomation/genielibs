
import logging
import os

from genie.libs.sdk.apis.execute import (
    _get_directory_entries,
    _get_sorted_directory_entries,
)

log = logging.getLogger(__name__)

def free_up_disk_space(device, destination, required_size, skip_deletion,
    protected_files, compact=False, min_free_space_percent=None,
    dir_output=None, allow_deletion_failure=False):

    '''Delete files to create space on device except protected files
    Args:
        device ('Obj') : Device object
        destination ('str' or list) : Destination directory, i.e bootflash:/
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
    if not isinstance(destination, list):
        destination = [destination]
    # Get running images to protect them from deletion
    running_images = []
    log.info("Sending 'show version' to learn the current running images")
    running_image = device.api.get_running_image()
    if running_image:
        if isinstance(running_image, list):
            for image in running_image:
                running_images.append(os.path.basename(image))
        else:
            running_images.append(os.path.basename(running_image))
    else:
        log.warning("Running image could not be determined. It may be deleted.")
    
    # # convert to set for O(1) lookup
    for dest in destination:
        if isinstance(protected_files, dict):
            dest_protected_files = protected_files.get(dest, [])
        else:
            dest_protected_files = set(protected_files)

        # Parse directory output to check
        dir_out = dir_output or device.execute(f'dir {dest}')
        
        # Get available free space on device
        available_space = device.api.get_available_space(
            directory=dest, output=dir_out)
        
        log.debug('available_space: {avs}'.format(avs=available_space))
        # Check if available space is sufficient
        if min_free_space_percent:

            # Get total space
            total_space = device.api.get_total_space(
                directory=dest, output=dir_out)

            # Get current available space in %
            avail_percent = available_space / total_space * 100

            log.info("There is {avail} % of free space on the disk, which is "
                    "{compare} than the target of {target} %.".\
                    format(avail=round(avail_percent, 2), compare='less' if \
                            avail_percent < min_free_space_percent else 'greater',
                            target=min_free_space_percent))

            # get bigger of required_space or min_free_space_percent
            required_size = round(
                max(required_size, min_free_space_percent * .01 * total_space))
            
        # If there's not enough space, delete non-protected files
        if device.api.verify_enough_disk_space(required_size=required_size,
                                            directory=dest,
                                            dir_output=dir_out):
            if required_size < 0:
                log.info("Required disk space is unknown, will not delete files")
            else:
                log.info("Verified there is enough space on the device. "
                        "No files are deleted")
            continue

        if skip_deletion:
            log.error("'skip_deletion' is set to True and there isn't enough space "
                    "on the device, files cannot be deleted.")
            return False
        else:
            log.info(f"Deleting unprotected files to free up some space on {dest}")
            parsed_dir_out = device.parse(f'dir {dest}', output=dir_out)
            file_list, directory_list = _get_directory_entries(parsed_dir_out)
            directory_list = _get_sorted_directory_entries(
                parsed_dir_out, directory_list)
            # turn parsed dir output to a list of files for sorting
            # Large files are given priority when deleting
            running_image_list = []
            not_protected_file_list = []
            for file, size in file_list:
                # separate running image from other files
                if any(file in image for image in running_images):
                    running_image_list.append((file, size))
                else:
                    not_protected_file_list.append((file, size))
                    
            not_protected_file_list.sort(key=lambda x: x[1], reverse=True)
            
            # add running images to the end so they are deleted as a last resort
            file_list = not_protected_file_list + running_image_list
            log.debug(f'file_list: {file_list}')

            # Recurse into directories before deleting top-level files. The
            # platform API removes contents but leaves directory entries intact.
            log.debug(f'directory_list: {directory_list}')
            for directory_name in directory_list:
                device.api.delete_unprotected_files(
                    directory=dest,
                    protected=dest_protected_files,
                    files_to_delete=[directory_name],
                    dir_output=dir_out,
                    allow_failure=allow_deletion_failure,
                    destination=dest,
                    recursive=True,
                    stop_check=lambda: device.api.verify_enough_disk_space(
                        required_size, dest))

                if device.api.verify_enough_disk_space(
                        required_size, dest):
                    log.info(
                        "Verified there is enough space on the device "
                        "after deleting unprotected files.")
                    break
            else:
                # If directory cleanup was insufficient, delete top-level
                # files next. Running images remain last as a fallback.
                for file, _ in file_list:

                    device.api.delete_unprotected_files(
                        directory=dest,
                        protected=dest_protected_files,
                        files_to_delete=[file],
                        dir_output=dir_out,
                        allow_failure=allow_deletion_failure,
                        destination=dest)

                    if device.api.verify_enough_disk_space(
                            required_size, dest):
                        log.info(
                            "Verified there is enough space on the device "
                            "after deleting unprotected files.")
                        break
                else:
                    log.error(
                        'There is still not enough space on the device after '
                        'deleting unprotected files.')
                    return False

    log.info("Sufficient space available on all members")
    return True
