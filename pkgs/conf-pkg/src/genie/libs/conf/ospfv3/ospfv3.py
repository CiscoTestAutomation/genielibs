
__all__ = (
    'Ospfv3',
)

# Python
from enum import Enum

# Genie
from genie.utils.cisco_collections import OrderedSet, typedset
from genie.decorator import managedattribute
from genie.conf.base.config import CliConfig
from genie.conf.base.base import DeviceFeature, LinkFeature

from genie.libs.conf.base import Routing
from genie.libs.conf.vrf import Vrf, VrfSubAttributes
from genie.libs.conf.address_family import AddressFamily, AddressFamilySubAttributes
from genie.conf.base.attributes import DeviceSubAttributes, SubAttributesDict,\
    AttributesHelper, KeyedSubAttributes,\
    InterfaceSubAttributes

# Multi-line config classes
from .arearange import AreaRange
from .arearoutemap import AreaRouteMap
from .summaryaddress import SummaryAddress
from .areadefaultcost import AreaDefaultCost
from .gracefulrestart import GracefulRestart


# OSPFv3 Heirarchy
# --------------
# Ospfv3
#     +- DeviceAttributes
#         +- VrfAttributes
#             +- AddressFamilyAttributes
#             +- AreaAttributes
#                 +- InterfaceAttributes
#                 +- VirtualLinkAttributes


class Ospfv3(Routing, DeviceFeature, LinkFeature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # ==========================================================================
    #                           CONF CLASS STRUCTURE
    # ==========================================================================

    # +- DeviceAttributes
    class DeviceAttributes(DeviceSubAttributes):

        # +- DeviceAttributes
        #   +- VrfAttributes
        class VrfAttributes(VrfSubAttributes):

            # Graceful Restart multi-line configs
            gr_keys = managedattribute(
                name='gr_keys',
                finit=OrderedSet,
                type=OrderedSet()._from_iterable,
                doc='A `set` of GracefulRestart keys objects')

            def add_gr_key(self, gr_key):
                self.gr_keys.add(gr_key)

            def remove_gr_key(self, gr_key):
                gr_key._device = None
                try:
                    self.gr_keys.remove(gr_key)
                except:
                    pass
            # +- DeviceAttributes
            #   +- VrfAttributes
            #      +- AddressFamilyAttributes

            class AddressFamilyAttributes(AddressFamilySubAttributes):

                def __init__(self, parent, key):
                    super().__init__(parent, key)

                # summary-address multi-line configs
                sumadd_keys = managedattribute(
                    name='sumadd_keys',
                    finit=OrderedSet,
                    type=OrderedSet()._from_iterable,
                    doc='A `set` of SummaryAddress keys objects')

                def add_sumadd_key(self, sumadd_key):
                    self.sumadd_keys.add(sumadd_key)

                def remove_sumadd_key(self, sumadd_key):
                    sumadd_key._device = None
                    try:
                        self.sumadd_keys.remove(sumadd_key)
                    except:
                        pass

                # Area Range multi-line configs
                arearange_keys = managedattribute(
                    name='arearange_keys',
                    finit=typedset(
                        managedattribute.test_isinstance(AreaRange)).copy,
                    type=typedset(managedattribute.test_isinstance(
                        AreaRange))._from_iterable,
                    doc='A `set` of AreaRange keys objects')

                def add_arearange_key(self, arearange_key):
                    self.arearange_keys.add(arearange_key)

                def remove_arearange_key(self, arearange_key):
                    arearange_key._device = None
                    try:
                        self.arearange_keys.remove(arearange_key)
                    except:
                        pass

                # Area route map multi-line configs
                arearoutemap_keys = managedattribute(
                    name='arearoutemap_keys',
                    finit=typedset(
                        managedattribute.test_isinstance(AreaRouteMap)).copy,
                    type=typedset(managedattribute.test_isinstance(
                        AreaRouteMap))._from_iterable,
                    doc='A `set` of AreaRouteMap keys objects')

                def add_arearoutemap_key(self, arearoutemap_key):
                    self.arearoutemap_keys.add(arearoutemap_key)

                def remove_arearoutemap_key(self, arearoutemap_key):
                    arearoutemap_key._device = None
                    try:
                        self.arearoutemap_keys.remove(arearoutemap_key)
                    except:
                        pass

                # Area default cost multi-line configs
                areacost_keys = managedattribute(
                    name='areacost_keys',
                    finit=typedset(
                        managedattribute.test_isinstance(AreaDefaultCost)).copy,
                    type=typedset(managedattribute.test_isinstance(
                        AreaDefaultCost))._from_iterable,
                    doc='A `set` of AreaDefaultCost keys objects')

                def add_areacost_key(self, areacost_key):
                    self.areacost_keys.add(areacost_key)

                def remove_arearoutemap_key(self, areacost_key):
                    areacost_key._device = None
                    try:
                        self.areacost_keys.remove(areacost_key)
                    except:
                        pass

            address_family_attr = managedattribute(
                name='address_family_attr',
                read_only=True,
                doc=AddressFamilyAttributes.__doc__)

            @address_family_attr.initter
            def address_family_attr(self):
                return SubAttributesDict(self.AddressFamilyAttributes, parent=self)
            # +- DeviceAttributes
            #   +- VrfAttributes
            #     +- AreaAttributes

            class AreaAttributes(KeyedSubAttributes):

                def __init__(self, parent, key):
                    self.area = key
                    super().__init__(parent)

                # +- DeviceAttributes
                #   +- VrfAttributes
                #     +- AreaAttributes
                #       +- VirtualLinkAttributes
                class VirtualLinkAttributes(KeyedSubAttributes):

                    def __init__(self, parent, key):
                        self.vlink = key
                        super().__init__(parent)

                virtual_link_attr = managedattribute(
                    name='virtual_link_attr',
                    read_only=True,
                    doc=VirtualLinkAttributes.__doc__)

                @virtual_link_attr.initter
                def virtual_link_attr(self):
                    return SubAttributesDict(self.VirtualLinkAttributes, parent=self)

                # +- DeviceAttributes
                #   +- VrfAttributes
                #     +- AreaAttributes
                #       +- InterfaceAttributes
                class InterfaceAttributes(InterfaceSubAttributes):
                    def __init__(self, parent, key):
                        super().__init__(parent, key)

                interface_attr = managedattribute(
                    name='interface_attr',
                    read_only=True,
                    doc=InterfaceAttributes.__doc__)

                @interface_attr.initter
                def interface_attr(self):
                    return SubAttributesDict(self.InterfaceAttributes, parent=self)

            area_attr = managedattribute(
                name='area_attr',
                read_only=True,
                doc=AreaAttributes.__doc__)

            @area_attr.initter
            def area_attr(self):
                return SubAttributesDict(self.AreaAttributes, parent=self)

        vrf_attr = managedattribute(
            name='vrf_attr',
            read_only=True,
            doc=VrfAttributes.__doc__)

        @vrf_attr.initter
        def vrf_attr(self):
            return SubAttributesDict(self.VrfAttributes, parent=self)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    # ==========================================================================
    #                           GLOBAL ENUM TYPES
    # ==========================================================================

    class INTF_TYPE(Enum):
        broadcast = 'broadcast'
        point_to_point = 'point-to-point'

    class AREA_TYPE(Enum):
        normal = 'normal'
        stub = 'stub'
        nssa = 'nssa'

    # ==========================================================================
    #                           MANAGED ATTRIBUTES
    # ==========================================================================

    # enabled
    enabled = managedattribute(
        name='enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ==========================================================================
    # +- DeviceAttributes
    #   +- VrfAttributes
    # ==========================================================================

    # instance
    instance = managedattribute(
        name='instance',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # enable
    inst_shutdown = managedattribute(
        name='inst_shutdown',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # router_id
    router_id = managedattribute(
        name='router_id',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # passive-interface
    passive_interface = managedattribute(
        name='passive_interface',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # log_adjacency_changes
    log_adjacency_changes = managedattribute(
        name='log_adjacency_changes',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # log_adjacency_changes_detail
    log_adjacency_changes_detail = managedattribute(
        name='log_adjacency_changes_detail',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # timers lsa-arrival msec
    lsa_arrival = managedattribute(
        name='lsa_arrival',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # timers lsa-group-pacing seconds
    lsa_group_pacing = managedattribute(
        name='lsa_group_pacing',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # timers throttle lsa start-time hold-interval max-time
    # throttle lsa start timer
    lsa_start_time = managedattribute(
        name='lsa_start_time',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # throttle lsa hold timer
    lsa_hold_time = managedattribute(
        name='lsa_hold_time',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # throttle lsa max timer
    lsa_max_timer = managedattribute(
        name='lsa_max_time',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    bfd_enable = managedattribute(
        name='bfd_enable',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ==========================================================================
    # +- DeviceAttributes
    #   +- VrfAttributes
    #     +- AreaAttributes
    # ==========================================================================

    # area_type
    area_type = managedattribute(
        name='area_type',
        default=AREA_TYPE.normal,
        type=(None, AREA_TYPE))

    # no-summary
    nosummary = managedattribute(
        name='nosummary',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # area area-id nssa no-redistribution
    nssa_no_redistribution = managedattribute(
        name='nssa_no_redistribution',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # area area-id nssa default-information-originate
    nssa_default_info_originate = managedattribute(
        name='nssa_default_info_originate',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # area area-id nssa route-map map-name
    nssa_route_map = managedattribute(
        name='nssa_route_map',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # area area-id nssa translate type7 always
    nssa_translate_always = managedattribute(
        name='nssa_translate_always',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # area area-id nssa translate type7 never
    nssa_translate_never = managedattribute(
        name='nssa_translate_never',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # area area-id nssa translate type7 suppress-fa
    nssa_translate_supressfa = managedattribute(
        name='nssa_translate_supressfa',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ==========================================================================
    # +- DeviceAttributes
    # +- VrfAttributes
    #     +- AdressFamilyAttributes
    # ==========================================================================

    # redist_bgp_id
    redist_bgp_id = managedattribute(
        name='redist_bgp_id',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # redist_bgp_route_map
    redist_bgp_route_map = managedattribute(
        name='redist_bgp_route_map',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # redist_isis_id
    redist_isis_id = managedattribute(
        name='redist_isis_id',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # redist_isis_route_map
    redist_isis_route_map = managedattribute(
        name='redist_isis_route_map',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # redist_rip_id
    redist_rip_id = managedattribute(
        name='redist_rip_id',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # redist_rip_route_map
    redist_rip_route_map = managedattribute(
        name='redist_rip_route_map',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # redist_static
    redist_static = managedattribute(
        name='redist_static',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # redist_static_route_map
    redist_static_route_map = managedattribute(
        name='redist_static_route_map',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # redist_direct
    redist_direct = managedattribute(
        name='redist_direct',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # redist_direct_route_map
    redist_direct_route_map = managedattribute(
        name='redist_direct_route_map',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # default_originate
    default_originate = managedattribute(
        name='default_originate',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # default_originate_always
    default_originate_always = managedattribute(
        name='default_originate_always',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # default_originate_routemap
    default_originate_routemap = managedattribute(
        name='default_originate_routemap',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # default_metric
    default_metric = managedattribute(
        name='default_metric',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # redist_max_prefix
    redist_max_prefix = managedattribute(
        name='redist_max_prefix',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # redist_max_prefix_thld
    redist_max_prefix_thld = managedattribute(
        name='redist_max_prefix_thld',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # redist_max_prefix_warn_only
    redist_max_prefix_warn_only = managedattribute(
        name='redist_max_prefix_warn_only',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # redist_max_prefix_withdraw
    redist_max_prefix_withdraw = managedattribute(
        name='redist_max_prefix_withdraw',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # redist_max_prefix_retries
    redist_max_prefix_retries = managedattribute(
        name='redist_max_prefix_retries',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # redist_max_prefix_retries_timeout
    redist_max_prefix_retries_timeout = managedattribute(
        name='redist_max_prefix_retries_timeout',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # timers throttle spf start-time hold-interval max-time
    # throttle spf start timer
    spf_start_time = managedattribute(
        name='spf_start_time',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # throttle spf hold timer
    spf_hold_time = managedattribute(
        name='spf_hold_time',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # throttle spf max timer
    spf_max_timer = managedattribute(
        name='spf_max_time',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # table_map
    table_map = managedattribute(
        name='table_map',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # default_cost
    default_cost = managedattribute(
        name='default_cost',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # ar_route_map_in
    ar_route_map_in = managedattribute(
        name='ar_route_map_in',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # ar_route_map_out
    ar_route_map_out = managedattribute(
        name='ar_route_map_out',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # ==========================================================================
    # +- DeviceAttributes
    # +- VrfAttributes
    #     +- AreaAttributes
    #         +- VirtualLinkAttributes
    # ==========================================================================
    # vl_router_id
    vl_router_id = managedattribute(
        name='vl_router_id',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # vl_hello_interval
    vl_hello_interval = managedattribute(
        name='vl_hello_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # vl_dead_interval
    vl_dead_interval = managedattribute(
        name='vl_dead_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # vl_retransmit_interval
    vl_retransmit_interval = managedattribute(
        name='vl_retransmit_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # vl_transmit_delay
    vl_transmit_delay = managedattribute(
        name='vl_transmit_delay',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # ==========================================================================
    # +- DeviceAttributes
    # +- VrfAttributes
    #     +- AreaAttributes
    #         +- InterfaceAttributes
    # ==========================================================================

    # if_name - Attribute key

    # if_admin_control
    if_admin_control = managedattribute(
        name='if_admin_control',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # if_cost
    if_cost = managedattribute(
        name='if_cost',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # if_type
    if_type = managedattribute(
        name='if_type',
        default=None,
        type=(None, INTF_TYPE))

    # if_passive
    if_passive = managedattribute(
        name='if_passive',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # if_priority
    if_priority = managedattribute(
        name='if_priority',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # if_hello_interval
    if_hello_interval = managedattribute(
        name='if_hello_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # if_dead_interval
    if_dead_interval = managedattribute(
        name='if_dead_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # if_retransmit_interval
    if_retransmit_interval = managedattribute(
        name='if_retransmit_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # if_mtu_ignore
    if_mtu_ignore = managedattribute(
        name='if_mtu_ignore',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # if_instance
    if_instance = managedattribute(
        name='if_instance',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # if_protocol_shutdown
    if_protocol_shutdown = managedattribute(
        name='if_protocol_shutdown',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # if_secondaries
    if_secondaries = managedattribute(
        name='if_secondaries',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # if_transmit_delay
    if_transmit_delay = managedattribute(
        name='if_transmit_delay',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # if_multi_area
    if_multi_area = managedattribute(
        name='if_multi_area',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # if_bfd_enable
    if_bfd_enable = managedattribute(
        name='if_bfd_enable',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ==========================================================================
    #                       BUILD_CONFIG & BUILD_UNCONFIG
    # ==========================================================================

    def build_config(self, devices=None, apply=True, attributes=None,
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

    def build_unconfig(self, devices=None, apply=True, attributes=None,
                       **kwargs):
        cfgs = {}
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
