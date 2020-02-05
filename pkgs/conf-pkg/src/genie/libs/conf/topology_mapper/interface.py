
import re

from pyats.topology import Interface as ATSInterface


class Interface(ATSInterface):

    @classmethod
    def validate_name(cls, name):
        if re.match(r'^(?:I\d+)$', name):
            return name
        raise ValueError('Not a valid %s "I#" name: %r'
                % (cls.__class__.__name__, name))

    @classmethod
    def validate_name_RI(cls, name):
        if re.match(r'^(?:R\d+|TGEN)(?:I\d+)$', name):
            return name
        raise ValueError('Not a valid %s "R#I#" name: %r'
                % (cls.__class__.__name__, name))

    def __init__(self, name, **kwargs):
        self.validate_name_RI(name)
        # Parameters
        kwargs.setdefault('label', [])
        # Constraints
        #kwargs.setdefault('router', None)
        kwargs.setdefault('match_name', None)
        kwargs.setdefault('type', None)
        #kwargs.setdefault('engine', None)
        kwargs.setdefault('product_id', None)
        #kwargs.setdefault('diff_slot', None)
        #kwargs.setdefault('same_slot', None)
        kwargs.setdefault('predicates', None)
        super().__init__(name=name, **kwargs)

    @property
    def interface_name(self):
        return self.name # R#I#

    @property
    def device_name(self):
        return self.device.device_name # R#

# vim: ft=python ts=8 sw=4 et
