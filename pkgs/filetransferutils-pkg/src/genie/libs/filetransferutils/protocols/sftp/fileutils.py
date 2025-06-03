""" Implementation for sftp File Utilities. """

__copyright__ = "# Copyright (c) 2018 by cisco Systems, Inc. " \
    "All rights reserved."

__author__ = "Myles Dear <pyats-support@cisco.com>"

__all__ = ['copyfile', 'dir', 'stat', 'chmod', 'renamefile', 'deletefile' ]

import os
import time
import logging

from urllib.parse import urlsplit, urlunsplit

from genie.libs.filetransferutils.exceptions import TimeLimitExceededOnFileTransfer
from genie.libs.filetransferutils.fileutils import FileUtils as FileUtilsLinuxBase

try:
    from paramiko import (SSHClient, AutoAddPolicy, SSHException,
        AuthenticationException)

    paramiko_installed = True
except ImportError:
    paramiko_installed = False


logger = logging.getLogger(__name__)


UNSUPPORTED_PROTOCOL_MSG = ("The fileutils module {} "
"can only support protocol {} when the following commands "
"are executed : \npip install paramiko")

class FileUtils(FileUtilsLinuxBase):
    """ FileUtils sftp implementation.
    """
    SCHEME = "sftp"
    SSH_DEFAULT_PORT = 22


    # To conserve CPU, the progress callback only does something when it
    # is called this many times.
    PROGRESS_IGNORE_COUNT = 1000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ssh = None
        self.sftp = None


    def get_sessions(self, server_name, port, timeout_seconds):
        if self.ssh == None or self.sftp == None:
            # Get auth details
            username, password = self.get_auth(server_name)

            if not self.ssh:
                ssh = SSHClient()
                self.ssh = ssh
                ssh.load_system_host_keys()

                # Ensure first-time connection goes through, even if
                # the server isn't found in local system keys.
                ssh.set_missing_host_key_policy(AutoAddPolicy())

                # Paramiko can't seem to switch from pubkey to
                # password auth when connecting to IOS or ASA (and other?)
                # network devices.
                # https://github.com/paramiko/paramiko/issues/23
                # describes the issue, a PR is pending.
                #
                # A workaround is to pass look_for_keys=False to ssh.connect,
                # but as this disables pubkey auth, we're only doing this
                # if the first connect fails with an Auth exception.
                look_for_keys = True
                while True:
                    try:
                        ssh.connect(
                            hostname=server_name,
                            port=port,
                            username=username,
                            password=password,
                            timeout=timeout_seconds,
                            look_for_keys=look_for_keys)

                    except AuthenticationException as e:
                        # before giving up, trying again without
                        # attempting to use pubkey auth
                        if look_for_keys is True:
                            look_for_keys = False
                            continue
                        else:
                            raise e
                    else:
                        break

            if not self.sftp:
                self.sftp = self.ssh.open_sftp()

        return self.ssh, self.sftp


    def close(self):
        """ Called by remove_child and on failed operation. """
        logging.debug("sftp : Closing all connections ...")
        if self.sftp:
            self.sftp.close()
        self.sftp = None

        if self.ssh:
            self.ssh.close()
        self.ssh = None


    def copyfile(self, source, destination,
            timeout_seconds, *args, upload, **kwargs):
        """ Copy a single file.

        Copy a single file either from local to remote, or remote to local.
        Remote to remote transfers are not supported.  Users are expected
        to make two calls to this API to do this.

        Raises
        ------
            Exception : When a remote to remote transfer is requested.
        """
        if paramiko_installed:

            quiet = kwargs.get('quiet', False)
            def progress(sent, size):
                """ Print progress as file transfer proceeds. """
                nonlocal start_time
                nonlocal timeout_seconds
                nonlocal progress_skipcount
                nonlocal quiet

                if quiet:
                    return
                progress_skipcount += 1
                if (progress_skipcount > self.PROGRESS_IGNORE_COUNT) or \
                        (size == sent):
                    progress_skipcount = 0

                    elapsed_time = time.time() - start_time
                    if elapsed_time > timeout_seconds:
                        raise TimeLimitExceededOnFileTransfer()

                    logger.info("progress: %.2f%%   \r" % (
                        float(sent)/float(size)*100) )

            progress_skipcount = 0
            if upload:
                # Upload file from local file system to server

                # Ignore server and port as this is a local file url
                _, _, from_path = \
                    self.validate_and_parse_url(source, 'copyfile')

                to_server_name, to_parsed_port, to_path = \
                    self.validate_and_parse_url(destination, 'copyfile')

                server_name = to_server_name
                port = to_parsed_port if to_parsed_port \
                    else self.SSH_DEFAULT_PORT

            else:
                # Download file from server to local file system
                from_server_name, from_parsed_port, from_path = \
                    self.validate_and_parse_url(source, 'copyfile')

                # Ignore server and port as this is a local file url
                _, _, to_path = \
                    self.validate_and_parse_url(destination, 'copyfile')

                server_name = from_server_name
                port = from_parsed_port if from_parsed_port \
                    else self.SSH_DEFAULT_PORT

            # Ensure connect timeout is set to a fraction of the copy
            # timeout, this ratio is hardcoded at the parent level.
            connect_timeout = int(
                timeout_seconds * self.DEFAULT_TIMEOUT_SECONDS \
                / self.DEFAULT_COPY_TIMEOUT_SECONDS)

            ssh, sftp = self.get_sessions(
                server_name = server_name,
                port = port,
                timeout_seconds = connect_timeout)

            start_time = time.time()
            if upload:
                result = sftp.put(
                    localpath = from_path,
                    remotepath = to_path,
                    callback = progress)
            else:
                result = sftp.get(
                    remotepath = from_path,
                    localpath = to_path,
                    callback=progress)

        else:
            raise ImportError(UNSUPPORTED_PROTOCOL_MSG.\
                format(self.__module__, self.SCHEME))


    def dir(self, target, timeout_seconds, *args, **kwargs):
        """ Retrieve filenames contained in a directory.

        Do not recurse into subdirectories, only list files at the top level
        of the given directory.

        Parameters
        ----------
            target : `str`
                The URL of the directory whose files are to be retrieved.

            timeout_seconds : `int`
                The number of seconds to wait before aborting the operation.

        Returns
        -------
            `list` : List of filename URLs.  Directory names are ignored.
        """
        if paramiko_installed:

            server_name, parsed_port, path = self.validate_and_parse_url(
                target, 'dir')
            port = parsed_port if parsed_port else self.SSH_DEFAULT_PORT

            ssh, sftp = self.get_sessions(
                server_name = server_name,
                port = port,
                timeout_seconds = timeout_seconds)

            # Get file list
            files = sftp.listdir(path)

            split_url = urlsplit(target)
            result = [urlunsplit(
                (split_url[0], split_url[1],
                os.path.join(split_url.path, file),
                split_url[3], split_url[4], )) \
                for file in files]

            return result


        else:
            raise ImportError(UNSUPPORTED_PROTOCOL_MSG.\
                format(self.__module__, self.SCHEME))


    def stat(self, target, timeout_seconds, *args, **kwargs):
        """ Retrieve file details such as length and permissions.

        Parameters
        ----------
            target : `str`
                The URL of the file whose details are to be retrieved.

            timeout_seconds : `int`
                The number of seconds to wait before aborting the operation.

        Returns
        -------
            `os.stat_result` : Filename details including size.

        Raises
        ------
            Exception : timeout exceeded

            Exception : File was not found
        """
        if paramiko_installed:

            server_name, parsed_port, path = self.validate_and_parse_url(
                target, 'stat')
            port = parsed_port if parsed_port else self.SSH_DEFAULT_PORT

            ssh, sftp = self.get_sessions(
                server_name = server_name,
                port = port,
                timeout_seconds = timeout_seconds)

            # Get file details
            result = sftp.stat(path)

            return result

        else:
            raise ImportError(UNSUPPORTED_PROTOCOL_MSG.\
                format(self.__module__, self.SCHEME))


    def chmod(self, target, mode, timeout_seconds, *args, **kwargs):
        """ Change file permissions

        Parameters
        ----------
            target : `str`
                The URL of the file whose permissions are to be changed.

            mode : `int`
                Same format as os.chmod

            timeout_seconds : `int`
                Maximum allowed amount of time for the operation.

        Returns
        -------
            `None` if operation succeeded.

        """
        if paramiko_installed:
            server_name, parsed_port, path = self.validate_and_parse_url(
                target, 'chmod')
            port = parsed_port if parsed_port else self.SSH_DEFAULT_PORT

            ssh, sftp = self.get_sessions(
                server_name = server_name,
                port = port,
                timeout_seconds = timeout_seconds)

            # Change file permissions
            result = sftp.chmod(
                path = path,
                mode = mode)

        else:
            raise ImportError(UNSUPPORTED_PROTOCOL_MSG.\
                format(self.__module__, self.SCHEME))


    def deletefile(self, target, timeout_seconds, *args, **kwargs):
        """ Delete a file

        Parameters
        ----------
            target : `str`
                The URL of the file to be deleted.

            timeout_seconds : `int`
                Maximum allowed amount of time for the operation.

        """
        if paramiko_installed:
            server_name, parsed_port, path = self.validate_and_parse_url(
                target, 'deletefile')
            port = parsed_port if parsed_port else self.SSH_DEFAULT_PORT

            ssh, sftp = self.get_sessions(
                server_name = server_name,
                port = port,
                timeout_seconds = timeout_seconds)

            # Delete file
            result = sftp.remove(path)

        else:
            raise ImportError(UNSUPPORTED_PROTOCOL_MSG.\
                format(self.__module__, self.SCHEME))


    def renamefile(self, source, destination,
            timeout_seconds, *args, **kwargs):
        """ Rename a file

        Parameters
        ----------
            source : `str`
                The URL of the file to be renamed.

            destination : `str`
                The URL of the new file name.

            timeout_seconds : `int`
                Maximum allowed amount of time for the operation.

        """
        if paramiko_installed:


            from_server_name, from_parsed_port, from_path = \
                self.validate_and_parse_url(source, 'renamefile')

            from_port = from_parsed_port if from_parsed_port \
                else self.SSH_DEFAULT_PORT

            to_server_name, to_parsed_port, to_path = \
                self.validate_and_parse_url(destination, 'renamefile')

            to_port = to_parsed_port if to_parsed_port \
                else self.SSH_DEFAULT_PORT

            server_name = from_server_name
            port = from_port

            ssh, sftp = self.get_sessions(
                server_name = server_name,
                port = port,
                timeout_seconds = timeout_seconds)

            # Rename file
            result = sftp.rename(
                oldpath = from_path,
                newpath = to_path)

        else:
            raise ImportError(UNSUPPORTED_PROTOCOL_MSG.\
                format(self.__module__, self.SCHEME))

    def getspace(self, target, timeout_seconds, *args, **kwargs):
        """
        get the available disk space from the file server, in bytes.

        Parameters
        ----------
        target : `str`
                The URL of the directory to check available space.

        timeout_seconds : `int`
            Maximum allowed amount of time for the operation.
        """
        if paramiko_installed:
            server_name, parsed_port, path = self.validate_and_parse_url(
                target, 'getspace')
            port = parsed_port if parsed_port else self.SSH_DEFAULT_PORT

            ssh, _ = self.get_sessions(
                server_name=server_name,
                port=port,
                timeout_seconds=timeout_seconds)



        else:
            raise ImportError(UNSUPPORTED_PROTOCOL_MSG.\
                format(self.__module__, self.SCHEME))

        result = self._getspace(path)

        if not result:
            # nothing matches the regex in df output
            raise Exception(
                "Cannot find available space from the output of df command on "
                "server '{}' at location '{}'".format(
                    server_name, target))

        else:
            return result