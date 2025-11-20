""" Base class for File Utilities. """

__copyright__ = "# Copyright (c) 2018 by cisco Systems, Inc. " \
    "All rights reserved."

__author__ = "Myles Dear <pyats-support@cisco.com>"

__all__ = ['FileUtilsBase', ]

import sys
import time
import psutil
import logging
import ipaddress

from urllib.parse import urlparse

from genie.libs import filetransferutils
from genie.abstract import Lookup
from pyats.utils.secret_strings import to_plaintext
from pyats.topology.credentials import DEFAULT_CRED

logger = logging.getLogger(__name__)

DEFAULT_CHECK_FILE_MAX_TRIES = 3
DEFAULT_CHECK_FILE_DELAY_SECONDS = 2
DEFAULT_TIMEOUT_SECONDS = 60

DEFAULT_PORTS = {
    'ftp': 21, 
    'tftp': 69, 
    'scp': 22, 
    'sftp': 22, 
    'http': 80, 
    'https': 443,
}

class FileUtilsBase(object):
    """ Base class for all FileUtils implementations.

    Based on the 'os' parameter, the appropriate os-specific subclass is
    identified and instantiated.
    """

    @classmethod
    def from_device(cls, device, *args, testbed=None, protocol=None, **kwargs):
        """ Instantiate a fileutils object from a device object.

        Parameters
        ----------
            device : `pyats.topology.device.Device`
                The device against which file client operations are to be
                executed.  This device must have its ``os`` member set.
                If ``device.testbed`` is set, this testbed object is used
                to authenticate file client operations, even if the
                ``testbed`` argument is specified.

            testbed : `pyats.topology.testbed.Testbed`
                The testbed object used to authenticate file client
                operations.  If ``device.testbed`` is set, this parameter,
                even if specified, is ignored.

            protocol : `str`
                Protocol name (ftp, scp, sftp, http, https, tftp)

        """
        testbed = device.testbed if hasattr(device, 'testbed') \
            else testbed

        return cls(
            os=device.os, testbed=testbed, device=device,
            protocol=protocol, *args, **kwargs)

    def __new__(cls, *args, os=None, protocol=None, **kwargs):
        """ Factory that finds and instantiates the correct os-specific
        subclass when a parent class is requested.

        If a child class is requested (``_parent`` is present in kwargs) then
        do not rewrite the class.
        """
        if not kwargs.get('_parent'):
            try:
                # Prepare tokens based on the presence of os and protocol
                tokens = []
                if os:
                    tokens.append(os)
                if protocol:
                    tokens.append(protocol)

                # Initialize Lookup with dynamic tokens and specified packages
                lookup = Lookup(
                    *tokens,
                    packages={'fileutils': filetransferutils,}
                    )
                
                if not os:
                    # Access the default fileutils
                    if protocol:
                        # If only protocol is provided, access lookup.fileutils.protocol.FileUtils
                        protocol_child = getattr(lookup.fileutils.protocols, protocol, None)
                        if not protocol_child:
                            raise Exception(f"Cannot find protocol {protocol} in default fileutils.")
                        new_cls = getattr(protocol_child, 'FileUtils', None)
                        if not new_cls:
                            raise Exception(f"FileUtils class not found for protocol {protocol}.")
                    else:
                        # No `os` or `protocol` - use the default fileutils class
                        new_cls = getattr(lookup.fileutils, 'FileUtils', None)
                        if not new_cls:
                            raise Exception("Default FileUtils class not found in lookup.")
                else:
                    # Access the fileutils plugin
                    fileutils_plugin = lookup.fileutils.plugins

                    # Access the FileUtils class for os
                    os_child = getattr(fileutils_plugin, os, None)
                    if not os_child:
                        raise Exception(f"Error accessing FileUtils class for os {os}.")

                    # Check for protocol only if it's not None
                    if protocol:
                        # Check for protocol child within the os child
                        protocol_child = getattr(os_child, protocol, None)
                        if not protocol_child:
                            raise Exception(f"Cannot find protocol {protocol} within os {os}.")

                    # Access the FileUtils class
                    new_cls = fileutils_plugin.FileUtils

            except Exception as e:
                raise Exception("Cannot find fileutils plugin for os {}.".\
                    format(os))

            try:
                if issubclass(new_cls, cls):
                    cls = new_cls
                else:
                    raise Exception(f"The FileUtils class for os {os} "
                        f"does not inherit from genie.libs.filetransferutils "
                        f"base class.")
            except TypeError:
                raise Exception(f"{new_cls} is the registered fileutils plugin for "
                    "os {os} but is not a class.")


        logger.debug("Instantiating {}class {} from module {}...".\
            format("child " if kwargs.get('_parent') else "",
            cls.__name__, cls.__module__))
        return super().__new__(cls)

    def __enter__(self):
        """ Allows the object to function as a self-closing context manager.
        """
        return self

    def __exit__(self, type, value, traceback):
        """ Allows the object to function as a self-closing context manager.
        """
        self.close()

    def __init__(self, *args, os=None, testbed=None, **kwargs):
        """ Initialize an instance of FileUtils

        Parameters
        ----------
            os : `str`
                The operating system of the device acting as a file transfer
                client.

            testbed : `pyats.topology.Testbed`
                The testbed object that contains auth and address details
                for servers referenced by file transfer URLs.
        """
        self.os = os
        self.testbed = testbed

        # add kwargs to self
        for key, value in kwargs.items():
            setattr(self, key, value)

        # Cache of child objects keyed by abstraction key.
        self.children = dict()

    @property
    def parent(self):
        """ Find the os-specific parent of a protocol-specific plugin. """
        try:
            parent = self._parent
        except AttributeError:
            parent = None

        return parent

    def is_local(self, url):
        """ Returns `True` if the url refers to a local resource. """
        scheme = urlparse(url).scheme
        return (scheme == '' or scheme == 'file')

    def is_remote(self, url):
        """ Returns `True` if the url refers to a remote resource. """
        return not self.is_local(url)

    def get_protocol(self, source, destination=None):
        """ Returns the url scheme (protocol) of either the source or
            destination as long as it is a valid file copy protocol. """
        scheme = urlparse(source).scheme
        if scheme:
            return scheme
        if destination:
            scheme = urlparse(destination).scheme
            return scheme

    def _server_name_number_check(self, server_name_or_ip):
        """Check if server name is just number

        If server name is number

        Returns
        -------
            True, False

        Raises
        ------
            N/A
        """
        # return True if server_name_or_ip is just number
        # because possible to have just module number and show unneeded warning on nxos
        # ex.) 2021-06-16T00:52:53: %UTILS-WARNING: No auth details found in testbed for hostname 1.
        try:
            int(server_name_or_ip)
            return True
        except Exception:
            return False

    def get_server_block(self, server_name_or_ip, protocol=None, device=None):
        """ Return the required server block from the testbed if it exists.

        Parameters
        ----------
            server_name_or_ip : `str`
                The name or IP address of the server
            protocol : `str`
                Protocol to be used during copy process

        Returns
        -------
            `dict` : Server block if found, empty dict if not found.
        """

        # check if server name is number
        is_number = self._server_name_number_check(server_name_or_ip)

        server_block = {}
        server_name_or_ip = '' if server_name_or_ip is None \
            else server_name_or_ip
        try:
            # Fast path : search for server name under testbed/servers
            servers = self.testbed.servers

            server_block = servers.get(server_name_or_ip, {})
            if server_block:
                logger.debug(f'Using server {server_name_or_ip} from testbed')

            if not server_block and protocol:
                # Case when same server is defined with different protocols blocks
                # in the testbed yaml file, we need to get the exact corresponding
                # credentials
                server_block = servers.get(protocol, {})
                if server_block:
                    logger.debug(f'Using server {server_name_or_ip} from testbed')

            # Slow path : search for IP address under servers/<name>/address
            # or server name under servers/<name>/server
            # (as the user may have a server key that differs from the
            # server name).
            if not server_block:
                for server, block in servers.items():
                    block_server = block.get('server', '').casefold()
                    block_name = server.casefold()
                    server_name = server_name_or_ip.casefold()
                    address = block.get('address', '')
                    if (server_name_or_ip == address) or\
                            (isinstance(address, list) and\
                             server_name_or_ip in address) or\
                            (server_name == block_name) or\
                            (server_name == block_server):
                        server_block = block
                        logger.debug(f'Using server {server_name} from testbed')
                        break
                else:
                    msg = "Could not find details in testbed for server {}.".\
                            format(server_name_or_ip)
                    if server_name_or_ip is not None:
                        if is_number:
                            logger.debug(msg)
                        else:
                            logger.warning(msg)
                    else:
                        logger.debug(msg)

            # If no server address try to determine using local address lookup
            if not is_number and not server_block.get('address'):
                local_ip = self.get_local_ip(device)
                if local_ip:
                    server_block['address'] = local_ip
                    logger.debug(f'Using {local_ip} for local server')

        except (TypeError, AttributeError):
            msg = ("Could not find details in testbed for "
                "server {}.".format(server_name_or_ip))
            if server_name_or_ip is not None:
                if is_number:
                    logger.debug(msg)
                else:
                    logger.warning(msg)
            else:
                logger.debug(msg)

        return server_block

    def get_auth(self, server_name_or_ip, protocol=None, device=None):
        """ Get authentication details.

        If credentials

        Returns
        -------
            username, password

            Each element in this tuple is returned as `None` if not found
            in the testbed.

        Raises
        ------
        `Exception`
            if auth details not found in testbed.

        """

        # check if server name is number
        is_number = self._server_name_number_check(server_name_or_ip)

        username = None
        password = None

        if protocol:
            server_block = self.get_server_block(
                server_name_or_ip = server_name_or_ip,
                protocol = protocol,
                device = device)
        else:
            server_block = self.get_server_block(
                server_name_or_ip = server_name_or_ip,
                device = device)

        if server_block:
            try:
                if server_block['credentials']:
                    if not protocol:
                        # this will only work if the abstraction key includes
                        # the protocol, which it currently does not. Only
                        # includes the OS.
                        protocol = getattr(self, 'abstraction_key',
                                           '').split('.')[-1]
                    credential_name = protocol if protocol else DEFAULT_CRED
                    credential = server_block['credentials'][credential_name]
                    username = credential.get('username')
                    password = to_plaintext(credential.get('password'))
                else:
                    # TBD - Remove support for these keys
                    # (which are deprecated as of Jul/2019)
                    # and cause a KeyError to raise here.
                    username = server_block.get('username')
                    password = server_block.get('password')
            except KeyError:
                # TBD - Remove support for these keys
                # (which are deprecated as of Jul/2019)
                # and cause a KeyError to raise here.
                username = server_block.get('username')
                password = server_block.get('password')
        else:
            msg = ("No auth details found in testbed "
                "for hostname {}.".format(server_name_or_ip))
            if server_name_or_ip is not None:
                if is_number:
                    logger.debug(msg)
                else:
                    logger.warning(msg)
            else:
                logger.debug(msg)

        return username, password

    def get_hostname(self, server_name_or_ip, *args, device=None, **kwargs):
        """ Get host name or address to connect to.

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

        # check if server name is number
        is_number = self._server_name_number_check(server_name_or_ip)

        server_block = self.get_server_block(
            server_name_or_ip = server_name_or_ip, device=device)

        if server_block:
            address = server_block.get('address', None)

            if address:
                if type(address) in (tuple, list):
                    # a list of ips were provided - use the first valid one
                    # that we can reach
                    for addr in address:
                        if self.is_valid_ip(addr, *args, **kwargs):
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
                if is_number:
                    logger.debug(msg)
                else:
                    logger.warning(msg)
            else:
                logger.debug(msg)

        # Server block lookup has failed, return originally specified hostname
        # (garbage in, garbage out).
        return server_name_or_ip

    def get_local_ip(self, device):
        """ Try to determine the local IP address by checking the spawn process
        of the device object for connections.

        Arguments:
            device: Device object with spawn attribute

        Returns:
            str (IP address) or None
        """
        if device is None:
            return
        try:
            p = psutil.Process(device.spawn.pid)
            conns = p.connections()
        except Exception:
            conns = None
        if conns:
            conn = conns[0]
            local_ip = conn.laddr[0]
            return local_ip

    def validate_and_update_url(self, url, device=None, **kwargs):
        """Validate the url and replace the hostname/address with a
            reachable address from the testbed"""
        parsed_url = urlparse(url)

        # if there is a host name, this means the address is remote
        if parsed_url.hostname:
            # get hostname to check for valid ip
            hostname = self.get_hostname(
                parsed_url.hostname, device=device, **kwargs)

            # If this remote address has credentials, prepend them to the
            # address
            protocol = self.get_protocol(url)
            username, password = self.get_auth(
                parsed_url.hostname, protocol, device)
            if username and not parsed_url.username:
                if protocol in ['ftp', 'http', 'https']:
                    if password:
                        hostname = '{u}:{p}@{h}'.format(u=username,
                                                        p=password,
                                                        h=hostname)
                elif protocol in ('scp', 'sftp'):
                    hostname = '{u}@{h}'.format(u=username, h=hostname)

            # Append port if it's defined
            server_block = self.get_server_block(
                server_name_or_ip = parsed_url.hostname,
                device = device)
            port = server_block.get('port')
            if port and port != DEFAULT_PORTS[protocol]:
                hostname = '%s:%s' % (hostname, str(port))

            # Make sure we don't replace the protocol when the hostname has the
            # same name eg. ftp://ftp/path/to/file
            if protocol and url.startswith(protocol):
                url = protocol + url[len(protocol):].replace(
                    parsed_url.hostname, hostname, 1)
            else:
                url = url.replace(parsed_url.hostname, hostname, 1)

            return url

        # just return url if it's local
        else:
            return url

    def is_valid_ip(self, ip):
        raise NotImplementedError

    def get_child(self, abstraction_key):
        """Get or create a child FileUtils object under the current OS given a key.

        This method retrieves a cached child object if it exists. If not, it
        dynamically creates a new child object based on the provided abstraction
        key (e.g., protocol) and caches it. If `os` is not provided, it uses
        default logic to determine the appropriate FileUtils object.

        Parameters
        ----------
        abstraction_key : str
            The key used to identify the child FileUtils object (e.g., protocol name).

        Returns
        -------
        FileUtils
            The corresponding child FileUtils object under the current OS plugin.

        Raises
        ------
        Exception
            If the required protocol or FileUtils class cannot be found.
        NotImplementedError
            If the plugin for the given OS does not support the specified key.

        Example
        -------
        >>> from pyats.utils import FileUtils
        >>> fu_linux = FileUtils(os='linux')
        >>> fu_linux_ftp = fu_linux.get_child('ftp')
        >>> assert(fu_linux_ftp.parent is fu_linux)
        """
        # Fast path: Return the child object if it's already cached.
        child_obj = self.children.get(abstraction_key)
        if child_obj:
            return child_obj

        # Slow path: Create a new child object and cache it.
        try:
            tokens = []
            if self.os:
                tokens.append(self.os)
            elif abstraction_key:
                # If `os` is not provided, rely on protocol-specific or default logic
                tokens.append(abstraction_key)

            # Initialize Lookup with dynamic tokens and specified packages
            lookup = Lookup(
                *tokens,
                packages={'fileutils': filetransferutils}
            )

            # Dynamically resolve the appropriate FileUtils plugin
            if self.os:
                # Use OS-specific logic
                child_module = lookup.fileutils.plugins
                if abstraction_key:
                    # Check for protocol-specific child
                    child_module = getattr(child_module, abstraction_key, None)
                    if not child_module:
                        raise Exception(
                            f"Cannot find protocol '{abstraction_key}' within OS '{self.os}'."
                        )
            else:
                # Use default logic when `os` is not provided
                if abstraction_key:
                    # Protocol-specific plugin under the default fileutils
                    child_module = getattr(lookup.fileutils.protocols, abstraction_key, None)
                    if not child_module:
                        raise Exception(
                            f"Cannot find protocol '{abstraction_key}' in default fileutils."
                        )
                else:
                    # Default FileUtils class if no `os` or protocol is provided
                    child_module = getattr(lookup.fileutils, 'FileUtils', None)
                    if not child_module:
                        raise Exception("Default FileUtils class not found in lookup.")

            # Ensure the child_module and FileUtils class exist
            if child_module:
                # Access the FileUtils class
                child_cls = getattr(child_module, 'FileUtils', None)
                if not child_cls:
                    raise Exception(
                        f"Cannot find FileUtils class in module '{child_module}'."
                    )

                # Instantiate the child object
                child_obj = child_cls(
                    os=self.os,
                    testbed=self.testbed,
                    _parent=self
                )

                # Cache the newly created child object
                self.children[abstraction_key] = child_obj
                child_obj.abstraction_key = abstraction_key
            else:
                raise NotImplementedError(
                    f"The fileutils plugin does not provide an implementation "
                    f"for key '{abstraction_key}'."
                )

        except AttributeError as e:
            raise Exception(
                f"Error accessing FileUtils class in module: {e}"
            ) from e

        return child_obj

    def close():
        """ Deallocate any resources being held.  """
        pass

    def remove_child(self, abstraction_key):
        """ Removes a child (protocol-specific) implementation from the cache.

        This method is to be called on the parent (os-specific).

        First, any resources held by the current child are deallocated.

        Then, the current child is removed from the cache so the next call to
        get_child causes a brand new child to be allocated.

        The child is then deleted.
        """
        child = self.get_child(abstraction_key)
        try:
            child.close()
        except Exception as exc:
            logger.warning("Failed to close child {} : {}.".\
                format(abstraction_key, exc))
        finally:
            # Ignore result
            _ = self.children.pop(abstraction_key, None)
            del child

    def checkfile(self, target, max_tries=DEFAULT_CHECK_FILE_MAX_TRIES,
            delay_seconds=DEFAULT_CHECK_FILE_DELAY_SECONDS,
            check_stability=False,
            timeout_seconds=DEFAULT_TIMEOUT_SECONDS, *args, **kwargs):
        """ Check for file existence and (optionally) stability.

        Parameters
        ----------
            target : `str`
                The URL of the file whose details are to be retrieved.

            max_tries : `int`
                Stat is run this many times at maximum

            delay_seconds : `int`
                Delay this many seconds between tries.

            check_stability : `bool`
                If `True`, up to the max possible tries are executed and the
                file length is monitored.  If at least two consecutive equal
                file lengths are seen then the file is deemed stable.

            timeout_seconds : `int`
                The number of seconds for each underlying stat call to wait
                before the stat is considered aborted.
                NOTE: If retries remain, an aborted stat still leads to
                delay/retry and does not necessarily lead to an exception
                being raised.


        Returns
        -------
            `None` if the file check succeeded

        Raises
        ------
        Exception
            check_stability is specified as True but the file
            length is not stable.

        Exception
            timeout exceeded

        """

        prev_file_len = -1
        num_consecutive_equal_length_tries = 0
        result = None
        prev_result = None
        for _try in range(max_tries):
            try:
                result = self.stat(target, timeout_seconds, *args, **kwargs)
            except NotImplementedError:
                raise
            except Exception as exc:
                logger.warning("File stat error : {}".format(exc))
                result = None
                prev_result = None
            else:
                if not check_stability:
                    break
                if prev_result and result.st_size == prev_result.st_size:
                    num_consecutive_equal_length_tries += 1
                else:
                    num_consecutive_equal_length_tries = 1
                prev_result = result

            time.sleep(delay_seconds)

        if not result:
            raise Exception("Failure to check existence and length of "
                "file {}.".format(target))

        if check_stability and num_consecutive_equal_length_tries < 2:
            raise Exception("The length of file {} is not stable.".\
                format(target))

    def copyfile(self, source, destination,
            timeout_seconds, *args, **kwargs):
        """ Copy a single file.

        Copy a single file either from local to remote, or remote to local.
        Remote to remote transfers are not supported.  Users are expected
        to make two calls to this API to do this.

        Parameters
        ----------
            source : `str`
                The URL of the file to be copied from.

            destination : `str`
                The URL of the file name to be copied to.

            timeout_seconds : `int`
                Maximum allowed amount of time for the operation.

        Raises
        ------
        Exception
            When a remote to remote transfer is requested.

        """
        raise NotImplementedError("The fileutils module {} "
            "does not implement copyfile.".format(self.__module__))

    def dir(self, target, timeout_seconds, *args, **kwargs):
        """ Retrieve filenames contained in a directory.

        Do not recurse into subdirectories, only list files at the top level
        of the given directory.

        Parameters
        ----------
            target : `str`
                The URL of the directory whose contained files are to be
                retrieved.

            timeout_seconds : `int`
                The number of seconds to wait before aborting the operation.

        Returns
        -------
            `list` : List of filename URLs.  Directory names are ignored.

        """
        raise NotImplementedError("The fileutils module {} "
            "does not implement dir.".format(self.__module__))

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
        Exception
            timeout exceeded

        Exception
            File was not found

        """

        raise NotImplementedError("The fileutils module {} "
            "does not implement stat.".format(self.__module__))

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

        raise NotImplementedError("The fileutils module {} "
            "does not implement chmod.".format(self.__module__))

    def deletefile(self, target, timeout_seconds, *args, **kwargs):
        """ Delete a file

        Parameters
        ----------
            target : `str`
                The URL of the file to be deleted.

            timeout_seconds : `int`
                Maximum allowed amount of time for the operation.

        """

        raise NotImplementedError("The fileutils module {} "
            "does not implement deletefile.".format(self.__module__))

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

        raise NotImplementedError("The fileutils module {} "
            "does not implement renamefile.".format(self.__module__))

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
            try:
                # only include address, no port or credentials
                used_server = str(ipaddress.ip_address(parsed.hostname))
                break
            except Exception:
                if parsed.hostname:
                    used_server = parsed.hostname

        if not used_server:
            # If both URLS have no valid IP addres, raise an exception
            raise Exception("No valid server address or hostname has been detected in the "
                "passed URLS '{from_URL}' & '{to_URL}'".format(
                    from_URL=source, to_URL=destination))

        return used_server

