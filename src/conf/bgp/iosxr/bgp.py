# import python
import warnings
from abc import ABC

# import genie
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import \
    UnsupportedAttributeWarning, AttributesHelper

# import genie.libs
from genie.libs.conf.rip import Rip
from genie.libs.conf.ospf import Ospf
from genie.libs.conf.isis import Isis
from genie.libs.conf.vrf import VrfSubAttributes
from genie.libs.conf.route_policy import RoutePolicy
from genie.libs.conf.address_family import AddressFamily

# Structure Hierarchy:
# Bgp
#   +--DeviceAttributes
#        +-- PeerSessionAttributes
#        +-- PeerPolicyAttributes
#        +-- VrfAttributes
#              +-- AddressFamilyAttributes
#              +-- NeighborAttributes
#                    +-- AddressFamilyAttributes


class Bgp(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None,
                         unconfig=False, **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            bgp_id = self.bgp_id or self.asn
            # iosxr: router bgp 100 [instance someword]
            line = 'router bgp {}'.format(bgp_id)
            if (self.instance_name and \
                self.instance_name != 'default') or \
               (attributes.value('instance_name') and \
                attributes.value('instance_name') != 'default'):
                line += ' instance {instance_name}'

            # iosxr: router bgp 100 [instance someword](config-bgp)
            with configurations.submode_context(attributes.format(line,
                                                                  force=True)):
                if unconfig:
                    if (attributes.attributes and \
                      'instance_name' in attributes.attributes and \
                      isinstance(attributes.attributes['instance_name'], dict) and \
                      None in attributes.attributes['instance_name'].values()) or \
                      attributes.iswildcard:
                        configurations.submode_unconfig()

                # iosxr: router bgp 100 [instance someword] / nsr
                # iosxr: router bgp 100 [instance someword] / nsr disable
                v = attributes.value('nsr')
                if v is not None:
                    if v:
                        configurations.append_line('nsr')
                    else:
                        configurations.append_line('nsr disable')

                # iosxr: router bgp 100 [instance someword] /
                # vrf someword (config-bgp-vrf)
                for sub, attributes2 in attributes.mapping_values(
                    'vrf_attr', sort=True):
                    configurations.append_block(
                        sub.build_config(apply=False,
                                         attributes=attributes2,
                                         unconfig=unconfig))

                # iosxr: router bgp 100 [instance someword]
                # / session-group <ps_name>
                for sub, attributes2 in attributes.mapping_values(
                    'peer_session_attr'):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig,
                                             **kwargs))

                # iosxr: router bgp 100 [instance someword]
                # / af-group <pp_name> address-family <af_name>
                for sub, attributes2 in attributes.mapping_values(
                    'peer_policy_attr'):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig,
                                             **kwargs))

                # iosxr: router bgp 100 / [instance someword] /
                # ibgp policy out enforce-modifications
                if attributes.value('ibgp_policy_out_enforce_modifications'):
                    configurations.append_line(
                        'ibgp policy out enforce-modifications')

            if apply:
                if configurations:
                    self.device.configure(configurations, fail_invalid=True)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations, fail_invalid=True)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply,
                                     attributes=attributes,
                                     unconfig=True, **kwargs)


        class PeerSessionAttributes(ABC):

            def build_config(self, apply=True, attributes=None,
                              unconfig=False, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)
                with configurations.submode_context(
                    attributes.format(
                        'session-group {ps_name}',force=True)):
                    if unconfig and attributes.iswildcard:
                        # Never reached!
                        configurations.submode_unconfig()

                    # iosxr: session-group <peer_session> \ bfd fast-detect
                    if attributes.value('ps_fall_over_bfd'):
                        configurations.append_line(
                            attributes.format('bfd fast-detect'))

                    # iosxr: session-group <peer_session> \
                    # capability suppress 4-byte-as
                    if attributes.value(
                        'ps_suppress_four_byte_as_capability'):
                        configurations.append_line(attributes.format(
                            'capability suppress 4-byte-as'))

                    # iosxr: session-group <peer_session> \
                    # description PEER-SESSION
                    if attributes.value('ps_description'):
                        configurations.append_line(
                            attributes.format('description {ps_description}'))

                    # iosxr: session-group <peer_session> \
                    # ignore-connected-check
                    if attributes.value('ps_disable_connected_check'):
                        configurations.append_line(
                            attributes.format('ignore-connected-check'))

                    # iosxr: session-group <peer_session> \
                    # ebgp-multihop 255
                    if attributes.value('ps_ebgp_multihop_max_hop'):
                        configurations.append_line(
                            attributes.format('ebgp-multihop '
                                '{ps_ebgp_multihop_max_hop}'))
                    elif attributes.value('ps_ebgp_multihop'):
                        configurations.append_line(
                            attributes.format('ebgp-multihop'))

                    # iosxr: session-group <peer_session> \
                    # local-as 111 [no-prepend replace-as dual-as]
                    if attributes.value('ps_local_as_as_no'):
                        base_s = 'local-as {ps_local_as_as_no}'
                        if attributes.value('ps_local_as_no_prepend'):
                            base_s += ' no-prepend'
                        if attributes.value('ps_local_as_replace_as'):
                            base_s += ' replace-as'
                        if attributes.value('ps_local_as_dual_as'):
                            base_s += ' dual-as'
                        configurations.append_line(
                            attributes.format(base_s))

                    # iosxr: session-group <peer_session> \
                    # password 386c0565965f89de
                    if attributes.value('ps_password_text'):
                        configurations.append_line(
                            attributes.format('password {ps_password_text}'))

                    # iosxr: session-group <peer_session> \ remote-as 500
                    if attributes.value('ps_remote_as'):
                        configurations.append_line(
                            attributes.format('remote-as {ps_remote_as}'))

                    # iosxr: session-group <peer_session> \ shutdown
                    if attributes.value('ps_shutdown'):
                        configurations.append_line(
                            attributes.format('shutdown'))

                    # iosxr: session-group <peer_session> \
                    # timers 111 222
                    if attributes.value('ps_keepalive_interval') and \
                        attributes.value('ps_hodltime'):
                        configurations.append_line(
                            attributes.format('timers bgp '
                                '{ps_keepalive_interval} {ps_hodltime}'))

                    # iosxr: session-group <peer_session> \
                    # transport connection-mode passive
                    if attributes.value('ps_transport_connection_mode'):
                        configurations.append_line(attributes.format(
                            'session-open-mode '
                            '{ps_transport_connection_mode.value}'))

                    # iosxr: session-group <peer_session> \
                    # update-source loopback0
                    if attributes.value('ps_update_source'):
                        configurations.append_line(
                            attributes.format('update-source '
                                              '{ps_update_source}'))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)


        class PeerPolicyAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)
                if not attributes.value('pp_af_name'):
                    return ''
                with configurations.submode_context(
                    attributes.format(
                        'af-group {pp_name} address-family {pp_af_name.value}',
                        force=True)):
                    if unconfig and attributes.iswildcard:
                        # Never reached!
                        configurations.submode_unconfig()

                    # iosxr: af-group <pp_name> address-family <pp_af_name> \
                    # allowas-in [9]
                    if attributes.value('pp_allowas_in'):
                        if attributes.value('pp_allowas_in_as_number'):
                            configurations.append_line(
                                attributes.format('allowas-in '
                                                  '{pp_allowas_in_as_number}'))
                        else:
                            configurations.append_line(
                                attributes.format('allowas-in'))

                    # iosxr: af-group <pp_name> address-family <pp_af_name> \
                    # as-override
                    if attributes.value('pp_as_override'):
                        configurations.append_line(
                            attributes.format('as-override'))

                    # iosxr: af-group <pp_name> address-family <pp_af_name> \
                    # default-originate
                    # iosxr: af-group <pp_name> address-family <pp_af_name> \
                    # default-originate route-policy test
                    if attributes.value('pp_default_originate'):
                        if attributes.value(
                            'pp_default_originate_route_map'):
                            configurations.append_line(
                                attributes.format('default-originate '
                                'route-policy '
                                '{pp_default_originate_route_map}'))
                        else:
                            configurations.append_line(
                                attributes.format('default-originate'))

                    # iosxr: af-group <pp_name> address-family <pp_af_name> \
                    # route-policy test-map in
                    if attributes.value('pp_route_map_name_in'):
                        configurations.append_line(
                            attributes.format('route-policy '
                                '{pp_route_map_name_in} in'))

                    # iosxr: af-group <pp_name> address-family <pp_af_name> \
                    # route-policy test-map out
                    if attributes.value('pp_route_map_name_out'):
                        configurations.append_line(
                            attributes.format('route-policy '
                                '{pp_route_map_name_out} out'))

                    # iosxr: af-group <pp_name> address-family <pp_af_name> \
                    # mmaximum-prefix <pp_maximum_prefix_max_prefix_no> 
                    # [<pp_maximum_prefix_threshold> ]
                    # [restart <pp_maximum_prefix_restart> | warning-only ]
                    if attributes.value('pp_maximum_prefix_max_prefix_no'):
                        line = 'maximum-prefix '\
                               '{pp_maximum_prefix_max_prefix_no}'
                        if attributes.value('pp_maximum_prefix_threshold'):
                            line += ' {pp_maximum_prefix_threshold}'
                        if attributes.value('pp_maximum_prefix_restart'):
                            line += ' restart {pp_maximum_prefix_restart}'
                        elif attributes.value(
                            'pp_maximum_prefix_warning_only'):
                            line += ' warning-only'
                        configurations.append_line(attributes.format(line))

                    # iosxr: af-group <pp_name> address-family <pp_af_name> \
                    # next-hop-self
                    if attributes.value('pp_next_hop_self'):
                        configurations.append_line(
                            attributes.format(
                                'next-hop-self'))

                    # iosxr: af-group <pp_name> address-family <pp_af_name> \
                    # route-reflector-client
                    if attributes.value('pp_route_reflector_client'):
                        configurations.append_line(
                            attributes.format(
                                'route-reflector-client'))

                    # iosxr: af-group <pp_name> address-family <pp_af_name> \
                    # send-community-ebgp
                    if attributes.value('pp_send_community'):
                        if attributes.value('pp_send_community').value ==\
                          'standard':
                            configurations.append_line(attributes.format(
                                'send-community-ebgp'))

                        # iosxr: template peer-session <peer_session> \
                        # send-extended-community-ebgp
                        if attributes.value('pp_send_community').value ==\
                          'extended':
                            configurations.append_line(attributes.format(
                                'send-extended-community-ebgp'))

                        # iosxr: af-group <pp_name> address-family <pp_af_name> \
                        # send-community-ebgp
                        # send-extended-community-ebgp
                        if attributes.value('pp_send_community').value == 'both':
                            configurations.append_line(attributes.format(
                                'send-community-ebgp'))
                            configurations.append_line(attributes.format(
                                'send-extended-community-ebgp'))

                    # iosxr: af-group <pp_name> address-family <pp_af_name> \
                    # soft-reconfiguration inbound
                    if attributes.value('pp_soft_reconfiguration'):
                        configurations.append_line(
                            attributes.format('soft-reconfiguration inbound'))

                    # iosxr: af-group <pp_name> address-family <pp_af_name> \
                    # site-of-origin 100:100
                    if attributes.value('pp_soo') and \
                       self.vrf_id != 'default':
                        configurations.append_line(
                            attributes.format('site-of-origin {pp_soo}'))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)


        class VrfAttributes(ABC):

            def build_config(self, apply=True, attributes=None,
                             unconfig=False, **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # iosxr: router bgp 100 / instance someword (config-bgp)
                # iosxr: router bgp 100 / [instance someword] /
                # vrf someword (config-bgp-vrf)
                with configurations.submode_context(
                        None if self.vrf_name == 'default' else \
                        attributes.format('vrf {vrf_name}', force=True)):
                    if self.vrf_name != 'default' and unconfig \
                        and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # iosxr: router bgp 100 / [instance someword] /
                    # [vrf someword] / bfd minimum-interval 3
                    if attributes.value('bfd_minimum_interval'):
                        configurations.append_line(attributes.format(
                            'bfd minimum-interval {bfd_minimum_interval}'))

                    # iosxr: router bgp 100 / [instance someword] /
                    # [vrf someword] / bfd multiplier 2
                    if attributes.value('bfd_multiplier'):
                        configurations.append_line(attributes.format(
                            'bfd multiplier {bfd_multiplier}'))

                    # iosxr: router bgp 100 [instance someword] /
                    # [vrf someword] /bgp bestpath cost-community ignore |
                    # bgp bestpath compare-routerid |
                    # bgp bestpath med always |
                    # bgp bestpath med missing-as-worst
                    if attributes.value('always_compare_med'):
                        configurations.append_line(attributes.format(
                            'bgp bestpath med always'))
                    if attributes.value('bestpath_compare_routerid'):
                        configurations.append_line(attributes.format(
                            'bgp bestpath compare-routerid'))
                    if attributes.value('bestpath_cost_community_ignore'):
                        configurations.append_line(attributes.format(
                            'bgp bestpath cost-community ignore'))
                    if attributes.value('bestpath_med_missing_at_worst'):
                        configurations.append_line(attributes.format(
                            'bgp bestpath med missing-as-worst'))

                    # iosxr: router bgp 100 [instance someword] /
                    # [vrf someword] / bgp cluster-id <cluster_id>
                    if attributes.value('cluster_id') and \
                       self.vrf_name == 'default':
                        configurations.append_line(attributes.format(
                            'bgp cluster-id {cluster_id}'))

                    # iosxr: router bgp 100 [instance someword] /
                    # [vrf someword] / bgp confederation identifier 
                    # <confederation_identifier>
                    if attributes.value('confederation_identifier') and \
                       self.vrf_name == 'default':
                        configurations.append_line(
                            attributes.format('bgp confederation identifier '
                                '{confederation_identifier}'))

                    # iosxr: router bgp 100 [instance someword] /
                    # [vrf someword] / bgp confederation peers 
                    # <confederation_peers_as>
                    if attributes.value('confederation_peers_as') and \
                       self.vrf_name == 'default':
                        configurations.append_line(
                            attributes.format('bgp confederation peers '
                                '{confederation_peers_as}'))

                    # iosxr: router bgp 100 [instance someword] /
                    # vrf someword / rd 100.200:300 | rd auto
                    if attributes.value('rd') and self.vrf_name != 'default':
                        configurations.append_line(attributes.format('rd {rd}'))

                    # iosxr: router bgp 100 [instance someword] /
                    # bgp graceful-restart
                    if self.vrf_name == 'default':
                        if attributes.value('graceful_restart'):
                            configurations.append_line('bgp graceful-restart')

                        # iosxr: router bgp 100 [instance someword] /
                        # bgp graceful-restart restart-time 1
                        if attributes.value('graceful_restart_restart_time'):
                            configurations.append_line(
                                attributes.format('bgp graceful-restart '
                                    'restart-time '
                                    '{graceful_restart_restart_time}'))

                        # iosxr: router bgp 100 [instance someword] /
                        # bgp graceful-restart stalepath-time 1
                        if attributes.value('graceful_restart_stalepath_time'):
                            configurations.append_line(
                                attributes.format('bgp graceful-restart '
                                    'stalepath-time '
                                    '{graceful_restart_stalepath_time}'))

                    # iosxr: router bgp 100 [vrf someword] /
                    # bgp log neighbor changes disable
                    if attributes.value('log_neighbor_changes') is False:
                        configurations.append_line(
                            attributes.format(
                                'bgp log neighbor changes disable'))

                    # iosxr: router bgp 100 [instance someword] /
                    # [vrf someword] / bgp router-id 1.2.3.4
                    #TODO: what about router id as loopback interface object ?
                    configurations.append_line(attributes.format(
                        'bgp router-id {router_id}'))

                    # iosxr: router bgp 100 [instance someword] /
                    # [vrf someword] /
                    # timers bgp <keepalive-interval> <holdtime>
                    if attributes.value('keepalive_interval') and \
                        attributes.value('holdtime'):
                        configurations.append_line(
                            attributes.format('timers bgp '
                                '{keepalive_interval} {holdtime}'))

                    # iosxr: router bgp 100 [instance someword] /
                    # [vrf someword] /
                    # bgp enforce-first-as disable
                    if attributes.value('enforce_first_as') is False:
                        configurations.append_line(
                            attributes.format('bgp enforce-first-as disable'))

                    # iosxr: router bgp 100 [instance someword] /
                    # [vrf someword] / 
                    # bgp fast-external-fallover disable
                    if attributes.value('fast_external_fallover') is False:
                        configurations.append_line(
                            attributes.format(
                                'bgp fast-external-fallover disable'))

                    # iosxr: router bgp 100 [instance someword] /
                    # [vrf someword] / address-family ... (config-bgp-vrf-af)
                    for sub, attributes2 in attributes.mapping_values(
                        'address_family_attr', sort=True):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))

                    # iosxr: router bgp 100 [instance someword] /
                    # [vrf someword] / neighbor <ipv4|ipv6> (config-bgp-vrf-nbr)
                    for sub, attributes2 in attributes.mapping_values(
                        'neighbor_attr'):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))

                    # iosxr: router bgp 100 [instance someword] /
                    # [vrf someword] / nexthop mpls forwarding ibgp
                    if attributes.value('nexthop_mpls_forwarding_ibgp'):
                        configurations.append_line(
                            'nexthop mpls forwarding ibgp')

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply,
                                         attributes=attributes,
                                         unconfig=True, **kwargs)

            class AddressFamilyAttributes(ABC):

                def build_config(self, apply=True, attributes=None,
                                 unconfig=False, **kwargs):
                    assert not apply
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    # iosxr: router bgp 100 [instance someword] /
                    # [vrf someword] / address-family ... (config-bgp-vrf-af)
                    with configurations.submode_context(attributes.format(
                        'address-family {address_family.value}', force=True)):
                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # iosxr: address-family ipv4 unicast/
                        # bgp dampening
                        # bgp dampening 25 |
                        # bgp dampening 25 1000 1500 255 |
                        # bgp dampening route_map_name
                        if attributes.value('af_dampening'):
                            if attributes.value(
                                'af_dampening_half_life_time') and \
                               attributes.value(
                                'af_dampening_reuse_time') and \
                               attributes.value(
                                'af_dampening_suppress_time') and \
                               attributes.value(
                                'af_dampening_max_suppress_time'):
                                configurations.append_line(
                                    attributes.format('bgp dampening '
                                        '{af_dampening_half_life_time} '
                                        '{af_dampening_resuse_time} '
                                        '{af_dampening_suppress_time} '
                                        '{af_dampening_max_suppress_time}'))
                            elif attributes.value(
                                'af_dampening_half_life_time'):
                                configurations.append_line(attributes.format(
                                    'bgp dampening '
                                    '{af_dampening_half_life_time}'))
                            elif attributes.value(
                                'af_dampening_route_map'):
                                configurations.append_line(attributes.format(
                                    'bgp dampening '
                                    'route-policy {af_dampening_route_map}'))
                            else:
                                configurations.append_line('bgp dampening')

                        # iosxr: address-family ipv4 unicast/
                        # nexthop route-map <af_nexthop_route_map>
                        if attributes.value('af_nexthop_route_map') and \
                           self.vrf_name == 'default':
                            configurations.append_line(
                                attributes.format(
                                    'nexthop route-policy '
                                    '{af_nexthop_route_map}'))

                        # iosxr: address-family ipv4 unicast/
                        # nexthop trigger-delay critical
                        # <af_nexthop_trigger_delay_critical> 
                        # nexthop trigger-delay non-critical
                        # <af_nexthop_trigger_delay_non_critical>
                        if attributes.value('af_nexthop_trigger_enable') and \
                           self.vrf_name == 'default':
                            if attributes.value(
                                'af_nexthop_trigger_delay_critical'):
                                configurations.append_line(attributes.format(
                                    'nexthop trigger-delay critical '
                                    '{af_nexthop_trigger_delay_critical}'))
                            elif attributes.value(
                                    'af_nexthop_trigger_delay_non_critical'):
                                configurations.append_line(attributes.format(
                                    'nexthop trigger-delay non-critical '
                                    '{af_nexthop_trigger_delay_non_critical}'))

                        # iosxr: address-family ipv4 unicast/
                        # bgp client-to-client reflection disable
                        if attributes.value('af_client_to_client_reflection') \
                           is False:
                            configurations.append_line(
                                attributes.format(
                                    'bgp client-to-client reflection disable'))

                        # iosxr: address-family ipv4 unicast/
                        # distance <af_distance_extern_as> 
                        # <af_distance_internal_as> <af_distance_local>
                        if attributes.value('af_distance_extern_as') and \
                           attributes.value('af_distance_internal_as') and \
                           attributes.value('af_distance_local') :
                            configurations.append_line(
                                attributes.format(
                                    'distance bgp {af_distance_extern_as} '
                                    '{af_distance_internal_as} '
                                    '{af_distance_local}'))

                        # iosxr: address-family ipv4 unicast/ 
                        # maximum-paths ebgp <af_maximum_paths_ebgp>
                        if attributes.value('af_maximum_paths_ebgp') or \
                           attributes.value('maximum_paths_ebgp'):
                            configurations.append_line(
                                'maximum-paths ebgp {}'.format(
                                    self.af_maximum_paths_ebgp or
                                    self.maximum_paths_ebgp))

                        # iosxr: address-family ipv4 unicast/
                        # maximum-paths ibgp <af_maximum_paths_ibgp>
                        if attributes.value('af_maximum_paths_ibgp') or \
                           attributes.value('maximum_paths_ibgp'):
                            configurations.append_line(
                                'maximum-paths ibgp {}'.format(
                                    self.af_maximum_paths_ibgp or
                                    self.maximum_paths_ibgp))

                        # iosxr: address-family ipv4 unicast/
                        # maximum-paths eibgp <af_maximum_paths_eibgp>
                        if attributes.value('af_maximum_paths_eibgp'):
                            configurations.append_line(
                                attributes.format('maximum-paths eibgp '
                                    '{af_maximum_paths_eibgp}'))

                        # iosxr: address-family ipv4 unicast/
                        # aggregate-address <af_aggregate_address_ipv4_address>
                        # /<af_aggregate_address_ipv4_mask>
                        # [as-set] | summary-only
                        v = attributes.value(
                            'af_aggregate_address_ipv4_address')
                        k = attributes.value('af_aggregate_address_ipv4_mask')
                        if v and k:
                            line = 'aggregate-address '\
                                   '{af_aggregate_address_ipv4_address}/'\
                                   '{af_aggregate_address_ipv4_mask}'
                            if attributes.value('af_aggregate_address_as_set'):
                                line += ' as-set'
                            elif attributes.value(
                                'af_aggregate_address_summary_only'):
                                line += ' summary-only'
                            configurations.append_line(attributes.format(line))

                        # iosxr: address-family ipv4 unicast/
                        # network <af_network_number>/<af_network_mask>
                        # [route-policy <af_network_route_map>]
                        if attributes.value('af_network_number') and \
                           attributes.value('af_network_mask'):
                            line = 'network {af_network_number}/'\
                                   '{af_network_mask}'
                            if attributes.value('af_network_route_map'):
                                line += ' route-policy {af_network_route_map}'
                            configurations.append_line(attributes.format(line))

                        if attributes.value('redistributes'):
                            # iosxr: router bgp 100 [instance someword] / 
                            # address-family ipv4|ipv6 unicast / 
                            # redistribute isis|ospf someword | rip
                            # [metric <0-4294967295>] [route-policy <rtepol>]
                            for redistribute, redistribute_attributes in \
                                attributes.sequence_values('redistributes'):
                                assert redistribute_attributes.iswildcard
                                cfg = 'redistribute'
                                if isinstance(redistribute.protocol, str):
                                    # connected, subscriber
                                    cfg += redistribute_attributes.format(
                                        ' {protocol}')
                                elif isinstance(redistribute.protocol, Ospf):
                                    cfg += redistribute_attributes.format(
                                        ' ospf {protocol.pid}')
                                elif isinstance(redistribute.protocol, Isis):
                                    cfg += redistribute_attributes.format(
                                        ' isis {protocol.pid}')
                                elif isinstance(redistribute.protocol, Rip):
                                    cfg += redistribute_attributes.format(' rip')
                                else:
                                    raise ValueError(redistribute.protocol)
                                cfg += redistribute_attributes.format(
                                    ' metric {metric}')
                                cfg += redistribute_attributes.format(
                                    ' route-policy {route_policy.name}')
                                configurations.append_line(cfg)
                        else:
                            # iosxr: address-family ipv4 unicast/
                            # redistribute isis <af_redist_isis>
                            # metric <af_redist_isis_metric> |
                            # route-policy <af_redist_isis_route_policy>
                            if attributes.value('af_redist_isis') and \
                               self.vrf_name == 'default':
                                line = 'redistribute isis '\
                                       '{af_redist_isis}'
                                if attributes.value('af_redist_isis_metric'):
                                    line += ' metric {af_redist_isis_metric}'
                                elif attributes.value(
                                    'af_redist_isis_route_policy'):
                                    line += ' route-policy '\
                                            '{af_redist_isis_route_policy}'
                                configurations.append_line(attributes.format(line))


                            # iosxr: address-family ipv4 unicast/
                            # redistribute ospf <af_redist_ospf>
                            # metric <af_redist_ospf_metric> |
                            # route-policy <af_redist_ospf_route_policy>
                            if attributes.value('af_redist_ospf'):
                                line = 'redistribute ospf '\
                                       '{af_redist_ospf}'
                                if attributes.value('af_redist_ospf_metric'):
                                    line += ' metric {af_redist_ospf_metric}'
                                elif attributes.value(
                                    'af_redist_ospf_route_policy'):
                                    line += ' route-policy '\
                                            '{af_redist_ospf_route_policy}'
                                configurations.append_line(attributes.format(line))

                            # iosxr: address-family ipv4 unicast/
                            # redistribute rip
                            # metric <af_redist_rip_metric> |
                            # route-policy <af_redist_rip_route_policy>
                            if attributes.value('af_redist_rip'):
                                line = 'redistribute rip'
                                if attributes.value('af_redist_rip_metric'):
                                    line += ' metric {af_redist_rip_metric}'
                                elif attributes.value(
                                    'af_redist_rip_route_policy'):
                                    line += ' route-policy '\
                                            '{af_redist_rip_route_policy}'
                                configurations.append_line(attributes.format(line))

                        # iosxr: address-family ipv4 unicast/
                        # redistribute static
                        # metric <af_redist_static_metric> |
                        # route-policy <af_redist_static_route_policy>
                        if attributes.value('af_redist_static'):
                            line = 'redistribute static'
                            if attributes.value('af_redist_static_metric'):
                                line += ' metric {af_redist_static_metric}'
                            elif attributes.value(
                                'af_redist_static_route_policy'):
                                line += ' route-policy '\
                                        '{af_redist_static_route_policy}'
                            configurations.append_line(attributes.format(line))

                        # iosxr: address-family ipv4 unicast/
                        # redistribute connected
                        # metric <af_redist_connected_metric> |
                        # route-policy <af_redist_static_route_policy>
                        if attributes.value('af_redist_connected'):
                            line = 'redistribute connected'
                            if attributes.value('af_redist_connected_metric'):
                                line += ' metric {af_redist_connected_metric}'
                            elif attributes.value(
                                'af_redist_connected_route_policy'):
                                line += ' route-policy '\
                                        '{af_redist_connected_route_policy}'
                            configurations.append_line(attributes.format(line))

                        # iosxr: address-family ipv6 unicast/
                        # aggregate-address <af_v6_aggregate_address_ipv6_address>
                        # [as-set] | summary-only
                        if attributes.value(
                            'af_v6_aggregate_address_ipv6_address'):
                            line = 'aggregate-address '\
                                   '{af_v6_aggregate_address_ipv6_address}'
                            if attributes.value(
                                'af_v6_aggregate_address_as_set'):
                                line += ' as-set'
                            elif attributes.value(
                                'af_v6_aggregate_address_summary_only'):
                                line += ' summary-only'
                            configurations.append_line(attributes.format(line))

                        # iosxr: address-family ipv6 unicast/
                        # network <af_v6_network_number>  [route-policy 
                        # <af_v6_network_route_map> ] +
                        if attributes.value('af_v6_network_number'):
                            if attributes.value('af_v6_network_route_map'):
                                configurations.append_line(attributes.format(
                                    'network {af_v6_network_number} '
                                    'route-policy {af_v6_network_route_map}'))
                            else:
                                configurations.append_line(attributes.format(
                                'network {af_v6_network_number}'))

                        # iosxr: address-family ipv4 unicast/
                        # allocate-label all
                        if attributes.value('af_v6_allocate_label_all'):
                            configurations.append_line(attributes.format(
                                'allocate-label all'))
                        else:
                            if isinstance(self.allocate_label, RoutePolicy):
                            # iosxr: router bgp 100 [instance someword] /
                            # [vrf someword] / address-family ipv4|ipv6 unicast /
                            # allocate-label all |
                            # allocate-label route-policy <rtepol>
                                configurations.append_line(attributes.format(
                                    'allocate-label route-policy '
                                    '{allocate_label.name}'))
                            else:
                                configurations.append_line(attributes.format(
                                    'allocate-label {allocate_label}'))

                        # iosxr: address-family vpnv4 unicast/
                        # retain route-target all | 
                        # retain route-target route-policy <rtepol>
                        if attributes.value('af_retain_rt_all') or \
                           attributes.value('retain_route_target'):
                            configurations.append_line(attributes.format(
                                'retain route-target all'))
                        else:
                            configurations.append_line(attributes.format(
                                'retain route-target route-policy '
                                '{retain_route_target}'))

                        # iosxr: address-family ipv4 unicast/
                        # label mode per-vrf
                        if attributes.value('af_label_allocation_mode') or \
                           attributes.value('label_mode'):
                            configurations.append_line(attributes.format(
                                'label mode per-vrf'))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply,
                                             attributes=attributes,
                                             unconfig=True, **kwargs)

            class NeighborAttributes(ABC):

                def build_config(self, apply=True, attributes=None,
                                 unconfig=False, **kwargs):
                    assert not apply
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    # iosxr: router bgp 100 [instance someword] /
                    # [vrf someword] / neighbor <ipv4|ipv6> (config-bgp-vrf-nbr)
                    with configurations.submode_context(attributes.format(
                        'neighbor {neighbor}', force=True)):
                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # iosxr: router bgp 100 [instance someword] /
                        # [vrf someword] / neighbor <ipv4|ipv6> /
                        # graceful-restart   |
                        # iosxr: router bgp 100 [instance someword] /
                        # [vrf someword] / neighbor <ipv4|ipv6> /
                        #  graceful-restart disable
                        v = attributes.value('graceful_restart',
                                             inherited=False)
                        if v is not None:
                            if v:
                                configurations.append_line(
                                    'graceful-restart')
                            else:
                                configurations.append_line(
                                    'graceful-restart disable')

                        # handle key nbr_fall_over_bfd
                        # iosxr: router bgp 100 [instance someword] /
                        # [vrf someword] / neighbor <ipv4|ipv6> 
                        # bfd fast-detect
                        if attributes.value('nbr_fall_over_bfd'):
                            configurations.append_line('bfd fast-detect')
                        elif attributes.value('bfd_fast_detect'):
                            v = attributes.value('bfd_fast_detect')
                            if v:
                                if v is True:
                                    configurations.append_line(
                                        'bfd fast-detect')
                                else:
                                    configurations.append_line(
                                        'bfd fast-detect {}'.format(v))

                        elif attributes.value('nbr_fall_over_bfd') is False or \
                             attributes.value('bfd_fast_detect') is False:
                            configurations.append_line(
                                'bfd fast-detect disable')

                        # iosxr: router bgp 100 [instance someword] /
                        # [vrf someword] / neighbor <ipv4|ipv6> /
                        # bfd minimum-interval 3
                        configurations.append_line(attributes.format(
                            'bfd minimum-interval {bfd_minimum_interval}',
                            inherited=False))

                        # iosxr: router bgp 100 [instance someword] /
                        # [vrf someword] /
                        # neighbor <ipv4|ipv6> / bfd multiplier 2
                        configurations.append_line(attributes.format(
                            'bfd multiplier {bfd_multiplier}', inherited=False))

                        # iosxr: router bgp 100 [instance someword] / [vrf someword] / neighbor <ipv4|ipv6> / remote-as 1
                        # iosxr: router bgp 100 [instance someword] / [vrf someword] / neighbor <ipv4|ipv6> / remote-as 100.200
                        # iosxr: router bgp 100 [instance someword] / [vrf someword] / neighbor <ipv4|ipv6> / remote-as 65536
                        if not self.bgp_id:
                            configurations.append_line(attributes.format(
                                'remote-as {asn}'))

                        # handle key nbr_remote_as
                        # iosxr: neighbor <neighbor_id> / remote-as
                        # <nbr_remote_as>
                        if attributes.value('nbr_remote_as'):
                            configurations.append_line(
                                attributes.format('remote-as {nbr_remote_as}'))

                        # iosxr: router bgp 100 [instance someword] /
                        # [vrf someword] / neighbor <ipv4|ipv6> /
                        # update-source Bundle-Ether1                        
                        if attributes.value('update_source') or \
                           attributes.value('nbr_update_source'):

                            if hasattr(attributes.value('update_source'), 'name'):
                                val = attributes.value('update_source').name
                            else:
                                val = self.nbr_update_source
                            configurations.append_line(
                                'update-source {}'.format(val))

                        # iosxr: neighbor <neighbor_id> \
                        # capability suppress 4-byte-as
                        if attributes.value(
                            'nbr_suppress_four_byte_as_capability'):
                            configurations.append_line(
                                attributes.format(
                                    'capability suppress 4-byte-as'))

                        # iosxr: neighbor <neighbor_id> \
                        # description <nbr_description>
                        if attributes.value(
                            'nbr_description'):
                            configurations.append_line(
                                attributes.format(
                                    'description {nbr_description}'))

                        # iosxr: neighbor <neighbor_id> \
                        # ignore-connected-check
                        if attributes.value(
                            'nbr_disable_connected_check'):
                            configurations.append_line(
                                attributes.format(
                                    'ignore-connected-check'))

                        # iosxr: neighbor <neighbor_id> \
                        # ebgp-multihop <nbr_ebgp_multihop_max_hop>
                        # [ <nbr_ebgp_multihop_max_hop> ]
                        if attributes.value('nbr_ebgp_multihop'):
                            if attributes.value('nbr_ebgp_multihop_max_hop'):
                                configurations.append_line(
                                    attributes.format(
                                        'ebgp-multihop '
                                        '{nbr_ebgp_multihop_max_hop}'))
                            else:
                                configurations.append_line(
                                        'ebgp-multihop')
                        elif attributes.value('ebgp_multihop_max_hop_count') \
                                is not None \
                                or attributes.value('ebgp_multihop_mpls'):
                            cfg = 'ebgp-multihop'
                            cfg += attributes.format(
                                ' {ebgp_multihop_max_hop_count}')
                            if attributes.value('ebgp_multihop_mpls') is True:
                                cfg += ' mpls'
                            configurations.append_line(cfg)

                        # iosxr: neighbor <neighbor_id> \ inherit peer-session
                        # <nbr_inherit_peer_session>
                        if attributes.value(
                            'nbr_inherit_peer_session'):
                            configurations.append_line(
                                attributes.format(
                                    'use session-group '
                                    '{nbr_inherit_peer_session}'))

                        # iosxr: neighbor <neighbor_id> \
                        # local-as 111 [no-prepend replace-as dual-as]
                        if attributes.value('nbr_local_as_as_no'):
                            base_s = 'local-as {nbr_local_as_as_no}'
                            if attributes.value('nbr_local_as_no_prepend'):
                                base_s += ' no-prepend'
                            if attributes.value('nbr_local_as_replace_as'):
                                base_s += ' replace-as'
                            if attributes.value('nbr_local_as_dual_as'):
                                base_s += ' dual-as'
                            configurations.append_line(
                                attributes.format(base_s))

                        # iosxr: neighbor <neighbor_id> / 
                        # address-family <nbr_remove_private_as_af_name>
                        # remove-private-as
                        if attributes.value('nbr_remove_private_as') and \
                           attributes.value('nbr_remove_private_as_af_name'):
                            configurations.append_line(
                                attributes.format(
                                    'address-family '
                                    '{nbr_remove_private_as_af_name.value} '
                                    'remove-private-AS'))

                        # iosxr: neighbor <neighbor_id> / shutdown
                        if attributes.value('nbr_shutdown'):
                            configurations.append_line(
                                attributes.format('shutdown'))

                        # iosxr: neighbor <neighbor_id> / timers
                        # <nbr_keepalive_interval>  <nbr_holdtime>
                        if attributes.value('nbr_keepalive_interval') and \
                            attributes.value('nbr_holdtime'):
                            configurations.append_line(
                                attributes.format('timers '
                                    '{nbr_keepalive_interval} {nbr_holdtime}'))

                        # iosxr: neighbor <neighbor_id> / password
                        # <nbr_password_text>
                        if attributes.value('nbr_password_text'):
                            configurations.append_line(attributes.format(
                                'password {nbr_password_text}'))

                        # iosxr: neighbor <neighbor_id> \
                        # transport connection-mode
                        # {nbr_transport_connection_mode}
                        if attributes.value('nbr_transport_connection_mode'):
                            configurations.append_line(attributes.format(
                                'session-open-mode '
                                '{nbr_transport_connection_mode.value}'))

                        # iosxr: router bgp 100 [instance someword] /
                        # [vrf someword] / neighbor <ipv4|ipv6> /
                        # address-family ... (config-bgp-vrf-nbr-af)
                        for sub, attributes2 in attributes.mapping_values(
                            'address_family_attr', sort=True):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig))


                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply,
                                             attributes=attributes,
                                             unconfig=True, **kwargs)

                class AddressFamilyAttributes(ABC):

                    def build_config(self, apply=True, attributes=None,
                                     unconfig=False, **kwargs):
                        assert not apply
                        assert not kwargs, kwargs
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        # iosxr: router bgp 100 [instance someword] /
                        # [vrf someword] / neighbor <ipv4|ipv6> /
                        # address-family ... (config-bgp-vrf-nbr-af)
                        with configurations.submode_context(
                            attributes.format(
                                'address-family {address_family.value}',
                                force=True)):
                            if unconfig and attributes.iswildcard:
                                configurations.submode_unconfig()

                            # iosxr: router bgp 100 / [instance someword] / vrf someword / neighbor <ipv4|ipv6> / address-family l2vpn evpn / encapsulation-type mpls
                            # iosxr: router bgp 100 / [instance someword] / vrf someword / neighbor <ipv4|ipv6> / address-family l2vpn evpn / encapsulation-type vxlan
                            # iosxr: router bgp 100 / [instance someword] / vrf someword / neighbor <ipv4|ipv6> / address-family vpnv4|vpnv6 unicast / encapsulation-type mpls
                            # iosxr: router bgp 100 / [instance someword] / vrf someword / neighbor <ipv4|ipv6> / address-family vpnv4|vpnv6 unicast / encapsulation-type vxlan
                            v = attributes.value('encapsulation_type')
                            if v is not None:
                                cfg = 'encapsulation-type {}'.format(v)
                                if self.address_family in [
                                        AddressFamily.l2vpn_evpn,
                                        AddressFamily.vpnv4_unicast,
                                        AddressFamily.vpnv6_unicast,
                                ]:
                                    configurations.append_line(cfg)
                                elif not self.isinherited('encapsulation_type'):
                                    warnings.warn('{} {}'.\
                                        format(self.address_family, cfg),\
                                        UnsupportedAttributeWarning)

                            # iosxr: router bgp 100 [instance someword] /
                            # vrf someword / neighbor <ipv4|ipv6> /
                            # address-family vpnv4|vpnv6 unicast /
                            # import [stitching-rt]
                            # [re-originate [stitching-rt]]
                            if attributes.value('import_stitching_rt') \
                                    or attributes.value('import_stitching_rt_re_originate') \
                                    or attributes.value('import_re_originate') \
                                    or attributes.value('import_re_originate_stitching_rt'):
                                cfg = 'import'
                                if attributes.value('import_stitching_rt', force=True) \
                                        or attributes.value('import_stitching_rt_re_originate', force=True):
                                    cfg += ' stitching-rt'
                                    if attributes.value('import_stitching_rt_re_originate', force=True):
                                        cfg += ' re-originate'
                                if attributes.value('import_re_originate', force=True) \
                                        or attributes.value('import_re_originate_stitching_rt', force=True):
                                    cfg += ' re-originate'
                                    if attributes.value('import_re_originate_stitching_rt', force=True):
                                        cfg += ' stitching-rt'
                                if self.address_family in [
                                        AddressFamily.l2vpn_evpn,
                                        AddressFamily.vpnv4_unicast,
                                        AddressFamily.vpnv6_unicast,
                                ]:
                                    configurations.append_line(cfg)
                                elif not (
                                    self.isinherited('import_stitching_rt')
                                    and self.isinherited('import_re_originate')
                                    and self.isinherited(
                                        'import_re_originate_stitching_rt')):
                                    warnings.warn('{} {}'.\
                                        format(self.address_family, cfg),\
                                        UnsupportedAttributeWarning)

                            # iosxr: router bgp 100 [instance someword] /
                            # vrf someword / neighbor <ipv4|ipv6> /
                            # address-family l2vpn evpn /
                            # advertise l2vpn evpn re-originated |
                            # re-originated regular-rt |
                            # re-originated stitching-rt
                            v = attributes.value(
                                'advertise_l2vpn_evpn_re_originated')
                            if v:
                                if v is True:
                                    cfg = 'advertise l2vpn evpn re-originated'
                                else:
                                    cfg = 'advertise l2vpn evpn re-originated {}'.format(v)
                                if self.address_family in [
                                        AddressFamily.l2vpn_evpn,
                                ]:
                                    configurations.append_line(cfg)
                                elif not self.isinherited(
                                    'advertise_l2vpn_evpn_re_originated'):
                                    warnings.warn('{} {}'.\
                                        format(self.address_family, cfg),\
                                        UnsupportedAttributeWarning)

                            # iosxr: router bgp 100 [instance someword] / vrf someword /
                            # neighbor <ipv4|ipv6> / address-family l2vpn evpn | vpnv4 unicast /
                            # advertise vpnv4 unicast
                            if attributes.value('advertise_vpnv4_unicast'):
                                cfg = 'advertise vpnv4 unicast'
                                # TODO
                                configurations.append_line(cfg)

                            # iosxr: address-family <nbr_af_name> \ allowas-in
                            # [ <allowas-in-cnt> ]
                            if attributes.value('nbr_af_allowas_in'):
                                if attributes.value(
                                    'nbr_af_allowas_in_as_number'):
                                    configurations.append_line(
                                        attributes.format('allowas-in '
                                            '{nbr_af_allowas_in_as_number}'))
                                else:
                                    configurations.append_line(
                                        attributes.format('allowas-in'))

                            # iosxr: address-family <nbr_af_name> \
                            # inherit peer-policy <nbr_af_inherit_peer_policy>
                            # <nbr_af_inherit_peer_seq>
                            if attributes.value('nbr_af_inherit_peer_policy'):
                                configurations.append_line(
                                    attributes.format('use af-group '
                                        '{nbr_af_inherit_peer_policy}'))

                            # iosxr: address-family <nbr_af_name> \
                            # maximum-prefix
                            # <nbr_af_maximum_prefix_max_prefix_no>
                            # [<nbr_af_maximum_prefix_threshold>] restart
                            # [restart <nbr_af_maximum_prefix_restart> |
                            # warning-only ]
                            if attributes.value(
                                'nbr_af_maximum_prefix_max_prefix_no'):
                                line = 'maximum-prefix '\
                                       '{nbr_af_maximum_prefix_max_prefix_no}'
                                if attributes.value(
                                    'nbr_af_maximum_prefix_threshold'):
                                    line += ' {nbr_af_maximum_prefix_threshold}'
                                if attributes.value(
                                    'nbr_af_maximum_prefix_restart'):
                                    line += ' restart '\
                                            '{nbr_af_maximum_prefix_restart}'
                                elif attributes.value(
                                    'nbr_af_maximum_prefix_warning_only'):
                                    line += ' warning-only'
                                configurations.append_line(
                                    attributes.format(line))

                            # iosxr: address-family <nbr_af_name> \
                            # route-policy <nbr_af_route_map_name_in> in
                            if attributes.value('nbr_af_route_map_name_in'):
                                configurations.append_line(
                                    attributes.format('route-policy '
                                        '{nbr_af_route_map_name_in} in'))
                            elif hasattr(self.route_policy_in, 'name'):
                                configurations.append_line(
                                    attributes.format('route-policy '
                                        '{route_policy_in.name} in'))

                            # iosxr: address-family <nbr_af_name> \
                            # route-policy <nbr_af_route_map_name_out> out
                            if attributes.value('nbr_af_route_map_name_out'):
                                configurations.append_line(
                                    attributes.format('route-policy \
                                        {nbr_af_route_map_name_out} out'))
                            elif hasattr(self.route_policy_out, 'name'):
                                configurations.append_line(
                                    attributes.format('route-policy '
                                        '{route_policy_out.name} in'))

                            # iosxr: address-family <nbr_af_name> \
                            # route-reflector-client
                            if attributes.value(
                                'nbr_af_route_reflector_client') or \
                               attributes.value('route_reflector_client'):
                                configurations.append_line(
                                    attributes.format(
                                        'route-reflector-client'))
                            elif attributes.value(
                                'route_reflector_client_inheritance_disable',
                                force=True):
                                configurations.append_line(
                                    attributes.format(
                                        'route-reflector-client '
                                        'inheritance-disable'))

                            # iosxr: address-family <nbr_af_name> \
                            # send-community-ebgp
                            nbr_v1 = attributes.value('nbr_af_send_community')
                            if nbr_v1:
                                if nbr_v1.value == 'standard':
                                    configurations.append_line(
                                        attributes.format(
                                        'send-community-ebgp'))

                                # iosxr: address-family <nbr_af_name> \
                                # send-extended-community-ebgp
                                if nbr_v1.value == 'extended':
                                    configurations.append_line(
                                        attributes.format(
                                        'send-extended-community-ebgp'))

                                # iosxr: address-family <nbr_af_name> \
                                # send-community-ebgp
                                # send-extended-community-ebgp
                                if nbr_v1.value == 'both':
                                    configurations.append_line(
                                        attributes.format(
                                        'send-community-ebgp'))
                                    configurations.append_line(
                                        attributes.format(
                                        'send-extended-community-ebgp'))
                            elif attributes.value('send_community_ebgp'):
                                configurations.append_line(
                                    attributes.format(
                                    'send-community-ebgp'))
                            elif attributes.value('send_extended_community_ebgp'):
                                configurations.append_line(
                                    attributes.format(
                                    'send-extended-community-ebgp'))
                            elif attributes.value(
                                'send_extended_community_ebgp_inheritance_disable',
                                force=True):
                                configurations.append_line(
                                    attributes.format(
                                    'send-extended-community-ebgp '
                                    'inheritance-disable'))


                            # iosxr: address-family <nbr_af_name> \
                            # soft-reconfiguration inbound
                            if attributes.value('nbr_af_soft_reconfiguration'):
                                configurations.append_line(
                                    attributes.format('soft-reconfiguration '
                                        'inbound'))

                            # iosxr: address-family <nbr_af_name> \
                            # next-hop-self
                            if attributes.value('nbr_af_next_hop_self') or \
                               attributes.value('nexthop_self'):
                                configurations.append_line(
                                    attributes.format('next-hop-self'))
                            elif attributes.value(
                                'nexthop_self_inheritance_disable'):
                                configurations.append_line(
                                    attributes.format('next-hop-self '
                                        'inheritance-disable'))

                            # iosxr: address-family <nbr_af_name> \
                            # as-override
                            if attributes.value('nbr_af_as_override') or \
                               attributes.value('as_override'):

                                configurations.append_line(
                                    attributes.format('as-override'))

                                if attributes.value(
                                  'as_override_inheritance', force=True) is False:                               
                                    configurations.append_line(
                                        attributes.format(
                                            'as-override inheritance-disable'))

                            # iosxr: address-family <nbr_af_name> \
                            # default-originate
                            # iosxr: address-family <nbr_af_name> \
                            # default-originate route-policy test
                            if attributes.value('nbr_af_default_originate'):
                                if attributes.value(
                                    'nbr_af_default_originate_route_map'):
                                    configurations.append_line(
                                        attributes.format('default-originate '
                                    'route-policy '
                                    '{nbr_af_default_originate_route_map}'))
                                else:
                                    configurations.append_line(
                                        attributes.format('default-originate'))

                            # iosxr: address-family <nbr_af_name> \
                            # site-of-origin 100:100
                            if attributes.value('nbr_af_soo') and \
                               self.vrf_id != 'default':
                                configurations.append_line(
                                    attributes.format(
                                        'site-of-origin {nbr_af_soo}'))

                            # signalling ldp disable
                            if attributes.value('nbr_af_suppress_signaling_protocol_ldp'):
                                configurations.append_line(
                                    attributes.format('signalling ldp disable'))

                        return str(configurations)

                    def build_unconfig(self, apply=True,
                                       attributes=None, **kwargs):
                        return self.build_config(apply=apply,
                                                 attributes=attributes,
                                                 unconfig=True, **kwargs)

