"""OSI/ISIS Network Entity Title (NET) implementation
"""

__all__ = (
    'IsisAreaAddress',
    'IsisSystemID',
    'IsisNET',
)

from copy import copy
import re
import functools

from genie.decorator import managedattribute

re_area_address = r'(?:[A-Za-z0-9]{2}(?:\.[A-Za-z0-9]{4}){0,6})'
re_system_id = r'(?:[A-Za-z0-9]{4}\.[A-Za-z0-9]{4}\.[A-Za-z0-9]{4})'
re_nsel = r'(?:[A-Za-z0-9]{2})'


@functools.total_ordering
class IsisAreaAddress(object):

    value = managedattribute(
        name='value',
        fdel=None)

    @value.setter
    def value(self, value):
        m = re.match(r'^' + re_area_address + '$', value)
        if not m:
            raise ValueError(value)
        self._value = value.upper()

    def __init__(self, value=None):

        if isinstance(value, IsisAreaAddress):
            # Copy constructor
            self.value = value.value
            return

        if isinstance(value, str):
            self.value = value
            return

        raise TypeError(value)

    def __eq__(self, other):
        if not isinstance(other, IsisAreaAddress):
            try:
                other = self.__class__(other)
            except Exception:
                return NotImplemented
        return self.value == other.value

    def __lt__(self, other):
        if not isinstance(other, IsisAreaAddress):
            try:
                other = self.__class__(other)
            except Exception:
                return NotImplemented
        return self.value < other.value

    def __hash__(self):
        # TODO mutable!
        return 0

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, str(self))

    def __str__(self):
        return self.value

    def __copy__(self):
        return self.__class__(self)


@functools.total_ordering
class IsisSystemID(object):

    value = managedattribute(
        name='value',
        fdel=None)

    @value.setter
    def value(self, value):
        m = re.match(r'^' + re_system_id + '$', value)
        if not m:
            raise ValueError(value)
        self._value = value.upper()

    def __init__(self, value=None):

        if isinstance(value, IsisSystemID):
            # Copy constructor
            self.value = value.value
            return

        if isinstance(value, str):
            self.value = value
            return

        raise TypeError(value)

    def __eq__(self, other):
        if not isinstance(other, IsisSystemID):
            try:
                other = self.__class__(other)
            except Exception:
                return NotImplemented
        return self.value == other.value

    def __lt__(self, other):
        if not isinstance(other, IsisSystemID):
            try:
                other = self.__class__(other)
            except Exception:
                return NotImplemented
        return self.value < other.value

    def __hash__(self):
        # TODO mutable!
        return 0

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, str(self))

    def __str__(self):
        return self.value

    def __copy__(self):
        return self.__class__(self)


@functools.total_ordering
class IsisNET(object):

    area_address = managedattribute(
        name='area_address',
        fdel=None,
        type=IsisAreaAddress)

    system_id = managedattribute(
        name='system_id',
        fdel=None,
        type=IsisSystemID)

    nsel = managedattribute(
        name='nsel',
        fdel=None)

    @nsel.setter
    def nsel(self, value):
        m = re.match(r'^' + re_nsel + '$', value)
        if not m:
            raise ValueError(value)
        self._nsel = value.upper()

    def __init__(self, value=None, **kwargs):
        if value is None:
            if 'area_address' not in kwargs or 'system_id' not in kwargs:
                raise TypeError('area_address and system_id arguments mandatory.')
            kwargs.setdefault('nsel', '00')
            for attr in (
                    'area_address',
                    'system_id',
                    'nsel',
            ):
                v = kwargs.pop(attr)
                setattr(self, attr, v)
            if kwargs:
                raise TypeError('Unexpected keyword arguments: {}'\
                                .format(', '.join(kwargs.keys())))
            return

        if kwargs:
            raise TypeError('Provide either value or kwargs, not both.')

        if isinstance(value, IsisNET):
            # Copy constructor
            for attr in (
                    'area_address',
                    'system_id',
                    'nsel',
            ):
                v = getattr(value, attr)
                setattr(self, attr, v)
            return

        if isinstance(value, str):
            m = re.match(r'^'
                         r'(?P<area_address>' + re_area_address + r')'
                         r'\.(?P<system_id>' + re_system_id + r')'
                         r'\.(?P<nsel>' + re_nsel + r')'
                         r'$', value)
            if not m:
                raise ValueError(value)
            for k, v in m.groupdict().items():
                setattr(self, k, v)
            return

        raise TypeError(value)

    def __eq__(self, other):
        if not isinstance(other, IsisNET):
            try:
                other = self.__class__(other)
            except Exception:
                return NotImplemented
        return \
            (self.area_address, self.system_id, self.nsel) \
            == \
            (other.area_address, other.system_id, other.nsel)

    def __lt__(self, other):
        if not isinstance(other, IsisNET):
            try:
                other = self.__class__(other)
            except Exception:
                return NotImplemented
        return \
            (self.area_address, self.system_id, self.nsel) \
            < \
            (other.area_address, other.system_id, other.nsel)

    def __hash__(self):
        # TODO mutable!
        return 0

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, str(self))

    def __str__(self):
        return '{}.{}.{}'.format(
            self.area_address,
            self.system_id,
            self.nsel)

    def __copy__(self):
        return self.__class__(self)

