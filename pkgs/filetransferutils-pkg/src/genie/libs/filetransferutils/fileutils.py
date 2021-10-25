""" File utils base class for filetransferutils package. """

import re
import logging
import contextlib
import time
from functools import lru_cache

# Urlparse
from urllib.parse import urlparse

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure

# FileUtils Core
try:
    from pyats.utils.fileutils import FileUtils as FileUtilsBase
except ImportError:
    # For apidoc building only
    from unittest.mock import Mock; FileUtilsBase=Mock

# Abstract lookup for config restore
from genie.abstract import Lookup
from genie.libs import sdk, parser

logger = logging.getLogger(__name__)

# Error patterns to be caught when executing cli on device
FAIL_MSG = ['Permission denied[^,]', 'failed to copy', 'Unable to find', 'Error opening', 'Error', 'operation failed',
            'Compaction is not supported', 'Copy failed', 'No route to host', 'Connection timed out', 'not found',
            'No space', 'not a remote file', 'Could not resolve', 'Invalid URI', "couldn't connect to host",
            "protocol identification string lack carriage return", "no such file or directory (invalid server)",
            ".*Cannot overwrite/delete.*"]


class FileUtils(FileUtilsBase):

    def send_cli_to_device(self, cli, used_server=None, invalid=None,
                           timeout_seconds=300, **kwargs):
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
            raise AttributeError("Device object is missing, can't proceed with"
                                 " execution")

        # Extracting username and password to be used during device calls
        if used_server:
            # Case when cli sent contains the username
            # EX: admin@1.1.1.1

            if 'username' in kwargs and kwargs['username'] and kwargs['username'] in used_server:
                used_server = used_server.split('@')[1]
            username, password = self.get_auth(used_server,
                                               protocol=kwargs.get('protocol'))
        else:
            username = None
            password = None

        # Checking if user passed any extra invalid patterns
        if 'invalid' in kwargs:
            invalid = kwargs['invalid']

        # Create unicon dialog
        dialog = Dialog([
            Statement(pattern=r'Address or name of remote host.*',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Destination filename.*',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'\[confirm\]',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Are you sure you want to continue connecting.*',
                      action='sendline(yes)',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Destination username.*',
                      action='sendline({username})'.format(username=username),
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Destination password.*',
                      action='sendline({password})'.format(password=password),
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'.*[D|d]estination file *name.*',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Enter username:',
                      action='sendline({username})'.format(username=username),
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'.*[P|p]assword: *',
                      action='sendline({password})'.format(password=password),
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'[P|p]assword for .*',
                      action='sendline({password})'.format(password=password),
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Do you want to delete.*',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Host name or IP address.*',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Delete filename.*',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Source username.*',
                      action='sendline({username})'.format(username=username),
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Source filename.*',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r' *[O|o]verwrite.*continu.*',
                      action='sendline({overwrite})'.format(overwrite='yes' if kwargs.get('overwrite', True) else 'no'),
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'.*Do you want to (overwrite|overwritte).*',
                      action='sendline({overwrite})'.format(
                          overwrite='y' if kwargs.get('overwrite', True) else 'n'),
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Enter vrf.*',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'.*This is a directory. +Do you want to continue.*',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False)
            ])

        error_pattern = FAIL_MSG
        # Check if user passed extra error/fail patterns to be caught
        if invalid:
            error_pattern.extend(invalid)

        output = device.execute(cli,
                                timeout=timeout_seconds,
                                reply=dialog,
                                prompt_recovery=True,
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

    def parse_url(self, url):
        """ Parse the given url

            Parameters
            ----------
                url: `str`
                  Full url to be parsed

            Returns
            -------
                ParseResult class with the following keyword arguments
                (scheme='', netloc='', path='', params='', query='', fragment='')

            Raises
            ------
                None

            Examples
            --------
                # FileUtils
                >>> from ..fileutils import FileUtils

                # Parse the URL
                  >>> output = FileUtils.parse_url(file_url)
                          ParseResult(scheme='flash', netloc='', path='memleak.tcl',
                          params='', query='', fragment='')

                  >>> output.scheme
                  ...   'flash'

                  >>> output.path
                  ...   'memleak.tcl'

        """
        return urlparse(url)

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

    def get_server(self, source, destination=None):
        """ Get the server address from the provided URLs

            Parameters
            ----------
                source: `str`
                  URL path of the from location
                destination: `str`
                  URL path of the to location

            Returns
            -------
                used_server: `str`
                  String of the used server

            Raises
            ------
              None

            Examples
            --------
            # FileUtils
            >>> from ..fileutils import FileUtils

            # Get the server
              >>> output = FileUtils.get_server(source, destination)

              >>> output
              ...   '10.1.7.250'

        """
        used_server = None

        if destination:
            new_list = [source, destination]
        else:
            new_list = [source]

        # Extract the server address to be used later for authentication
        for item in new_list:
            parsed = self.parse_url(item)
            # Validate parsed address is a valid IP address
            if parsed.hostname:
                # only include address, no port or credentials
                used_server = parsed.hostname
                break

        if not used_server:
            # If both URLS have no valid IP addres, raise an exception
            raise Exception("No valid server address or hostname has been detected in the "
                "passed URLS '{from_URL}' & '{to_URL}'".format(
                    from_URL=source, to_URL=destination))

        return used_server