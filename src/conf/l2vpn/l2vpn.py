
__all__ = (
        'L2vpn',
        )

import collections

from genie.utils.cisco_collections import typedset

from genie.decorator import managedattribute
from genie.conf.base import DeviceFeature
import genie.conf.base.attributes
from genie.conf.base.attributes import SubAttributes, SubAttributesDict, AttributesInheriter, AttributesHelper

from genie.libs.conf.base import IPv4Address, MAC
from .bridge_domain import BridgeDomain
from .g8032 import G8032Ring
from .pseudowire import PseudowireClass
from .xconnect import Xconnect

ForwardingInjectLocalMac = collections.namedtuple(
    'ForwardingInjectLocalMac',
    ('mac_address', 'interface', 'location'))

class L2vpn(DeviceFeature):
    
    ForwardingInjectLocalMac = ForwardingInjectLocalMac

    bridge_domains = managedattribute(
        name='bridge_domains',
        finit=typedset(managedattribute.test_isinstance(BridgeDomain)).copy,
        type=typedset(managedattribute.test_isinstance(BridgeDomain))._from_iterable,
        doc='A `set` of BridgeDomain associated objects')

    def add_bridge_domain(self, bridge_domain):  # TODO DEPRECATE
        self.bridge_domains.add(bridge_domain)

    def remove_bridge_domain(self, bridge_domain):  # TODO DEPRECATE
        self.bridge_domains.remove(bridge_domain)

    g8032_rings = managedattribute(
        name='g8032_rings',
        finit=typedset(managedattribute.test_isinstance(G8032Ring)).copy,
        type=typedset(managedattribute.test_isinstance(G8032Ring))._from_iterable,
        doc='A `set` of G.8032 Ring associated objects')

    def add_g8032_ring(self, g8032_ring):  # TODO DEPRECATE
        self.g8032_rings.add(g8032_ring)

    def remove_g8032_ring(self, g8032_ring):  # TODO DEPRECATE
        self.g8032_rings.remove(g8032_ring)

    pseudowire_classes = managedattribute(
        name='pseudowire_classes',
        finit=typedset(managedattribute.test_isinstance(PseudowireClass)).copy,
        type=typedset(managedattribute.test_isinstance(PseudowireClass))._from_iterable,
        doc='A `set` of Pseudowire Class associated objects')

    def add_pseudowire_class(self, pseudowire_class):  # TODO DEPRECATE
        self.pseudowire_classes.add(pseudowire_class)

    def remove_pseudowire_class(self, pseudowire_class):  # TODO DEPRECATE
        self.pseudowire_classes.remove(pseudowire_class)

    xconnects = managedattribute(
        name='xconnects',
        finit=typedset(managedattribute.test_isinstance(Xconnect)).copy,
        type=typedset(managedattribute.test_isinstance(Xconnect))._from_iterable,
        doc='A `set` of Xconnect associated objects')

    def add_xconnect(self, xconnect):  # TODO DEPRECATE
        self.xconnects.add(xconnect)

    def remove_xconnect(self, xconnect):  # TODO DEPRECATE
        self.xconnects.remove(xconnect)

    class DefaultDevicePbbAttributes(object):

        enabled = managedattribute(
            name='enabled',
            default=False,
            type=managedattribute.test_istype(bool))

        backbone_source_mac = managedattribute(
            name='backbone_source_mac',
            default=None,
            type=(None, MAC))

    pbb = managedattribute(
        name='pbb',
        read_only=True,
        finit=DefaultDevicePbbAttributes,
        doc=DefaultDevicePbbAttributes.__doc__)

    class DeviceAttributes(genie.conf.base.attributes.DeviceSubAttributes):

        router_id = managedattribute(
            name='router_id',
            default=None,
            type=(None, IPv4Address))

        forwarding_inject_local_macs = managedattribute(
            name='forwarding_inject_local_macs',
            finit=set)
            #finit=typedset(ForwardingInjectLocalMac).copy,
            #type=typedset(ForwardingInjectLocalMac)._from_iterable)

        class PbbAttributes(SubAttributes):

            def __init__(self, _device_attr):
                self._device_attr = _device_attr
                super().__init__(
                        # L2vpn.pbb
                        parent=_device_attr.parent.pbb)

            @property
            def testbed(self):
                return self._device_attr.testbed

            @property
            def device_name(self):
                return self._device_attr.device_name

            @property
            def device(self):
                return self._device_attr.device

        pbb = managedattribute(
            name='pbb',
            read_only=True,
            doc=PbbAttributes.__doc__)

        @pbb.initter
        def pbb(self):
            return self.PbbAttributes(_device_attr=self)

        @property
        def bridge_domains(self):
            device = self.device
            for bd in self.parent.bridge_domains:
                if device in bd.devices:
                    yield bd

        @property
        def g8032_rings(self):
            device = self.device
            for ring in self.parent.g8032_rings:
                if device in ring.devices:
                    yield ring

        @property
        def pseudowire_classes(self):
            device = self.device
            for pwc in self.parent.pseudowire_classes:
                if device in pwc.devices:
                    yield pwc

        @property
        def xconnects(self):
            device = self.device
            for xc in self.parent.xconnects:
                if device in xc.devices:
                    yield xc

        def __init__(self, parent, key):
            super().__init__(parent, key)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _on_added_from_device(self, device):
        super()._on_added_from_device(device)
        assert getattr(device, 'l2vpn', None) is None
        device.l2vpn = self

    def _on_removed_from_device(self, device):
        assert getattr(device, 'l2vpn', None) is self
        super()._on_removed_from_device(device)
        device.l2vpn = None

    def build_config(self, devices=None, apply=True,
            attributes=None,
            **kwargs):
        cfgs = {}
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)

        if devices is None:
            devices = self.devices
        devices = set(devices)

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr',
                keys=devices, sort=True):
            cfgs[key] = sub.build_config(apply=False, attributes=attributes2)

        if apply:
            self.testbed.config_on_devices(cfgs, fail_invalid=True)
        else:
            return cfgs

    def build_unconfig(self, devices=None, apply=True,
            attributes=None,
            **kwargs):
        cfgs = {}
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)

        if devices is None:
            devices = self.devices
        devices = set(devices)

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr',
                keys=devices, sort=True):
            cfgs[key] = sub.build_unconfig(apply=False, attributes=attributes2)

        if apply:
            self.testbed.config_on_devices(cfgs, fail_invalid=True)
        else:
            return cfgs

