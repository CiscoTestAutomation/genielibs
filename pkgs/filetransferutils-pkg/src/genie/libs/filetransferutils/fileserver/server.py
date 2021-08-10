import importlib
import logging
import multiprocessing
import queue
import socket
import random

import netaddr
import psutil
from pyats import configuration as cfg
from pyats.datastructures import AttrDict
from pyats.utils.dicts import recursive_update

logger = logging.getLogger(__name__)

process = multiprocessing.get_context('fork')

FILETRANSFER_SUBNET_CFG = 'filetransfer.subnet'

TIMEOUT_DEFAULT = 10

ALPHA = 'abcdefghijklmnopqrstuvwxyz'
ALPHA = ALPHA + ALPHA.upper() + '0123456789'

class FileServer:
    def __new__(cls, *args, **kwargs):
        '''Retrieve specific protocol of FileServer
        '''
        factory_cls = cls

        # Get class specific to protocol
        if factory_cls is FileServer:
            protocol = kwargs.get('protocol', '').lower()
            if not protocol:
                raise TypeError('No protocol specified')

            try:
                mod = 'genie.libs.filetransferutils.fileserver.protocols.%s' \
                    % protocol
                protocol_mod = importlib.import_module(mod)
                factory_cls = protocol_mod.FileServer
            except (ImportError, AttributeError) as e:
                raise TypeError('File server protocol %s not found!' %
                                str(protocol))

        # Init new class
        if factory_cls is not cls:
            self = factory_cls.__new__(factory_cls, *args, **kwargs)
        elif super().__new__ is object.__new__:
            self = super().__new__(factory_cls)
            self.__init__(*args, **kwargs)
        else:
            self = super().__new__(factory_cls, *args, **kwargs)

        return self

    def __init__(self, **kwargs):
        self.server_info = {}
        self.timeout = kwargs.pop('timeout', TIMEOUT_DEFAULT)
        self.server_info.update(kwargs)

        if 'subnet' not in self.server_info:
            if 'address' in self.server_info:
                # Can use the address as the subnet if given (with netmask /32)
                self.server_info['subnet'] = self.server_info['address']
            else:
                # Otherwise try looking in the pyats configuration
                self.server_info['subnet'] = cfg.get(FILETRANSFER_SUBNET_CFG)

        # Ensure FileServer has a subnet
        if not self.server_info.get('subnet'):
            raise TypeError('FileServer missing subnet')

        # Get specific ip from subnet
        self.server_info['address'] = self._get_ip(self.server_info['subnet'])

        # Extract name if provided
        self.name = None
        if 'name' in self.server_info:
            self.name = self.server_info.pop('name')

        # Extract testbed if provided
        self.testbed = None
        if 'testbed' in self.server_info:
            self.testbed = self.server_info.pop('testbed')

        # Extract synchro if provided to reduce number of file handles
        self.synchro = None
        if 'synchro' in self.server_info:
            self.synchro = self.server_info.pop('synchro')

    def __enter__(self):

        # Start server, usually by spawning a process and get new info
        info = self.start_server()
        recursive_update(self.server_info, info)

        # Verify server is successfully running using a client
        try:
            self.verify_server()
        except Exception as e:
            self.stop_server()
            raise OSError('Failed to verify %s' % str(type(self))) from e

        # Log address of server
        address = self.server_info['address']
        port = self.server_info.get('port')
        if port:
            address += ':%s' % port
        logger.info('%s File Server started on %s' %
                    (self.protocol.upper(), address))

        # Update testbed with new server info
        if self.testbed is not None and self.name:
            recursive_update(
                self.testbed.servers.setdefault(self.name, AttrDict()),
                self.server_info)

        return self.server_info

    def __exit__(self, type_=None, val=None, tb=None):
        self.stop_server()
        # Remove from testbed
        if self.testbed and self.name:
            self.testbed.servers.pop(self.name)


    def __del__(self):
        self.stop_server()

    def _get_ip(self, subnet, netmask=None):
        # convert subnet into an IPNetwork object
        subnet = netaddr.IPNetwork(subnet)
        if netmask:
            subnet.netmask = netmask

        valid_ips = []
        # Check the IP addresses of all interfaces to find the ones that match
        # the given subnet
        interfaces = psutil.net_if_addrs()
        for iname, iface in interfaces.items():
            for snic in iface:
                if snic.family == socket.AF_INET:
                    ip = netaddr.IPAddress(snic.address)
                    if ip in subnet:
                        valid_ips.append(snic.address)

        # Must have exactly one match
        if len(valid_ips) == 0:
            raise TypeError('No valid IP for subnet %s' % (subnet))
        elif len(valid_ips) > 1:
            raise TypeError('More than one valid IP for subnet %s.\n%s\nTry a '
                            'more specific subnet.' %
                            (subnet, '\n'.join(valid_ips)))
        return valid_ips[0]

    def start_server(self):
        # Start server
        if self.synchro:
            # start queue from given multiprocessing manager to reduce number of
            # file handles
            self.queue = self.synchro.Queue()
        else:
            # No multiprocessing manager, make a queue
            self.queue = multiprocessing.Queue()
        self.server_proc = process.Process(target=self.run_server)
        self.server_proc.start()

        # Wait for queue to ensure the server is running
        try:
            info = self.queue.get(True, self.timeout)
        except queue.Empty:
            self.stop_server()
            raise Exception('%s server did not start after %s seconds' %
                            (self.protocol.upper(), self.timeout))
        return info

    def run_server(self):
        # method to be run as a forked process
        raise NotImplementedError

    def verify_server(self):
        raise NotImplementedError

    def stop_server(self):
        # Use getattr because not all protocols start a process
        if getattr(self, 'server_proc', None):
            self.server_proc.terminate()
            self.server_proc.join()
            self.server_proc = None

    def _generate_credential(self):
        # Generate a random string to use as credentials if none are given
        return ''.join([random.choice(ALPHA) for x in range(10)])
