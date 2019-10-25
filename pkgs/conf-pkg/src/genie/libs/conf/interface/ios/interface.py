'''
    Interface classes for ios OS.
'''

__all__ = (
    'Interface',
    'PhysicalInterface',
    'VirtualInterface',
    'LoopbackInterface',
    'EthernetInterface',
    'SubInterface',
)

import re
import contextlib
import abc
from enum import Enum

from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase
from genie.conf.base.exceptions import UnknownInterfaceTypeError
from genie.conf.base.attributes import SubAttributes, KeyedSubAttributes, SubAttributesDict,\
    AttributesHelper
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder

from genie.libs.conf.base import \
    MAC, \
    IPv4Address, IPv4Interface, \
    IPv6Address, IPv6Interface

import genie.libs.conf.interface

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
    """ base Interface class for IOS devices
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
            if d_parsed.subintf:
                factory_cls = SubInterface
            else:
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

    description = managedattribute(
        name='description',
        default=None,
        type=(None, managedattribute.test_istype(str)))

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
            return CliConfig(device=self.device, unconfig=unconfig,
                             cli_config=configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply,
                                 attributes=attributes,
                                 unconfig=True, **kwargs)

    def _build_config_create_interface_submode_context(self, configurations):
        return configurations.submode_context('interface {}'.format(self.name))

    def _build_config_interface_submode(self, configurations, attributes, unconfig):

        # ios: interface {name} / description some line data
        v = attributes.value('description')
        if v:
            if v is True:
                pass  # TODO Create a usefull default description
            configurations.append_line('description {}'.format(v))

        # ios: interface {name} / ip address 1.1.1.1 255.255.255.255 
        configurations.append_line(
            attributes.format('ip address {ipv4.ip} {ipv4.netmask}'))

        # ios: interface {name} / shutdown
        # enabled
        enabled = attributes.value('enabled')
        if enabled is not None:
            if enabled:
                config_cmd = 'no shutdown'
                unconfig_cmd = 'shutdown'
            else:
                config_cmd = 'shutdown'
                unconfig_cmd = 'no shutdown'
            configurations.append_line(
                attributes.format(config_cmd),
                unconfig_cmd=unconfig_cmd)
        # Compatibility
        else:
            shutdown = attributes.value('shutdown')
            if shutdown is not None:
                if unconfig:
                    # Special case: unconfiguring always applies shutdown
                    configurations.append_line('shutdown', raw=True)
                elif shutdown:
                    configurations.append_line('shutdown', raw=True)
                else:
                    configurations.append_line('no shutdown', raw=True)
                    
    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PhysicalInterface(Interface, genie.libs.conf.interface.PhysicalInterface):

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VirtualInterface(Interface, genie.libs.conf.interface.VirtualInterface):

    def _build_config_interface_submode(self, configurations, attributes, unconfig):

        # Virtual interfaces can be fully unconfigured
        if unconfig and attributes.iswildcard:
            configurations.submode_unconfig()

        super()._build_config_interface_submode(configurations, attributes, unconfig)

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LoopbackInterface(VirtualInterface, genie.libs.conf.interface.LoopbackInterface):

    _interface_name_types = (
        'Loopback',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EthernetInterface(PhysicalInterface, genie.libs.conf.interface.EthernetInterface):

    _interface_name_types = (
        'Ethernet',  # TODO verify
        'FastEthernet',
        'GigabitEthernet',  # TODO verify
        'TenGigabitEthernet',  # TODO verify
        'TwentyFiveGigabitEthernet',  # TODO verify
        'HundredGigabitEthernet',  # TODO verify
        'FortyGigabitEthernet',  # TODO verify
        # TODO more?
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        if unconfig and attributes.iswildcard:
            configurations.append_line('default interface {}'.format(self.name),raw=True)

        else:
            with self._build_config_create_interface_submode_context(configurations):
                self._build_config_interface_submode(configurations=configurations, attributes=attributes, unconfig=unconfig)

        if apply:
            if configurations:
                self.device.configure(configurations, fail_invalid=True)
        else:
            return CliConfig(device=self.device, unconfig=unconfig,
                             cli_config=configurations)

    def _build_config_interface_submode(self, configurations, attributes, unconfig):

        super()._build_config_interface_submode(configurations=configurations,
                                                attributes=attributes,
                                                unconfig=unconfig)

        # ios: interface {name} / mac-address aaaa.bbbb.cccc
        configurations.append_line(attributes.format('mac-address {mac_address}'))

        # ios: interface {name} / negotiation auto
        v = attributes.value('auto_negotiation')
        if v is not None:
            if v:
                configurations.append_line('negotiation auto',unconfig_cmd = 'default negotiation auto')
            else:
                if not unconfig:
                    configurations.append_line('no negotiation auto',unconfig_cmd = 'default negotiation auto')

class SubInterface(VirtualInterface,
                   genie.libs.conf.interface.SubInterface):
    '''Class for ios sub-interfaces'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Interface._build_name_to_class_map()