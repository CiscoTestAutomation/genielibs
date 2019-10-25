'''
    Interface classes for iosxe OS.
'''

__all__ = (
    'Interface',
    'PhysicalInterface',
    'VirtualInterface',
    'LoopbackInterface',
    'EthernetInterface'
)

import re
import contextlib
import abc
import weakref
import string
from enum import Enum

from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase
from genie.conf.base.exceptions import UnknownInterfaceTypeError
from genie.conf.base.attributes import SubAttributes, KeyedSubAttributes, SubAttributesDict,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import YangConfig

from genie.libs.conf.base import \
    MAC, \
    IPv4Address, IPv4Interface, \
    IPv6Address, IPv6Interface

from genie.libs.conf.l2vpn import PseudowireNeighbor
from genie.libs.conf.l2vpn.pseudowire import EncapsulationType

import genie.libs.conf.interface

try:
    from ydk.models.ned import ned
    from ydk.types import DELETE, Empty
    from ydk.services import CRUDService
    from ydk.services import CodecService
    from ydk.providers import CodecServiceProvider
    # patch a netconf provider
    from ydk.providers import NetconfServiceProvider as _NetconfServiceProvider

    from ydk.providers._provider_plugin import _ClientSPPlugin

    class NetconfServiceProvider(_NetconfServiceProvider):

        def __init__(self, device):

            if 'yang' not in device.mapping:
                # Want it, but dont have a connection?
                raise Exception("Missing connection of "
                                "type 'yang' in the device "
                                "mapping '{map}'".format(map=device.mapping))
            alias = device.mapping['yang']
            dev = device.connectionmgr.connections[alias]

            super().__init__(address=str(dev.connection_info.ip),
                             port=dev.connection_info.port,
                             username=dev.connection_info.username,
                             password=dev.connection_info.password,
                             protocol = 'ssh')

            self.sp_instance = _ClientSPPlugin(self.timeout,
                                               use_native_client=False)

            self.sp_instance._nc_manager = dev

        def _connect(self, *args, **kwargs): pass
except Exception:
    pass

class ConfigurableInterfaceNamespace(ConfigurableBase):

    def __init__(self, interface=None):
        assert interface
        self._interface = interface

    _interface = None

    @property
    def interface(self):
        return self._interface

    @property
    def testbed(self):
        return self.interface.testbed

    @property
    def device(self):
        return self.interface.device


class Interface(genie.libs.conf.interface.Interface):
    """ base Interface class for IOS-XE devices
    """

    def __new__(cls, *args, **kwargs):

        factory_cls = cls
        if cls is Interface:
            try:
                name = kwargs['name']
            except KeyError:
                raise TypeError('\'name\' argument missing')
            d_parsed = genie.libs.conf.interface.ParsedInterfaceName(
                name, kwargs.get('device', None))
            try:
                factory_cls = cls._name_to_class_map[d_parsed.type]
            except KeyError:
                pass

        if factory_cls is not cls:
            self = factory_cls.__new__(factory_cls, *args, **kwargs)
        elif super().__new__ is object.__new__:
            self = super().__new__(factory_cls)
        else:
            self = super().__new__(factory_cls, *args, **kwargs)
        return self

    bandwidth = managedattribute(
        name='bandwidth',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    description = managedattribute(
        name='description',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    mtu = managedattribute(
        name='mtu',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    shutdown = managedattribute(
        name='shutdown',
        default=False,
        type=(None, managedattribute.test_istype(bool)))

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        assert not kwargs
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        with self._build_config_create_interface_submode_context(configurations):
            self._build_config_interface_submode(configurations=configurations, attributes=attributes, unconfig=unconfig)

        if apply:
            if configurations:
                self.device.configure(configurations, fail_invalid=True)
        else:
            return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply,
                                 attributes=attributes,
                                 unconfig=True, **kwargs)

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class PhysicalInterface(Interface, genie.libs.conf.interface.PhysicalInterface):

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VirtualInterface(Interface, genie.libs.conf.interface.VirtualInterface):

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LoopbackInterface(VirtualInterface, genie.libs.conf.interface.LoopbackInterface):

    _interface_name_types = (
        'Loopback',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)
        ydk_obj = ned.Native.Interface.Loopback()
        # name is a mandatory arguments
        keep = string.digits
        ydk_obj.name =  int(''.join(i for i in attributes.value('name') if i in keep))

        if unconfig and attributes.iswildcard:
            pass
        else:
            ipv4 = attributes.value('ipv4')
            if ipv4:
                ydk_obj.ip.address.primary.address = str(ipv4.ip)
                ydk_obj.ip.address.primary.mask = str(ipv4.netmask)

            vrf = attributes.value('vrf')
            if vrf:
                ydk_obj.vrf.forwarding = vrf.name
        # instantiate crud service
        crud_service = CRUDService()
        if apply:

            # create netconf connection
            ncp = NetconfServiceProvider(self.device)


            if unconfig:
                crud_service.delete(ncp, ydk_obj)
            else:
                crud_service.create(ncp, ydk_obj)
        else:
            if unconfig:
                return YangConfig(device=self.device, unconfig=unconfig,
                                  ncp=NetconfServiceProvider,
                                  ydk_obj=ydk_obj,
                                  crud_service=crud_service.delete)
            else:
                return YangConfig(device=self.device, unconfig=unconfig,
                                  ncp=NetconfServiceProvider,
                                  ydk_obj=ydk_obj,
                                  crud_service=crud_service.create)

class EthernetInterface(PhysicalInterface, genie.libs.conf.interface.EthernetInterface):

    _interface_name_types = (
        'Ethernet',  # TODO verify
        'FastEthernet',
        # TODO more?
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)
        ydk_obj = ned.Native.Interface.Gigabitethernet()
        ydk_obj.name = self.name
        if unconfig and attributes.iswildcard:
            ydk_obj = DELETE()
        else:
            shutdown = attributes.value('shutdown')
            if shutdown is not None:
                if unconfig:
                    # Special case: unconfiguring always applies shutdown
                    ydk_obj.shutdown = Empty()
                elif shutdown:
                    ydk_obj.shutdown = Empty()
                else:
                    ydk_obj.shutdown = DELETE()

            ipv4 = attributes.value('ipv4')
            if ipv4:
                ydk_obj.ip.address.primary.address = str(ipv4.ip)
                ydk_obj.ip.address.primary.mask = str(ipv4.netmask)

            vrf = attributes.value('vrf')
            if vrf:
                ydk_obj.vrf.forwarding = vrf.name

        # instantiate crud service
        crud_service = CRUDService()
        if apply:

            # create netconf connection
            ncp = NetconfServiceProvider(self.device)

            return crud_service.create(ncp, ydk_obj)
        else:
            return YangConfig(device=self.device, unconfig=unconfig,
                              ncp=NetconfServiceProvider,
                              ydk_obj=ydk_obj,
                              crud_service=crud_service.create)

class GigabitEthernetInterface(PhysicalInterface):

    _interface_name_types = (
        'GigabitEthernet',
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)
        ydk_obj = ned.Native.Interface.Gigabitethernet()
        keep = string.digits + '//'
        ydk_obj.name =  ''.join(i for i in attributes.value('name') if i in keep)

        shutdown = attributes.value('shutdown')
        if shutdown is not None:
            if unconfig:
                # Special case: unconfiguring always applies shutdown
                ydk_obj.shutdown = Empty()
            elif shutdown:
                ydk_obj.shutdown = Empty()
            else:
                ydk_obj.shutdown = DELETE()

        ipv4 = attributes.value('ipv4')
        if ipv4:
            if unconfig:
                ydk_obj.ip.address.primary.address = DELETE()
                ydk_obj.ip.address.primary.mask = DELETE()
            else:
                ydk_obj.ip.address.primary.address = str(ipv4.ip)
                ydk_obj.ip.address.primary.mask = str(ipv4.netmask)

        vrf = attributes.value('vrf')
        if vrf:
            if unconfig:
                ydk_obj.vrf.forwarding = DELETE()
            else:
                ydk_obj.vrf.forwarding = vrf.name

        # instantiate crud service
        crud_service = CRUDService()

        if apply:

            # create netconf connection
            ncp = NetconfServiceProvider(self.device)

            crud_service.create(ncp, ydk_obj)
        else:
            return YangConfig(device=self.device,
                              ydk_obj=ydk_obj,
                              ncp=NetconfServiceProvider,
                              crud_service=crud_service.create)

Interface._build_name_to_class_map()

