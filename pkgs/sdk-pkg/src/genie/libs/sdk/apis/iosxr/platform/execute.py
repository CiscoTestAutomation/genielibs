'''IOSXR execute functions for platform'''

# Python
import logging
import time

# pyATS
from pyats.utils.fileutils import FileUtils

# Genie
from genie.libs.sdk.apis.execute import (
    _get_directory_file_details,
    _get_disk_cleanup_operation_timeout,
    _get_entry_type,
    _normalize_disk_cleanup_candidates,
)
from genie.utils.timeout import Timeout
from genie.harness.utils import connect_device
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Logger
log = logging.getLogger(__name__)


def delete_unprotected_files(device, directory, protected,
                             files_to_delete=None, dir_output=None,
                             allow_failure=False, destination=None,
                             deadline=None):
    """Delete verified regular files from an IOS-XR filesystem.

    Args:
        device ('obj'): Device object.
        directory ('str'): Directory in which to delete files.
        protected ('str' or 'list' or 'set'): File patterns that must not be
            deleted.
        files_to_delete ('list' or 'tuple' or 'set'): Optional subset of files
            to delete.
        dir_output ('str'): Optional captured output of the 'dir' command.
        allow_failure ('bool'): Ignore individual deletion failures.
        destination ('str'): Destination directory, such as harddisk:.
        deadline ('float'): Optional monotonic cleanup deadline.

    Returns:
        bool or None: True when the cleanup deadline is reached; otherwise
            None.
    """
    if deadline is not None and time.monotonic() >= deadline:
        return True

    if isinstance(protected, str):
        protected_files = {protected}
    elif isinstance(protected, (list, set)):
        protected_files = set(protected)
    else:
        raise TypeError("'protected' must be a string, list, or set")

    try:
        parsed_dir_output = device.parse(
            f'dir {directory}', output=dir_output)
    except Exception as error:
        log.error(
            'Unable to parse the IOS-XR directory listing; no files will be '
            'deleted: %s', error)
        return None

    file_details = _get_directory_file_details(parsed_dir_output)
    if file_details is None:
        log.error(
            'Unable to identify safe IOS-XR cleanup candidates; no files '
            'will be deleted')
        return None

    candidates = _normalize_disk_cleanup_candidates(
        file_details=file_details,
        protected_files=protected_files,
        classify_entry=_get_entry_type,
    )
    safe_files = {
        candidate.path for candidate in candidates
        if not candidate.is_protected
    }

    if files_to_delete is None:
        requested_files = [
            candidate.path for candidate in candidates
            if not candidate.is_protected
        ]
    elif isinstance(files_to_delete, set):
        requested_files = sorted(files_to_delete, key=str)
    elif isinstance(files_to_delete, (list, tuple)):
        requested_files = files_to_delete
    else:
        log.error(
            "'files_to_delete' must be a list, tuple, or set; no files will "
            'be deleted')
        return None

    selected_files = []
    selected_file_set = set()
    for file_name in requested_files:
        if not isinstance(file_name, str):
            log.warning(
                'Skipping malformed IOS-XR cleanup file name: %r',
                file_name)
            continue
        if file_name in safe_files and file_name not in selected_file_set:
            selected_files.append(file_name)
            selected_file_set.add(file_name)

    if not selected_files:
        log.info('There are no safe unprotected IOS-XR files to delete')
        return None

    log.info(
        'The following files will be deleted:\n%s',
        '\n'.join(selected_files))

    file_utils = FileUtils.from_device(device)
    error_messages = []
    for file_name in selected_files:
        if deadline is not None and time.monotonic() >= deadline:
            return True

        target = f'{destination}{file_name}' if destination else file_name
        log.info('Deleting the unprotected file "%s"', file_name)
        try:
            delete_kwargs = {'device': device}
            if deadline is not None:
                delete_kwargs['timeout_seconds'] = (
                    _get_disk_cleanup_operation_timeout(deadline))
            file_utils.deletefile(target, **delete_kwargs)
        except Exception as error:
            if allow_failure:
                log.info(
                    'Failed to delete file "%s" but ignoring the failure '
                    'because allow_failure=True.', file_name)
                continue
            error_messages.append(
                f'Failed to delete file "{file_name}" due to: {error}')

    if error_messages:
        raise Exception('\n'.join(error_messages))


def execute_install_pie(device, image_dir, image, server=None,
    prompt_level="none", synchronous=True, install_timeout=600, _install=True):

    ''' Installs and activates given IOSXR pie on device
        Args:
            device (`obj`): Device object
            image_dir (`str`): Directory where pie file is located in
            image (`str`): Pie file name
            server(`str`): Hostname or IP address of server to use for install command
                           Default None (Optional - uses testbed YAML reverse lookup for protocol server)
            prompt_level(`str`): Prompt-level argument for install command
                                 Default 'none' (Optional)
            synchronous (`bool`): Synchronous option for install command
                                  Default True (Optional)
            install_timeout (`int`): Maximum time required for install command to complete
                                     Default 600 seconds (Optional)

            _install (`bool`): True to install, False to uninstall.
                Not meant to be changed manually.

        Raises:
            Exception
    '''

    # Verify prompt_level type is correct
    assert prompt_level in ['none', 'all']

    # Get protocol and address from testbed YAML
    protocol = 'tftp'
    if not server:
        if not hasattr(device.testbed, 'servers'):
            raise Exception("Server not provided and testbed YAML is missing "
                            "servers block section")
        else:
            if not device.testbed.servers.get(protocol, {}).get('address', {}):
                raise Exception("Unable to find valid {} server within testbed "
                                "YAML servers block".format(protocol))
            server = device.testbed.servers.get(protocol, {}).address

    # Build 'install' command
    if _install:
        cmd = "install add source {protocol}://{server}/{image_dir} {image} activate".\
                format(protocol=protocol, server=server, image_dir=image_dir,
                        image=image)
    else:
        cmd = "install deactivate {image}".format(image=image)

    if prompt_level:
        cmd += " prompt-level {}".format(prompt_level)

    if synchronous:
        cmd += " synchronous"
    elif not synchronous:
        cmd += " asynchronous"

    # Execute command
    try:
        device.admin_execute(cmd, timeout=install_timeout)
    except Exception as e:
        log.error(str(e))
        raise Exception("Error while executing install command for pie {} "
                        "on device {}".format(image, device.name))

    if _install:
        log.info("Installed and activated pie {} on device {}".\
                format(image, device.name))
    else:
        log.info("Deactivated pie {} on device {}".format(image, device.name))


def execute_deactivate_pie(device, image, server=None, prompt_level="none",
    synchronous=True, install_timeout=600):

    ''' De-activates given IOSXR pie on device
        Args:
            device (`obj`): Device object
            image (`str`): Pie file name
            server(`str`): Hostname or IP address of server to use for install command
                           Default None (Optional - uses testbed YAML reverse lookup for protocol server)
            prompt_level(`str`): Prompt-level argument for install command
                                 Default 'none' (Optional)
            synchronous (`bool`): Synchronous option for install command
                                  Default True (Optional)
            install_timeout (`int`): Maximum time required for install command to complete
                                     Default 600 seconds (Optional)

        Raises:
            Exception
    '''

    execute_install_pie(device, None, image, server, prompt_level,
        synchronous, install_timeout, _install=False)


def execute_remove_inactive_pies(device, remove_timeout=300):

    ''' Removes given IOSXR pie on device
        Args:
            device (`obj`): Device object
            remove_timeout (`str`): Maximum time to execute command
                                    Default 300 seconds (Optional)
        Raises:
            Exception
    '''

    log.info("Removing inactive pies on device {}".format(device.name))

    # Execute command to remove pie if uninstall specified
    try:
        device.admin_execute("install remove inactive", timeout=remove_timeout)
    except Exception as e:
        log.error(str(e))
        raise Exception("Error while removing inactive pies on device {}".\
                        format(device.name))
    else:
        log.info("Successfully removed inactive pies on device {}".format(device.name))


def execute_set_config_register(device, config_register, timeout=60):
    '''Set config register to load image in boot variable
        Args:
            device ('obj'): Device object
            config_reg ('str'): Hexadecimal value to set the config register to
            timeout ('int'): Max time to set config-register in seconds
                             Default 60 seconds (Optional)
    '''

    try:
        device.admin_execute("config-register {}".format(config_register),
                             timeout=timeout)
    except Exception as e:
        log.error(str(e))
        raise Exception("Failed to set config register to '{}' on device {}".\
                        format(config_register, device.name))
    else:
        log.info("Set config-register to '{}' on device".\
                format(config_register, device.name))
