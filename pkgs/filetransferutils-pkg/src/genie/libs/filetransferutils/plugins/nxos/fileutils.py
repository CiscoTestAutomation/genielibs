""" File utils base class for NXOS devices. """

import logging

# Parent inheritance
from .. import FileUtils as FileUtilsDeviceBase

# Dir parser
try:
    from genie.libs.parser.nxos.show_platform import Dir
except ImportError:
    # For apidoc building only
    from unittest.mock import Mock; Dir=Mock()

logger = logging.getLogger(__name__)


class FileUtils(FileUtilsDeviceBase):

    def copyfile(self, source, destination, timeout_seconds=300,
        vrf=None, compact=False, use_kstack=False, *args, **kwargs):
        """ Copy a file to/from NXOS device

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
                vrf: `str`
                    Vrf to be used during copy operation
                compact: `bool`
                    Compress image during copy operation
                use_kstack: `bool`
                    Use faster version during copy operation
                    Not supported with a file transfer protocol
                    prompting for a username and password

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

        """
        # use a device passed as an argument, or the device saved as an
        # attribute
        device = kwargs.get('device') or getattr(self, 'device', None)

        # update source and destination with the valid address from testbed
        source = self.validate_and_update_url(source,
                                              device=device,
                                              vrf=vrf,
                                              cache_ip=kwargs.get(
                                                  'cache_ip', True))
        destination = self.validate_and_update_url(destination,
                                                   device=device,
                                                   vrf=vrf,
                                                   cache_ip=kwargs.get(
                                                       'cache_ip', True))

        if vrf is None:
            logger.info('Using default vrf "management" for NXOS.')
            vrf = 'management'

        # copy flash:/memleak.tcl ftp://10.1.0.213//auto/tftp-ssr/memleak.tcl vrf management
        if vrf:
            # for n9k only
            if compact:
                cmd = 'copy {f} {t} compact vrf {vrf}'.format(f=source,
                                                              t=destination,
                                                              vrf=vrf)
            else:
                cmd = 'copy {f} {t} vrf {vrf}'.format(f=source,
                                                      t=destination,
                                                      vrf=vrf)
        else:
            if compact:
                cmd = 'copy {f} {t} compact'.format(f=source, t=destination)
            else:
                cmd = 'copy {f} {t}'.format(f=source, t=destination)

        # for n9k only
        if use_kstack:
            cmd += ' use-kstack'

        # Extract the server address to be used later for authentication
        used_server = self.get_server(source, destination)
        return super().copyfile(source=source, destination=destination,
            timeout_seconds=timeout_seconds, cmd=cmd, used_server=used_server,
            vrf=vrf, *args, **kwargs)

    def dir(self, target, timeout_seconds=300, *args, **kwargs):
        """ Retrieve filenames contained in a directory.

            Do not recurse into subdirectories, only list files at the top level
            of the given directory.

            Parameters
            ----------
                target : `str`
                    The directory whose details are to be retrieved.

                timeout_seconds : `int`
                    The number of seconds to wait before aborting the operation.

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

                # list all files on the device directory 'bootflash:'
                >>> directory_output = fu_device.dir(target='bootflash:',
                ...     timeout_seconds=300, device=device)

                >>> directory_output

                ['bootflash:/virt_strg_pool_bf_vdc_1/',
                 'bootflash:/platform-sdk.cmd', 'bootflash:/.swtam/',
                 'bootflash:/virtual-instance/', 'bootflash:/nxos.7.0.3.I7.1.bin',
                 'bootflash:/virtual-instance.conf', 'bootflash:/scripts/',
                 'bootflash:/memleak.tcl', 'bootflash:/acfg_base_running_cfg_vdc1',
                 'bootflash:/.rpmstore/']

        """

        dir_output = super().parsed_dir(target, timeout_seconds,
            Dir, *args, **kwargs)

        # Extract the files location requested
        output = self.parse_url(target)

        # Construct the directory name
        directory = output.scheme + ":/"

        # Create a new list to return
        new_list = []

        for key in dir_output['files']:
            new_list.append(directory+key)

        return new_list

    def stat(self, target, timeout_seconds=300, *args, **kwargs):
        """ Retrieve file details such as length and permissions.

            Parameters
            ----------
                target : `str`
                    The URL of the file whose details are to be retrieved.

                timeout_seconds : `int`
                    The number of seconds to wait before aborting the operation.

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
                >>> directory_output['permissions']

                (Pdb) directory_output
                {'last_modified_date': 'Mar 20 2018 10:26:01 +00:00',
                 'size': '104260', 'permissions': '-rw-', 'index': '69705'}

        """

        files = super().stat(target, timeout_seconds, Dir, *args, **kwargs)

        # Extract the file name requested
        output = self.parse_url(target)
        file_details = files['files'][output.path]

        return file_details

    def deletefile(self, target, timeout_seconds=300, *args, **kwargs):
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
                    When a device object is not present or device execution
                    encountered an unexpected behavior.

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

        super().deletefile(target, timeout_seconds, *args, **kwargs)

    def renamefile(self, source, destination, timeout_seconds=300, *args,
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
                    When a device object is not present or device execution
                    encountered an unexpected behavior.

            Examples
            --------
                # FileUtils
                >>> from pyats.utils.fileutils import FileUtils

                # Instanciate a filetransferutils instance for NXOS device
                >>> fu_device = FileUtils.from_device(device)

                # rename the file on the device 'bootflash:' directory
                >>> fu_device.renamefile(target='bootflash:memleak.tcl',
                ...     destination='memleak_backup.tcl'
                ...     timeout_seconds=300, device=device)

        """
        # move bootflash:memleak.tcl memleak_j.tcl
        cmd = 'move {f} {u}'.format(f=source, u=destination)

        super().renamefile(source, destination, timeout_seconds, cmd,
            *args, **kwargs)

    def chmod(self, target, mode, timeout_seconds=300, *args, **kwargs):
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

        raise NotImplementedError("The fileutils module {} "
            "does not implement chmod.".format(self.__module__))

    def validateserver(self, target, timeout_seconds=300,
        vrf='management', *args, **kwargs):
        ''' Make sure that the given server information is valid

            Function that verifies if the server information given is valid, and if
            the device can connect to it. It does this by saving `show clock`
            output to a particular file using transfer protocol. Then deletes the
            file.

            Parameters
            ----------
                target (`str`):  File path including the protocol,
                    server and file location.
                timeout_seconds (`str`):
                    The number of seconds to wait before aborting the operation.
                vrf (`str`):
                    Vrf value to be used during execution. Default is `management`

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
        '''
        # Extract the server address to be used later for authentication
        used_server = self.get_server(target)

        # Patch up the command together
        # show clock > tftp://10.1.0.213//auto/ftp-ssr/show_clock vrf management
        cmd = "show clock > {e} vrf {vrf}".format(e=target, vrf=vrf)

        super().validateserver(cmd=cmd, target=target,
            timeout_seconds=timeout_seconds, used_server=used_server, *args,
            **kwargs)

    def copyconfiguration(self, source, destination, timeout_seconds=300,
        vrf='management', *args, **kwargs):
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
                ...     source='ftp://10.1.0.213//auto/tftp-ssr/memleak.tcl',
                ...     destination='running-config',
                ...     timeout_seconds='300', device=device)

                # copy running-configuration to device memory
                >>> fu_device.copyconfiguration(
                ...     source='running-configuration',
                ...     destination='bootflash:filename',
                ...     timeout_seconds='300', device=device)

                # copy startup-configuration running-configuration
                >>> fu_device.copyconfiguration(
                ...     source='startup-configuration',
                ...     destination='running-configuration',
                ...     timeout_seconds='300', device=device)
        """

        # Extract the server address to be used later for authentication
        try:
            used_server = self.get_server(source, destination)
        except:
            # We catch exception in the case where we copy configurations
            # between running and startup on the device
            used_server = None
            vrf = None

        # Build copy command
        # Example - copy running-configuration bootflash:tempfile1
        if vrf:
            cmd = 'copy {f} {t} vrf {vrf}'.format(f=source, t=destination,
                vrf=vrf)
        else:
            cmd = 'copy {f} {t}'.format(f=source, t=destination)

        super().copyconfiguration(source=source, destination=destination,
            timeout_seconds=timeout_seconds, cmd=cmd, used_server=used_server,
            *args, **kwargs)
