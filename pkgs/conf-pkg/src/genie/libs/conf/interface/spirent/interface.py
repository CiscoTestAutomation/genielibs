'''
    Interface classes for spirent OS (Spirent HLTAPI devices).
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
import types
from enum import Enum
from netaddr import mac_cisco, EUI
from ipaddress import IPv4Interface, IPv6Interface
try:
    from pyats.tcl import tclstr
except Exception:
    pass

from genie.decorator import managedattribute, mixedmethod
from genie.conf.base import ConfigurableBase
from genie.conf.base.exceptions import UnknownInterfaceTypeError
from genie.conf.base.attributes import SubAttributes, SubAttributesDict,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.libs.conf.base.ipaddress import ip_address
from genie.conf.base.utils import MAC

import genie.libs.conf.interface
import genie.libs.conf.interface.hltapi
from genie.libs.conf.interface import ParsedInterfaceName


class SpirentParsedInterfaceName(ParsedInterfaceName):

    def __init__(self, name, device=None):
        if device is None and isinstance(name, SpirentParsedInterfaceName):
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
    '''Base Interface class for HLTAPI devices with spirent OS'''

    def __new__(cls, *args, **kwargs):

        factory_cls = cls
        if cls is Interface:
            try:
                name = kwargs['name']
            except KeyError:
                raise TypeError('\'name\' argument missing')
            try:
                d_parsed = SpirentParsedInterfaceName(
                    name, kwargs.get('device', None))
            except ValueError as e1:
                # Not based on a Spirent physical port?
                d_parsed = ParsedInterfaceName(
                    name, kwargs.get('device', None))
                if d_parsed.subintf:
                    factory_cls = SubInterface
                else:
                    raise UnknownInterfaceTypeError
            else:
                # Based on a Spirent physical port.
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
                return SpirentParsedInterfaceName(
                    name=inst.name,
                    device=inst.device)
            except ValueError:
                # Not based on a Spirent physical port?
                return ParsedInterfaceName(
                    name=inst.name,
                    device=inst.device)
        else:
            try:
                return SpirentParsedInterfaceName(*args, **kwargs)
            except ValueError:
                # Not based on a Spirent physical port?
                return ParsedInterfaceName(*args, **kwargs)


class PhysicalInterface(Interface,
                        genie.libs.conf.interface.hltapi.PhysicalInterface):
    '''Class for physical Spirent interfaces/ports'''

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

        bNeedStcApply = False
        try:

            if unconfig:

                if self.tgen_port_configured:
                    if False:
                        hltkwargs = self._build_interface_config_hltkwargs(
                            attributes=attributes, unconfig=True)
                        if hltkwargs:
                            hltkl = hltapi.interface_config(**hltkwargs)
                            bNeedStcApply = False
                    else:
                        # Spirent HLTAPI drops the whole port instead of the "port_address" host on the port. Do this ourselves... {{{
                        for host_handle in hltapi.stc_get(
                                self.tgen_port_handle, '-AffiliationPort-Sources',
                                cast_=functools.partial(
                                    hltapi.tcl.cast_list, item_cast=tclstr)):
                            if hltapi.stc_get(host_handle,
                                              '-Name',
                                              cast_=tclstr) == 'port_address':
                                hltapi.stc_delete(host_handle)
                                bNeedStcApply = True
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

                    # Spirent: arp_target is Spirent-specific
                    if hltkwargs.get('arp_send_req', None) == 1:
                        hltkwargs.setdefault('arp_target', 'all')

                    # Spirent: bugfix SR-1-334940921
                    if hltkwargs.get('speed', None) == "ether10000":
                        hltkwargs.pop('intf_mode', None)

                    # Spirent: does not support -op_mode
                    hltkwargs.pop('op_mode', None)

                    # Spirent: tx_scrambling/rx_scrambling -> scramble (give precedence to tx_scrambling)
                    if 'tx_scrambling' in hltkwargs:
                        hltkwargs.setdefault('scramble',
                                             hltkwargs.pop('tx_scrambling'))
                    if 'rx_scrambling' in hltkwargs:
                        hltkwargs.setdefault('scramble',
                                             hltkwargs.pop('rx_scrambling'))

                    hltkl = hltapi.interface_config(**hltkwargs)
                    bNeedStcApply = False
                    self.tgen_port_configured = True
                    if 'interface_handle' in hltkl:
                        self.tgen_handle = hltkl.interface_handle

                    # Spirent: Enable ping response
                    if 'intf_ip_addr' in hltkwargs:
                        for host_handle in hltapi.stc_get(
                                self.tgen_port_handle,
                                '-AffiliationPort-Sources',
                                cast_=functools.partial(hltapi.tcl.cast_list,
                                                        item_cast=tclstr)):
                            if hltapi.stc_get(host_handle,
                                              '-Name',
                                              cast_=tclstr) == 'port_address':
                                if not hltapi.stc_get(host_handle,
                                                      '-EnablePingResponse',
                                                      cast_=tclstr) != 'TRUE':
                                    hltapi.stc_config(host_handle,
                                                      '-EnablePingResponse',
                                                      'TRUE')
                                    bNeedStcApply = True

        finally:
            if bNeedStcApply:
                hltapi.stc_apply()
                bNeedStcApply = False

        return ''  # No CLI lines

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply,
                                 attributes=attributes,
                                 unconfig=True, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_arp_cache(self, update_cache=True):
        # XXXJST Spirent's HLTAPI arp_control is widely broken, bad parsing,
        # unable to deal with named streams, ... Let's implement our own
        # correctly.

        hltapi = self.hltapi
        tcl = hltapi.tcl

        if update_cache:
            hltapi.stc_perform('ArpNdUpdateArpCacheCommand',
                               HandleList=(self.tgen_port_handle,))

        ArpCache, = hltapi.stc_get(self.tgen_port_handle, '-children-ArpCache',
                                   cast_=functools.partial(tcl.cast_list,
                                                           item_cast=tclstr))
        rawArpCacheData = hltapi.stc_get(ArpCache, '-ArpCacheData',
                                         cast_=functools.partial(
                                             tcl.cast_list, item_cast=tclstr))
        # '{10.85.69.149-1-10 //1/10\tA->B/MAC+IPv4/vlan1 :2\t192.0.4.3\t192.0.4.1\tfc00.0001.0000} {...}'

        arp_cache = []

        for rawArpCacheEntry in rawArpCacheData:
            (
                arpLocation,
                arpObjName,
                arpSourceAddress,
                arpGatewayAddress,
                arpResolvedMacAddress,
            ) = rawArpCacheEntry.split('\t')
            arp_cache_entry = types.SimpleNamespace(
                object_name=arpObjName,
                source_address=ip_address(arpSourceAddress),
                gateway_address=ip_address(arpGatewayAddress),
                mac_address=MAC(arpResolvedMacAddress),
            )
            arp_cache.append(arp_cache_entry)

        return arp_cache


class EthernetInterface(PhysicalInterface,
                        genie.libs.conf.interface.hltapi.EthernetInterface):
    '''Class for physical ethernet Spirent interfaces/ports'''

    phy_mode = PhysicalInterface.phy_mode.copy(
        default=PhysicalInterface.PhysicalMode.fiber)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AtmInterface(PhysicalInterface,
                   genie.libs.conf.interface.hltapi.AtmInterface):
    '''Class for physical ATM Spirent interfaces/ports'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PosInterface(PhysicalInterface,
                   genie.libs.conf.interface.hltapi.PosInterface):
    '''Class for physical POS Spirent interfaces/ports'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EmulatedInterface(Interface,
                        genie.libs.conf.interface.hltapi.EmulatedInterface):
    '''Class for emulated Spirent interfaces'''

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)


class EmulatedLoopbackInterface(EmulatedInterface,
                                genie.libs.conf.interface.LoopbackInterface):
    '''Class for emulated Spirent loopback interfaces'''
    pass


class EmulatedEthernetInterface(EmulatedInterface,
                                genie.libs.conf.interface.EthernetInterface):
    '''Class for emulated Spirent ethernet interfaces'''
    pass


class VirtualInterface(Interface,
                       genie.libs.conf.interface.hltapi.VirtualInterface):
    '''Class for virtual Spirent interfaces'''

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SubInterface(VirtualInterface,
                   genie.libs.conf.interface.hltapi.SubInterface):
    '''Class for Spirent sub-interfaces'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

