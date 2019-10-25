
__all__ = (
    'ESI',
)

import functools
from copy import copy
import collections.abc

from genie.libs.conf.base import MAC, IPv4Address


@functools.total_ordering
class ESI(object):
    '''Representation of a EVPN Ethernet Segment Identifier (ESI).
    '''

    __slots__ = {'_type', '_bytes'}

    @classmethod
    def create_type_0(cls, value):
        return cls(value, type=0)

    @classmethod
    def create_type_1(cls, system_mac, port_key):
        return cls(
            (1,)
            + tuple(MAC(system_mac).packed)
            + tuple(int(port_key).to_bytes(2, 'big'))
            + (0,)
        )

    @classmethod
    def create_type_2(cls, root_bridge_mac, root_bridge_priority):
        return cls(
            (2,)
            + tuple(MAC(root_bridge_mac).packed)
            + tuple(int(root_bridge_priority).to_bytes(2, 'big'))
            + (0,)
        )

    @classmethod
    def create_type_3(cls, system_mac, local_discriminator):
        return cls(
            (3,)
            + tuple(MAC(system_mac).packed)
            + tuple(int(local_discriminator).to_bytes(3, 'big'))
        )

    @classmethod
    def create_type_4(cls, router_id, local_discriminator):
        return cls(
            (4,)
            + tuple(IPv4Address(router_id).packed)
            + tuple(int(local_discriminator).to_bytes(4, 'big'))
            + (0,)
        )

    @classmethod
    def create_type_5(cls, asn, local_discriminator):
        return cls(
            (5,)
            + tuple(int(asn).to_bytes(4, 'big'))
            + tuple(int(local_discriminator).to_bytes(4, 'big'))
            + (0,)
        )

    def __init__(self, value, type=None):
        '''
        Args:
            value (:obj:`ESI` to copy, :obj:`str`, sequence of :obj:`int` bytes, or :obj:`int`): The ESI value.
            type (int): The ESI type (Default 0).
        '''
        _type = type
        del type
        super().__init__()

        if isinstance(value, ESI):
            # Copy constructor
            if _type is not None and _type != value.type:
                raise ValueError('cannot switch ESI type '
                                 'using copy constructor!')
            self.bytes = copy(value.bytes)
            self.type = value.type
            return

        if isinstance(value, str):
            if value == '::':
                self.bytes = [0] * 9
            else:
                if '::' in value:
                    try:
                        prefix, suffix = value.split('::')
                    except:
                        raise ValueError('too many :: in ESI: %r' % (value,))
                    prefix = prefix.split(':') if prefix else []
                    suffix = suffix.split(':') if suffix else []
                    if len(prefix) + len(suffix) >= 9:
                        raise ValueError('compressed ESI not composed of less \
                                         than 9 bytes: %r' % (value,))
                    bytes = (
                        [int(v, 16) for v in prefix]
                        + [0] * (9 - len(prefix) - len(suffix))
                        + [int(v, 16) for v in suffix])
                else:
                    if '.' in value:
                        bytes = [int(v, 16) for v in value.split('.')]
                        if len(bytes) == 5:
                            # dotted_hex5words_with_type
                            words = bytes
                            bytes = []
                            for word in words:
                                bytes += [word >> 8, word & 0xFF]
                    else:
                        bytes = [int(v, 16) for v in value.split(':')]
                if len(bytes) == 10:
                    if _type is not None and _type != int(bytes[0]):
                        raise ValueError('type argument does not match value')
                    _type, *self.bytes = bytes
                else:
                    self.bytes = bytes

        elif isinstance(value, collections.abc.Sequence) and len(value) == 10:
            if _type is not None and _type != int(value[0]):
                raise ValueError('type argument does not match value')
            _type, *self.bytes = value

        elif isinstance(value, collections.abc.Sequence) and len(value) == 9:
            self.bytes = value

        elif isinstance(value, int):
            self.value = value

        else:
            raise TypeError('bad ESI format: %r' % (value,))

        if _type is None:
            _type = 0
        self.type = _type

    @property
    def bytes(self):
        '''`tuple` of `int`: ESI value as a sequence of bytes (w/o type)'''
        return self._bytes

    @bytes.setter
    def bytes(self, value):
        if isinstance(value, str) \
                or not isinstance(value, collections.abc.Sequence):
            raise ValueError('ESI bytes sequence expected: %r' % (value,))
        value = tuple(
            (int(byte, 16) if isinstance(byte, str) else int(byte))
            for byte in value)
        if len(value) != 9:
            raise ValueError('ESI not composed of 9 bytes: %r' % (value,))
        for byte in value:
            if not (0 <= byte <= 0xff):
                raise ValueError('ESI bytes out of range: %r' % (value,))
        self._bytes = value

    @property
    def bytes_with_type(self):
        return (self.type,) + self.bytes

    @property
    def words_with_type(self):
        bytes = self.bytes_with_type
        words = []
        while bytes:
            b1, b2, *bytes = bytes
            words.append(b1 << 8 | b2)
        return tuple(words)

    @property
    def type(self):
        '''`int`: Type byte of the ESI'''
        return self._type

    @type.setter
    def type(self, value):
        if not isinstance(value, int) or not (0 <= int(value) <= 5):
            raise ValueError('invalid ESI type: %r' % (value,))
        self._type = int(value)

    @property
    def value(self):
        '''`int`: ESI value as an integer (w/o type)'''
        return sum([
            v << (8 * shift)
            for shift, v in enumerate(reversed(self.bytes))])

    @value.setter
    def value(self, value):
        if not isinstance(value, int):
            raise ValueError('ESI integer value expected: %r' % (value,))
        if not (0 <= value <= 0xffffffffffffffffff):
            raise ValueError('ESI integer value out of range: %r' % (value,))
        self.bytes = [
            value >> (8 * shift) & 0xff
            for shift in reversed(range(9))]

    @property
    def system_mac(self):
        if self.type == 1:
            return MAC(':'.join(str(octet) for octet in self.bytes[0:6]))
        if self.type == 3:
            return MAC(':'.join(str(octet) for octet in self.bytes[0:6]))
        raise AttributeError

    @property
    def root_bridge_mac(self):
        if self.type == 2:
            return MAC(':'.join(str(octet) for octet in self.bytes[0:6]))
        raise AttributeError

    @property
    def router_id(self):
        if self.type == 4:
            return IPv4Address('.'.join(str(octet) for octet in self.bytes[0:4]))
        raise AttributeError

    @property
    def asn(self):
        if self.type == 5:
            return int.from_bytes(self.bytes[0:4], 'big')
        raise AttributeError

    @property
    def port_key(self):
        if self.type == 1:
            return int.from_bytes(self.bytes[6:8], 'big')
        raise AttributeError

    @property
    def root_bridge_priority(self):
        if self.type == 2:
            return int.from_bytes(self.bytes[6:8], 'big')
        raise AttributeError

    @property
    def local_discriminator(self):
        if self.type == 3:
            return int.from_bytes(self.bytes[6:9], 'big')
        if self.type == 4:
            return int.from_bytes(self.bytes[4:8], 'big')
        if self.type == 5:
            return int.from_bytes(self.bytes[4:8], 'big')
        raise AttributeError

    def __eq__(self, other):
        if not isinstance(other, ESI):
            try:
                other = self.__class__(other)
            except Exception:
                return NotImplemented
        return (self.type, self.bytes) == (other.type, other.bytes)

    def __lt__(self, other):
        if not isinstance(other, ESI):
            try:
                other = self.__class__(other)
            except Exception:
                return NotImplemented
        return (self.type, self.bytes) < (other.type, other.bytes)

    def __hash__(self):
        # TODO mutable! return hash((self.type, self.bytes))
        return 0

    def __repr__(self):
        return 'ESI(%r, type=%r)' % (str(self), self.type)

    def __str__(self):
        '''`str`: String representation of the ESI bytes (xx:xx:...:xx).'''
        return ':'.join('%02x' % (byte,) for byte in self.bytes)

    def __copy__(self):
        return self.__class__(self)

    @property
    def dotted(self):
        '''`str`: String representation of the ESI bytes (xx.xx.....xx).'''
        return '.'.join('%02x' % (byte,) for byte in self.bytes)

    @property
    def dotted_with_type(self):
        '''`str`: String representation of the ESI bytes (tt.xx.xx.....xx).'''
        return '.'.join('%02x' % (byte,) for byte in self.bytes_with_type)

    @property
    def dotted_hex5words_with_type(self):
        '''`str`: String representation of the ESI bytes (ttxx.....xxxx).'''
        return '.'.join('%04x' % (word,) for word in self.words_with_type)

    def __format__(self, format_spec):
        if len(format_spec) == 0 or format_spec == 'x:x:x:x:x:x:x:x:x':
            return str(self)
        if format_spec == 'x.x.x.x.x.x.x.x.x':
            return self.dotted
        if format_spec == 't.x.x.x.x.x.x.x.x.x':
            return self.dotted_with_type
        if format_spec == 'tx.xx.xx.xx.xx':
            return self.dotted_hex5words_with_type
        raise ValueError('Invalid format specifier: ' + format_spec)

