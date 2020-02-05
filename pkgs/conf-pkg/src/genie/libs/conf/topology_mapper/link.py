
import re
import functools

from pyats.topology import Link as ATSLink

from genie.utils.cisco_collections import OrderedSet


class Link(ATSLink):

    @classmethod
    def validate_name(cls, name):
        if re.match(r'^(?:L\d+)$', name):
            return name
        raise ValueError('Not a valid %s name: %r'
                % (cls.__class__.__name__, name))

    def __init__(self, name, **kwargs):
        self.validate_name(name)
        # Parameters
        kwargs.setdefault('label', [])
        # Constraints
        kwargs.setdefault('type', None)
        kwargs.setdefault('interface', None)
        kwargs.setdefault('match_name', None)
        kwargs.setdefault('predicates', None)
        super().__init__(name=name, **kwargs)

    def connect_interface(self, interface):
        '''Post-process base connect_interface and keep the interfaces list in
        dictionnary order.
        '''
        super().connect_interface(interface)

        try:
            from pyats.tcl.internal import DictionaryCompare
            self.interfaces = type(self.interfaces)(
                sorted(self.interfaces, key=functools.cmp_to_key(
                    lambda intf1, intf2: DictionaryCompare(
                        intf1.name, intf2.name))))
        except ImportError:
            # Considering users with no sourced tcl environment
            pass

    @property
    def link_name(self):
        return self.name

    @property
    def device_names(self):
        '''List of Device names (R#) in dictionnary order.
        
        The order is consistent with devices corresponding to self.interfaces
        and self.interface_names but may contain duplicates.
        '''
        sRs = [intf.device_name for intf in self.interfaces]  # R#
        return sRs

    @property
    def interface_names(self):
        '''OrderedSet of Interface names (R#I#) in dictionnary order.

        The order is consistent with devices corresponding to self.interfaces
        and self.device_names.
        '''
        sRIs = OrderedSet([intf.interface_name for intf in self.interfaces])  # R#I#
        return sRIs

# vim: ft=python ts=8 sw=4 et
