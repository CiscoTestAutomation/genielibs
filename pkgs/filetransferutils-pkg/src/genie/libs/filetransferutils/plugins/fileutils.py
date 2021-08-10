""" File utils common base class """
# Logging
import logging

try:
    from pyats.utils.fileutils import FileUtils as server
    # Server FileUtils core implementation

    # filemode_to_mode
    from pyats.utils.fileutils.plugins.localhost.ftp.fileutils import \
        filemode_to_mode
except ImportError:
    try:
        from pyats.utils.fileutils import FileUtils as server
        # Server FileUtils core implementation

        # filemode_to_mode
        from pyats.utils.fileutils.plugins.localhost.ftp.fileutils import \
            filemode_to_mode
    except ImportError:
        # For apidoc building only
        from unittest.mock import Mock
        server = Mock
        filemode_to_mode = Mock()

# Parent inheritance
from .. import FileUtils as FileUtilsCommonDeviceBase

# Initialize the logger
logger = logging.getLogger(__name__)


class FileUtils(FileUtilsCommonDeviceBase):
    def copyfile(self, source, destination, timeout_seconds, cmd, used_server,
                 *args, interface=None, **kwargs):
        """ Copy a file to/from device

            Copy any file to/from a device to any location supported on the
            device and on the running-configuration.

            Parameters
            ----------
                source: `str`
                    Full path to the copy 'from' location
                destination: `str`
                    Full path to the copy 'to' location
                timeout_seconds: `str`
                    The number of seconds to wait before aborting the operation
                cmd: `str`
                    Command to be executed on the device
                used_server: `str`
                    Server address/name

            Returns
            -------
                `None`

            Raises
            ------
                Exception
                    When a device object is not present or device execution encountered
                    an unexpected behavior.

            Examples
            --------
                # FileUtils
                >>> from pyats.utils.fileutils import FileUtils

                # Instanciate a filetransferutils instance for NXOS device
                >>> fu_device = FileUtils.from_device(device)

                # copy file from device to server
                >>> fu_device.copyfile(
                ...     source='flash:/memleak.tcl',
                ...     destination='ftp://10.1.0.213//auto/tftp-ssr/memleak.tcl',
                ...     timeout_seconds='300', device=device)

                # copy file from server to device
                >>> fu_device.copyfile(
                ...     source='ftp://10.1.0.213//auto/tftp-ssr/memleak.tcl',
                ...     destination='flash:/new_file.tcl',
                ...     timeout_seconds='300', device=device)

                # copy file from server to device running configuration
                >>> fu_device.copyfile(
                ...     source='ftp://10.1.0.213//auto/tftp-ssr/memleak.tcl',
                ...     destination='running-config',
                ...     timeout_seconds='300', device=device)
        """

        with self.file_transfer_config(used_server, interface=interface, **kwargs):
            return self.send_cli_to_device(cli=cmd,
                                    timeout_seconds=timeout_seconds,
                                    used_server=used_server,
                                    **kwargs)



    def parsed_dir(self, target, timeout_seconds, dir_output, *args, **kwargs):
        """ Retrieve filenames contained in a directory.

            Do not recurse into subdirectories, only list files at the top level
            of the given directory.

            Parameters
            ----------
                target : `str`
                    The directory whose details are to be retrieved.

                timeout_seconds : `int`
                    The number of seconds to wait before aborting the operation.

                dir_output : `obj`
                    The OS corresponding `dir` parser object

            Returns
            -------
                `dict` : Dict of filename URLs and the corresponding info (ex:size)

            Raises
            ------
                AttributeError
                    device object not passed in the function call

                Exception
                    Parser encountered an issue

            Examples
            --------
                # FileUtils
                >>> from pyats.utils.fileutils import FileUtils

                # Instanciate a filetransferutils instance for NXOS device
                >>> fu_device = FileUtils.from_device(device)

                # list all files on the device directory 'flash:'
                >>> directory_output = fu_device.dir(target='flash:',
                ...     timeout_seconds=300, device=device)

                >>> directory_output['dir']['flash:/']['files']
                ...     (Pdb) directory_output['dir']['flash:/']['files']['boothelper.log']
                        {'index': '69699', 'permissions': '-rw-', 'size': '76',
                        'last_modified_date': 'Mar 20 2018 10:25:46 +00:00'}

        """

        # Extract device from the keyword arguments, if not passed raise an
        # AttributeError

        device = kwargs.get('device') or getattr(self, 'device', None)
        if not device:
            raise AttributeError("Device object is missing, can't proceed with"
                                 " execution")

        # Call the parser

        obj = dir_output(device=device)
        return obj.parse()

    def stat(self, target, timeout_seconds, dir_output, *args, **kwargs):
        """ Retrieve file details such as length and permissions.

            Parameters
            ----------
                target : `str`
                    The URL of the file whose details are to be retrieved.

                timeout_seconds : `int`
                    The number of seconds to wait before aborting the operation.

                dir_output : `obj`
                    The OS corresponding `dir` parser object

            Returns
            -------
                `file_details` : File details including size, permissions, index
                    and last modified date.

            Raises
            ------
                AttributeError
                    device object not passed in the function call

                Exception
                    Parser encountered an issue

            Examples
            --------
                # FileUtils
                >>> from pyats.utils.fileutils import FileUtils

                # Instanciate a filetransferutils instance for NXOS device
                >>> fu_device = FileUtils.from_device(device)

                # list the file details on the device 'flash:' directory
                >>> directory_output = fu_device.stat(target='flash:memleak.tcl',
                ...     timeout_seconds=300, device=device)

                >>> directory_output['size']
                ...     '104260'
                >>> directory_output['permissions']
                ...     '-rw-'

        """

        # Extract device from the keyword arguments, if not passed raise an
        # AttributeError
        device = kwargs.get('device') or getattr(self, 'device', None)
        if not device:
            raise AttributeError("Device object is missing, can't proceed with"
                                 " execution")

        return self.parsed_dir(target=target,
                               timeout_seconds=timeout_seconds,
                               dir_output=dir_output,
                               **kwargs)

    def deletefile(self, target, timeout_seconds, *args, **kwargs):
        """ Delete a file

            Parameters
            ----------
                target : `str`
                    The URL of the file whose details are to be retrieved.

                timeout_seconds : `int`
                    The number of seconds to wait before aborting the operation.

            Returns
            -------
                None

            Raises
            ------
            Exception
                When a device object is not present or device execution encountered
                an unexpected behavior.

            Examples
            --------
                # FileUtils
                >>> from pyats.utils.fileutils import FileUtils

                # Instanciate a filetransferutils instance for NXOS device
                >>> fu_device = FileUtils.from_device(device)

                # delete a specific file on device directory 'flash:'
                >>> directory_output = fu_device.deletefile(
                ...     target='flash:memleak_bckp.tcl',
                ...     timeout_seconds=300, device=device)

        """

        # delete flash:memleak.tcl
        cmd = 'delete {f}'.format(f=target)

        self.send_cli_to_device(cli=cmd,
                                timeout_seconds=timeout_seconds,
                                **kwargs)

    def renamefile(self, source, destination, timeout_seconds, cmd, *args,
                   **kwargs):
        """ Rename a file

            Parameters
            ----------
                source : `str`
                    The URL of the file to be renamed.

                destination : `str`
                    The URL of the new file name.

                timeout_seconds : `int`
                    Maximum allowed amount of time for the operation.

            Returns
            -------
                None

            Raises
            ------
            Exception
                When a device object is not present or device execution encountered
                an unexpected behavior.

            Examples
            --------
                # FileUtils
                >>> from pyats.utils.fileutils import FileUtils

                # Instanciate a filetransferutils instance for NXOS device
                >>> fu_device = FileUtils.from_device(device)

                # rename the file on the device 'flash:' directory
                >>> fu_device.renamefile(target='flash:memleak.tcl',
                ...     destination='memleak_backup.tcl'
                ...     timeout_seconds=300, device=device)

        """

        self.send_cli_to_device(cli=cmd,
                                timeout_seconds=timeout_seconds,
                                **kwargs)

    def chmod(self, target, mode, timeout_seconds, *args, **kwargs):
        """ Change file permissions

            Parameters
            ----------
                target : `str`
                    The URL of the file whose permissions are to be changed.

                mode : `int`
                    Same format as `os.chmod`.

                timeout_seconds : `int`
                    Maximum allowed amount of time for the operation.

            Returns
            -------
                `None` if operation succeeded.

        """

        # To be used when implemented
        # import stat as libstat
        # stat.filemode(output.st_mode)
        # libstat.filemode(mode)

        raise NotImplementedError("The fileutils module {} "
                                  "does not implement chmod.".format(
                                      self.__module__))

    def validateserver(self,
                       cmd,
                       target,
                       timeout_seconds=300,
                       *args,
                       **kwargs):
        """ Make sure that the given server information is valid

            Function that verifies if the server information given is valid, and if
            the device can connect to it. It does this by saving `show clock`
            output to a particular file using transfer protocol. Then deletes the
            file.

            Parameters
            ----------
                cmd (`str`):  Command to be executed on the device
                target (`str`):  File path including the protocol, server and
                    file location.
                timeout_seconds: `str`
                    The number of seconds to wait before aborting the operation.
                    Default is 300

            Returns
            -------
                `None`

            Raises
            ------
                Exception: If the command from the device to server is unreachable
                    or the protocol used doesn't support remote checks.

            Examples
            --------
                # FileUtils
                >>> from pyats.utils.fileutils import FileUtils

                # Instanciate a filetransferutils instance for NXOS device
                >>> fu_device = FileUtils.from_device(device)

                # Validate server connectivity
                >>> fu_device.validateserver(
                ...     target='ftp://10.1.7.250//auto/tftp-ssr/show_clock',
                ...     timeout_seconds=300, device=device)
        """

        logger.info(
            'Verifying if server can be reached and if a temp file can '
            'be created')

        # Send the command
        try:
            self.send_cli_to_device(cli=cmd,
                                    timeout_seconds=timeout_seconds,
                                    **kwargs)
        except Exception as e:
            raise type(e)('TFTP/FTP server is unreachable') from e

        # Instanciate a server
        futlinux = server(testbed=self.testbed)

        # Check server created file
        try:
            futlinux.checkfile(target)
        except Exception as e:
            raise type(e)("Server created file can't be checked") from e

        # Delete server created file
        try:
            futlinux.deletefile(target)
        except Exception as e:
            raise type(e)("Server created file can't be deleted") from e

        # Great success!
        logger.info("Server is ready to be used")

    def copyconfiguration(self,
                          source,
                          destination,
                          cmd,
                          used_server,
                          timeout_seconds=300,
                          *args,
                          **kwargs):
        """ Copy configuration to/from device

            Copy configuration on the device or between locations supported on the
            device and on the server.

            Parameters
            ----------
                source: `str`
                    Full path to the copy 'from' location
                destination: `str`
                    Full path to the copy 'to' location
                timeout_seconds: `str`
                    The number of seconds to wait before aborting the operation
                vrf: `str`
                    Vrf to be used during copy operation

            Returns
            -------
                `None`

            Raises
            ------
                Exception
                    When a device object is not present or device execution
                    encountered an unexpected behavior.

            Examples
            --------
                # FileUtils
                >>> from pyats.utils.fileutils import FileUtils

                # Instantiate a filetransferutils instance for NXOS device
                >>> from pyats.utils.fileutils import FileUtils
                >>> fu_device = FileUtils.from_device(device)

                # copy file from server to device running configuration
                >>> fu_device.copyconfiguration(
                ...     source='ftp://10.1.0.213//auto/tftp-ssr/config.py',
                ...     destination='running-config',
                ...     timeout_seconds='300', device=device)

                # copy running-configuration to device memory
                >>> fu_device.copyconfiguration(
                ...     from_file_url='running-config',
                ...     to_file_url='bootflash:filename',
                ...     timeout_seconds='300', device=device)

                # copy startup-configuration running-configuration
                >>> fu_device.copyconfiguration(
                ...     from_file_url='startup-config',
                ...     to_file_url='running-config',
                ...     timeout_seconds='300', device=device)
        """

        self.send_cli_to_device(cli=cmd,
                                timeout_seconds=timeout_seconds,
                                used_server=used_server,
                                **kwargs)
