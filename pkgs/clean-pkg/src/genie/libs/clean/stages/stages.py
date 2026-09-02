# Python
import re
import time
import shutil
import os.path
import fnmatch
import hashlib
import logging
import ipaddress
from typing import List

# Genie
from genie.utils.timeout import Timeout
from genie.libs.clean import BaseStage
from genie.libs.clean.utils import (_apply_configuration, find_clean_variable,
                                    verify_num_images_provided,
                                    remove_string_from_image, raise_)
from genie.metaparser.util.schemaengine import Optional, Required, Any, Or, ListOf
from genie.metaparser.util.exceptions import SchemaEmptyParserError

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
    ALIAS = None
    TIMEOUT = 200
    RETRY_TIMEOUT = 0
    RETRY_INTERVAL = 0

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('via',
                 description="Which connection to use from the testbed file. Uses the default connection if not specified."):
        str,
        Optional('alias', description="Which connection alias to use."):
        str,
        Optional('timeout',
                 description=f"The timeout for the connection to complete in seconds. Defaults to {TIMEOUT}.",
                 default=TIMEOUT):
        Or(str, int),
        Optional('retry_timeout',
                 description=f"Overall timeout for retry mechanism in seconds. Defaults to {RETRY_TIMEOUT} which means no retry.",
                 default=RETRY_TIMEOUT):
        Or(str, int, float),
        Optional('retry_interval',
                 description=f"Interval for retry mechanism in seconds. Defaults to {RETRY_INTERVAL} which means no retry.",
                 default=RETRY_INTERVAL):
        Or(str, int, float),
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = ['connect']

    def connect(self,
                steps,
                device,
                via=VIA,
                alias=ALIAS,
                timeout=TIMEOUT,
                retry_timeout=RETRY_TIMEOUT,
                retry_interval=RETRY_INTERVAL):

        with steps.start("Connecting to the device") as step:

            log.info('Checking connection to device: %s' % device.name)

            # Create a timeout that will loop
            retry_timeout = Timeout(float(retry_timeout),
                                    float(retry_interval))
            retry_timeout.one_more_time = True
            # Without this we see 'Performing the last attempt' even if retry
            # is not being used.
            retry_timeout.disable_log = True

            while retry_timeout.iterate():
                retry_timeout.disable_log = False

                device.instantiate(connection_timeout=timeout,
                                   learn_hostname=True,
                                   prompt_recovery=True,
                                   via=via,
                                   alias=alias)

                try:
                    if alias:
                        getattr(device, alias).connect()
                    else:
                        device.connect()
                except Exception:
                    log.error("Connection to the device failed", exc_info=True)
                    device.destroy_all()
                    # Loop
                else:
                    step.passed("Successfully connected".format(device.name))
                    # Don't loop

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
    exec_order = ['ping_server']

    def ping_server(self,
                    steps,
                    device,
                    server,
                    vrf=VRF,
                    timeout=TIMEOUT,
                    min_success_rate=MIN_SUCCESS_RATE,
                    max_attempts=MAX_ATTEMPTS,
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
                    if 'Requested protocol was not running during ping' in str(
                            err):
                        step.failed(
                            'No IP routing (or other relevant protocol) '
                            'configured, not retrying')
                    else:
                        # Success rate is 0%
                        log.warning(
                            f"Unable to meet minimum ping success rate "
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
                step.failed(
                    f"'{server}' is not reachable after {max_attempts} "
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
    exec_order = ['copy_to_linux']

    def copy_to_linux(self,
                      steps,
                      device,
                      origin,
                      destination,
                      protocol=PROTOCOL,
                      timeout=TIMEOUT,
                      check_image_length=CHECK_IMAGE_LENGTH,
                      overwrite=OVERWRITE,
                      append_hostname=APPEND_HOSTNAME,
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
        with steps.start("Collecting file info on origin and '{d}' "
                         "before copy".format(
                             d=destination_hostname or dest_dir)) as step:
            file_size = -1
            for index, file in enumerate(origin_path):
                with step.start(
                        "Collecting '{f}' info".format(f=file)) as substep:
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
                                "Could not verify the size for file '{}'.\nError: {}"
                                .format(file, e))

                    # file to copy is local
                    else:
                        try:
                            file_size = os.path.getsize(file)
                        except FileNotFoundError:
                            step.failed("Can not find file {} on local server."
                                        "Terminating clean".format(file))
                        except Exception as e:
                            log.warning(
                                "Could not verify the size for file '{}' due to {}"
                                .format(file, e))

                    if rename_images:
                        new_filename = rename_images + '_' + str(
                            index) if index else rename_images

                    else:
                        new_filename = None

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
                            new_name=new_filename)
                    except Exception as e:
                        log.exception('Cannot change filename')
                        step.failed(
                            "Can not change file name. Terminating clean:\n{e}"
                            .format(e=e))

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
                                    file_path, destination_hostname
                                    or dest_dir, str(e)))
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

                    with step.start("Verify stability of '{f}'".format(
                            f=file)) as substep:

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

        with steps.start("Copying the files to {}".format(
                destination_hostname or dest_dir)) as step:
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
                                    server=fu.get_hostname(
                                        destination_hostname),
                                    protocol=protocol,
                                    timeout=timeout,
                                    quiet=True)
                            elif destination_hostname:
                                device.api.copy_to_server(
                                    testbed=device.testbed,
                                    remote_path=file_data['dest_path'],
                                    local_path=file,
                                    server=fu.get_hostname(
                                        destination_hostname),
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
                                log.info(
                                    "Sleeping for {} seconds before retrying".
                                    format(copy_attempts_sleep))
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
                        'CopyToLinux'].parameters.setdefault(
                            'files_copied', {})
                    history.update({file: file_data})

        # verify file copied section below
        with steps.start(
                "Verify the files have been copied correctly") as step:
            if protocol.lower() in ['tftp', 'scp']:
                step.skipped(
                    'tftp protocol does not support check file size, skipping this step.'
                )

            if 'files_copied' not in self.history['CopyToLinux'].parameters:
                step.skipped(
                    'No files was copied in previous steps, skipping this step.'
                )

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
                            step.failed(
                                "File size is not the same on the origin"
                                " and on the file server")
                        else:
                            step.passed("File size is the same on the origin "
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

    connection_alias (str): Connection alias to use

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

    overwrite_if_size_different (bool, optional): Overwrite the file if a file with
        the same name exists but size is different. Defaults to False.

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

    prompt_recovery(bool, optional): Enable the prompt recovery when the  execution
        command timeout. Defaults to False.

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
    OVERWRITE_IF_SIZE_DIFFERENT = False
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
    PROMPT_RECOVERY = False
    PROTOCOL = 'https'
    CONNECTION_ALIAS = 'default'

    # ============
    # Stage Schema
    # ============
    schema = {
        'origin': {
            Optional('files',
                     description="Image files location on the server."):
            list,
            Optional('hostname',
                     description="Hostname or address of the server."):
            str
        },
        'destination': {
            Required('directory',
                     description="Directory on the device to copy the images to."):
            str,
            Optional('standby_directory',
                     description="Standby directory on the device to copy the images to"):
            str,
            Optional('stack_directory',
                     description="Stack directories on the device to copy the images to"):
            list
        },
        Optional('protocol',
                 description="Protocol used for copy operation.",
                 default=PROTOCOL):
        str,
        Optional('connection_alias',
                 description='Connection alias to use',
                 default='default'):
        str,
        Optional('verify_num_images',
                 description="Verify number of images provided by user for clean is correct.",
                 default=VERIFY_NUM_IMAGES):
        bool,
        Optional('expected_num_images',
                 description="Number of images expected to be provided by user for clean.",
                 default=EXPECTED_NUM_IMAGES):
        int,
        Optional('vrf',
                 description="Vrf used to copy. Defaults to an empty string.",
                 default=VRF):
        str,
        Optional('timeout',
                 description="Copy operation timeout in seconds.",
                 default=TIMEOUT):
        int,
        Optional('compact',
                 description="Compact copy mode if supported by the device.",
                 default=COMPACT):
        bool,
        Optional('use_kstack',
                 description="Use faster version of copy with limited options.",
                 default=USE_KSTACK):
        bool,
        Optional('protected_files',
                 description="File patterns that should not be deleted.",
                 default=PROTECTED_FILES):
        list,
        Optional('overwrite',
                 description="Overwrite the file if a file with the same name already exists.",
                 default=OVERWRITE):
        bool,
        Optional('overwrite_if_size_different',
                 description="Overwrite the file if a file with the same name exists but size is different.",
                 default=OVERWRITE_IF_SIZE_DIFFERENT):
        bool,
        Optional('skip_deletion',
                 description="Do not delete any files even if there isn't any space on device.",
                 default=SKIP_DELETION):
        bool,
        Optional('copy_attempts',
                 description="Number of times to attempt copying image files.",
                 default=COPY_ATTEMPTS):
        int,
        Optional('copy_attempts_sleep',
                 description="Number of seconds to sleep between copy_attempts.",
                 default=COPY_ATTEMPTS_SLEEP):
        int,
        Optional('check_file_stability',
                 description="Verifies that the file size is not changing. This ensures the image is not actively being copied.",
                 default=CHECK_FILE_STABILITY):
        bool,
        Optional('stability_check_tries',
                 description="Max number of checks that can be done when checking file stability.",
                 default=STABILITY_CHECK_TRIES):
        int,
        Optional('stability_check_delay',
                 description="Delay between tries when checking file stability in seconds.",
                 default=STABILITY_CHECK_DELAY):
        int,
        Optional('min_free_space_percent',
                 description="Percentage of total disk space that must be free. If specified the percentage is not free then the stage will attempt to delete unprotected files to reach the minimum percentage.",
                 default=MIN_FREE_SPACE_PERCENT):
        int,
        Optional('interface',
                 description="The interface to use for file transfers, may be needed for copying files on some IOSXE platforms, such as ASR1K when using a VRF.",
                 default=INTERFACE):
        str,
        Optional('unique_file_name',
                 description="Appends a random six-digit number to the end of the image name.",
                 default=UNIQUE_FILE_NAME):
        bool,
        Optional('unique_number',
                 description="Appends the provided number to the end of the image name. Requires unique_file_name is True to be applied.",
                 default=UNIQUE_NUMBER):
        int,
        Optional('rename_images',
                 description="Rename the image to the provided name. If multiple files exist then an incrementing number is also appended.",
                 default=RENAME_IMAGES):
        str,
        Optional('prompt_recovery',
                 description="Enable the prompt recovery when the  execution command timeout.",
                 default=PROMPT_RECOVERY):
        bool
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = ['copy_to_device']

    def copy_to_device(self,
                       steps,
                       device,
                       origin,
                       destination,
                       protocol=PROTOCOL,
                       connection_alias=CONNECTION_ALIAS,
                       verify_num_images=VERIFY_NUM_IMAGES,
                       expected_num_images=EXPECTED_NUM_IMAGES,
                       vrf=VRF,
                       timeout=TIMEOUT,
                       compact=COMPACT,
                       use_kstack=USE_KSTACK,
                       protected_files=PROTECTED_FILES,
                       overwrite=OVERWRITE,
                       overwrite_if_size_different=OVERWRITE_IF_SIZE_DIFFERENT,
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
                       prompt_recovery=PROMPT_RECOVERY,
                       **kwargs):
        log.info(
            "Section steps:\n1- Verify correct number of images provided"
            "\n2- Get filesize of image files"
            "\n3- Check if image files already exist on device"
            "\n4- (Optional) Verify stability of image files"
            "\n5- Verify free space on device else delete unprotected files"
            "\n6- Copy image files to device"
            "\n7- Verify copied image files are present on device")

        if connection_alias:
            log.info(f'Using connection alias {connection_alias}')

        with device.temp_default_alias(connection_alias):

            # list of destination directories
            destinations = []

            # Establish FileUtils session for all FileUtils operations
            file_utils = FileUtils(testbed=device.testbed)

            # Get args
            server = origin.get('hostname')

            image_files = origin['files']

            if server:
                # Check remote server info present in testbed YAML
                if not file_utils.get_server_block(server):
                    self.failed(
                        "Server '{}' was provided in the clean yaml file but "
                        "doesn't exist in the testbed file.\n".format(server))

                string_to_remove = file_utils.get_server_block(server).get(
                    'path', '')
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

            if 'stack_directory' in destination:
                destination_stack = destination['stack_directory']
                for member_dir in destination_stack:
                    destinations.append(member_dir)

            # Check image files provided
            if verify_num_images:
                # Verify correct number of images provided
                with steps.start(
                        "Verify correct number of images provided") as step:
                    if not verify_num_images_provided(
                            image_list=image_files,
                            expected_images=expected_num_images):
                        step.failed(
                            "Incorrect number of images provided. Please "
                            "provide {} expected image(s) under destination"
                            ".path in clean yaml file.\n".format(
                                expected_num_images))
                    else:
                        step.passed("Correct number of images provided")

            # Loop over all image files provided by user
            for index, file in enumerate(image_files):
                # Init
                files_to_copy = {}
                unknown_size = False

                file_size = None

                # try to get file size from file directly
                with steps.start(f"Get filesize of '{file}'") as step:
                    try:
                        file_size = os.stat(file).st_size
                    except Exception:
                        step.passx('Failed to get file size')

                if not file_size and server:
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
                                "Can not find file {} on server {}. Terminating clean"
                                .format(file, server))
                        except Exception as e:
                            log.warning(str(e))
                            # Something went wrong, set file_size to -1
                            file_size = -1
                            unknown_size = True
                            err_msg = "\nUnable to get filesize for file '{}' on "\
                                    "remote server {}".format(file, server)
                            if overwrite:
                                err_msg += " - will copy file to device"
                            if overwrite_if_size_different:
                                err_msg += " - will copy file to device if size is different"
                            step.passx(err_msg)
                        else:
                            step.passed("Verified filesize of file '{}' to be "
                                        "{} bytes".format(file, file_size))
                else:
                    log.info(f'Local file has size {file_size}')

                for dest in destinations:

                    # Check if file with same name and size exists on device
                    dest_file_path = os.path.join(dest, os.path.basename(file))
                    image_mapping = self.history[
                        'CopyToDevice'].parameters.setdefault(
                            'image_mapping', {})
                    image_mapping.update(
                        {origin['files'][index]: dest_file_path})
                    with steps.start("Check if file '{}' exists on device {} {}".\
                                    format(dest_file_path, device.name, dest)) as step:
                        # Execute 'dir' before copying image files
                        dir_before = device.execute('dir {}'.format(dest))

                        # Check if file exists
                        try:
                            exist = device.api.verify_file_exists(
                                file=dest_file_path,
                                size=file_size,
                                dir_output=dir_before)
                        except Exception as e:
                            exist = False
                            log.warning(
                                "Unable to check if image '{}' exists on device {} {}."
                                "Error: {}".format(dest_file_path, device.name,
                                                   dest, str(e)))
                        name_exists = False
                        try:
                            if os.path.basename(dest_file_path) in dir_before:
                                name_exists = True
                        except Exception:
                            name_exists = False
                        if name_exists and not exist and not (unique_file_name or unique_number or rename_images):
                            if not overwrite_if_size_different:
                                step.failed(
                                    f"The file '{dest_file_path}' already exists on device {device.name} {dest} with a different size. "
                                    f"Set overwrite_if_size_different as True to proceed with copying the image to the device."
                                )
                            else:
                                file_copy_info = {
                                    file: {
                                        'size': file_size,
                                        'dest_path': dest_file_path,
                                        'size_mismatch': True, # Flag to indicate this is a size mismatch scenario
                                        'exist': False,
                                    }
                                }
                                files_to_copy.update(file_copy_info)
                                step.passed(
                                    f"Destination file '{dest_file_path}' exists with different size on device {device.name} {dest}. "
                                    "overwrite_if_size_different is True, Proceeding with copying image to device."
                                )
                        elif (not exist) or (exist and overwrite) or (
                                exist and (unique_file_name or unique_number
                                           or rename_images)):
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
                                "skipping copy".format(file, device.name,
                                                       dest))

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
                                            "Size of file '{}' is stable".
                                            format(file))
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
                                            file_data in files_to_copy.values()) if files_to_copy else file_size or -1

                            try:
                                free_space = device.api.free_up_disk_space(
                                    destination=dest,
                                    required_size=total_size,
                                    skip_deletion=skip_deletion,
                                    protected_files=protected_files,
                                    min_free_space_percent=
                                    min_free_space_percent,
                                    dir_output=dir_before,
                                    allow_deletion_failure=True)
                                if not free_space:
                                    step.failed("Unable to create enough space for "
                                                "image on device {} {}".\
                                                format(device.name, dest))
                                else:
                                    step.passed(
                                        "Device {} {} has sufficient space to "
                                        "copy images".format(
                                            device.name, dest))
                            except Exception as e:
                                log.error(str(e))
                                step.failed("Error while creating free space for "
                                            "image on device {} {}".\
                                            format(device.name, dest))
                        else:
                            step.skipped(
                                f"Skip verifying free space on the device '{device.name}'"
                                " because skip_deletion is set to True")

                    # Copy the file to the devices
                    dir_output = None
                    for file, file_data in files_to_copy.items():
                        with steps.start("Copying image file {} to device {} {}".\
                                        format(file, device.name, dest)) as step:

                            # Copy file unless overwrite is False
                            if not overwrite and file_data['exist'] and not (
                                    unique_file_name or unique_number
                                    or rename_images) and not file_data.get('size_mismatch', False):
                                step.skipped(
                                    "File with the same name size exists on "
                                    "the device {} {}, skipped copying".format(
                                        device.name, dest))

                            for i in range(1, copy_attempts + 1):
                                if unique_file_name or unique_number or rename_images:

                                    log.info('renaming files for copying')
                                    if rename_images:
                                        rename_images = rename_images + '_' + str(
                                            index)

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
                                            "Can not change file name. Terminating clean:\n{e}"
                                            .format(e=e))

                                    log.info(
                                        f'Renamed {os.path.basename(file)} to {new_name}'
                                    )

                                    renamed_local_path = os.path.join(
                                        dest, new_name)

                                    renamed_file_data = {
                                        x: y
                                        for x, y in file_data.items()
                                    }
                                    renamed_file_data[
                                        'dest_path'] = renamed_local_path

                                    self.history['CopyToDevice'].parameters[
                                        'image_mapping'][
                                            file] = renamed_local_path

                                    try:
                                        force_overwrite = overwrite or file_data.get('size_mismatch', False)
                                        res = device.api.\
                                            copy_to_device(protocol=protocol,
                                                        server=file_utils.get_hostname(server) if server else None,
                                                        remote_path=file,
                                                        local_path=renamed_local_path,
                                                        vrf=vrf,
                                                        timeout=timeout,
                                                        compact=compact,
                                                        use_kstack=use_kstack,
                                                        interface=interface,
                                                        overwrite=force_overwrite,
                                                        prompt_recovery=prompt_recovery,
                                                        **kwargs)
                                        if not res:
                                            raise Exception(
                                                'Failed to copy file to device'
                                            )
                                    except Exception as e:
                                        # Retry attempt if user specified
                                        if i < copy_attempts:
                                            log.warning("Attempt #{}: Unable to copy {} to '{} {}' due to:\n{}".\
                                                        format(i, file, device.name, dest, e))
                                            log.info(
                                                "Sleeping for {} seconds before retrying"
                                                .format(copy_attempts_sleep))
                                            time.sleep(copy_attempts_sleep)
                                            continue
                                        else:
                                            log.error(str(e))
                                            step.failed(
                                                "Failed to copy image '{}' to '{}' on device"
                                                " '{}'\n".format(
                                                    file, dest, device.name), )
                                else:
                                    try:
                                        force_overwrite = overwrite or file_data.get('size_mismatch', False)
                                        res = device.api. \
                                            copy_to_device(protocol=protocol,
                                                        server=file_utils.get_hostname(server) if server else None,
                                                        remote_path=file,
                                                        local_path=file_data['dest_path'],
                                                        vrf=vrf,
                                                        timeout=timeout,
                                                        compact=compact,
                                                        use_kstack=use_kstack,
                                                        interface=interface,
                                                        overwrite=force_overwrite,
                                                        prompt_recovery=prompt_recovery,
                                                        **kwargs)
                                        if not res:
                                            raise Exception(
                                                'Failed to copy file to device'
                                            )
                                    except Exception as e:
                                        # Retry attempt if user specified
                                        if i < copy_attempts:
                                            log.warning("Attempt #{}: Unable to copy {} to '{} {}' due to:\n{}". \
                                                        format(i, file, device.name, dest, e))
                                            log.info(
                                                "Sleeping for {} seconds before retrying"
                                                .format(copy_attempts_sleep))
                                            time.sleep(copy_attempts_sleep)
                                            continue
                                        else:
                                            log.error(str(e))
                                            step.failed(
                                                "Failed to copy image '{}' to '{}' on device"
                                                " '{}'\n".format(
                                                    file, dest, device.name), )

                                    # After a successful copy,After detecting renamed image, If found, update file_data and image_mapping so that the
                                    # verification step checks the real on-device path, not the
                                    # originally expected path.
                                    expected_dest = file_data['dest_path']
                                    expected_basename = os.path.basename(expected_dest)

                                    try:
                                        dir_output = device.execute('dir {}'.format(dest))
                                    except Exception as e:
                                        log.warning(f"Error running 'dir {dest}' after copy: {e}. "
                                                    f"Skipping rename detection, proceeding with expected path.")
                                        dir_output = None

                                    if dir_output is not None:
                                        actual_dest_path = None

                                        # First check if the file landed at the expected location
                                        if expected_basename in dir_output:
                                            if device.api.verify_file_exists(
                                                    file=expected_dest,
                                                    size=file_data['size'],
                                                    dir_output=dir_output):
                                                actual_dest_path = expected_dest
                                                log.info(f"File found at expected location: {expected_dest}")

                                        # If not at the expected location, scan for a device-renamed copy.
                                        # We then update dest_path and
                                        # image_mapping so downstream stages use the correct on-device path.
                                        if not actual_dest_path:
                                            base_name_no_ext = os.path.splitext(expected_basename)[0]
                                            pattern = re.compile(
                                                rf'(?<!\S){re.escape(base_name_no_ext)}_\d+(?!\S)')

                                            files_before = set(pattern.findall(dir_before))
                                            files_after = set(pattern.findall(dir_output))
                                            new_files = files_after - files_before

                                            if len(new_files) == 1:
                                                renamed_file = new_files.pop()
                                                actual_dest_path = os.path.join(dest, renamed_file)
                                                log.info(f"Device renamed file during copy: {expected_dest} -> {actual_dest_path}")
                                            elif len(new_files) > 1:
                                                # Multiple new suffixed files; disambiguate by size
                                                for renamed_file in new_files:
                                                    renamed_path = os.path.join(dest, renamed_file)
                                                    if device.api.verify_file_exists(
                                                            file=renamed_path,
                                                            size=file_data['size'],
                                                            dir_output=dir_output):
                                                        actual_dest_path = renamed_path
                                                        log.info(f"Device renamed file during copy: {expected_dest} -> {actual_dest_path}")
                                                        break
                                                if not actual_dest_path:
                                                    log.warning(
                                                        f"Multiple new files found matching {base_name_no_ext}_*' but none matched "
                                                        f"expected size {file_data['size']}. Proceeding with expected path.")
                                            else:
                                                log.warning(
                                                    f"No renamed file detected for {expected_dest}. "
                                                    f"Proceeding with expected path.")

                                        # Update tracking if the device used a different filename
                                        if actual_dest_path and actual_dest_path != expected_dest:
                                            log.warning(f"Updating destination path from {expected_dest} to {actual_dest_path}")
                                            file_data['dest_path'] = actual_dest_path
                                            self.history['CopyToDevice'].parameters['image_mapping'][file] = actual_dest_path

                                log.info(
                                    "File {} has been copied to {} on device {}"
                                    " successfully".format(
                                        file, dest, device.name))
                                success_copy_ha = True
                                break

                            # Save the file copied path and size info for future use
                            history = self.history['CopyToDevice'].parameters.\
                                                setdefault('files_copied', {})

                            if unique_file_name or unique_number or rename_images:
                                history.update({file: renamed_file_data})
                            else:
                                history.update({file: file_data})

                    with steps.start(
                            "Verify images successfully copied") as step:
                        # If nothing copied don't need to verify, skip
                        if 'files_copied' not in self.history[
                                'CopyToDevice'].parameters:
                            step.skipped(
                                "Image files were not copied for {} {} in previous steps, "
                                "skipping verification steps".format(
                                    device.name, dest))

                        # Reuse the dir output from the post-copy rename detection if available,
                        # otherwise fetch it now.
                        if dir_output is None:
                            dir_output = device.execute('dir {}'.format(dest))

                        for name, image_data in self.history['CopyToDevice'].\
                                                        parameters['files_copied'].items():
                            with step.start("Verify image '{}' copied to {} on device {}".\
                                            format(image_data['dest_path'], dest, device.name)) as substep:
                                # if size is -1 it means it failed to get the size
                                if not device.api.verify_file_exists(
                                        file=image_data['dest_path'],
                                        size=image_data['size'],
                                        dir_output=dir_output):
                                    substep.failed(
                                        "Either the file failed to copy OR the local file size is different "
                                        "than the origin file size on the device {}."
                                        .format(device.name))
                                else:
                                    file_name = os.path.basename(image_data['dest_path'])
                                    if file_name not in protected_files:
                                        protected_files.append(file_name)
                                    log.info(
                                        '{file_name} added to protected list'.
                                        format(file_name=file_name))
                                    if image_data['size'] != -1:
                                        substep.passed(
                                            "File was successfully copied to device {}. "
                                            "Local file size is the same as the origin file size.".\
                                            format(device.name))
                                    else:
                                        substep.skipped(
                                            "File has been copied to device {}.Cannot verify integrity as "
                                            "the original file size is unknown."
                                            .format(device.name))


class RecoveryImage(BaseStage):
    """Copy recovery images to stable local targets for device recovery.

    Image discovery is performed by the producer of clean data.  This public
    stage only resolves the supplied server, transfers the resolved paths,
    verifies the targets, and publishes them to ``device_recovery``.

    Example
    -------
    recovery_image:
        images:
        - /images/recovery.bin
        copy_images:
        - /short/1234/recovery.bin
        golden_image:
        - bootflash:recovery.bin
        recovery_server: recovery-server
        protocol: https
        verify_size: True

    ``images`` and ``golden_image`` are paired by position. ``copy_images``
    may provide corresponding server-relative transfer paths while preserving
    ``images`` as the filesystem paths used for size or MD5 verification. If
    ``images`` is omitted and a golden-image target is configured, the stage
    consumes resolved image paths already present in clean data. If neither
    recovery-image input nor a golden-image target is configured, the stage
    skips so shared templates remain safe for devices without recovery-image
    attributes. ``verify_size`` and ``verify_md5`` require a remote image
    source so the stage can calculate the expected metadata before checking
    the device target. Size verification is faster, but unlike MD5 it cannot
    distinguish different images that have the same byte count.
    """

    PROTOCOL = 'https'
    DESTINATION = {}
    TIMEOUT = 300
    COPY_ATTEMPTS = 1
    COPY_ATTEMPTS_SLEEP = 30
    VERIFY_SIZE = False
    VERIFY_MD5 = False
    VRF = ''
    CONNECTION_ALIAS = 'default'
    UPDATE_DEVICE_RECOVERY = True
    DEFAULT_PORTS = {
        'ftp': 21,
        'http': 80,
        'https': 443,
        'scp': 22,
        'sftp': 22,
        'tftp': 69,
    }

    schema = {
        Optional('images',
                 description='Remote image paths, paired with golden_image.'):
        list,
        Optional('copy_images',
                 description='Optional server-relative transfer paths, paired '
                             'with images.'): list,
        Optional('golden_image',
                 description='Local device path used for ROMMON recovery'):
        Or(str, list),
        Optional('recovery_server',
                 description='Testbed server name or address'): str,
        Optional('recovery_server_port',
                 description='Recovery server service port.'): int,
        Optional('protocol', description='Transfer protocol.',
                 default=PROTOCOL): str,
        Optional('destination', default=DESTINATION): {
            Optional('directory'): str,
            Optional('standby_directory'): str,
            Optional('stack_directory'): list,
        },
        Optional('connection_alias', default=CONNECTION_ALIAS): str,
        Optional('vrf', default=VRF): str,
        Optional('timeout',
                 description='Transfer and remote metadata timeout in seconds.',
                 default=TIMEOUT): int,
        Optional('copy_attempts', description='Number of copy attempts.',
                 default=COPY_ATTEMPTS): int,
        Optional('copy_attempts_sleep',
                 description='Seconds between copy attempts.',
                 default=COPY_ATTEMPTS_SLEEP): int,
        Optional('verify_size',
                 description='Verify the source and device image sizes.',
                 default=VERIFY_SIZE): bool,
        Optional('verify_md5',
                 description='Verify the remote and device image digests.',
                 default=VERIFY_MD5): bool,
        Optional('prompt_recovery', default=False): bool,
        Optional('update_device_recovery', default=UPDATE_DEVICE_RECOVERY): bool,
    }

    exec_order = [
        'resolve_recovery_image',
        'resolve_recovery_server',
        'check_golden_image',
        'copy_recovery_image',
        'verify_golden_image',
        'update_device_recovery',
    ]

    @staticmethod
    def _as_list(value):
        return [] if value is None else value if isinstance(value, list) else [value]

    @staticmethod
    def _target_parts(target, default_directory):
        target = target.rstrip('/')
        separator = max(target.rfind('/'), target.rfind(':'))
        if separator == -1:
            return default_directory, target
        return target[:separator + 1], target[separator + 1:]

    @staticmethod
    def _join_device_path(directory, filename):
        if directory.endswith(':'):
            return directory + filename
        return os.path.join(directory, filename)

    @staticmethod
    def _inspection_path(path):
        """Return a device path normalized for file-inspection APIs."""
        volume, separator, filename = path.partition(':')
        if separator and filename and not filename.startswith('/'):
            return '{}:/{}'.format(volume, filename)
        return path

    @staticmethod
    def _get_platform_default_directory(device):
        try:
            directory = device.api.get_platform_default_dir()
        except Exception as error:
            raise RuntimeError(
                "Unable to determine the platform default directory: {}"
                .format(error))
        if not directory:
            raise RuntimeError("No platform default directory was found")
        return directory

    @classmethod
    def _default_port(cls, protocol):
        return cls.DEFAULT_PORTS.get(protocol.lower())

    @staticmethod
    def _service_rank(service):
        """Rank valid numeric orders ahead of unordered services."""
        try:
            order = float(service.get('order'))
        except (TypeError, ValueError):
            return (1, 0)
        return (0, order)

    @classmethod
    def _url_hostname(cls, hostname, port, protocol=PROTOCOL):
        """Return a host suitable for URL construction."""
        if not port or port == cls._default_port(protocol):
            return hostname
        if ':' in hostname and not hostname.startswith('['):
            hostname = '[{}]'.format(hostname)
        return '{}:{}'.format(hostname, port)

    @staticmethod
    def _clean_images(device):
        """Return resolved image paths already stored in clean data."""
        clean = getattr(device, 'clean', {}) or {}
        if hasattr(clean, 'get'):
            return clean.get('images', []) or []
        return getattr(clean, 'images', []) or []

    def _resolve_recovery_images(self, device, images):
        """Use paths from clean data; image discovery is outside this stage."""
        images = self._as_list(images)
        if images:
            return images

        return [image for image in self._as_list(self._clean_images(device))
                if isinstance(image, str) and image]

    def _fail_transfer(self, server, hostname, source, target, device, error):
        self.failed(
            "Unable to use {} recovery server '{}' ({}) while "
            "copying '{}' to '{}' on device '{}': {}. Verify that the "
            "server is reachable, its transfer service is available, and the "
            "server is defined correctly in the testbed.".format(
                self._recovery_context.get('protocol', '').upper(), server,
                hostname, source, target, device.name, error))

    def resolve_recovery_image(self,
                               steps,
                               device,
                               images=None,
                               copy_images=None,
                               golden_image=None,
                               recovery_server=None,
                               recovery_server_port=None,
                               protocol=PROTOCOL,
                               destination=DESTINATION):
        """Resolve the remote recovery image and local golden-image target."""
        clean = getattr(device, 'clean', {}) or {}
        device_recovery = (clean.get('device_recovery', {})
                           if hasattr(clean, 'get') else {}) or {}
        configured_golden_images = self._as_list(
            device_recovery.get('golden_image'))
        if (images is None and copy_images is None and golden_image is None and
                not configured_golden_images and recovery_server is None and
                recovery_server_port is None and not destination):
            self.skipped(
                "No recovery-image source or golden-image target was "
                "configured for device '{}'.".format(device.name))

        images = self._resolve_recovery_images(device, images)
        copy_images = self._as_list(copy_images)

        if copy_images and len(copy_images) != len(images):
            self.failed(
                "The number of copy_images paths ({}) must match the number "
                "of recovery images ({}) for device '{}'.".format(
                    len(copy_images), len(images), device.name))

        destination = destination or {}
        default_directory = destination.get('directory')
        golden_images = self._as_list(golden_image)
        if not golden_images:
            golden_images = configured_golden_images
        if not golden_images and images:
            try:
                default_directory = (default_directory or
                                     self._get_platform_default_directory(device))
            except Exception as error:
                self.failed(
                    "Unable to determine the platform default directory for "
                    "device '{}': {}".format(device.name, error))
            if not default_directory:
                self.failed(
                    "No platform default directory was found for device '{}'."
                    .format(device.name))
            if len(images) == 1:
                target_names = ['golden_image.bin']
            else:
                target_names = [
                    'golden_image_{}.bin'.format(index)
                    for index in range(1, len(images) + 1)]
            golden_images = [self._join_device_path(default_directory, name)
                             for name in target_names]
        if (golden_images and not default_directory and
                any('/' not in target and ':' not in target
                    for target in golden_images)):
            try:
                default_directory = self._get_platform_default_directory(
                    device)
            except Exception as error:
                self.failed(
                    "Unable to determine the platform default directory for "
                    "device '{}': {}".format(device.name, error))
        if not golden_images:
            self.failed(
                "No local golden_image target was found for device '{}'. "
                "Provide golden_image or device_recovery.golden_image when "
                "running without a remote recovery image.".format(device.name))
        if images and len(golden_images) != len(images):
            self.failed(
                "The number of golden_image targets ({}) must match "
                "the number of recovery images ({}) for device '{}'.".format(
                    len(golden_images), len(images), device.name))
        # Each source is paired with exactly one golden-image target.  The
        # target_sets entries are (device directories, filename) pairs.
        target_sets = []
        for target_path in golden_images:
            target_dir, target_name = self._target_parts(
                target_path, default_directory)
            target_destinations = [target_dir]
            if destination and destination.get('standby_directory'):
                target_destinations.append(destination['standby_directory'])
            target_destinations.extend((destination or {}).get(
                'stack_directory', []))
            target_sets.append((target_destinations, target_name))

        self._recovery_context = {
            'filesystem_sources': images,
            'copy_sources': copy_images or images,
            'copy_sources_explicit': bool(copy_images),
            'target': golden_images[0],
            'golden_images': golden_images,
            'target_sets': target_sets,
            'protocol': protocol.lower(),
        }

    def resolve_recovery_server(self,
                                steps,
                                device,
                                recovery_server=None,
                                recovery_server_port=None):
        """Resolve the recovery server and server-relative image path."""
        context = self._recovery_context
        if not context['filesystem_sources']:
            context.update({'recovery_server': None, 'hostname': None,
                            'file_utils': None, 'port': None})
            return
        protocol = context['protocol']
        selected_service = None
        if not recovery_server:
            candidates = []
            for server_index, (name, block) in enumerate(
                    getattr(device.testbed, 'servers', {}).items()):
                for service_index, service in enumerate(
                        (block.get('services', {}) or {}).values()):
                    if (service.get('type') != 'file_transfer' or
                            service.get('protocol', '').lower() != protocol):
                        continue
                    # Ordered services take precedence; otherwise preserve
                    # testbed server/service order as the tie-breaker.
                    candidates.append((self._service_rank(service),
                                       server_index, service_index, name,
                                       service))
            if candidates:
                _, _, _, recovery_server, selected_service = min(
                    candidates, key=lambda item: item[:3])
            else:
                self.failed(
                    "No {} recovery server was found for device '{}'. "
                    "Provide recovery_server or define a file-transfer "
                    "server in the testbed.".format(protocol.upper(),
                                                     device.name))

        source = context['filesystem_sources'][0]
        target = context['target']
        file_utils = FileUtils.from_device(device, protocol=protocol)
        try:
            server_block = file_utils.get_server_block(recovery_server)
            hostname = file_utils.get_hostname(recovery_server)
        except Exception as error:
            self._fail_transfer(recovery_server, '', source, target, device,
                                error)
        copy_sources = context['copy_sources']
        if server_block and not context['copy_sources_explicit']:
            copy_sources = remove_string_from_image(
                images=copy_sources, string=server_block.get('path', ''))
            source = copy_sources[0]

        if not hostname:
            self._fail_transfer(recovery_server, hostname, source, target,
                                device, 'no server address was resolved')

        matching_services = [
            service for service in
            (server_block or {}).get('services', {}).values()
            if (service.get('type') == 'file_transfer' and
                service.get('protocol', '').lower() == protocol)
        ]
        if selected_service is None and matching_services:
            if recovery_server_port is None:
                selected_service = min(
                    enumerate(matching_services),
                    key=lambda item: (self._service_rank(item[1]), item[0]))[1]
            else:
                selected_service = next(
                    (service for service in matching_services
                     if service.get('port') in (None, recovery_server_port)),
                    None)

        port = recovery_server_port
        if port is None and selected_service is not None:
            port = selected_service.get('port')
        if port is None:
            port = self._default_port(protocol)
        context.update({
            'recovery_server': recovery_server,
            'hostname': hostname,
            'copy_sources': copy_sources,
            'server_path': (server_block or {}).get('path', ''),
            'port': port,
            'file_utils': file_utils,
        })

    def check_golden_image(self,
                           steps,
                           device,
                           connection_alias=CONNECTION_ALIAS,
                           timeout=TIMEOUT,
                           verify_size=VERIFY_SIZE,
                           verify_md5=VERIFY_MD5):
        """Select local targets that need a FileUtils-managed copy."""
        context = self._recovery_context
        filesystem_sources = context['filesystem_sources']
        source = filesystem_sources[0] if filesystem_sources else None
        target = context['target']
        recovery_server = context['recovery_server']
        hostname = context['hostname']
        remote_sizes = []
        remote_md5s = []
        if verify_size and not source:
            self.failed(
                "verify_size requires a remote recovery image source for "
                "device '{}'.".format(device.name))
        if verify_md5 and not source:
            self.failed(
                "verify_md5 requires a remote recovery image source for "
                "device '{}'.".format(device.name))
        if source and verify_size:
            remote_size_sources = remove_string_from_image(
                images=filesystem_sources,
                string=context.get('server_path', ''))
            try:
                endpoint = self._url_hostname(
                    hostname, context['port'], context['protocol'])
                for filesystem_source, remote_source in zip(
                        filesystem_sources, remote_size_sources):
                    if os.path.isfile(filesystem_source):
                        image_size = os.path.getsize(filesystem_source)
                    else:
                        image_size = device.api.get_file_size_from_server(
                            server=endpoint,
                            path=remote_source,
                            protocol=context['protocol'],
                            timeout=timeout,
                            fu_session=context['file_utils'])
                    try:
                        image_size = int(image_size)
                    except (TypeError, ValueError):
                        raise RuntimeError(
                            "the recovery server returned an invalid size "
                            "for '{}'".format(filesystem_source))
                    if image_size <= 0:
                        raise RuntimeError(
                            "the recovery server returned a non-positive "
                            "size for '{}'".format(filesystem_source))
                    remote_sizes.append(image_size)
            except Exception as error:
                self._fail_transfer(recovery_server, hostname, source, target,
                                    device, error)
        if source and verify_md5:
            server_device = None
            try:
                for remote_source in filesystem_sources:
                    if os.path.isfile(remote_source):
                        with open(remote_source, 'rb') as image_file:
                            digest = hashlib.md5()
                            for chunk in iter(
                                    lambda: image_file.read(1024 * 1024), b''):
                                digest.update(chunk)
                            remote_md5s.append(digest.hexdigest())
                        continue
                    if server_device is None:
                        server_device = device.api.convert_server_to_linux_device(
                            recovery_server)
                        if not server_device:
                            raise RuntimeError(
                                "recovery image source is not locally readable "
                                "and the recovery server is not SSH-accessible")
                        server_device.connect()
                    remote_md5s.append(
                        server_device.api.get_md5_hash_of_file(
                            remote_source, timeout=timeout))
            except Exception as error:
                self._fail_transfer(recovery_server, hostname, source, target,
                                    device, error)
            finally:
                if server_device is not None:
                    try:
                        server_device.disconnect()
                    except Exception as error:
                        log.warning(
                            "Unable to disconnect recovery server '%s': %s",
                            recovery_server, error)
            if (not remote_md5s or
                    any(not image_md5 for image_md5 in remote_md5s)):
                self._fail_transfer(
                    recovery_server, hostname, source, target, device,
                    "the recovery server returned no MD5 for '{}'".format(source))

        context['remote_sizes'] = remote_sizes
        context['remote_md5s'] = remote_md5s
        context['verify_size'] = verify_size
        context['verify_md5'] = verify_md5
        context['copy_targets'] = []

        with device.temp_default_alias(connection_alias):
            for index, (target_destinations, target_filename) in enumerate(
                    context['target_sets']):
                for directory in target_destinations:
                    local_target = self._join_device_path(
                        directory, target_filename)
                    with steps.start(
                            "Check recovery image '{}' on device {}".format(
                                local_target, device.name)) as step:
                        try:
                            dir_output = device.execute('dir {}'.format(directory))
                            inspection_target = self._inspection_path(
                                local_target)
                            name_exists = device.api.verify_file_exists(
                                file=inspection_target,
                                size=None,
                                dir_output=dir_output)
                            exists = name_exists
                            if name_exists and verify_size:
                                exists = device.api.verify_file_exists(
                                    file=inspection_target,
                                    size=remote_sizes[index],
                                    dir_output=dir_output)
                            if exists and source and verify_md5:
                                local_md5 = device.api.get_md5_hash_of_file(
                                    local_target,
                                    timeout=timeout)
                                exists = bool(
                                    local_md5 and
                                    local_md5.lower() ==
                                    remote_md5s[index].lower())
                        except Exception as error:
                            self.failed(
                                "Unable to inspect recovery image destination "
                                "'{}' on device '{}': {}".format(
                                    local_target, device.name, error))
                        if exists:
                            if verify_size and verify_md5:
                                message = (
                                    "Recovery image already exists with the "
                                    "expected size and MD5")
                            elif verify_size:
                                message = (
                                    "Recovery image already exists with the "
                                    "expected size")
                            elif verify_md5:
                                message = (
                                    "Recovery image already exists with the "
                                    "expected MD5")
                            else:
                                message = (
                                    "Recovery image already exists at the "
                                    "expected target path")
                            step.passed(message)
                        else:
                            if not source:
                                self.failed(
                                    "No remote recovery image was resolved and "
                                    "local golden image '{}' is missing on device '{}'."
                                    .format(local_target, device.name))
                            context['copy_targets'].append({
                                'source': context['copy_sources'][index],
                                'target': local_target,
                                # A mismatched verified target is the only
                                # case where the transport must overwrite.
                                'overwrite': bool(
                                    name_exists and
                                    (verify_size or verify_md5)),
                            })
                            step.passed("Recovery image copy is required")

    def copy_recovery_image(self,
                            steps,
                            device,
                            connection_alias=CONNECTION_ALIAS,
                            vrf=VRF,
                            timeout=TIMEOUT,
                            copy_attempts=COPY_ATTEMPTS,
                            copy_attempts_sleep=COPY_ATTEMPTS_SLEEP,
                            prompt_recovery=False):
        """Copy the recovery image to each target selected for transfer."""
        context = self._recovery_context
        if not context['copy_targets']:
            with steps.start("Copy recovery image to device {}".format(
                    device.name)) as step:
                step.skipped("All recovery image targets are already present")
            return

        with device.temp_default_alias(connection_alias):
            for copy_target in context['copy_targets']:
                local_target = copy_target['target']
                source = copy_target['source']
                for attempt in range(1, copy_attempts + 1):
                    endpoint = self._url_hostname(
                        context['hostname'], context['port'],
                        context['protocol'])
                    with steps.start(
                            "Copy recovery image '{}' to '{}' on device {} "
                            "via {}://{} (attempt {}/{})".format(
                                source, local_target, device.name,
                                context['protocol'], endpoint, attempt,
                                copy_attempts)) as step:
                        try:
                            # The SDK returns command output on success and a
                            # false value when the device copy failed.
                            copy_kwargs = {
                                'protocol': context['protocol'],
                                # Preserve the testbed server name so the SDK
                                # can resolve its server block and let the
                                # device-specific FileUtils plugin select the
                                # reachable address, certificate, and proxy.
                                'server': context['recovery_server'],
                                'remote_path': source,
                                'local_path': local_target,
                                'vrf': vrf,
                                'timeout': timeout,
                                'prompt_recovery': prompt_recovery,
                            }
                            # Only replace an existing target after a size or
                            # MD5 mismatch. Missing targets use FileUtils'
                            # normal copy behavior and do not need an
                            # overwrite flag.
                            if copy_target['overwrite']:
                                copy_kwargs['overwrite'] = True
                            # The SDK omits the default port from URLs; pass an
                            # override only when one was supplied.
                            if (context.get('port') !=
                                    self._default_port(context['protocol'])):
                                copy_kwargs['port'] = context['port']
                            result = device.api.copy_to_device(**copy_kwargs)
                            if not result:
                                raise RuntimeError('copy API returned failure')
                        except Exception as error:
                            if attempt < copy_attempts:
                                log.warning(
                                    "Recovery image copy attempt %s failed: "
                                    "%s; retrying", attempt, error)
                                time.sleep(copy_attempts_sleep)
                                continue
                            self._fail_transfer(
                                context['recovery_server'],
                                context['hostname'], source,
                                local_target, device, error)
                        else:
                            step.passed(
                                "Recovery image copied to '{}' successfully"
                                .format(local_target))
                            break

    def verify_golden_image(self,
                            steps,
                            device,
                            connection_alias=CONNECTION_ALIAS,
                            timeout=TIMEOUT):
        """Verify every local golden-image target after copying."""
        context = self._recovery_context
        with device.temp_default_alias(connection_alias):
            for index, (target_destinations, target_filename) in enumerate(
                    context['target_sets']):
                for directory in target_destinations:
                    local_target = self._join_device_path(
                        directory, target_filename)
                    with steps.start(
                            "Verify recovery image '{}' on device {}".format(
                                local_target, device.name)) as step:
                        try:
                            # FileUtils owns remote transfer.  The stage only
                            # verifies the exact local destination here.
                            dir_output = device.execute('dir {}'.format(directory))
                            inspection_target = self._inspection_path(
                                local_target)
                            name_verified = device.api.verify_file_exists(
                                file=inspection_target,
                                size=None,
                                dir_output=dir_output)
                        except Exception as error:
                            self.failed(
                                "Recovery image was copied to '{}' on device "
                                "'{}', but verification failed: {}".format(
                                    local_target, device.name, error))
                        if not name_verified:
                            if context['filesystem_sources']:
                                message = (
                                    "Recovery image copy completed, but '{}' was "
                                    "not found on device '{}'.")
                            else:
                                message = (
                                    "Golden image target '{}' was not found on "
                                    "device '{}'.")
                            self.failed(message.format(local_target, device.name))
                        if context.get('verify_size', False):
                            try:
                                size_verified = device.api.verify_file_exists(
                                    file=inspection_target,
                                    size=context['remote_sizes'][index],
                                    dir_output=dir_output)
                            except Exception as error:
                                self.failed(
                                    "Unable to verify recovery image size for "
                                    "'{}' on device '{}': {}".format(
                                        local_target, device.name, error))
                            if not size_verified:
                                self.failed(
                                    "Recovery image size verification failed "
                                    "for '{}' on device '{}'. Expected {} "
                                    "bytes.".format(
                                        local_target, device.name,
                                        context['remote_sizes'][index]))
                        if context.get('verify_md5', False):
                            local_md5 = device.api.get_md5_hash_of_file(
                                local_target, timeout=timeout)
                            expected_md5 = context['remote_md5s'][index]
                            if not local_md5 or local_md5.lower() != expected_md5.lower():
                                self.failed(
                                    "Recovery image MD5 verification failed for "
                                    "'{}' on device '{}'.".format(
                                        local_target, device.name))
                        step.passed("Recovery image verified successfully")

    def update_device_recovery(self,
                               steps,
                               device,
                               update_device_recovery=UPDATE_DEVICE_RECOVERY):
        """Expose the local target to subsequent recovery stages."""
        if update_device_recovery:
            device.clean.setdefault('device_recovery', {})[
                'golden_image'] = self._recovery_context['golden_images']


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
    exec_order = ['write_erase']

    def write_erase(self, steps, device, timeout=TIMEOUT):

        with steps.start("Execute write erase on the device") as step:

            try:
                device.api.execute_write_erase(timeout=timeout)
            except Exception as e:
                step.failed("Failed to execute 'write erase'",
                            from_exception=e)


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

        error_pattern (list, optional): List of regex patterns to check for errors.
            Defaults to an empty list (no error checking).

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
    check_modules:
        check: False
"""
    # =================
    # Argument Defaults
    # =================
    RELOAD_SERVICE_ARGS = {
        'timeout': 800,
        'reload_creds': 'default',
        'prompt_recovery': True,
        'error_pattern': []
    }
    CHECK_MODULES = {
        'check': True,
        'timeout': 180,
        'interval': 30,
        'ignore_modules': None
    }
    RECONNECT_VIA = None

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('check_modules'): {
            Optional('check'): bool,
            Optional('timeout'): int,
            Optional('interval'): int,
            Optional('ignore_modules'): list
        },
        Optional('reload_service_args'): {
            Optional('timeout'): int,
            Optional('reload_creds'): str,
            Optional('prompt_recovery'): bool,
            Optional('error_pattern'): list,
            Any(): Any()
        },
        Optional('reconnect_via'): str,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = ['reload', 'disconnect_and_reconnect', 'check_modules']

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
        # Disable device recovey for unicon service
        reload_service_args.update({'device_recovery': False})
        with steps.start(f"Reload {device.name}") as step:

            try:
                device.reload(**reload_service_args)
            except Exception as e:
                step.failed(
                    f"Failed to reload within {reload_service_args['timeout']} "
                    f"seconds.",
                    from_exception=e)

    def disconnect_and_reconnect(self,
                                 steps,
                                 device,
                                 reload_service_args=None,
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
                log.warning(
                    "Failed to destroy the device connection but "
                    "attempting to continue",
                    exc_info=True)
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

            with steps.start(
                    f"Checking the modules on '{device.name}' are in a "
                    f"stable state") as step:

                try:
                    device.api.verify_module_status(
                        timeout=check_modules['timeout'],
                        interval=check_modules['interval'],
                        ignore_modules=check_modules['ignore_modules'])
                except Exception as e:
                    step.failed("Modules are not in a stable state",
                                from_exception=e)


class ExecuteCommand(BaseStage):
    """Executing commands on the device.

Stage Schema
------------
execute_command:

    commands (list): List of commands to execute.

    execute_timeout (int, optional): Max time in seconds allowed for executing the
        command. Defaults to 60.

    sleep_time(int,optional): Time in seconds to sleep after running each command.

Example
-------
execute_command:
    commands:
        - show version
        - show boot
    execute_timeout: 60
    sleep_time: 10

"""

    # =================
    # Argument Defaults
    # =================
    EXECUTE_TIMEOUT = 60
    SLEEP_TIME = 10
    # ============
    # Stage Schema
    # ============
    schema = {
        'commands': list,
        Optional('execute_timeout'): int,
        Optional('sleep_time'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = ['execute_command']

    def execute_command(self,
                        steps,
                        device,
                        commands,
                        execute_timeout=EXECUTE_TIMEOUT,
                        sleep_time=SLEEP_TIME):

        # User has provided a list of commands to apply onto device
        with steps.start("Executing commands on the device {} ".\
                         format(device.name)) as step:
            for cmd in commands:
                try:
                    device.execute(cmd, timeout=execute_timeout)
                except Exception as e:
                    step.failed("Error while executing command on the device "
                                "{}\n{}".format(device.name, str(e)))
                else:
                    log.info(f"Sleeping for {sleep_time} seconds.")
                    time.sleep(sleep_time)
            step.passed(
                "Successfully executed commands on the device {} ".format(
                    device.name))


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

    max_time (int, optional): Maximum time in seconds allowed for copying the
        running configuration to startup and any verifications. Defaults to
        300.

    check_interval (int, optional): How often in seconds to check. Defaults to 60.

    skip_copy_run_start (bool, optional): If 'True' do not copy the running config
        to the startup config. Defaults to False.

    copy_directly_to_startup (bool, optional): If 'True' copy the provided
        configuration directly to the startup config. Defaults to False.

    error_pattern (list, optional): if error_pattern list is given,
        it will be passed to device.configure() to use the error_pattern

    skip_if_no_config (bool, optional): If 'True' and no configuration is provided,
        the stage will skip execution. Defaults to True.

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
    skip_if_no_config: True

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
    ERROR_PATTERN = None
    SKIP_IF_NO_CONFIG = True

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
        Optional('error_pattern'): list,
        Optional('skip_if_no_config'): bool,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = ['apply_configuration']

    def apply_configuration(self,
                            steps,
                            device,
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
                            copy_directly_to_startup=COPY_DIRECTLY_TO_STARTUP,
                            error_pattern=ERROR_PATTERN,
                            skip_if_no_config=SKIP_IF_NO_CONFIG):
        
        if skip_if_no_config and not any(
                [configuration, configuration_from_file, file]):
            log.info(
                "No configuration provided and skip_if_no_config is True. "
                "Skipping apply_configuration on device {}".format(device.name))
            self.skipped()

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
                    copy_directly_to_startup=copy_directly_to_startup,
                    error_pattern=error_pattern)
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
                    device.api.execute_copy_run_to_start(
                        command_timeout=max_time,
                        copy_vdc_all=copy_vdc_all)
                except Exception as e:
                    step.failed(
                        "Failed to copy running-config to startup-config on "
                        "{}\n{}".format(device.name, str(e)))
                else:
                    step.passed(
                        "Successfully copied running-config to startup-config "
                        "on {}".format(device.name))

        # Allow configuration to stabilize
        with steps.start("Allow configuration to stabilize on device {}".\
                         format(device.name)) as step:
            log.info("Sleeping for '{}' seconds".format(config_stable_time))
            time.sleep(config_stable_time)
            step.passed(
                "Successfully applied configuration on device {}".format(
                    device.name))

        with steps.start('Show running-config'):
            device.execute('show running-config', timeout=max_time, error_pattern=[])

        with steps.start('Show startup-config'):
            device.execute('show startup-config', timeout=max_time, error_pattern=[])


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

    ignore_flash (bool, optional): Ignore flash directory names. Default False.

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
    IGNORE_FLASH = False
    REGEX_SEARCH = False

    # ============
    # Stage Schema
    # ============
    schema = {
        'images': list,
        Optional('ignore_flash'): bool,
        Optional('verify_md5'): {
            'hostname': str,
            Optional('timeout'): int
        }
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = ['verify_running_image']

    def verify_running_image(self,
                             steps,
                             device,
                             images,
                             verify_md5=VERIFY_MD5,
                             ignore_flash=IGNORE_FLASH,
                             regex_search=REGEX_SEARCH):
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
                    step.failed("Failed to connect to {}.\nError: {}".format(
                        hostname, e))

                server_hashes = {}

                # Generate the hash for each image
                for image in images:
                    with step.start("Generating the MD5 hash for '{}'"
                                    "".format(image)) as substep:

                        hash_ = server.api.get_md5_hash_of_file(
                            image, timeout=timeout)

                        if hash_:
                            server_hashes[image] = hash_
                            substep.passed(
                                "The MD5 has for '{}' is '{}'".format(
                                    image, hash_))
                        else:
                            substep.failed(
                                "Failed to get MD5 hash for {}".format(image))

            with steps.start("Get the running image(s) on {}"
                             "".format(device.name)) as step:

                running_images = device.api.get_running_image()
                if not running_images:
                    step.failed("Failed to get running image(s)")

                if not isinstance(running_images, list):
                    running_images = [running_images]

                step.passed(
                    "The running image(s) are: {}".format(running_images))

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
                            substep.passed(
                                "The MD5 hash for '{}' is '{}'".format(
                                    image, hash_))
                        else:
                            substep.failed(
                                "Failed to get MD5 hash for {}".format(image))

            with steps.start(
                    "Compare the hashes from the origin to the running "
                    "images") as step:

                # Values must be compared since the path or name
                # of the image can be different
                if set(server_hashes.values()) == set(
                        running_image_hashes.values()):
                    step.passed(
                        "The hashes from the running image(s) match the "
                        "hashes from the origin server.\n"
                        "Server hash(es): {}\n"
                        "Running image hash(es): {}".format(
                            server_hashes, running_image_hashes))
                else:
                    step.failed(
                        "The hashes from the running image(s) do not match "
                        "the hashes from the origin server\n"
                        "Server hash(es): {}\n"
                        "Running image hash(es): {}".format(
                            server_hashes, running_image_hashes))
        else:

            # Verify via filename comparison
            with steps.start("Verify running image on device {}". \
                                     format(device.name)) as step:
                try:
                    device.api.verify_current_image(images=images,
                                                    ignore_flash=ignore_flash,
                                                    regex_search=regex_search)
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
    exec_order = ['verify_enough_available_disk_space', 'create_backup']

    def verify_enough_available_disk_space(self, steps, device, copy_dir,
                                           copy_file):

        with steps.start(
                "Verify there is enough disk space to create a backup "
                "of '{copy_dir}/{copy_file}'") as step:

            file_size = device.api.get_file_size(
                file=f'{copy_dir}/{copy_file}')
            if file_size is None:
                step.failed(
                    f"Could not get the size of '{copy_dir}/{copy_file}'")

            avail_space = device.api.get_available_space(directory=copy_dir)
            if not avail_space:
                step.failed(
                    f"Could not get the remaining disk space of '{copy_dir}'")

            if avail_space <= file_size:
                step.failed(f"Cannot create backup - not enough disk space.\n"
                            f"Available space: '{avail_space}'\n"
                            f"Required space: '{file_size}'")

            step.passed(f"There is enough disk space available to backup "
                        f"'{copy_dir}/{copy_file}'")

    def create_backup(self,
                      steps,
                      device,
                      copy_dir,
                      copy_file,
                      overwrite=OVERWRITE,
                      timeout=TIMEOUT):

        with steps.start(
                f"Create a backup of '{copy_dir}/{copy_file}'") as step:

            overwrite_dialog = Dialog([
                Statement(
                    pattern=r'.*over\s*write.*',
                    action='sendline({})'.format('y' if overwrite else 'n'),
                    loop_continue=True,
                    continue_timer=False)
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
    exec_order = ['restore_backup', 'delete_file', 'delete_file_on_stby']

    delete_dialog = Dialog([
        Statement(pattern=r'.*Do you want to delete.*',
                  action='sendline(y)',
                  loop_continue=True,
                  continue_timer=False)
    ])

    def restore_backup(self,
                       steps,
                       device,
                       delete_dir,
                       delete_file,
                       restore_from_backup=RESTORE_FROM_BACKUP,
                       overwrite=OVERWRITE,
                       timeout=TIMEOUT):

        if restore_from_backup:
            original_file = delete_file.strip("backup_")

            with steps.start(
                    f"Restoring '{delete_dir}/{original_file}' from the "
                    f"backup") as step:

                overwrite_dialog = Dialog([
                    Statement(pattern=r'.*over\s*write.*',
                              action='sendline({})'.format(
                                  'y' if overwrite else 'n'),
                              loop_continue=True,
                              continue_timer=False)
                ])

                try:
                    device.copy(source=delete_dir,
                                source_file=delete_file,
                                dest=delete_dir,
                                dest_file=original_file,
                                reply=overwrite_dialog,
                                timeout=timeout)
                except Exception as e:
                    step.failed("Failed to restore the original file.",
                                from_exception=e)

    def delete_file(self, steps, device, delete_dir, delete_file):

        with steps.start(f"Delete '{delete_dir}/{delete_file}' from the device"
                         ) as step:

            try:
                device.execute(f"delete {delete_dir}{delete_file}",
                               reply=self.delete_dialog,
                               append_error_pattern=['.*%Error.*'])
            except Exception as e:
                step.failed("Failed to delete the file.", from_exception=e)

    def delete_file_on_stby(self,
                            steps,
                            device,
                            delete_dir,
                            delete_file,
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
    exec_order = ['delete_files']

    def delete_files(self,
                     steps,
                     device,
                     server=SERVER,
                     files=FILES,
                     protocol=PROTOCOL):

        # pyats FU only support sftp or ftp delete
        with steps.start('Delete files from the server') as step:

            if not files:
                # Get list of files from copy_to_linux stage
                if 'CopyToLinux' in self.history:
                    log.warning(
                        "No files to delete have been specified. Will "
                        "delete the files copied from the 'copy_to_linux' "
                        "stage.")

                    files = getattr(self.history['CopyToLinux'], 'parameters', {}).\
                        get('files_copied', {})

                    # covert the stored file paths to a list of files
                    files = [files[file]['dest_path'] for file in files]

                else:
                    step.skipped("No files to delete")

            is_local_deletion = False
            # If 'server' was not explicitly passed to DeleteFilesFromServer/CopyToLinux

            if not server:
                # Get server from copy_to_linux stage
                log.warning("No server has been specified. Will use the same "
                            "server from the 'copy_to_linux' stage.")

                if 'CopyToLinux' in self.history:
                    server_from_copy = getattr(self.history['CopyToLinux'], 'parameters', {}).\
                        get('destination', {}).get('hostname')
                    if server_from_copy:
                        # If server not provided in stage
                        server = server_from_copy
                    else:
                        is_local_deletion = True
                else:
                    step.skipped(
                        "No server has been specified. Cannot delete files.")

            fu_session = None
            if not is_local_deletion:

                if not server:
                    step.skipped(
                        "Cannot perform remote deletion as no valid server was identified."
                    )
                    return

                # establish a FileUtils session for all FileUtils operations
                fu_session = FileUtils(testbed=device.testbed)

            for file_path in files:
                with step.start(f"Deleting {file_path}") as substep:
                    try:
                        if is_local_deletion:
                            if os.path.exists(file_path):
                                os.remove(file_path)
                                log.info(
                                    f"Successfully deleted local file: {file_path}"
                                )
                            else:
                                log.warning(
                                    f"Local file not found, skipping deletion: {file_path}"
                                )
                        else:
                            device.api.delete_file_on_server(
                                testbed=device.testbed,
                                path=file_path,
                                server=server,
                                protocol=protocol,
                                fu_session=fu_session)
                    except Exception as e:
                        substep.passx(f"Failed to delete '{file_path}'",
                                      from_exception=e)


class DeleteFiles(BaseStage):
    """Delete files from the device.

Uses the `delete_files` device API.

Stage Schema
------------
delete_files:

    files (list): List of files including location.

    regex (bool, optional): If regex is used in the file names, set to True. Default False.

    timeout (int, optional): Timeout in seconds for deleting files. Defaults to 3600.

Example
-------
delete_files:
    files:
        - flash:core/*.gz
        - crashinfo/*.tar.gz
"""

    # =================
    # Argument Defaults
    # =================
    REGEX = False
    TIMEOUT = 3600

    # ============
    # Stage Schema
    # ============
    schema = {
        'files': list,
        Optional('regex'): bool,
        Optional('timeout'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'delete_files',
    ]

    def delete_files(self, steps, device, files, regex=REGEX, timeout=TIMEOUT):

        for fn in files:
            with steps.start(f"Delete '{fn}' from the device") as step:

                # if the filename as a location specified as bootflash:filename, use location1 as "bootflash:"
                location1 = fn.split(':')[0] + ':' if ':' in fn else ''
                # if the filename has a slash specified, e.g. flash:/directory/filename, use location2 as "flash:/directory"
                location2 = '/'.join(fn.split('/')[:-1]) if len(
                    fn.split('/')) > 1 else ''
                location = location2 or location1

                # Get the filename portion of the expression
                # if only ':' in the filename, use filenames1
                filenames1 = fn.split(':')[-1] if ':' in fn else fn
                # if '/' in filename, get the part after the /
                filenames = fn.split('/')[-1] if len(
                    fn.split('/')) > 1 else filenames1

                # If user did not specify regex to be used, assume unix filename matching
                # Translate the expresion to a regex one to pass to the API
                if not regex:
                    filenames = fnmatch.translate(filenames)

                log.debug(
                    f'Delete files - Location: {location} filenames: {filenames}'
                )

                try:
                    device.api.delete_files(locations=[location],
                                            filenames=[filenames],
                                            timeout=timeout)
                except SchemaEmptyParserError:
                    step.passx(
                        f"Directory '{location}' does not exist or is "
                        f"empty on the device. Nothing to delete.")
                except Exception as e:
                    step.failed("Failed to delete the file.", from_exception=e)


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
    exec_order = ['revert_vm_snapshot']

    def revert_vm_snapshot(
            self,
            steps,
            device,
            esxi_server,
            recovery_snapshot_name,
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
                step.passed(
                    "Verified that {esxi_server} is specified in testbed "
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
                    step.failed(
                        "Failed to connect to ESXi server {server} with "
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
                    step.failed(
                        "Failed to power {state} of VM {vm} with error: "
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
                                       'recovery: {err}'.format(
                                           dev=device.name, err=str(err)))

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

    sleep_before_connect (int, optional): Time to sleep before connecting
        to the device. Defaults to 60 seconds.

    sleep_after_connect (int, optional): Time to sleep after connecting
        to the device. Defaults to 0 (no sleep).

    connect_arguments (dict, optional): Arguments to connect() method.

    connect_retry_wait (int, optional). Time to wait before retrying to
        connect to the device. Defaults to 60 seconds.

    connection_timeout(int, optional): Time to wait during connect to the 
        device, Default to 120 seconds

    rommon_boot (bool, optional): Boot the device from ROMMON after power
        cycling. Defaults to False.

    golden_image (list or dict, optional): Golden image to use for ROMMON
        boot. If not provided, device recovery information is used.

Example
-------
power_cycle:
    sleep_after_power_off: 5
    sleep_after_connect: 10
    rommon_boot: True
    golden_image:
      - bootflash:golden_image.bin
"""

    # =================
    # Argument Defaults
    # =================
    SLEEP_AFTER_POWER_OFF = 30
    BOOT_TIMEOUT = 600
    SLEEP_BEFORE_CONNECT = 60
    SLEEP_AFTER_CONNECT = 0
    CONNECT_ARGUMENTS = {}
    CONNECT_RETRY_WAIT = 60
    CONNECTION_TIMEOUT = 120
    ROMMON_BOOT = False

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('sleep_after_power_off'): int,
        Optional('boot_timeout'): int,
        Optional('sleep_before_connect'): int,
        Optional('sleep_after_connect'): int,
        Optional('connect_arguments'): dict,
        Optional('connect_retry_wait'): int,
        Optional('connection_timeout'): int,
        Optional('rommon_boot'): bool,
        Optional('golden_image'): Or(list, {
            'system': str,
            Optional('kickstart'): str,
        }),
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = ['powercycle', 'rommon_boot', 'reconnect']

    def powercycle(self,
                   steps,
                   device,
                   sleep_after_power_off=SLEEP_AFTER_POWER_OFF):

        with steps.start(f"Powercycling '{device.name}'") as step:
            try:
                device.api.execute_power_cycle_device(
                    delay=sleep_after_power_off)
            except Exception as e:
                step.failed("Failed to powercycle", from_exception=e)

    def rommon_boot(self,
                    steps,
                    device,
                    rommon_boot=ROMMON_BOOT,
                    golden_image=None):

        if not rommon_boot:
            return

        with steps.start(f"Booting '{device.name}' from ROMMON") as step:
            try:
                if golden_image:
                    device.api.device_recovery_boot(golden_image=golden_image)
                else:
                    device.api.device_recovery_boot()
            except Exception as e:
                step.failed("Failed to boot from ROMMON", from_exception=e)

    def reconnect(self,
                  steps,
                  device,
                  boot_timeout=BOOT_TIMEOUT,
                  sleep_before_connect=SLEEP_BEFORE_CONNECT,
                  sleep_after_connect=SLEEP_AFTER_CONNECT,
                  connect_arguments=CONNECT_ARGUMENTS,
                  connect_retry_wait=CONNECT_RETRY_WAIT,
                  connection_timeout=CONNECTION_TIMEOUT):

        if sleep_before_connect:
            with steps.start(
                    f"Sleeping for {sleep_before_connect} seconds before connect"
            ) as step:
                time.sleep(sleep_before_connect)
                step.passed(f'Waited {sleep_before_connect} seconds')

        with steps.start(f"Reconnecting to '{device.name}'") as step:

            timeout = Timeout(boot_timeout, connect_retry_wait)
            while timeout.iterate():
                device.destroy()

                try:
                    device.connect(learn_hostname=True,
                                   **connect_arguments,
                                   connection_timeout=connection_timeout)

                except Exception as e:
                    connect_exception = e
                    log.info(f"Could not reconnect {e}")
                else:
                    step.passed("Reconnected")

                timeout.sleep()

            step.failed("Could not reconnect",
                        from_exception=connect_exception)

        if sleep_after_connect:
            with steps.start(
                    f"Sleeping for {sleep_after_connect} seconds after connect"
            ) as step:
                time.sleep(sleep_after_connect)
                step.passed(f'Waited {sleep_after_connect} seconds')


class CopyRunToFlash(BaseStage):
    """This stage will copy running-configuration to device flash.

Stage Schema
------------
copy_run_to_flash:

    file_name (str): Name of the file to be saved to flash.
    timeout (int, optional): Copy operation timeout in seconds. Defaults to 300.
    overwrite (bool, optional): Overwrite the file if a file with the same name already exists. Defaults to True.

Example
-------
copy_run_to_flash:
    file_name: base.cfg
    timeout: 300
    overwrite: True
"""
    # =================
    # Argument Defaults
    # =================
    TIMEOUT = 300
    OVERWRITE = True

    # ============
    # Stage Schema
    # ============
    schema = {
        'file_name': str,
        Optional('timeout'): int,
        Optional('overwrite'): bool
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = ['copy_run_to_flash']

    def copy_run_to_flash(self,
                          steps,
                          device,
                          file_name,
                          timeout=TIMEOUT,
                          overwrite=OVERWRITE):

        with steps.start("Copying running config to flash") as step:

            try:
                device.copy(source='running-config',
                            dest=file_name,
                            timeout=timeout,
                            overwrite=overwrite)
            except Exception as e:
                step.failed("Failed to copy running-config to flash:",
                            from_exception=e)


class ConfigureManagement(BaseStage):
    """This stage configures the management IP settings on the device.

Stage Schema
------------
configure_management:

        address ('dict', optional):  Address(es) to configure on the device (syntax: address/mask) (optional)
            ipv4 ('str') or ('list'): ipv4 address
            ipv6 ('str') or ('list'): ipv6 address

        gateway: (dict, optional) Gateway address(es) for default route
            ipv4 ('str') or ('list'): ipv4 gateway address
            ipv6 ('str') or ('list'): ipv6 gateway address

        vrf (str, optional): VRF to use for management interface

        interface (str, optional): Management interface to use

        routes ('dict', optional):
           ipv4 (list of 'dict'): ipv4 routes
              - subnet: (str) subnet including mask
                next_hop: (str) next_hop for this subnet
           ipv6 (list of 'dict'): ipv6 routes
              - subnet: (str) subnet including mask
                next_hop: (str) next_hop for this subnet

        dhcp_timeout ('int', optional): DHCP timeout in seconds (default: 30)

        protocols ('list', optional): [list of protocols]

        set_hostname (bool): Configure device hostname (default: True)
        alias_as_hostname (bool): When used with `set_hostname`, will use the
            alias as the hostname. (default: False)

        config_stable_time (int, optional): Max time in seconds allowed for the
            configuration to stabilize. Defaults to 10.


Example
-------
configure_management:
    vrf: Mgmt-vrf

"""
    # =================
    # Argument Defaults
    # =================
    SET_HOSTNAME = True
    CONFIG_STABLE_TIME = 10
    PING_ATTEMPTS = 3
    PING_SLEEP = 10

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('address'): {
            Optional('ipv4'): Or(str, list),
            Optional('ipv6'): Or(str, list)
        },
        Optional('gateway'): {
            Optional('ipv4'): Or(str, list),
            Optional('ipv6'): Or(str, list)
        },
        Optional('vrf'): str,
        Optional('interface'): str,
        Optional('routes'): {
            Optional('ipv4'): ListOf({
                'subnet': str,
                'next_hop': str
            }),
            Optional('ipv6'): ListOf({
                'subnet': str,
                'next_hop': str
            })
        },
        Optional('dhcp_timeout'): int,
        Optional('protocols'): ListOf(str),
        Optional('set_hostname'): bool,
        Optional('alias_as_hostname'): bool,
        Optional('config_stable_time'): int,
        Optional('ping_attempts'): int,
        Optional('ping_sleep'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'configure_management',
        'check_management_interface_status',
        'ping_gateway',
    ]

    def configure_management(self,
                             steps,
                             device,
                             set_hostname=SET_HOSTNAME,
                             config_stable_time=CONFIG_STABLE_TIME,
                             **kwargs):
        if "configure_management" not in dir(device.api):
            self.passx("No support for configure_management API")

        with steps.start("Configuring device management") as step:
            exclude_keys = {'ping_attempts', 'ping_sleep'}
            config_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k in [k.schema for k in self.schema.keys()] and k not in exclude_keys
            }

            config_kwargs["set_hostname"] = set_hostname

            if hasattr(device, "management") and device.management:
                device.api.configure_management(**config_kwargs)
                log.info(
                    f"Waiting {config_stable_time} seconds for the configuration to be applied"
                )
                time.sleep(config_stable_time)
            else:
                step.passx("No management info for device")

    def check_management_interface_status(self, steps, device, **kwargs):
        """Check if the management interface is up and running."""
        management = getattr(device, "management", {})
        config_kwargs = {
            k: v
            for k, v in kwargs.items()
            if k in [k.schema for k in self.schema.keys()]
        }
        interface = config_kwargs.get("interface") or management.get(
            "interface")

        with steps.start("Check management interface status") as step:
            try:
                output = device.parse(f"show interface {interface}")
            except Exception as e:
                step.failed(
                    f"Failed to verify the interface {interface} status",
                    from_exception=e,
                )

            if not output:
                step.failed(f"No output returned when checking interface {interface} status")

            if interface not in output:
                step.failed(
                    f"Interface {interface} not found in output when checking management interface status"
                )

            if output[interface].get("oper_status") == "up":
                step.passed("Management interface is up")
            else:
                step.failed("Management interface is down")

    def ping_gateway(self,
                     steps,
                     device,
                     ping_attempts=PING_ATTEMPTS,
                     ping_sleep=PING_SLEEP,
                     **kwargs):
        """Ping the gateway to ensure connectivity."""
        with steps.start("Verify Gateway Configuration") as step:
            management = getattr(device, "management", {})
            config_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k in [k.schema for k in self.schema.keys()]
            }
            ip4_gateway = config_kwargs.get("gateway",
                                            {}).get("ipv4") or management.get(
                                                "gateway", {}).get("ipv4")
            ip6_gateway = config_kwargs.get("gateway",
                                            {}).get("ipv6") or management.get(
                                                "gateway", {}).get("ipv6")
            interface = config_kwargs.get("interface") or management.get(
                "interface")

            vrf = config_kwargs.get("vrf") or management.get("vrf")

            if not ip4_gateway and not ip6_gateway:
                step.failed("No gateway configured for management interface")
                return

        for gateway in [ip4_gateway, ip6_gateway]:
            if gateway:
                with steps.start(f"Ping gateway {gateway}") as step:
                    ping_successful = False
                    last_exception = None
                    for attempt in range(1, ping_attempts + 1):
                        try:
                            device.ping(addr=gateway,
                                        vrf=vrf,
                                        source=interface,
                                        timeout=120,
                                        count=5)
                            step.passed("Ping to gateway successful")
                            ping_successful = True
                            break 
                        except Exception as e:
                            last_exception = e
                            if attempt < ping_attempts:
                                log.warning(
                                    f"Ping to gateway '{gateway}' failed (attempt #{attempt} of {ping_attempts}): {e}\n"
                                    f"Retrying in {ping_sleep} seconds."
                                )
                                time.sleep(ping_sleep)

                    if not ping_successful:
                        step.failed(f"Ping to gateway {gateway} failed after {ping_attempts} attempts", from_exception=last_exception)

class ConfigureInterfaces(BaseStage):
    """This stage configures interfaces on the device.

    This stages uses genie Conf objects and build_config() API to configure
    interfaces on devices.

Stage Schema
------------
configure_interfaces:
    interfaces:
        <interfaces>:  # regex, default: '.*'
            attributes ('list', optional):  List of interface attributes to configure.
                Default: [enabled, speed, breakout]

Example
-------
configure_interfaces:
    interfaces:
        <interface>:   # regex
            attributes:
                - enabled
                - speed
                - ipv4
"""

    # =================
    # Argument Defaults
    # =================
    ATTRIBUTES = [
        'enabled',
        'speed',
        'breakout',
    ]
    INTERFACE_NAME_REGEX = '.*'
    ATTRIBUTE_FILTER = {}
    INTERFACES = {
        INTERFACE_NAME_REGEX: {
            "attributes": ATTRIBUTES,
        }
    }

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('interfaces'): {
            str: {
                Optional("attributes"): list,
            }
        }
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = ['configure_interfaces']

    def configure_interfaces(self,
                             steps,
                             device,
                             interfaces=INTERFACES,
                             **kwargs):
        configuration_lines = []
        for iface_regex in interfaces:
            for _, iface_obj in device.interfaces.items():
                # Skip stackwise virtual link interfaces as they dont need to be configured here
                if hasattr(iface_obj, "stackwise_virtual_link") and iface_obj.stackwise_virtual_link:
                    log.debug(f"Skipping stackwise virtual link interface {iface_obj.name}")
                    continue
                
                if re.match(iface_regex, iface_obj.name) or \
                    (isinstance(getattr(iface_obj, "alias", None), str) and re.match(iface_regex, iface_obj.alias)):
                    log.info(
                        f'Preparing interface config for: {iface_obj.name}')
                    attributes = interfaces.get(iface_regex,
                                                {}).get('attributes', {})

                    # Create dictionary of attributes to configure
                    attrs = {attr: getattr(iface_obj, attr) for attr in attributes \
                                if getattr(iface_obj, attr, None) is not None}

                    # disable switchport if configuring ipv4/ipv6
                    if ("switchport" in attributes) and \
                            ("ipv4" in attrs or "ipv6" in attrs) and \
                            "switchport" not in attrs:
                        iface_obj.switchport = False
                        attrs["switchport"] = False

                    # enable interfaces if not breakout
                    if not getattr(iface_obj, "breakout", False) and \
                            getattr(iface_obj, 'enabled') is not False:
                        iface_obj.enabled = True
                        attrs.update({'enabled': True})

                    # Get configuration lines from config builder
                    try:
                        log.debug(
                            f'Building config for {iface_obj.name} with '
                            f'attributes: {attrs}')
                        config_lines = str(
                            iface_obj.build_config(attributes=attrs,
                                                   apply=False))
                        if config_lines.strip():
                            log.info(
                                f'Built config for {iface_obj.name}:\n'
                                f'{config_lines}')
                        else:
                            log.warning(
                                f'No configuration lines generated for '
                                f'{iface_obj.name}')
                        # Extend lines to configuration variable
                        configuration_lines.extend(config_lines.splitlines())
                    except Exception as e:
                        log.warning(
                            f'Failed to build config for {iface_obj.name}: {e}'
                        )

        if getattr(device, "custom_config_cli", None):
            config_lines = str(device.build_config(apply=False))
            configuration_lines = config_lines.splitlines(
            ) + configuration_lines

        # Configure all interfaces
        if configuration_lines:
            self._apply_configuration_lines(device, configuration_lines)

    def _apply_configuration_lines(self, device, configuration_lines):
        """Apply a list of configuration lines to the device.

        Override this method in an OS-specific subclass to change how
        configuration is applied (e.g. Linux uses execute instead of configure).
        """
        device.configure(configuration_lines)
