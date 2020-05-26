
# Python
import re
import time
import shutil
import os.path
import logging

# pyATS
from pyats import aetest
from pyats.log.utils import banner
from pyats.utils.fileutils import FileUtils

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure, ConnectionError

# Genie
from genie.libs.clean.utils import clean_schema
from genie.libs.clean.utils import _apply_configuration, find_clean_variable,\
                                   verify_num_images_provided

# MetaParser
from genie.metaparser.util.schemaengine import Optional

# Logger
log = logging.getLogger()


#===============================================================================
#                       stage: connect
#===============================================================================

def handle_rommon_exception(spawn, context):
    log.error('Device is in Rommon')
    raise Exception('Device is in Rommon')

@clean_schema({
    Optional('timeout'): str,
})
@aetest.test
def connect(section, device, timeout=200, **kwargs):
    """
    Checks if the connection to device is available
    """
    log.info('Checking connection to device : %s' % device.name)

    # If the device is in rommon, just raise an exception
    device.instantiate(timeout=timeout, learn_hostname=True)
    rommon = Statement(pattern=r'^(.*)(rommon(.*)|loader(.*))+>.*$',
                       #action=lambda section: section.failed('Device is in rommon'),
                       action=handle_rommon_exception,
                       loop_continue=False,
                       continue_timer=False)
    device.connect_reply.append(rommon)

    try:
        device.connect(learn_hostname=True)
    except Exception as err:
        log.error('Connection to the device failed, with error {e}'.\
                  format(e=str(err)))
        device.destroy_all()
        section.failed("Could not connect to '{d}'".format(d=device.name))
    else:
        section.passed("Successfully connected to '{}'".format(device.name))
    finally:
        try:
            device.connect_reply.remove(rommon)
        except Exception:
            pass


#===============================================================================
#                       stage: ping_server
#===============================================================================

@clean_schema({
    'server':str,
    Optional('vrf'): str,
    Optional('timeout'): int,
    Optional('min_success_rate'): int,
    Optional('max_attempts'): int,
    Optional('interval'): int,
})
@aetest.test
def ping_server(section, steps, device, server, vrf=None, timeout=60,
    min_success_rate=60, max_attempts=5, interval=30):
    '''
    Clean yaml file schema:
    -----------------------
        devices:
            <device>:
                ping_server:
                  server: <Hostname or address of the server to ping `str`> (Mandatory)
                  vrf: <Vrf used in ping `str`> (Optional)
                  timeout: <timeout for ping command. Default 60 seconds `int`> (Optional)
                  min_success_rate: <minimum ping success rate to mark seciton as passed. Default 60 % `int`> (Optional)
                  max_attempts: <maximum number of attempts to check minimum ping success rate. Default 5 `int`> (Optional)
                  interval: <time between re-attempts to check minimum ping success rate. Default 30 seconds `int`> (Optional)

    Example:
    --------
        devices:
            N95_1:
                ping_server:
                  server: server-1
                  vrf: management
                  timeout: 120
                  min_success_rate: 75
                  max_attempts: 3
                  interval: 60

    Flow:
    -----
        before:
            copy_to_device (Optional, checks if server is reachable before trying to copy)
        after:
            None
    '''

    with steps.start("Checking connectivity between device and file server"):

        # Patterns for success rate
        p1 = r'Success +rate +is +(?P<success>(\d+)) +percent +\((?P<pass>(\d+))\/(?P<fail>(\d+))\)'
        p2 = r'(?P<transmit>(\d+)) +packets +transmitted, (?P<recv>(\d+)) +packets +received, (?P<loss>(\S+))% +packet +loss'

        # Verify given server is found in the testbed YAML file
        try:
            server_from_obj = device.api.convert_server_to_linux_device(server)
        except Exception:
            log.error(banner("*** Terminating Genie Clean ***"))
            section.failed("Server '{}' was provided in the clean YAML file "
                           "but doesn't exist in the testbed YAML file".\
                           format(server), goto=['exit'])
        else:
            log.info("Server '{}' found in the testbed YAML file".\
                     format(server))

        # If hostname of server given, return IP address
        fu = FileUtils(testbed=device.testbed)
        server = fu.get_hostname(server)

        for i in range(1, max_attempts+1):
            log.info ("\nAttempt #{}: Ping server '{}'".format(i, server))

            # Ping server from device
            try:
                if vrf:
                    output = device.ping(server, vrf=vrf, timeout=timeout)
                else:
                    output = device.ping(server, timeout=timeout)
            except SubCommandFailure:
                # Success rate is 0%
                log.warning('Server {} is not reachable from device {}\nUnable '
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
                    if float(m1.groupdict()['success']) >= float(min_success_rate):
                        section.passed('Server {} is reachable from device {}'.\
                                       format(server, device.name))
                        break
                elif m2:
                    group = m2.groupdict()
                    success_rate = (float(group['recv'])/float(group['transmit']))*100
                    if float(success_rate) >= float(min_success_rate):
                        section.passed('Server {} is reachable from device {}'.\
                                       format(server, device.name))
                        break

                # Minimum success rate not met, retry
                log.error('Server {} is not reachable from device {}\nUnable '
                            'to meet minimum ping success rate of {}%\nRetrying'
                            ' after {} seconds'.format(server, device.name,
                            min_success_rate, interval))
                time.sleep(interval)
        else:
            log.error(banner("*** Terminating Genie Clean ***"))
            section.failed('Server {} is not reachable from device {} after {} '
                           'attempts'.format(server, device.name, max_attempts),
                           goto=['exit'])


#===============================================================================
#                       stage: copy_to_linux
#===============================================================================

@clean_schema({
    'origin':{
        'files': list,
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
})
@aetest.test
def copy_to_linux(section, steps, device, origin, destination, protocol='sftp',
    timeout=300, check_image_length=False, overwrite=False,
    append_hostname=False, image_length_limit=63, copy_attempts=1,
    check_file_stability=False, unique_file_name=False, unique_number=None):

    '''
    Clean yaml file schema:
    -----------------------
        devices:
            <device>:
                copy_to_linux:
                    origin:
                        files: <File location on remote server or local disk, 'list'> (Mandatory)
                        hostanme: <Hostname or address of the server, if not provided the file will be treated as local. 'str'> (Optional)
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

    Example:
    --------
        devices:
            N95_1:
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

    Flow:
    -----
        before:
            None
        after:
            None
    '''

    if not hasattr(device.testbed, 'servers'):
        log.error(banner("*** Terminating Genie Clean ***"))
        section.failed("Cannot find any servers in the testbed", goto=['exit'])

    destination_hostname = destination.get('hostname')

    origin_path = origin['files']

    if len(origin_path) == 0:
        log.error(banner("*** Terminating Genie Clean ***"))
        section.failed("No file was provided to copy. Please provide files under destination.path in the clean yaml file.", goto=['exit'])

    dest_dir = destination['directory']

    # If not provided, assume its localhost
    server_from = origin.get('hostname')

    if not server_from:
        server_from_obj = None
    else:
        try:
            # From IP/hostname find server from testbed file - get device obj
            server_from_obj = device.api.convert_server_to_linux_device(server_from)
        except (KeyError, AttributeError):
            log.error(banner("*** Terminating Genie Clean ***"))
            section.failed("Server '{}' was provided in the clean yaml file "
                           "but doesn't exist in the testbed file".\
                           format(server_from), goto=['exit'])

        try:
            # Connect to the server
            server_from_obj.connect()
        except Exception as e:
            log.error(banner("*** Terminating Genie Clean ***"))
            section.failed('Failed to connect to {} due to {}'.\
                           format(server_from_obj.name, str(e)), goto=['exit'])

    # establish a FileUtils session for all FileUtils operations
    fu = FileUtils(testbed=device.testbed)

    files_to_copy = {}
    with steps.start("Collecting file info on origin and '{d}' "
                     "before copy".format(d=destination_hostname or dest_dir)) as step:
        file_size = -1
        for file in origin_path:
            with step.start("Collecting '{f}' info".format(f=file)) as substep:
                # file to copy is remote
                if server_from:
                    try:
                        log.info(
                            "Getting size of the file '{}' from file server '{}'".format(
                                file, server_from))
                        file_size = device.api.get_file_size_from_server(server=server_from,
                                                                         path=file,
                                                                         protocol=protocol,
                                                                         timeout=timeout,
                                                                         fu_session=fu)
                    except FileNotFoundError:
                        log.error(banner("*** Terminating Genie Clean ***"))
                        section.failed("Can not find file {} on server {}. Terminating clean"
                            .format(file, server_from), goto=['exit'])
                    except Exception:
                        log.warning("Could not verify the size for file '{}'".format(file))

                # file to copy is local
                else:
                    try:
                        file_size = os.path.getsize(file)
                    except FileNotFoundError:
                        log.error(banner("*** Terminating Genie Clean ***"))
                        section.failed("Can not find file {} on local server."
                            "Terminating clean".format(file), goto=['exit'])
                    except Exception:
                        log.warning("Could not verify the size for file '{}'".format(file))

                try:
                    new_name = device.api.modify_filename(file=os.path.basename(file),
                                                          directory=dest_dir,
                                                          protocol=protocol,
                                                          append_hostname=append_hostname,
                                                          check_image_length=check_image_length,
                                                          limit=image_length_limit,
                                                          unique_file_name=unique_file_name,
                                                          unique_number=unique_number)
                except Exception as e:
                    log.error(banner("*** Terminating Genie Clean ***"))
                    section.failed("Can not change file name. Terminating clean:\n{e}"
                            .format(e=e), goto=['exit'])

                file_path = os.path.join(destination_hostname or dest_dir, new_name)

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
                        log.error("Unable to verify if file '{}' already exists"
                                  " at {}\n{}".format(file_path,
                                  destination_hostname or dest_dir, str(e)))
                else:
                    exist = False

                file_copy_info = {
                    file: {
                        'size': file_size,
                        'dest_path': file_path,
                        'exist': exist
                    }}
                files_to_copy.update(file_copy_info)

                substep.passed('Verified file {} on source and destination servers'.format(os.path.basename(file)))

    if check_file_stability:
        with steps.start("Check if any file is being copied") as step:
            if not server_from:
                # no need to check stability if the file is local
                step.skipped("File is local, skipping this step")

            log.info("Verify if the files are still being copied on the origin server")

            for file, file_data in files_to_copy.items():

                with step.start("Verify stability of '{f}'".format(f=file)) as substep:

                    try:
                        stable = device.api.verify_file_size_stable_on_server(protocol=protocol,
                                                                              server=server_from,
                                                                              file=file,
                                                                              timeout=timeout,
                                                                              fu_session=fu)
                    except NotImplementedError as e:
                        step.skipped(str(e))

                    if not stable:
                        fu.close()
                        log.error(banner("*** Terminating Genie Clean ***"))
                        section.failed("The the size of file '{}' on server "
                                       "'{}' is not stable".format(file,
                                       server_from), goto=['exit'])

    with steps.start("Check if there is enough space on {server} to "
                     "perform the copy".format(server=destination_hostname or dest_dir)) as step:

        total_size = sum(file_data['size'] for file_data in files_to_copy.values())

        try:
            if not device.api.verify_enough_server_disk_space(server=destination_hostname,
                                                              required_space=total_size,
                                                              directory=dest_dir,
                                                              protocol=protocol,
                                                              timeout=timeout,
                                                              fu_session=fu):
                fu.close()
                log.error(banner("*** Terminating Genie Clean ***"))
                section.failed("There is not enough space on server '{}' at '{}'."
                               "Terminating clean".format(destination_hostname,
                                                            dest_dir),
                               goto=['exit'])
        except NotImplementedError as e:
            step.skipped(str(e))
        except Exception as e:
            step.skipped(str(e))

    with steps.start("Copying the files to {}".format(destination_hostname or dest_dir)) as step:
        for file, file_data in files_to_copy.items():
            with step.start("Copying '{}'".format(file)) as substep:
                if not overwrite and file_data['exist']:
                    substep.skipped(
                        'File with the same name and same size already exist on the '
                        'server and overwrite is set to False, skipped copying')

                for i in range(1, copy_attempts + 1):
                    try:
                        if server_from:
                            server_from_obj.api.copy_from_device(remote_path=file_data['dest_path'],
                                                                 local_path=file,
                                                                 server=destination_hostname,
                                                                 protocol=protocol,
                                                                 timeout=timeout,
                                                                 quiet=True)
                        elif destination_hostname:
                            device.api.copy_to_server(testbed=device.testbed,
                                                      remote_path=file_data['dest_path'],
                                                      local_path=file,
                                                      server=destination_hostname,
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
                                    file=file, d=destination_hostname, e=e, iteration=i+1))
                        else:
                            section.failed("Could not copy '{file}' to '{d}'\n{e}".format(
                                    file=file, d=destination_hostname, e=e))
                    else:
                        # copy passed, will not retry
                        log.info('{f} has been copied correctly'.format(f=file))
                        break

                # save the file copied name and size info for future use
                history = section.history['copy_to_linux'].parameters.setdefault(
                    'files_copied', {})
                history.update({file: file_data})

    # verify file copied section below
    with steps.start("Verify the files have been copied correctly") as step:
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
                        log.error(banner("*** Terminating Genie Clean ***"))
                        section.failed("File size is not the same on the origin"
                                       " and on the file server", goto=['exit'])
                    else:
                        section.passed("File size is the same on the origin "
                                       "and on the file server")
                except Exception as e:
                    log.error(banner("*** Terminating Genie Clean ***"))
                    section.failed("File size is not the same on the origin"
                                   " and on the file server", goto=['exit'])
            else:
                step.skipped("File has been copied correctly but cannot "
                             "verify file size")


#===============================================================================
#                       stage: copy_to_device
#===============================================================================

@clean_schema({
    'origin':{
        'files': list,
        'hostname': str
        },
    'destination': {
        'directory': str,
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
def copy_to_device(section, steps, device, origin, destination, protocol,
    verify_num_images=True, expected_num_images=1, vrf=None, timeout=300,
    compact=False, use_kstack=False, protected_files=None,
    overwrite=False, skip_deletion=False, copy_attempts=1,
    check_file_stability=False, stability_check_tries=3,
    stability_check_delay=2, min_free_space_percent=None, **kwargs):

    '''
    Clean yaml file schema:
    -----------------------
    devices:
      <device>:
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

    Example:
    --------
    devices:
      ASR1_1:
        copy_to_device:
          protocol: sftp
          origin:
            hostname: server-1
            files:
            - /home/cisco/asr1k.bin
          timeout: 300
          destination:
              directory: harddisk:/

    Flow:
    -----
    before:
      None
    after:
      None
    '''

    log.info("Section steps:\n1- Verify correct number of images provided"
             "\n2- Get filesize of image files on remote server"
             "\n3- Check if image files already exist on device"
             "\n4- (Optional) Verify stability of image files"
             "\n5- Verify free space on device else delete unprotected files"
             "\n6- Copy image files to device"
             "\n7- Verify copied image files are present on device")

    # Get args
    server = origin['hostname']
    image_files = origin['files']
    destination = destination['directory']

    # Check remote server info present in testbed YAML
    if not FileUtils.from_device(device).get_server_block(server):
        log.error(banner("*** Terminating Genie Clean ***"))
        section.failed("Server '{}' was provided in the clean yaml file but "
                       "doesn't exist in the testbed file.\n".format(server),
                       goto=['exit'])

    # Check image files provided
    if verify_num_images:
        # Verify correct number of images provided
        with steps.start("Verify correct number of images provided") as step:
            if not verify_num_images_provided(image_list=image_files,
                                        expected_images=expected_num_images):
                log.error(banner("*** Terminating Genie Clean ***"))
                section.failed("Incorrect number of images provided. Please "
                               "provide {} expected image(s) under destination"
                               ".path in clean yaml file.\n".format(
                                expected_num_images), goto=['exit'])
            else:
                step.passed("Correct number of images provided")

    # Init
    files_to_copy = {}
    unknown_size = False

    # Establish FileUtils session for all FileUtils operations
    file_utils = FileUtils(testbed=device.testbed)

    # Execute 'dir' before copying image files
    log.info(banner("Executing 'dir {}' before copying image files".\
                    format(destination)))
    dir_before = device.execute('dir {}'.format(destination))

    # Loop over all image files provided by user
    for file in image_files:

        # Get filesize of image files on remote server
        with steps.start("Get filesize of '{}' on remote server '{}'".\
                        format(file, server)) as step:
            try:
                file_size = device.api.get_file_size_from_server(
                                            server=server,
                                            path=file,
                                            protocol=protocol,
                                            timeout=timeout,
                                            fu_session=file_utils)
            except FileNotFoundError:
                log.error(banner("*** Terminating Genie Clean ***"))
                section.failed("Can not find file {} on server {}. Terminating clean"
                    .format(file, server), goto=['exit'])
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
        
        # Check if file with same name and size exists on device
        dest_file_path = os.path.join(destination, os.path.basename(file))
        with steps.start("Check if file '{}' exists on device {}".\
                        format(dest_file_path, device.name)) as step:

            # Check if file exists
            try:
                exist = device.api.verify_file_exists(file=dest_file_path,
                                                      size=file_size,
                                                      dir_output=dir_before)
                if (not exist) or (exist and overwrite):
                    # Update list of files to copy
                    file_copy_info = {
                        file: {
                            'size': file_size,
                            'dest_path': dest_file_path,
                            'exist': exist
                        }}
                    files_to_copy.update(file_copy_info)
                    # Print message to user
                    step.passed("Proceeding with copying image {} to device {}".\
                                format(dest_file_path, device.name))
                else:
                    step.passed("Image '{}' already exists on device {}, "
                                "skipping copy".format(file, device.name))
            except Exception as e:
                log.warning(str(e))
                step.passx("Unable to check if image '{}' exists on device {}".\
                           format(dest_file_path, device.name))

    # Check if any file copy is in progress
    if check_file_stability:
        for file in files_to_copy:
            with steps.start("Verify stability of file '{}'".\
                             format(file)) as step:
                # Check file stability
                try:
                    stable = device.api.verify_file_size_stable_on_server(
                                                file=file,
                                                server=server,
                                                protocol=protocol,
                                                fu_session=file_utils,
                                                delay=stability_check_delay,
                                                max_tries=stability_check_tries)

                    if not stable:
                        log.error(banner("*** Terminating Genie Clean ***"))
                        section.failed("The size of file '{}' on server is not "
                                       "stable\n".format(file),
                                       goto=['exit'])
                    else:
                        step.passed("Size of file '{}' is stable".format(file))
                except NotImplementedError:
                    # cannot check using tftp
                    step.passx("Unable to check file stability over {protocol}"
                               .format(protocol=protocol))
                except Exception as e:
                    log.error(str(e))
                    log.error(banner("*** Terminating Genie Clean ***"))
                    section.failed("Error while verifying file stability on "
                                   "server\n", goto=['exit'])

    # Verify available space on the device is sufficient for image copy, delete
    # unprotected files if needed, copy file to the device 
    # unless overwrite: False
    if files_to_copy:
        with steps.start("Verify sufficient free space on device '{}' or delete"
                         " unprotected files".format(device.name)) as step:
            if unknown_size:
                total_size = -1
                log.warning("Amount of space required cannot be confirmed, "
                            "copying the files on the device '{}' may fail".\
                            format(device.name))
            else:
                # Check protected files list
                if not protected_files:
                    protected_files = []

                # TODO: add golden images, config to protected files once we have golden section
                golden_config = find_clean_variable(section, 'golden_config')
                golden_image = find_clean_variable(section, 'golden_image')

                if golden_config:
                    protected_files.extend(golden_config)
                if golden_image:
                    protected_files.extend(golden_image)

                for file, file_data in files_to_copy.items():
                    # Only calculate size of file being copied
                    total_size = sum(0 if file_data['exist'] \
                                     else file_data['size'] for \
                                     file_data in files_to_copy.values())

                    try:
                        free_space = device.api.free_up_disk_space(
                                        destination=destination,
                                        required_size=total_size,
                                        skip_deletion=skip_deletion,
                                        protected_files=protected_files,
                                        min_free_space_percent=min_free_space_percent,
                                        dir_output=dir_before)
                        if not free_space:
                            log.error(banner("*** Terminating Genie Clean ***"))
                            section.failed("Unable to create enough space for "
                                           "image on device {}".\
                                           format(device.name), goto=['exit'])
                        else:
                            step.passed("Device has sufficient space to "
                                        "copy images")
                    except Exception as e:
                        log.error(str(e))
                        log.error(banner("*** Terminating Genie Clean ***"))
                        section.failed("Error while creating free space for "
                                       "image on device {}".\
                                       format(device.name), goto=['exit'])

    # Copy the file to the devices
    for file, file_data in files_to_copy.items():
        with steps.start("Copying image file {} to device {}".\
                         format(file, device.name)) as step:
            with step.start("Copying image '{}' to '{}'".\
                            format(file, device.name)) as substep:

                # Copy file unless overwrite is False
                if not overwrite and file_data['exist']:
                    substep.skipped("File with the same name size exists on "
                                    "the device, skipped copying")

                for i in range(1, copy_attempts+1):
                    try:
                        device.api.\
                            copy_to_device(protocol=protocol,
                                           server=server,
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
                            log.warning("Attempt #{}: Unable to copy {} to '{}' due to:\n{}".\
                                        format(i, file, device.name, e))
                            continue
                        else:
                            log.error(str(e))
                            log.error(banner("*** Terminating Genie Clean ***"))
                            section.failed("Failed to copy image '{}' to device"
                                           " '{}'\n".format(file, device.name),
                                           goto=['exit'])
                    else:
                        log.info("File {} has been copied to device {} "
                                 "successfully".format(file, device.name))
                        break

                # Save the file copied path and size info for future use
                history = section.history['copy_to_device'].parameters.\
                                  setdefault('files_copied', {})
                history.update({file: file_data})

    # If nothing copied dont need to verify, skip
    if 'files_copied' not in section.history['copy_to_device'].parameters:
        step.skipped("Image files were not copied in previous steps, "
                     "skipping verification steps")

    # Execute 'dir' after copying image files
    log.info(banner("Executing 'dir {}' after copying image files".\
                    format(destination)))
    dir_after = device.execute('dir {}'.format(destination))

    for name, image_data in section.history['copy_to_device'].\
                                    parameters['files_copied'].items():

        with steps.start("Verify image '{}' copied to device {}".\
                        format(image_data['dest_path'], device.name)) as step:

            # if size is -1 it means it failed to get the size
            if image_data['size'] != -1:
                if not device.api.verify_file_exists(
                                            file=image_data['dest_path'],
                                            size=image_data['size'],
                                            dir_output=dir_after):
                    log.error(banner("*** Terminating Genie Clean ***"))
                    section.failed("Size of image file copied to device {} is "
                                   "not the same as remote server filesize".\
                                   format(device.name), goto=['exit'])
                else:
                    section.passed("Size of image file copied to device {} is "
                                   "the same as imaage filesize on remote server".\
                                   format(device.name))
            else:
                step.skipped("Image file has been copied to device {} correctly"
                             " but cannot verify file size".format(device.name))


#===============================================================================
#                       stage: write_erase
#===============================================================================

@clean_schema({
    Optional('timeout'): int,
})
@aetest.test
def write_erase(section, steps, device, timeout=300):

    '''
    Clean yaml file schema:
    -----------------------
    devices:
      <device>:
        write_erase:

    Example:
    --------
    devices:
      N95_1:
        write_erase:

    Flow:
    -----
    before:
      backup_file_on_device (Optional, Backup configuration file then perform write erase)
    after:
      delete_backup_from_device (Optional, Delete the backed up configuration file)
      apply_golden_config (Optional, user wants to apply golden config or not)
    '''

    log.info('''Section steps:\n1 - Execute write erase on the device''')

    # Execute 'write erase' on the device
    with steps.start("Execute write erase on the device") as step:
        try:
            device.api.execute_write_erase(timeout=timeout)
        except Exception as e:
            log.error(banner("*** Terminating Genie Clean ***"))
            section.failed("Unable to execute 'write erase' on {}:\n{}".\
                           format(device.name, str(e)), goto=['exit'])
        else:
            section.passed("Successfully executed 'write erase' on device {}".\
                            format(device.name))

#===============================================================================
#                       stage: reload
#===============================================================================

@clean_schema({
    Optional('prompt_recovery'): bool,
    Optional('sleep_after_reload'): int,
    Optional('credentials'): str,
    Optional('timeout'): int,
    Optional('check_modules'): bool,
    Optional('module_timeout'): int,
    Optional('module_interval'): int,
})
@aetest.test
def reload(section, steps, device, prompt_recovery=True, sleep_after_reload=120,
    credentials=None, timeout=800, check_modules=True, module_timeout=180,
    module_interval=30):

    '''
    Clean yaml file schema:
    -----------------------
    devices:
      <device>:
        reload:
          prompt_recovery: <Enable/Disable prompt recovery feature, 'bool'> (Optional)
          sleep_after_reload: <Time to sleep after reload, 'int'> (Optional)
          credentials: <Credential name defined in the testbed yaml file to be used during reload, 'str'> (Optional)
          timeout: <reload timeout value, default 800 seconds. 'int'> (Optional)
          check_modules: <Enable/Disable checking of modules after reload, 'bool'> (Optional)
          module_timeout: <timeout value to verify modules are in stable state, default 180 seconds. 'int'> (Optional)
          module_interval: <interval value between checks for verifying module status, default 30 seconds. 'int'> (Optional)

    Example:
    --------
    devices:
      N95_1:
        reload:
          prompt_recovery: True
          sleep_after_reload: 120
          credentials: clean_reload_creds
          timeout: 600
          check_modules: True
          module_timeout: 120
          module_interval: 30

    Flow:
    -----
    before:
      change_boot_variable (Mandatory)
      apply_golden_config (Optional, configure device to come up with specific startup configs)
    after:
      change_boot_variable (Optional, to verify current boot variable and set next)
    '''

    log.info("Section steps:\n1- Reload the device"
             "\n2- Disconnect from the device"
             "\n3- Reconnect to the device"
             "\n4- Verify all modules are in stable state after reload")

    # Reloading the device
    with steps.start("Reload device {}".format(device.name)) as step:
        try:
            device.api.execute_reload(prompt_recovery=prompt_recovery,
                                      reload_creds=credentials,
                                      sleep_after_reload=sleep_after_reload,
                                      timeout=timeout)
        except (SubCommandFailure, TimeoutError) as e:
            # Could not reload the device, or it didn't go as expected
            log.error(banner("*** Terminating Genie Clean ***"))
            section.failed("Could not reload the device correctly in the "
                           "maximum allotted time of {} seconds:\n{}".\
                           format(timeout, str(e)), goto=['exit'])
        else:
            log.info("Device {} has reloaded successfully".format(device.name))

    # Disconnect from the device
    with steps.start("Disconnect from device {} after reload".\
                     format(device.name)) as step:
        try:
            device.destroy()
        except Exception as e:
            # That's okay, as long we can reconnect, keep moving!
            pass
        else:
            log.info("Disconnected successfully from device '{}'".\
                     format(device.name))

    # Reconnect to device
    with steps.start("Reconnect to device {} after reload".\
                     format(device.name)) as step:
        try:
            device.connect(learn_hostname=True)
        except Exception as e:
            log.error(banner("*** Terminating Genie Clean ***"))
            section.failed("Could not reconnect to device {} after reload:\n{}".\
                           format(device.name, str(e)), goto=['exit'])
        else:
            log.info("Reconnected to the device {} sucessfully".\
                     format(device.name))

    # Verify all modules are in stable state
    if check_modules:
        with steps.start("Verify modules on {} are in stable state after "
                         "reload".format(device.name)) as step:
            try:
                device.api.verify_module_status(timeout=module_timeout,
                                                interval=module_interval)
            except Exception as e:
                log.error(banner("*** Terminating Genie Clean ***"))
                section.failed("Modules on {} are not in stable state after "
                               "reload".format(device.name), goto=['exit'])
            else:
                section.passed("Modules on {} are in stable state after "
                               "reload".format(device.name))


#===============================================================================
#                       stage: apply_configuration
#===============================================================================

@clean_schema({
    Optional('configuration'): str,
    Optional('file'): str,
    Optional('config_timeout'): int,
    Optional('config_stable_time'): int,
    Optional('copy_vdc_all'): bool,
    Optional('max_time'): int,
    Optional('check_interval'): int,
})
@aetest.test
def apply_configuration(section, steps, device, configuration=None, file=None,
    config_timeout=60, config_stable_time=10, copy_vdc_all=False, max_time=300,
    check_interval=60):

    '''
    Apply configuration on the device, either by providing a file and/or
    straight configuration

    Clean yaml file schema:
    -----------------------
    devices:
      <device>:
        apply_configuration:
          configuration: <Configuration block to be applied, 'str'> (Optional)
          file: <Configuration file> (Optional)
          config_timeout: <Timeout in seconds, 'int'> (Optional)
          config_stable_time: <Time for configuration stability in seconds, 'int'> (Optional)
          copy_vdc_all: <To copy on all VDCs or not, 'bool'> (Optional)
          max_time: <Maximum time section will take for checks in seconds, 'int'> (Optional)
          check_interval: <Time interval, 'int'> (Optional)

    Example:
    --------
    devices:
      N95_1:
        apply_configuration:
          configuration: |
            interface ethernet2/1
              no shutdown
          file: bootflash:/ISSUCleanGolden.cfg
          config_timeout: 600
          config_stable_time: 10
          copy_vdc_all: True
          max_time: 300
          check_interval: 20

    Flow:
    -----
    before:
      None
    after:
      None
    '''

    log.info("Section steps:\n1- Copy/Apply configuration to/on the device"
             "\n2- Copy running-config to startup-config"
             "\n3- Sleep to stabilize configuration on the device")

    # User has provided raw output or configuration file to apply onto device
    with steps.start("Apply configuration to device {} after reload".\
                     format(device.name)) as step:
        try:
            _apply_configuration(device=device, configuration=configuration,
                                 file=file, timeout=config_timeout)
        except Exception as e:
            log.error(banner("*** Terminating Genie Clean ***"))
            section.failed("Error while applying configuration to device "
                            "{} after reload\n{}".format(device.name, str(e)),
                            goto=['exit'])
        else:
            step.passed("Successfully applied configuration to device {} "
                        "after reload".format(device.name))

    # Copy running-config to startup-config
    with steps.start("Copy running-config to startup-config on device {}".\
                     format(device.name)) as step:
        try:
            device.api.execute_copy_run_to_start(command_timeout=config_timeout,
                                                 max_time=max_time,
                                                 check_interval=check_interval,
                                                 copy_vdc_all=copy_vdc_all)
        except Exception as e:
            log.error(banner("*** Terminating Genie Clean ***"))
            section.failed("Failed to copy running-config to startup-config on "
                           "{}\n{}".format(device.name, str(e)), goto=['exit'])
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

@clean_schema({'images': list})
@aetest.test
def verify_running_image(section, steps, device, images):

    '''
    Clean yaml file schema:
    -----------------------
    devices:
      <device>:
        verify_running_image:
          images: <Images reloaded on the device, 'list'> (Mandatory)

    Example:
    --------
    devices:
      N95_1:
        verify_running_image:
          images:
          - test_image.gbin

    Flow:
    -----
    before:
      reload (Mandatory, Reload device first then verify it)
    after:
      None
    '''

    log.info("Section steps:\n1- Verify the running image on the device")

    # Verify running image on the device
    with steps.start("Verify running image on device {}".\
                     format(device.name)) as step:
        try:
            device.api.verify_current_image(images=images)
        except Exception as e:
            log.error(banner("*** Terminating Genie Clean ***"))
            section.failed("Unable to verify running image on device {}\n{}".\
                           format(device.name, str(e)), goto=['exit'])
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
def backup_file_on_device(section, steps, device, copy_dir, copy_file,
    overwrite=True, timeout=300):

    '''
    Clean yaml file schema:
    -----------------------
    devices:
      <device>:
        backup_file_on_device:
          copy_dir ('str'): Directory containing file to be backed up (Mandatory)
          copy_file ('str'): File to be backed up (Mandatory)
          overwrite ('bool'): Overwrite the file if exists. Default value is True (Optional)
          timeout ('int'): Copy timeout in second. Default value is 300 (Optional)

    Example:
    --------
    devices:
      PE1:
        backup_file_on_device:
          copy_dir: bootflash:
          copy_file: ISSUCleanGolden.cfg

    Flow:
    -----
    before:
      None
    after:
      write_erase (Optional, Backup configuration file then perform write erase)
    '''

    log.info("Section steps:\n1- Backup file on the device")

    with steps.start("Backup file '{}/{}' on the device {}".\
                     format(copy_dir, copy_file, device.name)) as step:

        # Copy golden config to a backup file name, so that it can be
        # restored later (write erase destroys golden config on some
        # platforms).
        dest_file ="backup_{}".format(copy_file)

        # check space
        file_size = device.api.get_file_size(file='{}/{}'.format(copy_dir, copy_file))
        avail_space = device.api.get_available_space(directory=copy_dir)

        if file_size is None or avail_space is None:
            log.error(banner("*** Terminating Genie Clean ***"))
            section.failed("Failed to get '{}' file size or available space on {}".format(
                                copy_file, device.name), goto=['exit'])

        if avail_space <= file_size:
            log.error(banner("*** Terminating Genie Clean ***"))
            section.failed("Do not have enough space to copy file. "
                           "Required '{}' bytes, Available '{}' bytes".format(
                               file_size, avail_space), goto=['exit'])
        else:
            log.info("Required '{}' bytes, Available '{}' bytes".format(
                      file_size, avail_space))

        owt = Statement(pattern=r'.*over\s*write.*',
                        action='sendline({})'.format('y' if overwrite else 'n'),
                        loop_continue=True,
                        continue_timer=False)
        # Copy file
        try:
            device.copy(source=copy_dir, source_file=copy_file,
                        dest=copy_dir, dest_file=dest_file,
                        reply=Dialog([owt]), timeout=timeout)
        except Exception as e:
            log.error(str(e))
            log.error(banner("*** Terminating Genie Clean ***"))
            section.failed("Unable to backup '{}/{}'' on device {}".format(
                           copy_dir, copy_file, device.name), goto=['exit'])
        else:
            section.passed("Successfully backed up '{}/{}' on device {}".\
                           format(copy_dir, copy_file, device.name))


#===============================================================================
#                       stage: delete_backup_from_device
#===============================================================================

@clean_schema({
    'delete_dir': str,
    'delete_file': str,
    Optional('restore_from_backup'): bool,
    Optional('overwrite'): bool,
    Optional('timeout'): int,
})
@aetest.test
def delete_backup_from_device(section, steps, device, delete_dir, delete_file,
    restore_from_backup=False, overwrite=True, timeout=300):

    '''
    Clean yaml file schema:
    -----------------------
    devices:
      <device>:
        delete_backup_from_device:
          delete_dir ('str'): Directory containing file to be deleted (Mandatory)
          delete_file ('str'): File to be deleted up (Mandatory)
          restore_from_backup ('bool'): Restore the file from backup file. 
                                        Default value is False (Optional)
          overwrite ('bool'): Overwrite the file if exists. Default value is True (Optional)
          timeout ('int'): Copy/Execute timeout in second. Default value is 300 (Optional)

    Example:
    --------
    devices:
      PE1:
        delete_backup_from_device:
          delete_dir: 'bootflash:'
          delete_file: ISSUCleanGolden.cfg_backup

    Flow:
    -----
    before:
      write_erase (Optional, Perform write erase then delete the backed up file)
    after:
      None
    '''

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

            owt = Statement(pattern=r'.*over\s*write.*',
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
                log.error(banner("*** Terminating Genie Clean ***"))
                section.failed("Unable to restore '{}/{}'' on device {}".format(
                               delete_dir, delete_file, device.name),
                               goto=['exit'])

        device.execute.error_pattern.extend(['.*%Error.*', '.*No such file.*'])
        try:
            # Delete the golden backup file
            device.execute('delete {}{}'.format(delete_dir, delete_file),
                            reply=Dialog([delete_backup]))
        except Exception as e:
            log.error(e)
            log.error(banner("*** Terminating Genie Clean ***"))
            section.failed("Unable to delete '{}/{} from device {}".format(
                           delete_dir, delete_file, device.name), goto=['exit'])
        else:
            step.passed("Successfully deleted '{}/{}' from device {}".\
                        format(delete_dir, delete_file, device.name))


#===============================================================================
#                       stage: delete_files_from_server
#===============================================================================

@clean_schema({
    Optional('server'): str,
    Optional('files'): list,
    Optional('protocol'): str,
})
@aetest.test
def delete_files_from_server(section, steps, device, server=None, files=None,
    protocol='sftp'):
    """ delete images from server
        Clean yaml file schema:
    -----------------------
        devices:
            <device>:
                delete_files_from_server:
                  server ('str'): <Hostname or address of the server> (optional)
                  files ('list'): <list of images to delete> (Optional)
                  protocol ('str'): <protocol used for deletion, Default value is sftp> (Optional)

    Example:
    --------
        devices:
            N95_1:
                delete_files_from_server:
                    server: 1.1.1.1
                    files:
                    - /home/cisco/kickstart.bin
                    protocol: sftp

    Flow:
    -----
        before:
            None
        after:
            copy_to_device (optional, delete the image from server to save space after copy is done)
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
                section.skipped("No file has been provided to delete in the clean yaml file")

        if not server:
            log.info(
                "No server has been provided in the clean yaml, will use the same server "
                "from 'copy_to_linux' stage.")
            if 'copy_to_linux' in section.history:
                server = getattr(section.history['copy_to_linux'], 'parameters').\
                                 get('destination', {}).get('hostname')

        if not server:
            log.error(banner("*** Terminating Genie Clean ***"))
            section.failed("No server has been provided in the clean yaml file")

        for file in files:
            with step.start('Deleting {f}'.format(f=file)) as substep:
                try:
                    device.api.delete_file_on_server(testbed=device.testbed, path=file,
                                                     server=server, protocol=protocol, fu_session=fu)
                except Exception as e:
                    substep.passx('Failed to delete image "{}" due '
                               'to :{}'.format(file, str(e)))

