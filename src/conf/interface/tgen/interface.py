'''
    Generic Interface classes for TGEN devices.
'''

__all__ = (
    'Interface',
    'PhysicalInterface',
    'EmulatedInterface',
    'VirtualInterface',
    'SubInterface',
)

import abc

from genie.decorator import managedattribute

import genie.libs.conf.interface


class Interface(genie.libs.conf.interface.Interface):
    '''Base Interface class for TGEN devices'''

    @property
    def streams_tx(self):
        for stream in self.device.streams:
            if stream.source_tgen_interface is self:
                yield stream

    @property
    def streams_rx(self):
        for stream in self.device.streams:
            if self in stream.destination_tgen_interfaces:
                yield stream

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PhysicalInterface(Interface,
                        genie.libs.conf.interface.PhysicalInterface):
    '''Class for physical TGEN interfaces/ports'''

    tgen_port_configured = managedattribute(
        name='tgen_port_configured',
        default=False,
        type=managedattribute.test_istype(bool))

    @property
    def tgen_interface(self):
        '''Return the physical TGEN interface (self)'''
        return self

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EmulatedInterface(Interface,
                        genie.libs.conf.interface.EmulatedInterface):
    '''Class for emulated TGEN interfaces'''

    @property
    def tgen_interface(self):
        '''Return the physical TGEN interface (from emulated device)'''
        return self.device.tgen_interface

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VirtualInterface(Interface,
                       genie.libs.conf.interface.VirtualInterface):
    '''Class for virtual TGEN interfaces'''

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SubInterface(VirtualInterface,
                   genie.libs.conf.interface.SubInterface):
    '''Class for TGEN sub-interfaces

    Typically, TGEN sub-interfaces are purely logical and only meant for
    symmetry with sub-interfaces of normal devices as they do not have a state
    of their own and their configuration is done through their parent
    interface.
    '''

    def build_config(self, apply=True, attributes=None, **kwargs):
        '''SubInterface build_config of TGEN devices does nothing.
        Configuration is done through their parent_interface.
        '''
        return ''  # no CLI

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        '''SubInterface build_unconfig of TGEN devices does nothing.
        Configuration is done through their parent_interface.
        '''
        return ''  # no CLI

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

