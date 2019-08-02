'''
    Interface classes for pagent OS (Pagent HLTAPI devices).
'''

__all__ = (
    'Interface',
    'PhysicalInterface',
    'EthernetInterface',
    'SubInterface',
)

import functools
import re
import abc
from enum import Enum
from netaddr import mac_cisco, EUI
from ipaddress import IPv4Interface, IPv6Interface

from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase
from genie.conf.base.exceptions import UnknownInterfaceTypeError
from genie.conf.base.attributes import SubAttributes, SubAttributesDict,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder

import genie.libs.conf.interface
import genie.libs.conf.interface.hltapi
import genie.libs.conf.interface.ios


class Interface(genie.libs.conf.interface.hltapi.Interface,
                genie.libs.conf.interface.ios.Interface):
    '''Base Interface class for HLTAPI devices with pagent OS'''

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
                factory_cls = SubInterface  # TODO
            else:
                try:
                    factory_cls = cls._name_to_class_map[d_parsed.type]
                except KeyError:
                    raise UnknownInterfaceTypeError
            #  Async              Async interface
            #  BVI                Bridge-Group Virtual Interface
            #  CDMA-Ix            CDMA Ix interface
            #  CTunnel            CTunnel interface
            #  Dialer             Dialer interface
            #  FastEthernet       FastEthernet IEEE 802.3
            #  Group-Async        Async Group interface
            #  Lex                Lex interface
            #  Loopback           Loopback interface
            #  MFR                Multilink Frame Relay bundle interface
            #  Multilink          Multilink-group interface
            #  Null               Null interface
            #  Port-channel       Ethernet Channel of interfaces
            #  Tunnel             Tunnel interface
            #  Vif                PGM Multicast Host interface
            #  Virtual-PPP        Virtual PPP interface
            #  Virtual-Template   Virtual Template interface
            #  Virtual-TokenRing  Virtual TokenRing
            #  XTagATM            Extended Tag ATM interface

        if factory_cls is not cls:
            self = factory_cls.__new__(factory_cls, *args, **kwargs)
        elif super().__new__ is object.__new__:
            self = super().__new__(factory_cls)
        else:
            self = super().__new__(factory_cls, *args, **kwargs)
        return self

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PhysicalInterface(Interface,
                        genie.libs.conf.interface.hltapi.PhysicalInterface,
                        genie.libs.conf.interface.ios.PhysicalInterface):
    '''Class for physical Pagent interfaces/ports'''

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)

        hltapi = self.device.hltapi

        if unconfig:

            if self.tgen_port_configured:
                hltkwargs = self._build_interface_config_hltkwargs(
                    attributes=attributes, unconfig=True)
                if hltkwargs:
                    hltkl = hltapi.interface_config(**hltkwargs)
                self.tgen_port_configured = False

        else:

            if self.tgen_port_configured and attributes.iswildcard:
                # interface_config -mode modify is very flaky (mostly on
                # Pagent). So destroy the old configuration first.
                self.build_unconfig()

            hltkwargs = self._build_interface_config_hltkwargs(
                attributes=attributes)
            if hltkwargs:

                # Pagent does not support -arp_send_req
                hltkwargs.pop('arp_send_req', None)

                # Pagent does not support -intf_mode
                hltkwargs.pop('intf_mode', None)

                # Pagent does not support -op_mode; Unset if "normal"
                if hltkwargs.get('op_mode', None) == 'normal':
                    del hltkwargs['op_mode']

                # Pagent does not support -vlan; Unset if false
                if hltkwargs.get('vlan', None) is False:
                    del hltkwargs['vlan']

                hltkl = hltapi.interface_config(**hltkwargs)

        return ''  # No CLI lines

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply,
                                 attributes=attributes,
                                 unconfig=True, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# XXXJST TODO Not a HLTAPI VirtualInterface
class VirtualInterface(Interface,
                       genie.libs.conf.interface.ios.VirtualInterface):

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LoopbackInterface(VirtualInterface,
                        genie.libs.conf.interface.ios.LoopbackInterface):

    _interface_name_types = genie.libs.conf.interface.ios.LoopbackInterface._interface_name_types

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EthernetInterface(PhysicalInterface,
                        genie.libs.conf.interface.hltapi.EthernetInterface,
                        genie.libs.conf.interface.ios.EthernetInterface):
    '''Class for physical ethernet Pagent interfaces/ports'''

    _interface_name_types = genie.libs.conf.interface.ios.EthernetInterface._interface_name_types

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SubInterface(VirtualInterface, genie.libs.conf.interface.SubInterface):
    '''Class for pageant sub-interfaces'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

Interface._build_name_to_class_map()
