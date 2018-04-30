
__all__ = (
    'Ospf',
)

# Python
from enum import Enum

# Genie
from genie.utils.cisco_collections import typedset
from genie.decorator import managedattribute
from genie.conf.base.config import CliConfig
from genie.conf.base.base import DeviceFeature, InterfaceFeature, LinkFeature

from genie.libs.conf.base import Routing
from genie.libs.conf.vrf import Vrf, VrfSubAttributes
from genie.conf.base.attributes import DeviceSubAttributes, SubAttributesDict,\
                                       AttributesHelper, KeyedSubAttributes,\
                                       InterfaceSubAttributes

# Multi-line config classes
from .arearange import AreaRange
from .stubrouter import StubRouter
from .areanetwork import AreaNetwork
from .gracefulrestart import GracefulRestart
from .interfacestaticneighbor import InterfaceStaticNeighbor

# OSPF Heirarchy
# --------------
# Ospf
#  +- DeviceAttributes
#      +- VrfAttributes
#          +- AreaAttributes
#              +- VirtualLinkAttributes
#              +- ShamLinkAttributes
#              +- InterfaceAttributes


class Ospf(Routing, DeviceFeature, LinkFeature):

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
                finit=typedset(managedattribute.test_isinstance(GracefulRestart)).copy,
                type=typedset(managedattribute.test_isinstance(GracefulRestart))._from_iterable,
                doc='A `set` of GracefulRestart keys objects')

            def add_gr_key(self, gr_key):
                self.gr_keys.add(gr_key)

            def remove_gr_key(self, gr_key):
                gr_key._device = None
                try:
                    self.gr_keys.remove(gr_key)
                except:
                    pass

            # Stub Router multi-line configs
            sr_keys = managedattribute(
                name='sr_keys',
                finit=typedset(managedattribute.test_isinstance(StubRouter)).copy,
                type=typedset(managedattribute.test_isinstance(StubRouter))._from_iterable,
                doc='A `set` of StubRouter keys objects')

            def add_sr_key(self, sr_key):
                self.sr_keys.add(sr_key)

            def remove_sr_key(self, sr_key):
                sr_key._device = None
                try:
                    self.sr_keys.remove(sr_key)
                except:
                    pass

            # +- DeviceAttributes
            #   +- VrfAttributes
            #     +- AreaAttributes
            class AreaAttributes(KeyedSubAttributes):
                
                def __init__(self, parent, key):
                    self.area = key
                    super().__init__(parent)

                # Area Network multi-line configs
                areanetwork_keys = managedattribute(
                    name='areanetwork_keys',
                    finit=typedset(managedattribute.test_isinstance(AreaNetwork)).copy,
                    type=typedset(managedattribute.test_isinstance(AreaNetwork))._from_iterable,
                    doc='A `set` of AreaNetwork keys objects')

                def add_areanetwork_key(self, areanetwork_key):
                    self.areanetwork_keys.add(areanetwork_key)

                def remove_areanetwork_key(self, areanetwork_key):
                    areanetwork_key._device = None
                    try:
                        self.areanetwork_keys.remove(areanetwork_key)
                    except:
                        pass

                # Area Range multi-line configs
                arearange_keys = managedattribute(
                    name='arearange_keys',
                    finit=typedset(managedattribute.test_isinstance(AreaRange)).copy,
                    type=typedset(managedattribute.test_isinstance(AreaRange))._from_iterable,
                    doc='A `set` of AreaRange keys objects')

                def add_arearange_key(self, arearange_key):
                    self.arearange_keys.add(arearange_key)

                def remove_arearange_key(self, arearange_key):
                    arearange_key._device = None
                    try:
                        self.arearange_keys.remove(arearange_key)
                    except:
                        pass

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
                #       +- ShamLinkAttributes
                class ShamLinkAttributes(KeyedSubAttributes):

                    def __init__(self, parent, key):
                        self.vlink = key
                        super().__init__(parent)

                sham_link_attr = managedattribute(
                    name='sham_link_attr',
                    read_only=True,
                    doc=ShamLinkAttributes.__doc__)

                @sham_link_attr.initter
                def sham_link_attr(self):
                    return SubAttributesDict(self.ShamLinkAttributes, parent=self)

                # +- DeviceAttributes
                #   +- VrfAttributes
                #     +- AreaAttributes
                #       +- InterfaceAttributes
                class InterfaceAttributes(InterfaceSubAttributes):

                    # Interface Static Neighbor multi-line configs
                    intf_staticnbr_keys = managedattribute(
                        name='intf_staticnbr_keys',
                        finit=typedset(managedattribute.test_isinstance(InterfaceStaticNeighbor)).copy,
                        type=typedset(managedattribute.test_isinstance(InterfaceStaticNeighbor))._from_iterable,
                        doc='A `set` of InterfaceStaticNeighbor keys objects')

                    def add_staticnbr_key(self, intf_staticnbr_key):
                        self.intf_staticnbr_keys.add(intf_staticnbr_key)

                    def remove_staticnbr_key(self, intf_staticnbr_key):
                        intf_staticnbr_key._device = None
                        try:
                            self.intf_staticnbr_keys.remove(intf_staticnbr_key)
                        except:
                            pass

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

    class REDIST_BGP_METRIC_TYPE(Enum):
        type_one = '1'
        type_two = '2'

    class AUTO_COST_BANDWIDTH_UNIT(Enum):
        mbps = 'mbps'
        gbps = 'gbps'

    class AREA_TYPE(Enum):
        normal = 'normal'
        stub = 'stub'
        nssa = 'nssa'

    class AUTH_CRYPTO_ALGORITHM(Enum):
        simple = 'simple'
        md5 = 'md5'

    class INTF_TYPE(Enum):
        broadcast = 'broadcast'
        non_broadcast = 'non-broadcast'
        point_to_multipoint  = 'point-to-multipoint'
        point_to_point = 'point-to-point'

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

    # vrf - N/A ?
    vrf = managedattribute(
        name='vrf',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # enable
    enable = managedattribute(
        name='enable',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # router_id
    router_id = managedattribute(
        name='router_id',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # pref_all
    pref_all = managedattribute(
        name='pref_all',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # pref_intra_area
    pref_intra_area = managedattribute(
        name='pref_intra_area',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # pref_inter_area
    pref_inter_area = managedattribute(
        name='pref_inter_area',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # pref_internal
    pref_internal = managedattribute(
        name='pref_internal',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # pref_external
    pref_external = managedattribute(
        name='pref_external',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # nsr_enable
    nsr_enable = managedattribute(
        name='nsr_enable',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ldp_autoconfig
    ldp_autoconfig = managedattribute(
        name='ldp_autoconfig',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ldp_auto_config_area_id
    ldp_auto_config_area_id = managedattribute(
        name='ldp_auto_config_area_id',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # ldp_igp_sync
    ldp_igp_sync = managedattribute(
        name='ldp_igp_sync',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # redist_bgp_id
    redist_bgp_id = managedattribute(
        name='redist_bgp_id',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # redist_bgp_metric
    redist_bgp_metric = managedattribute(
        name='redist_bgp_metric',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # redist_bgp_metric_type
    redist_bgp_metric_type = managedattribute(
        name='redist_bgp_metric_type',
        default=REDIST_BGP_METRIC_TYPE.type_one,
        type=(None, REDIST_BGP_METRIC_TYPE))

    # redist_bgp_nssa_only
    redist_bgp_nssa_only = managedattribute(
        name='redist_bgp_nssa_only',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # redist_bgp_route_map
    redist_bgp_route_map = managedattribute(
        name='redist_bgp_route_map',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # redist_bgp_subnets
    redist_bgp_subnets = managedattribute(
        name='redist_bgp_subnets',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # redist_bgp_tag
    redist_bgp_tag = managedattribute(
        name='redist_bgp_tag',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # redist_bgp_lsa_type_summary 
    redist_bgp_lsa_type_summary = managedattribute(
        name='redist_bgp_lsa_type_summary',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # redist_bgp_preserve_med
    redist_bgp_preserve_med = managedattribute(
        name='redist_bgp_preserve_med',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # redist_connected
    redist_connected = managedattribute(
        name='redist_connected',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # redist_connected_metric
    redist_connected_metric = managedattribute(
        name='redist_connected_metric',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # redist_connected_route_policy
    redist_connected_route_policy = managedattribute(
        name='redist_connected_route_policy',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # redist_static
    redist_static = managedattribute(
        name='redist_static',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # redist_static_metric
    redist_static_metric = managedattribute(
        name='redist_static_metric',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # redist_static_route_policy
    redist_static_route_policy = managedattribute(
        name='redist_static_route_policy',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # redist_isis
    redist_isis = managedattribute(
        name='redist_isis',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # redist_isis_metric
    redist_isis_metric = managedattribute(
        name='redist_isis_metric',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # redist_isis_route_policy
    redist_isis_route_policy = managedattribute(
        name='redist_isis_route_policy',
        default=None,
        type=(None, managedattribute.test_istype(str)))

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

    # bfd_enable
    bfd_enable = managedattribute(
        name='bfd_enable',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # bfd_strict_mode
    bfd_strict_mode = managedattribute(
        name='bfd_strict_mode',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # te_router_id
    te_router_id = managedattribute(
        name='te_router_id',
        default=None,
        type=(None, managedattribute.test_istype(str)))

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

    # adjacency_stagger_initial_number
    adjacency_stagger_initial_number = managedattribute(
        name='adjacency_stagger_initial_number',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # adjacency_stagger_maximum_number
    adjacency_stagger_maximum_number = managedattribute(
        name='adjacency_stagger_maximum_number',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # adjacency_stagger_disable
    adjacency_stagger_disable = managedattribute(
        name='adjacency_stagger_disable',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # adjacency_stagger_no_initial_limit
    adjacency_stagger_no_initial_limit = managedattribute(
        name='adjacency_stagger_no_initial_limit',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # auto_cost_enable
    auto_cost_enable = managedattribute(
        name='auto_cost_enable',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # auto_cost_reference_bandwidth
    auto_cost_reference_bandwidth = managedattribute(
        name='auto_cost_reference_bandwidth',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # auto_cost_bandwidth_unit
    auto_cost_bandwidth_unit = managedattribute(
        name='auto_cost_bandwidth_unit',
        default=None,
        type=(None, AUTO_COST_BANDWIDTH_UNIT))

    # maximum_interfaces
    maximum_interfaces = managedattribute(
        name='maximum_interfaces',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # spf_paths
    spf_paths = managedattribute(
        name='spf_paths',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # spf_start
    spf_start = managedattribute(
        name='spf_start',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # spf_hold
    spf_hold = managedattribute(
        name='spf_hold',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # spf_maximum
    spf_maximum = managedattribute(
        name='spf_maximum',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # spf_lsa_start
    spf_lsa_start = managedattribute(
        name='spf_lsa_start',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # spf_lsa_hold
    spf_lsa_hold = managedattribute(
        name='spf_lsa_hold',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # spf_lsa_maximum
    spf_lsa_maximum = managedattribute(
        name='spf_lsa_maximum',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # db_ctrl_max_lsa
    db_ctrl_max_lsa = managedattribute(
        name='db_ctrl_max_lsa',
        default=None,
        type=(None, managedattribute.test_istype(int)))

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

    # ==========================================================================
    # +- DeviceAttributes
    #   +- VrfAttributes
    #     +- AreaAttributes
    # ==========================================================================
    
    # area_id
    area_id = managedattribute(
        name='area_id',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # area_te_enable
    area_te_enable = managedattribute(
        name='area_te_enable',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # area_bfd_enable
    area_bfd_enable = managedattribute(
                name='area_bfd_enable',
                default=None,
                type=(None, managedattribute.test_istype(bool)))

    # area_bfd_min_interval
    area_bfd_min_interval = managedattribute(
        name='area_bfd_min_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # area_bfd_multiplier
    area_bfd_multiplier = managedattribute(
        name='area_bfd_multiplier',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # area_passive
    area_passive = managedattribute(
        name='area_passive',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # area_mtu_ignore
    area_mtu_ignore = managedattribute(
        name='area_mtu_ignore',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # area_demand_cirtuit
    area_demand_cirtuit = managedattribute(
        name='area_demand_cirtuit',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # area_external_out
    area_external_out = managedattribute(
        name='area_external_out',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # area_flood_reduction
    area_flood_reduction = managedattribute(
        name='area_flood_reduction',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # area_link_down_fast_detect
    area_link_down_fast_detect = managedattribute(
        name='area_link_down_fast_detect',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # area_ldp_auto_config
    area_ldp_auto_config = managedattribute(
        name='area_ldp_auto_config',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # area_ldp_sync
    area_ldp_sync = managedattribute(
        name='area_ldp_sync',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # area_ldp_sync_igp_shortcuts
    area_ldp_sync_igp_shortcuts = managedattribute(
        name='area_ldp_sync_igp_shortcuts',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # area_type
    area_type = managedattribute(
        name='area_type',
        default=AREA_TYPE.normal,
        type=(None, AREA_TYPE))

    # summary
    summary = managedattribute(
        name='summary',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # default_cost
    default_cost = managedattribute(
        name='default_cost',
        default=None,
        type=(None, managedattribute.test_istype(int)))

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

    # vl_ttl_sec_hops
    vl_ttl_sec_hops = managedattribute(
        name='vl_ttl_sec_hops',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # vl_auth_trailer_key_chain
    vl_auth_trailer_key_chain = managedattribute(
        name='vl_auth_trailer_key_chain',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # vl_auth_trailer_key
    vl_auth_trailer_key = managedattribute(
        name='vl_auth_trailer_key',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # vl_auth_trailer_key_crypto_algorithm
    vl_auth_trailer_key_crypto_algorithm = managedattribute(
        name='vl_auth_trailer_key_crypto_algorithm',
        default=None,
        type=(None, AUTH_CRYPTO_ALGORITHM))

    # ==========================================================================
    # +- DeviceAttributes
    #     +- VrfAttributes
    #         +- AreaAttributes
    #             +- ShamLinkAttributes
    # ==========================================================================

    # sl_local_id
    sl_local_id = managedattribute(
        name='sl_local_id',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # sl_remote_id
    sl_remote_id = managedattribute(
        name='sl_remote_id',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # sl_hello_interval
    sl_hello_interval = managedattribute(
        name='sl_hello_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # sl_dead_interval
    sl_dead_interval = managedattribute(
        name='sl_dead_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # sl_retransmit_interval
    sl_retransmit_interval = managedattribute(
        name='sl_retransmit_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # sl_transmit_delay
    sl_transmit_delay = managedattribute(
        name='sl_transmit_delay',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # sl_ttl_sec_hops
    sl_ttl_sec_hops = managedattribute(
        name='sl_ttl_sec_hops',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # sl_cost
    sl_cost = managedattribute(
        name='sl_cost',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # sl_auth_trailer_key_chain
    sl_auth_trailer_key_chain = managedattribute(
        name='sl_auth_trailer_key_chain',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # sl_auth_trailer_key
    sl_auth_trailer_key = managedattribute(
        name='sl_auth_trailer_key',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # sl_auth_trailer_key_crypto_algorithm
    sl_auth_trailer_key_crypto_algorithm = managedattribute(
        name='sl_auth_trailer_key_crypto_algorithm',
        default=None,
        type=(None, AUTH_CRYPTO_ALGORITHM))
    

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

    # if_demand_circuit
    if_demand_circuit = managedattribute(
        name='if_demand_circuit',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # if_priority
    if_priority = managedattribute(
        name='if_priority',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # if_bfd_enable
    if_bfd_enable = managedattribute(
        name='if_bfd_enable',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # if_bfd_min_interval
    if_bfd_min_interval = managedattribute(
        name='if_bfd_min_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # if_bfd_multiplier
    if_bfd_multiplier = managedattribute(
        name='if_bfd_multiplier',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # if_bfd_interval
    if_bfd_interval = managedattribute(
        name='if_bfd_interval',
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

    # if_lls
    if_lls = managedattribute(
        name='if_lls',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # if_ttl_sec_enable
    if_ttl_sec_enable = managedattribute(
        name='if_ttl_sec_enable',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # if_ttl_sec_hops
    if_ttl_sec_hops = managedattribute(
        name='if_ttl_sec_hops',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # if_auth_trailer_key_chain
    if_auth_trailer_key_chain = managedattribute(
        name='if_auth_trailer_key_chain',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # if_auth_trailer_key
    if_auth_trailer_key = managedattribute(
        name='if_auth_trailer_key',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # if_auth_trailer_key_crypto_algorithm
    if_auth_trailer_key_crypto_algorithm = managedattribute(
        name='if_auth_trailer_key_crypto_algorithm',
        default=None,
        type=(None, AUTH_CRYPTO_ALGORITHM))

    # if_mtu_ignore
    if_mtu_ignore = managedattribute(
        name='if_mtu_ignore',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # if_prefix_suppression
    if_prefix_suppression = managedattribute(
        name='if_prefix_suppression',
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


