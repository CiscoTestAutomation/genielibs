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
    from ydk.models.ydkmodels import Cisco_IOS_XR_ifmgr_cfg as xr_ifmgr_cfg
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
        default=None,
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
        interface_configurations = xr_ifmgr_cfg.InterfaceConfigurations()
        interface_configuration = interface_configurations.InterfaceConfiguration()
        interface_configuration.active = "act"
        interface_configuration.interface_name = attributes.value('name')
        interface_configuration.interface_virtual = Empty()
        # name is a mandatory arguments
        #keep = string.digits
        #ydk_obj.name =  int(''.join(i for i in attributes.value('name') if i in keep))

        if unconfig and attributes.iswildcard:
            pass
        else:
            vrf = attributes.value('vrf')
            if vrf:
                interface_configuration.vrf = vrf.name
            
            ipv4 = attributes.value('ipv4')
            if ipv4:
                primary = interface_configuration.ipv4_network.addresses.Primary()
                primary.address = str(ipv4.ip)
                primary.netmask = str(ipv4.netmask)
                interface_configuration.ipv4_network.addresses.primary = primary
        # instantiate crud service
        crud_service = CRUDService()
        if apply:

            # create netconf connection
            ncp = NetconfServiceProvider(self.device)


            if unconfig:
                crud_service.delete(ncp, interface_configuration)
            else:
                crud_service.create(ncp, interface_configuration)
        else:
            if unconfig:
                return YangConfig(device=self.device, unconfig=unconfig,
                                  ncp=NetconfServiceProvider,
                                  ydk_obj=interface_configuration,
                                  crud_service=crud_service.delete)
            else:
                return YangConfig(device=self.device, unconfig=unconfig,
                                  ncp=NetconfServiceProvider,
                                  ydk_obj=interface_configuration,
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
        interface_configurations = xr_ifmgr_cfg.InterfaceConfigurations()
        interface_configuration = interface_configurations.InterfaceConfiguration()
        interface_configuration.active = "act"
        interface_configuration.interface_name = attributes.value('name')
        if unconfig and attributes.iswildcard:
            interface_configuration = DELETE()
        else:
            shutdown = attributes.value('shutdown')
            if shutdown is not None:
                if unconfig:
                    # Special case: unconfiguring always applies shutdown
                    interface_configuration.shutdown = Empty()
                elif shutdown:
                    interface_configuration.shutdown = Empty()
                else:
                    interface_configuration.shutdown = DELETE()

            ipv4 = attributes.value('ipv4')
            primary = interface_configuration.ipv4_network.addresses.Primary()
            if ipv4:
                primary.address = str(ipv4.ip)
                primary.netmask = str(ipv4.netmask)

            vrf = attributes.value('vrf')
            if vrf:
                interface_configuration.vrf = vrf.name

        # instantiate crud service
        crud_service = CRUDService()
        if apply:

            # create netconf connection
            ncp = NetconfServiceProvider(self.device)

            return crud_service.create(ncp, interface_configuration)
        else:
            return YangConfig(device=self.device, unconfig=unconfig,
                              ncp=NetconfServiceProvider,
                              interface_configuration=interface_configuration,
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
        interface_configurations = xr_ifmgr_cfg.InterfaceConfigurations()
        # crud_service = CRUDService()
        # ncp = NetconfServiceProvider(self.device)
        # x = crud_service.read(ncp, interface_configurations)
        # abc = YangConfig(device=self.device, ydk_obj=x, ncp=ncp, crud_service=crud_service)
        # print(abc)
        interface_configuration = interface_configurations.InterfaceConfiguration()
        interface_configuration.active = "act"
        interface_configuration.interface_name = attributes.value('name')
        shutdown = attributes.value('shutdown')

        if shutdown is not None:
            if unconfig:
                # Special case: unconfiguring always applies shutdown
                interface_configuration.shutdown = Empty()
            elif shutdown:
                interface_configuration.shutdown = Empty()

            else:
                interface_configuration.shutdown = DELETE()

        vrf = attributes.value('vrf')
        if vrf:
            if unconfig:
                interface_configuration.vrf = DELETE()
            else:
                interface_configuration.vrf = vrf.name

        ipv4 = attributes.value('ipv4')
        if ipv4:
            primary = interface_configuration.ipv4_network.addresses.Primary()
            if unconfig:
                primary.address = DELETE()
                primary.netmask = DELETE()
                interface_configuration.ipv4_network.addresses.primary = primary
            else:
                primary.address = str(ipv4.ip)
                primary.netmask = str(ipv4.netmask)
                interface_configuration.ipv4_network.addresses.primary = primary

        # In Cisco-IOS-XR-l2-eth-infra-cfg.yang, augmentation section
        # augment "/a1:interface-configurations/a1:interface-configuration"
        # container ethernet-service is defined
        eth_encap_type1 = attributes.value('eth_encap_type1')
        eth_encap_val1 = attributes.value('eth_encap_val1')
        # eth_encap_type2 = attributes.value('eth_encap_type2')
        eth_encap_val2 = attributes.value('eth_encap_val2')

        if eth_encap_type1:
            interface_configuration.ethernet_service\
                                   .local_traffic_default_encapsulation\
                                   .outer_tag_type = eth_encap_type1

        if eth_encap_val1:
            interface_configuration.ethernet_service\
                                   .local_traffic_default_encapsulation\
                                   .outer_vlan_id = eth_encap_val1

        # if eth_encap_type2:
        #     interface_configuration.encapsulation.encapsulation = \
        #         eth_encap_type2

        if eth_encap_val2:
            interface_configuration.ethernet_service\
                                   .local_traffic_default_encapsulation\
                                   .inner_vlan_id = eth_encap_val2

        # instantiate crud service
        crud_service = CRUDService()

        if apply:

            # create netconf connection
            ncp = NetconfServiceProvider(self.device)

            crud_service.create(ncp, interface_configuration)
        else:
            return YangConfig(device=self.device,
                              ydk_obj=interface_configuration,
                              ncp=NetconfServiceProvider,
                              crud_service=crud_service.create)

Interface._build_name_to_class_map()

