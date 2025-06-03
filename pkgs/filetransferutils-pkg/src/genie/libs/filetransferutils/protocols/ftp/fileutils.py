""" File utils class for FTP on Linux servers.

NOTE : The author is expected to subclass all base class operations
not supported by this protocol and raise a NotImplementedError.
"""

import os
import re
import time
import stat as libstat
import datetime
import logging

from ftplib import FTP
from urllib.parse import urlsplit, urlunsplit
from pyats.datastructures import AttrDict

from genie.libs.filetransferutils.exceptions import TimeLimitExceededOnFileTransfer
from genie.libs.filetransferutils.fileutils import FileUtils as FileUtilsLinuxBase

logger = logging.getLogger(__name__)

# datetime is in the form : Mmm dd hh:mm
DATETIME_PAT_RECENT = "%b %d %H:%M %Y"
STAT_DIR_FORMAT_SCAN_PATTERN_RECENT = r"\s*(?P<mode>\S+)\s+(?P<num_links>\d+)\s+(?P<owner>\w+)(\s+(?P<group>\w+))?\s+(?P<size>\d+)\s+(?P<month>[A-Za-z]{3})\s+(?P<day>\d+)\s+(?P<hour>\d+):(?P<minute>\d+)\s*(?P<filename>\S+)\s*$"

# datetime is in the form : Mmm dd yyyy
DATETIME_PAT_NOT_RECENT = "%b %d %Y"
STAT_DIR_FORMAT_SCAN_PATTERN_NOT_RECENT = r"\s*(?P<mode>\S+)\s+(?P<num_links>\d+)\s+(?P<owner>\w+)\s+(?P<group>\w+)\s+(?P<size>\d+)\s+(?P<month>[A-Za-z]{3})\s+(?P<day>\d+)\s+(?P<year>\d{4})\s*(?P<filename>\S+)\s*$"


def filemode_to_mode(filemode):
    """ Convert a filemode string to an os.stat.st_mode style number.

    Example
    -------
    >>> import stat
    >>> my_filemode = "-rw-r--r--"
    >>> stat.filemode(filemode_to_mode(my_filemode))
    -rw-r--r--
    """
    mode = 0
    for idx in range(len(filemode)):
        tbl = libstat._filemode_table[idx]
        mode_char = filemode[idx]
        for bit, char in tbl:
            if char == mode_char:
                mode |= bit
                break
    return mode


class FileUtils(FileUtilsLinuxBase):

    # To conserve CPU, the progress callback only does something when it
    # is called this many times.
    PROGRESS_IGNORE_COUNT = 30
    FROM_FTP = "Hello From FTP"

    def copyfile(self, source, destination,
            timeout_seconds, *args, upload, strip_leading_slash=True,
            **kwargs):
        """ Copy a single file.

        Copy a single file either from local to remote, or remote to local.
        Remote to remote transfers are not supported.  Users are expected
        to make two calls to this API to do this.

        Parameters
        ----------
            timeout_seconds : `int`
                The number of seconds to wait before aborting the operation.

            upload : `bool`
                If `True`, copying from local to remote.
                If `False`, copying from remote to local.

            strip_leading_slash : `bool`
                If `True`, strip any leading slash from the remote path.
                If `False`, do not strip leading slash from the remote path.

        Raises
        ------
            Exception : When a remote to remote transfer is requested.
        """

        def check_for_timeout():
            nonlocal start_time
            nonlocal timeout_seconds
            nonlocal progress_skipcount

            progress_skipcount += 1
            if (progress_skipcount > self.PROGRESS_IGNORE_COUNT):
                progress_skipcount = 0

                elapsed_time = time.time() - start_time
                if elapsed_time > timeout_seconds:
                    raise TimeLimitExceededOnFileTransfer()

        def upload_cb(data):
            """ Callback invoked during file upload. """
            check_for_timeout()

        def download_cb(data):
            """ Callback invoked during file download. """
            nonlocal file_to_transfer
            check_for_timeout()
            file_to_transfer.write(data)

        progress_skipcount = 0

        if upload:
            # Upload file from local file system to server

            # Ignore server and port as this is a local file url
            _, _, from_path = \
                self.validate_and_parse_url(source, 'copyfile')

            to_server_name, to_parsed_port, to_path = \
                self.validate_and_parse_url(destination, 'copyfile')

            server_name = to_server_name
            port = to_parsed_port if to_parsed_port else 0
            if strip_leading_slash and to_path and to_path[0] == '/':
                to_path = to_path[1:]
        else:
            # Download file from server to local file system
            from_server_name, from_parsed_port, from_path = \
                self.validate_and_parse_url(source, 'copyfile')

            # Ignore server and port as this is a local file url
            _, _, to_path = \
                self.validate_and_parse_url(destination, 'copyfile')

            server_name = from_server_name
            port = from_parsed_port if from_parsed_port else 0
            if strip_leading_slash and from_path and from_path[0] == '/':
                from_path = from_path[1:]


        # Get auth details
        username, password = self.get_auth(server_name)

        file_to_transfer = None

        with FTP() as ftp_sess:
            logger.debug(
                "Connecting to ftp host {} port {} with timeout {} ...".\
                format(server_name, port, timeout_seconds))
            ftp_sess.connect(
                host=server_name, port=port, timeout=timeout_seconds)
            ftp_sess.login(user=username, passwd=password)

            start_time = time.time()
            if upload:
                logger.debug(
                    "Copying local file {} to remote location {} ...".\
                    format(from_path, to_path))
                with open (from_path, 'rb') as fil:
                    file_to_transfer = fil
                    ftp_sess.storbinary(
                        cmd = 'STOR {}'.format(to_path),
                        fp =  file_to_transfer,
                        callback = upload_cb)
            else:
                logger.debug(
                    "Copying remote file {} to local location {} ...".\
                    format(from_path, to_path))
                with open (to_path, 'wb') as fil:
                    file_to_transfer = fil
                    ftp_sess.retrbinary(
                        cmd = 'RETR {}'.format(from_path),
                        callback=download_cb)


    def _normalize_filename(self, filename, parent_path):
        """ Normalize a remote filename/path to work across different servers.

        Construct path to file whether or not the filename already has
        parent directory elements included.

        Example
        -------
            self._normalize_filename(
                filename='extra/paths/myfile.txt',
                parent_path='/my/parent/path')
            '/my/parent/path/myfile.txt'

            self._normalize_filename(
                filename='myfile.txt',
                parent_path='/my/parent/path')
            '/my/parent/path/myfile.txt'
        """
        normalized_filename = filename
        filename = os.path.basename(filename)
        if filename:
            normalized_filename = os.path.join('/', parent_path, filename)
        return normalized_filename


    def dir(self, target,
            timeout_seconds, *args, strip_leading_slash=True, **kwargs):
        """ Retrieve filenames contained in a directory.

        Do not recurse into subdirectories, only list files at the top level
        of the given directory.

        Parameters
        ----------
            target : `str`
                The URL of the directory whose files are to be retrieved.

            timeout_seconds : `int`
                The number of seconds to wait before aborting the operation.

            strip_leading_slash : `bool`
                If `True`, strip any leading slash from the remote path.
                If `False`, do not strip leading slash from the remote path.

        Returns
        -------
            `list` : List of filename URLs.  Directory names are ignored.
        """

        server_name, parsed_port, path = self.validate_and_parse_url(
            target, 'dir')
        port = parsed_port if parsed_port else 0
        if strip_leading_slash and path and path[0] == '/':
            path = path[1:]

        # Get auth details
        username, password = self.get_auth(server_name)

        # Get file list
        files = []
        # NOTE : Not all FTP servers may implement the MLSD command
        # (RFC-3659).  Take a directory listing via the NLST command
        # to ensure wider compatibility.
        with FTP() as ftp_sess:
            ftp_sess.connect(
                host=server_name, port=port, timeout=timeout_seconds)
            ftp_sess.login(user=username, passwd=password)
            files = ftp_sess.nlst(path)


        split_url = urlsplit(target)

        return [urlunsplit(
            (split_url[0], split_url[1],
            self._normalize_filename(filename=file, parent_path=path),
            split_url[3], split_url[4], )) \
            for file in files]


    def stat(self, target, timeout_seconds, *args, strip_leading_slash=True,
            **kwargs):
        """ Retrieve file details such as length and permissions.

        Parameters
        ----------
            target : `str`
                The URL of the file whose details are to be retrieved.

            timeout_seconds : `int`
                The number of seconds to wait before aborting the operation.

            strip_leading_slash : `bool`
                If `True`, strip any leading slash from the remote path.
                If `False`, do not strip leading slash from the remote path.

        Returns
        -------
            `os.stat_result` : Filename details including size.

        Raises
        ------
            Exception : timeout exceeded

            Exception : File was not found
        """
        dir_output = []
        def dir_output_callback(data):
            dir_output.append(data)

        server_name, parsed_port, path = self.validate_and_parse_url(
            target, 'stat')
        port = parsed_port if parsed_port else 0
        if strip_leading_slash and path and path[0] == '/':
            path = path[1:]

        # Get auth details
        username, password = self.get_auth(server_name)

        # Get file details
        # NOTE : Not all FTP servers may implement the MLSD command
        # (RFC-3659).  Take a directory listing via the NLST command
        # to ensure wider compatibility.
        with FTP() as ftp_sess:
            ftp_sess.connect(
                host=server_name, port=port, timeout=timeout_seconds)
            ftp_sess.login(user=username, passwd=password)
            ftp_sess.dir(path, dir_output_callback)

        if len(dir_output) > 1:
            raise Exception("More than one result was found, did you request "
                "a stat of a directory ?")

        result = None
        # Normalize the data into as many fields of os.stat_result as possible.
        if dir_output:
            logger.debug(dir_output)
            recent = False
            logger.debug('Checking for files matching pattern %s' % STAT_DIR_FORMAT_SCAN_PATTERN_RECENT)
            stat_match = re.match(
                STAT_DIR_FORMAT_SCAN_PATTERN_RECENT, dir_output[0])
            if stat_match:
                recent = True
            else:
                logger.debug('Checking for files matching pattern %s' % STAT_DIR_FORMAT_SCAN_PATTERN_NOT_RECENT)
                stat_match = re.match(
                    STAT_DIR_FORMAT_SCAN_PATTERN_NOT_RECENT, dir_output[0])
                if not stat_match:
                    raise Exception("File {} was not found on "
                        "remote server {}.".\
                        format(path, server_name))

            result = AttrDict()

            # Construct st_mode
            result.st_mode = filemode_to_mode(stat_match.group('mode'))

            # Construct st_nlink
            result.st_nlink = int(stat_match.group('num_links'))

            # Construct st_uid
            try:
                result.st_uid = int(stat_match.group('owner'))
            except ValueError:
                result.st_uid = stat_match.group('owner')

            # Construct st_gid
            try:
                result.st_gid = int(stat_match.group('group'))
            except ValueError:
                result.st_gid = stat_match.group('group')
            except:
                pass

            # Construct st_size
            result.st_size = int(stat_match.group('size'))

            # Construct st_mtime, assume ftp server is reporting time in
            # UTC, correct for local timezone.
            if recent:
                mod_time_str = "{month} {day} {hour}:{minute} {year}".format(
                    month = stat_match.group('month'),
                    day = stat_match.group('day'),
                    hour = stat_match.group('hour'),
                    minute = stat_match.group('minute'),
                    year = datetime.date.today().year)
                result.st_mtime = int(datetime.datetime.strptime(
                    mod_time_str, DATETIME_PAT_RECENT).timestamp()) \
                    - time.timezone
            else:
                mod_time_str = "{month} {day} {year}".format(
                    month = stat_match.group('month'),
                    day = stat_match.group('day'),
                    year = stat_match.group('year'))
                result.st_mtime = int(datetime.datetime.strptime(
                    mod_time_str, DATETIME_PAT_NOT_RECENT).timestamp()) \
                    - time.timezone
        else:
            raise Exception (
                "File {filename} not found on server {server_name}.".\
                format(filename=path, server_name=server_name))
        return result


    def chmod(self, target, mode, timeout_seconds, *args,
            strip_leading_slash=True, **kwargs):
        """ Change file permissions

        Parameters
        ----------
            target : `str`
                The URL of the file whose permissions are to be changed.

            mode : `int`
                Same format as os.chmod

            timeout_seconds : `int`
                Maximum allowed amount of time for the operation.

            strip_leading_slash : `bool`
                If `True`, strip any leading slash from the remote path.
                If `False`, do not strip leading slash from the remote path.

        Returns
        -------
            `None` if operation succeeded.

        """

        server_name, parsed_port, path = self.validate_and_parse_url(
            target, 'chmod')

        port = parsed_port if parsed_port else 0
        if strip_leading_slash and path and path[0] == '/':
            path = path[1:]

        # Get auth details
        username, password = self.get_auth(server_name)

        with FTP() as ftp_sess:
            ftp_sess.connect(
                host=server_name, port=port, timeout=timeout_seconds)
            ftp_sess.login(user=username, passwd=password)

            # Input is integer, FTP server requires it in octal.
            # Strip out the leading "0o".
            mode = oct(mode)[2:]
            ftp_sess.voidcmd("SITE CHMOD {mode} {filename}".\
                format(mode = mode, filename = path))


    def deletefile(self, target, timeout_seconds, *args,
            strip_leading_slash=True, **kwargs):
        """ Delete a file

        Parameters
        ----------
            target : `str`
                The URL of the file to be deleted.

            timeout_seconds : `int`
                Maximum allowed amount of time for the operation.

            strip_leading_slash : `bool`
                If `True`, strip any leading slash from the remote path.
                If `False`, do not strip leading slash from the remote path.

        """

        server_name, parsed_port, path = self.validate_and_parse_url(
            target, 'deletefile')
        port = parsed_port if parsed_port else 0
        if strip_leading_slash and path and path[0] == '/':
            path = path[1:]

        # Get auth details
        username, password = self.get_auth(server_name)

        with FTP() as ftp_sess:
            ftp_sess.connect(
                host=server_name, port=port, timeout=timeout_seconds)
            ftp_sess.login(user=username, passwd=password)

            # Input is integer, FTP server requires it in octal.
            # Strip out the leading "0o".
            ftp_sess.delete(filename = path)


    def renamefile(self, source, destination,
            timeout_seconds, *args, strip_leading_slash=True, **kwargs):
        """ Rename a file

        Parameters
        ----------
            source : `str`
                The URL of the file to be renamed.

            destination : `str`
                The URL of the new file name.

            timeout_seconds : `int`
                Maximum allowed amount of time for the operation.

            strip_leading_slash : `bool`
                If `True`, strip any leading slash from the remote path.
                If `False`, do not strip leading slash from the remote path.

        """

        from_server_name, from_parsed_port, from_path = \
            self.validate_and_parse_url(source, 'renamefile')

        from_port = from_parsed_port if from_parsed_port else 0
        if strip_leading_slash and from_path and from_path[0] == '/':
            from_path = from_path[1:]

        to_server_name, to_parsed_port, to_path = \
            self.validate_and_parse_url(destination, 'renamefile')

        to_port = to_parsed_port if to_parsed_port else 0
        if strip_leading_slash and to_path and to_path[0] == '/':
            to_path = to_path[1:]

        if from_server_name != to_server_name:
            raise Exception("fileutils module {} requires from/to files to be "
                "renamed to have the same server.".format(self.__module__))

        if from_port != to_port:
            raise Exception("fileutils module {} requires from/to files to be "
                "renamed to have the same port.".format(self.__module__))


        server_name = from_server_name
        port = from_port

        # Get auth details
        username, password = self.get_auth(server_name)

        with FTP() as ftp_sess:
            ftp_sess.connect(
                host=server_name, port=port, timeout=timeout_seconds)
            ftp_sess.login(user=username, passwd=password)
            ftp_sess.rename(fromname=from_path, toname=to_path)


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
        raise NotImplementedError("The fileutils module {} "
            "does not implement getspace.".format(self.__module__))