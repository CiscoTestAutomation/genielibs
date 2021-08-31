""" File utils base class for XE devices. """

# Parent inheritance
from .. import FileUtils as FileUtilsDeviceBase

# Dir parser
try:
    from genie.libs.parser.iosxe.show_platform import Dir
except ImportError:
    # For apidoc building only
    from unittest.mock import Mock; Dir=Mock()


class FileUtils(FileUtilsDeviceBase):

    def copyfile(self, source, destination, timeout_seconds=300,
                 vrf=None, *args, **kwargs):
        """ Copy a file to/from IOSXE device

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

                # Instanciate a filetransferutils instance for IOSXE device
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

        # copy flash:/memleak.tcl ftp://10.1.0.213//auto/tftp-ssr/memleak.tcl
        if vrf:
            cmd = 'copy {f} {t} vrf {vrf_value}'.format(f=source,
                                                        t=destination,
                                                        vrf_value=vrf)
        else:
            # copy flash:/memleak.tcl ftp://10.1.0.213//auto/tftp-ssr/memleak.tcl
            if vrf:
                cmd = 'copy {f} {t} vrf {vrf_value}'.format(f=source, t=destination, vrf_value=vrf)
            else:
                cmd = 'copy {f} {t}'.format(f=source, t=destination)

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

                # Instanciate a filetransferutils instance for IOSXE device
                >>> fu_device = FileUtils.from_device(device)

                # list all files on the device directory 'flash:'
                >>> directory_output = fu_device.dir(target='flash:',
                ...     timeout_seconds=300, device=device)

                >>> directory_output

                ['flash:/core', 'flash:/.installer',
                 'flash:/bootloader_evt_handle.log', 'flash:/stby-vlan.dat',
                 'flash:/memleak.tcl', 'flash:/nvram_config_bkup',
                 'flash:/tech_support', 'flash:/.rollback_timer',
                 'flash:/vlan.dat', 'flash:/onep', 'flash:/.dbpersist',
                 'flash:/ISSUCleanGolden', 'flash:/iox', 'flash:/tools',
                 'flash:/dc_profile_',
                 'flash:/RestoreTue_Mar_20_12_13_39_2018-Mar-20-11-14-38.106-0',
                 'flash:/RestoreTue_Mar_20_12_19_11_2018-Mar-20-11-20-09.900-0',
                 'flash:/nvram_config', 'flash:/boothelper.log', 'flash:/CRDU',
                 'flash:/.prst_sync', 'flash:/fake_config.tcl', 'flash:/gs_script']

        """

        dir_output = super().parsed_dir(target, timeout_seconds,
            Dir, *args, **kwargs)

        # Extract the files location requested
        output = self.parse_url(target)

        # Construct the directory name
        directory = output.scheme + ":/"

        # Create a new list to return
        new_list = []

        for key in dir_output['dir'][directory]['files']:
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

                # Instanciate a filetransferutils instance for IOSXE device
                >>> fu_device = FileUtils.from_device(device)

                # list the file details on the device 'flash:' directory
                >>> directory_output = fu_device.stat(target='flash:memleak.tcl',
                ...     timeout_seconds=300, device=device)

                >>> directory_output['size']
                >>> directory_output['permissions']

                EX
                --
                    (Pdb) directory_output
                    {'last_modified_date': 'Mar 20 2018 10:26:01 +00:00',
                     'size': '104260', 'permissions': '-rw-', 'index': '69705'}

        """

        files = super().stat(target, timeout_seconds, Dir, *args, **kwargs)

        # Extract the file name requested
        output = self.parse_url(target)
        directory = output.scheme + ":/"
        file_details = files['dir'][directory]['files'][output.path]

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

                # Instanciate a filetransferutils instance for IOSXE device
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

                # Instanciate a filetransferutils instance for IOSXE device
                >>> fu_device = FileUtils.from_device(device)

                # rename the file on the device 'flash:' directory
                >>> fu_device.renamefile(target='flash:memleak.tcl',
                ...     destination='memleak_backup.tcl'
                ...     timeout_seconds=300, device=device)

        """
        # rename bootflash:memleak.tcl memleak_j.tcl
        cmd = 'rename {f} {u}'.format(f=source, u=destination)

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

    def validateserver(self, target, timeout_seconds=300, *args, **kwargs):
        ''' Make sure that the given server information is valid


            Function that verifies if the server information given is valid, and if
            the device can connect to it. It does this by saving `show clock`
            output to a particular file using transfer protocol. Then deletes the
            file.

            Parameters
            ----------
                target (`str`):  File path including the protocol,
                    server and file location.
                timeout_seconds: `str`
                    The number of seconds to wait before aborting the operation.

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
                ...     target='ftp://10.1.6.242//auto/tftp-ssr/show_clock',
                ...     timeout_seconds=300, device=device)
        '''
        # Extract the server address to be used later for authentication
        used_server = self.get_server(target)

        # Patch up the command together
        # show clock | redirect ftp://10.1.6.242//auto/tftp-ssr/show_clock
        cmd = "show clock | redirect {e}".format(e=target)

        self.parse_url(target)
        super().validateserver(cmd=cmd, target=target,
            timeout_seconds=timeout_seconds, used_server=used_server, *args,
            **kwargs)

    def copyconfiguration(self, source, destination, timeout_seconds=300,
        *args, **kwargs):
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
                ...     source='running-config',
                ...     destination='bootflash:filename',
                ...     timeout_seconds='300', device=device)

                # copy startup-configuration running-configuration
                >>> fu_device.copyconfiguration(
                ...     source='startup-config',
                ...     destination='running-config',
                ...     timeout_seconds='300', device=device)
        """

        # Extract the server address to be used later for authentication
        try:
            used_server = self.get_server(source, destination)
        except:
            # We catch exception in the case where we copy configurations
            # between running and startup on the device
            used_server = None

        # Build copy command
        # Example - copy running-configuration bootflash:tempfile1
        cmd = 'copy {f} {t}'.format(f=source, t=destination)

        super().copyconfiguration(source=source, destination=destination,
            timeout_seconds=timeout_seconds, cmd=cmd, used_server=used_server,
            *args, **kwargs)