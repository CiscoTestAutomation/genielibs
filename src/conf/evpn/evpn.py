
__all__ = (
    'Evpn',
)

from genie.utils.cisco_collections import typedset

from genie.decorator import managedattribute
from genie.conf.base import Base, Interface
import genie.conf.base.attributes
from genie.conf.base.attributes import SubAttributes, SubAttributesDict, AttributesHelper

from genie.libs.conf.base import MAC
from genie.libs.conf.base import RouteDistinguisher, RouteTarget
from genie.libs.conf.base.feature import *
from genie.libs.conf.l2vpn.pseudowire import PseudowireNeighborSubAttributes

from .esi import ESI
from .vni import Vni, VniSubAttributes
from .evi import Evi

# evpn.
#     # Defaults:
#     bgp.
#     ethernet_segment.
#         bgp.
#     load_balancing.
#     # Actual:
#     device_attr[]. (parent = evpn)
#         # Defaults:
#         ethernet_segment. (parent = evpn.ethernet_segment)
#             bgp.
#         # Actual:
#         interface_attr[]. (parent = evpn.device_attr[])
#             ethernet_segment. (parent = evpn.device_attr[].ethernet_segment)
#                 bgp.
#         vni_attr[]. (parent = evpn.device_attr[])
#             ethernet_segment. (parent = evpn.device_attr[].ethernet_segment)
#                 bgp.
#         pw_neighbor_attr[]. (parent = evpn.device_attr[])
#             ethernet_segment. (parent = evpn.device_attr[].ethernet_segment)
#                 bgp.
#         vfi_attr[]. (parent = evpn.device_attr[])
#             ethernet_segment. (parent = evpn.device_attr[].ethernet_segment)
#                 bgp.
#         bgp. (parent = evpn.bgp)
#         load_balancing. (parent = evpn.load_balancing)


class BaseNamespace(Base):
    '''A simple namespace that inherits some attributes from a Base-like object.

    Attributes inherited:
        - testbed
    '''

    base = managedattribute(
        name='base',
        read_only=True,
        doc='''Object that is either a Base or inherits from it.''')

    def __init__(self, base, **kwargs):
        self._base = base
        super().__init__(**kwargs)

    @property
    def testbed(self):
        return self.base.testbed

class DeviceNamespace(BaseNamespace):
    '''A simple namespace that inherits some attributes from a Device-like object.

    Attributes inherited:
        - testbed (BaseNamespace)
        - device_name (if base is a DeviceSubAttributes)
        - device
    '''

    @property
    def device_name(self):
        return self.base.device_name

    @property
    def device(self):
        return self.base.device

class InterfaceNamespace(DeviceNamespace):
    '''A simple namespace that inherits some attributes from a Interface-like object.

    Attributes inherited:
        - testbed (BaseNamespace)
        - device_name (DeviceNamespace)
        - device (DeviceNamespace)
        - interface_name (if base is a InterfaceSubAttributes)
        - interface
    '''

    @property
    def interface_name(self):
        return self.base.interface_name

    @property
    def interface(self):
        return self.base.interface

class PseudowireNeighborNamespace(BaseNamespace):
    pass

class VfiNamespace(BaseNamespace):
    pass

class VniNamespace(BaseNamespace):
    '''A simple namespace that inherits some attributes from a Vni-like object.

    Attributes inherited:
        - testbed (BaseNamespace)
        - vni (if base is a VniAttributes)
        - vni_id
    '''

    @property
    def vni_id(self):
        return self.base.vni_id

    @property
    def vni(self):
        return self.base.vni

class VfiSubAttributes(genie.conf.base.attributes.KeyedSubAttributes):

    vfi_name = managedattribute(
                name='vfi_name',
                read_only=True)

    def __init__(self, parent, key):
        assert isinstance(key, str)
        self._vfi_name = key
        super().__init__(parent=parent)

class Evpn(DeviceFeature, InterfaceFeature):

    class DefaultDeviceBgpAttributes(BaseNamespace):

        enabled = managedattribute(
            name='enabled',
            default=False,
            type=managedattribute.test_istype(bool))

        rd = managedattribute(
            name='rd',
            default=None,
            type=(None, RouteDistinguisher))

    bgp = managedattribute(
        name='bgp',
        read_only=True,
        doc=DefaultDeviceBgpAttributes.__doc__)

    @bgp.initter
    def bgp(self):
        return self.DefaultDeviceBgpAttributes(base=self)

    evis = managedattribute(
        name='evis',
        finit=typedset(managedattribute.test_isinstance(Evi)).copy,
        type=typedset(managedattribute.test_isinstance(Evi))._from_iterable,
        doc='A `set` of Evi associated objects')

    def add_evi(self, evi):  # TODO DEPRECATE
        self.evis.add(evi)

    def remove_evi(self, evi):  # TODO DEPRECATE
        self.evis.remove(evi)

    class InterfaceAttributes(genie.conf.base.attributes.InterfaceSubAttributes):

        class EthernetSegmentAttributes(InterfaceNamespace, SubAttributes):

            esi = managedattribute(
                name='esi',
                default=None,
                type=(None, ESI))

            class BgpAttributes(InterfaceNamespace, SubAttributes):

                def __init__(self, base):
                    super().__init__(
                        base=base,
                        # Evpn.device_attr[].ethernet_segment.bgp
                        parent=base.parent.ethernet_segment.bgp)

            bgp = managedattribute(
                name='bgp',
                read_only=True,
                doc=BgpAttributes.__doc__)

            @bgp.initter
            def bgp(self):
                return self.BgpAttributes(base=self.base)

            def __init__(self, base):
                super().__init__(
                    base=base,
                    # Evpn.device_attr[].ethernet_segment
                    parent=base.parent.ethernet_segment)

        ethernet_segment = managedattribute(
            name='ethernet_segment',
            read_only=True,
            doc=EthernetSegmentAttributes.__doc__)

        @ethernet_segment.initter
        def ethernet_segment(self):
            return self.EthernetSegmentAttributes(base=self)

        def __init__(self, parent, key):
            super().__init__(parent, key)

    class PseudowireNeighborAttributes(PseudowireNeighborSubAttributes):

        class EthernetSegmentAttributes(PseudowireNeighborNamespace, SubAttributes):

            esi = managedattribute(
                name='esi',
                default=None,
                type=(None, ESI))

            class BgpAttributes(PseudowireNeighborNamespace, SubAttributes):

                def __init__(self, base):
                    super().__init__(
                        base=base,
                        # Evpn.device_attr[].ethernet_segment.bgp
                        parent=base.parent.ethernet_segment.bgp)

            bgp = managedattribute(
                name='bgp',
                read_only=True,
                doc=BgpAttributes.__doc__)

            @bgp.initter
            def bgp(self):
                return self.BgpAttributes(base=self.base)

            def __init__(self, base):
                super().__init__(
                    base=base,
                    # Evpn.device_attr[].ethernet_segment
                    parent=base.parent.ethernet_segment)

        ethernet_segment = managedattribute(
            name='ethernet_segment',
            read_only=True,
            doc=EthernetSegmentAttributes.__doc__)

        @ethernet_segment.initter
        def ethernet_segment(self):
            return self.EthernetSegmentAttributes(base=self)

        def __init__(self, parent, key):
            super().__init__(parent, key)

    class VfiAttributes(VfiSubAttributes):

        class EthernetSegmentAttributes(VfiNamespace, SubAttributes):

            esi = managedattribute(
                name='esi',
                default=None,
                type=(None, ESI))

            class BgpAttributes(VfiNamespace, SubAttributes):

                def __init__(self, base):
                    super().__init__(
                        base=base,
                        # Evpn.device_attr[].ethernet_segment.bgp
                        parent=base.parent.ethernet_segment.bgp)

            bgp = managedattribute(
                name='bgp',
                read_only=True,
                doc=BgpAttributes.__doc__)

            @bgp.initter
            def bgp(self):
                return self.BgpAttributes(base=self.base)

            def __init__(self, base):
                super().__init__(
                    base=base,
                    # Evpn.device_attr[].ethernet_segment
                    parent=base.parent.ethernet_segment)

        ethernet_segment = managedattribute(
            name='ethernet_segment',
            read_only=True,
            doc=EthernetSegmentAttributes.__doc__)

        @ethernet_segment.initter
        def ethernet_segment(self):
            return self.EthernetSegmentAttributes(base=self)

        def __init__(self, parent, key):
            super().__init__(parent, key)

    class VniAttributes(VniSubAttributes):

        class EthernetSegmentAttributes(VniNamespace, SubAttributes):

            esi = managedattribute(
                name='esi',
                default=None,
                type=(None, ESI))

            class BgpAttributes(VniNamespace, SubAttributes):

                def __init__(self, base):
                    super().__init__(
                        base=base,
                        # Evpn.device_attr[].ethernet_segment.bgp
                        parent=base.parent.ethernet_segment.bgp)

            bgp = managedattribute(
                name='bgp',
                read_only=True,
                doc=BgpAttributes.__doc__)

            @bgp.initter
            def bgp(self):
                return self.BgpAttributes(base=self.base)

            def __init__(self, base):
                super().__init__(
                    base=base,
                    # Evpn.device_attr[].ethernet_segment
                    parent=base.parent.ethernet_segment)

        ethernet_segment = managedattribute(
            name='ethernet_segment',
            read_only=True,
            doc=EthernetSegmentAttributes.__doc__)

        @ethernet_segment.initter
        def ethernet_segment(self):
            return self.EthernetSegmentAttributes(base=self)

        def __init__(self, parent, key):
            super().__init__(parent, key)

    class DefaultInterfaceEthernetSegmentAttributes(BaseNamespace):

        enabled = managedattribute(
            name='enabled',
            default=False,
            type=managedattribute.test_istype(bool))

        backbone_source_mac = managedattribute(
            name='backbone_source_mac',
            default=None,
            type=(None, MAC))

        class DefaultBgpAttributes(BaseNamespace):

            enabled = managedattribute(
                name='enabled',
                default=False,
                type=managedattribute.test_istype(bool))

            import_route_target = managedattribute(
                name='import_route_target',
                default=None,
                type=(None, MAC))  # Yes, this corresponds to the system_mac/root_bridge_mac of type 1/2/3 ESIs

        bgp = managedattribute(
            name='bgp',
            read_only=True,
            doc=DefaultBgpAttributes.__doc__)

        @bgp.initter
        def bgp(self):
            return self.DefaultBgpAttributes(base=self.base)

        force_single_homed = managedattribute(
            name='force_single_homed',
            default=False,
            type=managedattribute.test_istype(bool))

        esi = managedattribute(
            name='esi',
            default=None,
            type=(None, ESI))

        load_balancing_mode = managedattribute(
            name='load_balancing_mode',
            default=None,
            type=(None, managedattribute.test_istype(str)))

    ethernet_segment = managedattribute(
        name='ethernet_segment',
        read_only=True,
        doc=DefaultInterfaceEthernetSegmentAttributes.__doc__)

    @ethernet_segment.initter
    def ethernet_segment(self):
        return self.DefaultInterfaceEthernetSegmentAttributes(base=self)

    mac_flush = managedattribute(
        name='mac_flush',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    recovery_timer = managedattribute(
        name='recovery_timer',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    peering_timer = managedattribute(
        name='peering_timer',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    source_interface = managedattribute(
        name='source_interface',
        default=None,
        type=(None, managedattribute.test_isinstance(Interface)))

    class DefaultDeviceLoadBalancingAttributes(BaseNamespace):

        enabled = managedattribute(
            name='enabled',
            default=False,
            type=(None, managedattribute.test_istype(bool)))

        flow_label_static = managedattribute(
            name='flow_label_static',
            default=None,
            type=(None, managedattribute.test_istype(bool)))

    load_balancing = managedattribute(
        name='load_balancing',
        read_only=True,
        doc=DefaultDeviceLoadBalancingAttributes.__doc__)

    @load_balancing.initter
    def load_balancing(self):
        return self.DefaultDeviceLoadBalancingAttributes(base=self)

    class DeviceAttributes(genie.conf.base.attributes.DeviceSubAttributes):

        replication_type = managedattribute(
            name='replication_type',
            default=None,
            type=(None,str))

        label_mode = managedattribute(
            name='label_mode',
            default=None,
            type=(None,str))

        arp_flooding_suppression = managedattribute(
            name='arp_flooding_suppression',
            default=None,
            type=(None,bool))

        interface_attr = managedattribute(
            name='interface_attr',
            read_only=True,
            #doc=Evpn.InterfaceAttributes.__doc__,
            doc='Interface-specific attributes. See Evpn.InterfaceAttributes')

        @interface_attr.initter
        def interface_attr(self):
            return SubAttributesDict(Evpn.InterfaceAttributes, parent=self)

        pw_neighbor_attr = managedattribute(
            name='pw_neighbor_attr',
            read_only=True,
            doc='pw-neighbor-specific attributes. See Evpn.PseudowireNeighborAttributes')

        @pw_neighbor_attr.initter
        def pw_neighbor_attr(self):
            return SubAttributesDict(Evpn.PseudowireNeighborAttributes, parent=self)

        vfi_attr = managedattribute(
            name='vfi_attr',
            read_only=True,
            doc='vfi-specific attributes. See Evpn.VfiAttributes')

        @vfi_attr.initter
        def vfi_attr(self):
            return SubAttributesDict(Evpn.VfiAttributes, parent=self)

        vni_attr = managedattribute(
            name='vni_attr',
            read_only=True,
            #doc=Evpn.VniAttributes.__doc__,
            doc='VNI-specific attributes. See Evpn.VniAttributes')

        @vni_attr.initter
        def vni_attr(self):
            return SubAttributesDict(Evpn.VniAttributes, parent=self)

        class BgpAttributes(DeviceNamespace, SubAttributes):

            def __init__(self, base):
                super().__init__(
                    base=base,
                    # Evpn.bgp
                    parent=base.parent.bgp)

        bgp = managedattribute(
            name='bgp',
            read_only=True,
            doc=BgpAttributes.__doc__)

        @bgp.initter
        def bgp(self):
            return self.BgpAttributes(base=self)

        class DefaultInterfaceEthernetSegmentAttributes(DeviceNamespace, SubAttributes):

            class BgpAttributes(DeviceNamespace, SubAttributes):

                def __init__(self, base):
                    super().__init__(
                        base=base,
                        # Evpn.ethernet_segment.bgp
                        parent=base.parent.ethernet_segment.bgp)

            bgp = managedattribute(
                name='bgp',
                read_only=True,
                doc=BgpAttributes.__doc__)

            @bgp.initter
            def bgp(self):
                return self.BgpAttributes(base=self.base)

            esi = managedattribute(
                name='esi',
                default=None,
                type=(None, ESI))

            def __init__(self, base):
                super().__init__(
                    base=base,
                    # Evpn.ethernet_segment
                    parent=base.parent.ethernet_segment)

        ethernet_segment = managedattribute(
            name='ethernet_segment',
            read_only=True,
            doc=DefaultInterfaceEthernetSegmentAttributes.__doc__)

        @ethernet_segment.initter
        def ethernet_segment(self):
            return self.DefaultInterfaceEthernetSegmentAttributes(base=self)

        class LoadBalancingAttributes(DeviceNamespace, SubAttributes):

            def __init__(self, base):
                super().__init__(
                    base=base,
                    # Evpn.load_balancing
                    parent=base.parent.load_balancing)

        load_balancing = managedattribute(
            name='load_balancing',
            read_only=True,
            doc=LoadBalancingAttributes.__doc__)

        @load_balancing.initter
        def load_balancing(self):
            return self.LoadBalancingAttributes(base=self)

        @property
        def evis(self):
            '''EVIs on this device'''
            device = self.device
            for evi in self.parent.evis:
                if evi.device is device:
                    yield evi

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
        assert getattr(device, 'evpn', None) is None
        device.evpn = self

    def _on_removed_from_device(self, device):
        assert getattr(device, 'evpn', None) is self
        super()._on_removed_from_device(device)
        device.evpn = None

    def _on_added_from_interface(self, interface):
        super()._on_added_from_interface(interface)
        assert getattr(interface, 'evpn', None) is None
        interface.evpn = self

    def _on_removed_from_interface(self, interface):
        assert getattr(interface, 'evpn', None) is self
        super()._on_removed_from_interface(interface)
        interface.evpn = None

    def build_config(self, devices=None, interfaces=None,
                     apply=True, attributes=None):
        attributes = AttributesHelper(self, attributes)
        cfgs = {}

        devices, interfaces, links = consolidate_feature_args(self, devices, interfaces, None)

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr',
                keys=devices, sort=True):
            cfgs[key] = sub.build_config(apply=False, attributes=attributes2,
                                         interfaces=interfaces)
        cfgs = {key: value for key, value in cfgs.items() if value}

        if apply:
            self.testbed.config_on_devices(cfgs, fail_invalid=True)
        else:
            return cfgs

    def build_unconfig(self, devices=None, interfaces=None,
                       apply=True, attributes=None):
        attributes = AttributesHelper(self, attributes)
        cfgs = {}

        devices, interfaces, links = consolidate_feature_args(self, devices, interfaces, None)

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr',
                keys=devices, sort=True):
            cfgs[key] = sub.build_unconfig(apply=False, attributes=attributes2,
                                           interfaces=interfaces)
        cfgs = {key: value for key, value in cfgs.items() if value}

        if apply:
            self.testbed.config_on_devices(cfgs, fail_invalid=True)
        else:
            return cfgs

