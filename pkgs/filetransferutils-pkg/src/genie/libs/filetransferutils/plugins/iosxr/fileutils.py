""" File utils base class for IOSXR devices. """

import logging
import ipaddress
# Parent inheritance
from .. import FileUtils as FileUtilsDeviceBase
from urllib.parse import urlparse

# Dir parser
try:
    from genie.libs.parser.iosxr.show_platform import Dir
except ImportError:
    # For apidoc building only
    from unittest.mock import Mock
    Dir = Mock()

# Unicon
from unicon.core.errors import SubCommandFailure

DEFAULT_PORTS = {'ftp': 21, 'tftp': 69, 'scp': 22, 'sftp': 22, 'http': 80}
logger = logging.getLogger(__name__)


def _same_next_hop(first, second):
    """ Return True when two next-hop values name the same address.

        Testbed-declared next hops and gateways are free-form strings that
        may carry a prefix length or differ in IPv6 formatting
        (``2001:db8:1::1`` vs ``2001:0db8:1::1``), so compare parsed
        addresses rather than raw text. Values that do not parse fall back
        to a plain string comparison.
    """
    if not first or not second:
        return False
    first_value = str(first).split('/')[0]
    second_value = str(second).split('/')[0]
    try:
        return (ipaddress.ip_address(first_value)
                == ipaddress.ip_address(second_value))
    except ValueError:
        return first_value == second_value


class FileUtils(FileUtilsDeviceBase):

    def copyfile(self,
                 source,
                 destination,
                 timeout_seconds=300,
                 vrf=None,
                 cmd=None,
                 *args,
                 **kwargs):
        """ Copy a file to/from IOSXR device

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
                cmd: `str`
                    Optional command to use for copying
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

                # Instanciate a filetransferutils instance for IOSXR device
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

        # Extract the server address BEFORE route rewrite so that
        # auth/cert lookups use the original (automation-reachable) hostname
        used_server = self.get_server(source, destination)

        # Rewrite URL hostname using server route lookup if applicable
        source = self._resolve_server_route_url(source, device=device)
        destination = self._resolve_server_route_url(destination, device=device)
        ssh_protocol = {'sftp'}

        # Build copy command if not provided
        if not cmd:
            protocol = self.get_protocol(source) or self.get_protocol(destination)
            s = source.replace(f'{protocol}://', '').replace('//', ':/')
            d = destination.replace(f'{protocol}://', '').replace('//', ':/')

            if protocol in ssh_protocol:
                cmd = f"{protocol} {s} {d}" + (f" vrf {vrf}" if vrf else "")
            else:
                cmd = f"copy {source} {destination}" + (f" vrf {vrf}" if vrf else "")

        return super().copyfile(source=source,
                         destination=destination,
                         timeout_seconds=timeout_seconds,
                         cmd=cmd,
                         used_server=used_server,
                         vrf=vrf,
                         *args,
                         **kwargs)

    def _get_transfer_endpoint_ip(self, source, destination):
        """ Return the remote host of a transfer, or None when neither side
            is a routable remote endpoint.

            A route is only ever needed for an endpoint that resolves to a
            routable IP address. Device-local paths (``disk0:``,
            ``harddisk:``, ``running-config`` ...) never produce a hostname
            when parsed, and DNS names cannot be turned into a host route,
            so both are skipped.
        """
        for location in (source, destination):
            if not location:
                continue
            hostname = urlparse(str(location)).hostname
            if not hostname:
                # Device-local path such as 'disk0:/image.bin'.
                continue
            try:
                ipaddress.ip_address(hostname)
            except ValueError:
                logger.debug(
                    'Temporary transfer route: transfer endpoint %r is not an '
                    'IP address, skipping route installation', hostname)
                continue
            return hostname
        return None

    def _get_management_gateway(self, device, address_family):
        """ Return the configured management gateway for an address family.

            Never infers a gateway: when the testbed does not declare one,
            None is returned and no route is installed.
        """
        management = getattr(device, 'management', None) or {}
        gateway = management.get('gateway', {}) if hasattr(
            management, 'get') else getattr(management, 'gateway', {})
        if not gateway:
            return None
        addresses = gateway.get(address_family) if hasattr(
            gateway, 'get') else getattr(gateway, address_family, None)
        if not addresses:
            return None
        if not isinstance(addresses, (list, tuple, set)):
            addresses = [addresses]
        for address in addresses:
            if not address:
                continue
            value = str(address).split('/')[0]
            try:
                ipaddress.ip_address(value)
            except ValueError:
                continue
            return value
        return None

    @staticmethod
    def _management_value(container, key):
        """ Read ``key`` from a testbed management container.

            The management block may arrive as a plain dict or as an
            attribute-style object depending on how the testbed was loaded.
        """
        if container is None:
            return None
        if hasattr(container, 'get'):
            return container.get(key)
        return getattr(container, key, None)

    def _get_management_routes(self, device, address_family):
        """ Return the routes declared under ``device.management.routes``
            for an address family, as a list.

            Returns an empty list when the testbed declares none.
        """
        management = getattr(device, 'management', None)
        routes = self._management_value(management, 'routes')
        if not routes:
            return []
        entries = self._management_value(routes, address_family)
        if not entries:
            return []
        if not isinstance(entries, (list, tuple)):
            entries = [entries]
        return list(entries)

    def _get_declared_route_next_hop(self, device, endpoint, address_family):
        """ Return the next hop of the declared management route covering the
            endpoint, or None when the testbed declares no covering route.

            When several declared routes cover the endpoint the most
            specific one wins, matching how the device itself resolves a
            destination. Testbed ``routes`` lists are written in arbitrary
            order, so a first-match scan could otherwise answer with a
            broad route (``0.0.0.0/0``) while the device would actually
            follow a longer prefix listed after it.

            The pyATS device-management schema spells the key ``next-hop``;
            a normalised testbed may expose it as ``next_hop``. Both are
            accepted.

            This reports *which* next hop the testbed declares; it does not
            decide whether that next hop is the one the transfer needs.
            Callers must compare the returned value against the gateway they
            are trying to reach - a covering route via some other next hop
            is not evidence of reachability via the management gateway.
        """
        try:
            address = ipaddress.ip_address(endpoint)
        except ValueError:
            return None

        best_prefix_length = -1
        best_next_hop = None
        for entry in self._get_management_routes(device, address_family):
            subnet = (self._management_value(entry, 'subnet')
                      or self._management_value(entry, 'prefix'))
            next_hop = (self._management_value(entry, 'next-hop')
                        or self._management_value(entry, 'next_hop'))
            if not subnet or not next_hop:
                continue
            try:
                network = ipaddress.ip_network(str(subnet), strict=False)
            except ValueError:
                logger.debug('Temporary transfer route: ignoring malformed '
                             'management route subnet %r on %s', subnet,
                             device.name)
                continue
            if network.version != address.version:
                continue
            if address not in network:
                continue
            # Longest prefix wins, as it would on the device. A strict
            # comparison keeps the first entry when two declared routes
            # share a prefix length, so equally specific duplicates
            # resolve in testbed order rather than arbitrarily.
            if network.prefixlen > best_prefix_length:
                best_prefix_length = network.prefixlen
                best_next_hop = str(next_hop)
        return best_next_hop

    def _ensure_temporary_transfer_route(self, device=None, **kwargs):
        """ Install a temporary host route towards the transfer endpoint.

            The route exists only for the duration of the file transfer: it
            is configured before the transfer starts and removed again by
            :meth:`_remove_temporary_transfer_route` during cleanup.

            This is evaluated automatically for every IOS-XR transfer; there
            is no opt-in flag. The route is installed when *all* of the
            following hold:

            * the transfer endpoint is a remote IP address
            * a management gateway is declared in the testbed
            * the route lookup completed, so reachability is known
            * the device does not already reach the endpoint via that gateway
            * no ``device.management.routes`` entry already covers the
              endpoint *via that same gateway*; a declared route via any
              other next hop does not establish reachability through the
              gateway and so does not suppress installation

            Nothing is configured when reachability could not be determined:
            a failed lookup is never treated as a missing route.

            The route is installed in the VRF used by the transfer. When no
            ``vrf`` is supplied the default VRF is used, matching how the
            rest of the file transfer configuration interprets ``vrf=None``.

            Returns a dict describing the installed route (used for cleanup)
            or None when nothing was configured.

            When the configuration call fails it may still have applied the
            route before erroring, so an exact removal is attempted before
            returning None. The transfer then continues regardless: a
            missing temporary route is not by itself fatal.
        """
        device = device or getattr(self, 'device', None)
        if device is None:
            return None
        device = getattr(device, 'device', device)

        # An absent vrf means the transfer uses the default VRF; the route
        # belongs in that same table. This is not an inference - the default
        # routing table is where a vrf-less transfer is routed.
        vrf = kwargs.get('vrf')

        endpoint = self._get_transfer_endpoint_ip(kwargs.get('source'),
                                                  kwargs.get('destination'))
        if not endpoint:
            return None

        try:
            address = ipaddress.ip_address(endpoint)
        except ValueError:
            return None
        address_family = 'ipv6' if address.version == 6 else 'ipv4'
        prefix = f'{endpoint}/{128 if address.version == 6 else 32}'

        gateway = self._get_management_gateway(device, address_family)
        if not gateway:
            logger.info('Temporary transfer route: no %s management gateway '
                        'declared for %s, skipping route installation',
                        address_family, device.name)
            return None

        logger.info('Temporary transfer route: evaluating endpoint %s '
                    '(prefix %s, vrf %s, %s) against gateway %s on %s',
                    endpoint, prefix, vrf,
                    address_family, gateway, device.name)

        try:
            existing = device.api.get_routing_route_next_hop(
                route=endpoint, address_family=address_family, vrf=vrf)
        except Exception:
            # The lookup did not complete, so reachability is unknown.
            # Installing a route on a guess could black-hole traffic, so
            # leave the routing table untouched.
            logger.warning('Temporary transfer route: failed to look up route '
                           'for %s on %s, reachability is unknown, skipping '
                           'route installation',
                           endpoint, device.name, exc_info=True)
            return None

        # Log the raw lookup result: an empty/None result or a next-hop list
        # that does not name the gateway is what drives the decision below,
        # so record it verbatim to make that decision auditable.
        logger.info('Temporary transfer route: route lookup for %s on %s '
                    'returned %r', endpoint, device.name, existing)

        # Compare the live next hops through _same_next_hop rather than by
        # raw string membership: the device renders addresses in its own
        # canonical form, so a next hop reported as '2001:db8:1::1' must
        # still match a testbed gateway written as '2001:0db8:1:0::1'.
        # Raw membership would miss that and install a redundant host route
        # over a path that already uses the gateway.
        if existing and any(
                _same_next_hop(next_hop, gateway)
                for next_hop in (existing.get('next_hops') or [])):
            logger.info('Temporary transfer route: %s already reachable via '
                        '%s on %s, nothing to configure', endpoint, gateway,
                        device.name)
            return None

        # The testbed may declare the path itself under
        # ``device.management.routes``. That only settles the question when
        # the declared next hop *is* the management gateway we are trying to
        # use: the contract of this method is to guarantee reachability via
        # that gateway, so a covering route pointing somewhere else says
        # nothing about it and must not suppress the temporary route.
        declared_next_hop = self._get_declared_route_next_hop(
            device, endpoint, address_family)
        if _same_next_hop(declared_next_hop, gateway):
            logger.info('Temporary transfer route: %s is covered by a '
                        'declared management route via gateway %s on %s, '
                        'nothing to configure', endpoint, declared_next_hop,
                        device.name)
            return None
        if declared_next_hop:
            logger.info('Temporary transfer route: %s is covered by a '
                        'declared management route via %s on %s, but that is '
                        'not the management gateway %s this transfer uses, '
                        'so it does not establish reachability via the '
                        'gateway; continuing with route installation',
                        endpoint, declared_next_hop, device.name, gateway)

        if not existing:
            logger.info('Temporary transfer route: no usable route '
                        'information for %s on %s, installing %s', endpoint,
                        device.name, prefix)
        else:
            logger.info('Temporary transfer route: %s is reachable via %s on '
                        '%s but not via gateway %s (covering route %r), '
                        'installing %s',
                        endpoint, existing.get('next_hops') or
                        existing.get('outgoing_interfaces'), device.name,
                        gateway, existing.get('route'), prefix)

        # Build the cleanup record *before* touching the device.
        # ``configure_static_routing_route`` can fail after the route has
        # already been applied (for example when a later line of the
        # configuration session is rejected), so the record needed to undo
        # it must exist independently of the call succeeding.
        temporary_route = {
            'prefix': prefix,
            'next_hop': gateway,
            'address_family': address_family,
            'vrf': vrf,
        }

        try:
            device.api.configure_static_routing_route(
                prefix=prefix,
                next_hop=gateway,
                address_family=address_family,
                vrf=vrf)
        except Exception:
            logger.warning('Temporary transfer route: failed to configure %s '
                           'via %s (vrf %s, %s) on %s, attempting to remove '
                           'any partially applied route before continuing '
                           'with the transfer',
                           prefix, gateway, vrf, address_family, device.name,
                           exc_info=True)
            # The failure may have left the route installed. Removing a
            # route that was never applied is harmless - the removal is
            # exact (same prefix, next hop, family and vrf) and its own
            # failure is logged rather than raised - whereas leaving a
            # partially applied route behind would outlive the transfer.
            self._remove_temporary_transfer_route(device, temporary_route)
            return None

        logger.info('Temporary transfer route: configured %s via %s (vrf %s, '
                    '%s) on %s',
                    prefix, gateway, vrf, address_family, device.name)
        return temporary_route

    def _remove_temporary_transfer_route(self, device, temporary_route):
        """ Remove only the route installed by
            :meth:`_ensure_temporary_transfer_route`.
        """
        if not temporary_route:
            return None
        device = getattr(device, 'device', device)
        try:
            device.api.unconfigure_static_routing_route(
                prefix=temporary_route['prefix'],
                next_hop=temporary_route['next_hop'],
                address_family=temporary_route['address_family'],
                vrf=temporary_route['vrf'])
        except Exception:
            logger.warning('Temporary transfer route: failed to remove %s via '
                           '%s (vrf %s, %s) on %s', temporary_route['prefix'],
                           temporary_route['next_hop'], temporary_route['vrf'],
                           temporary_route['address_family'], device.name,
                           exc_info=True)
            return None
        logger.info('Temporary transfer route: removed %s via %s (vrf %s, %s) '
                    'on %s',
                    temporary_route['prefix'], temporary_route['next_hop'],
                    temporary_route['vrf'],
                    temporary_route['address_family'],
                    device.name)
        return temporary_route

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

                # Instanciate a filetransferutils instance for IOSXR device
                >>> fu_device = FileUtils.from_device(device)

                # list all files on the device directory 'disk0:'
                >>> directory_output = fu_device.dir(target='disk0:',
                ...     timeout_seconds=300, device=device)

                >>> directory_output

                ['disk0:/lost+found', 'disk0:/ztp', 'disk0:/core',
                 'disk0:/envoke_log', 'disk0:/cvac', 'disk0:/cvac.log',
                 'disk0:/clihistory', 'disk0:/config -> /misc/config',
                 'disk0:/status_file', 'disk0:/kim', 'disk0:/pnet_cfg.log',
                 'disk0:/nvgen_traces', 'disk0:/oor_aware_process',
                 'disk0:/.python-history']

        """

        dir_output = super().parsed_dir(target, timeout_seconds, Dir, *args,
                                        **kwargs)

        # Extract the files location requested
        output = self.parse_url(target)

        # Construct the directory name
        directory = output.scheme + ":/"

        # Create a new list to return
        return [directory + key for key in dir_output['dir']['files']]

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

                # Instanciate a filetransferutils instance for IOSXR device
                >>> fu_device = FileUtils.from_device(device)

                # list the file details on the device 'flash:' directory
                >>> directory_output = fu_device.stat(target='flash:memleak.tcl',
                ...     timeout_seconds=300, device=device)

                >>> directory_output['size']
                >>> directory_output['permissions']

                (Pdb) directory_output
                {'index': '14', 'date': 'Mar 28 12:23',
                 'permission': '-rw-r--r--', 'size': '10429'}

        """

        files = super().stat(target, timeout_seconds, Dir, *args, **kwargs)

        # Extract the file name requested
        output = self.parse_url(target)
        directory = output.scheme + ":/"
        return files['dir']['files'][output.path]

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

                # Instanciate a filetransferutils instance for IOSXR device
                >>> fu_device = FileUtils.from_device(device)

                # delete a specific file on device directory 'disk0:'
                >>> directory_output = fu_device.deletefile(
                ...     target='disk0:memleak_bckp.tcl',
                ...     timeout_seconds=300, device=device)

        """

        super().deletefile(target, timeout_seconds, *args, **kwargs)

    def renamefile(self,
                   source,
                   destination,
                   timeout_seconds=300,
                   *args,
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

                # Instanciate a filetransferutils instance for IOSXR device
                >>> fu_device = FileUtils.from_device(device)

                # rename the file on the device 'flash:' directory
                >>> fu_device.renamefile(target='flash:memleak.tcl',
                ...     destination='memleak_backup.tcl'
                ...     timeout_seconds=300, device=device)

        """

        raise NotImplementedError("The fileutils module {} "
                                  "does not implement renamefile.".format(
                                      self.__module__))

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
                                  "does not implement chmod.".format(
                                      self.__module__))

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
        # show clock | file ftp://10.1.6.242//auto/tftp-ssr/show_clock
        cmd = "show clock | file {e}".format(e=target)

        super().validateserver(cmd=cmd,
                               target=target,
                               timeout_seconds=timeout_seconds,
                               used_server=used_server,
                               *args,
                               **kwargs)

    def copyconfiguration(self,
                          source,
                          destination,
                          timeout_seconds=300,
                          vrf=None,
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
                ...     source='startup-configuration',
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

        super().copyconfiguration(source=source,
                                  destination=destination,
                                  timeout_seconds=timeout_seconds,
                                  cmd=cmd,
                                  used_server=used_server,
                                  *args,
                                  **kwargs)

    def send_cli_to_device(self,
                           cli,
                           used_server=None,
                           invalid=None,
                           timeout_seconds=300,
                           **kwargs):

        output = super().send_cli_to_device(cli=cli,
                                            used_server=used_server,
                                            invalid=invalid,
                                            timeout_seconds=timeout_seconds,
                                            **kwargs)
        return output


    def validate_and_update_url(self, url, device=None, **kwargs ):
        """Validate the url and replace the hostname/address with a
        reachable address from the testbed"""
        parsed_url = urlparse(url)
        protocol = self.get_protocol(url)
        if protocol != 'ftp':
            return super().validate_and_update_url(url, device=device, **kwargs)
        if hasattr(device,'version') and device.version:
           version = device.version
        else: 
            try:
                out = device.parse('show version')
            except Exception as e:
                logger.error(f'Could not copy file because of {e}')
                raise e
            version = out.get('software_version')
        if version and int(version.split('.')[0]) >= 7:
            # if there is a host name, this means the address is remote
            if parsed_url.hostname:
                # get hostname to check for valid ip
                hostname = self.get_hostname(parsed_url.hostname, device=device, **kwargs)
                    
                # Append port if it's defined
                server_block = self.get_server_block(
                server_name_or_ip = parsed_url.hostname, device = device)
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
        else:
            return super().validate_and_update_url(url, device=None, **kwargs)