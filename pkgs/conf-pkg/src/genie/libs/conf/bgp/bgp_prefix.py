"""BgpPrefix type implementation
"""

__all__ = (
    'BgpRoute',
    'BgpIpv4UnicastRoute',
    'BgpL2vpnEvpnRoute',
)

import abc
from copy import copy
import re
from enum import IntEnum, Enum
import functools

from genie.decorator import managedattribute
from genie.libs.conf.address_family import AddressFamily
from genie.libs.conf.base import MAC
from genie.libs.conf.base import RouteDistinguisher
from genie.libs.conf.base import \
    ip_address, \
    ip_network, ip_network as _ip_network, \
    IPv4Address, IPv6Address, \
    IPv4Network
from genie.libs.conf.evpn.esi import ESI


@functools.total_ordering
class BgpRoute(abc.ABC):

    @staticmethod
    def create(af, *args, **kwargs):
        if af is AddressFamily.ipv4_unicast:
            cls = BgpIpv4UnicastRoute
        elif af is AddressFamily.l2vpn_evpn:
            cls = BgpL2vpnEvpnRoute
        else:
            raise NotImplementedError(af)
        return cls(*args, **kwargs)

    @property
    @abc.abstractmethod
    def af(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def type(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def prefix_length(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __eq__(self, other):
        if not isinstance(other, BgpRoute):
            try:
                other = BgpRoute(other)
            except Exception:
                return NotImplemented
        return self.af == other.af

    @abc.abstractmethod
    def __lt__(self, other):
        if not isinstance(other, BgpRoute):
            try:
                other = BgpRoute(other)
            except Exception:
                return NotImplemented
        return self.af < other.af

    @abc.abstractmethod
    def __hash__(self):
        # TODO rest is mutable!
        return hash(self.af)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, str(self))

    def __copy__(self):
        return self.__class__(self)

    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError


class BgpIpv4UnicastRouteType(IntEnum):
    ip = 1


class BgpIpv4UnicastRoute(BgpRoute):

    af = managedattribute(
        name='af',
        default=AddressFamily.ipv4_unicast,
        read_only=True)

    Type = BgpIpv4UnicastRouteType

    type = managedattribute(
        name='type',
        type=Type)

    ip = managedattribute(
        name='ip',
        default=None,
        type=(None, IPv4Address))

    prefix_length = managedattribute(
        name='prefix_length',
        type=int)

    @property
    def ip_network(self):
        return IPv4Network('{}/{}'.format(self.ip, self.prefix_length))

    @ip_network.setter
    def ip_network(self, value):
        ip_network = IPv4Network(value)
        self.ip = ip_network.network_address
        self.prefix_length = ip_network.prefixlen

    def __init__(self, value=None, **kwargs):
        if value is None:
            if 'type' not in kwargs:
                raise TypeError('type argument mandatory.')
            for attr in (
                    'type',
                    'prefix_length',
                    'ip',
            ):
                v = kwargs.pop(attr, None)
                if v is not None:
                    setattr(self, attr, v)
            if kwargs:
                raise TypeError('Unexpected keyword arguments: {}'\
                                .format(', '.join(kwargs.keys())))
            return

        if kwargs:
            raise TypeError('Provide either value or kwargs, not both.')

        if isinstance(value, BgpIpv4UnicastRoute):
            # Copy constructor
            for attr in (
                    'type',
                    'prefix_length',
                    'ip',
            ):
                v = getattr(value, attr)
                if v is not None:
                    setattr(self, attr, v)
            return

        if isinstance(value, (str, IPv4Address, IPv4Network)):
            # '1.2.3.4', '1.2.3.0/24'
            self.ip_network = IPv4Network(value)
            self.type = BgpIpv4UnicastRouteType.ip
            return

        raise TypeError(value)

    def __eq__(self, other):
        if not isinstance(other, BgpRoute):
            try:
                other = BgpRoute(other)
            except Exception:
                return NotImplemented
        supeq = super().__eq__(other)
        if not supeq or supeq is NotImplemented:
            return supeq
        assert isinstance(other, BgpIpv4UnicastRoute)
        return (
            self.type,
            self.prefix_length,
            self.ip,
        ) == (
            other.type,
            other.prefix_length,
            other.ip,
        )

    def __lt__(self, other):
        if not isinstance(other, BgpRoute):
            try:
                other = BgpRoute(other)
            except Exception:
                return NotImplemented
        suplt = super().__lt__(other)
        if suplt or not isinstance(other, BgpIpv4UnicastRoute):
            return suplt
        return (
            self.type,
            self.prefix_length,
            self.ip is not None, self.ip,
        ) < (
            other.type,
            other.prefix_length,
            other.ip is not None, other.ip,
        )

    def __hash__(self):
        return super().__hash__()

    def __str__(self):
        s = ''
        if self.type is BgpIpv4UnicastRouteType.ip:
            # 1.2.3.4/32
            s += '{self.ip_network}'\
                .format(self=self)
        else:
            raise RuntimeError(self.type)
        return s


class BgpL2vpnEvpnRouteType(IntEnum):
    ethernet_ad = 1
    mac = 2
    inclusive_multicast = 3
    ethernet_segment = 4
    ip = 5


class BgpL2vpnEvpnRoute(BgpRoute):

    af = managedattribute(
        name='af',
        default=AddressFamily.l2vpn_evpn,
        read_only=True)

    Type = BgpL2vpnEvpnRouteType

    type = managedattribute(
        name='type',
        type=Type)

    esi = managedattribute(
        name='esi',
        default=None,
        type=(None, ESI))

    rd = managedattribute(
        name='rd',
        default=None,
        type=(None, RouteDistinguisher))

    eth_tag = managedattribute(
        name='eth_tag',
        default=None,
        type=(None, int))

    mac_length = managedattribute(
        name='mac_length',
        type=int)

    @mac_length.defaulter
    def mac_length(self):
        mac = self.mac
        if mac is None:
            return 0
        return 48

    mac = managedattribute(
        name='mac',
        default=None,
        type=(None, MAC))

    ip_length = managedattribute(
        name='ip_length',
        type=int)

    @ip_length.defaulter
    def ip_length(self):
        return self.ip_max_length

    @property
    def ip_max_length(self):
        ip = self.ip
        if ip is None:
            return 0
        if isinstance(ip, IPv4Address):
            return 32
        if isinstance(ip, IPv6Address):
            return 128
        raise RuntimeError(ip)

    ip = managedattribute(
        name='ip',
        default=None,
        type=(None, ip_address))

    @property
    def ip_network(self):
        return _ip_network('{}/{}'.format(self.ip, self.ip_length))

    @ip_network.setter
    def ip_network(self, value):
        ip_network = _ip_network(value)
        self.ip = ip_network.network_address
        self.ip_length = ip_network.prefixlen

    prefix_length = managedattribute(
        name='prefix_length',
        type=managedattribute.test_istype(int))

    @prefix_length.defaulter
    def prefix_length(self):
        if self.type is BgpL2vpnEvpnRouteType.ethernet_ad:
            return 120 + (64 if self.rd is not None else 0)
        if self.type is BgpL2vpnEvpnRouteType.mac:
            return 104 + self.ip_max_length
        if self.type is BgpL2vpnEvpnRouteType.inclusive_multicast:
            return 48 + self.ip_max_length
        if self.type is BgpL2vpnEvpnRouteType.ethernet_segment:
            return 88 + self.ip_max_length
        if self.type is BgpL2vpnEvpnRouteType.ip:
            return 48 + self.ip_max_length
        raise RuntimeError(self.type)

    def __init__(self, value=None, **kwargs):
        if value is None:
            if 'type' not in kwargs:
                raise TypeError('type argument mandatory.')
            for attr in (
                    'type',
                    'esi',
                    'rd',
                    'eth_tag',
                    'ip_length',
                    'ip',
                    'mac_length',
                    'mac',
                    'prefix_length',
            ):
                v = kwargs.pop(attr, None)
                if v is not None:
                    setattr(self, attr, v)
            if kwargs:
                raise TypeError('Unexpected keyword arguments: {}'\
                                .format(', '.join(kwargs.keys())))
            return

        if kwargs:
            raise TypeError('Provide either value or kwargs, not both.')

        if isinstance(value, BgpL2vpnEvpnRoute):
            # Copy constructor
            for attr in (
                    'type',
                    'esi',
                    'rd',
                    'eth_tag',
                    'ip_length',
                    'ip',
                    'mac_length',
                    'mac',
                    'prefix_length',
            ):
                v = getattr(value, attr)
                if v is not None:
                    setattr(self, attr, v)
            return

        if isinstance(value, str):
            m = re.match(r'^\[(?P<type>[0-9]+)\]', value)
            if not m:
                raise ValueError(value)
            self.type = BgpL2vpnEvpnRouteType(int(m.group('type')))
            m = re.match(r'^(?P<value>.+)/(?P<prefix_length>\d+)$', value)
            if m:
                value = m.group('value')
                self.prefix_length = int(m.group('prefix_length'))
            if self.type is BgpL2vpnEvpnRouteType.ethernet_ad:
                # [Type][ESI][ETag] -----> EVI AD Route
                # [Type][RD][ESI][ETag] -----> Per ES AD Route
                m = re.match(r'^'
                             r'\[[0-9]+\]'
                             r'(?:\[(?P<rd>[^\]]+)\])?'
                             r'\[(?P<esi>[^\]]+)\]'
                             r'\[(?P<eth_tag>[0-9]+)\]'
                             r'$', value)
                if not m:
                    raise ValueError(value)
                for attr, v in m.groupdict().items():
                    setattr(self, attr, v)
            elif self.type is BgpL2vpnEvpnRouteType.mac:
                # [Type][ETag][MAC Len][MAC Addr][IP Addr Len][IP Addr]
                m = re.match(r'^'
                             r'\[[0-9]+\]'
                             r'\[(?P<eth_tag>[0-9]+)\]'
                             r'\[(?P<mac_length>[0-9]+)\]'
                             r'\[(?P<mac>[A-Fa-f0-9.]+)\]'
                             r'\[(?P<ip_length>[0-9]+)\]'
                             r'(?:\[(?P<ip>[A-Fa-f0-9:.]+)\])?'
                             r'$', value)
                if not m:
                    raise ValueError(value)
                for attr, v in m.groupdict().items():
                    setattr(self, attr, v)
            elif self.type is BgpL2vpnEvpnRouteType.inclusive_multicast:
                # [Type][ETag][IP Addr Len][IP Addr]
                m = re.match(r'^'
                             r'\[[0-9]+\]'
                             r'\[(?P<eth_tag>[0-9]+)\]'
                             r'\[(?P<ip_length>[0-9]+)\]'
                             r'\[(?P<ip>[A-Fa-f0-9:.]+)\]'
                             r'$', value)
                if not m:
                    raise ValueError(value)
                for attr, v in m.groupdict().items():
                    setattr(self, attr, v)
            elif self.type is BgpL2vpnEvpnRouteType.ethernet_segment:
                # [Type][ESI][IP Addr Len][IP Addr]
                m = re.match(r'^'
                             r'\[[0-9]+\]'
                             r'\[(?P<esi>[^\]]+)\]'
                             r'(?:'
                             r'\[(?P<ip_length>[0-9]+)\]'
                             r'\[(?P<ip>[A-Fa-f0-9:.]+)\]'
                             r')?'
                             r'$', value)
                if not m:
                    raise ValueError(value)
                d = m.groupdict()
                if d['ip_length'] is None:
                    d['ip_length'] = 0
                for attr, v in d.items():
                    setattr(self, attr, v)
            elif self.type is BgpL2vpnEvpnRouteType.ip:
                # [Type][ETag][IP Addr Len][IP Addr]
                m = re.match(r'^'
                             r'\[[0-9]+\]'
                             r'\[(?P<eth_tag>[0-9]+)\]'
                             r'\[(?P<ip_length>[0-9]+)\]'
                             r'\[(?P<ip>[A-Fa-f0-9:.]+)\]'
                             r'$', value)
                if not m:
                    raise ValueError(value)
                for attr, v in m.groupdict().items():
                    setattr(self, attr, v)
            else:
                raise RuntimeError(self.type)
            return

        raise TypeError(value)

    def __eq__(self, other):
        if not isinstance(other, BgpRoute):
            try:
                other = BgpRoute(other)
            except Exception:
                return NotImplemented
        supeq = super().__eq__(other)
        if not supeq or supeq is NotImplemented:
            return supeq
        assert isinstance(other, BgpL2vpnEvpnRoute)
        return (
            self.type,
            self.esi, self.rd, self.eth_tag,
            self.ip_length, self.ip,
            self.mac_length, self.mac,
        ) == (
            other.type,
            other.esi, other.rd, other.eth_tag,
            other.ip_length, other.ip,
            other.mac_length, other.mac,
        )

    def __lt__(self, other):
        if not isinstance(other, BgpRoute):
            try:
                other = BgpRoute(other)
            except Exception:
                return NotImplemented
        suplt = super().__lt__(other)
        if suplt or not isinstance(other, BgpL2vpnEvpnRoute):
            return suplt
        return (
            self.type,
            self.esi is not None, self.esi,
            self.rd is not None, self.rd,
            self.eth_tag is not None, self.eth_tag,
            self.ip_length, self.ip.version if self.ip is not None else 0, self.ip,
            self.mac_length, self.mac is not None, self.mac,
        ) < (
            other.type,
            other.esi is not None, other.esi,
            other.rd is not None, other.rd,
            other.eth_tag is not None, other.eth_tag,
            other.ip_length, other.ip.version if other.ip is not None else 0, other.ip,
            other.mac_length, other.mac is not None, other.mac,
        )

    def __hash__(self):
        return super().__hash__()

    def __str__(self):
        s = '[{self.type.value}]'.format(self=self)
        if self.type is BgpL2vpnEvpnRouteType.ethernet_ad:
            # [Type][ESI][ETag] -----> EVI AD Route
            # [Type][RD][ESI][ETag] -----> Per ES AD Route
            if self.rd is not None:
                s += '[{self.rd}]'.format(self=self)
            s += '[{self.esi:tx.xx.xx.xx.xx}][{self.eth_tag}]'\
                .format(self=self)
        elif self.type is BgpL2vpnEvpnRouteType.mac:
            # [Type][ETag][MAC Len][MAC Addr][IP Addr Len][IP Addr]
            s += '[{self.eth_tag}][{self.mac_length}][{self.mac}]'\
                '[{self.ip_length}]'.format(self=self)
            if self.ip_length:
                s += '[{self.ip}]'.format(self=self)
        elif self.type is BgpL2vpnEvpnRouteType.inclusive_multicast:
            # [Type][ETag][IP Addr Len][IP Addr]
            s += '[{self.eth_tag}]'\
                '[{self.ip_length}][{self.ip}]'\
                .format(self=self)
        elif self.type is BgpL2vpnEvpnRouteType.ethernet_segment:
            # [Type][ESI][IP Addr Len][IP Addr]
            s += '[{self.esi:tx.xx.xx.xx.xx}]'.format(self=self)
            if self.ip_length:
                s += '[{self.ip_length}][{self.ip}]'\
                    .format(self=self)
        elif self.type is BgpL2vpnEvpnRouteType.ip:
            # [Type][ETag][IP Addr Len][IP Addr]
            s += '[{self.eth_tag}]'\
                '[{self.ip_length}][{self.ip}]'\
                .format(self=self)
        else:
            raise RuntimeError(self.type)
        s += '/{}'.format(self.prefix_length)
        return s

