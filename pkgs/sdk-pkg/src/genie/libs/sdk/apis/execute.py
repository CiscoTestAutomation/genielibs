'''Common execute functions'''

# Python
import re
import os
import time
import logging
import json
import functools
import signal
from dataclasses import dataclass
from typing import Callable

# pyATS
from pyats.async_ import pcall

# Genie
from genie.utils.timeout import Timeout
from genie.libs.sdk.apis.utils import get_power_cycler_configs
from genie.libs.sdk.powercycler.base import PowerCycler

# Unicon
from unicon.eal.dialogs import Statement, Dialog

# Logger
log = logging.getLogger(__name__)

POWER_CYCLER_STATE_CHANGE_TIMEOUT = 600

# Disk cleanup is intentionally bounded. These limits are internal so the
# public free_up_disk_space() API remains backward compatible.
DISK_CLEANUP_BATCH_SIZE = 10
DISK_CLEANUP_MAX_CANDIDATES = 1000
DISK_CLEANUP_TIMEOUT = 300

# These files and directories are needed to boot, restore configuration, or
# operate in package mode. Callers can add platform/job-specific entries
# through protected_files, but must not be able to weaken these defaults.
DISK_CLEANUP_PROTECTED_FILES = frozenset({
    '.installer',
    '.prst_sync',
    '.rollback_timer',
    'SHARED-IOX',
    'config.text',
    'lost+found',
    'nvram_config',
    'nvram_config_bkup',
    'packages.conf',
    'private-config.text',
    'startup-config',
    'vlan.dat',
})


def _get_disk_cleanup_operation_timeout(deadline, timeout=DISK_CLEANUP_TIMEOUT):
    """Limit an operation timeout to the remaining cleanup deadline."""
    if deadline is None:
        return timeout
    return max(1, min(timeout, int(deadline - time.monotonic()) + 1))


@dataclass(frozen=True)
class _DiskCleanupCandidate:
    """A type-aware disk cleanup candidate."""

    path: str
    size: int
    is_directory: bool
    is_protected: bool


@dataclass(frozen=True)
class _DiskCleanupStrategy:
    """Platform-specific callbacks for the shared disk cleanup flow."""

    classify_entry: Callable[..., object]
    delete_batch: Callable[..., object]
    get_available_space: Callable[..., object]
    supports_directories: bool = False


def execute_clear_line(device, alias: str = 'cli', disconnect_termserver: bool = True):
    ''' Executes 'clear line <port>' to clear busy console port on device
        Args:
            device ('obj'): Device object
            alias ('str'): Alias used for console port connection
                           Default: 'cli'
            disconnect_termserver ('bool'): Boolean to indicate if the
                               termserver connection should be closed.
                               Default: True

        Returns:
            None
    '''

    # Init
    connected = set()

    # Find device's terminal server information
    terminal_server = getattr(device, 'peripherals', {}).get('terminal_server', {})
    if not terminal_server:
        raise Exception("Terminal server information is not provided in the "
                        "testbed YAML file for device '{}'\nUnable to clear "
                        "the console port line".format(device.name))

    for server, ports in terminal_server.items():
        # Fix ports type if incorrect from user
        if isinstance(ports, (str, int)):
            ports = [ports, ]

        if not isinstance(ports, list):
            raise Exception(f"The port/s of terminal_server '{server}' are not in list, string or an integer format.")

        # Connect to terminal server
        term_serv_dev = device.testbed.devices[server]
        if term_serv_dev not in connected:
            term_serv_dev.connect(init_exec_commands=[], init_config_commands=[])
            connected.add(term_serv_dev)

        # Execute clear line on port
        for port in ports:
            try:
                term_serv_dev.execute("clear line {}".format(port))
            except Exception as e:
                log.error("Failed to clear line '{}'\n{}".format(port, str(e)))
                raise
            else:
                log.info("Executed 'clear line {}' on terminal server '{}'".\
                         format(port, term_serv_dev.name))

    if disconnect_termserver:
        # Disconnect from terminal server
        log.info("Disconnecting from terminal server...")
        for item in connected:
            item.destroy()

    # Disconnect from actual device now that line has been successfully cleared
    log.info("Disconnecting from {} as line was cleared successfully".\
             format(device.name))
    device.disconnect(alias=alias)


def execute_power_off_device(device):
    '''Power off a device

    Args:
        device ('obj'): Device object

    Raises:
        Exception if power off fails

    Returns:
        None
    '''
    _change_power_cycler_configs_state(
        device,
        get_power_cycler_configs(device),
        'off')


def execute_power_on_device(device):
    '''Power on a device

    Args:
        device ('obj'): Device object

    Raises:
        Exception if power on fails

    Returns:
        None
    '''

    _change_power_cycler_configs_state(
        device,
        get_power_cycler_configs(device),
        'on')


def _format_powercycler_target(powercycler, outlets):
    """Return a compact target description for powercycler errors."""
    return "host={!r}, type={!r}, outlets={!r}".format(
        powercycler.get('host') if isinstance(powercycler, dict)
        else getattr(powercycler, 'host', None),
        powercycler.get('type') if isinstance(powercycler, dict)
        else getattr(powercycler, 'type', None),
        outlets)


def _disconnect_powercycler(powercycler):
    """Disconnect a powercycler and its proxy, if any."""
    try:
        powercycler.disconnect()
    except Exception as e:
        log.debug(f"Failed to disconnect from powercycler. {e}")

    proxy_dev = getattr(powercycler, 'proxy_dev', None)
    if proxy_dev and proxy_dev.connected:
        try:
            proxy_dev.disconnect()
        except Exception as e:
            log.debug(f"Failed to disconnect from powercycler proxy. {e}")


def _build_powercycler(power_cycler, holder=None):
    """Build a powercycler and keep a cleanup reference during init."""
    if (getattr(PowerCycler, '__module__', None) ==
            'genie.libs.sdk.powercycler.base' and
            getattr(PowerCycler, '__name__', None) == 'PowerCycler'):
        pc = PowerCycler.__new__(PowerCycler, **power_cycler)
        if holder is not None:
            holder['powercycler'] = pc
        pc.__init__(**power_cycler)
        return pc
    return PowerCycler(**power_cycler)


def _change_power_cycler_config_state(
        device_name, power_cycler, outlets, state, timeout=None):
    """Build one powercycler object and change its state."""
    pc = None
    holder = {}
    previous_alarm_handler = None
    previous_alarm_timer = None
    alarm_set = False

    def timeout_handler(signum, frame):
        raise TimeoutError(
            "timed out after {} seconds".format(timeout))

    try:
        if timeout:
            try:
                previous_alarm_handler = signal.getsignal(signal.SIGALRM)
                previous_alarm_timer = signal.getitimer(signal.ITIMER_REAL)
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.setitimer(signal.ITIMER_REAL, timeout)
                alarm_set = True
            except (AttributeError, ValueError):
                log.debug("Powercycler worker timeout is only supported in "
                          "the main thread")
        pc = _build_powercycler(power_cycler, holder)
        if state == 'on':
            pc.on(*outlets)
        elif state == 'off':
            pc.off(*outlets)
        else:
            raise Exception("Invalid state provided for powercycler\n"
                            "Acceptable states are 'on' or 'off'")
    except Exception as e:
        return "{} failed: {!r}".format(
            _format_powercycler_target(power_cycler, outlets), e)
    finally:
        if alarm_set:
            signal.setitimer(signal.ITIMER_REAL, *previous_alarm_timer)
            signal.signal(signal.SIGALRM, previous_alarm_handler)
        pc = pc or holder.get('powercycler')
        if pc is not None:
            _disconnect_powercycler(pc)

    log.debug(f"Powercycled device '{device_name}' to '{state}' state")


def _change_power_cycler_configs_state(device, pcs, state, timeout=None):
    """Change all power cyclers to the requested state.

    A single powercycler keeps the historical synchronous behavior. Multiple
    configured powercyclers are handled with pyATS pcall so each target PDU is
    built, connected, power-cycled, and disconnected in its own worker process.
    Timeout handling is passed into each worker instead of pcall so worker
    cleanup can run before the worker returns.
    """
    if timeout is None:
        timeout = POWER_CYCLER_STATE_CHANGE_TIMEOUT

    if len(pcs) <= 1:
        errors = [
            _change_power_cycler_config_state(
                device.name, power_cycler, outlets, state)
            for power_cycler, outlets in pcs
        ]
    else:
        ikwargs = [
            {
                'device_name': device.name,
                'power_cycler': power_cycler,
                'outlets': outlets,
                'state': state,
                'timeout': timeout,
            }
            for power_cycler, outlets in pcs
        ]

        errors = pcall(
            _change_power_cycler_config_state,
            ikwargs=ikwargs)

    errors = [error for error in errors if error]
    if errors:
        raise Exception("Failed to powercycle device {}:\n{}".format(
            state, "\n".join(errors)))


def execute_power_cycle_device(device, delay=30, destroy=True):
    ''' Powercycle a device

    Args:
        device ('obj'): Device object

        delay (int, optional): Time in seconds to sleep between turning the
            device off and then back on. Defaults to 30.

        destroy (bool): Determine if the device connection object should be
            destroyed. Defaults to True

    Raises:
        Exception if powercycling fails.

    Returns:
        None
    '''
    # Destroy device object
    if destroy:
        try:
            device.destroy_all()
        except Exception as e:
            log.warning('could not destroy the device object continue with powercycle.')


    device.api.execute_power_off_device()
    log.info(f"Waiting '{delay}' seconds before powercycling device on")
    time.sleep(delay)
    device.api.execute_power_on_device()


def change_power_cycler_state(device, powercycler, state, outlets):
    ''' Turn on the power cycler
        Args:
            device ('obj'): Device object
            powercycler ('obj'): Powercycler object
            state ('str'): Power cycler state on/off
            outlets ('str'): Power cycler outlets
        Returns:
            None
    '''

    if state not in ['on', 'off']:
        raise Exception("Invalid state provided for powercycler\n"
                        "Acceptable states are 'on' or 'off'")
    if state == 'on':
        powercycler.on(*outlets)
    elif state == 'off':
        powercycler.off(*outlets)

    # Disconnect from powercycler.
    _disconnect_powercycler(powercycler)


def _get_directory_file_details(parsed_dir_output):
    """Return file details from supported directory parser shapes."""
    if not isinstance(parsed_dir_output, dict):
        return None

    directory_data = parsed_dir_output.get('dir', {})
    if isinstance(directory_data, dict):
        # IOS/IOS-XE shape:
        # {'dir': {'dir': 'bootflash:/', 'bootflash:/': {'files': {...}}}}
        directory_path = directory_data.get('dir')
        directory_details = directory_data.get(directory_path, {})
        if isinstance(directory_details, dict):
            file_details = directory_details.get('files')
            if isinstance(file_details, dict):
                return file_details

        # IOS-XR shape:
        # {'dir': {'dir_name': 'harddisk:', 'files': {...}}}
        file_details = directory_data.get('files')
        if isinstance(file_details, dict):
            return file_details

    # Some parsers, including NX-OS, expose a top-level files mapping.
    file_details = parsed_dir_output.get('files')
    return file_details if isinstance(file_details, dict) else None


def _get_entry_type(entry_name, file_details=None, use_name_fallback=False):
    """Return ``file``, ``directory``, or None for an unknown entry type.

    When ``use_name_fallback`` is True, entries without permission metadata
    use the trailing-slash directory convention.
    """
    if not isinstance(entry_name, str) or not isinstance(file_details, dict):
        return None

    entry_details = file_details.get(entry_name)
    if not isinstance(entry_details, dict):
        return None

    permissions = str(entry_details.get('permissions') or entry_details.get('permission') or '')
    if permissions.startswith('-'):
        return 'file'
    if permissions.startswith('d'):
        return 'directory'
    if permissions or not use_name_fallback:
        return None

    # NX-OS dir output does not include permissions and identifies
    # directories with a trailing slash.
    return 'directory' if entry_name.endswith('/') else 'file'


def _is_directory_entry(entry_name, file_details=None):
    """Return whether a parsed dir entry represents a directory."""
    return _get_entry_type(entry_name, file_details) == 'directory'


def _get_entry_size(entry_name, file_details=None):
    """Return a parsed dir entry size as an int."""
    if not isinstance(file_details, dict):
        return 0
    entry_details = file_details.get(entry_name)
    if not isinstance(entry_details, dict):
        return 0
    try:
        return int(entry_details.get('size', 0) or 0)
    except (TypeError, ValueError):
        return 0


def _matches_protected_file(path, protected_files):
    """Return whether *path* matches an existing protection rule."""
    basename = os.path.basename(str(path).rstrip('/'))
    for pattern in protected_files:
        # Existing protection patterns containing an opening parenthesis are
        # treated as regular expressions.
        if '(' in pattern:
            regexp = re.compile(pattern)
            if regexp.match(path) or regexp.match(basename):
                return True
        elif pattern in (path, basename):
            return True
    return False


def _build_disk_cleanup_candidates(candidate_entries, protected_files=None):
    """Build deterministic, type-aware cleanup candidates.

    Args:
        candidate_entries: Iterable of ``(path, size, is_directory)`` values.
        protected_files: Existing exact-name or regular-expression rules.

    Regular files are preferred to directories, and larger entries are
    preferred within each type.  Name ordering provides a stable tie breaker.
    """
    if isinstance(protected_files, str):
        protected_patterns = {protected_files}
    else:
        protected_patterns = set(protected_files or [])
    protected_patterns.update(DISK_CLEANUP_PROTECTED_FILES)
    candidates = []

    for entry in candidate_entries:
        if not isinstance(entry, (list, tuple)) or len(entry) != 3:
            log.warning('Skipping malformed disk cleanup candidate: %r', entry)
            continue

        path, size, is_directory = entry
        if (not isinstance(path, str) or not path or
                not isinstance(is_directory, bool)):
            log.warning('Skipping malformed disk cleanup candidate: %r', entry)
            continue
        if isinstance(size, bool):
            log.warning('Skipping malformed disk cleanup candidate: %r', entry)
            continue
        try:
            candidate_size = int(size)
        except (TypeError, ValueError):
            log.warning('Skipping malformed disk cleanup candidate: %r', entry)
            continue
        if candidate_size < 0:
            log.warning('Skipping malformed disk cleanup candidate: %r', entry)
            continue

        candidates.append(_DiskCleanupCandidate(
            path=path,
            size=candidate_size,
            is_directory=bool(is_directory),
            is_protected=_matches_protected_file(path, protected_patterns),
        ))

    return sorted(
        candidates,
        key=lambda candidate: (
            candidate.is_protected,
            candidate.is_directory,
            -candidate.size,
            candidate.path,
        ),
    )


def _normalize_disk_cleanup_candidates(file_details, protected_files,
                                       classify_entry,
                                       include_directories=False):
    """Validate parsed entries and build deterministic cleanup candidates."""
    if not isinstance(file_details, dict):
        log.error('Unable to identify safe cleanup candidates')
        return []

    candidate_entries = []
    for path, entry_details in file_details.items():
        if not isinstance(entry_details, dict):
            log.warning('Skipping cleanup candidate %r because its parsed details are malformed', path)
            continue

        try:
            entry_type = classify_entry(path, file_details)
        except Exception as error:
            log.warning('Skipping cleanup candidate %r because its parsed file type is invalid: %s', path, error)
            continue

        if entry_type == 'directory':
            if not include_directories:
                continue
            is_directory = True
        elif entry_type == 'file':
            is_directory = False
        else:
            log.warning('Skipping cleanup candidate %r because its parsed file type is unknown', path)
            continue

        raw_entry_size = entry_details.get('size')
        if isinstance(raw_entry_size, bool):
            log.warning('Skipping cleanup candidate %r because its parsed size is unknown', path)
            continue
        try:
            entry_size = int(raw_entry_size)
        except (TypeError, ValueError):
            log.warning('Skipping cleanup candidate %r because its parsed size is unknown', path)
            continue
        if entry_size < 0:
            log.warning('Skipping cleanup candidate %r because its parsed size is invalid', path)
            continue
        candidate_entries.append((path, entry_size, is_directory))

    return _build_disk_cleanup_candidates(candidate_entries, protected_files=protected_files)


def _run_disk_cleanup(candidates, required_size, delete_batch,
                      get_available_space,
                      batch_size=DISK_CLEANUP_BATCH_SIZE,
                      max_candidates=DISK_CLEANUP_MAX_CANDIDATES,
                      cleanup_timeout=DISK_CLEANUP_TIMEOUT):
    """Delete bounded candidate batches and verify space between batches.

    ``delete_batch`` receives a list of candidates and the monotonic cleanup
    deadline.  ``get_available_space`` must use a concise platform query when
    one is available.  Unknown post-delete space stops cleanup immediately so
    another destructive batch is never chosen from unverified state.
    """
    if batch_size < 1 or max_candidates < 1 or cleanup_timeout <= 0:
        log.error('Disk cleanup limits must be positive')
        return False

    deletable_candidates = [candidate for candidate in candidates if not candidate.is_protected]
    if len(deletable_candidates) > max_candidates:
        log.warning('Limiting disk cleanup from %s to %s candidates', len(deletable_candidates), max_candidates)
        deletable_candidates = deletable_candidates[:max_candidates]

    if not deletable_candidates:
        log.error('There are no safe unprotected files to delete')
        return False

    deadline = time.monotonic() + cleanup_timeout
    candidate_index = 0
    while candidate_index < len(deletable_candidates):
        if time.monotonic() >= deadline:
            log.error('Disk cleanup deadline expired before enough space could be verified')
            return False

        # Recursive directory size is not a reliable estimate, so process one
        # directory per verification. Regular files are deleted in batches.
        current_candidate = deletable_candidates[candidate_index]
        if current_candidate.is_directory:
            candidate_batch = [current_candidate]
        else:
            batch_end = candidate_index
            while batch_end < len(deletable_candidates):
                if batch_end - candidate_index >= batch_size:
                    break
                if deletable_candidates[batch_end].is_directory:
                    break
                batch_end += 1
            candidate_batch = deletable_candidates[candidate_index:batch_end]

        safety_limit_reached = delete_batch(candidate_batch, deadline)
        candidate_index += len(candidate_batch)

        if time.monotonic() >= deadline:
            log.error('Disk cleanup deadline expired during deletion')
            return False

        try:
            available_space = get_available_space()
        except Exception as error:
            log.error('Available-space verification failed after deletion: %s', error)
            return False
        if available_space is None:
            log.error('Available space is unknown after deletion; stopping cleanup without selecting another batch')
            return False

        log.info('Space required: %s bytes,\nSpace available : %s bytes',
                 required_size if required_size > -1 else 'Unknown',
                 available_space)
        if available_space > int(required_size):
            log.info('Verified there is enough space on the device after deleting unprotected files.')
            return True
        if safety_limit_reached is True:
            log.error('Disk cleanup stopped at a safety limit before enough space was available')
            return False

    log.error('There is still not enough space on the device after deleting unprotected files.')
    return False


def _classify_generic_disk_cleanup_entry(entry_name, file_details):
    """Return the filesystem entry type from permission metadata."""
    return _get_entry_type(entry_name, file_details)


def _delete_generic_disk_cleanup_batch(device, destination, protected_files,
                                       candidate_batch, directory_output,
                                       allow_deletion_failure, deadline,
                                       **_kwargs):
    """Delete a batch of regular files through the platform API."""
    return device.api.delete_unprotected_files(
        directory=destination,
        protected=protected_files,
        files_to_delete=[candidate.path for candidate in candidate_batch],
        dir_output=directory_output,
        allow_failure=allow_deletion_failure,
        destination=destination,
        deadline=deadline,
    )


def _get_generic_disk_cleanup_space(device, destination):
    """Return available space through the platform cleanup-space API."""
    return device.api.get_available_space_after_cleanup(directory=destination)


_GENERIC_DISK_CLEANUP_STRATEGY = _DiskCleanupStrategy(
    classify_entry=_classify_generic_disk_cleanup_entry,
    delete_batch=_delete_generic_disk_cleanup_batch,
    get_available_space=_get_generic_disk_cleanup_space,
)


def _run_disk_cleanup_with_strategy(device, destination, required_size,
                                    file_details, protected_files,
                                    directory_output,
                                    allow_deletion_failure,
                                    recursive, cleanup_strategy):
    """Build candidates and run the shared bounded cleanup loop."""
    candidates = _normalize_disk_cleanup_candidates(
        file_details=file_details,
        protected_files=protected_files,
        classify_entry=cleanup_strategy.classify_entry,
        include_directories=(recursive and cleanup_strategy.supports_directories),
    )
    log.debug('cleanup candidates: %s', candidates)

    recursive_deletions = 0

    def delete_batch(candidate_batch, deadline):
        def stop_recursive_cleanup():
            nonlocal recursive_deletions
            recursive_deletions += 1
            candidate_limit_reached = recursive_deletions >= DISK_CLEANUP_MAX_CANDIDATES
            deadline_reached = time.monotonic() >= deadline
            return candidate_limit_reached or deadline_reached

        return cleanup_strategy.delete_batch(
            device=device,
            destination=destination,
            protected_files=protected_files,
            candidate_batch=candidate_batch,
            directory_output=directory_output,
            allow_deletion_failure=allow_deletion_failure,
            deadline=deadline,
            stop_check=stop_recursive_cleanup,
        )

    return _run_disk_cleanup(
        candidates=candidates,
        required_size=required_size,
        delete_batch=delete_batch,
        get_available_space=lambda: cleanup_strategy.get_available_space(
            device, destination),
    )


def _free_up_disk_space_with_strategy(device, destination, required_size, skip_deletion,
    protected_files, compact=False, min_free_space_percent=None,
    dir_output=None, allow_deletion_failure=False, recursive=False,
    cleanup_strategy=_GENERIC_DISK_CLEANUP_STRATEGY):
    """Delete safe candidates until the required free space is available.

    Args:
        device ('obj'): Device object.
        destination ('str'): Destination directory, such as bootflash:/.
        required_size ('int'): Required free space in bytes.
        skip_deletion ('bool'): Only perform the space check when True.
        protected_files ('list'): File names or patterns that must not be
            deleted.
        compact ('bool'): Apply compact-image size estimation.
        min_free_space_percent ('int'): Minimum acceptable free-space percent.
        dir_output ('str'): Optional captured output of the 'dir' command.
        allow_deletion_failure ('bool'): Ignore individual deletion failures.
        recursive ('bool'): Request recursive cleanup after regular files when
            the platform strategy supports directories.
        cleanup_strategy (_DiskCleanupStrategy): Platform callbacks for entry
            classification, deletion, and post-delete verification.

    Returns:
        bool: True when enough space is verified, otherwise False.
    """
    # A compacted Nexus 9000 image is typically 36-48% of the original size.
    # Use 60% as a conservative estimate.
    if compact:
        required_size *= 0.6

    # Capture the directory output once.  Candidate selection and the initial
    # space calculation must use the same snapshot.
    directory_output = dir_output if dir_output is not None else device.execute(f'dir {destination}')

    try:
        available_space = device.api.get_available_space(directory=destination, output=directory_output)
    except Exception as error:
        log.error('Unable to verify available space from the directory listing: %s; no files will be deleted', error)
        return False

    log.debug('Available space: %s', available_space)
    if available_space is None:
        log.error('Unable to verify available space from the directory listing; no files will be deleted')
        return False

    if min_free_space_percent:
        try:
            total_space = device.api.get_total_space(directory=destination, output=directory_output)
        except Exception as error:
            log.error('Unable to verify total disk space: %s; no files will be deleted', error)
            return False

        if total_space is None or total_space <= 0:
            log.error('Unable to verify total disk space; no files will be deleted')
            return False

        available_percent = available_space / total_space * 100
        comparison = 'less' if available_percent < min_free_space_percent else 'greater'
        log.info(
            'There is %s %% of free space on the disk, which is %s than the '
            'target of %s %%.',
            round(available_percent, 2), comparison, min_free_space_percent)

        # Use the larger of the required size and minimum free-space target.
        required_size = round(max(required_size, min_free_space_percent * 0.01 * total_space))

    # Reuse the initial parsed free-space value instead of reparsing or
    # executing another full directory listing.
    if available_space > int(required_size):
        if required_size < 0:
            log.info("Required disk space is unknown, will not delete files")
        else:
            log.info("Verified there is enough space on the device. "
                     "No files are deleted")
        return True

    if skip_deletion:
        log.error("'skip_deletion' is set to True and there isn't enough space "
                  "on the device, files cannot be deleted.")
        return False
    else:
        log.info("Deleting unprotected files to free up some space")

        running_images = []
        log.info("Sending 'show version' to learn the current running images")
        running_image = device.api.get_running_image()
        if running_image:
            if isinstance(running_image, list):
                for image in running_image:
                    running_images.append(os.path.basename(str(image).rsplit(':', 1)[-1]))
            else:
                running_images.append(os.path.basename(str(running_image).rsplit(':', 1)[-1]))
        else:
            log.warning('Running image could not be determined. Caller and '
                        'default protection rules will still be enforced.')

        # Running images are never last-resort deletion candidates.  Add them
        # to the same protection set used for candidate selection and by the
        # platform deletion implementation as a second safety check.
        if isinstance(protected_files, str):
            protected_files = {protected_files}
        else:
            protected_files = set(protected_files or [])
        protected_files.update(DISK_CLEANUP_PROTECTED_FILES)
        protected_files.update(running_images)
        try:
            parsed_directory_output = device.parse(f'dir {destination}', output=directory_output)
        except Exception as error:
            log.error(
                'Unable to identify safe cleanup candidates: %s', error)
            return False
        file_details = _get_directory_file_details(parsed_directory_output)
        if file_details is None:
            log.error('Unable to identify safe cleanup candidates')
            return False

        return _run_disk_cleanup_with_strategy(
            device=device,
            destination=destination,
            required_size=required_size,
            file_details=file_details,
            protected_files=protected_files,
            directory_output=directory_output,
            allow_deletion_failure=allow_deletion_failure,
            recursive=recursive,
            cleanup_strategy=cleanup_strategy,
        )


def _free_up_disk_space(device, destination, required_size, skip_deletion,
    protected_files, compact=False, min_free_space_percent=None,
    dir_output=None, allow_deletion_failure=False, recursive=False):
    """Delete safe candidates until the required free space is available.

    Args:
        device ('obj'): Device object.
        destination ('str'): Destination directory, such as bootflash:/.
        required_size ('int'): Required free space in bytes.
        skip_deletion ('bool'): Only perform the space check when True.
        protected_files ('list'): File names or patterns that must not be
            deleted.
        compact ('bool'): Apply compact-image size estimation.
        min_free_space_percent ('int'): Minimum acceptable free-space percent.
        dir_output ('str'): Optional captured output of the 'dir' command.
        allow_deletion_failure ('bool'): Ignore individual deletion failures.
        recursive ('bool'): Request recursive cleanup after regular files when
            the platform strategy supports directories.

    Returns:
        bool: True when enough space is verified, otherwise False.
    """
    return _free_up_disk_space_with_strategy(
        device=device,
        destination=destination,
        required_size=required_size,
        skip_deletion=skip_deletion,
        protected_files=protected_files,
        compact=compact,
        min_free_space_percent=min_free_space_percent,
        dir_output=dir_output,
        allow_deletion_failure=allow_deletion_failure,
        recursive=recursive,
        cleanup_strategy=_GENERIC_DISK_CLEANUP_STRATEGY,
    )


def _free_up_disk_space_for_roles(device, destination, required_size,
    skip_deletion, protected_files, compact=False,
    min_free_space_percent=None, dir_output=None,
    allow_deletion_failure=False, recursive=False,
    cleanup_strategy=_GENERIC_DISK_CLEANUP_STRATEGY):
    """Run the selected cleanup strategy on each device role."""
    free_up_result = _free_up_disk_space_with_strategy(
        device=device,
        destination=destination,
        required_size=required_size,
        skip_deletion=skip_deletion,
        protected_files=protected_files,
        compact=compact,
        min_free_space_percent=min_free_space_percent,
        dir_output=dir_output,
        allow_deletion_failure=allow_deletion_failure,
        recursive=recursive,
        cleanup_strategy=cleanup_strategy,
    )

    if not hasattr(device, 'swap_roles'):
        return free_up_result

    device.swap_roles()
    try:
        free_up_result_other = _free_up_disk_space_with_strategy(
            device=device,
            destination=destination,
            required_size=required_size,
            skip_deletion=skip_deletion,
            protected_files=protected_files,
            compact=compact,
            min_free_space_percent=min_free_space_percent,
            dir_output=dir_output,
            allow_deletion_failure=allow_deletion_failure,
            recursive=recursive,
            cleanup_strategy=cleanup_strategy,
        )
    finally:
        device.swap_roles()
    return free_up_result or free_up_result_other


@functools.wraps(_free_up_disk_space)
def free_up_disk_space(device, destination, required_size, skip_deletion,
    protected_files, compact=False, min_free_space_percent=None,
    dir_output=None, allow_deletion_failure=False, recursive=False):
    return _free_up_disk_space_for_roles(
        device=device,
        destination=destination,
        required_size=required_size,
        skip_deletion=skip_deletion,
        protected_files=protected_files,
        compact=compact,
        min_free_space_percent=min_free_space_percent,
        dir_output=dir_output,
        allow_deletion_failure=allow_deletion_failure,
        recursive=recursive,
        cleanup_strategy=_GENERIC_DISK_CLEANUP_STRATEGY,
    )


def execute_reload(device,
                   prompt_recovery=True,
                   reload_creds='default',
                   sleep_after_reload=120,
                   timeout=800,
                   reload_command='reload',
                   error_pattern=None,
                   devices=None,
                   exclude_devices=None):
    ''' Reload device
        Args:
            device ('obj'): Device object
            prompt_recovery ('bool'): Enable/Disable prompt recovery feature. default: True
            reload_creds ('str'): Credential name defined in the testbed yaml file to be used during reload. default: 'default'
            sleep_after_reload ('int'): Time to sleep after reload in seconds, default: 120
            timeout ('int'): reload timeout value, defaults 800 seconds.
            reload_command ('str'): reload command. default: 'reload'
            error_pattern ('list'): List of regex strings to check output for errors.
            devices ('list'): list of device names
            exclude_devices ('list'): excluded device list
        Usage:
            device.api.execute_reload(devices=['ce1', 'ce2', 'pe1'], error_pattern=[], sleep_after_reload=0)
    '''

    def _execute_reload(device, prompt_recovery, reload_creds, sleep_after_reload,
                        timeout, reload_command, error_pattern):
        '''
        internal function of execute_reload for pcall
        '''
        log.info("Reloading device '{d}'".format(d=device.name))

        if device.is_ha and device.type == 'iol':
            reload_command = 'redundancy reload shelf'

        try:
            if isinstance(error_pattern, list):
                device.reload(prompt_recovery=prompt_recovery,
                              reload_creds=reload_creds,
                              timeout=timeout,
                              reload_command=reload_command,
                              error_pattern=error_pattern)
            else:
                device.reload(prompt_recovery=prompt_recovery,
                              reload_creds=reload_creds,
                              timeout=timeout,
                              reload_command=reload_command)
        except Exception as e:
            log.error(f"Error while reloading device {device.name}")
            raise e

        log.info(f"Waiting '{sleep_after_reload}' seconds after reload ...")
        time.sleep(sleep_after_reload)


    if exclude_devices is None:
        exclude_devices = []

    if devices:
        device_list = [{
            'device': device.testbed.devices[dev]
        } for dev in devices if dev not in exclude_devices]
        ikwargs = device_list
        ckwargs = {
            'prompt_recovery': prompt_recovery,
            'reload_creds': reload_creds,
            'sleep_after_reload': sleep_after_reload,
            'timeout': timeout,
            'reload_command': reload_command,
            'error_pattern': error_pattern,
        }
        pcall(_execute_reload, ckwargs=ckwargs, ikwargs=ikwargs)
    else:
        _execute_reload(device=device,
                        prompt_recovery=prompt_recovery,
                        reload_creds=reload_creds,
                        sleep_after_reload=sleep_after_reload,
                        timeout=timeout,
                        reload_command=reload_command,
                        error_pattern=error_pattern)

def execute_copy_to_running_config(device, file, copy_config_timeout=60):
    ''' Copying file to running-config on device
        Args:
            device ('obj'): Device object
            file ('str'): String object to copy to device
            copy_config_timeout ('int'): Timeout for copy in seconds (default: 60)
    '''

    log.info("Copying {} to running-config on '{}'".format(file, device.name))
    try:
        output = device.copy(source=file, dest='running-config',
                             timeout=copy_config_timeout)
    except Exception as e:
        raise Exception("Failed to apply config file {} to running-config\n{}".\
                        format(file, str(e)))
    else:
        if re.search(r'^0 bytes.*', output):
            raise Exception("Config file {} not applied to "\
                            "running-config - 0 bytes was copied".\
                            format(file))


def execute_copy_to_startup_config(device, file, dest='startup-config', copy_config_timeout=60):
    ''' Copying file to startup-config on device
        Args:
            device ('obj'): Device object
            file ('str'): String object to copy to device
            dest ('str'): Target to copy to (default: startup-config)
            copy_config_timeout ('int'): Timeout for copy in seconds (default: 60)
    '''

    log.info("Copying {} to startup-config on '{}'".format(file, device.name))
    try:
        output = device.copy(source=file, dest=dest,
                             timeout=copy_config_timeout)
    except Exception as e:
        raise Exception("Failed to apply config file {} to startup-config\n{}".\
                        format(file, str(e)))
    else:
        if re.search(r'^0 bytes.*', output):
            raise Exception("Config file {} not applied to "\
                            "startup-config - 0 bytes was copied".\
                            format(file))


def execute_copy_run_to_start(device, command_timeout=300, max_time=120,
    check_interval=30, copy_vdc_all=False):
    ''' Execute copy running-config to startup-config
        Args:
            device ('obj'): Device object
            command_timeout ('int'): Copy-command timeout in seconds. Defaults
                to 300.
            max_time ('int'): Ignored compatibility argument. Retained for
                backward compatibility. Defaults to 120.
            check_interval ('int'): Ignored compatibility argument. Retained
                for backward compatibility. Defaults to 30.
            copy_vdc_all ('boolean'): Whether to copy on all VDCs. Defaults to
                False.
    '''

    # Build command
    cmd = "copy running-config startup-config"
    if copy_vdc_all:
        cmd += " vdc-all"

    # Build Unicon Dialogs
    copy_run_to_start_dialog = Dialog([
        Statement(
            pattern=r'^.*Destination +(filename|file +name)(\s\(control\-c +to +(cancel|abort)\)\:)? +\[(\S+\/)?startup\-config]\?\s*$',
            action='sendline()',
            loop_continue=True,
            continue_timer=False),
        Statement(
            pattern=r'.*proceed anyway\?.*$',
            action='sendline(y)',
            loop_continue=True,
            continue_timer=False),
        Statement(
            pattern=r'Continue\? \[no\]:\s*$',
            action='sendline(y)',
            loop_continue=True,
            continue_timer=False),
        # XR platform specific when over-write the existing configurations
        Statement(
            pattern=r'Continue\? \[no\]:\s*$',
            action='sendline(y)',
            loop_continue=True,
            continue_timer=False)
    ])

    output = device.execute(cmd, timeout=command_timeout,
                            reply=copy_run_to_start_dialog)

    # IOSXE platform
    if "[OK]" in output or "Copy complete" in output:
        return True

    return


def execute(device, *args, **kwargs):
    ''' execute command to device
        Args:
            device (`obj`): Device object
        Return:
            output (`str`): output from command on device
    '''
    output = ''
    # get connected aliases
    connected_aliases = device.api.get_connected_alias()

    for alias, connection_dict in connected_aliases.items():
        # check if CLI(Unicon), or not
        if 'unicon' in connection_dict['connection_provider'].__module__:
            output = getattr(device, alias).execute(*args, **kwargs)
            return output

    if connected_aliases:
        raise Exception('Found aliases {a}, but not CLI(Unicon).'.format(a=connected_aliases.keys()))
    else:
        raise Exception('No connected alias found.')

def execute_and_parse_json(device, command):
    ''' execute the specified command on the device which must return output in JSON format.
        The JSON is parsed into a dict.

        Args:
            device (`obj`): Device object
        Return:
            output (`dict`): parsed JSON output from command on device as a dict
    '''

    output = {}
    try:
        output = execute(device, command)
        output = json.loads(output)
    except Exception as e:
        log.error("An exception occurred when trying to run or parse the output of a command as JSON. "
                "The command was '{}' and the exception is {}".format(command, e))
        output = {}
    return output
