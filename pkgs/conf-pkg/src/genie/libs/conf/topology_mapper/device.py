
import re
import functools

from pyats.topology import Device as ATSDevice

from genie.utils.cisco_collections import OrderedSet

try:
    from pyats.tcl.internal import DictionaryCompare
except Exception:
    pass


class Device(ATSDevice):

    @classmethod
    def validate_name(cls, name):
        # TODO Support other types
        if re.match(r'^(?:R\d+|TGEN)$', name):
            return name
        raise ValueError('Not a valid %s name: %r'
                % (cls.__class__.__name__, name))

    def __init__(self, name, **kwargs):
        self.validate_name(name)
        # Parameters
        kwargs.setdefault('label', [])
        kwargs.setdefault('role', [])
        kwargs.setdefault('draw_rank', None)
        kwargs.setdefault('draw_cluster', None)
        # Constraints
        kwargs.setdefault('type', None)
        kwargs.setdefault('match_name', None)
        kwargs.setdefault('platform', None)
        kwargs.setdefault('tgen_platform', None)
        kwargs.setdefault('os', None)
        kwargs.setdefault('multinode_requested', None)
        kwargs.setdefault('predicates', None)
        super().__init__(name=name, **kwargs)

    @property
    def device_name(self):
        return self.name

    @property
    def interface_names(self):
        '''OrderedSet of interface names (#R#I) on this device.'''
        sRIs = [intf.interface_name for intf in self.interfaces.values()]
        sRIs = OrderedSet(sorted(sRIs, key=functools.cmp_to_key(DictionaryCompare)))
        return sRIs

    @property
    def next_interface_name(self):
        I = len(self.interfaces) + 1
        while True:
            sRI = '%sI%d' % (self.name, I)
            if sRI not in self.interfaces:
                return sRI


# vim: ft=python ts=8 sw=4 et
