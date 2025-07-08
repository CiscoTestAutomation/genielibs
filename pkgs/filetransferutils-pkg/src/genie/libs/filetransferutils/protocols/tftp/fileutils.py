""" Implementationfor Curl-based tftp File Utilities. """

__copyright__ = "# Copyright (c) 2018 by cisco Systems, Inc. " \
    "All rights reserved."

__author__ = "Myles Dear <pyats-support@cisco.com>"

__all__ = ['copyfile', 'dir', 'stat', 'chmod', 'renamefile', 'deletefile' ]

import logging

from urllib.parse import urlunsplit

from genie.libs.filetransferutils.fileutils import FileUtils as FileUtilsLinuxBase

logger = logging.getLogger(__name__)


class FileUtils(FileUtilsLinuxBase):
    """ FileUtils Curl TFTP implementation.
    """

    TFTP_DEFAULT_PORT = 69

    SCHEME = "tftp"

    CURL_UPLOAD_PATTERN = \
        "curl --upload-file {file_to_upload} {remote_file_url}"

    CURL_DOWNLOAD_PATTERN = \
        "curl --output {file_to_download} {remote_file_url}"

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
        if upload:
            # Upload file from local file system to server

            # Ignore server and port as this is a local file url
            _, _, from_path = \
                self.validate_and_parse_url(source, 'copyfile')

            to_server_name, to_parsed_port, to_path = \
                self.validate_and_parse_url(destination, 'copyfile')

            server_name = to_server_name
            port = to_parsed_port if to_parsed_port else self.TFTP_DEFAULT_PORT

        else:
            # Download file from server to local file system
            from_server_name, from_parsed_port, from_path = \
                self.validate_and_parse_url(source, 'copyfile')

            # Ignore server and port as this is a local file url
            _, _, to_path = \
                self.validate_and_parse_url(destination, 'copyfile')

            server_name = from_server_name
            port = from_parsed_port if from_parsed_port \
                else self.TFTP_DEFAULT_PORT

        if upload:
            logger.debug(
                "Copying local file {} to remote location {} ...".\
                format(from_path, to_path))
            remote_file_url = urlunsplit((
               self.SCHEME,
               "{}:{}".format(server_name, port),
               to_path,
               "",
               "",
            ))
            command = self.CURL_UPLOAD_PATTERN.format(
                file_to_upload = from_path,
                remote_file_url = remote_file_url
            )
        else:
            logger.debug(
                "Copying remote file {} to local location {} ...".\
                format(from_path, to_path))
            remote_file_url = urlunsplit((
               self.SCHEME,
               "{}:{}".format(server_name, port),
               from_path,
               "",
               "",
            ))
            command = self.CURL_DOWNLOAD_PATTERN.format(
                remote_file_url = remote_file_url,
                file_to_download = to_path
            )

        self.execute_in_subprocess(
            command, timeout_seconds = timeout_seconds)


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

        raise NotImplementedError("The fileutils module {} "
            "does not implement stat.".format(self.__module__))

