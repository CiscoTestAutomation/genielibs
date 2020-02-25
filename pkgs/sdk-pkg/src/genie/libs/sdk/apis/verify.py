# python
import os
import time
import logging

# pyATS
from ats.log.utils import banner
from pyats.utils.fileutils import FileUtils

log = logging.getLogger()


def verify_connectivity(device):

    log.info(banner("Verifying device connectivity"))
    try:
        device.execute("show clock")
    except Exception:
        # Nope!
        return False
    else:
        # All good!
        return True


def verify_enough_server_disk_space(device, protocol, server=None, directory='.',
    required_space=None, timeout=300, fu_session=None):
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
        return _verify_enough_server_disk_space(device, protocol, server=server,
                                                directory=directory,
                                                required_space=required_space,
                                                timeout=timeout,
                                                fu_session=fu_session)
    else:
        with FileUtils(testbed=device.testbed) as fu:
            return _verify_enough_server_disk_space(device, protocol, server=server,
                                                    directory=directory,
                                                    required_space=required_space,
                                                    timeout=timeout,
                                                    fu_session=fu)


def _verify_enough_server_disk_space(device, protocol, fu_session, server=None,
    directory='.', required_space=None, timeout=300):
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
    try:
        avail_space = fu_session.getspace(target=url, timeout_seconds=timeout)
    except NotImplementedError:
        raise NotImplementedError(
            'The protocol {} does not support checking disk space.'.format(
                protocol)) from None
    except Exception as e:
        raise Exception(
            "Failed to check disk space at location {} due to {}.".format(directory,
                                                                          str(e)))

    log.info(
        "Space required: {} bytes, Space available : {} bytes".format(
            required_space if avail_space >= 0 else 'Unknown',
            avail_space if avail_space >= 0 else 'Unknown'))

    return avail_space > required_space


def verify_file_exists_on_server(device, protocol, file, server=None, size=None,
    timeout=300, fu_session=None, max_tries=1):
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
        return _verify_file_exists_on_server(device, protocol, file, server=server, size=size,
                                      timeout=timeout, fu_session=fu_session, max_tries=max_tries)
    # no global session, establish a local one
    else:
        with FileUtils(testbed=device.testbed) as fu:
            return _verify_file_exists_on_server(device, protocol, file, server=server, size=size,
                                          timeout=timeout, fu_session=fu, max_tries=max_tries)


def _verify_file_exists_on_server(device, protocol, file, server=None,size=None,
    timeout=300, fu_session=None, max_tries=1):
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
    if not server:
        if os.path.exists(file):
            log.info("Found the file '{}'".format(file))
            file_size = os.path.getsize(file)
        else:
            log.info("File '{}' does not exist.".format(file))
            return False

    else:
        url = '{p}://{s}/{f}'.format(p=protocol, s=server, f=file)

        try:
            fu_session.checkfile(target=url, max_tries=max_tries, timeout_seconds=timeout)
        except NotImplementedError:
            raise NotImplementedError(
                'The protocol {} does not support file listing, unable to verify file '
                'existence.'.format(
                    protocol)) from None
        except Exception:
            log.info("File '{}' does not exist.".format(file))
            return False
        else:
            log.info("Found the file '{}'".format(file))

        if not size:
            return True

        # if exist then check if size are the same
        file_size = device.api.get_file_size_from_server(server=server, path=file,
                                                         protocol=protocol,
                                                         timeout=timeout,
                                                         fu_session=fu_session)


    log.info(
        "Expected size: {} bytes, Actual size : {} bytes".format(
            size if size > -1 else 'Unknown',
            file_size if file_size > -1 else 'Unknown'))

    if size > -1 and file_size > -1:
        return size == file_size

    else:
        log.warning("File name '{}' exist but size is unknown.")
        return True


def verify_file_size_stable_on_server(device, protocol, file, server=None, max_tries=3,
    delay=2, timeout=300, fu_session=None):
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
        return _verify_file_size_stable_on_server(device, protocol, file, server=server,
                                                  max_tries=max_tries, delay=delay,
                                                  timeout=timeout, fu_session=fu_session)
    # no global session, establish a local one
    else:
        with FileUtils(testbed=device.testbed) as fu:
            return _verify_file_size_stable_on_server(device, protocol, file, server=server,
                                                      max_tries=max_tries, delay=delay,
                                                      timeout=timeout, fu_session=fu)


def _verify_file_size_stable_on_server(device, protocol, file, server=None, max_tries=3,
    delay=2, timeout=300, fu_session=None):
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
        return _verify_local_file_size_stable(file, max_tries=max_tries, delay_seconds=delay)
    url = '{p}://{s}/{f}'.format(p=protocol, s=server, f=file)
    try:
        fu_session.checkfile(target=url, timeout_seconds=timeout, max_tries=max_tries,
                             delay_seconds=delay, check_stability=True)
    except NotImplementedError:
        raise NotImplementedError(
            'The protocol {} does not support file listing, unable to verify file '
            'size stability.'.format(
                protocol)) from None
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
                log.warning("Failed to get file size for file :'{file}'".format(file=file))
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


def verify_current_image(device, images):
    '''Verify current images on the device
        Args:
            device (`obj`): Device object
            images (`list`): List of images expected on the device
        Returns:
            None
    '''

    # Get current running image
    running_images = device.api.get_running_image()

    # Check type
    if not isinstance(running_images, list):
        running_images = [running_images]

    # Compare num images
    log.info("Comparing running image...")
    if len(images) != len(running_images):
        raise Exception("Retrieved running image(s) '{}' are not of the same "
                        "length as the image(s) to be verified '{}'".format(
                        running_images, images))

    for runimage in running_images:
        if runimage not in images:
            raise Exception("Running image '{}' not found in the list of the "
                            "expected images '{}'".format(images, runimage))
        else:
            log.info("Image '{}' is loaded successfully onto device {}".\
                     format(runimage, device.name))

    log.info("All required images are loaded successfully")

    return


def verify_enough_disk_space(device, required_size, directory='', dir_output=None):
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
