# Python
import re
import time
import shutil
import os.path
import logging
import ipaddress

# Genie
from genie.utils.timeout import Timeout
from genie.libs.clean import BaseStage
from genie.libs.clean.utils import (
    _apply_configuration,
    find_clean_variable,
    verify_num_images_provided,
    handle_rommon_exception,
    remove_string_from_image)
from genie.metaparser.util.schemaengine import Optional, Any, Or

# pyATS
from pyats.utils.fileutils import FileUtils

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

class Connect(BaseStage):
    """This stage connects to the device that is being cleaned.

Stage Schema
------------
connect:

    via (str, optional): Which connection to use from the testbed file. Uses the
        default connection if not specified.

    timeout (int, optional): The timeout for the connection to complete in seconds.
        Defaults to 200.

    retry_timeout (int, optional): Overall timeout for retry mechanism in seconds.
        Defaults to 0 which means no retry.

    retry_interval (int, optional): Interval for retry mechanism in seconds. Defaults
        to 0 which means no retry.

Example
-------
connect:
    timeout: 60
"""

    # =================
    # Argument Defaults
    # =================
    VIA = None
    TIMEOUT = 200
    RETRY_TIMEOUT = 0
    RETRY_INTERVAL = 0

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('via'): str,
        Optional('timeout'): Or(str, int),
        Optional('retry_timeout'): Or(str, int, float),
        Optional('retry_interval'): Or(str, int, float),
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'connect'
    ]

    def connect(self, steps, device, via=VIA, timeout=TIMEOUT,
                retry_timeout=RETRY_TIMEOUT, retry_interval=RETRY_INTERVAL):

        with steps.start("Connecting to the device") as step:

            log.info('Checking connection to device: %s' % device.name)

            # Create a timeout that will loop
            retry_timeout = Timeout(float(retry_timeout), float(retry_interval))
            retry_timeout.one_more_time = True
            # Without this we see 'Performing the last attempt' even if retry
            # is not being used.
            retry_timeout.disable_log = True

            while retry_timeout.iterate():
                retry_timeout.disable_log = False

                # If the device is in rommon, just raise an exception
                device.instantiate(connection_timeout=timeout,
                                   learn_hostname=True,
                                   prompt_recovery=True,
                                   via=via)

                rommon = Statement(
                    pattern=r'^(.*)(rommon(.*)|loader(.*))+>.*$',
                    #action=lambda section: section.failed('Device is in rommon'),
                    action=handle_rommon_exception,
                    loop_continue=False,
                    continue_timer=False)

                device.connect_reply.append(rommon)

                try:
                    device.connect()
                except Exception:
                    log.error("Connection to the device failed", exc_info=True)
                    device.destroy_all()
                    # Loop
                else:
                    step.passed("Successfully connected".format(device.name))
                    # Don't loop
                finally:
                    try:
                        device.connect_reply.remove(rommon)
                    except Exception:
                        pass

                retry_timeout.sleep()

            step.failed("Could not connect. Scroll up for tracebacks.")


class PingServer(BaseStage):
    """ This stage pings a server from a device to ensure connectivity.

Stage Schema
------------
ping_server:

    server (str): Hostname or address of the server to ping.

    vrf (str, optional): Vrf used in ping command. Defaults to None.

    timeout (int, optional): Maximum time in seconds for ping. Defaults to 60.

    min_success_rate (int, optional): Minimum acceptable success rate (percentage)
        of the ping command. Defaults to 60.

    max_attempts (int, optional): Maximum number of attempts to check minimum
        ping success rate. Defaults to 5.

    interval (int, optional): Time in seconds between re-attempts to check
        minimum ping success rate. Defaults to 30.

Example
-------
ping_server:
    server: server-1
    vrf: management
    timeout: 120
    min_success_rate: 75
    max_attempts: 3
    interval: 60
"""

    # =================
    # Argument Defaults
    # =================
    VRF = None
    TIMEOUT = 60
    MIN_SUCCESS_RATE = 60
    MAX_ATTEMPTS = 5
    INTERVAL = 30

    # ============
    # Stage Schema
    # ============
    schema = {
        'server': str,
        Optional('vrf'): str,
        Optional('timeout'): int,
        Optional('min_success_rate'): int,
        Optional('max_attempts'): int,
        Optional('interval'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'ping_server'
    ]

    def ping_server(self, steps, device, server, vrf=VRF, timeout=TIMEOUT,
                    min_success_rate=MIN_SUCCESS_RATE, max_attempts=MAX_ATTEMPTS,
                    interval=INTERVAL):
        with steps.start("Pinging server") as step:

            # Success rate is 80 percent (4/5)
            p1 = r'Success +rate +is +(?P<success>\d+) +percent +\((?P<pass>\d+)\/(?P<fail>\d+)\)'

            #   5 packets transmitted, 5 packets received, 0.00% packet loss
            #   5 packets transmitted, 5 received, 0% packet loss, time 4005ms
            p2 = r'(?P<transmit>\d+) +packets +transmitted, (?P<recv>\d+) +(packets )?received, (?P<loss>\S+)% +packet +loss'

            # Send count=3, Receive count=3
            # Send count=3, Receive count=3 from 172.25.195.115 
            p3 = r'Send count=+(?P<send>\d+), Receive count=+(?P<received>\d+)'

            try:
                # If the server is a valid IP (v4 or v6) use it directly instead
                # of going through FileUtils as this would support more OS's
                # than FileUtils supports.
                ipaddress.ip_address(server)
            except ValueError:
                # Not an IP (v4 or v6). Attempt to retrieve address from
                # testbed.servers block using FileUtils
                fu = FileUtils.from_device(device)
                server = fu.get_hostname(server, device, vrf=vrf)

            for i in range(1, max_attempts + 1):
                log.info(f"Attempt #{i}: Ping '{server}'")

                try:
                    if vrf:
                        output = device.ping(server, vrf=vrf, timeout=timeout)
                    elif 'aireos' in device.os:
                        output = device.ping(addr=server, timeout=timeout)
                    else:
                        output = device.ping(server, timeout=timeout)
                except SubCommandFailure as err:
                    if 'Requested protocol was not running during ping' in str(err):
                        step.failed('No IP routing (or other relevant protocol) '
                                    'configured, not retrying')
                    else:
                        # Success rate is 0%
                        log.warning(f"Unable to meet minimum ping success rate "
                                    f"of {min_success_rate}. Retrying after "
                                    f"{interval} seconds.")

                        time.sleep(interval)
                        continue

                # Success rate is 80 percent (4/5)
                m = re.search(p1, output)
                if m:
                    group = m.groupdict()

                    success_rate = group['success']

                    if float(success_rate) >= float(min_success_rate):
                        step.passed(f"'{server}' is reachable")

                #   5 packets transmitted, 5 packets received, 0.00% packet loss
                #   5 packets transmitted, 5 received, 0% packet loss, time 4005ms
                m = re.search(p2, output)
                if m:
                    group = m.groupdict()

                    recv = group['recv']
                    transmit = group['transmit']
                    success_rate = float(recv) / float(transmit) * 100

                    if float(success_rate) >= float(min_success_rate):
                        step.passed(f"'{server}' is reachable")

                m = re.search(p3, output)
                if m:
                    group = m.groupdict()

                    if int(group['received']) > 0:
                        step.passed(f"{server} is reachable")

                # Minimum success rate not met, retry
                log.warning(f'Unable to meet minimum ping success rate of '
                            f'{min_success_rate}%. Retrying after {interval} '
                            f'seconds.')

                time.sleep(interval)

            else:
                step.failed(f"'{server}' is not reachable after {max_attempts} "
                            f"attempts.")


class CopyToLinux(BaseStage):
    """This stage copies an image to a location on a linux device. It can keep
the original name or modify the name as required.

Stage Schema
------------
copy_to_linux:

    origin:

        files (list): Location of file on the origin server.

        hostname (str, optional): Hostname or address of the origin server.
            If not provided the file is treated as a local file on the
            execution host.

    destination:

        directory (str): Directory that the file will be copied to.

        hostname (str, optional): Hostname or address of the origi server.
            If not provided the directory is treated as a local directory on the
            execution host. This key is only optional if the hostname under
            origin is not provided.

    protocol (str, optional): Protocol used for the copy operation. Defaults to
        sftp.

    overwrite (bool, optional): Overwrite the file if a file with the same
        name already exists. Defaults to False.

    timeout (int, optional): Copy operation timeout in seconds. Defaults to 300.

    check_image_length (bool, optional): Check if the length of the image name
        exceeds the image_length_limit. Defaults to False.

    image_length_limit (int, optional): Maximum length of the image name.
        Defaults to 63.

    append_hostname (bool, optional): Append hostname to the end of the image
        name during copy. Defaults to False.

    copy_attempts (int, optional): Number of times to attempt copying image
        files. Defaults to 1 (no retry).

    copy_attempts_sleep (int, optional): Number of seconds to sleep between
        copy_attempts. Defaults to 30.

    check_file_stability (bool, optional): Verifies that the file size is not
        changing. This ensures the image is not actively being copied.
        Defaults to False.

    unique_file_name (bool, optional): Appends a random six-digit number to
        the end of the image name. Defaults to False.

    unique_number: (int, optional): Appends the provided number to the end of
        the image name. Defaults to None.

    rename_images: (str, optional): Rename the image to the provided name.
        If multiple files exist then an incrementing number is also appended.
        Defaults to None

Example
-------
copy_to_linux:
    protocol: sftp
    origin:
        hostname: server-1
        files:
        - /home/cisco/kickstart.bin
        - /home/cisco/system.bin
    timeout: 300
    destination:
        hostname: file-server
        directory: /auto/tftp-ssr/
    copy_attempts: 2
    check_file_stability: True
    unique_file_name: True

"""

    # =================
    # Argument Defaults
    # =================
    PROTOCOL = 'sftp'
    TIMEOUT = 300
    CHECK_IMAGE_LENGTH = False
    OVERWRITE = False
    APPEND_HOSTNAME = False
    IMAGE_LENGTH_LIMIT = 63
    COPY_ATTEMPTS = 1
    COPY_ATTEMPTS_SLEEP = 30
    CHECK_FILE_STABILITY = False
    UNIQUE_FILE_NAME = False
    UNIQUE_NUMBER = None
    RENAME_IMAGES = None

    # ============
    # Stage Schema
    # ============
    schema = {
        'origin': {
            Optional('files'): list,
            Optional('hostname'): str
        },
        'destination': {
            'directory': str,
            Optional('hostname'): str
        },
        Optional('protocol'): str,
        Optional('timeout'): int,
        Optional('check_image_length'): bool,
        Optional('overwrite'): bool,
        Optional('append_hostname'): bool,
        Optional('image_length_limit'): int,
        Optional('copy_attempts'): int,
        Optional('copy_attempts_sleep'): int,
        Optional('check_file_stability'): bool,
        Optional('unique_file_name'): bool,
        Optional('unique_number'): int,
        Optional('rename_images'): str
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'copy_to_linux'
    ]

    def copy_to_linux(self, steps, device, origin, destination, protocol=PROTOCOL,
                      timeout=TIMEOUT, check_image_length=CHECK_IMAGE_LENGTH,
                      overwrite=OVERWRITE, append_hostname=APPEND_HOSTNAME,
                      image_length_limit=IMAGE_LENGTH_LIMIT,
                      copy_attempts=COPY_ATTEMPTS,
                      copy_attempts_sleep=COPY_ATTEMPTS_SLEEP,
                      check_file_stability=CHECK_FILE_STABILITY,
                      unique_file_name=UNIQUE_FILE_NAME,
                      unique_number=UNIQUE_NUMBER,
                      rename_images=RENAME_IMAGES):

        if not hasattr(device.testbed, 'servers'):
            self.failed("Cannot find any servers in the testbed")

        destination_hostname = destination.get('hostname')

        # If not provided, assume its localhost
        server_from = origin.get('hostname')

        if not server_from:
            server_from_obj = None
        else:
            try:
                # From IP/hostname find server from testbed file - get device obj
                server_from_obj = device.api.convert_server_to_linux_device(
                    server_from)
            except (KeyError, AttributeError):
                self.failed("Server '{}' was provided in the clean yaml file "
                               "but doesn't exist in the testbed file".\
                               format(server_from))

            try:
                # Connect to the server
                server_from_obj.connect()
            except Exception as e:
                self.failed('Failed to connect to {} due to {}'.\
                               format(server_from_obj.name, str(e)))

        # establish a FileUtils session for all FileUtils operations
        fu = FileUtils(testbed=device.testbed)
        if server_from:
            server_block = fu.get_server_block(server_from)
            string_to_remove = server_block.get('path', '')
        else:
            string_to_remove = ''

        origin_path = remove_string_from_image(images=origin['files'],
                                               string=string_to_remove)

        if len(origin_path) == 0:
            self.failed(
                "No file was provided to copy. Please provide files under destination.path in the clean yaml file."
            )

        dest_dir = destination['directory']

        files_to_copy = {}
        with steps.start(
                "Collecting file info on origin and '{d}' "
                "before copy".format(d=destination_hostname or dest_dir)) as step:
            file_size = -1
            for index, file in enumerate(origin_path):
                with step.start("Collecting '{f}' info".format(f=file)) as substep:
                    # file to copy is remote
                    if server_from:
                        try:
                            log.info(
                                "Getting size of the file '{}' from file server '{}'"
                                .format(file, server_from))
                            file_size = device.api.get_file_size_from_server(
                                server=fu.get_hostname(server_from),
                                path=file,
                                protocol=protocol,
                                timeout=timeout,
                                fu_session=fu)
                        except FileNotFoundError:
                            step.failed(
                                "Can not find file {} on server {}. Terminating clean"
                                .format(file, server_from))
                        except Exception as e:
                            log.warning(
                                "Could not verify the size for file '{}'.\nError: {}".format(
                                    file, e))

                    # file to copy is local
                    else:
                        try:
                            file_size = os.path.getsize(file)
                        except FileNotFoundError:
                            step.failed("Can not find file {} on local server."
                                        "Terminating clean".format(file))
                        except Exception as e:
                            log.warning(
                                "Could not verify the size for file '{}' due to {}".format(
                                    file, e))

                    if rename_images:
                        rename_images = rename_images + '_' + str(index)

                    try:
                        new_name = device.api.modify_filename(
                            file=os.path.basename(file),
                            directory=dest_dir,
                            protocol=protocol,
                            append_hostname=append_hostname,
                            check_image_length=check_image_length,
                            limit=image_length_limit,
                            unique_file_name=unique_file_name,
                            unique_number=unique_number,
                            new_name=rename_images)
                    except Exception as e:
                        step.failed(
                            "Can not change file name. Terminating clean:\n{e}".
                            format(e=e))

                    file_path = os.path.join(dest_dir, new_name)

                    if not overwrite:
                        log.info("Checking if file '{}' already exists at {}".\
                                format(file_path, destination_hostname or dest_dir))
                        try:
                            exist = device.api.verify_file_exists_on_server(
                                protocol=protocol,
                                server=destination_hostname,
                                file=file_path,
                                size=file_size,
                                timeout=timeout,
                                fu_session=fu)
                        except Exception as e:
                            exist = False
                            log.error(
                                "Unable to verify if file '{}' already exists"
                                " at {}\n{}".format(
                                    file_path, destination_hostname or dest_dir,
                                    str(e)))
                    else:
                        exist = False

                    image_mapping = self.history[
                        'CopyToLinux'].parameters.setdefault(
                            'image_mapping', {})
                    image_mapping.update({origin['files'][index]: file_path})

                    file_copy_info = {
                        file: {
                            'size': file_size,
                            'dest_path': file_path,
                            'exist': exist
                        }
                    }
                    files_to_copy.update(file_copy_info)

                    substep.passed(
                        'Verified file {} on source and destination servers'.
                        format(os.path.basename(file)))

        if check_file_stability:
            with steps.start("Check if any file is being copied") as step:
                if not server_from:
                    # no need to check stability if the file is local
                    step.skipped("File is local, skipping this step")

                log.info(
                    "Verify if the files are still being copied on the origin server"
                )

                for file, file_data in files_to_copy.items():

                    with step.start(
                            "Verify stability of '{f}'".format(f=file)) as substep:

                        try:
                            stable = device.api.verify_file_size_stable_on_server(
                                protocol=protocol,
                                server=server_from,
                                file=file,
                                timeout=timeout,
                                fu_session=fu)
                        except NotImplementedError as e:
                            step.skipped(str(e))

                        if not stable:
                            fu.close()
                            substep.failed("The size of file '{}' on server "
                                           "'{}' is not stable".format(
                                               file, server_from))

        with steps.start("Check if there is enough space on {server} to "
                         "perform the copy".format(
                             server=destination_hostname or dest_dir)) as step:

            total_size = sum(file_data['size']
                             for file_data in files_to_copy.values())

            try:
                if not device.api.verify_enough_server_disk_space(
                        server=destination_hostname,
                        required_space=total_size,
                        directory=dest_dir,
                        protocol=protocol,
                        timeout=timeout,
                        fu_session=fu):
                    fu.close()
                    step.failed(
                        "There is not enough space on server '{}' at '{}'."
                        "Terminating clean".format(destination_hostname,
                                                   dest_dir), )
            except NotImplementedError as e:
                step.skipped(str(e))
            except Exception as e:
                step.skipped(str(e))

        with steps.start("Copying the files to {}".format(destination_hostname
                                                          or dest_dir)) as step:
            for file, file_data in files_to_copy.items():
                with step.start("Copying '{}'".format(file)) as substep:
                    if not overwrite and file_data['exist']:
                        substep.skipped(
                            'File with the same name and same size already exist on the '
                            'server and overwrite is set to False, skipped copying'
                        )

                    for i in range(1, copy_attempts + 1):
                        try:
                            if server_from:
                                server_from_obj.api.copy_from_device(
                                    remote_path=file_data['dest_path'],
                                    local_path=file,
                                    server=fu.get_hostname(destination_hostname),
                                    protocol=protocol,
                                    timeout=timeout,
                                    quiet=True)
                            elif destination_hostname:
                                device.api.copy_to_server(
                                    testbed=device.testbed,
                                    remote_path=file_data['dest_path'],
                                    local_path=file,
                                    server=fu.get_hostname(destination_hostname),
                                    protocol=protocol,
                                    timeout=timeout,
                                    fu_session=fu,
                                    quiet=True)
                            else:
                                shutil.copyfile(file, file_data['dest_path'])

                        except Exception as e:
                            # if user wants to retry
                            if i < copy_attempts:
                                log.warning(
                                    "Could not copy file '{file}' to '{d}', {e}\n"
                                    "attempt #{iteration}".format(
                                        file=file,
                                        d=destination_hostname,
                                        e=e,
                                        iteration=i + 1))
                                log.info("Sleeping for {} seconds before retrying"
                                         .format(copy_attempts_sleep))
                                time.sleep(copy_attempts_sleep)
                            else:
                                substep.failed("Could not copy '{file}' to '{d}'\n{e}"\
                                            .format(file=file, d=destination_hostname, e=e))
                        else:
                            # copy passed, will not retry
                            log.info(
                                '{f} has been copied correctly'.format(f=file))
                            break

                    # save the file copied name and size info for future use
                    history = self.history[
                        'CopyToLinux'].parameters.setdefault('files_copied', {})
                    history.update({file: file_data})

        # verify file copied section below
        with steps.start("Verify the files have been copied correctly") as step:
            if protocol.lower() in ['tftp', 'scp']:
                step.skipped(
                    'tftp protocol does not support check file size, skipping this step.'
                )

            if 'files_copied' not in self.history['CopyToLinux'].parameters:
                step.skipped(
                    'No files was copied in previous steps, skipping this step.')

            for name, image_data in self.history['CopyToLinux'].parameters[
                    'files_copied'].items():

                # If size is -1 it means it failed to get the size
                if image_data['size'] != -1:
                    try:
                        if not device.api.verify_file_exists_on_server(
                                protocol=protocol,
                                server=destination_hostname,
                                file=image_data['dest_path'],
                                size=image_data['size'],
                                timeout=timeout,
                                fu_session=fu):
                            step.failed("File size is not the same on the origin"
                                        " and on the file server")
                        else:
                            self.passed("File size is the same on the origin "
                                           "and on the file server")
                    except Exception as e:
                        step.failed("Failed to verify file. Error: {}".format(
                            str(e)))
                else:
                    step.skipped("File has been copied correctly but cannot "
                                 "verify file size")


class CopyToDevice(BaseStage):
    """This stage will copy an image to a device from a networked location.

Stage Schema
------------
copy_to_device:

    origin:

        files (list): Image files location on the server.

        hostname (str): Hostname or address of the server.

    destination:

        directory (str): Directory on the device to copy the images to.

        standby_directory (str, optional): Standby directory on the device
            to copy the images to. Defaults to None.

    protocol (str): Protocol used for copy operation.

    verify_num_images (bool, optional): Verify number of images provided by
        user for clean is correct. Defaults to True.

    expected_num_images (int, optional): Number of images expected to be
        provided by user for clean. Defaults to 1.

    vrf (str, optional): Vrf used to copy. Defaults to an empty string.

    timeout (int, optional): Copy operation timeout in seconds. Defaults to 300.

    compact (bool, optional): Compact copy mode if supported by the device.
        Defaults to False.

    protected_files (list, optional): File patterns that should not be deleted.
        Defaults to None.

    overwrite (bool, optional): Overwrite the file if a file with the same
        name already exists. Defaults to False.

    skip_deletion (bool, optional): Do not delete any files even if there isn't
        any space on device. Defaults to False.

    copy_attempts (int, optional): Number of times to attempt copying image
        files. Defaults to 1 (no retry).

    copy_attempts_sleep (int, optional): Number of seconds to sleep between
        copy_attempts. Defaults to 30.

    check_file_stability (bool, optional): Verifies that the file size is not
        changing. This ensures the image is not actively being copied.
        Defaults to False.

    stability_check_tries (int, optional): Max number of checks that can be
        done when checking file stability. Defaults to 3.

    stability_check_delay (int, optional): Delay between tries when checking
        file stability in seconds. Defaults to 2.

    min_free_space_percent ('int', optional) : Percentage of total disk space
        that must be free. If specified the percentage is not free then the
        stage will attempt to delete unprotected files to reach the minimum
        percentage. Defaults to None.

    use_kstack (bool, optional): Use faster version of copy with limited options.
        Defaults to False.

    interface (str, optional): The interface to use for file transfers, may be needed
        for copying files on some IOSXE platforms, such as ASR1K when using a VRF
        Defaults to None

    unique_file_name (bool, optional): Appends a random six-digit number to
        the end of the image name. Defaults to False.

    unique_number: (int, optional): Appends the provided number to the end of
        the image name. Defaults to None. Requires unique_file_name is True
        to be applied.

    rename_images: (str, optional): Rename the image to the provided name.
        If multiple files exist then an incrementing number is also appended.
        Defaults to None

Example
-------
copy_to_device:
    origin:
        hostname: server-1
        files:
            - /home/cisco/asr1k.bin
    destination:
        directory: harddisk:/
    protocol: sftp
    timeout: 300
"""
    # =================
    # Argument Defaults
    # =================
    VERIFY_NUM_IMAGES = True
    EXPECTED_NUM_IMAGES = 1
    # must be '' instead of None to prevent NXOS from
    # defaulting to 'management'
    VRF = ''
    TIMEOUT = 300
    COMPACT = False
    USE_KSTACK = False
    PROTECTED_FILES = None
    OVERWRITE = False
    SKIP_DELETION = False
    COPY_ATTEMPTS = 1
    COPY_ATTEMPTS_SLEEP = 30
    CHECK_FILE_STABILITY = False
    STABILITY_CHECK_TRIES = 3
    STABILITY_CHECK_DELAY = 2
    MIN_FREE_SPACE_PERCENT = None
    INTERFACE = None
    UNIQUE_FILE_NAME = False
    UNIQUE_NUMBER = None
    RENAME_IMAGES = None


    # ============
    # Stage Schema
    # ============
    schema = {
        'origin': {
            Optional('files'): list,
            'hostname': str
        },
        'destination': {
            'directory': str,
            Optional('standby_directory'): str,
        },
        'protocol': str,
        Optional('verify_num_images'): bool,
        Optional('expected_num_images'): int,
        Optional('vrf'): str,
        Optional('timeout'): int,
        Optional('compact'): bool,
        Optional('use_kstack'): bool,
        Optional('protected_files'): list,
        Optional('overwrite'): bool,
        Optional('skip_deletion'): bool,
        Optional('copy_attempts'): int,
        Optional('copy_attempts_sleep'): int,
        Optional('check_file_stability'): bool,
        Optional('stability_check_tries'): int,
        Optional('stability_check_delay'): int,
        Optional('min_free_space_percent'): int,
        Optional('interface'): str,
        Optional('unique_file_name'): bool,
        Optional('unique_number'): int,
        Optional('rename_images'): str
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'copy_to_device'
    ]

    def copy_to_device(self, steps, device, origin, destination, protocol,
                       verify_num_images=VERIFY_NUM_IMAGES,
                       expected_num_images=EXPECTED_NUM_IMAGES,
                       vrf=VRF,
                       timeout=TIMEOUT,
                       compact=COMPACT,
                       use_kstack=USE_KSTACK,
                       protected_files=PROTECTED_FILES,
                       overwrite=OVERWRITE,
                       skip_deletion=SKIP_DELETION,
                       copy_attempts=COPY_ATTEMPTS,
                       copy_attempts_sleep=COPY_ATTEMPTS_SLEEP,
                       check_file_stability=CHECK_FILE_STABILITY,
                       stability_check_tries=STABILITY_CHECK_TRIES,
                       stability_check_delay=STABILITY_CHECK_DELAY,
                       min_free_space_percent=MIN_FREE_SPACE_PERCENT,
                       interface=INTERFACE,
                       unique_file_name=UNIQUE_FILE_NAME,
                       unique_number=UNIQUE_NUMBER,
                       rename_images=RENAME_IMAGES,
                       **kwargs
                       ):
        log.info("Section steps:\n1- Verify correct number of images provided"
                 "\n2- Get filesize of image files on remote server"
                 "\n3- Check if image files already exist on device"
                 "\n4- (Optional) Verify stability of image files"
                 "\n5- Verify free space on device else delete unprotected files"
                 "\n6- Copy image files to device"
                 "\n7- Verify copied image files are present on device")

        # list of destination directories
        destinations = []

        # Get args
        server = origin['hostname']

        # Establish FileUtils session for all FileUtils operations
        file_utils = FileUtils(testbed=device.testbed)

        string_to_remove = file_utils.get_server_block(server).get('path', '')
        image_files = remove_string_from_image(images=origin['files'],
                                               string=string_to_remove)

        # Set active node destination directory
        destination_act = destination['directory']

        # Set standby node destination directory
        if 'standby_directory' in destination:
            destination_stby = destination['standby_directory']
            destinations = [destination_stby, destination_act]
        else:
            destination_stby = None
            destinations = [destination_act]

        # Check remote server info present in testbed YAML
        if not file_utils.get_server_block(server):
            self.failed(
                "Server '{}' was provided in the clean yaml file but "
                "doesn't exist in the testbed file.\n".format(server))

        # Check image files provided
        if verify_num_images:
            # Verify correct number of images provided
            with steps.start("Verify correct number of images provided") as step:
                if not verify_num_images_provided(
                        image_list=image_files,
                        expected_images=expected_num_images):
                    step.failed(
                        "Incorrect number of images provided. Please "
                        "provide {} expected image(s) under destination"
                        ".path in clean yaml file.\n".format(expected_num_images))
                else:
                    step.passed("Correct number of images provided")

        # Loop over all image files provided by user
        for index, file in enumerate(image_files):
            # Init
            files_to_copy = {}
            unknown_size = False

            # Get filesize of image files on remote server
            with steps.start("Get filesize of '{}' on remote server '{}'".\
                            format(file, server)) as step:
                try:
                    file_size = device.api.get_file_size_from_server(
                        server=file_utils.get_hostname(server),
                        path=file,
                        protocol=protocol,
                        timeout=timeout,
                        fu_session=file_utils)
                except FileNotFoundError:
                    step.failed(
                        "Can not find file {} on server {}. Terminating clean".
                        format(file, server))
                except Exception as e:
                    log.warning(str(e))
                    # Something went wrong, set file_size to -1
                    file_size = -1
                    unknown_size = True
                    err_msg = "\nUnable to get filesize for file '{}' on "\
                              "remote server {}".format(file, server)
                    if overwrite:
                        err_msg += " - will copy file to device"
                    step.passx(err_msg)
                else:
                    step.passed("Verified filesize of file '{}' to be "
                                "{} bytes".format(file, file_size))
            for dest in destinations:

                # Execute 'dir' before copying image files
                dir_before = device.execute('dir {}'.format(dest))

                # Check if file with same name and size exists on device
                dest_file_path = os.path.join(dest, os.path.basename(file))
                image_mapping = self.history[
                    'CopyToDevice'].parameters.setdefault('image_mapping', {})
                image_mapping.update({origin['files'][index]: dest_file_path})
                with steps.start("Check if file '{}' exists on device {} {}".\
                                format(dest_file_path, device.name, dest)) as step:
                    # Check if file exists
                    try:
                        exist = device.api.verify_file_exists(
                            file=dest_file_path,
                            size=file_size,
                            dir_output=dir_before)
                    except Exception as e:
                        exist = False
                        log.warning("Unable to check if image '{}' exists on device {} {}."
                                    "Error: {}".format(dest_file_path,
                                                       device.name,
                                                       dest,
                                                       str(e)))

                    if (not exist) or (exist and overwrite) or (exist and (unique_file_name or unique_number or rename_images)):
                        # Update list of files to copy
                        file_copy_info = {
                            file: {
                                'size': file_size,
                                'dest_path': dest_file_path,
                                'exist': exist
                            }
                        }
                        files_to_copy.update(file_copy_info)
                        # Print message to user
                        step.passed("Proceeding with copying image {} to device {}".\
                                    format(dest_file_path, device.name))
                    else:
                        step.passed(
                            "Image '{}' already exists on device {} {}, "
                            "skipping copy".format(file, device.name, dest))

                # Check if any file copy is in progress
                if check_file_stability:
                    for file in files_to_copy:
                        with steps.start("Verify stability of file '{}'".\
                                         format(file)) as step:
                            # Check file stability
                            try:
                                stable = device.api.verify_file_size_stable_on_server(
                                    file=file,
                                    server=file_utils.get_hostname(server),
                                    protocol=protocol,
                                    fu_session=file_utils,
                                    delay=stability_check_delay,
                                    max_tries=stability_check_tries)

                                if not stable:
                                    step.failed(
                                        "The size of file '{}' on server is not "
                                        "stable\n".format(file), )
                                else:
                                    step.passed(
                                        "Size of file '{}' is stable".format(file))
                            except NotImplementedError:
                                # cannot check using tftp
                                step.passx(
                                    "Unable to check file stability over {protocol}"
                                    .format(protocol=protocol))
                            except Exception as e:
                                log.error(str(e))
                                step.failed(
                                    "Error while verifying file stability on "
                                    "server\n")

                # Verify available space on the device is sufficient for image copy, delete
                # unprotected files if needed, copy file to the device
                # unless overwrite: False
                if files_to_copy:
                    with steps.start(
                            "Verify sufficient free space on device '{}' '{}' or delete"
                            " unprotected files".format(device.name,
                                                        dest)) as step:

                        if unknown_size:
                            total_size = -1
                            log.warning("Amount of space required cannot be confirmed, "
                                        "copying the files on the device '{}' '{}' may fail".\
                                        format(device.name, dest))

                        if not protected_files:
                            protected_files = []

                        # Try to free up disk space if skip_deletion is not set to True
                        if not skip_deletion:
                            # TODO: add golden images, config to protected files once we have golden section
                            golden_config = find_clean_variable(
                                self, 'golden_config')
                            golden_image = find_clean_variable(
                                self, 'golden_image')

                            if golden_config:
                                protected_files.extend(golden_config)
                            if golden_image:
                                protected_files.extend(golden_image)

                            # Only calculate size of file being copied
                            total_size = sum(0 if file_data['exist'] \
                                             else file_data['size'] for \
                                             file_data in files_to_copy.values())

                            try:
                                free_space = device.api.free_up_disk_space(
                                    destination=dest,
                                    required_size=total_size,
                                    skip_deletion=skip_deletion,
                                    protected_files=protected_files,
                                    min_free_space_percent=min_free_space_percent,
                                    dir_output=dir_before,
                                    allow_deletion_failure=True)
                                if not free_space:
                                    step.failed("Unable to create enough space for "
                                                   "image on device {} {}".\
                                                   format(device.name, dest))
                                else:
                                    step.passed(
                                        "Device {} {} has sufficient space to "
                                        "copy images".format(device.name, dest))
                            except Exception as e:
                                log.error(str(e))
                                step.failed("Error while creating free space for "
                                               "image on device {} {}".\
                                               format(device.name, dest))

                # Copy the file to the devices
                for file, file_data in files_to_copy.items():
                    with steps.start("Copying image file {} to device {} {}".\
                                     format(file, device.name, dest)) as step:

                        # Copy file unless overwrite is False
                        if not overwrite and file_data['exist'] and not (unique_file_name or unique_number or rename_images):
                            step.skipped(
                                "File with the same name size exists on "
                                "the device {} {}, skipped copying".format(
                                    device.name, dest))

                        for i in range(1, copy_attempts + 1):
                            if unique_file_name or unique_number or rename_images:

                                log.info('renaming files for copying')
                                if rename_images:
                                    rename_images = rename_images + '_' + str(index)

                                try:
                                    new_name = device.api.modify_filename(
                                        file=os.path.basename(file),
                                        directory=destination_act,
                                        server=server,
                                        protocol=protocol,
                                        unique_file_name=unique_file_name,
                                        unique_number=unique_number,
                                        new_name=rename_images)
                                except Exception as e:
                                    step.failed(
                                        "Can not change file name. Terminating clean:\n{e}".format(e=e))

                                log.info(f'Renamed {os.path.basename(file)} to {new_name}')

                                renamed_local_path = os.path.join(dest, new_name)

                                renamed_file_data = {x: y for x,y in file_data.items()}
                                renamed_file_data['dest_path'] = renamed_local_path

                                self.history['CopyToDevice'].parameters['image_mapping'][file] = renamed_local_path

                                try:
                                    device.api.\
                                        copy_to_device(protocol=protocol,
                                                       server=file_utils.get_hostname(server),
                                                       remote_path=file,
                                                       local_path=renamed_local_path,
                                                       vrf=vrf,
                                                       timeout=timeout,
                                                       compact=compact,
                                                       use_kstack=use_kstack,
                                                       interface=interface,
                                                       overwrite=overwrite,
                                                       **kwargs)
                                except Exception as e:
                                    # Retry attempt if user specified
                                    if i < copy_attempts:
                                        log.warning("Attempt #{}: Unable to copy {} to '{} {}' due to:\n{}".\
                                                    format(i, file, device.name, dest, e))
                                        log.info("Sleeping for {} seconds before retrying"
                                                 .format(copy_attempts_sleep))
                                        time.sleep(copy_attempts_sleep)
                                        continue
                                    else:
                                        log.error(str(e))
                                        step.failed(
                                            "Failed to copy image '{}' to '{}' on device"
                                            " '{}'\n".format(file, dest,
                                                             device.name), )
                            else:
                                try:
                                    device.api. \
                                        copy_to_device(protocol=protocol,
                                                       server=file_utils.get_hostname(server),
                                                       remote_path=file,
                                                       local_path=file_data['dest_path'],
                                                       vrf=vrf,
                                                       timeout=timeout,
                                                       compact=compact,
                                                       use_kstack=use_kstack,
                                                       interface=interface,
                                                       overwrite=overwrite,
                                                       **kwargs)
                                except Exception as e:
                                    # Retry attempt if user specified
                                    if i < copy_attempts:
                                        log.warning("Attempt #{}: Unable to copy {} to '{} {}' due to:\n{}". \
                                                    format(i, file, device.name, dest, e))
                                        log.info("Sleeping for {} seconds before retrying"
                                                 .format(copy_attempts_sleep))
                                        time.sleep(copy_attempts_sleep)
                                        continue
                                    else:
                                        log.error(str(e))
                                        step.failed(
                                            "Failed to copy image '{}' to '{}' on device"
                                            " '{}'\n".format(file, dest,
                                                             device.name), )

                            log.info(
                                "File {} has been copied to {} on device {}"
                                " successfully".format(file, dest,
                                                       device.name))
                            success_copy_ha = True
                            break

                        # Save the file copied path and size info for future use
                        history = self.history['CopyToDevice'].parameters.\
                                            setdefault('files_copied', {})

                        if unique_file_name or unique_number or rename_images:
                            history.update({file: renamed_file_data})
                        else:
                            history.update({file: file_data})

                with steps.start("Verify images successfully copied") as step:
                    # If nothing copied don't need to verify, skip
                    if 'files_copied' not in self.history[
                            'CopyToDevice'].parameters:
                        step.skipped(
                            "Image files were not copied for {} {} in previous steps, "
                            "skipping verification steps".format(device.name, dest))

                    # Execute 'dir' after copying image files
                    dir_after = device.execute('dir {}'.format(dest))

                    for name, image_data in self.history['CopyToDevice'].\
                                                    parameters['files_copied'].items():
                        with step.start("Verify image '{}' copied to {} on device {}".\
                                        format(image_data['dest_path'], dest, device.name)) as substep:
                            # if size is -1 it means it failed to get the size
                            if image_data['size'] != -1:
                                if not device.api.verify_file_exists(
                                        file=image_data['dest_path'],
                                        size=image_data['size'],
                                        dir_output=dir_after):
                                    substep.failed("Size of image file copied to device {} is "
                                                   "not the same as remote server filesize".\
                                                   format(device.name))
                                else:
                                    file_name = os.path.basename(file)
                                    if file_name not in protected_files:
                                        protected_files.append(file_name)
                                    log.info('{file_name} added to protected list'.format(file_name=file_name))

                                    substep.passed("Size of image file copied to device {} is "
                                                   "the same as image filesize on remote server".\
                                                   format(device.name))

                            else:
                                file_name = os.path.basename(file)
                                if file_name not in protected_files:
                                    protected_files.append(file_name)
                                log.info('{file_name} added to protected list'.format(file_name=file_name))

                                substep.skipped(
                                    "Image file has been copied to device {} correctly"
                                    " but cannot verify file size".format(device.name))


class WriteErase(BaseStage):
    """ This stage executes 'write erase' on the device

Stage Schema
------------
write_erase:

    timeout (int, optional): Max time allowed for command to complete.
        Defaults to 300 seconds.

Example
-------
write_erase:
    timeout: 100
"""
    # =================
    # Argument Defaults
    # =================
    TIMEOUT = 300

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('timeout'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'write_erase'
    ]

    def write_erase(self, steps, device, timeout=TIMEOUT):

        with steps.start("Execute write erase on the device") as step:

            try:
                device.api.execute_write_erase(timeout=timeout)
            except Exception as e:
                step.failed("Failed to execute 'write erase'", from_exception=e)


class Reload(BaseStage):
    """ This stage reloads the device.

Stage Schema
------------
reload:

    reload_service_args (optional):

        timeout (int, optional): Maximum time in seconds allowed for the reload.
            Defaults to 800.

        reload_creds (str, optional): The credential to use after the reload is
            complete. The credential name comes from the testbed yaml file.
            Defaults to the 'default' credential.

        prompt_recovery (bool, optional): Enable or disable the prompt recovery
            feature of unicon. Defaults to True.

        <Key>: <Value>
            Any other arguments that the Unicon reload service supports

    check_modules:

        check (bool, optional): Enable the checking of modules after reload.
            Defaults to True.

        timeout (int, optional): Maximum time in seconds allowed for verifying
            the modules are in a stable state. Defaults to 180.

        interval (int, optional): How often to check the module states in
            seconds. Defaults to 30.

    reconnect_via (str, optional): Specify which connection to use after reloading.
        Defaults to the 'default' connection in the testbed yaml file.


Example
-------
reload:
    reload_service_args:
        timeout: 600
        reload_creds: clean_reload_creds
        prompt_recovery: True
        reconnect_sleep: 200 (Unicon NXOS reload service argument)
    check_modules:
        check: False
"""
    # =================
    # Argument Defaults
    # =================
    RELOAD_SERVICE_ARGS = {
        'timeout': 800,
        'reload_creds': 'default',
        'prompt_recovery': True
    }
    CHECK_MODULES = {
        'check': True,
        'timeout': 180,
        'interval': 30
    }
    RECONNECT_VIA = None

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('check_modules'): {
            Optional('check'): bool,
            Optional('timeout'): int,
            Optional('interval'): int
        },
        Optional('reload_service_args'): {
            Optional('timeout'): int,
            Optional('reload_creds'): str,
            Optional('prompt_recovery'): bool,
            Any(): Any()
        },
        Optional('reconnect_via'): str,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'reload',
        'disconnect_and_reconnect',
        'check_modules'
    ]

    def reload(self, steps, device, reload_service_args=None):

        if reload_service_args is None:
            # If user provides no custom values, take the defaults
            reload_service_args = self.RELOAD_SERVICE_ARGS
        else:
            # If user provides custom values, update the default with the user
            # provided. This is needed because if the user only provides 1 of
            # the many optional arguments, we still need to default the others.
            self.RELOAD_SERVICE_ARGS.update(reload_service_args)
            reload_service_args = self.RELOAD_SERVICE_ARGS

        with steps.start(f"Reload {device.name}") as step:

            try:
                device.reload(**reload_service_args)
            except Exception as e:
                step.failed(f"Failed to reload within {reload_service_args['timeout']} "
                            f"seconds.", from_exception=e)

    def disconnect_and_reconnect(self, steps, device, reload_service_args=None,
                                 reconnect_via=RECONNECT_VIA):

        if reload_service_args is None:
            # If user provides no custom values, take the defaults
            reload_service_args = self.RELOAD_SERVICE_ARGS
        else:
            # If user provides custom values, update the default with the user
            # provided. This is needed because if the user only provides 1 of
            # the many optional arguments, we still need to default the others.
            self.RELOAD_SERVICE_ARGS.update(reload_service_args)
            reload_service_args = self.RELOAD_SERVICE_ARGS

        with steps.start(f"Disconnect and Reconnect to {device.name}") as step:

            try:
                device.destroy()
            except Exception:
                log.warning("Failed to destroy the device connection but "
                            "attempting to continue", exc_info=True)

            connect_kwargs = {
                'learn_hostname': True,
                'prompt_recovery': reload_service_args['prompt_recovery']
            }

            if reconnect_via:
                connect_kwargs.update({'via': reconnect_via})

            try:
                device.connect(**connect_kwargs)
            except Exception as e:
                step.failed("Failed to reconnect", from_exception=e)

    def check_modules(self, steps, device, check_modules=None):

        if check_modules is None:
            # If user provides no custom values, take the defaults
            check_modules = self.CHECK_MODULES
        else:
            # If user provides custom values, update the default with the user
            # provided. This is needed because if the user only provides 1 of
            # the many optional arguments, we still need to default the others.
            self.CHECK_MODULES.update(check_modules)
            check_modules = self.CHECK_MODULES

        if check_modules['check']:

            with steps.start(f"Checking the modules on '{device.name}' are in a "
                             f"stable state") as step:

                try:
                    device.api.verify_module_status(
                        timeout=check_modules['timeout'],
                        interval=check_modules['interval'])
                except Exception as e:
                    step.failed("Modules are not in a stable state",
                                from_exception=e)


class ApplyConfiguration(BaseStage):
    """Apply configuration on the device, either by providing a file or a
raw configuration.

Stage Schema
------------
apply_configuration:

    configuration (str, optional): String representation of the configuration to
        apply. Defaults to None.

    configuration_from_file (str, optional): A file that contains a configuration
        that will be read. The configuration contained will then be applied as
        if a string representation of the config was applied. Defaults to None.

    file (str, optional): A saved configuration file that will be used. The file
        will either be used in copy run start or configure replace based on the
        'configure_replace' argument. Defaults to None.

    configure_replace (bool, optional): When 'True' use 'configure replace' instead
        of 'copy run start'. Defaults to False.

    config_timeout (int, optional): Max time in seconds allowed for applying the
        configuration. Defaults to 60.

    config_stable_time (int, optional): Max time in seconds allowed for the
        configuration to stabilize. Defaults to 10.

    copy_vdc_all (bool, optional): If 'True' copy on all VDCs. Defaults to False.

    max_time (int, optional): Maximum time in seconds allowed for any
        verifications. Defaults to 300.

    check_interval (int, optional): How often in seconds to check. Defaults to 60.

    skip_copy_run_start (bool, optional): If 'True' do not copy the running config
        to the startup config. Defaults to False.

    copy_directly_to_startup (bool, optional): If 'True' copy the provided
        configuration directly to the startup config. Defaults to False.

Example
-------
apply_configuration:
    configuration: |
        interface ethernet2/1
        no shutdown
    config_timeout: 600
    config_stable_time: 10
    copy_vdc_all: True
    max_time: 300
    check_interval: 20
    copy_directly_to_startup: False

"""

    # =================
    # Argument Defaults
    # =================
    CONFIGURATION = None
    CONFIGURATION_FROM_FILE = None
    FILE = None
    CONFIG_TIMEOUT = 60
    CONFIG_STABLE_TIME = 10
    COPY_VDC_ALL = False
    MAX_TIME = 300
    CHECK_INTERVAL = 60
    CONFIGURE_REPLACE = False
    SKIP_COPY_RUN_START = False
    COPY_DIRECTLY_TO_STARTUP = False

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('configuration'): str,
        Optional('configuration_from_file'): str,
        Optional('file'): str,
        Optional('config_timeout'): int,
        Optional('config_stable_time'): int,
        Optional('copy_vdc_all'): bool,
        Optional('max_time'): int,
        Optional('check_interval'): int,
        Optional('configure_replace'): bool,
        Optional('skip_copy_run_start'): bool,
        Optional('copy_directly_to_startup'): bool,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'apply_configuration'
    ]

    def apply_configuration(self, steps, device,
                            configuration=CONFIGURATION,
                            configuration_from_file=CONFIGURATION_FROM_FILE,
                            file=FILE,
                            config_timeout=CONFIG_TIMEOUT,
                            config_stable_time=CONFIG_STABLE_TIME,
                            copy_vdc_all=COPY_VDC_ALL,
                            max_time=MAX_TIME,
                            check_interval=CHECK_INTERVAL,
                            configure_replace=CONFIGURE_REPLACE,
                            skip_copy_run_start=SKIP_COPY_RUN_START,
                            copy_directly_to_startup=COPY_DIRECTLY_TO_STARTUP):
        log.info("Section steps:\n1- Copy/Apply configuration to/on the device"
                 "\n2- Copy running-config to startup-config"
                 "\n3- Sleep to stabilize configuration on the device")

        # User has provided raw output or configuration file to apply onto device
        with steps.start("Apply configuration to device {} after reload".\
                         format(device.name)) as step:
            try:
                _apply_configuration(
                    device=device,
                    configuration=configuration,
                    configuration_from_file=configuration_from_file,
                    file=file,
                    configure_replace=configure_replace,
                    timeout=config_timeout,
                    copy_directly_to_startup=copy_directly_to_startup)
            except Exception as e:
                step.failed("Error while applying configuration to device "
                            "{}\n{}".format(device.name, str(e)))
            else:
                step.passed(
                    "Successfully applied configuration to device {} ".format(
                        device.name))

        # Copy running-config to startup-config
        if not copy_directly_to_startup and not skip_copy_run_start:
            with steps.start("Copy running-config to startup-config on device {}".\
                            format(device.name)) as step:
                try:
                    device.api.execute_copy_run_to_start(command_timeout=config_timeout,
                                                        max_time=max_time,
                                                        check_interval=check_interval,
                                                        copy_vdc_all=copy_vdc_all)
                except Exception as e:
                    step.failed("Failed to copy running-config to startup-config on "
                                   "{}\n{}".format(device.name, str(e)))
                else:
                    step.passed("Successfully copied running-config to startup-config "
                                "on {}".format(device.name))

        # Allow configuration to stabilize
        with steps.start("Allow configuration to stabilize on device {}".\
                         format(device.name)) as step:
            log.info("Sleeping for '{}' seconds".format(config_stable_time))
            time.sleep(config_stable_time)
            self.passed("Successfully applied configuration after reloading "
                           "device {}".format(device.name))


class VerifyRunningImage(BaseStage):
    """This stage verifies the current running image is the expected image.
The verification can be done by either MD5 hash comparison or by filename
comparison.

Stage Schema
------------
verify_running_image:

    images (list): Image(s) that should be running on the device. If not
        using verify_md5 then this should be the image path on the device.
        If using verify_md5 then this should be the original image location
        from the linux server.

    verify_md5 (dict, optional): When this dictionary is defined, the image
            verification will by done by comparing the MD5 hashes of the
            running image against the expected image.

        hostname (str): Linux server that is used to generate the MD5
            hashes. This server must exist in the testbed servers block.

        timeout (int, optional): Maximum time in seconds allowed for the
            hashes to generate. Defaults to 60.

Example
-------
verify_running_image:
    images:
        - test_image.bin
"""

    # =================
    # Argument Defaults
    # =================
    VERIFY_MD5 = None
    VERIFY_MD5_TIMEOUT = 60

    # ============
    # Stage Schema
    # ============
    schema = {
        'images': list,
        Optional('verify_md5'): {
            'hostname': str,
            Optional('timeout'): int
        }
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'verify_running_image'
    ]

    def verify_running_image(self, steps, device, images, verify_md5=VERIFY_MD5):
        if verify_md5:
            # Set default if not provided
            timeout = verify_md5.setdefault('timeout', self.VERIFY_MD5_TIMEOUT)
            hostname = verify_md5['hostname']

            try:
                server = device.api.convert_server_to_linux_device(hostname)
            except AttributeError:
                self.failed("The hostname '{}' provided does not exist in the "
                               "testbed servers block".format(hostname))

            with steps.start("Generate the MD5 hash of the image(s) on {}"
                             "".format(server.name)) as step:

                try:
                    server.connect()
                except Exception as e:
                    step.failed("Failed to connect to {}.\nError: {}".format(hostname, e))

                server_hashes = {}

                # Generate the hash for each image
                for image in images:
                    with step.start("Generating the MD5 hash for '{}'"
                                    "".format(image)) as substep:

                        hash_ = server.api.get_md5_hash_of_file(
                            image, timeout=timeout)

                        if hash_:
                            server_hashes[image] = hash_
                            substep.passed("The MD5 has for '{}' is '{}'"
                                           .format(image, hash_))
                        else:
                            substep.failed("Failed to get MD5 hash for {}"
                                           .format(image))

            with steps.start("Get the running image(s) on {}"
                             "".format(device.name)) as step:

                running_images = device.api.get_running_image()
                if not running_images:
                    step.failed("Failed to get running image(s)")

                if not isinstance(running_images, list):
                    running_images = [running_images]

                step.passed("The running image(s) are: {}".format(running_images))

            with steps.start("Generate the MD5 hash of the running image(s) "
                             "on {}".format(device.name)) as step:

                running_image_hashes = {}

                for image in running_images:
                    with step.start("Generating the MD5 hash for '{}'"
                                    "".format(image)) as substep:

                        hash_ = device.api.get_md5_hash_of_file(
                            image, timeout=timeout)

                        if hash_:
                            running_image_hashes[image] = hash_
                            substep.passed("The MD5 hash for '{}' is '{}'"
                                           .format(image, hash_))
                        else:
                            substep.failed("Failed to get MD5 hash for {}"
                                           .format(image))

            with steps.start("Compare the hashes from the origin to the running "
                             "images") as step:

                # Values must be compared since the path or name
                # of the image can be different
                if set(server_hashes.values()) == set(running_image_hashes.values()):
                    step.passed("The hashes from the running image(s) match the "
                                "hashes from the origin server.\n"
                                "Server hash(es): {}\n"
                                "Running image hash(es): {}".format(server_hashes,
                                                                    running_image_hashes))
                else:
                    step.failed("The hashes from the running image(s) do not match "
                                "the hashes from the origin server\n"
                                "Server hash(es): {}\n"
                                "Running image hash(es): {}".format(server_hashes,
                                                                    running_image_hashes))
        else:

            # Verify via filename comparison
            with steps.start("Verify running image on device {}". \
                                     format(device.name)) as step:
                try:
                    device.api.verify_current_image(images=images)
                except Exception as e:
                    step.failed("Unable to verify running image on device {}\n{}". \
                                format(device.name, str(e)))
                else:
                    step.passed(
                        "Successfully verified running image on device {}". \
                        format(device.name))


class BackupFileOnDevice(BaseStage):
    """This stage copies an existing file on the device and prepends 'backup_'
to the start of the file name.

Stage Schema
------------
backup_file_on_device:

    copy_dir (str): Directory containing file to be backed up

    copy_file (str): File to be backed up

    overwrite (bool, optional): Overwrite the file if exists. Defaults to True.

    timeout (int, optional): Copy timeout in second. Defaults to 300.

Example
-------
backup_file_on_device:
    copy_dir: bootflash:
    copy_file: ISSUCleanGolden.cfg
"""

    # =================
    # Argument Defaults
    # =================
    OVERWRITE = True
    TIMEOUT = 300

    # ============
    # Stage Schema
    # ============
    schema = {
        'copy_dir': str,
        'copy_file': str,
        Optional('overwrite'): bool,
        Optional('timeout'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'verify_enough_available_disk_space',
        'create_backup'
    ]

    def verify_enough_available_disk_space(self, steps, device, copy_dir, copy_file):

        with steps.start("Verify there is enough disk space to create a backup "
                         "of '{copy_dir}/{copy_file}'") as step:

            file_size = device.api.get_file_size(file=f'{copy_dir}/{copy_file}')
            if not file_size:
                step.failed(f"Could not get the size of '{copy_dir}/{copy_file}'")

            avail_space = device.api.get_available_space(directory=copy_dir)
            if not avail_space:
                step.failed(f"Could not get the remaining disk space of '{copy_dir}'")

            if avail_space <= file_size:
                step.failed(f"Cannot create backup - not enough disk space.\n"
                            f"Available space: '{avail_space}'\n"
                            f"Required space: '{file_size}'")

            step.passed(f"There is enough disk space available to backup "
                        f"'{copy_dir}/{copy_file}'")

    def create_backup(self, steps, device, copy_dir, copy_file, overwrite=OVERWRITE,
                      timeout=TIMEOUT):

        with steps.start(f"Create a backup of '{copy_dir}/{copy_file}'") as step:

            overwrite_dialog = Dialog([
                Statement(
                    pattern=r'.*over\s*write.*',
                    action='sendline({})'.format('y' if overwrite else 'n'),
                    loop_continue=True,
                    continue_timer=False
                )
            ])

            try:
                device.copy(source=copy_dir,
                            source_file=copy_file,
                            dest=copy_dir,
                            dest_file=f"backup_{copy_file}",
                            reply=overwrite_dialog,
                            timeout=timeout)
            except Exception as e:
                step.failed("Failed to create a backup.", from_exception=e)

            step.passed("Successfully created the backup.")


class DeleteBackupFromDevice(BaseStage):
    """This stage removes a backed up file from the device. It can optionally
replace the original file with the one that was backed up.

Stage Schema
------------
delete_backup_from_device:

    delete_dir (str): Directory containing file to be deleted

    delete_dir_stby (str, optional): For high availability devices, the directory
        containing file to be deleted on standby. Defaults to None.

    delete_file (str): File to be deleted

    restore_from_backup (bool, optional): Restore the file from backup file.
        Defaults to False.

    overwrite (bool, optional): When creating the backup, overwrite the file
        if one with the same name already exists. Defaults to True.

    timeout (int, optional): Timeout in seconds for copying. Defaults to 300.

Example
-------
delete_backup_from_device:
    delete_dir: 'bootflash:'
    delete_dir_stby: 'bootflash-stby:'
    delete_file: ISSUCleanGolden.cfg_backup
"""

    # =================
    # Argument Defaults
    # =================
    DELETE_DIR_STBY = None
    RESTORE_FROM_BACKUP = False
    OVERWRITE = True
    TIMEOUT = 300

    # ============
    # Stage Schema
    # ============
    schema = {
        'delete_dir': str,
        Optional('delete_dir_stby'): str,
        'delete_file': str,
        Optional('restore_from_backup'): bool,
        Optional('overwrite'): bool,
        Optional('timeout'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'restore_backup',
        'delete_file',
        'delete_file_on_stby'
    ]

    delete_dialog = Dialog([
        Statement(pattern=r'.*Do you want to delete.*',
                  action='sendline(y)',
                  loop_continue=True,
                  continue_timer=False)
    ])

    def restore_backup(self, steps, device, delete_dir, delete_file,
                       restore_from_backup=RESTORE_FROM_BACKUP, overwrite=OVERWRITE,
                       timeout=TIMEOUT):

        if restore_from_backup:
            original_file = delete_file.strip("backup_")

            with steps.start(f"Restoring '{delete_dir}/{original_file}' from the "
                             f"backup") as step:

                overwrite_dialog = Dialog([
                    Statement(
                        pattern=r'.*over\s*write.*',
                        action='sendline({})'.format('y' if overwrite else 'n'),
                        loop_continue=True,
                        continue_timer=False
                    )
                ])

                try:
                    device.copy(source=delete_dir,
                                source_file=delete_file,
                                dest=delete_dir,
                                dest_file=original_file,
                                reply=overwrite_dialog,
                                timeout=timeout)
                except Exception as e:
                    step.failed("Failed to restore the original file.", from_exception=e)

    def delete_file(self, steps, device, delete_dir, delete_file):

        with steps.start(f"Delete '{delete_dir}/{delete_file}' from the device") as step:

            try:
                device.execute(f"delete {delete_dir}{delete_file}",
                               reply=self.delete_dialog,
                               append_error_pattern=['.*%Error.*'])
            except Exception as e:
                step.failed("Failed to delete the file.", from_exception=e)

    def delete_file_on_stby(self, steps, device, delete_dir, delete_file,
                            delete_dir_stby=DELETE_DIR_STBY):

        if device.is_ha:
            with steps.start(f"Delete '{delete_dir}/{delete_file}' from the "
                             f"standby device") as step:

                if not delete_dir_stby:
                    step.skipped("No standby directory was specified.")

                try:
                    device.execute(f"delete {delete_dir_stby}{delete_file}",
                                   reply=self.delete_dialog,
                                   append_error_pattern=['.*%Error.*'])
                except Exception as e:
                    step.failed("Failed to delete the file.", from_exception=e)


class DeleteFilesFromServer(BaseStage):
    """This stage deletes files from a server.

Stage Schema
------------
delete_files_from_server:

    server (str, optional): Hostname or address of the server. If not provided,
        uses the same server from copy_to_linux (if applicable).

    files (list, optional): List of files to delete. If not provided, uses the
        same files from copy_to_linux (if applicable).

    protocol (str, optional): Protocol used for deletion. Only ftp or sftp is
        supported. Defaults to sftp.

Example
-------
delete_files_from_server:
    server: 1.1.1.1
    files:
        - /home/cisco/kickstart.bin
    protocol: sftp

"""

    # =================
    # Argument Defaults
    # =================
    SERVER = None
    FILES = None
    PROTOCOL = 'sftp'

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('server'): str,
        Optional('files'): list,
        Optional('protocol'): Or('ftp', 'sftp'),
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'delete_files'
    ]

    def delete_files(self, steps, device, server=SERVER, files=FILES,
                     protocol=PROTOCOL):

        # pyats FU only support sftp or ftp delete
        with steps.start('Delete files from the server') as step:

            if not files:
                # Get list of files from copy_to_linux stage
                if 'CopyToLinux' in self.history:
                    log.warning("No files to delete have been specified. Will "
                                "delete the files copied from the 'copy_to_linux' "
                                "stage.")

                    files = getattr(self.history['CopyToLinux'], 'parameters', {}).\
                        get('files_copied', {})

                    # covert the stored file paths to a list of files
                    files = [files[file]['dest_path'] for file in files]

                else:
                    step.skipped("No files to delete")

            if not server:
                # Get server from copy_to_linux stage
                log.warning("No server has been specified. Will use the same "
                            "server from the 'copy_to_linux' stage.")

                if 'CopyToLinux' in self.history:
                    server = getattr(self.history['CopyToLinux'], 'parameters', {}).\
                        get('destination', {}).get('hostname')

                else:
                    step.skipped("No server has been specified. Cannot delete files.")

            # establish a FileUtils session for all FileUtils operations
            fu = FileUtils(testbed=device.testbed)

            for file in files:
                with step.start(f"Deleting {file}") as substep:
                    try:
                        device.api.delete_file_on_server(
                            testbed=device.testbed,
                            path=file,
                            server=server,
                            protocol=protocol,
                            fu_session=fu)
                    except Exception as e:
                        substep.passx(f"Failed to delete '{file}'", from_exception=e)


class RevertVmSnapshot(BaseStage):
    """This stage reverts the virtual device to the provided snapshot

Stage schema
------------
revert_snapshot:

    vm_hostname (str, optional): Name of the VM that is on the ESXi
        server, if not provided, it will be set as the device name.

    esxi_server (str): ESXI Server which holds the vm to revert the
        snapshot.

    recovery_snapshot_name (str): Name of the snapshot to have VM
        reverted back to.

    max_recovery_attempts (int, optional): Maximum number of recovery
        attempts. Defaults to 2.

    sleep_after_powering_off (int, optional): Wait time after powering
        off devices. Default value is 60 seconds.

    sleep_time_stabilize_device (int, optional): Wait time before
        finishing revert snapshot stage. Defaults to 300.

    sleep_time_after_powering_on (int, optional): Wait time after
        powering on devices to reach steady state. Defaults to 600.

Example
-------
revert_vm_snapshot:
    esxi_server: ssr-ucs2
    vm_hostname: P1-4
    max_recovery_attempts: 2
    sleep_after_powering_off: 60
    sleep_time_after_powering_on: 600
    sleep_time_stabilize_device: 300
    recovery_snapshot_name: golden
"""

    # =================
    # Argument Defaults
    # =================
    VM_HOSTNAME = ""
    MAX_RECOVERY_ATTEMPTS = 2
    SLEEP_TIME_AFTER_POWERING_OFF = 60
    SLEEP_TIME_STABILIZE_DEVICE = 300
    SLEEP_TIME_AFTER_POWERING_ON = 600

    # ============
    # Stage Schema
    # ============
    schema = {
        'esxi_server': str,
        'recovery_snapshot_name': str,
        Optional('vm_hostname'): str,
        Optional('max_recovery_attempts'): int,
        Optional('sleep_time_after_powering_off'): int,
        Optional('sleep_time_after_powering_on'): int,
        Optional('sleep_time_stabilize_device'): int
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'revert_vm_snapshot'
    ]

    def revert_vm_snapshot(self, steps, device, esxi_server, recovery_snapshot_name,
                           max_recovery_attempts=MAX_RECOVERY_ATTEMPTS,
                           vm_hostname=VM_HOSTNAME,
                           sleep_time_after_powering_off=SLEEP_TIME_AFTER_POWERING_OFF,
                           sleep_time_stabilize_device=SLEEP_TIME_STABILIZE_DEVICE,
                           sleep_time_after_powering_on=SLEEP_TIME_AFTER_POWERING_ON):
        tb = device.testbed

        # If vm_hostname is not provided, set it as the device name
        if not vm_hostname:
            vm_hostname = device.name

        with steps.start("Check if {server} exists in the testbed YAML file".\
            format(server=esxi_server)) as step:

            # Check if esxi_server device is provided
            if esxi_server not in tb.devices:
                step.failed("{} device is not found in testbed YAML file".\
                    format(esxi_server))
            else:
                server = tb.devices[esxi_server]
                step.passed("Verified that {esxi_server} is specified in testbed "
                            "YAML file".format(esxi_server=server.name))

        # Start snapshot recovery
        with steps.start("Launching snapshot recovery on server: {server}".\
            format(server=server.name)) as step:

            # Try reverting snapshot for max_recovery_attempts of times
            for attempt in range(1, max_recovery_attempts + 1):
                log.info("Attempt {n}: Starting recovery of device {dev}".\
                    format(n=attempt, dev=device.name))

                # String to store error message to print out if substep step failed
                # in max_recovery_attempt
                error_msg = ""

                # Boolean flag indicating the connection to the ESXi server
                connected_to_esxi_server = True
                with step.start("Connecting to ESXi server {server}...".\
                    format(server=server.name), continue_=True) as substep:
                    try:
                        # Connect to the esxi server
                        server.connect()
                    except Exception as err:
                        connected_to_esxi_server = False
                        error_msg = str(err)
                        substep.failed("Could not connect to ESXi server "
                                           "{server} due to error: {err}".\
                                               format(server=server.name,
                                                      err=str(err)))

                    substep.passed(
                        "Successfully connected to ESXi server {server}".\
                            format(server=server.name))

                if not connected_to_esxi_server and attempt == max_recovery_attempts + 1:
                    step.failed("Failed to connect to ESXi server {server} with "
                                "error: {err}".format(server=server.name,
                                                      err=error_msg))
                elif not connected_to_esxi_server:
                    continue

                with step.start("Get VM on ESXI server {server}".\
                    format(server=server.name), continue_=True) as substep:

                    # Get VM instance
                    server_vm = server.api.\
                        get_server_vm(vm_hostname=vm_hostname)

                    if not server_vm:
                        # Destroy session
                        server.destroy()
                        substep.failed("Could not get VM {vm} on ESXi server "
                                       "{server}".format(vm=vm_hostname,
                                                         server=server.name))

                    substep.passed(
                        "Successfully obtained VM instance {vm} on ESXi "
                        "server {server}".format(vm=vm_hostname,
                                                 server=server.name))

                if not server_vm and attempt == max_recovery_attempts + 1:
                    step.failed("Failed to get VM {vm} on ESXi server {server}".\
                        format(vm=vm_hostname,
                               server=server.name))
                elif not server_vm:
                    continue

                # Boolean flag to indicating whether we caught any erros when
                # switching power of the VM
                power_switch_errored = False
                with step.start("Checking the power state of the VM {vm}".\
                    format(vm=vm_hostname), continue_=True) as substep:

                    # Check power state of the VM
                    dev_power_state = server.api.\
                        get_vm_power_state(vm_name=vm_hostname,
                                           vm_id=server_vm.get(vm_hostname)\
                                               .get('vmid'))
                    if not dev_power_state:
                        # Destroy session
                        server.destroy()
                        substep.failed("Failed to get power state of VM {vm}".\
                                format(vm=vm_hostname))

                    if dev_power_state == 'ON':
                        # Power off device
                        log.info('Powering off device {dev}'.\
                            format(dev=vm_hostname))

                        try:
                            server.api.switch_vm_power(
                                vm_id=server_vm.get(vm_hostname).get('vmid'),
                                state='off')
                        except Exception as err:
                            server.destroy()
                            power_switch_errored = True
                            error_msg = str(err)
                            substep.failed("Could not power {state} VM {vm} "
                                           "with error: {err}".\
                                               format(state='off',
                                                      vm=vm_hostname,
                                                      err=str(err)))

                        # Wait $sleep_time second after powering off device
                        log.info('Waiting {sec} seconds after powering '
                                'off device {dev}'.\
                                    format(dev=vm_hostname,
                                           sec=sleep_time_after_powering_off))
                        time.sleep(sleep_time_after_powering_off)
                    else:
                        log.info("Device {dev} is already off".\
                            format(dev=vm_hostname))

                    substep.passed("Device {dev} was powered off".\
                                format(dev=vm_hostname))

                if not dev_power_state and attempt == max_recovery_attempts + 1:
                    step.failed("Failed to get power state of VM {vm}".\
                        format(vm=vm_hostname))
                elif power_switch_errored and attempt == max_recovery_attempts + 1:
                    step.failed("Failed to power {state} of VM {vm} with error: "
                                "{err}".format(state='off',
                                               vm=vm_hostname,
                                               err=error_msg))
                elif not dev_power_state or power_switch_errored:
                    continue

                with step.start("Get device snapshot ID",
                                continue_=True) as substep:
                    # Get device snapshot id
                    vmid = server_vm.get(vm_hostname).get('vmid')
                    vm_snapshot_id = server.api.get_vm_snapshot(
                        vm_name=vm_hostname,
                        vm_id=vmid,
                        snapshot_name=recovery_snapshot_name)

                    if not vm_snapshot_id:
                        # Destroy session
                        server.destroy()
                        substep.failed("Failed to get snapshot {snapshot} on VM"
                                       " {vm}".\
                                           format(snapshot=recovery_snapshot_name,
                                                  vm=vm_hostname))

                    substep.passed("Successfully obtained snpashot id {id} for "
                                   "snapshot {snapshot} on VM {vm}".\
                                       format(id=vm_snapshot_id,
                                              snapshot=recovery_snapshot_name,
                                              vm=vm_hostname))

                if not vm_snapshot_id and attempt == max_recovery_attempts + 1:
                    step.failed("Failed to get snapshot {snapshot} on VM {vm}".\
                        format(snapshot=recovery_snapshot_name,
                               vm=vm_hostname))
                elif not vm_snapshot_id:
                    continue

                # Boolean flag to indicate whether VM has been reverted to given snapshot
                reverted_to_snapshot = True
                with step.start('Revert to snapshot {snapshot} for instance {dev}'.\
                    format(snapshot=recovery_snapshot_name,
                           dev=vm_hostname), continue_=True) as substep:
                    try:
                        # Revert to snapshot
                        server.api.revert_vm_snapshot(
                            vm_name=vm_hostname,
                            vm_id=vmid,
                            vm_snapshot_id=vm_snapshot_id,
                            snapshot_name=recovery_snapshot_name)
                    except Exception as err:
                        # Destroy session
                        server.destroy()
                        reverted_to_snapshot = False
                        error_msg = str(err)
                        substep.failed("Failed to revert back to snapshot "
                                       "{snapshot} on VM {vm} with error: {err}".\
                                           format(snapshot=recovery_snapshot_name,
                                                  vm=vm_hostname,
                                                  err=str(err)))

                    substep.passed(
                        "Successfully reverted to snapshot {snapshot} on"
                        "VM {vm}".format(snapshot=recovery_snapshot_name,
                                         vm=vm_hostname))

                if not reverted_to_snapshot and attempt == max_recovery_attempts + 1:
                    step.failed("Failed to revert back to snapshot")
                elif not reverted_to_snapshot:
                    continue

                power_switch_errored = False
                with step.start("Powering on device {dev}".\
                    format(dev=vm_hostname), continue_=True) as substep:
                    try:
                        # Power on device
                        server.api.switch_vm_power(
                            vm_id=server_vm.get(vm_hostname).get('vmid'),
                            state='on')

                    except Exception as err:
                        # Destroy session
                        server.destroy()
                        power_switch_errored = True
                        error_msg = str(err)
                        substep.failed("Could not power {state} VM {vm} with "
                                       "error: {err}".format(state='on',
                                                             vm=vm_hostname,
                                                             err=str(err)))

                    substep.passed("Successfully powered on device {dev}".\
                        format(dev=vm_hostname))

                if power_switch_errored and attempt == max_recovery_attempts + 1:
                    step.failed("Failed to power {state} VM {vm} with error: {err}".\
                        format(state='on',
                               vm=vm_hostname,
                               err=error_msg))
                elif power_switch_errored:
                    continue

                # Wait $sleep_after_powering_on seconds after powering on device
                log.info('Waiting {sec} seconds after powering on device to'
                         ' reach steady state'.\
                             format(sec=sleep_time_after_powering_on))
                time.sleep(sleep_time_after_powering_on)

                # Boolean flag to check the connection to VM
                connected_to_dev = True
                with step.start("Attempting to connect to {dev} after power on".\
                    format(dev=vm_hostname), continue_=True) as substep:
                    try:
                        # Connect to device to make sure device is powered on successfully
                        device.connect(learn_hostname=True)
                    except Exception as err:
                        connected_to_dev = False
                        error_msg = str(err)
                        substep.failed('Could not connect to {dev} after '
                                       'recovery: {err}'.format(dev=device.name,
                                                                err=str(err)))

                    # Disconnect from device
                    log.info("Disconnect from {dev}".format(dev=device.name))
                    try:
                        device.destroy()
                    except Exception:
                        # Do nothing as we dont care if the destroy fails as long as
                        #  we can connect
                        pass

                    substep.passed(
                        "Successfully connected to and disconnected from"
                        " device {dev}".format(dev=device.name))

                if not connected_to_dev and attempt == max_recovery_attempts + 1:
                    step.failed("Failed to connect to device {dev}")
                elif not connected_to_dev:
                    continue

                # Wait for $sleep_stabilize_device for VM to stablize
                log.info('Waiting {sec} seconds to reach steady state'.\
                    format(sec=sleep_time_stabilize_device))
                time.sleep(sleep_time_stabilize_device)

                # Destroy session at the end
                server.destroy()
                step.passed("Successfully reverted {dev} to snapshot {snapshot}".\
                    format(dev=device.name,
                           snapshot=recovery_snapshot_name))

            else:
                if server:
                    server.destroy()
                step.failed('Recovery failed after {n} attempts '.\
                    format(n=max_recovery_attempts))


class PowerCycle(BaseStage):
    """This stage power cycles the device

Stage schema
------------
power_cycle:

    sleep_after_power_off (int, optional): Time in seconds to sleep
        after powering off the device. Defaults to 30.

    boot_timeout (int, optional): Max time in seconds allowed for the
        device to boot. Defaults to 600.

Example
-------
power_cycle:
    sleep_after_power_off: 5
"""

    # =================
    # Argument Defaults
    # =================
    SLEEP_AFTER_POWER_OFF = 30
    BOOT_TIMEOUT = 600

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('sleep_after_power_off'): int,
        Optional('boot_timeout'): int
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'powercycle',
        'reconnect'
    ]

    def powercycle(self, steps, device, sleep_after_power_off=SLEEP_AFTER_POWER_OFF):

        with steps.start(f"Powercycling '{device.name}'") as step:
            try:
                device.api.execute_power_cycle_device(delay=sleep_after_power_off)
            except Exception as e:
                step.failed("Failed to powercycle", from_exception=e)

    def reconnect(self, steps, device, boot_timeout=BOOT_TIMEOUT):

        with steps.start(f"Reconnecting to '{device.name}'") as step:

            timeout = Timeout(boot_timeout, 60)
            while timeout.iterate():
                timeout.sleep()
                device.destroy()

                try:
                    device.connect(learn_hostname=True)
                except Exception as e:
                    connect_exception = e
                    log.info("Could not reconnect")
                else:
                    step.passed("Reconnected")

            step.failed("Could not reconnect", from_exception=connect_exception)
