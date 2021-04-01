__all__ = (
    'Bgp',
)

import ipaddress
from enum import Enum
from ipaddress import IPv4Address, IPv4Interface, \
    IPv6Address, IPv6Interface, IPv6Network

import genie.conf.base.attributes
from genie.abstract import Lookup
from genie.conf.base import Base, DeviceFeature, Interface
from genie.conf.base.attributes import SubAttributes, \
    SubAttributesDict, \
    AttributesHelper, \
    KeyedSubAttributes
from genie.decorator import managedattribute
from genie.libs import parser
from genie.libs.conf.address_family import AddressFamily, \
    AddressFamilySubAttributes
from genie.libs.conf.base import Redistribution
from genie.libs.conf.base import RouteDistinguisher, RouteTarget
from genie.libs.conf.base import Routing, IPNeighbor
from genie.libs.conf.base.neighbor import IPNeighborSubAttributes
from genie.libs.conf.route_policy import RoutePolicy
from genie.libs.conf.vrf import Vrf, VrfSubAttributes
from genie.ops.base import Base as ops_Base
from genie.ops.base import Context
from genie.utils.cisco_collections import typedset


class Bgp(Routing, DeviceFeature):
    bgp_id = managedattribute(
        name='bgp_id',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    asn = managedattribute(
        name='asn',
        type=int,
        doc='AS number (mandatory)')

    address_families = managedattribute(
        name='address_families',
        finit=typedset(AddressFamily, {AddressFamily.ipv4_unicast}).copy,
        type=typedset(AddressFamily)._from_iterable)

    nsr = managedattribute(
        name='nsr',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # iosxr only
    instance_name = managedattribute(
        name='instance_name',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    ibgp_policy_out_enforce_modifications = managedattribute(
        name='ibgp_policy_out_enforce_modifications',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    activate = managedattribute(
        name='activate',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ==== Device attribute section =======
    protocol_shutdown = managedattribute(
        name='protocol_shutdown',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Bgp instance shutdown')

    # ==================== NXOS specific ====================

    # feature bgp
    enabled = managedattribute(
        name='enabled',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc='Enable or disable feature bgp')

    # ===========================================================

    # ==== Peer Session section =======
    class PS_TRANSPORT_CONNECTION_MODE(Enum):
        active = 'active'
        passive = 'passive'

    ps_transport_connection_mode = managedattribute(
        name='ps_transport_connection_mode',
        default=None,
        type=(None, PS_TRANSPORT_CONNECTION_MODE),
        doc='Peer session transport connection mode')

    ps_name = managedattribute(
        name='ps_name',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Peer session name')

    ps_fall_over_bfd = managedattribute(
        name='ps_fall_over_bfd',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Peer session fall over bfd')

    ps_suppress_four_byte_as_capability = managedattribute(
        name='ps_suppress_four_byte_as_capability',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    ps_description = managedattribute(
        name='ps_description',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    ps_disable_connected_check = managedattribute(
        name='ps_disable_connected_check',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    ps_ebgp_multihop = managedattribute(
        name='ps_ebgp_multihop',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    ps_ebgp_multihop_max_hop = managedattribute(
        name='ps_ebgp_multihop_max_hop',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    ps_local_as_as_no = managedattribute(
        name='ps_local_as_as_no',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    ps_local_as_no_prepend = managedattribute(
        name='ps_local_as_no_prepend',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    ps_local_as_dual_as = managedattribute(
        name='ps_local_as_dual_as',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    ps_local_as_replace_as = managedattribute(
        name='ps_local_as_replace_as',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    ps_password_text = managedattribute(
        name='ps_password_text',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    ps_remote_as = managedattribute(
        name='ps_remote_as',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    ps_shutdown = managedattribute(
        name='ps_shutdown',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    ps_keepalive_interval = managedattribute(
        name='ps_keepalive_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    ps_hodltime = managedattribute(
        name='ps_hodltime',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    ps_update_source = managedattribute(
        name='ps_update_source',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # ==== Peer Policy section ===================
    class PP_SEND_COMMUNITY(Enum):
        standard = 'standard'
        extended = 'extended'
        both = 'both'

    pp_send_community = managedattribute(
        name='pp_send_community',
        default=None,
        type=(None, PP_SEND_COMMUNITY),
        doc='Peer policy send community type')

    class PP_AF_NAME(Enum):
        ipv4_unicast = 'ipv4 unicast'
        ipv6_unicast = 'ipv6 unicast'

    # XR only
    pp_af_name = managedattribute(
        name='pp_af_name',
        default=None,
        type=(None, PP_AF_NAME),
        doc='Peer policy address-family name')

    pp_name = managedattribute(
        name='pp_name',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    pp_allowas_in = managedattribute(
        name='pp_allowas_in',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    pp_allowas_in_as_number = managedattribute(
        name='pp_allowas_in_as_number',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    pp_as_override = managedattribute(
        name='pp_as_override',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    pp_default_originate = managedattribute(
        name='pp_default_originate',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    pp_default_originate_route_map = managedattribute(
        name='pp_default_originate',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    pp_route_map_name_in = managedattribute(
        name='pp_route_map_name_in',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    pp_route_map_name_out = managedattribute(
        name='pp_route_map_name_out',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    pp_maximum_prefix_max_prefix_no = managedattribute(
        name='pp_maximum_prefix_max_prefix_no',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    pp_maximum_prefix_threshold = managedattribute(
        name='pp_maximum_prefix_threshold',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    pp_maximum_prefix_restart = managedattribute(
        name='pp_maximum_prefix_restart',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    pp_maximum_prefix_warning_only = managedattribute(
        name='pp_maximum_prefix_restart',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    pp_next_hop_self = managedattribute(
        name='pp_next_hop_self',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    pp_route_reflector_client = managedattribute(
        name='pp_route_reflector_client',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    pp_soft_reconfiguration = managedattribute(
        name='pp_soft_reconfiguration',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    pp_soo = managedattribute(
        name='pp_soo',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # ==== VRF section ===========================
    dynamic_med_interval = managedattribute(
        name='dynamic_med_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Dynamic med interval time in seconds')

    shutdown = managedattribute(
        name='shutdown',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Bgp VRF shutdown')

    flush_routes = managedattribute(
        name='flush_routes',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    isolate = managedattribute(
        name='isolate',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    disable_policy_batching_ipv4 = managedattribute(
        name='disable_policy_batching_ipv4',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    disable_policy_batching_ipv6 = managedattribute(
        name='disable_policy_batching_ipv6',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    always_compare_med = managedattribute(
        name='always_compare_med',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    bestpath_compare_routerid = managedattribute(
        name='bestpath_compare_routerid',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    bestpath_cost_community_ignore = managedattribute(
        name='bestpath_cost_community_ignore',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    bestpath_med_missing_at_worst = managedattribute(
        name='bestpath_med_missing_at_worst',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    cluster_id = managedattribute(
        name='cluster_id',
        default=None,
        type=(None, managedattribute.test_istype(int),
              managedattribute.test_istype(str)))

    confederation_identifier = managedattribute(
        name='confederation_identifier',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    confederation_peers_as = managedattribute(
        name='confederation_peers_as',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    graceful_restart = managedattribute(
        name='graceful_restart',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    graceful_restart_restart_time = managedattribute(
        name='graceful_restart_restart_time',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    maxas_limit = managedattribute(
        name='maxas_limit',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    graceful_restart_stalepath_time = managedattribute(
        name='graceful_restart_stalepath_time',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    log_neighbor_changes = managedattribute(
        name='log_neighbor_changes',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    router_id = managedattribute(
        name='router_id',
        default=None,
        type=(None, IPv4Address))

    keepalive_interval = managedattribute(
        name='keepalive_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    prefix_peer_timeout = managedattribute(
        name='prefix_peer_timeout',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    holdtime = managedattribute(
        name='holdtime',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    enforce_first_as = managedattribute(
        name='enforce_first_as',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    fast_external_fallover = managedattribute(
        name='fast_external_fallover',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    default_choice_ipv4_unicast = managedattribute(
        name='default_choice_ipv4_unicast',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ==== Address-family section ================
    class AF_LABEL_ALLOCATION_MODE(Enum):
        per_vrf = 'per-vrf'

    af_label_allocation_mode = managedattribute(
        name='af_label_allocation_mode',
        default=None,
        type=(None, AF_LABEL_ALLOCATION_MODE),
        doc='Address family label allocation mode')
    # vxlan
    af_advertise_pip = managedattribute(
        name='af_advertise_pip',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    af_advertise_l2_evpn = managedattribute(
        name='af_advertise_l2_evpn',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    af_name = managedattribute(
        name='af_name',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    af_dampening = managedattribute(
        name='af_dampening',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    af_dampening_route_map = managedattribute(
        name='af_dampening_route_map',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    af_dampening_half_life_time = managedattribute(
        name='af_dampening_half_life_time',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    af_dampening_reuse_time = managedattribute(
        name='af_dampening_reuse_time',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    af_dampening_suppress_time = managedattribute(
        name='af_dampening_suppress_time',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    af_dampening_max_suppress_time = managedattribute(
        name='af_dampening_max_suppress_time',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    af_nexthop_route_map = managedattribute(
        name='af_nexthop_route_map',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    af_nexthop_trigger_enable = managedattribute(
        name='af_nexthop_trigger_enable',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    af_nexthop_trigger_delay_critical = managedattribute(
        name='af_nexthop_trigger_delay_critical',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    af_nexthop_trigger_delay_non_critical = managedattribute(
        name='af_nexthop_trigger_delay_non_critical',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    af_client_to_client_reflection = managedattribute(
        name='af_client_to_client_reflection',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    af_distance_extern_as = managedattribute(
        name='af_distance_extern_as',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    af_distance_internal_as = managedattribute(
        name='af_distance_internal_as',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    af_distance_local = managedattribute(
        name='af_distance_local',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    af_maximum_paths_ebgp = managedattribute(
        name='af_maximum_paths_ebgp',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    af_maximum_paths_ibgp = managedattribute(
        name='af_maximum_paths_ibgp',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    af_maximum_paths_eibgp = managedattribute(
        name='af_maximum_paths_eibgp',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    af_aggregate_address_ipv4_address = managedattribute(
        name='af_aggregate_address_ipv4_address',
        default=None,
        type=(None, IPv4Address))

    af_aggregate_address_ipv4_mask = managedattribute(
        name='af_aggregate_address_ipv4_mask',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    af_aggregate_address_as_set = managedattribute(
        name='af_aggregate_address_as_set',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    af_aggregate_address_summary_only = managedattribute(
        name='af_aggregate_address_summary_only',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    af_network_number = managedattribute(
        name='af_network_number',
        default=None,
        type=(None, IPv4Address))

    af_network_mask = managedattribute(
        name='af_network_mask',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    af_network_route_map = managedattribute(
        name='af_network_route_map',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    af_redist_isis = managedattribute(
        name='af_redist_isis',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    af_redist_isis_metric = managedattribute(
        name='af_redist_isis_metric',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    af_redist_isis_route_policy = managedattribute(
        name='af_redist_isis_route_policy',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    af_redist_ospf = managedattribute(
        name='af_redist_ospf',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    af_redist_ospf_metric = managedattribute(
        name='af_redist_ospf_metric',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    af_redist_ospf_route_policy = managedattribute(
        name='af_redist_ospf_route_policy',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    af_redist_rip = managedattribute(
        name='af_redist_rip',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    af_redist_rip_metric = managedattribute(
        name='af_redist_rip_metric',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    af_redist_rip_route_policy = managedattribute(
        name='af_redist_rip_route_policy',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    af_redist_static = managedattribute(
        name='af_redist_static',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    af_redist_static_metric = managedattribute(
        name='af_redist_static_metric',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    af_redist_static_route_policy = managedattribute(
        name='af_redist_static_route_policy',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    af_redist_connected = managedattribute(
        name='af_redist_connected',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    af_redist_connected_metric = managedattribute(
        name='af_redist_connected_metric',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    af_redist_connected_route_policy = managedattribute(
        name='af_redist_connected_route_policy',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    af_v6_aggregate_address_ipv6_address = managedattribute(
        name='af_v6_aggregate_address_ipv6_address',
        default=None,
        type=(None, IPv6Network))

    af_v6_aggregate_address_as_set = managedattribute(
        name='af_v6_aggregate_address_as_set',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    af_v6_aggregate_address_summary_only = managedattribute(
        name='af_v6_aggregate_address_summary_only',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    af_v6_network_number = managedattribute(
        name='af_v6_network_number',
        default=None,
        type=(None, IPv6Network))

    af_v6_network_route_map = managedattribute(
        name='af_v6_network_route_map',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    af_v6_allocate_label_all = managedattribute(
        name='af_v6_allocate_label_all',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    af_retain_rt_all = managedattribute(
        name='af_retain_rt_all',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    af_default_metric = managedattribute(
        name='af_default_metric',
        default=None,
        type=(None, managedattribute.test_istype(bool))
    )
    af_default_metric_value = managedattribute(
        name='af_default_metric_value',
        default=None,
        type=(None, managedattribute.test_istype(int))
    )

    af_default_information_originate = managedattribute(
        name='af_default_information_originate',
        default=None,
        type=(None, managedattribute.test_istype(bool))
    )
    # ==== Neighbor section ======================
    class NBR_TRANSPORT_CONNECTION_MODE(Enum):
        active = 'active'
        passive = 'passive'

    nbr_transport_connection_mode = managedattribute(
        name='nbr_transport_connection_mode',
        default=None,
        type=(None, NBR_TRANSPORT_CONNECTION_MODE),
        doc='Neighbor transport connection mode')

    class NBR_PEER_TYPE(Enum):
        fabric_border_leaf = 'fabric-border-leaf'
        fabric_external = 'fabric-external'

    nbr_peer_type = managedattribute(
        name='nbr_peer_type',
        default=None,
        type=(None, NBR_PEER_TYPE),
        doc='Neighbor peer type')

    class NBR_SEND_COMMUNITY(Enum):
        standard = 'standard'
        extended = 'extended'
        both = 'both'

    nbr_send_community = managedattribute(
        name='nbr_send_community',
        default=None,
        type=(None, NBR_SEND_COMMUNITY),
        doc='Neighbor address family send community type')

    nbr_fall_over_bfd = managedattribute(
        name='nbr_fall_over_bfd',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    nbr_suppress_four_byte_as_capability = managedattribute(
        name='nbr_suppress_four_byte_as_capability',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    nbr_description = managedattribute(
        name='nbr_description',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    nbr_disable_connected_check = managedattribute(
        name='nbr_disable_connected_check',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    nbr_ebgp_multihop = managedattribute(
        name='nbr_ebgp_multihop',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    nbr_ebgp_multihop_max_hop = managedattribute(
        name='nbr_ebgp_multihop_max_hop',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    nbr_inherit_peer_session = managedattribute(
        name='nbr_inherit_peer_session',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    nbr_local_as_as_no = managedattribute(
        name='nbr_local_as_as_no',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    nbr_local_as_no_prepend = managedattribute(
        name='nbr_local_as_no_prepend',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    nbr_local_as_replace_as = managedattribute(
        name='nbr_local_as_replace_as',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    nbr_local_as_dual_as = managedattribute(
        name='nbr_local_as_dual_as',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    nbr_remote_as = managedattribute(
        name='nbr_remote_as',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    nbr_remove_private_as = managedattribute(
        name='nbr_remove_private_as',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    class NBR_REMOVE_PRIVATE_AS_AF_NAME(Enum):
        ipv4_unicast = 'ipv4 unicast'
        ipv6_unicast = 'ipv6 unicast'

    nbr_remove_private_as_af_name = managedattribute(
        name='nbr_remove_private_as_af_name',
        default=None,
        type=(None, NBR_REMOVE_PRIVATE_AS_AF_NAME),
        doc='meighbor remove private as')

    nbr_shutdown = managedattribute(
        name='nbr_shutdown',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    nbr_keepalive_interval = managedattribute(
        name='nbr_keepalive_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    nbr_holdtime = managedattribute(
        name='nbr_holdtime',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    nbr_update_source = managedattribute(
        name='nbr_update_source',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    nbr_password_text = managedattribute(
        name='nbr_password_text',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # ==== Neighbor/Address-family section =======
    nbr_af_name = managedattribute(
        name='nbr_af_name',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    nbr_af_suppress_signaling_protocol_ldp = managedattribute(
        name='nbr_af_suppress_signaling_protocol_ldp',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    nbr_af_allowas_in = managedattribute(
        name='nbr_af_allowas_in',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    nbr_af_allowas_in_as_number = managedattribute(
        name='nbr_af_allowas_in_as_number',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    nbr_af_inherit_peer_policy = managedattribute(
        name='nbr_af_inherit_peer_policy',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    nbr_af_inherit_peer_seq = managedattribute(
        name='nbr_af_inherit_peer_seq',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    nbr_af_maximum_prefix_max_prefix_no = managedattribute(
        name='nbr_af_maximum_prefix_max_prefix_no',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    nbr_af_maximum_prefix_threshold = managedattribute(
        name='nbr_af_maximum_prefix_threshold',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    nbr_af_maximum_prefix_restart = managedattribute(
        name='nbr_af_maximum_prefix_restart',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    nbr_af_maximum_prefix_warning_only = managedattribute(
        name='nbr_af_maximum_prefix_warning_only',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    nbr_af_route_map_name_in = managedattribute(
        name='nbr_af_route_map_name_in',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    nbr_af_route_map_name_out = managedattribute(
        name='nbr_af_route_map_name_out',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    nbr_af_route_reflector_client = managedattribute(
        name='nbr_af_route_reflector_client',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    nbr_af_suppress_inactive = managedattribute(
        name='nbr_af_suppress_inactive',
        default=None,
        type=(None, managedattribute.test_istype(bool))
    )

    nbr_af_disable_peer_as_check = managedattribute(
        name='nbr_af_disable_peer_as_check',
        default=None,
        type=(None, managedattribute.test_istype(bool))
    )

    class NBR_AF_SEND_COMMUNITY(Enum):
        standard = 'standard'
        extended = 'extended'
        both = 'both'

    nbr_af_send_community = managedattribute(
        name='nbr_af_send_community',
        default=None,
        type=(None, NBR_AF_SEND_COMMUNITY),
        doc='Neighbor address family send community type')

    nbr_af_soft_reconfiguration = managedattribute(
        name='nbr_af_soft_reconfiguration',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    nbr_af_next_hop_self = managedattribute(
        name='nbr_af_next_hop_self',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    nbr_af_as_override = managedattribute(
        name='nbr_af_as_override',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    nbr_af_default_originate = managedattribute(
        name='nbr_af_default_originate',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    nbr_af_default_originate_route_map = managedattribute(
        name='nbr_af_default_originate_route_map',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    nbr_af_soo = managedattribute(
        name='nbr_af_soo',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    nbr_af_rewrite_evpn_rt_asn = managedattribute(
        name='nbr_af_rewrite_evpn_rt_asn',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    nbr_af_rewrite_mvpn_rt_asn = managedattribute(
        name='nbr_af_rewrite_mvpn_rt_asn',
        default=None,
        type=(None, managedattribute.test_istype(bool)))
    # XXXJST TODO Merge with send_community_ebgp
    send_community = managedattribute(
        name='send_community',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    ha_mode = managedattribute(
        name='ha_mode',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    bfd_fast_detect = managedattribute(
        name='bfd_fast_detect',
        default=None,
        type=(None,
              managedattribute.test_istype(bool),
              managedattribute.test_in((
                  'strict-mode',
              ))))
    # this will configured under vrf in Takashi's structure
    # this one is under vrf/neighbor
    bfd_minimum_interval = managedattribute(
        name='bfd_minimum_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    bfd_multiplier = managedattribute(
        name='bfd_multiplier',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # ########
    # only supports in XR, TODO apply in other platforms
    encapsulation_type = managedattribute(
        name='encapsulation_type',
        default=None,
        type=(None, managedattribute.test_in((
            'mpls',
            'vxlan',
        ))))

    import_stitching_rt = managedattribute(
        name='import_stitching_rt',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    import_re_originate = managedattribute(
        name='import_re_originate',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    import_re_originate_stitching_rt = managedattribute(
        name='import_re_originate_stitching_rt',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    import_stitching_rt_re_originate = managedattribute(
        name='import_stitching_rt_re_originate',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    advertise_l2vpn_evpn_re_originated = managedattribute(
        name='advertise_l2vpn_evpn_re_originated',
        default=None,
        type=(None,
              managedattribute.test_istype(bool),
              managedattribute.test_in((
                  'regular-rt',
                  'stitching-rt',
              ))))

    advertise_vpnv4_unicast = managedattribute(
        name='advertise_vpnv4_unicast',
        default=None,
        type=(None, managedattribute.test_istype(bool)))
    # ##############

    route_policy_in = managedattribute(
        name='route_policy_in',
        default=None,
        type=(None,
              managedattribute.test_istype(RoutePolicy)))

    route_policy_out = managedattribute(
        name='route_policy_out',
        default=None,
        type=(None,
              managedattribute.test_istype(RoutePolicy)))

    send_community_ebgp = managedattribute(
        name='send_community_ebgp',
        default=None,
        type=(None,
              managedattribute.test_istype(bool)))

    retain_route_target = managedattribute(
        name='retain_route_target',
        default=None,
        type=(None,
              managedattribute.test_istype(bool),
              managedattribute.test_istype(RoutePolicy)))

    disable_bgp_default_ipv4_unicast = managedattribute(
        name='disable_bgp_default_ipv4_unicast',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    route_reflector_client = managedattribute(
        name='route_reflector_client',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    route_reflector_client_inheritance_disable = managedattribute(
        name='route_reflector_client_inheritance_disable',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    nexthop_self = managedattribute(
        name='nexthop_self',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    nexthop_self_inheritance_disable = managedattribute(
        name='nexthop_self_inheritance_disable',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    ebgp_multihop_max_hop_count = managedattribute(
        name='ebgp_multihop_max_hop_count',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    ebgp_multihop_mpls = managedattribute(
        name='ebgp_multihop_mpls',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    send_extended_community_ebgp = managedattribute(
        name='send_extended_community_ebgp',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    send_extended_community_ebgp_inheritance_disable = managedattribute(
        name='send_extended_community_ebgp_inheritance_disable',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ########
    # only supports in XR, TODO apply in other platforms
    nexthop_mpls_forwarding_ibgp = managedattribute(
        name='nexthop_mpls_forwarding_ibgp',
        default=None,
        type=(None, managedattribute.test_istype(bool)))
    # #########

    as_override = managedattribute(
        name='as_override',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    as_override_inheritance = managedattribute(
        name='as_override_inheritance',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    allocate_label = managedattribute(
        name='allocate_label',
        default=None,
        type=(None,
              managedattribute.test_istype(RoutePolicy),
              managedattribute.test_in((
                  'all',
              ))))

    label_mode = managedattribute(
        name='label_mode',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    maximum_paths_ibgp = managedattribute(
        name='maximum_paths_ibgp',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    maximum_paths_ebgp = managedattribute(
        name='maximum_paths_ebgp',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    redistributes = managedattribute(
        name='redistributes',
        fdef=list,
        type=managedattribute.test_list_of(Redistribution))

    class DeviceAttributes(genie.conf.base.attributes.DeviceSubAttributes):

        update_source = managedattribute(
            name='update_source',
            default=None,
            type=(None, managedattribute.test_isinstance(Interface)))

        vrfs = managedattribute(
            name='vrfs',
            finit=typedset(managedattribute.test_isinstance((
                type(None), Vrf)), {None}).copy,
            type=typedset(managedattribute.test_isinstance((
                type(None), Vrf)))._from_iterable)

        def add_vrf(self, vrf):  # TODO DEPRECATE
            self.vrfs.add(vrf)

        def remove_vrf(self, vrf):  # TODO DEPRECATE
            self.vrfs.remove(vrf)

        @property
        def router_id(self):
            return self.vrf_attr[None].router_id

        @router_id.setter
        def router_id(self, value):
            self.vrf_attr[None].router_id = value

        class PeerSessionAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.ps_name = key
                super().__init__(parent)

        peer_session_attr = managedattribute(
            name='peer_session_attr',
            read_only=True,
            doc=PeerSessionAttributes.__doc__)

        @peer_session_attr.initter
        def peer_session_attr(self):
            return SubAttributesDict(self.PeerSessionAttributes, parent=self)

        class PeerPolicyAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.pp_name = key
                super().__init__(parent)

        peer_policy_attr = managedattribute(
            name='peer_policy_attr',
            read_only=True,
            doc=PeerPolicyAttributes.__doc__)

        @peer_policy_attr.initter
        def peer_policy_attr(self):
            return SubAttributesDict(self.PeerPolicyAttributes, parent=self)

        class VrfAttributes(VrfSubAttributes):
            rd = Vrf.rd.copy()

            @rd.defaulter
            def rd(self):
                vrf = self.vrf
                return vrf and vrf.rd

            address_families = managedattribute(
                name='address_families',
                finit=typedset(AddressFamily).copy,
                type=typedset(AddressFamily)._from_iterable)

            @address_families.defaulter
            def address_families(self):
                return self.parent.address_families.copy()

            class AddressFamilyAttributes(AddressFamilySubAttributes):
                pass

            address_family_attr = managedattribute(
                name='address_family_attr',
                read_only=True,
                doc=AddressFamilySubAttributes.__doc__)

            @address_family_attr.initter
            def address_family_attr(self):
                return SubAttributesDict(self.AddressFamilyAttributes,
                                         parent=self)

            class NeighborAttributes(IPNeighborSubAttributes):
                address_families = managedattribute(
                    name='address_families',
                    finit=typedset(AddressFamily).copy,
                    type=typedset(AddressFamily)._from_iterable)

                @address_families.defaulter
                def address_families(self):
                    return self.parent.address_families.copy()

                class AddressFamilyAttributes(AddressFamilySubAttributes):
                    pass

                address_family_attr = managedattribute(
                    name='address_family_attr',
                    read_only=True,
                    doc=AddressFamilySubAttributes.__doc__)

                @address_family_attr.initter
                def address_family_attr(self):
                    return SubAttributesDict(self.AddressFamilyAttributes,
                                             parent=self)

            neighbor_attr = managedattribute(
                name='neighbor_attr',
                read_only=True,
                doc=NeighborAttributes.__doc__)

            @neighbor_attr.initter
            def neighbor_attr(self):
                return SubAttributesDict(self.NeighborAttributes, parent=self)

            router_id = managedattribute(
                name='router_id',
                default=None,
                type=(None, IPv4Address))

            neighbors = managedattribute(
                name='neighbors',
                finit=set,
                type=managedattribute.test_set_of(IPNeighbor),
                gettype=frozenset)

            neighbors = managedattribute(
                name='neighbors',
                finit=typedset(IPNeighbor).copy,
                type=typedset(IPNeighbor)._from_iterable)

            def add_neighbor(self, neighbor):  # TODO DEPRECATE
                self.neighbors.add(neighbor)

            def remove_neighbor(self, neighbor):  # TODO DEPRECATE
                self.neighbors.remove(neighbor)

        vrf_attr = managedattribute(
            name='vrf_attr',
            read_only=True,
            doc=VrfAttributes.__doc__)

        @vrf_attr.initter
        def vrf_attr(self):
            return SubAttributesDict(self.VrfAttributes, parent=self)

        @property
        def neighbors(self):
            return self.vrf_attr[None].neighbors

        @property
        def add_neighbor(self):
            return self.vrf_attr[None].add_neighbor

        @property
        def remove_neighbor(self):
            return self.vrf_attr[None].remove_neighbor

        @property
        def address_family_attr(self):
            return self.vrf_attr[None].address_family_attr

        @property
        def neighbor_attr(self):
            return self.vrf_attr[None].neighbor_attr

        def __init__(self, parent, key):
            super().__init__(parent, key)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    def __init__(self, asn=None, bgp_id=None, instance_name=None, *args, **kwargs):
        if asn:
            self.asn = asn
        if bgp_id:
            self.bgp_id = int(bgp_id)
        if instance_name:
            self.instance_name = instance_name
        super().__init__(*args, **kwargs)

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

    @classmethod
    def learn_config(self, device, **kwargs):
        '''
            A method that learn the device configurational state and create
            a conf object with the same configuration.

            Args:
                self (`obj`): Conf object.
                device (`obj`): The device that will be used to parse the
                    command.
        '''

        # Abstracting the show running bgp as per device os
        ret = Lookup.from_device(device)
        cmd = ret.parser.show_bgp.ShowRunningConfigBgp

        maker = ops_Base(device=device)

        maker.add_leaf(cmd=cmd,
                       src='[bgp][instance][(?P<instance>.*)][bgp_id]',
                       dest='bgp[instance][(?P<instance>.*)][bgp_id]')

        maker.add_leaf(cmd=cmd,
                       src='[bgp][instance][(?P<instance>.*)]'
                           '[protocol_shutdown]',
                       dest='bgp[instance][(?P<instance>.*)]'
                            '[protocol_shutdown]')

        maker.add_leaf(cmd=cmd,
                       src='[bgp][instance][(?P<instance>.*)][pp_name]'
                           '[(?P<pp_name>.*)]',
                       dest='bgp[instance][(?P<instance>.*)][peer_policy_attr]'
                            '[(?P<pp_name>.*)]')

        maker.add_leaf(cmd=cmd,
                       src='[bgp][instance][(?P<instance>.*)][ps_name]'
                           '[(?P<ps_name>.*)]',
                       dest='bgp[instance][(?P<instance>.*)]'
                            '[peer_session_attr][(?P<ps_name>.*)]')

        maker.add_leaf(cmd=cmd,
                       src='[bgp][instance][(?P<instance>.*)]'
                           '[vrf][(?P<vrf>.*)]',
                       dest='bgp[instance][(?P<instance>.*)][vrf_attr]'
                            '[(?P<vrf>.*)]')

        maker.add_leaf(cmd=cmd,
                       src='[bgp][instance][(?P<instance>.*)][vrf]'
                           '[(?P<vrf>.*)][af_name][(?P<af_name>.*)]',
                       dest='bgp[instance][(?P<instance>.*)][vrf_attr]'
                            '[(?P<vrf>.*)][address_family_attr]'
                            '[(?P<af_name>.*)]')

        maker.add_leaf(cmd=cmd,
                       src='[bgp][instance][(?P<instance>.*)][vrf]'
                           '[(?P<vrf>.*)][neighbor_id][(?P<neighbor_id>.*)]',
                       dest='bgp[instance][(?P<instance>.*)][vrf_attr]'
                            '[(?P<vrf>.*)][neighbor_attr]'
                            '[(?P<neighbor_id>.*)]')

        maker.add_leaf(cmd=cmd,
                       src='[bgp][instance][(?P<instance>.*)][vrf]'
                           '[(?P<vrf>.*)][neighbor_id][(?P<neighbor_id>.*)]'
                           '[nbr_af_name][(?P<nbr_af_name>.*)]',
                       dest='bgp[instance][(?P<instance>.*)][vrf_attr]'
                            '[(?P<vrf>.*)][neighbor_attr][(?P<neighbor_id>.*)]'
                            '[address_family_attr][(?P<nbr_af_name>.*)]')

        # A workaround to pass the context as in maker it expects Context.cli
        # not just a string 'cli.
        maker.context_manager[cmd] = Context.cli

        maker.make()

        # Take a copy of the object dictionary
        if not hasattr(maker, 'bgp'):
            maker.bgp = {}
        new_bgp = maker.bgp

        # List of mapped conf objects
        conf_obj_list = []

        # Main structure attributes in the conf object
        structure_keys = ['peer_policy_attr',
                          'vrf_attr',
                          'peer_session_attr',
                          'address_family_attr',
                          'neighbor_attr']

        # Deleting the old format keys from the object and building the
        # conf objects
        for instance_key in new_bgp['instance']:
            if 'vrf_attr' in new_bgp['instance'][instance_key]:
                for vrf in new_bgp['instance'][instance_key]['vrf_attr']:
                    if 'neighbor_id' in new_bgp['instance'][instance_key] \
                            ['vrf_attr'][vrf]:
                        del new_bgp['instance'][instance_key]['vrf_attr'][vrf] \
                            ['neighbor_id']
                    if 'af_name' in new_bgp['instance'][instance_key] \
                            ['vrf_attr'][vrf]:
                        del new_bgp['instance'][instance_key]['vrf_attr'][vrf] \
                            ['af_name']
                    if 'neighbor_attr' in new_bgp['instance'][instance_key] \
                            ['vrf_attr'][vrf]:
                        for neighbor in new_bgp['instance'][instance_key] \
                                ['vrf_attr'][vrf]['neighbor_attr'].keys():
                            if 'nbr_af_name' in new_bgp['instance'] \
                                    [instance_key]['vrf_attr'][vrf] \
                                    ['neighbor_attr'][neighbor]:
                                del new_bgp['instance'][instance_key] \
                                    ['vrf_attr'][vrf]['neighbor_attr'] \
                                    [neighbor]['nbr_af_name']

            # Instiantiate a BGP conf object
            conf_obj = self(bgp_id=new_bgp['instance'][instance_key]['bgp_id'])

            # Pass the class method not the instnace.
            maker.dict_to_obj(conf=conf_obj, \
                              struct=structure_keys, \
                              struct_to_map=new_bgp['instance'][instance_key])

            conf_obj_list.append(conf_obj)

        # List of mapped conf objects
        return conf_obj_list
