""" File utils base class for filetransferutils package. """

import logging
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

logger = logging.getLogger(__name__)

# Error patterns to be caught when executing cli on device
FAIL_MSG = ['failed to copy', 'Unable to find', 'Error opening', 'Error', 'operation failed',
            'Compaction is not supported', 'Copy failed', 'No route to host', 'Connection timed out', 'not found', 'No space',
            'not a remote file']

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
        if 'device' in kwargs:
            device = kwargs['device']
        else:
            raise AttributeError("Device object is missing, can't proceed with"
                             " execution")

        # Extracting username and password to be used during device calls
        if used_server:
            username, password = self.get_auth(used_server)
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
            Statement(pattern=r'.*Do you want to overwrite.*',
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

        output = device.execute(cli, timeout=timeout_seconds, reply=dialog, prompt_recovery=True)

        # Check if user passed extra error/fail patterns to be caught
        if invalid:
            FAIL_MSG.extend(invalid)

        # Checking for the error/fail patterns, raise an exception if found
        for line in output.splitlines():
            for word in FAIL_MSG:
                if word in line:
                    raise SubCommandFailure('Error message caught in the following line: "{line}"'.format(line=line))

        return output

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

    def is_valid_ip(self, ip, device, vrf=None, cache_ip=True):
        if cache_ip:
            return self.is_valid_ip_cache(ip, device, vrf)
        else:
            return self.is_valid_ip_no_cache(ip, device, vrf)

    def get_hostname(self, server_name_or_ip, device, vrf=None, cache_ip=True):
        """ Get host name or address to connect to.
            (inherited from pyats FileUtils with support for device connection)
        Returns
        -------
            DNS name or IP address of server to connect to.

            If IP address (single or list) specified in server block:
            Return first reachable address (plugin determines reachability).

            If no address specified, or if no address reachable:
            Server name, if specified in server block, is next preferred.
            If neither address nor server keys are present in server block,
            or if the server could not be found in the testbed,
            return the user-specified server name or IP address.

        Raises
        ------
        Exception
            if server details not found in testbed.

        """
        server_block = self.get_server_block(
            server_name_or_ip = server_name_or_ip)

        if server_block:
            address = server_block.get('address', None)

            if address:
                if type(address) in (tuple, list):
                    # a list of ips were provided - use the first valid one
                    # that we can reach
                    for addr in address:
                        if self.is_valid_ip(addr, device, vrf=vrf, cache_ip=cache_ip):
                            return addr
                else:
                    # not a list - return it
                    return address

            # no reachable address, or no address specified,
            # default to server dns name or alias, or originally specified
            # hostname if all server block lookups fail.
            return server_block.get('server', server_name_or_ip)
        else:
            msg = "No details found in testbed for hostname {}.".\
                format(server_name_or_ip)
            if server_name_or_ip is not None:
                logger.warning(msg)
            else:
                logger.debug(msg)

        # Server block lookup has failed, return originally specified hostname
        # (garbage in, garbage out).
        return server_name_or_ip

    def validate_and_update_url(self, url, device, vrf=None, cache_ip=True):
        """Validate the url and replace the hostname/address with a
            reachable address from the testbed"""
        parsed_url = urlparse(url)

        # if there is a host name, this means the address is remote
        if parsed_url.hostname:
            hostname = self.get_hostname(parsed_url.hostname, device, vrf=vrf, cache_ip=cache_ip)
            return url.replace(parsed_url.hostname, hostname)

        # just return url if it's local
        else:
            return url


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
            if parsed.netloc:
                # remove tailing colon
                netloc = parsed.netloc.split(':')[0]
                used_server = netloc
                break

        if not used_server:
            # If both URLS have no valid IP addres, raise an exception
            raise Exception("No valid server address or hostname has been detected in the "
                "passed URLS '{from_URL}' & '{to_URL}'".format(
                    from_URL=source, to_URL=destination))

        return used_server
