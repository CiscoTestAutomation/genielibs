# Python
import re
import time
import shutil
import os.path
import logging

# pyATS
from pyats import aetest
from pyats.utils.fileutils import FileUtils
try:
    from ats.datastructures.logic import Or
except ImportError:
    from pyats.datastructures.logic import Or

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure

# Genie
from genie.utils.timeout import Timeout
from genie.libs.clean.utils import clean_schema
from genie.libs.clean.utils import (_apply_configuration, find_clean_variable,
                                    verify_num_images_provided,
                                    handle_rommon_exception,
                                    remove_string_from_image)

# MetaParser
from genie.metaparser.util.schemaengine import Optional, Any

# Logger
log = logging.getLogger(__name__)

#===============================================================================
#                       stage: connect
#===============================================================================


@clean_schema({
    Optional('timeout'): Or(str, int),
    Optional('max_timeout'): Or(str, int, float),
    Optional('interval'): Or(str, int, float),
})
@aetest.test
def connect(section,
            device,
            timeout=200,
            retry_timeout=0,
            retry_interval=0,
            **kwargs):
    """ This stage connects to the device that is being cleaned.

    Stage Schema
    ------------
    connect:
        timeout (int, optional): Connection timeout. Defaults to 200.
        retry_timeout (int, optional): Overall timeout for retry mechanism. Defaults to 0 which means no retry.
        retry_interval (int, optional): Interval for retry mechanism. Defaults to 0 which means no retry.

    Example
    -------
    connect:
        timeout: 60

    """

    log.info('Checking connection to device: %s' % device.name)

    # Create a timeout that will loop
    retry_timeout = Timeout(float(retry_timeout), float(retry_interval))
    retry_timeout.one_more_time = True
    while retry_timeout.iterate():

        # If the device is in rommon, just raise an exception
        device.instantiate(connection_timeout=timeout,
                           learn_hostname=True,
                           prompt_recovery=True)

        rommon = Statement(
            pattern=r'^(.*)(rommon(.*)|loader(.*))+>.*$',
            #action=lambda section: section.failed('Device is in rommon'),
            action=handle_rommon_exception,
            loop_continue=False,
            continue_timer=False)

        device.connect_reply.append(rommon)

        try:
            device.connect()
        except Exception as err:
            log.error('Connection to the device failed, with error {e}'.\
                    format(e=str(err)))
            device.destroy_all()
            # Loop
        else:
            section.passed("Successfully connected to '{}'".format(
                device.name))
            # Don't loop
        finally:
            try:
                device.connect_reply.remove(rommon)
            except Exception:
                pass

        retry_timeout.sleep()

    section.failed("Could not connect to '{d}'".format(d=device.name))


#===============================================================================
#                       stage: ping_server
#===============================================================================


@clean_schema({
    'server': str,
    Optional('vrf'): str,
    Optional('timeout'): int,
    Optional('min_success_rate'): int,
    Optional('max_attempts'): int,
    Optional('interval'): int,
})
@aetest.test
def ping_server(section,
                steps,
                device,
                server,
                vrf=None,
                timeout=60,
                min_success_rate=60,
                max_attempts=5,
                interval=30):
    """ This stage pings a server from a device to ensure connectivity.

    Stage Schema
    ------------
    ping_server:
        server: <Hostname or address of the server to ping `str`> (Mandatory)
        vrf: <Vrf used in ping `str`> (Optional)
        timeout: <timeout for ping command. Default 60 seconds `int`> (Optional)
        min_success_rate: <minimum ping success rate to mark seciton as passed. Default 60 % `int`> (Optional)
        max_attempts: <maximum number of attempts to check minimum ping success rate. Default 5 `int`> (Optional)
        interval: <time between re-attempts to check minimum ping success rate. Default 30 seconds `int`> (Optional)

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

    with steps.start(
            "Checking connectivity between device and file server") as step:

        # Patterns for success rate
        p1 = r'Success +rate +is +(?P<success>(\d+)) +percent +\((?P<pass>(\d+))\/(?P<fail>(\d+))\)'
        p2 = r'(?P<transmit>(\d+)) +packets +transmitted, (?P<recv>(\d+)) +packets +received, (?P<loss>(\S+))% +packet +loss'

        # Verify given server is found in the testbed YAML file
        try:
            server_from_obj = device.api.convert_server_to_linux_device(server)
        except Exception:
            step.failed("Server '{}' was provided in the clean YAML file "
                           "but doesn't exist in the testbed YAML file".\
                           format(server))
        else:
            log.info("Server '{}' found in the testbed YAML file".\
                     format(server))

        # If hostname of server given, return IP address
        fu = FileUtils.from_device(device)
        server = fu.get_hostname(server, device, vrf=vrf)

        for i in range(1, max_attempts + 1):
            log.info("\nAttempt #{}: Ping server '{}'".format(i, server))

            # Ping server from device
            try:
                if vrf:
                    output = device.ping(server, vrf=vrf, timeout=timeout)
                else:
                    output = device.ping(server, timeout=timeout)
            except SubCommandFailure:
                # Success rate is 0%
                log.warning(
                    'Server {} is not reachable from device {}\nUnable '
                    'to meet minimum ping success rate of {}%\nRetrying'
                    ' after {} seconds'.format(server, device.name,
                                               min_success_rate, interval))
                time.sleep(interval)
                continue
            else:
                # Check if success rate was minimum success rate
                m1 = re.search(p1, output)
                m2 = re.search(p2, output)
                if m1:
                    if float(m1.groupdict()['success']) >= float(
                            min_success_rate):
                        section.passed('Server {} is reachable from device {}'.\
                                       format(server, device.name))
                        break
                elif m2:
                    group = m2.groupdict()
                    success_rate = (float(group['recv']) /
                                    float(group['transmit'])) * 100
                    if float(success_rate) >= float(min_success_rate):
                        section.passed('Server {} is reachable from device {}'.\
                                       format(server, device.name))
                        break

                # Minimum success rate not met, retry
                log.error('Server {} is not reachable from device {}\nUnable '
                          'to meet minimum ping success rate of {}%\nRetrying'
                          ' after {} seconds'.format(server, device.name,
                                                     min_success_rate,
                                                     interval))
                time.sleep(interval)
        else:
            step.failed('Server {} is not reachable from device {} after {} '
                        'attempts'.format(server, device.name, max_attempts))


#===============================================================================
#                       stage: copy_to_linux
#===============================================================================


@clean_schema({
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
    Optional('check_file_stability'): bool,
    Optional('unique_file_name'): bool,
    Optional('unique_number'): int,
    Optional('rename_images'): str
})
@aetest.test
def copy_to_linux(section,
                  steps,
                  device,
                  origin,
                  destination,
                  protocol='sftp',
                  timeout=300,
                  check_image_length=False,
                  overwrite=False,
                  append_hostname=False,
                  image_length_limit=63,
                  copy_attempts=1,
                  check_file_stability=False,
                  unique_file_name=False,
                  unique_number=None,
                  rename_images=None):
    """ This stage copies an image to a location on a linux device. It can keep
    the original name or modify the name as required.

    Stage Schema
    ------------
    copy_to_linux:
        origin:
            files: <File location on remote server or local disk, 'list'> (Mandatory)
            hostname: <Hostname or address of the server, if not provided the file will be treated as local. 'str'> (Optional)
        destination:
            directory: <Location on the file server, 'str'> (Mandatory)
            hostname: <Hostname or address of the file server, if not provided the directory will be treated as local.
                        This value is optional only when the hostname under origin is also optional. 'str'> (Optional)
        protocol: <Protocol used for copy operation, 'str', default sftp> (Optional)
        overwrite: <overwrite the file if the same file already exists, 'bool', default False> (Optional)
        timeout: <Copy operation timeout in seconds, default 300 'int'> (Optional)
        check_image_length: <check if image length exceeds certain limit 'bool', default False> (Optional)
        image_length_limit: <custom image length limit, defaults 63, 'int'>  (Optional)
        append_hostname: <append device hostname to the end of image while copying 'bool', default False> (Optional)
        copy_attempts: <number of times to retry if copy failed, default 1 (no retry) 'int'> (Optional)
        check_file_stability: <Verify if the files are still being copied on the file server, 'bool' default False> (Optional)
        unique_file_name: <Enable/Disable appending six-digit random number to the end of file name to make it unique, 'bool', default False> (Optional)
        unique_number: <User provided six-digit random number to append to the end of file name to make it unique, 'int', default None> (Optional)
        rename_images: <User provided new file name. If multiple files exist then we append an incrementing number 'str'> (Optional)

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

    if not hasattr(device.testbed, 'servers'):
        section.failed("Cannot find any servers in the testbed")

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
            section.failed("Server '{}' was provided in the clean yaml file "
                           "but doesn't exist in the testbed file".\
                           format(server_from))

        try:
            # Connect to the server
            server_from_obj.connect()
        except Exception as e:
            section.failed('Failed to connect to {} due to {}'.\
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
        section.failed(
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
                    except Exception:
                        log.warning(
                            "Could not verify the size for file '{}'".format(
                                file))

                # file to copy is local
                else:
                    try:
                        file_size = os.path.getsize(file)
                    except FileNotFoundError:
                        step.failed("Can not find file {} on local server."
                                    "Terminating clean".format(file))
                    except Exception:
                        log.warning(
                            "Could not verify the size for file '{}'".format(
                                file))

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

                image_mapping = section.history[
                    'copy_to_linux'].parameters.setdefault(
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
                        else:
                            substep.failed("Could not copy '{file}' to '{d}'\n{e}"\
                                        .format(file=file, d=destination_hostname, e=e))
                    else:
                        # copy passed, will not retry
                        log.info(
                            '{f} has been copied correctly'.format(f=file))
                        break

                # save the file copied name and size info for future use
                history = section.history[
                    'copy_to_linux'].parameters.setdefault('files_copied', {})
                history.update({file: file_data})

    # verify file copied section below
    with steps.start("Verify the files have been copied correctly") as step:
        if protocol.lower() in ['tftp', 'scp']:
            step.skipped(
                'tftp protocol does not support check file size, skipping this step.'
            )

        if 'files_copied' not in section.history['copy_to_linux'].parameters:
            step.skipped(
                'No files was copied in previous steps, skipping this step.')

        for name, image_data in section.history['copy_to_linux'].parameters[
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
                        section.passed("File size is the same on the origin "
                                       "and on the file server")
                except Exception as e:
                    step.failed("Failed to verify file. Error: {}".format(
                        str(e)))
            else:
                step.skipped("File has been copied correctly but cannot "
                             "verify file size")


#===============================================================================
#                       stage: copy_to_device
#===============================================================================


@clean_schema({
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
    Optional('check_file_stability'): bool,
    Optional('stability_check_tries'): int,
    Optional('stability_check_delay'): int,
    Optional('min_free_space_percent'): int,
})
@aetest.test
def copy_to_device(section,
                   steps,
                   device,
                   origin,
                   destination,
                   protocol,
                   verify_num_images=True,
                   expected_num_images=1,
                   vrf=None,
                   timeout=300,
                   compact=False,
                   use_kstack=False,
                   protected_files=None,
                   overwrite=False,
                   skip_deletion=False,
                   copy_attempts=1,
                   check_file_stability=False,
                   stability_check_tries=3,
                   stability_check_delay=2,
                   min_free_space_percent=None,
                   **kwargs):
    """ This stage will copy an image to a device from a networked location.

    Stage Schema
    ------------
    copy_to_device:
        origin:
            files ('list'): Image files location on the server (Mandatory)
            hostname ('str'): Hostname or address of the server (Mandatory)
        destination:
            directory ('str'): Location on the device to copy images (Mandatory)
        protocol ('str'): Protocol used for copy operation (Mandatory)
        verify_num_images ('bool'): Verify number of images provided by user
                                  for clean is correct
                                  Default True (Optional)
        expected_num_images ('int'): Number of images expected to be provided
                                   by user for clean
                                   Default 1 (Optional)
        vrf ('str'): Vrf name if applicable
                   Default None (Optional)
        timeout ('int'): Copy operation timeout in seconds
                       Default 300 (Optional)
        compact ('bool'): Compact copy mode if supported by the device
                        Default False (Optional)
        protected_files ('list'): File patterns that shouldn't be deleted
                                Default None (Optional)
        overwrite ('bool'): If image file already exists on device,
                          still copy the file to the device
                          Default False (Optional)
        skip_deletion ('bool'): Do not delete any files even if there isn't
                              any space on device
                              Default False (Optional)
        copy_attempts ('int'): Number of times to attempt copying image files
                             Default 1 (no retry) (Optional)
        check_file_stability ('bool'): Verify if the files are still being
                                     copied on the file server
                                     Default False (Optional)
        stability_check_tries ('int'): Max number of checks that can be done
                                     when checking file stability
                                     Default 3 (Optional)
        stability_check_delay ('int'): Delay between tries when checking file
                                     stability in seconds
                                     Default 2 (Optional)
        min_free_space_percent ('int') : Minimum acceptable free disk space
                                       percentage trying to reach by
                                       deleting unprotected files
                                       Default None (Optional)
        use_kstack ('bool'): Use faster version of copy with limited options
                           Default False (Optional)

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
    if not FileUtils.from_device(device).get_server_block(server):
        section.failed(
            "Server '{}' was provided in the clean yaml file but "
            "doesn't exist in the testbed file.\n".format(server), )

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
            image_mapping = section.history[
                'copy_to_device'].parameters.setdefault('image_mapping', {})
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

                if (not exist) or (exist and overwrite):
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
                            section, 'golden_config')
                        golden_image = find_clean_variable(
                            section, 'golden_image')

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
                                dir_output=dir_before)
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
                    if not overwrite and file_data['exist']:
                        step.skipped(
                            "File with the same name size exists on "
                            "the device {} {}, skipped copying".format(
                                device.name, dest))

                    for i in range(1, copy_attempts + 1):
                        try:
                            device.api.\
                                copy_to_device(protocol=protocol,
                                               server=file_utils.get_hostname(server),
                                               remote_path=file,
                                               local_path=file_data['dest_path'],
                                               vrf=vrf,
                                               timeout=timeout,
                                               compact=compact,
                                               use_kstack=use_kstack,
                                               **kwargs)
                        except Exception as e:
                            # Retry attempt if user specified
                            if i < copy_attempts:
                                log.warning("Attempt #{}: Unable to copy {} to '{} {}' due to:\n{}".\
                                            format(i, file, device.name, dest, e))
                                continue
                            else:
                                log.error(str(e))
                                step.failed(
                                    "Failed to copy image '{}' to '{}' on device"
                                    " '{}'\n".format(file, dest,
                                                     device.name), )
                        else:
                            log.info(
                                "File {} has been copied to {} on device {}"
                                " successfully".format(file, dest,
                                                       device.name))
                            success_copy_ha = True

                            break
                    # Save the file copied path and size info for future use
                    history = section.history['copy_to_device'].parameters.\
                                        setdefault('files_copied', {})
                    history.update({file: file_data})

            with steps.start("Verify images successfully copied") as step:
                # If nothing copied don't need to verify, skip
                if 'files_copied' not in section.history[
                        'copy_to_device'].parameters:
                    step.skipped(
                        "Image files were not copied for {} {} in previous steps, "
                        "skipping verification steps".format(device.name, dest))

                # Execute 'dir' after copying image files
                dir_after = device.execute('dir {}'.format(dest))

                for name, image_data in section.history['copy_to_device'].\
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
                                substep.passed("Size of image file copied to device {} is "
                                               "the same as image filesize on remote server".\
                                               format(device.name))
                        else:
                            substep.skipped(
                                "Image file has been copied to device {} correctly"
                                " but cannot verify file size".format(device.name))


#===============================================================================
#                       stage: write_erase
#===============================================================================


@clean_schema({
    Optional('timeout'): int,
})
@aetest.test
def write_erase(section, steps, device, timeout=300):
    """ This stage executes 'write erase' on the device

    Stage Schema
    ------------
    write_erase:
        timeout (int, optional): Max time allowed for command to complete. Defaults to 300 seconds.

    Example
    -------
    write_erase:
        timeout: 100

    """

    log.info('''Section steps:\n1 - Execute write erase on the device''')

    # Execute 'write erase' on the device
    with steps.start("Execute write erase on the device") as step:
        try:
            device.api.execute_write_erase(timeout=timeout)
        except Exception as e:
            step.failed("Unable to execute 'write erase' on {}:\n{}".\
                           format(device.name, str(e)))
        else:
            section.passed("Successfully executed 'write erase' on device {}".\
                            format(device.name))


#===============================================================================
#                       stage: reload
#===============================================================================


@clean_schema({
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
    }
})
@aetest.test
def reload(section,
           steps,
           device,
           reload_service_args=None,
           check_modules=None):
    """ This stage reloads the device.

    Stage Schema
    ------------
    reload:
        reload_service_args: (Optional, if not specified defaults below are used)
            timeout: <reload timeout value, default 800 seconds. 'int'> (Optional)
            reload_creds: <Credential name defined in the testbed yaml file to be used during reload, default 'default'. 'str'> (Optional)
            prompt_recovery: <Enable/Disable prompt recovery feature, 'bool'> (Optional)
            <Key>: <Value> (Any other key:value pairs that the unicon reload service allows for)

        check_modules:
            check: <Enable/Disable checking of modules after reload, default 'True'. 'bool'> (Optional)>
            timeout: <timeout value to verify modules are in stable state, default 180 seconds. 'int'> (Optional)
            interval: <interval value between checks for verifying module status, default 30 seconds. 'int'> (Optional)


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

    # Initialize 'reload_service_args' defaults if not defined by user
    if not reload_service_args:
        reload_service_args = {}
    reload_service_args.setdefault('timeout', 800)
    reload_service_args.setdefault('reload_creds', 'default')
    reload_service_args.setdefault('prompt_recovery', True)

    # Initialize 'check_modules' defaults if not defined by user
    if not check_modules:
        check_modules = {}
    check_modules.setdefault('check', True)
    check_modules.setdefault('timeout', 180)
    check_modules.setdefault('interval', 30)

    log.info("Section steps:\n1- Reload the device"
             "\n2- Disconnect from the device"
             "\n3- Reconnect to the device"
             "\n4- Verify all modules are in stable state after reload")

    # Reloading the device
    with steps.start("Reload '{dev}'".format(dev=device.name)) as step:
        try:
            device.reload(**reload_service_args)
        except Exception as e:
            step.failed("'{dev}' failed to reload within {timeout} seconds.\n"
                        "Error: {e}".format(
                            dev=device.name,
                            timeout=reload_service_args['timeout'],
                            e=str(e)))

        step.passed(
            "'{dev}' has successfully reloaded".format(dev=device.name))

    # Disconnect from the device
    with steps.start(
            "Disconnect from '{dev}'".format(dev=device.name)) as step:
        try:
            device.destroy()
        except Exception:
            # That's okay, as long we can reconnect, keep moving!
            pass
        else:
            step.passed("Disconnected successfully from device '{dev}'".format(
                dev=device.name))

    # Reconnect to device
    with steps.start("Reconnect to '{dev}'".format(dev=device.name)) as step:
        try:
            device.connect(
                learn_hostname=True,
                prompt_recovery=reload_service_args['prompt_recovery'])
        except Exception as e:
            step.failed("Could not reconnect to '{dev}':\nError: {e}".format(
                dev=device.name, e=str(e)))
        else:
            step.passed(
                "Successfully reconnected to '{dev}'".format(dev=device.name))

    # Verify all modules are in stable state
    if check_modules['check']:
        with steps.start(
                "Verify modules on '{dev}' are in a stable state".format(
                    dev=device.name)) as step:
            try:
                device.api.verify_module_status(
                    timeout=check_modules['timeout'],
                    interval=check_modules['interval'])
            except Exception:
                step.failed(
                    "Modules on '{dev}' are not in stable state".format(
                        dev=device.name))
            else:
                step.passed("Modules on '{dev}' are in stable state".format(
                    dev=device.name))


#===============================================================================
#                       stage: apply_configuration
#===============================================================================


@clean_schema({
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
})
@aetest.test
def apply_configuration(section, steps, device, configuration=None,
    configuration_from_file=None, file=None, config_timeout=60,
    config_stable_time=10, copy_vdc_all=False, max_time=300,
    check_interval=60, configure_replace=False, skip_copy_run_start=False):

    """ Apply configuration on the device, either by providing a file and/or
    raw configuration.

    Stage Schema
    ------------
    apply_configuration:
        configuration: <Configuration block to be applied, 'str'> (Optional)
        configuration_from_file: <File that contains a configuration to apply, 'str'> (Optional)
        file: <Configuration file for config replace> (Optional)
        configure_replace: <Use configure replace instead of copy 'bool'> (Optional)
        config_timeout: <Timeout in seconds, 'int'> (Optional)
        config_stable_time: <Time for configuration stability in seconds, 'int'> (Optional)
        copy_vdc_all: <To copy on all VDCs or not, 'bool'> (Optional)
        max_time: <Maximum time section will take for checks in seconds, 'int'> (Optional)
        check_interval: <Time interval, 'int'> (Optional)
        skip_copy_run_start: <Option to skip copy run start. Default False. 'bool'> (Optional)

    Example
    -------
    apply_configuration:
        configuration: |
            interface ethernet2/1
            no shutdown
        file: bootflash:/ISSUCleanGolden.cfg
        configure_replace: True
        config_timeout: 600
        config_stable_time: 10
        copy_vdc_all: True
        max_time: 300
        check_interval: 20

    """

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
                timeout=config_timeout)
        except Exception as e:
            step.failed("Error while applying configuration to device "
                        "{}\n{}".format(device.name, str(e)))
        else:
            step.passed(
                "Successfully applied configuration to device {} ".format(
                    device.name))

    # Copy running-config to startup-config
    if not skip_copy_run_start:
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
        section.passed("Successfully applied configuration after reloading "
                       "device {}".format(device.name))


#===============================================================================
#                       stage: verify_running_image
#===============================================================================


@clean_schema({Optional('images'): list})
@aetest.test
def verify_running_image(section, steps, device, images):
    """ This stage verifies the currently running image is the expected image.

    Stage Schema
    ------------
    verify_running_image:
        images: <Images reloaded on the device, 'list'> (Mandatory)

    Example
    -------
    verify_running_image:
        images:
            - test_image.gbin

    """

    log.info("Section steps:\n1- Verify the running image on the device")

    # Verify running image on the device
    with steps.start("Verify running image on device {}".\
                     format(device.name)) as step:
        try:
            device.api.verify_current_image(images=images)
        except Exception as e:
            step.failed("Unable to verify running image on device {}\n{}".\
                           format(device.name, str(e)))
        else:
            section.passed("Successfully verified running image on device {}".\
                           format(device.name))


#===============================================================================
#                       stage: backup_file_on_device
#===============================================================================


@clean_schema({
    'copy_dir': str,
    'copy_file': str,
    Optional('overwrite'): bool,
    Optional('timeout'): int,
})
@aetest.test
def backup_file_on_device(section,
                          steps,
                          device,
                          copy_dir,
                          copy_file,
                          overwrite=True,
                          timeout=300):
    """ This stage copies an existing file on the device and prepends 'backup_'
    to the start of the file name.

    Stage Schema
    ------------
    backup_file_on_device:
        copy_dir ('str'): Directory containing file to be backed up (Mandatory)
        copy_file ('str'): File to be backed up (Mandatory)
        overwrite ('bool'): Overwrite the file if exists. Default value is True (Optional)
        timeout ('int'): Copy timeout in second. Default value is 300 (Optional)

    Example
    -------
    backup_file_on_device:
        copy_dir: bootflash:
        copy_file: ISSUCleanGolden.cfg

    """

    log.info("Section steps:\n1- Backup file on the device")

    with steps.start("Backup file '{}/{}' on the device {}".\
                     format(copy_dir, copy_file, device.name)) as step:

        # Copy golden config to a backup file name, so that it can be
        # restored later (write erase destroys golden config on some
        # platforms).
        dest_file = "backup_{}".format(copy_file)

        # check space
        file_size = device.api.get_file_size(
            file='{}/{}'.format(copy_dir, copy_file))
        avail_space = device.api.get_available_space(directory=copy_dir)

        if file_size is None or avail_space is None:
            step.failed(
                "Failed to get '{}' file size or available space on {}".format(
                    copy_file, device.name))

        if avail_space <= file_size:
            step.failed("Do not have enough space to copy file. "
                        "Required '{}' bytes, Available '{}' bytes".format(
                            file_size, avail_space))
        else:
            log.info("Required '{}' bytes, Available '{}' bytes".format(
                file_size, avail_space))

        owt = Statement(
            pattern=r'.*over\s*write.*',
            action='sendline({})'.format('y' if overwrite else 'n'),
            loop_continue=True,
            continue_timer=False)
        # Copy file
        try:
            device.copy(source=copy_dir,
                        source_file=copy_file,
                        dest=copy_dir,
                        dest_file=dest_file,
                        reply=Dialog([owt]),
                        timeout=timeout)
        except Exception as e:
            log.error(str(e))
            step.failed("Unable to backup '{}/{}'' on device {}".format(
                copy_dir, copy_file, device.name))
        else:
            section.passed("Successfully backed up '{}/{}' on device {}".\
                           format(copy_dir, copy_file, device.name))


#===============================================================================
#                       stage: delete_backup_from_device
#===============================================================================


@clean_schema({
    'delete_dir': str,
    Optional('delete_dir_stby'): str,
    'delete_file': str,
    Optional('restore_from_backup'): bool,
    Optional('overwrite'): bool,
    Optional('timeout'): int,
})
@aetest.test
def delete_backup_from_device(section,
                              steps,
                              device,
                              delete_dir,
                              delete_file,
                              restore_from_backup=False,
                              overwrite=True,
                              delete_dir_stby=None,
                              timeout=300):
    """ This stage removes a backed up file from the device. It can optionally
    replace the original file with the one that was backed up.

    Stage Schema
    ------------
    delete_backup_from_device:
        delete_dir ('str'): Directory containing file to be deleted (Mandatory)
        delete_dir_stby ('str'): Directory containing file to be deleted for standby (Optional)
        delete_file ('str'): File to be deleted up (Mandatory)
        restore_from_backup ('bool'): Restore the file from backup file.
                                    Default value is False (Optional)
        overwrite ('bool'): Overwrite the file if exists. Default value is True (Optional)
        timeout ('int'): Copy/Execute timeout in second. Default value is 300 (Optional)

    Example
    -------
    delete_backup_from_device:
        delete_dir: 'bootflash:'
        delete_dir_stby: 'bootflash-stby:'
        delete_file: ISSUCleanGolden.cfg_backup

    """

    log.info("Section steps:\n1- Delete the targeted file")

    delete_backup = Statement(pattern=r'.*Do you want to delete.*',
                              action='sendline(y)',
                              loop_continue=True,
                              continue_timer=False)

    with steps.start("Delete the targeted file '{}/{}' from device {}".\
                     format(delete_dir, delete_file, device.name)) as step:

        if restore_from_backup:
            # Set original filename
            original_file = delete_file.strip("backup_")

            owt = Statement(
                pattern=r'.*over\s*write.*',
                action='sendline({})'.format('y' if overwrite else 'n'),
                loop_continue=True,
                continue_timer=False)
            try:
                log.info("Restoring the file from backup file")
                # Copy back the golden config file
                device.copy(source=delete_dir,
                            source_file=delete_file,
                            dest=delete_dir,
                            dest_file=original_file,
                            reply=Dialog([owt]),
                            timeout=timeout)
            except Exception as e:
                log.error(e)
                step.failed(
                    "Unable to restore '{}/{}'' on device {}".format(
                        delete_dir, delete_file, device.name), )

        device.execute.error_pattern.extend(['.*%Error.*'])
        try:
            # Delete the golden backup file
            device.execute('delete {}{}'.format(delete_dir, delete_file),
                           reply=Dialog([delete_backup]))
        except Exception as e:
            log.error(e)
            step.failed("Unable to delete '{}/{} from device {}".format(
                delete_dir, delete_file, device.name))
        else:
            if not device.is_ha:
                step.passed("Successfully deleted '{}/{}' from device {}".\
                                format(delete_dir, delete_file, device.name))

            # Delete file from on standby
            if device.is_ha and delete_dir_stby:
                # Make sure standby directory is provided

                # Delete the golden backup file
                log.info("Successfully deleted '{}/{}' from device {}".format(
                    delete_dir, delete_file, device.name))
                log.info("Deleting '{}/{}' on standby from device{}".format(
                    delete_dir_stby, delete_file, device.name))
                try:
                    device.execute('delete {}{}'.format(
                        delete_dir_stby, delete_file),
                                   reply=Dialog([delete_backup]))
                except Exception as e:
                    log.error(e)
                    log.error("*** Cannot delete from standby ***")
                    step.failed(
                        "Unable to delete '{}/{} from device {}".format(
                            delete_dir_stby, delete_file, device.name))
                else:
                    step.passed("Successfully deleted from standby '{}/{}' from device {}".\
                                format(delete_dir_stby, delete_file, device.name))
            else:
                step.failed(
                    "*** HA device, but no standby device provided ***")


#===============================================================================
#                       stage: delete_files_from_server
#===============================================================================


@clean_schema({
    Optional('server'): str,
    Optional('files'): list,
    Optional('protocol'): str,
})
@aetest.test
def delete_files_from_server(section,
                             steps,
                             device,
                             server=None,
                             files=None,
                             protocol='sftp'):
    """ This stage deletes files from a server.

    Stage Schema
    ------------
    delete_files_from_server:
        server ('str'): <Hostname or address of the server> (optional)
        files ('list'): <list of images to delete> (Optional)
        protocol ('str'): <protocol used for deletion, Default value is sftp> (Optional)

    Example
    -------
    delete_files_from_server:
        server: 1.1.1.1
        files:
            - /home/cisco/kickstart.bin
        protocol: sftp

    """

    # pyats FU only support sftp or ftp delete
    # if image not provided, get it from copy stage
    with steps.start('Deleting files from the server') as step:
        # establish a FileUtils session for all FileUtils operations
        fu = FileUtils(testbed=device.testbed)
        if not files:
            if 'copy_to_linux' in section.history:
                log.info(
                    "No file has been provided to delete in the clean yaml, "
                    "will delete the files copied from 'copy_to_linux' stage.")
                files = getattr(section.history['copy_to_linux'], 'parameters', {}).\
                                                 get('files_copied', {})

                # covert the stored file paths to a list of files
                files = [files[file]['dest_path'] for file in files]
            else:
                section.skipped(
                    "No file has been provided to delete in the clean yaml file"
                )

        if not server:
            log.info(
                "No server has been provided in the clean yaml, will use the same server "
                "from 'copy_to_linux' stage.")
            if 'copy_to_linux' in section.history:
                server = getattr(section.history['copy_to_linux'], 'parameters').\
                                 get('destination', {}).get('hostname')

        if not server:
            step.failed("No server has been provided in the clean yaml file")

        for file in files:
            with step.start('Deleting {f}'.format(f=file)) as substep:
                try:
                    device.api.delete_file_on_server(testbed=device.testbed,
                                                     path=file,
                                                     server=server,
                                                     protocol=protocol,
                                                     fu_session=fu)
                except Exception as e:
                    substep.passx('Failed to delete image "{}" due '
                                  'to :{}'.format(file, str(e)))


#===============================================================================
#                       stage: revert_vm_snapshot
#===============================================================================
@clean_schema({
    'esxi_server': str,
    'recovery_snapshot_name': str,
    Optional('vm_hostname'): str,
    Optional('max_recovery_attempts'): int,
    Optional('sleep_time_after_powering_off'): int,
    Optional('sleep_time_after_powering_on'): int,
    Optional('sleep_time_stabilize_device'): int
})
@aetest.test
def revert_vm_snapshot(section,
                       steps,
                       device,
                       esxi_server,
                       recovery_snapshot_name,
                       max_recovery_attempts=2,
                       vm_hostname="",
                       sleep_time_after_powering_off=60,
                       sleep_time_stabilize_device=300,
                       sleep_time_after_powering_on=600):
    """ This stage reverts the virtual device to the provided snapshot

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

@clean_schema({
    Optional('sleep_after_power_off'): int,
    Optional('boot_timeout'): int
})
@aetest.test
def power_cycle(section, steps, device, sleep_after_power_off=30, boot_timeout=600):
    """ This stage power cycles the device

        Stage schema
        ------------
        power_cycle:

            sleep_after_power_off (int, optional): Time in seconds to sleep
                after powering off the device. Defaults to 30.

            boot_timeout (int, option): Max time in seconds allowed for the
                device to boot. Defaults to 600.

        Example
        -------
        power_cycle:
            sleep_after_power_off: 5
    """

    with steps.start("Powercycling '{}'".format(device.name)) as step:
        try:
            device.api.execute_power_cycle_device(
                delay=sleep_after_power_off)
        except Exception as e:
            step.failed("Failed to powercycle '{}'. Error: {}".format(
                device.name, str(e)))


    with steps.start("Reconnecting to '{dev}'".format(
            dev=device.name)) as step:

        timeout = Timeout(boot_timeout, 60)
        while timeout.iterate():
            timeout.sleep()
            device.destroy()

            try:
                device.connect(learn_hostname=True)
            except Exception as e:
                connection_error = e
                log.info("Could not connect to {dev}"
                         .format(dev=device.hostname))
            else:
                step.passed("Connected to {dev}"
                            .format(dev=device.hostname))

        step.failed("Could not connect to {dev}. Error: {e}"
                    .format(dev=device.hostname, e=str(connection_error)))