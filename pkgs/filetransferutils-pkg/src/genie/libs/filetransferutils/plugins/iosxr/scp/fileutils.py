""" File utils base class for SCP on IOSXR devices. """

from ..fileutils import FileUtils as FileUtilsXRBase

from urllib.parse import urlparse

class FileUtils(FileUtilsXRBase):
    """ File utils base class for SCP on IOSXR devices. """
    def copyfile(self,
                 source,
                 destination,
                 timeout_seconds=300,
                 vrf=None,
                 *args,
                 **kwargs):
        """
            Copy any file to/from a device using SCP protocol with IOSXR-specific
            command format.

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
                `str` : Output of copy command

            Raises
            ------
                Exception
                    When a device object is not present or device execution
                    encountered an unexpected behavior.

            Examples
            --------
                # FileUtils
                >>> from pyats.utils.fileutils import FileUtils

                # Instanciate a filetransferutils instance for IOSXR SCP
                >>> fu_device = FileUtils.from_device(device, protocol='scp')

                # copy file from server to device with SCP
                >>> fu_device.copyfile(
                ...     source='scp://user@10.1.0.213:22/test_file.txt',
                ...     destination='harddisk:/test_file.txt',
                ...     timeout_seconds='300', device=device)

                # copy file from device to server with SCP
                >>> fu_device.copyfile(
                ...     source='harddisk:/test_file.txt',
                ...     destination='scp://user@10.1.0.213:22/backup_file.txt',
                ...     timeout_seconds='300', device=device)
        """
        # To check if source or destination is SCP
        is_source_scp = False

        # Parse URLs once to check for SCP protocol and extract components
        source_parsed = urlparse(source)
        dest_parsed = urlparse(destination)

        # Check if this is SCP and handle it with dynamic logic before URL validation
        if source_parsed.scheme == 'scp' or dest_parsed.scheme == 'scp':
            # Determine which URL is SCP and extract common components
            if source_parsed.scheme == 'scp':
                scp_parsed = source_parsed
                is_source_scp = True
            else:
                scp_parsed = dest_parsed

            # Extract SCP components
            username = scp_parsed.username
            password = scp_parsed.password
            hostname = scp_parsed.hostname
            port = scp_parsed.port
            filename = scp_parsed.path.lstrip('/')

            # Store credentials for authentication
            kwargs.update({'username': username, 'password': password})

            # Build IOSXR SCP command based on direction
            scp_target = f"{username}@{hostname}:{filename}"
            port_option = f" port {port}" if port and port != 22 else ""
            if is_source_scp:
                # SCP from server to device
                cmd = f"scp {scp_target} {destination}{port_option}"
            else:
                # SCP from device to server
                cmd = f"scp {source} {scp_target}{port_option}"

            # Add VRF if specified
            if vrf:
                cmd += ' vrf {vrf_value}'.format(vrf_value=vrf)

            # Execute SCP command directly with dynamic parsing
            return super().copyfile(source=source,
                                    destination=destination,
                                    timeout_seconds=timeout_seconds,
                                    cmd=cmd,
                                    vrf=vrf,
                                    *args,
                                    **kwargs)

