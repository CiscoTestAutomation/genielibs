'''
    Interface classes for ixia OS (Ixia HLTAPI devices).
'''

__all__ = (
    'Interface',
    'PhysicalInterface',
    'EthernetInterface',
    'PosInterface',
    'AtmInterface',
    'EmulatedInterface',
    'EmulatedLoopbackInterface',
    'EmulatedEthernetInterface',
    'VirtualInterface',
    'SubInterface',
)

import functools
import re
import abc
from enum import Enum
from netaddr import mac_cisco, EUI
from ipaddress import IPv4Interface, IPv6Interface

from genie.decorator import managedattribute, mixedmethod
from genie.conf.base import ConfigurableBase
from genie.conf.base.exceptions import UnknownInterfaceTypeError
from genie.conf.base.attributes import SubAttributes, SubAttributesDict,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder

import genie.libs.conf.interface
import genie.libs.conf.interface.hltapi
from genie.libs.conf.interface import ParsedInterfaceName


class IxiaParsedInterfaceName(ParsedInterfaceName):

    def __init__(self, name, device=None):
        if device is None and isinstance(name, IxiaParsedInterfaceName):
            # copy constructor
            return super().__init__(vars(name))
        assert type(name) is str

        d = dict(
            # main parts
            type=None,
            number=None,
            subintf_sep=None,
            subintf=None,
            # sub-parts
            slot=None,
            port=None,
        )

        m = re.match(r'''
            ^
            # ignore leading spaces
            \s*
            # not an empty string
            (?=\S)
            (?P<number>
                # <slot>/<port>
                (?P<slot>\d+)/(?P<port>\d+)
            )
            # optional <subintf>
            (?:(?P<subintf_sep>[.:])(?P<subintf>\d+))?
            # ignore trailing spaces
            \s*
            $
        ''', name, re.VERBOSE | re.IGNORECASE)
        if not m:
            raise ValueError('Unrecognized interface name %r' % (name,))
        d.update(m.groupdict())

        # Skip over ParsedInterfaceName __init__
        super(ParsedInterfaceName, self).__init__(**d)

    def reconstruct(self):
        return '{slot}/{port}{subintf_sep}{subintf}'.format(
            slot=self.slot,
            port=self.port,
            subintf_sep=(self.subintf_sep or '.') if self.subintf is not None else '',
            subintf=self.subintf if self.subintf is not None else '',
        )


class Interface(genie.libs.conf.interface.hltapi.Interface):
    '''Base Interface class for HLTAPI devices with ixia OS'''

    def __new__(cls, *args, **kwargs):

        factory_cls = cls
        if cls is Interface:
            try:
                name = kwargs['name']
            except KeyError:
                raise TypeError('\'name\' argument missing')
            try:
                d_parsed = IxiaParsedInterfaceName(
                    name, kwargs.get('device', None))
            except ValueError as e1:
                # Not based on an Ixia physical port?
                d_parsed = ParsedInterfaceName(
                    name, kwargs.get('device', None))
                if d_parsed.subintf:
                    factory_cls = SubInterface
                else:
                    raise UnknownInterfaceTypeError
            else:
                # Based on an Ixia physical port.
                if d_parsed.subintf:
                    factory_cls = SubInterface
                else:
                    factory_cls = PhysicalInterface

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

    @mixedmethod
    def parse_interface_name(inst, cls, *args, **kwargs):
        if inst:
            if args or kwargs:
                raise TypeError('Unexpected arguments: %r %r' % (args, kwargs))
            try:
                return IxiaParsedInterfaceName(
                    name=inst.name,
                    device=inst.device)
            except ValueError:
                # Not based on an Ixia physical port?
                return ParsedInterfaceName(
                    name=inst.name,
                    device=inst.device)
        else:
            try:
                return IxiaParsedInterfaceName(*args, **kwargs)
            except ValueError:
                # Not based on an Ixia physical port?
                return ParsedInterfaceName(*args, **kwargs)


class PhysicalInterface(Interface,
                        genie.libs.conf.interface.hltapi.PhysicalInterface):
    '''Class for physical Ixia interfaces/ports'''

    def __new__(cls, *args, **kwargs):

        factory_cls = cls
        if cls is PhysicalInterface:
            intf_mode = cls.InterfaceMode.ethernet
            try:
                intf_mode = kwargs['intf_mode']
            except KeyError:
                pass
            try:
                intf_mode = cls.InterfaceMode(intf_mode)
            except ValueError:
                pass  # handled later
            if intf_mode is cls.InterfaceMode.ethernet:
                factory_cls = EthernetInterface
            elif intf_mode is cls.InterfaceMode.atm:
                factory_cls = AtmInterface
            elif intf_mode in (
                cls.InterfaceMode.pos_hdlc,
                cls.InterfaceMode.fr,
                cls.InterfaceMode.pos_ppp,
            ):
                factory_cls = PosInterface
            else:
                pass  # raise ValueError('Unsupported intf_mode %r' % (self.intf_mode,))

        if factory_cls is not cls:
            self = factory_cls.__new__(factory_cls, *args, **kwargs)
        elif super().__new__ is object.__new__:
            self = super().__new__(factory_cls)
        else:
            self = super().__new__(factory_cls, *args, **kwargs)
        return self

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)

        hltapi = self.device.hltapi

        bNeedIxNetApply = False
        try:

            if unconfig:

                if self.tgen_port_configured:
                    hltkwargs = self._build_interface_config_hltkwargs(
                        attributes=attributes, unconfig=True)
                    if hltkwargs:
                        hltkl = hltapi.interface_config(**hltkwargs)
                        bNeedIxNetApply = False
                    self.tgen_port_configured = False

            else:

                if self.tgen_port_configured and attributes.iswildcard:
                    # interface_config -mode modify is very flaky (mostly on
                    # Spirent). So destroy the old configuration first.  Note
                    # that, for Spirent, hltapi::interface_config is required
                    # to properly handle -mode destroy.
                    self.build_unconfig()

                hltkwargs = self._build_interface_config_hltkwargs(
                    attributes=attributes)
                if hltkwargs:

                    # Ixia: ignore_link is Ixia-specific
                    hltkwargs.setdefault('ignore_link', True)

                    # Ixia: Use Ixia-specific speed values
                    if 'speed' in hltkwargs:
                        speed = hltkwargs['speed']
                        hltkwargs['speed'] = {
                            'ether10000': 'ether10000lan',
                            'ether40Gig': 'ether40000lan',
                            'ether100Gig': 'ether100000lan',
                        }.get(speed, speed)

                    hltkl = hltapi.interface_config(**hltkwargs)
                    bNeedIxNetApply = False
                    self.tgen_port_configured = True
                    if 'interface_handle' in hltkl:
                        self.tgen_handle = hltkl.interface_handle

        finally:
            if bNeedIxNetApply:
                hltapi.ixNetworkCommit()
                bNeedIxNetApply = False

        return ''  # No CLI lines

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply,
                                 attributes=attributes,
                                 unconfig=True, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EthernetInterface(PhysicalInterface,
                        genie.libs.conf.interface.hltapi.EthernetInterface):
    '''Class for physical ethernet Ixia interfaces/ports'''

    phy_mode = PhysicalInterface.phy_mode.copy(
        default=PhysicalInterface.PhysicalMode.fiber)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AtmInterface(PhysicalInterface,
                   genie.libs.conf.interface.hltapi.AtmInterface):
    '''Class for physical ATM Ixia interfaces/ports'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PosInterface(PhysicalInterface,
                   genie.libs.conf.interface.hltapi.PosInterface):
    '''Class for physical POS Ixia interfaces/ports'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EmulatedInterface(Interface,
                        genie.libs.conf.interface.hltapi.EmulatedInterface):
    '''Class for emulated Ixia interfaces'''

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)


class EmulatedLoopbackInterface(EmulatedInterface,
                                genie.libs.conf.interface.LoopbackInterface):
    '''Class for emulated Ixia loopback interfaces'''
    pass


class EmulatedEthernetInterface(EmulatedInterface,
                                genie.libs.conf.interface.EthernetInterface):
    '''Class for emulated Ixia ethernet interfaces'''
    pass


class VirtualInterface(Interface,
                       genie.libs.conf.interface.hltapi.VirtualInterface):
    '''Class for virtual Ixia interfaces'''

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SubInterface(VirtualInterface,
                   genie.libs.conf.interface.hltapi.SubInterface):
    '''Class for Ixia sub-interfaces'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

