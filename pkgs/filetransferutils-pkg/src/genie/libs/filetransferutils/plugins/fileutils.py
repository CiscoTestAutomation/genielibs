""" File utils common base class """
import re
import logging
import contextlib
import ipaddress
import time
import shlex
import subprocess
from functools import lru_cache
from urllib.parse import urlparse
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure

import contextlib

from functools import cache
from datetime import datetime
from urllib.parse import urlparse

from cryptography import x509
from cryptography.hazmat.backends import default_backend

try:
    from genie.libs.filetransferutils.bases.fileutils import FileUtilsBase as server
    from genie.libs.filetransferutils.ftp.fileutils import filemode_to_mode
except ImportError:
    # For apidoc building only
    from unittest.mock import Mock
    server = Mock
    filemode_to_mode = Mock

logger = logging.getLogger(__name__)

# Error patterns to be caught when executing CLI on a device
FAIL_MSG = [
    'Permission denied[^,]', 'failed to copy', 'Unable to find',
    r'Error(?! opening tftp://255\.255\.255\.255)', 'operation failed',
    'Compaction is not supported', 'Copy failed', 'No route to host',
    'Connection timed out', 'not found', 'No space', 'not a remote file',
    'Could not resolve', 'Invalid URI', "couldn't connect to host",
    "no such file or directory (invalid server)", ".*Cannot overwrite/delete.*",
    "No such file or directory"
]

# Parent inheritance
from .. import FileUtils as FileUtilsCommonDeviceBase


class FileUtils(FileUtilsCommonDeviceBase):

    def send_cli_to_device(self, cli, used_server=None, invalid=None,
                           timeout_seconds=300, prompt_recovery=True,
                           destination='', **kwargs):
        """ Send command to a particular device and deal with its result

            Parameters
            ----------
                cli: `str`
                  Full command to be executed on the device
                invalid: `str`
                  Any invalid patterns need to be caught during execution
                timeout_seconds: `str`
                  The number of seconds to wait before aborting the operation.
                used_server: `str`
                  Server address/name
                destination: `str`
                  Destination url/path

            Returns
            -------
                `None`

            Raises
            ------
                Exception
                    When a device object is not present or device execution encountered
                    an unexpected behavior.

                ValueError
                    When a device execution output shows one of the invalid patterns.

            Examples
            --------
                # FileUtils
                >>> from ..fileutils import FileUtils

                  # copy flash:/memleak.tcl ftp://10.1.0.213//auto/tftp-ssr/memleak.tcl
                  >>> cmd = 'copy {f} {t}'.format(f=source, t=destination)

                  >>> FileUtils.send_cli_to_device(cli=cmd,
                  ...   timeout_seconds=timeout_seconds, **kwargs)
        """

        # Extract device from the keyword arguments, if not passed raise an
        # AttributeError
        device = kwargs.get('device') or getattr(self, 'device', None)
        if not device:
            raise AttributeError("Device object is missing, can't proceed with execution")

        # Extracting username and password to be used during device calls
        if used_server:
            # Case when cli sent contains the username
            # EX: admin@1.1.1.1

            if 'username' in kwargs and kwargs['username'] and kwargs['username'] in used_server:
                used_server = used_server.split('@')[1]
            username, password = self.get_auth(used_server,
                                               protocol=kwargs.get('protocol'))
        else:
            username = kwargs.get('username', '')
            password = kwargs.get('password', '')

        destination_filename = ''
        if destination:
            # proto://server:port//filename.bin -> /filename.bin
            # bootflash:/filename.bin -> /filename.bin
            try:
                p = urlparse(destination)
                # if destination ends with a slash, assume it's a directory
                # rather than a filename
                if not p.path.endswith('/'):
                    destination_filename = p.path.replace('//', '/')
            except Exception:
                pass

        # Checking if user passed any extra invalid patterns
        if 'invalid' in kwargs:
            invalid = kwargs['invalid']

        # Create unicon dialog
        dialog = Dialog([
            Statement(pattern=r'Address or name of remote host.*$',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Destination filename.*$',
                      action=f'sendline({destination_filename})',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Abort Copy\? \[confirm\]\s*$',
                      action='sendline(n)',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'(?<!Abort Copy\? )\[confirm\]\s*$',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Are you sure you want to continue connecting.*$',
                      action='sendline(yes)',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Destination username.*$',
                      action='sendline({username})'.format(username=username),
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Destination password.*$',
                      action='sendline({password})'.format(password=password),
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'.*[D|d]estination file *name.*$',
                      action=f'sendline({destination_filename})',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Enter username:\s*$',
                      action='sendline({username})'.format(username=username),
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'.*[P|p]assword:\s*$',
                      action='sendline({password})'.format(password=password),
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'[P|p]assword for .*$',
                      action='sendline({password})'.format(password=password),
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Do you want to delete.*$',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Host name or IP address.*$',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Delete filename.*$',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Source username.*$',
                      action='sendline({username})'.format(username=username),
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Source filename.*$',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r' *[O|o]verwrite.*continu.*$',
                      action='sendline({overwrite})'.format(overwrite='yes' if kwargs.get('overwrite', True) else 'no'),
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'.*Do you want to (overwrite|overwritte|overwrit).*$',
                      action='sendline({overwrite})'.format(
                          overwrite='y' if kwargs.get('overwrite', True) else 'n'),
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Enter vrf.*$',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'.*This is a directory. +Do you want to continue.*$',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False)
            ])

        error_pattern = FAIL_MSG
        # Check if user passed extra error/fail patterns to be caught
        if invalid:
            error_pattern.extend(invalid)

        if hasattr(device, 'testbed'):
            if hasattr(device.testbed, 'custom'):
                if hasattr(device.testbed.custom, 'fileutils'):
                    error_pattern = device.testbed.custom.fileutils.get('error_pattern')
                    if isinstance(error_pattern, list):
                        error_pattern = error_pattern
                    append_error_pattern = device.testbed.custom.fileutils.get('append_error_pattern')
                    if isinstance(append_error_pattern, list):
                        error_pattern.extend(append_error_pattern)
        output = device.execute(cli,
                                prompt_recovery=prompt_recovery,
                                timeout=timeout_seconds,
                                reply=dialog,
                                error_pattern=error_pattern)

        return output

    @contextlib.contextmanager
    def file_transfer_config(self, server=None, interface=None, **kwargs):
        """ Context manager to try configuring a device for an upcoming file
            transfer. Saves a configuration checkpoint, applies configuration,
            and upon exit reverts the configuration.

            Arguments
            ---------
            server: `str`
                The server address to copy files to or from.

            interface: `str`
                Device interface to use as source interface (will apply
                protocol source interface configuration to the device if provided)

        """
        device = kwargs.get('device') or getattr(self, 'device', None)
        if not device:
            raise AttributeError("Device object is missing, can't proceed with"
                                 " configuration")
        # device might be a connection, get actual device
        device = device.device

        vrf = kwargs.get('vrf')
        # Retrieve correct config template for this OS
        if vrf:
            copy_config = getattr(self, 'COPY_CONFIG_VRF_TEMPLATE', None)
        else:
            copy_config = getattr(self, 'COPY_CONFIG_TEMPLATE', None)

        if not (interface and copy_config):
            copy_config = None

        config_restore = None
        if copy_config:
            try:
                config_send = []
                config_restore = []
                for each_config in copy_config:
                    cfg_include = each_config.split('{')[0]
                    if interface:
                        each_config = each_config.format(vrf=vrf,
                                                         interface=interface,
                                                         blocksize=8192)
                    output = device.execute(
                        'show running-config | include {}'.format(cfg_include))
                    output = re.sub(r'.*Building configuration...',
                                    '',
                                    output,
                                    flags=re.S)
                    if cfg_include not in output:
                        # prepare configure config and restore config
                        config_send.append(each_config)
                        config_restore.append('no ' + each_config)
                if config_send:
                    device.configure(config_send)
            except Exception:
                logger.warning(
                    'Failed to apply configuration on %s' % str(device),
                    exc_info=True)
                config_restore = None

        try:
            # Inside context manager
            yield

        finally:
            if config_restore:
                try:
                    device.configure(config_restore)
                    # If specified, wait for a period of time after restoring
                    # configuration to let it settle
                    wait_time = kwargs.get('wait_after_restore', 1)
                    time.sleep(wait_time)
                except Exception:
                    logger.warning(
                        'Failed to restore configuration on %s' % str(device),
                        exc_info=True)

    @lru_cache(maxsize=32)
    def is_valid_ip_cache(self, ip, device, vrf=None):
        # check if ip is reachable from device by sending ping command,
        # this one is cached that it only pings the first time
        try:
            if vrf:
                device.ping(ip, vrf=vrf)
            else:
                device.ping(ip)
            return True
        except SubCommandFailure:
            return False

    def is_valid_ip_no_cache(self, ip, device, vrf=None):
        # check if ip is reachable from device by sending ping command, not cached version
        try:
            if vrf:
                device.ping(ip, vrf=vrf)
            else:
                device.ping(ip)
            return True
        except SubCommandFailure:
            return False

    def is_valid_ip(self, ip, device=None, vrf=None, cache_ip=True):
        device = device or getattr(self, 'device')
        if cache_ip:
            return self.is_valid_ip_cache(ip, device, vrf)
        else:
            return self.is_valid_ip_no_cache(ip, device, vrf)

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

        with self.file_transfer_config(used_server, interface=interface, **kwargs, 
                                       source=source, destination=destination):
            try:
                return self.send_cli_to_device(
                    cli=cmd,
                    timeout_seconds=timeout_seconds,
                    used_server=used_server,
                    destination=destination,
                    **kwargs)
            except Exception as e:
                if "https" in cmd:
                    logger.warning("HTTPS transfer failed, retrying with HTTP")
                    return self.send_cli_to_device(
                        cli=cmd.replace("https", "http"),
                        timeout_seconds=timeout_seconds,
                        used_server=used_server,
                        destination=destination,
                        **kwargs)
                raise e

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

    def deletefile(self, target, timeout_seconds, cmd = None, *args, **kwargs):
        """ Delete a file

            Parameters
            ----------
                target : `str`
                    The URL of the file whose details are to be retrieved.

                timeout_seconds : `int`
                    The number of seconds to wait before aborting the operation.

                cmd : `str`
                    Command to override the default delete command

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
        cmd = cmd or 'delete {f}'.format(f=target)

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

    def execute_in_subprocess(self, command, timeout_seconds, **kwargs):
        """ Executes a command in a subprocess.

        Parameters
        ----------
            command : `str`
                The command to run

            timeout_seconds : `int`
                The maximum number of seconds to wait before aborting the
                command execution.

            kwargs : `dict`
                Extra arguments to pass to Popen constructor


        Returns
        -------
            `None`

        Raises
        ------
            `subprocess.CalledProcessError` if error is encountered.

            `subprocess.TimeoutExpired` if the timeout expires before the
            command returns a result.
        """
        if command:
            logger.info("Executing command %s" % command)
            args = shlex.split(command)
            subprocess.check_call(args, timeout=timeout_seconds, shell=False,
                **kwargs)

class HTTPFileUtilsBase(FileUtilsCommonDeviceBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_mapping = {}

    @cache
    def get_certificate_details(self, device, hostname, port):
        """Retrieve SSL/TLS certificate details from a server.
        This method connects to a server at the specified hostname and port to retrieve
        its SSL/TLS certificate in PEM format and extract the Common Name (CN) from the
        certificate's subject field.
        If a URL mapping exists for the provided hostname, the method will recursively
        call itself with the mapped hostname instead.

        Args:
            device: The device object that provides the API interface for certificate retrieval.
            hostname (str): The hostname or IP address of the server to connect to.
            port (int): The port number on which to establish the SSL/TLS connection.

        Returns:
            tuple: A tuple containing:
                - cert (str): The PEM-encoded certificate string.
                - cn (str): The Common Name (CN) extracted from the certificate's subject.

        Raises:
            Exception: May raise exceptions related to network connectivity, certificate
                parsing, or if the certificate doesn't contain a Common Name field.
        """
        if self.url_mapping.get(hostname):
            hostname = self.url_mapping.get(hostname)
            return self.get_certificate_details(device, hostname, port)
        cert = device.api.get_server_certificate_pem(hostname, port).strip()

        # Extract CN from certificate
        x_509_cert = x509.load_pem_x509_certificate(cert.encode(), default_backend())
        cn = x_509_cert.subject.get_attributes_for_oid(x509.oid.NameOID.COMMON_NAME)[0].value

        return cert, cn

    @contextlib.contextmanager
    def file_transfer_config(self, server=None, interface=None, **kwargs):
        """
        Context manager to configure device for file transfer operations.
        This method configures the device with necessary settings to perform file transfers,
        particularly for HTTPS-based transfers. It sets up DNS host entries, trustpoints, and
        PKI authentication, then cleans up these configurations after the transfer completes.

        Args:
            server (str, optional): Server address for file transfer. Defaults to None.
            interface (str, optional): Interface to use for file transfer. Defaults to None.
            **kwargs: Additional keyword arguments including:
                - device: Device object to configure (required)
                - source (str): Source URL for file transfer
                - destination (str): Destination URL for file transfer

        Yields:
            None: Control is yielded back to caller to perform file transfer operations

        Raises:
            AttributeError: If device object is not provided or cannot be found

        Notes:
            - Sets the device clock to current time
            - For HTTPS URLs, retrieves server certificates and configures trustpoints
            - Configures DNS host entries for certificate common names
            - Automatically cleans up all configurations in the finally block
            - Uses temporary trustpoint named "pyats_temp_trustpoint"
            - Supports VRF-aware configurations through device.management.vrf
        """
        
        # Get device object
        device = kwargs.get('device') or getattr(self, 'device', None)
        if not device:
            raise AttributeError("Device object is missing, can't proceed with"
                                " configuration")
    
        # device might be a connection, get actual device
        device = device.device
        
        # Get current time in format 'hh:mm:ss d MMM'
        current_time = datetime.now().strftime('%H:%M:%S %-d %b %Y').lower()
        device.execute('clock set {}'.format(current_time))

        # Need the source URL to extract hostname and port
        source = kwargs.get('source')
        destination = kwargs.get('destination')
        for loc in (source, destination):
            parsed_url = urlparse(loc)
            if parsed_url.scheme.lower() != 'https':
                continue
            hostname = parsed_url.hostname
            port = parsed_url.port if parsed_url.port else 443

            # Retrieve server certificate
            cert, cn = self.get_certificate_details(device, hostname, port)

            mgmt = getattr(device, 'management', {})

            # Configure DNS host entry
            device.api.configure_ip_host(
                hostname=cn,
                ip_address=self.url_mapping.get(cn, hostname),
                vrf=mgmt.get('vrf')
            )

            # Configure trustpoint and PKI authenticate
            device.api.configure_trustpoint(
                revoke_check="none", 
                tp_name="pyats_temp_trustpoint",
                enrollment_option="terminal")
            device.api.configure_pki_authenticate_certificate(cert, "pyats_temp_trustpoint")

        try:
            yield
        finally:
            # Unconfigure trustpoint
            device.api.unconfigure_trustpoint("pyats_temp_trustpoint")
            device.api.unconfigure_ip_host(
                hostname=cn,
                ip_address=self.url_mapping.get(cn, hostname),
                vrf=mgmt.get('vrf')
            )

    def validate_and_update_url(self, url, device=None, **kwargs):
        """
        Validates and updates a URL by replacing the hostname with the CN from the server's SSL certificate.
        This method parses the provided URL and, if it uses HTTPS, retrieves the SSL certificate
        from the server to extract the Common Name (CN). It then rebuilds the URL using the CN
        instead of the original hostname, which can be useful for certificate validation scenarios.
        The mapping between CN and original hostname is stored for later reference.

        Args:
            url (str): The URL to validate and potentially update.
            device: Optional device object used to retrieve certificate details. Defaults to None.
            **kwargs: Additional keyword arguments passed to certificate retrieval.

        Returns:
            str: The updated URL with CN as hostname (for HTTPS), or the original URL (for non-HTTPS).
            
        Note:
            - Only HTTPS URLs are modified; other schemes are returned unchanged.
            - The original hostname is stored in self.url_mapping with CN as the key.
            - If no port is specified in the URL, port 443 is used by default for certificate retrieval.
        """
        
        parsed_url = urlparse(url)
        if parsed_url.scheme.lower() != 'https':
            return url
        _cert, cn = self.get_certificate_details(
            device, 
            parsed_url.hostname, 
            parsed_url.port if parsed_url.port else 443)
        
        # Rebuild URL with CN instead of hostname
        netloc = cn
        if parsed_url.port:
            netloc += f":{parsed_url.port}"
        rebuilt_url = parsed_url._replace(netloc=netloc)

        self.url_mapping[cn] = parsed_url.hostname

        return rebuilt_url.geturl()