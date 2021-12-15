'''Common verify functions'''

# Python
import os
import re
from os import device_encoding
import time
import logging

# pyATS
from pyats.utils.fileutils import FileUtils

# Genie
from genie.utils.timeout import Timeout

# Unicon
from unicon.core.errors import StateMachineError

# Logger
log = logging.getLogger(__name__)


def verify_connectivity(device):

    log.info("Verifying device connectivity")
    try:
        device.execute("show clock")
    except Exception:
        # Nope!
        log.warning("Device is not connected")
        return False
    else:
        # All good!
        log.debug("Device is connected")
        return True


def verify_enough_server_disk_space(device,
                                    protocol,
                                    server=None,
                                    directory='.',
                                    required_space=None,
                                    timeout=300,
                                    fu_session=None):
    """Verify there are enough space on the server
        Args:
            device ('obj'): Device object
            protocol ('str'): Protocol used to check disk space, scp or sftp
            server ('str'): Server address or hostname. if not provided it will perform
                            operation on local file system (Optional)
            required_space ('int'): required total disk space (Optional)
            directory ('str'): directory to check file size (Optional)
            timeout('int'): timeout in seconds (Optional, default 300)
            fu_session ('obj'): existing FileUtils object to reuse (Optional)
        Returns:
            True if enough space, False otherwise
        """

    if fu_session:
        return _verify_enough_server_disk_space(device,
                                                protocol,
                                                server=server,
                                                directory=directory,
                                                required_space=required_space,
                                                timeout=timeout,
                                                fu_session=fu_session)
    with FileUtils(testbed=device.testbed) as fu:
        return _verify_enough_server_disk_space(device,
                                                protocol,
                                                server=server,
                                                directory=directory,
                                                required_space=required_space,
                                                timeout=timeout,
                                                fu_session=fu)


def _verify_enough_server_disk_space(device,
                                     protocol,
                                     fu_session,
                                     server=None,
                                     directory='.',
                                     required_space=None,
                                     timeout=300):
    """Verify there are enough space on the server
        Args:
            device ('obj'): Device object
            protocol ('str'): Protocol used to check disk space, scp or sftp
            server ('str'): Server address or hostname. if not provided it will perform
                            operation on local file system (Optional)
            required_space ('int'): required total disk space (Optional)
            directory ('str'): directory to check file size (Optional)
            timeout('int'): timeout in seconds (Optional, default 300)
            fu_session ('obj'): existing FileUtils object to reuse (Optional)
        Returns:
            True if enough space, False otherwise
        """
    if not server:
        url = directory
    else:
        url = '{p}://{s}/{d}'.format(p=protocol, s=server, d=directory)
        url = fu_session.validate_and_update_url(url)
    try:
        avail_space = fu_session.getspace(target=url, timeout_seconds=timeout)
    except NotImplementedError:
        raise NotImplementedError(
            'The protocol {} does not support checking disk space.'.format(
                protocol)) from None
    except Exception as e:
        raise Exception(
            "Failed to check disk space at location {} due to {}.".format(
                directory, str(e)))

    log.info("Space required: {} bytes, Space available : {} bytes".format(
        required_space if avail_space >= 0 else 'Unknown',
        avail_space if avail_space >= 0 else 'Unknown'))

    return avail_space > required_space


def verify_file_exists_on_server(device,
                                 protocol,
                                 file,
                                 server=None,
                                 size=None,
                                 timeout=300,
                                 fu_session=None,
                                 max_tries=1):
    """Verify there are enough space on the server
        Args:
            device ('obj'): Device object
            protocol ('str'): Protocol used to check file, ftp or sftp
            file ('int'): file path
            server ('str'): Server address or hostname. if not provided it will perform
                            operation on local file system (Optional)
            size ('int'): expected file size in bytes, if not provided will only check
                file existence with name (Optional)
            timeout('int'): timeout in seconds (Optional)
            fu_session ('obj'): existing FileUtils object to reuse (Optional)
            max_tries ('int;): max number of attempts (Optional)
        Returns:
            True if enough space, false otherwise
        """

    # global session
    if fu_session:
        return _verify_file_exists_on_server(device,
                                             protocol,
                                             file,
                                             server=server,
                                             size=size,
                                             timeout=timeout,
                                             fu_session=fu_session,
                                             max_tries=max_tries)
    # no global session, establish a local one
    with FileUtils(testbed=device.testbed) as fu:
        return _verify_file_exists_on_server(device,
                                             protocol,
                                             file,
                                             server=server,
                                             size=size,
                                             timeout=timeout,
                                             fu_session=fu,
                                             max_tries=max_tries)


def _verify_file_exists_on_server(device,
                                  protocol,
                                  file,
                                  server=None,
                                  size=None,
                                  timeout=300,
                                  fu_session=None,
                                  max_tries=1):
    """Verify there are enough space on the server
        Args:
            device ('obj'): Device object
            protocol ('str'): Protocol used to check file, ftp or sftp
            file ('int'): file path
            server ('str'): Server address or hostname. if not provided it will perform
                            operation on local file system (Optional)
            size ('int'): expected file size in bytes, if not provided will only check
                file existence with name (Optional)
            timeout('int'): timeout in seconds (Optional)
            fu_session ('obj'): existing FileUtils object to reuse (Optional)
            max_tries ('int'): max number of attempts (Optional)
        Returns:
            True if enough space, false otherwise
        """
    # file is local
    if server:
        url = '{p}://{s}/{f}'.format(p=protocol, s=server, f=file)
        url = fu_session.validate_and_update_url(url)
        try:
            fu_session.checkfile(target=url,
                                 max_tries=max_tries,
                                 timeout_seconds=timeout)
        except NotImplementedError:
            raise NotImplementedError(
                'The protocol {} does not support file listing, unable to verify file '
                'existence.'.format(protocol)) from None
        except Exception:
            log.info("File '{}' does not exist.".format(file))
            return False
        else:
            log.info("Found the file '{}'".format(file))

        if not size:
            return True

        # if exist then check if size are the same
        file_size = device.api.get_file_size_from_server(server=server,
                                                         path=file,
                                                         protocol=protocol,
                                                         timeout=timeout,
                                                         fu_session=fu_session)

    elif os.path.exists(file):
        log.info("Found the file '{}'".format(file))
        file_size = os.path.getsize(file)
    else:
        log.info("File '{}' does not exist.".format(file))
        return False

    log.info("Expected size: {} bytes, Actual size : {} bytes".format(
        size if size > -1 else 'Unknown',
        file_size if file_size > -1 else 'Unknown'))

    if size > -1 and file_size > -1:
        return size == file_size

    log.warning("File name '{}' exist but size is unknown.")
    return True


def verify_file_size_stable_on_server(device,
                                      protocol,
                                      file,
                                      server=None,
                                      max_tries=3,
                                      delay=2,
                                      timeout=300,
                                      fu_session=None):
    """Verify size stability of given file on the server
        Args:
            device ('obj'): Device object
            server ('str'): Server address or hostname. if not provided it will perform
                            operation on local file system (Optional)
            protocol ('str'): Protocol used to check file, ftp or sftp
            file ('int'): file path
            timeout ('int'): timeout in seconds
            fu_session ('obj'): existing FileUtils object to reuse
            max_tries ('int'): number of tries to check file stability, defaults 3
            delay ('int'): time delay between tries in seconds, defaults 2
        Returns:
            True if file size is stable, false otherwise
        """

    # global session
    if fu_session:
        return _verify_file_size_stable_on_server(device,
                                                  protocol,
                                                  file,
                                                  server=server,
                                                  max_tries=max_tries,
                                                  delay=delay,
                                                  timeout=timeout,
                                                  fu_session=fu_session)
    # no global session, establish a local one
    with FileUtils(testbed=device.testbed) as fu:
        return _verify_file_size_stable_on_server(device,
                                                  protocol,
                                                  file,
                                                  server=server,
                                                  max_tries=max_tries,
                                                  delay=delay,
                                                  timeout=timeout,
                                                  fu_session=fu)


def _verify_file_size_stable_on_server(device,
                                       protocol,
                                       file,
                                       server=None,
                                       max_tries=3,
                                       delay=2,
                                       timeout=300,
                                       fu_session=None):
    """Verify size stability of given file on the server
        Args:
            device ('obj'): Device object
            server ('str'): Server address or hostname. if not provided it will perform
                            operation on local file system (Optional)
            protocol ('str'): Protocol used to check file, ftp or sftp
            file ('int'): file path
            timeout('int'): timeout in seconds
            fu_session ('obj'): existing FileUtils object to reuse
            max_tries('int'): number of tries to check file stability, defaults 3
            delay ('int'): time delay between tries in seconds, defaults 2
        Returns:
            True if file size is stable, false otherwise
        """
    if not server:
        return _verify_local_file_size_stable(file,
                                              max_tries=max_tries,
                                              delay_seconds=delay)
    url = '{p}://{s}/{f}'.format(p=protocol, s=server, f=file)
    url = fu_session.validate_and_update_url(url)
    try:
        fu_session.checkfile(target=url,
                             timeout_seconds=timeout,
                             max_tries=max_tries,
                             delay_seconds=delay,
                             check_stability=True)
    except NotImplementedError:
        raise NotImplementedError(
            'The protocol {} does not support file listing, unable to verify file '
            'size stability.'.format(protocol)) from None
    except Exception:
        log.warning("The size of the given file is not stable")
        return False

    log.info("The size of the given file is stable")
    return True


def _verify_local_file_size_stable(file, max_tries=3, delay_seconds=2):
    """
    Args
        Verify if the file size is stable, not changing
        device ('obj'): Device Object
        file ('str'): file path to check the size
        max_tries('int'): number of tries to check file stability, defaults 3
        delay_seconds ('int'): time delay between tries in seconds, defaults 2
    Returns
        True if file size is stable, false otherwise
    """
    num_consecutive_equal_length_tries = 0
    result = None
    prev_result = None
    for _try in range(max_tries):
        try:
            result = os.path.getsize(file)
            if not result:
                log.warning(
                    "Failed to get file size for file :'{file}'".format(
                        file=file))
                return False
        except Exception as exc:
            log.warning("Failed to get file size for file '{file}'"
                        " due to: {exc}".format(file=file, exc=exc))
            result = None
            prev_result = None
        else:
            # Check if first time, prev_result will be none
            # if so, then just do a +1
            # If not empty verify current result with prev result and
            # make sure they are equal
            if prev_result and result == prev_result:
                num_consecutive_equal_length_tries += 1
            else:
                num_consecutive_equal_length_tries = 1
            prev_result = result

        time.sleep(delay_seconds)

    # Verify that the last two matches
    if num_consecutive_equal_length_tries < 2:
        log.warning("The length of file {} is not stable.".format(file))
        return False
    return True


def verify_current_image(device, images, delimiter_regex=None):
    '''Verify current images on the device
        Args:
            device (`obj`): Device object
            images (`list`): List of images expected on the device
        Returns:
            None
    '''

    if not delimiter_regex:
        delimiter_regex = ':|\/'

    # Get current running image
    running_images = device.api.get_running_image()

    # Check if images is None
    if running_images is None:
        raise Exception("Failed to get running images.")

    # Check type
    if not isinstance(running_images, list):
        running_images = [running_images]

    # Compare num images
    log.info("Comparing running image...")
    if len(images) != len(running_images):
        raise Exception("Retrieved running image(s) '{}' are not of the same "
                        "length as the image(s) to be verified '{}'".format(
                            running_images, images))

    # Split images on delimiters to compare them more reliably. 
    # Example, bootflash:/some/path/to/csr1000v-boot.16.09.01.SPA.pkg becomes 
    # ['bootflash', 'some', 'path', 'to', 'csr1000v-boot.16.09.01.SPA.pkg']
    split_images = \
        [[x for x in re.split(delimiter_regex, image) if x] 
            for image in images]

    split_running_images = \
        [[x for x in re.split(delimiter_regex, running_image) if x] 
            for running_image in running_images]

    # Compare the (directory, image) tuple sets of images and running images
    if split_images != split_running_images:
        raise Exception("Running images '{}' do not match list of the "
                        "expected images '{}'. \nNote: delimeters have been "
                        "excluded from this comparison based on this regex "
                        "patern: '{}'"
                        .format(running_images, images, delimiter_regex))
    log.info("Successfully loaded the following images on device '{}':".\
             format(device.name))
    for i in running_images:
        log.info(i)
    return


def verify_enough_disk_space(device,
                             required_size,
                             directory='',
                             dir_output=None):
    '''Verify there are enough space on the disk
        Args:
            device ('obj'): Device Object
            required_size ('int'): required file size
            directory ('str'): directory to check file size
            dir_output ('str'): Output of 'dir' command
                            if not provided, executes the cmd on device
    Returns:
        True if enough space, false otherwise
    '''

    available_space = device.api.get_available_space(directory=directory,
                                                     output=dir_output)
    if not available_space:
        available_space = -1

    log.info("Space required: {} bytes,\nSpace available : {} bytes".format(
        required_size if required_size > -1 else 'Unknown',
        available_space if available_space > -1 else 'Unknown'))

    return available_space > int(required_size)


def verify_device_connection_state(device,
                                   reconnect=False,
                                   reconnect_max_time=900,
                                   reconnect_interval=60):
    '''Verify device's Unicon machine state
        Args:
            device ('obj'): Device Object
            reconnect ('bool'): flag to reconnect in case state cannot be detected
            reconnect_max_time ('int'): maximum time to reconnect
                                        Default to 900 secs
            reconnect_interval ('int'): interval of sleep after state detection issue
                            if not provided, executes the cmd on device
    Returns:
        (`str` or None) : Return Unicon machine state
                          if could not detected, return None
    '''

    # check if state can be confirmed
    try:
        # get state machine state on device to check device reachability
        # need to get state to detect if device reloading or
        # any other condition which cannot respond
        if hasattr(device, 'is_ha') and device.is_ha:
            for con in device.subconnections:
                device.spawn.match = None
                con.device.state_machine.detect_state(device.spawn)
        else:
            device.spawn.match = None
            device.state_machine.detect_state(device.spawn)
    except StateMachineError as e:
        # reconnect = None means `reconnect` is defined
        # raise StateMachineError instead of reconnecting
        if reconnect:
            timeout = Timeout(max_time=reconnect_max_time,
                              interval=reconnect_interval)
            while timeout.iterate():
                log.info(
                    'could not detect machine state for {d}'.format(d=device))

                # save via info for current connection
                via = device.via
                log.info('disconnecting {d}'.format(d=device))
                # disconnect(destroy) device
                device.destroy()
                # reconnect to device
                log.info('reconnecting device {d}'.format(d=device))
                try:
                    if via:
                        device.connect(via=via)
                    else:
                        device.connect()
                except Exception as e:
                    log.info('could not login to {d}'.format(d=device))
                    timeout.sleep()
                else:
                    return device.state_machine.current_state

        # couldn't detect state even after reconnecting
        return None
    else:
        return device.state_machine.current_state


def verify_device_connection(device,
                             reconnect=False,
                             reconnect_max_time=900,
                             reconnect_interval=60):
    '''Verify device connectivity and reconnect if needed
        Args:
            device ('obj'): Device Object
            reconnect ('bool'): flag to reconnect in case device is not connected
            reconnect_max_time ('int'): maximum time to reconnect
                                        Default to 900 secs
            reconnect_interval ('int'): interval of sleep after detecting device is not connected
                            if not provided, executes the cmd on device
    Returns:
        (`bool`) : Return True(device is connected)/False(device is not connected)
    '''

    # check if device is connected
    if not device.connected and reconnect:
        timeout = Timeout(max_time=reconnect_max_time,
                          interval=reconnect_interval)
        while timeout.iterate():
            log.info('could not detect machine state for {d}'.format(d=device))

            # save via info for current connection
            via = device.via
            log.info('disconnecting {d}'.format(d=device))
            # disconnect(destroy) device
            device.destroy()
            # reconnect to device
            log.info('reconnecting device {d}'.format(d=device))
            try:
                if via:
                    device.connect(via=via)
                else:
                    device.connect()
            except Exception as e:
                log.info('could not login to {d}'.format(d=device))
                timeout.sleep()
            else:
                return device.connected

    # returning device.connected
    # device is connected or device couldn't be connected even after reconnect
    return device.connected
