
# import python
from abc import ABC
from netaddr import IPNetwork

# import genie
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig
from genie.libs.conf.ospf import Ospf
from genie.libs.conf.isis import Isis
from genie.libs.conf.rip import Rip


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

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # nxos: feature bgp
            if attributes.value('enabled'):
                if unconfig is False:
                    configurations.append_line(
                        attributes.format('feature bgp'))

                # Make sure that only enabled was provided in attributes
                # If wildcard,  then delete everything
                elif unconfig is True and\
                     attributes.attributes == {'enabled': {True: None}} or \
                        attributes.iswildcard:
                    configurations.append_line('no feature bgp', raw=True)
                    if apply:
                        if configurations:
                            self.device.configure(configurations)
                    else:
                        return CliConfig(device=self.device, unconfig=unconfig,
                                         cli_config=configurations)

            # nxos: router bgp 100
            with configurations.submode_context(attributes.format(
                'router bgp {bgp_id}', force=True)):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                # nxos: router bgp 100 / shutdown
                if attributes.value('protocol_shutdown'):
                    configurations.append_line(
                        attributes.format('shutdown'))

                for sub, attributes2 in attributes.mapping_values('vrf_attr',
                    sort=True, keys=self.vrf_attr):configurations.append_block(
                        sub.build_config(apply=False,
                                         attributes=attributes2,
                                         unconfig=unconfig))

                for sub, attributes2 in attributes.mapping_values(
                    'peer_session_attr', keys=self.peer_session_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig,
                                             **kwargs))

                for sub, attributes2 in attributes.mapping_values(
                    'peer_policy_attr', keys=self.peer_policy_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig,
                                             **kwargs))

            if apply:
                if configurations:
                    self.device.configure(configurations)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes,
                                     unconfig=True, **kwargs)

        class PeerPolicyAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)
                with configurations.submode_context(
                    attributes.format('template peer-policy {pp_name}',
                                      force=True)):
                    if unconfig and attributes.iswildcard:
                        # Never reached!
                        configurations.submode_unconfig()

                    # nxos: template peer-policy <pp_name> \
                    # allowas-in [9]
                    if attributes.value('pp_allowas_in'):
                        if attributes.value('pp_allowas_in_as_number'):
                            configurations.append_line(
                                attributes.format('allowas-in '
                                                  '{pp_allowas_in_as_number}'))
                        else:
                            configurations.append_line(
                                attributes.format('allowas-in'))

                    # nxos: template peer-policy <pp_name>\
                    # as-override
                    if attributes.value('pp_as_override'):
                        configurations.append_line(
                            attributes.format('as-override'))

                    # nxos: template peer-policy <pp_name> \
                    # send-community
                    if attributes.value('pp_send_community'):
                        if attributes.value('pp_send_community').value ==\
                          'standard':
                            configurations.append_line(attributes.format(
                                'send-community'))

                        # nxos: template peer-policy <pp_name> \
                        # send-community extended
                        if attributes.value('pp_send_community').value == \
                            'extended':
                            configurations.append_line(attributes.format(
                                'send-community extended'))

                        # nxos: template peer-policy <pp_name>\
                        # send-communitys
                        # nxos: template peer-policy <pp_name> \
                        # send-community extended
                        if attributes.value('pp_send_community').value == \
                            'both':
                            configurations.append_line(attributes.format(
                                'send-community'))
                            configurations.append_line(attributes.format(
                                'send-community extended'))

                    # nxos: template peer-policy <pp_name> \
                    # route-reflector-client
                    if attributes.value('pp_route_reflector_client'):
                        configurations.append_line(
                            attributes.format(
                                'route-reflector-client'))

                    # nxos: template peer-policy <pp_name> \
                    # next-hop-self
                    if attributes.value('pp_next_hop_self'):
                        configurations.append_line(
                            attributes.format(
                                'next-hop-self'))

                    # nxos: template peer-policy <pp_name> \
                    # route-map test-map in
                    if attributes.value('pp_route_map_name_in'):
                        configurations.append_line(
                            attributes.format('route-map '
                                '{pp_route_map_name_in} in'))

                    # nxos: template peer-policy <pp_name> \
                    # route-map test-map out
                    if attributes.value('pp_route_map_name_out'):
                        configurations.append_line(
                            attributes.format('route-map '
                                '{pp_route_map_name_out} out'))

                    # nxos: template peer-policy <pp_name> \
                    # mmaximum-prefix <pp_maximum_prefix_max_prefix_no> 
                    # [<pp_maximum_prefix_threshold> ]
                    # [restart <pp_maximum_prefix_restart> | warning-only ]
                    if attributes.value('pp_maximum_prefix_max_prefix_no'):
                        if attributes.value('pp_maximum_prefix_threshold'):
                            if attributes.value('pp_maximum_prefix_restart'):
                                configurations.append_line(
                                    attributes.format('maximum-prefix '
                                    '{pp_maximum_prefix_max_prefix_no} '
                                    '{pp_maximum_prefix_threshold} '
                                    'restart {pp_maximum_prefix_restart}'))
                            if attributes.value(
                                'pp_maximum_prefix_warning_only'):
                                configurations.append_line(
                                    attributes.format('maximum-prefix '
                                    '{pp_maximum_prefix_max_prefix_no} '
                                    '{pp_maximum_prefix_threshold} '
                                    'warning-only'))
                        elif attributes.value('pp_maximum_prefix_restart'):
                            configurations.append_line(
                                attributes.format('maximum-prefix '
                                '{pp_maximum_prefix_max_prefix_no} '
                                'restart {pp_maximum_prefix_restart}'))
                        elif attributes.value(
                            'pp_maximum_prefix_warning_only'):
                            configurations.append_line(
                                attributes.format('maximum-prefix '
                                '{pp_maximum_prefix_max_prefix_no} '
                                'warning-only'))
                        else:
                            configurations.append_line(attributes.format(
                                'maximum-prefix '
                                '{pp_maximum_prefix_max_prefix_no}'))

                    # nxos: template peer-policy <pp_name> \
                    # default-originate
                    # nxos: template peer-policy <pp_name> \
                    # default-originate route-map test
                    if attributes.value('pp_default_originate'):
                        if attributes.value(
                            'pp_default_originate_route_map'):
                            configurations.append_line(
                                attributes.format('default-originate '
                                'route-map '
                                '{pp_default_originate_route_map}'))
                        else:
                            configurations.append_line(
                                attributes.format('default-originate'))

                    # nxos: template peer-policy <pp_name> \
                    # soft-reconfiguration inbound
                    if attributes.value('pp_soft_reconfiguration'):
                        configurations.append_line(
                            attributes.format('soft-reconfiguration inbound'))

                    # nxos: template peer-policy <pp_name> \
                    # soo 100:100
                    if attributes.value('pp_soo'):
                        configurations.append_line(
                            attributes.format('soo {pp_soo}'))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

        class PeerSessionAttributes(ABC):

            def build_config(self, apply=True, attributes=None,
                              unconfig=False, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)
                with configurations.submode_context(
                    attributes.format(
                        'template peer-session {ps_name}',force=True)):
                    if unconfig and attributes.iswildcard:
                        # Never reached!
                        configurations.submode_unconfig()

                    # nxos: template peer-session <peer_session> \ bfd
                    if attributes.value('ps_fall_over_bfd'):
                        configurations.append_line(
                            attributes.format('bfd'))

                    # nxos: template peer-session <peer_session> \
                    # remote-as 500
                    if attributes.value('ps_remote_as'):
                        configurations.append_line(
                            attributes.format('remote-as {ps_remote_as}'))

                    # nxos: template peer-session <peer_session> \
                    # local-as 111
                    if attributes.value('ps_local_as_as_no'):
                        configurations.append_line(
                            attributes.format('local-as {ps_local_as_as_no}'))

                    # nxos: template peer-session <peer_session> \
                    # local-as 111 [no-prepend [replace-as [dual-as]]]
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

                    # nxos: template peer-session <peer_session> \
                    # description PEER-SESSION
                    if attributes.value('ps_description'):
                        configurations.append_line(
                            attributes.format('description {ps_description}'))

                    # nxos: template peer-session <peer_session> \
                    # password 3 386c0565965f89de
                    if attributes.value('ps_password_text'):
                        configurations.append_line(
                            attributes.format('password {ps_password_text}'))

                    # nxos: template peer-session <peer_session> \ shutdown
                    if attributes.value('ps_shutdown'):
                        configurations.append_line(
                            attributes.format('shutdown'))

                    # nxos: template peer-session <peer_session> \
                    # update-source loopback0
                    if attributes.value('ps_update_source'):
                        configurations.append_line(
                            attributes.format('update-source '
                                              '{ps_update_source}'))

                    # nxos: template peer-session <peer_session> \
                    # disable-connected-check
                    if attributes.value('ps_disable_connected_check'):
                        configurations.append_line(
                            attributes.format('disable-connected-check'))

                    # nxos: template peer-session <peer_session> \
                    # capability suppress 4-byte-as
                    if attributes.value(
                        'ps_suppress_four_byte_as_capability'):
                        configurations.append_line(attributes.format(
                            'capability suppress 4-byte-as'))

                    # nxos: template peer-session <peer_session> \
                    # ebgp-multihop 255
                    if attributes.value('ps_ebgp_multihop_max_hop'):
                        configurations.append_line(
                            attributes.format('ebgp-multihop '
                                '{ps_ebgp_multihop_max_hop}'))
                    elif attributes.value('ps_ebgp_multihop'):
                        configurations.append_line(
                            attributes.format('ebgp-multihop 255'))

                    # nxos: template peer-session <peer_session> \
                    # transport connection-mode passive
                    if attributes.value('ps_transport_connection_mode'):
                        if attributes.value(
                            'ps_transport_connection_mode').value ==\
                          'active':
                            configurations.append_line(attributes.format(
                                'no transport connection-mode passive'))

                        if attributes.value(
                            'ps_transport_connection_mode').value ==\
                          'passive':
                            configurations.append_line(attributes.format(
                                'transport connection-mode passive'))

                    # nxos: template peer-session <peer_session> \
                    # timers 111 222
                    if attributes.value('ps_keepalive_interval') and \
                        attributes.value('ps_hodltime'):
                        configurations.append_line(
                            attributes.format('timers '
                                '{ps_keepalive_interval} {ps_hodltime}'))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

        class VrfAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context(
                        None if self.vrf_name == 'default' else
                            attributes.format('vrf {vrf_name}', force=True)):
                    if self.vrf_name != 'default' and unconfig and \
                        attributes.iswildcard:
                        configurations.submode_unconfig()

                    # nxos: router bgp 100 / [instance someword] /
                    # [vrf someword] /bestpath { always-compare-med |
                    # med missing-as-worst | compare-routerid |
                    # cost-community ignore }
                    if attributes.value('always_compare_med'):
                        configurations.append_line(attributes.format(
                            'bestpath always-compare-med'))
                    if attributes.value('bestpath_compare_routerid'):
                        configurations.append_line(attributes.format(
                            'bestpath compare-routerid'))
                    if attributes.value('bestpath_cost_community_ignore'):
                        configurations.append_line(attributes.format(
                            'bestpath cost-community ignore'))
                    if attributes.value('bestpath_med_missing_at_worst'):
                        configurations.append_line(attributes.format(
                            'bestpath med missing-as-worst'))

                    # nxos: router bgp 100 / [instance someword] /
                    # [vrf someword] / cluster-id <cluster_id>
                    if attributes.value('cluster_id'):
                        configurations.append_line(attributes.format(
                            'cluster-id {cluster_id}'))

                    # nxos: router bgp 100 / [instance someword] /
                    # [vrf someword] / confederation identifier 
                    # <confederation_identifier>
                    if attributes.value('confederation_identifier'):
                        configurations.append_line(
                            attributes.format('confederation identifier '
                                '{confederation_identifier}'))

                    # nxos: router bgp 100 / [instance someword] /
                    # [vrf someword] / confederation peers 
                    # <confederation_peers_as>
                    if attributes.value('confederation_peers_as'):
                        configurations.append_line(
                            attributes.format('confederation peers '
                                '{confederation_peers_as}'))

                    # nxos: router bgp 100 / [vrf someword] / graceful-restart
                    if attributes.value('graceful_restart'):
                        configurations.append_line(
                            attributes.format('graceful-restart'))

                    # nxos: router bgp 100 / [vrf someword] /
                    # graceful-restart restart-time 240
                    if attributes.value('graceful_restart_restart_time'):
                        configurations.append_line(
                            attributes.format('graceful-restart restart-time '
                                '{graceful_restart_restart_time}'))

                    if attributes.value('maxas_limit'):
                        configurations.append_line(
                            attributes.format('maxas-limit {maxas_limit}'))

                    # nxos: router bgp 100 / [vrf someword] /
                    # graceful-restart stalepath-time 600
                    if attributes.value('graceful_restart_stalepath_time'):
                        configurations.append_line(
                            attributes.format('graceful-restart '
                                'stalepath-time '
                                '{graceful_restart_stalepath_time}'))

                    # nxos: router bgp 100 / [vrf someword] /
                    # log-neighbor-changes
                    if attributes.value('log_neighbor_changes'):
                        configurations.append_line(
                            attributes.format('log-neighbor-changes'))

                    # nxos: router bgp 100 / [vrf someword] / router-id 1.2.3.4
                    if attributes.value('router_id'):
                        configurations.append_line(attributes.format(
                            'router-id {router_id}'))

                    # nxos: router bgp 100 / [vrf someword] /
                    # timers bgp <keepalive-interval> <holdtime>
                    if attributes.value('keepalive_interval') and \
                        attributes.value('holdtime'):
                        configurations.append_line(
                            attributes.format('timers bgp '
                                '{keepalive_interval} {holdtime}'))

                    if attributes.value('prefix_peer_timeout'):
                        configurations.append_line(
                            attributes.format('timers prefix-peer-timeout '
                                              '{prefix_peer_timeout}'))

                    # nxos: router bgp 100 / [vrf someword] /
                    # enforce-first-as
                    if attributes.value('enforce_first_as'):
                        configurations.append_line(
                            attributes.format('enforce-first-as'))

                    # nxos: router bgp 100 / [vrf someword] / 
                    # fast-external-fallover
                    if attributes.value('fast_external_fallover'):
                        configurations.append_line(
                            attributes.format('fast-external-fallover'))

                   # nxos: router bgp 100 / [vrf someword] /
                   # dynamic-med-interval 78
                    if attributes.value('dynamic_med_interval'):
                        configurations.append_line(
                            attributes.format('dynamic-med-interval '
                                '{dynamic_med_interval}'))

                    # nxos: router bgp 100 / [vrf someword] /
                    # shutdown
                    if attributes.value('shutdown'):
                        configurations.append_line(
                            attributes.format('shutdown'))

                    # nxos: router bgp 100 / [vrf someword] /
                    # flush_routes
                    if attributes.value('flush_routes'):
                        configurations.append_line(
                            attributes.format('flush_routes'))

                    # nxos: router bgp 100 / [vrf someword] /
                    # isolate
                    if attributes.value('isolate'):
                        configurations.append_line(
                            attributes.format('isolate'))

                    # nxos: router bgp 100 / [vrf someword] /
                    # disable-policy-batching ipv4 prefix-list <WORD>
                    if attributes.value('disable_policy_batching_ipv4'):
                        configurations.append_line(
                            attributes.format('disable-policy-batching '
                                'ipv4 prefix-list '
                                '{disable_policy_batching_ipv4}'))

                    # nxos: router bgp 100 / [vrf someword] /
                    # disable-policy-batching ipv6 prefix-list <WORD>
                    if attributes.value('disable_policy_batching_ipv6'):
                        configurations.append_line(
                            attributes.format('disable-policy-batching '
                                'ipv6 prefix-list '
                                '{disable_policy_batching_ipv6}'))

                    for neighbor_sub, neighbor_attributes in \
                        attributes.mapping_values('neighbor_attr'):
                        configurations.append_block(
                            neighbor_sub.build_config(apply=False,
                                attributes=neighbor_attributes,
                                unconfig=unconfig))

                    for address_family_sub, address_family_attributes in \
                        attributes.mapping_values(
                            'address_family_attr', sort=True,
                            keys = self.address_family_attr):
                        configurations.append_block(
                            address_family_sub.build_config(apply=False,
                                attributes=address_family_attributes,
                                unconfig=unconfig))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

            class AddressFamilyAttributes(ABC):

                def build_config(self, apply=True, attributes=None,
                                 unconfig=False, **kwargs):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    with configurations.submode_context(
                        attributes.format('address-family '
                                          '{address_family.value}',
                                          force=True)):
                        if unconfig and attributes.iswildcard:
                            # Never reached!
                            configurations.submode_unconfig()

                        # nxos: address-family ipv4 unicast/
                        # redistribute <protocol> route-map <route_policy>
                        isis_route_policy_name = ''
                        ospf_route_policy_name = ''
                        rip_route_policy_name = ''
                        if attributes.value('af_redist_isis_route_policy'):
                            isis_route_policy_name = attributes.format(
                                'af_redist_isis_route_policy')
                        elif attributes.value('af_redist_ospf_route_policy'):
                            ospf_route_policy_name = attributes.format(
                                'af_redist_ospf_route_policy')
                        elif attributes.value('af_redist_rip_route_policy'):
                            rip_route_policy_name = attributes.format(
                                'af_redist_rip_route_policy')

                        # redistribute ospf <af_redist_ospf> route-map <route_policy>
                        if attributes.value('af_redist_ospf') and \
                           attributes.value('af_redist_ospf_route_policy'):
                            configurations.append_line(
                                attributes.format(
                                    'redistribute ospf {af_redist_ospf} route-map '
                                    '{af_redist_ospf_route_policy}'))

                        # redistribute rip <af_redist_rip> route-map <route_policy>
                        if attributes.value('af_redist_rip') and \
                           attributes.value('af_redist_rip_route_policy'):
                            configurations.append_line(
                                attributes.format(
                                    'redistribute rip {af_redist_rip} route-map '
                                    '{af_redist_rip_route_policy}'))

                        # redistribute isis <af_redist_isis> route-map <route_policy>
                        if attributes.value('af_redist_isis') and \
                           attributes.value('af_redist_ospf_route_policy'):
                            configurations.append_line(
                                attributes.format(
                                    'redistribute isis {af_redist_isis} route-map '
                                    '{af_redist_isis_route_policy}'))

                        for redistribute, redistribute_attributes in \
                            attributes.sequence_values('redistributes'):
                            assert redistribute_attributes.iswildcard
                            cfg = 'redistribute'
                            if isinstance(redistribute.protocol, Ospf) and\
                                ospf_route_policy_name:
                                cfg += redistribute_attributes.format(
                                    ' ospf {protocol.pid} '
                                    'route-map {ospf_route_policy_name}')
                            elif isinstance(redistribute.protocol, Isis) and\
                                isis_route_policy_name:
                                cfg += redistribute_attributes.format(
                                    ' isis {protocol.pid} '
                                    'route-map {isis_route_policy_name}')
                            elif isinstance(redistribute.protocol, Rip) and\
                                rip_route_policy_name:
                                cfg += redistribute_attributes.format(
                                    ' rip {protocol.pid} '
                                    'route-map {rip_route_policy_name}')
                            else:
                                raise ValueError(redistribute.protocol)
                            configurations.append_line(cfg)

                        # nxos: address-family ipv4 unicast/
                        # redistribute static route-map <route_policy>
                        if attributes.value('af_redist_static'):
                            configurations.append_line(
                                attributes.format(
                                    'redistribute static route-map '
                                    '{af_redist_static_route_policy}'))

                        # nxos: address-family ipv4 unicast/
                        # redistribute direct route-map <route_policy>
                        if attributes.value('af_redist_connected'):
                            configurations.append_line(
                                attributes.format(
                                    'redistribute direct route-map '
                                    '{af_redist_connected_route_policy}'))

                        if attributes.value('af_default_metric'):
                            configurations.append_line(
                                attributes.format(
                                    'default-metric '
                                    '{af_default_metric_value}'
                                )
                            )

                        if attributes.value('af_default_information_originate'):
                            configurations.append_line(
                                'default-information originate'
                            )
                        # nxos: address-family ipv4 unicast/
                        # dampening 25 1000 1500 255
                        if attributes.value('af_dampening'):
                            if attributes.value('af_dampening_half_life_time'):
                                if attributes.value('af_dampening_reuse_time'):
                                    if attributes.value(
                                        'af_dampening_suppress_time'):
                                        if attributes.value(
                                            'af_dampening_max_suppress_time'):
                                            configurations.append_line(
                                                attributes.format('dampening '
                                        '{af_dampening_half_life_time} '
                                        '{af_dampening_reuse_time} '
                                        '{af_dampening_suppress_time} '
                                        '{af_dampening_max_suppress_time}'))
                            # dampening
                            else:
                                configurations.append_line(
                                    'dampening')

                        # nxos: address-family ipv4 unicast/
                        # nexthop route-map <af_nexthop_route_map>
                        if attributes.value('af_nexthop_route_map'):
                            configurations.append_line(
                                attributes.format(
                                    'nexthop route-map '
                                    '{af_nexthop_route_map}'))

                        # nxos: address-family ipv4 unicast/
                        # nexthop trigger-delay critical
                        # <af_nexthop_trigger_delay_critical> non-critical
                        # <af_nexthop_trigger_delay_non_critical>
                        if attributes.value('af_nexthop_trigger_enable'):
                            if attributes.value(
                                'af_nexthop_trigger_delay_critical') and \
                                attributes.value(
                                    'af_nexthop_trigger_delay_non_critical') :
                                configurations.append_line(attributes.format(
                                    'nexthop trigger-delay critical '
                                    '{af_nexthop_trigger_delay_critical} '
                                    'non-critical '
                                    '{af_nexthop_trigger_delay_non_critical}'))

                        # nxos: address-family ipv4 unicast/
                        # client-to-client reflection
                        if attributes.value('af_client_to_client_reflection'):
                            configurations.append_line(
                                attributes.format(
                                    'client-to-client reflection'))

                        # nxos: address-family ipv4 unicast/
                        # distance <af_distance_extern_as> 
                        # <af_distance_internal_as> <af_distance_local>
                        if attributes.value('af_distance_extern_as'):
                            if attributes.value('af_distance_internal_as') and\
                                 attributes.value('af_distance_local') :
                                configurations.append_line(
                                    attributes.format(
                                        'distance {af_distance_extern_as} '
                                        '{af_distance_internal_as} '
                                        '{af_distance_local}'))

                        # nxos: address-family ipv4 unicast/ 
                        # maximum-paths <af_maximum_paths_ebgp>
                        if attributes.value('af_maximum_paths_ebgp'):
                            configurations.append_line(
                                attributes.format('maximum-paths '
                                    '{af_maximum_paths_ebgp}'))

                        # nxos: address-family ipv4 unicast/
                        # maximum-paths ibgp <af_maximum_paths_ibgp>
                        if attributes.value('af_maximum_paths_ibgp'):
                            configurations.append_line(
                                attributes.format('maximum-paths ibgp '
                                    '{af_maximum_paths_ibgp}'))

                        # nxos: address-family ipv4 unicast/
                        # maximum-paths eigp <af_maximum_paths_eibgp>
                        if attributes.value('af_maximum_paths_eibgp'):
                            configurations.append_line(
                                attributes.format('maximum-paths eibgp '
                                    '{af_maximum_paths_eibgp}'))

                        # nxos: address-family ipv4 unicast/
                        # aggregate-address <af_aggregate_address_ipv4_address>
                        # /<af_aggregate_address_ipv4_mask>
                        # [ as-set | summary-only ]
                        v = attributes.value(
                            'af_aggregate_address_ipv4_address')
                        k = attributes.value('af_aggregate_address_ipv4_mask')
                        if v and k:
                            base_s = 'aggregate-address '\
                                     '{af_aggregate_address_ipv4_address}/'\
                                     '{af_aggregate_address_ipv4_mask}'
                            if attributes.value(
                                'af_aggregate_address_as_set'):
                                base_s += ' as-set'
                            if attributes.value(
                                'af_aggregate_address_summary_only'):
                                base_s += ' summary-only'

                            configurations.append_line(
                                attributes.format(base_s))

                        # nxos: address-family ipv4 unicast/
                        # network <af_network_number> mask <af_network_mask>
                        if attributes.value('af_network_number') and \
                            attributes.value('af_network_mask'):

                            # Convert mask from /24 to 255.255.255.0 (example)
                            dummy = '{}/{}'.format('0.0.0.0',
                                            attributes.value('af_network_mask'))
                            mask = str(IPNetwork(dummy).netmask)

                            # Build cfg string
                            cfg_str = 'network {af_network_number} '
                            cfg_str += ' mask {}'.format(mask)

                            # Add configuration
                            configurations.append_line(attributes.format(cfg_str))

                        # nxos: address-family ipv4 unicast/ aggregate-address 
                        # <af_v6_aggregate_address_ipv6_address> 
                        if attributes.value(
                            'af_v6_aggregate_address_ipv6_address'):
                            configurations.append_line(
                                attributes.format('aggregate-address '
                                    '{af_v6_aggregate_address_ipv6_address}'))

                        # nxos: address-family ipv4 unicast/
                        # network <af_v6_network_number>  [route-map 
                        # <af_v6_network_route_map> ] +
                        if attributes.value('af_v6_network_number'):
                            if attributes.value('af_v6_network_route_map'):
                                configurations.append_line(attributes.format(
                                    'network {af_v6_network_number} '
                                    'route-map {af_v6_network_route_map}'))
                            else:
                                configurations.append_line(attributes.format(
                                'network {af_v6_network_number}'))

                        # nxos: address-family ipv4 unicast/
                        # af_v6_allocate_label_all
                        if attributes.value('af_v6_allocate_label_all'):
                            configurations.append_line(attributes.format(
                                'allocate-label all'))

                        # nxos: address-family ipv4 unicast/
                        # retain route-target all
                        if attributes.value('af_retain_rt_all'):
                            configurations.append_line(attributes.format(
                                'retain route-target all'))

                        # nxos: address-family ipv4 unicast/
                        # label-allocation-mode per-vrf |
                        # no label-allocation-mode [ per-vrf ]
                        if attributes.value('af_label_allocation_mode'):
                            configurations.append_line(attributes.format(
                                'label-allocation-mode per-vrf'))

                        # nxos: address-family <af>/
                        # advertise-pip | no advertise-pip ]
                        if attributes.value('af_advertise_pip'):
                            configurations.append_line(attributes.format(
                                'advertise-pip'))

                        if attributes.value('af_advertise_l2_evpn'):
                            configurations.append_line(attributes.format(
                                'advertise l2vpn evpn'))
                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None,
                                   **kwargs):
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

                    with configurations.submode_context(
                        attributes.format('neighbor {neighbor}',
                                          force=True)):
                        if unconfig and attributes.iswildcard:
                            # Never reached!
                            configurations.submode_unconfig()

                        # nxos: neighbor <neighbor_id> \ bfd
                        if attributes.value('nbr_fall_over_bfd') or \
                            attributes.value('bfd_fast_detect'):
                            configurations.append_line(
                                attributes.format('bfd'))

                        # nxos: neighbor <neighbor_id> \
                        # capability suppress 4-byte-as
                        if attributes.value(
                            'nbr_suppress_four_byte_as_capability'):
                            configurations.append_line(
                                attributes.format(
                                    'capability suppress 4-byte-as'))

                        # nxos: neighbor <neighbor_id> \
                        # description <nbr_description>
                        if attributes.value(
                            'nbr_description'):
                            configurations.append_line(
                                attributes.format(
                                    'description {nbr_description}'))

                        # nxos: neighbor <neighbor_id> \
                        # disable-connected-check
                        if attributes.value(
                            'nbr_disable_connected_check'):
                            configurations.append_line(
                                attributes.format(
                                    'disable-connected-check'))

                        # nxos: neighbor <neighbor_id> \
                        # ebgp-multihop <nbr_ebgp_multihop_max_hop>
                        # no ebgp-multihop [<nbr_ebgp_multihop_max_hop>]
                        if attributes.value('nbr_ebgp_multihop'):
                            if attributes.value('nbr_ebgp_multihop_max_hop'):
                                configurations.append_line(
                                    attributes.format('ebgp-multihop '
                                        '{nbr_ebgp_multihop_max_hop}'),
                                        unconfig_cmd='default ebgp-multihop')

                        # nxos: neighbor <neighbor_id> \
                        # ebgp-multihop <ebgp_multihop_max_hop_count>
                        if attributes.value(
                            'ebgp_multihop_max_hop_count'):
                            configurations.append_line(attributes.format(
                                    'ebgp-multihop '
                                    '{ebgp_multihop_max_hop_count}'))

                        # nxos: neighbor <neighbor_id> \ inherit peer-session
                        # <nbr_inherit_peer_session>
                        if attributes.value(
                            'nbr_inherit_peer_session'):
                            configurations.append_line(
                                attributes.format(
                                    'inherit peer-session '
                                    '{nbr_inherit_peer_session}'))

                        # nxos: neighbor <neighbor_id> \ local-as 
                        #<nbr_local_as_as_no>[no-prepend[replace-as[dual-as]]]}
                        if attributes.value('nbr_local_as_as_no'):
                            cfg = 'local-as {nbr_local_as_as_no}'
                            if attributes.value('nbr_local_as_no_prepend'):
                                cfg += ' no-prepend'
                            if attributes.value('nbr_local_as_replace_as'):
                                cfg += ' replace-as'
                                if attributes.value('nbr_local_as_dual_as'):
                                    cfg += ' dual-as'

                            configurations.append_line(
                                attributes.format(cfg))

                        if attributes.value('nbr_local_as_as_no'):
                            if attributes.value('nbr_local_as_no_prepend'):
                                if attributes.value('nbr_local_as_replace_as'):
                                    if attributes.value(
                                        'nbr_local_as_dual_as'):
                                        configurations.append_line(
                                            attributes.format('local-as '
                                            '{nbr_local_as_as_no} no-prepend '
                                            'replace-as dual-as'))
                            else:
                                configurations.append_line(
                                    attributes.format('local-as '
                                    '{nbr_local_as_as_no}'))

                        # nxos: neighbor <neighbor_id> / remote-as
                        # <nbr_remote_as>
                        if attributes.value('nbr_remote_as'):
                            configurations.append_line(
                                attributes.format('remote-as {nbr_remote_as}'))

                        # nxos: neighbor <neighbor_id> / remove-private-as
                        if attributes.value('nbr_remove_private_as'):
                            configurations.append_line(
                                attributes.format('remove-private-as'))

                        # nxos: neighbor <neighbor_id> / shutdown
                        if attributes.value('nbr_shutdown'):
                            configurations.append_line(
                                attributes.format('shutdown'))

                        # nxos: neighbor <neighbor_id> / timers
                        # <nbr_keepalive_interval>  <nbr_holdtime>
                        if attributes.value('nbr_keepalive_interval') and \
                            attributes.value('nbr_holdtime'):
                            configurations.append_line(
                                attributes.format('timers '
                                    '{nbr_keepalive_interval} {nbr_holdtime}'))

                        # nxos: neighbor <neighbor_id> / update-source
                        # <nbr_update_source>
                        if attributes.value('update_source') or \
                           attributes.value('nbr_update_source'):

                            if hasattr(attributes.value('update_source'),
                                'name'):
                                val = attributes.value('update_source').name
                            else:
                                val = self.nbr_update_source
                            configurations.append_line(
                                'update-source {}'.format(val))

                        # nxos: neighbor <neighbor_id> / password
                        # <nbr_password_text>
                        if attributes.value('nbr_password_text'):
                            configurations.append_line(attributes.format(
                                'password {nbr_password_text}'))

                        # nxos: neighbor <neighbor_id> \
                        # transport connection-mode
                        # {nbr_transport_connection_mode}
                        if attributes.value('nbr_transport_connection_mode'):
                            configurations.append_line(attributes.format(
                                'transport connection-mode '
                                '{nbr_transport_connection_mode.value}'))

                        # nxos: neighbor <neighbor_id> \
                        # peer-type {nbr_peer_type>}
                        if attributes.value('nbr_peer_type'):
                            configurations.append_line(attributes.format(
                                'peer-type {nbr_peer_type.value}'))

                        for address_family_sub, address_family_attributes in \
                            attributes.mapping_values(
                                'address_family_attr', sort=True):
                            configurations.append_block(
                                address_family_sub.build_config(apply=False,
                                    attributes=address_family_attributes,
                                    unconfig=unconfig))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None,
                                   **kwargs):
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

                        with configurations.submode_context(
                            attributes.format('address-family '
                                              '{address_family.value}',
                                              force=True)):
                            if unconfig and attributes.iswildcard:
                                # Never reached!
                                configurations.submode_unconfig()

                            # nxos: address-family <nbr_af_name> \ allowas-in
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

                            # nxos: address-family <nbr_af_name> \
                            # inherit peer-policy <nbr_af_inherit_peer_policy>
                            # <nbr_af_inherit_peer_seq>
                            if attributes.value(
                                'nbr_af_inherit_peer_policy') and \
                                attributes.value('nbr_af_inherit_peer_seq'):
                                configurations.append_line(
                                    attributes.format('inherit peer-policy '
                                        '{nbr_af_inherit_peer_policy} '
                                        '{nbr_af_inherit_peer_seq}'))

                            # nxos: address-family <nbr_af_name> \
                            # maximum-prefix
                            # <nbr_af_maximum_prefix_max_prefix_no>
                            # [<nbr_af_maximum_prefix_threshold>] restart
                            # [restart <nbr_af_maximum_prefix_restart> |
                            # warning-only ]
                            v = attributes.value(
                                'nbr_af_maximum_prefix_warning_only')
                            if attributes.value(
                                'nbr_af_maximum_prefix_max_prefix_no'):
                                if attributes.value(
                                    'nbr_af_maximum_prefix_threshold'):
                                    if attributes.value(
                                        'nbr_af_maximum_prefix_restart'):
                                        if v:
                                            configurations.append_line(
                                                attributes.format(
                                    'maximum-prefix '
                                    '{nbr_af_maximum_prefix_max_prefix_no}'
                                    ' restart '
                                    '{nbr_af_maximum_prefix_restart} '
                                    '{nbr_af_maximum_prefix_warning_only}'))
                                else:
                                    configurations.append_line(
                                        attributes.format('maximum-prefix '
                                    '{nbr_af_maximum_prefix_max_prefix_no}'))

                            if attributes.value('nbr_af_suppress_inactive'):
                                configurations.append_line('suppress-inactive')

                            if attributes.value('nbr_af_disable_peer_as_check'):
                                configurations.append_line('disable-peer-as-check')
                            # nxos: address-family <nbr_af_name> \
                            # route-map <nbr_af_route_map_name_in> in
                            if attributes.value('nbr_af_route_map_name_in'):
                                configurations.append_line(
                                    attributes.format('route-map '
                                        '{nbr_af_route_map_name_in} in'))

                            # nxos: address-family <nbr_af_name> \
                            # route-map <nbr_af_route_map_name_out> out
                            if attributes.value('nbr_af_route_map_name_out'):
                                configurations.append_line(
                                    attributes.format('route-map'
                                        ' {nbr_af_route_map_name_out} out'))

                            # nxos: address-family <nbr_af_name> \
                            # route-reflector-client
                            if attributes.value(
                                'nbr_af_route_reflector_client'):
                                    configurations.append_line(
                                        attributes.format(
                                            'route-reflector-client'))

                            # nxos: address-family <nbr_af_name> \
                            # send-community
                            if attributes.value('nbr_af_send_community'):
                                if attributes.value(
                                    'nbr_af_send_community').value == \
                                    'standard':
                                    configurations.append_line(
                                        attributes.format('send-community'))

                                # nxos: address-family <nbr_af_name> \
                                # send-community extended
                                if attributes.value(
                                    'nbr_af_send_community').value == \
                                    'extended':
                                    configurations.append_line(
                                        attributes.format(
                                        'send-community extended'))

                                # nxos: address-family <nbr_af_name> \
                                # send-communitys
                                # nxos: address-family <nbr_af_name> \
                                # send-community extended
                                if attributes.value(
                                    'nbr_af_send_community').value == 'both':
                                    configurations.append_line(
                                        attributes.format('send-community'))
                                    configurations.append_line(
                                        attributes.format(
                                        'send-community extended'))

                            # nxos: address-family <nbr_af_name> \
                            # soft-reconfiguration inbound
                            if attributes.value('nbr_af_soft_reconfiguration'):
                                configurations.append_line(
                                    attributes.format('soft-reconfiguration '
                                        'inbound'))

                            # nxos: address-family <nbr_af_name> \
                            # next-hop-self
                            if attributes.value('nbr_af_next_hop_self'):
                                configurations.append_line(
                                    attributes.format('next-hop-self'))

                            # nxos: address-family <nbr_af_name> \
                            # as-override
                            if attributes.value('nbr_af_as_override'):
                                configurations.append_line(
                                    attributes.format('as-override'))

                            # nxos: address-family <nbr_af_name> \
                            # default-originate
                            # nxos: address-family <nbr_af_name> \
                            # default-originate route-map test
                            if attributes.value('nbr_af_default_originate'):
                                if attributes.value(
                                    'nbr_af_default_originate_route_map'):
                                    configurations.append_line(
                                        attributes.format('default-originate '
                                    'route-map '
                                    '{nbr_af_default_originate_route_map}'))
                                else:
                                    configurations.append_line(
                                        attributes.format('default-originate'))

                            # nxos except n9k,n9kv : address-family <nbr_af_name> \
                            # suppress-signaling-protocol ldp
                            if attributes.value('nbr_af_suppress_signaling_protocol_ldp'):
                                configurations.append_line(
                                    attributes.format('suppress-signling-protocol ldp'))

                            # nxos: address-family <nbr_af_name> \
                            # soo 100:100
                            if attributes.value('nbr_af_soo'):
                                configurations.append_line(
                                    attributes.format('soo {nbr_af_soo}'))

                            # nxos: address-family <nbr_af_name> \
                            # rewrite-evpn-rt-asn
                            if attributes.value('nbr_af_rewrite_evpn_rt_asn'):
                                configurations.append_line(
                                    attributes.format('rewrite-evpn-rt-asn'))
                            # rewrite-mvpn-rt-asn
                            if attributes.value('nbr_af_rewrite_mvpn_rt_asn'):
                                configurations.append_line(
                                    attributes.format('rewrite-rt-asn'))

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None,
                                       **kwargs):
                        return self.build_config(apply=apply,
                                                 attributes=attributes,
                                                 unconfig=True, **kwargs)

