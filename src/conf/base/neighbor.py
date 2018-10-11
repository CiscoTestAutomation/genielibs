
__all__ = (
    'IPv4Neighbor',
    'IPv4LsrNeighbor',
    'IPv6Neighbor',
    # Abstract classes:
    'Neighbor',
    'IPNeighbor',
)

import functools
import abc
import ipaddress
import re

from genie.decorator import managedattribute
from genie.conf.base.attributes import KeyedSubAttributes

from genie.libs.conf.base import ABCBase


@functools.total_ordering
class Neighbor(ABCBase):
    '''Base for all Neighbor subclasses.'''

    @abc.abstractmethod
    def _neighbor_comparison_tokens(self):
        return (self.testbed,)

    def __hash__(self):
        '''Subclasses are encouraged to override.'''
        return 0

    def __eq__(self, other):
        if not isinstance(other, Neighbor):
            return NotImplemented
        return self._neighbor_comparison_tokens() \
            == other._neighbor_comparison_tokens()

    def __lt__(self, other):
        if not isinstance(other, Neighbor):
            return NotImplemented
        return self._neighbor_comparison_tokens() \
            < other._neighbor_comparison_tokens()


class IPNeighbor(Neighbor):

    ip = managedattribute(
        name='ip',
        read_only=True,  # read-only hash key
        doc='''IPv4Address or IPv6Address (mandatory)''')

    def __new__(cls, *args, **kwargs):

        factory_cls = cls
        if cls is IPNeighbor:
            if not kwargs and len(args) == 1 \
                    and isinstance(args[0], IPNeighbor):
                # Copy constructor
                factory_cls = type(args[0])
            else:
                if not kwargs and len(args) == 1:
                    ip = args[0]
                else:
                    try:
                        ip = kwargs['ip']
                    except KeyError:
                        raise TypeError('\'ip\' argument missing')
                if isinstance(ip, (ipaddress.IPv4Interface,
                                   ipaddress.IPv6Interface)):
                    ip = ip.ip
                elif isinstance(ip, (ipaddress.IPv4Address,
                                     ipaddress.IPv6Address)):
                    pass
                else:
                    ip = ipaddress.ip_address(ip)
                if isinstance(ip, ipaddress.IPv4Address):
                    factory_cls = IPv4Neighbor
                elif isinstance(ip, ipaddress.IPv6Address):
                    factory_cls = IPv6Neighbor
                else:
                    raise ValueError(ip)

        if factory_cls is not cls:
            self = factory_cls.__new__(factory_cls, *args, **kwargs)
        elif super().__new__ is object.__new__:
            self = super().__new__(factory_cls)
        else:
            self = super().__new__(factory_cls, *args, **kwargs)
        return self

    def __str__(self):
        return str(self.ip)

    def __repr__(self):
        return '{}(\'{}\')'.format(
            self.__class__.__name__,
            self.ip)

    def __init__(self, ip, **kwargs):
        if isinstance(ip, (ipaddress.IPv4Interface, ipaddress.IPv6Interface)):
            ip = ip.ip
        elif isinstance(ip, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
            pass
        else:
            ip = ipaddress.ip_address(ip)
        self._ip = ip
        super().__init__(**kwargs)

    def _neighbor_comparison_tokens(self):
        return super()._neighbor_comparison_tokens() + (
            'ip', self.ip.version, self.ip,
        )

    def __hash__(self):
        return hash(self.ip)


class IPv4Neighbor(IPNeighbor):

    def __init__(self, ip, **kwargs):
        if not kwargs:
            if isinstance(ip, IPv4Neighbor):
                # Copy constructor
                ip = ip.ip
        if type(ip) is not ipaddress.IPv4Address:
            if isinstance(ip, ipaddress.IPv4Interface):
                ip = ip.ip
            else:
                ip = ipaddress.IPv4Address(ip)
        super().__init__(ip=ip, **kwargs)


class IPv6Neighbor(IPNeighbor):

    def __init__(self, ip, **kwargs):
        if not kwargs:
            if isinstance(ip, IPv6Neighbor):
                # Copy constructor
                ip = ip.ip
        if type(ip) is not ipaddress.IPv6Address:
            if isinstance(ip, ipaddress.IPv6Interface):
                ip = ip.ip
            else:
                ip = ipaddress.IPv6Address(ip)
        super().__init__(ip=ip, **kwargs)


class IPv4LsrNeighbor(IPv4Neighbor):

    label_space = managedattribute(
        name='label_space',
        read_only=True)

    def __init__(self, ip, label_space=None, **kwargs):
        if label_space is None and not kwargs:
            if isinstance(ip, IPv4LsrNeighbor):
                # Copy constructor
                ip, label_space = ip.ip, ip.label_space
            elif type(ip) is str:
                m = re.match(r'^(?P<ip>\d+\.\d+\.\d+\.\d+)(?::(?P<label_space>\d+))?$', ip)
                if m:
                    ip, label_space = m.groups()
            # all other cases should be handled in super().__init__
        if label_space is None:
            label_space = 0
        self._label_space = int(label_space)
        super().__init__(ip=ip, **kwargs)

    def __str__(self):
        return super().__str__() + ':' + str(self.label_space)

    def __repr__(self):
        return '{}(\'{}:{}\')'.format(
            self.__class__.__name__,
            self.ip,
            self.label_space)

    def _neighbor_comparison_tokens(self):
        return super()._neighbor_comparison_tokens() + (
            'label_space', self.label_space,
        )


class IPv4NeighborSubAttributes(KeyedSubAttributes):

    neighbor = managedattribute(
        name='neighbor',
        read_only=True,  # key
        doc='''IPv4Neighbor key''')

    def __init__(self, parent, key):
        self._neighbor = key
        super().__init__(parent=parent)

    @classmethod
    def _sanitize_key(cls, key):
        try:
            key = IPv4Neighbor(key)
        except ValueError:
            pass
        return key

    @classmethod
    def _assert_key_allowed(cls, key):
        if type(key) is not IPv4Neighbor:
            raise KeyError(
                    '{cls} only accepts IPv4Neighbor types, not {key!r}'.
                    format(cls=cls.__name__, key=key))


class IPv4LsrNeighborSubAttributes(KeyedSubAttributes):

    neighbor = managedattribute(
        name='neighbor',
        read_only=True,  # key
        doc='''IPv4LsrNeighbor key''')

    def __init__(self, parent, key):
        self._neighbor = key
        super().__init__(parent=parent)

    @classmethod
    def _sanitize_key(cls, key):
        try:
            key = IPv4LsrNeighbor(key)
        except ValueError:
            pass
        return key

    @classmethod
    def _assert_key_allowed(cls, key):
        if type(key) is not IPv4LsrNeighbor:
            raise KeyError(
                    '{cls} only accepts IPv4LsrNeighbor types, not {key!r}'.
                    format(cls=cls.__name__, key=key))


class IPv6NeighborSubAttributes(KeyedSubAttributes):

    neighbor = managedattribute(
        name='neighbor',
        read_only=True,  # key
        doc='''IPv6Neighbor key''')

    def __init__(self, parent, key):
        self._neighbor = key
        super().__init__(parent=parent)

    @classmethod
    def _sanitize_key(cls, key):
        try:
            key = IPv6Neighbor(key)
        except ValueError:
            pass
        return key

    @classmethod
    def _assert_key_allowed(cls, key):
        if type(key) is not IPv6Neighbor:
            raise KeyError(
                    '{cls} only accepts IPv6Neighbor types, not {key!r}'.
                    format(cls=cls.__name__, key=key))


class IPNeighborSubAttributes(KeyedSubAttributes):

    neighbor = managedattribute(
        name='neighbor',
        read_only=True,  # key
        doc='''IPNeighbor (IPv4Neighbor or IPv6Neighbor) key''')

    def __init__(self, parent, key):
        self._neighbor = key
        super().__init__(parent=parent)

    @classmethod
    def _sanitize_key(cls, key):
        try:
            key = IPv4Neighbor(key)
        except ValueError:
            try:
                key = IPv6Neighbor(key)
            except ValueError:
                pass
        return key

    @classmethod
    def _assert_key_allowed(cls, key):
        if type(key) not in (IPv4Neighbor, IPv6Neighbor):
            raise KeyError(
                    '{cls} only accepts IPNeighbor (v4/v6) types, not {key!r}'.
                    format(cls=cls.__name__, key=key))


class IPLsrNeighborSubAttributes(KeyedSubAttributes):

    neighbor = managedattribute(
        name='neighbor',
        read_only=True,  # key
        doc='''IPv4LsrNeighbor or IPv6Neighbor key''')

    def __init__(self, parent, key):
        self._neighbor = key
        super().__init__(parent=parent)

    @classmethod
    def _sanitize_key(cls, key):
        try:
            key = IPv4LsrNeighbor(key)
        except ValueError:
            try:
                key = IPv6Neighbor(key)
            except ValueError:
                pass
        return key

    @classmethod
    def _assert_key_allowed(cls, key):
        if type(key) not in (IPv4LsrNeighbor, IPv6Neighbor):
            raise KeyError(
                    '{cls} only accepts IPv4LsrNeighbor and IPv6Neighbor types, not {key!r}'.
                    format(cls=cls.__name__, key=key))

