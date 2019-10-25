
__all__ = (
        'VpnId',
        )

from copy import copy
import collections.abc
import re
from enum import Enum
import functools


@functools.total_ordering
class VpnId(object):

    @functools.total_ordering
    class Format(Enum):
        OUI_VPN_index = "OUI:VPN-index"

        def __eq__(self, other):
            if not isinstance(other, VpnId.Format):
                return NotImplemented
            return self is other

        def __lt__(self, other):
            if not isinstance(other, VpnId.Format):
                return NotImplemented
            return self.value < other.value

        __hash__ = Enum.__hash__

    __slots__ = {'_parts'}

    def __init__(self, value):
        super().__init__()

        if isinstance(value, VpnId):
            # Copy constructor
            self.parts = copy(value.parts)
            return

        if isinstance(value, str):
            m = re.match(r'^([0-9A-Fa-f]{1,6}):([0-9A-Fa-f]{1,8})$', value)
            if m:
                oui = int(m.group(1), base=16)
                idx = int(m.group(2), base=16)
                self.parts = [oui, idx]
            else:
                raise ValueError(value)

        elif isinstance(value, collections.abc.Sequence):
            self.parts = value

        else:
            raise ValueError('bad VpnId format: %r' % (value,))

    @property
    def parts(self):
        return self._parts

    @parts.setter
    def parts(self, value):
        if isinstance(value, str):
            raise ValueError(value)
        value = tuple(value)
        if len(value) != 2:
            raise ValueError(value)
        if isinstance(value[0], int) and isinstance(value[1], int):
            if not 0 <= value[0] <= 0xFFFFFF:
                raise ValueError(value)
            if not 0 <= value[1] <= 0xFFFFFFFF:
                raise ValueError(value)
            self._parts = tuple([int(value[0]), int(value[1])])
        else:
            raise ValueError(value)

    @property
    def format(self):
        return VpnId.Format.OUI_VPN_index

    @property
    def oui(self):
        if self.format is not VpnId.Format.OUI_VPN_index:
            raise TypeError
        return self.parts[0]

    @property
    def index(self):
        return self.parts[1]

    def __eq__(self, other):
        if not isinstance(other, VpnId):
            try:
                other = self.__class__(other)
            except Exception:
                return NotImplemented
        return (self.format, self.parts) == (other.format, other.parts)

    def __lt__(self, other):
        if not isinstance(other, VpnId):
            try:
                other = self.__class__(other)
            except Exception:
                return NotImplemented
        return (self.format, self.parts) < (other.format, other.parts)

    def __hash__(self):
        # TODO mutable! return hash((self.format, self.parts))
        return 0

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, str(self),)

    def __str__(self):
        return '%x:%x' % self.parts

    def __copy__(self):
        return self.__class__(self.parts)

