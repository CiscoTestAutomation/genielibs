"""RouteTarget type implementation

A RouteTarget is distinct from a RouteDistinguisher but has the same type 0/1/2
format.
"""

__all__ = (
        'RouteTarget',
        )

from copy import copy
import collections.abc
import re
from ipaddress import IPv4Address
from enum import Enum
import functools
import struct

from genie.decorator import managedattribute


@functools.total_ordering
class RouteTargetType(Enum):
    ASN2_index = (0, "ASN2:index", struct.Struct('!BHL'))
    IPv4Address_index = (1, "IPv4Address:index", struct.Struct('!BLH'))
    ASN4_index = (2, "ASN4:index", struct.Struct('!BLH'))

    def __init__(self, type, format_str, struct_format):
        self.__class__._value2member_map_[type] = self
        self.__class__._value2member_map_[format_str] = self

    @property
    def type(self):
        return self.value[0]

    @property
    def format_str(self):
        return self.value[1]

    @property
    def struct_format(self):
        return self.value[2]

    def __str__(self):
        return self.format_str

    def __int__(self):
        return self.type

    def __eq__(self, other):
        if not isinstance(other, RouteTargetType):
            try:
                other = self.__class__(other)
            except Exception:
                return NotImplemented
        return self.type is other.type

    def __lt__(self, other):
        if not isinstance(other, RouteTargetType):
            try:
                other = self.__class__(other)
            except Exception:
                return NotImplemented
        return self.type < other.type

    __hash__ = Enum.__hash__


@functools.total_ordering
class RouteTargetImportExport(object):

    route_target = managedattribute(
        name='route_target',
        read_only=True)  # (read-only hash key)

    stitching = False

    def __init__(self, route_target, *, stitching=None):
        if stitching is None and isinstance(route_target, RouteTargetImportExport):
            # copy constructor
            route_target, stitching = \
                route_target.route_target, \
                route_target.stitching
        self._route_target = RouteTarget(route_target)
        self.stitching = bool(stitching)

    def __eq__(self, other):
        if not isinstance(other, RouteTargetImportExport):
            return NotImplemented
        return (self.route_target, self.stitching) \
            == (other.route_target, other.stitching)

    def __lt__(self, other):
        if not isinstance(other, RouteTargetImportExport):
            return NotImplemented
        return (self.route_target, self.stitching) \
            < (other.route_target, other.stitching)

    def __hash__(self):
        # return hash((self.route_target, self.stitching))
        return hash(self.route_target)

    def __repr__(self):
        return '%s(%r%s)' % (
            self.__class__.__name__,
            self.route_target,
            ', stitching=%r' % (self.stitching,) if self.stitching else '')


@functools.total_ordering
class RouteTarget(object):

    __slots__ = {'_fields'}

    Type = RouteTargetType

    ImportExport = RouteTargetImportExport

    def create_import_export(self, **kwargs):
        return self.ImportExport(route_target=self, **kwargs)

    def __init__(self, value, *, type=None):
        type_ = type
        del type
        super().__init__()

        if type_ is not None:
            type_ = RouteTargetType(type_)

        if isinstance(value, RouteTarget):
            # Copy constructor
            if type_ is not None and type_ is not value.type:
                raise TypeError
            self._fields = value._fields  # no need to copy a tuple
            return

        if isinstance(value, str):

            m = re.match(r'^(\d+\.\d+\.\d+\.\d+):(\d+)$', value)
            if m:
                # IPv4Address:index
                if type_ is None:
                    type_ = RouteTargetType.IPv4Address_index
                elif type_ is not RouteTargetType.IPv4Address_index:
                    raise TypeError
                ip = IPv4Address(m.group(1))
                idx = int(m.group(2))
                self.fields = [type_, ip, idx]
                return

            m = re.match(r'^(\d+):(\d+)$', value)
            if m:
                # ASN2:index or ASN4:index
                asn = int(m.group(1))
                idx = int(m.group(2))
                if type_ is None:
                    type_ = RouteTargetType.ASN2_index if asn <= 0xFFFF else \
                            RouteTargetType.ASN4_index
                elif type_ not in (
                        RouteTargetType.ASN2_index,
                        RouteTargetType.ASN4_index):
                    raise TypeError
                self.fields = [type_, asn, idx]
                return

            m = re.match(r'^(\d+)\.(\d+):(\d+)$', value)
            if m:
                # "dotted" ASN4:index
                asnh = int(m.group(1))
                asnl = int(m.group(2))
                idx = int(m.group(3))
                if type_ is None:
                    type_ = RouteTargetType.ASN4_index
                elif type_ is not RouteTargetType.ASN4_index:
                    raise TypeError
                if asnh > 0xFFFF or asnl > 0xFFFF:
                    raise ValueError(value)
                asn = asnh << 16 | asnl
                self.fields = [type_, asn, idx]
                return

            m = re.match(r'^([0-9a-fA-F]{1,4})'
                         r'\.([0-9a-fA-F]{1,4})'
                         r'\.([0-9a-fA-F]{1,4})$', value)
            if m:
                # "dotted_hex3words" ASN2:index or ASN4:index
                w1 = int(m.group(1), 16)
                w2 = int(m.group(2), 16)
                w3 = int(m.group(3), 16)
                if type_ is None:
                    type_ = RouteTargetType.ASN2_index \
                        if w1 == 0 \
                        else RouteTargetType.ASN4_index
                if type_ is RouteTargetType.ASN2_index:
                    asn = w1
                    idx = w2 << 16 | w3
                    self.fields = [type_, asn, idx]
                elif type_ is RouteTargetType.ASN4_index:
                    ip = IPv4Address(w1 << 16 | w2)
                    idx = w3
                    self.fields = [type_, ip, idx]
                elif type_ is RouteTargetType.ASN4_index:
                    asn = w1 << 16 | w2
                    idx = w3
                    self.fields = [type_, asn, idx]
                else:
                    raise TypeError
                return

            raise ValueError(value)

        if isinstance(value, collections.abc.Sequence):
            if type_ is not None:
                raise TypeError
            self.fields = value
            return

        raise ValueError('bad RouteTarget format: %r' % (value,))

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, value):
        if isinstance(value, str):
            raise ValueError(value)
        value = list(value)
        if not value:
            raise ValueError(value)
        value[0] = RouteTargetType(value[0])
        if value[0] is RouteTargetType.ASN2_index:
            if len(value) != 3:
                raise ValueError(value)
            value[1] = int(value[1])
            value[2] = int(value[2])
            if not (0 <= value[1] <= 0xFFFF and 0 <= value[2] <= 0xFFFFFFFF):
                raise ValueError(value)
        elif value[0] is RouteTargetType.IPv4Address_index:
            value[1] = IPv4Address(value[1])
            value[2] = int(value[2])
            if not (0 <= value[2] <= 0xFFFF):
                raise ValueError(value)
        elif value[0] is RouteTargetType.ASN4_index:
            if len(value) != 3:
                raise ValueError(value)
            value[1] = int(value[1])
            value[2] = int(value[2])
            if not (0 <= value[1] <= 0xFFFFFFFF and 0 <= value[2] <= 0xFFFF):
                raise ValueError(value)
        else:
            raise ValueError(value)
        self._fields = tuple(value)

    @property
    def type(self):
        return self.fields[0]

    @property
    def ip(self):
        if self.type is RouteTargetType.IPv4Address_index:
            return copy(self.fields[1])
        else:
            raise TypeError

    @property
    def asn(self):
        if self.type in (
                RouteTargetType.ASN2_index,
                RouteTargetType.ASN4_index,
                ):
            return self.fields[1]
        else:
            raise TypeError

    @property
    def index(self):
        if self.type in (
                RouteTargetType.ASN2_index,
                RouteTargetType.IPv4Address_index,
                RouteTargetType.ASN4_index,
                ):
            return self.fields[2]
        else:
            raise TypeError

    def __eq__(self, other):
        if not isinstance(other, RouteTarget):
            try:
                other = self.__class__(other, type=self.type)
            except Exception:
                return NotImplemented
        return self.fields == other.fields

    def __lt__(self, other):
        if not isinstance(other, RouteTarget):
            try:
                other = self.__class__(other, type=self.type)
            except Exception:
                return NotImplemented
        return self.fields < other.fields

    def __hash__(self):
        # TODO mutable! return hash(self.fields)
        return 0

    def __repr__(self):
        if (self.type is RouteTargetType.ASN4_index
            and self.asn <= 0xFFFF) \
            or (self.type is RouteTargetType.ASN2_index
                and self.asn > 0xFFFF):
            return '%s(%r, type=%s)' % (
                self.__class__.__name__,
                str(self),
                self.type)
        else:
            # Unambiguous
            return '%s(%r)' % (
                self.__class__.__name__,
                str(self))

    def __str__(self):
        return ':'.join(str(p) for p in self.fields[1:])

    def __copy__(self):
        return self.__class__(self)

    @property
    def dotted(self):
        if self.type is RouteTargetType.ASN4_index:
            # 1.2:3 "dotted" format as seen on Nexus
            # "The AS number can a 32-bit integer in the form of a higher
            # 16-bit decimal number and a lower 16-bit decimal number in xx.xx
            # format"
            return "%d.%d:%d" % self.value_words
        else:
            return str(self)

    @property
    def packed(self):
        return self.type.struct_format.pack(*[int(v) for v in self.fields])

    @property
    def value_packed(self):
        return self.packed[1:]

    @property
    def bytes(self):
        return struct.unpack('B' * 7, self.packed)

    @property
    def value_bytes(self):
        return struct.unpack('B' * 6, self.value_packed)

    @property
    def value_words(self):
        return struct.unpack('!HHH', self.value_packed)

    @property
    def dotted_hex3words(self):
        return '%04x.%04x.%04x' % self.value_words

    def __format__(self, format_spec):
        if len(format_spec) == 0 or format_spec == 'd:d':
            return str(self)
        if format_spec == 'x.x.x':
            return self.dotted_hex3words
        if format_spec == 'd.d:d':
            return self.dotted
        raise ValueError('Invalid format specifier: ' + format_spec)

