
# import python
from abc import ABC

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

            # self.bgp_id condition is for the partial_configuration scenarios
            if attributes.format('{bgp_id}') or self.bgp_id:

                # We need to build 'mpls ....' configuration line on the same
                # level as router bgp <bgp_id> while the configuartion needs
                # vrf/address_family attributes. Hence, we create that
                # dictionary to collect the correspomnding vrf/address_family
                # info and build it back at the top of the structure.
                if not hasattr (self, 'mpls_label_dict'):
                    self.mpls_label_dict = {}

                # iosxe: router bgp 100
                with configurations.submode_context(attributes.format(
                    'router bgp {bgp_id}', force=True)):

                    if unconfig and attributes.iswildcard:
                        # Looping over vrf to cover the case of
                        # 'af_label_allocation_mode'
                        for sub, attributes2 in attributes.mapping_values(
                            'vrf_attr', sort=True,
                            keys=self.vrf_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig))
                        configurations.submode_unconfig()

                    for sub, attributes2 in attributes.mapping_values(
                        'vrf_attr', sort=True,
                        keys=self.vrf_attr):
                        configurations.append_block(
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

                if self.mpls_label_dict:
                    for vrf in self.mpls_label_dict['vrf']:
                        for add_family in self.mpls_label_dict['vrf'][vrf]\
                            ['add_family']:
                            af_name = add_family
                            af_label_allocation_mode = \
                                self.mpls_label_dict['vrf'][vrf]\
                                ['add_family'][af_name]\
                                ['af_label_allocation_mode']
                        configurations.append_line(
                            'mpls label mode vrf {vrf_name} protocol '
                            '{af_name} {label_mode}'.format(
                                af_name=af_name,
                                vrf_name=vrf,
                                label_mode=af_label_allocation_mode))
            else:
                # iosxe: router bgp 100
                with configurations.submode_context(attributes.format(
                    'router bgp {asn}', force=True)):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # iosxe: router bgp 100 / bgp router-id 1.2.3.4
                    configurations.append_line(attributes.format(
                        'bgp router-id {router_id}'))

                    # iosxe: router bgp 100 / bgp graceful-restart
                    if attributes.value('graceful_restart'):
                        configurations.append_line(attributes.format(
                            'bgp graceful-restart'))

                    # iosxe : router bgp 100 / no bgp default ipv4-unicast
                    if attributes.value('disable_bgp_default_ipv4_unicast'):
                        configurations.append_line(
                            attributes.format('no bgp default ipv4-unicast'), 
                            unconfig_cmd = attributes.format(
                                'bgp default ipv4-unicast'))

                    for sub, attributes2 in attributes.mapping_values(
                        'vrf_attr', sort=True, keys=self.vrfs):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))

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

                    # iosxe: template peer-policy <pp_name> \
                    # allowas-in [9]
                    if attributes.value('pp_allowas_in'):
                        if attributes.value('pp_allowas_in_as_number'):
                            configurations.append_line(
                                attributes.format('allowas-in '
                                                  '{pp_allowas_in_as_number}'))
                        else:
                            configurations.append_line(
                                attributes.format('allowas-in'))

                    # iosxe: template peer-policy <pp_name> \
                    # as-override
                    if attributes.value('pp_as_override'):
                        configurations.append_line(
                            attributes.format('as-override'))

                    # iosxe: template peer-policy <pp_name> \
                    # send-community [ both | extended | standard ]
                    if attributes.value('pp_send_community'):
                        configurations.append_line(attributes.format(
                            'send-community {pp_send_community.value}'))

                    # iosxe: template peer-policy <pp_name> \
                    # route-reflector-client
                    if attributes.value('pp_route_reflector_client'):
                        configurations.append_line(
                            attributes.format(
                                'route-reflector-client'))

                    # iosxe: template peer-policy <pp_name> \
                    # next-hop-self
                    if attributes.value('pp_next_hop_self'):
                        configurations.append_line(
                            attributes.format(
                                'next-hop-self'))

                    # iosxe: template peer-policy <pp_name> \
                    # route-map test-map in
                    if attributes.value('pp_route_map_name_in'):
                        configurations.append_line(
                            attributes.format('route-map '
                                '{pp_route_map_name_in} in'))

                    # iosxe: template peer-policy <pp_name> \
                    # route-map test-map out
                    if attributes.value('pp_route_map_name_out'):
                        configurations.append_line(
                            attributes.format('route-map '
                                '{pp_route_map_name_out} out'))

                    # iosxe: template peer-policy <pp_name> \
                    # mmaximum-prefix <pp_maximum_prefix_max_prefix_no> 
                    # [<pp_maximum_prefix_threshold> [ restart 
                    # <pp_maximum_prefix_restart> | warning-only ]]
                    if attributes.value('pp_maximum_prefix_max_prefix_no'):
                        if attributes.value('pp_maximum_prefix_threshold'):
                            if attributes.value(
                                'pp_maximum_prefix_restart'):
                                configurations.append_line(
                                    attributes.format('maximum-prefix '
                                    '{pp_maximum_prefix_max_prefix_no} '
                                    '{pp_maximum_prefix_threshold} '
                                    'restart {pp_maximum_prefix_restart}'))
                            elif attributes.value(
                                'pp_maximum_prefix_warning_only'):
                                configurations.append_line(
                                    attributes.format('maximum-prefix '
                                    '{pp_maximum_prefix_max_prefix_no} '
                                    '{pp_maximum_prefix_threshold} '
                                    'warning-only'))
                            else:
                                configurations.append_line(
                                    attributes.format('maximum-prefix '
                                    '{pp_maximum_prefix_max_prefix_no} '
                                    '{pp_maximum_prefix_threshold}'))
                        else:
                            configurations.append_line(attributes.format(
                                'maximum-prefix '
                                '{pp_maximum_prefix_max_prefix_no}'))

                    # iosxe: template peer-policy <pp_name> \
                    # default-originate
                    # iosxe: template peer-policy <pp_name> \
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

                    # iosxe: template peer-policy <pp_name> \
                    # soft-reconfiguration inbound
                    if attributes.value('pp_soft_reconfiguration'):
                        configurations.append_line(
                            attributes.format('soft-reconfiguration inbound'))

                    # iosxe: template peer-policy <pp_name> \
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

                    # iosxe: template peer-session <peer_session> \ bfd
                    if attributes.value('ps_fall_over_bfd'):
                        configurations.append_line(
                            attributes.format('fall-over bfd'))

                    # iosxe: template peer-session <peer_session> \
                    # remote-as 500
                    if attributes.value('ps_remote_as'):
                        configurations.append_line(
                            attributes.format('remote-as {ps_remote_as}'))

                    # iosxe: template peer-session <peer_session> \
                    # local-as 111 [[dual-as] | [no-prepend [replace-as]]]
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

                    # iosxe: template peer-session <peer_session> \
                    # description PEER-SESSION
                    if attributes.value('ps_description'):
                        configurations.append_line(
                            attributes.format('description {ps_description}'))

                    # iosxe: template peer-session <peer_session> \
                    # password 3 386c0565965f89de
                    if attributes.value('ps_password_text'):
                        configurations.append_line(
                            attributes.format('password {ps_password_text}'))

                    # iosxe: template peer-session <peer_session> \ shutdown
                    if attributes.value('ps_shutdown'):
                        configurations.append_line(
                            attributes.format('shutdown'))

                    # iosxe: template peer-session <peer_session> \
                    # update-source loopback0
                    if attributes.value('ps_update_source'):
                        configurations.append_line(
                            attributes.format('update-source '
                                              '{ps_update_source}'))

                    # iosxe: template peer-session <peer_session> \
                    # disable-connected-check
                    if attributes.value('ps_disable_connected_check'):
                        configurations.append_line(
                            attributes.format('disable-connected-check'))

                    # iosxe: template peer-session <peer_session> \
                    # capability suppress 4-byte-as
                    if attributes.value(
                        'ps_suppress_four_byte_as_capability'):
                        configurations.append_line(attributes.format(
                            'dont-capability-negotiate four-octets-as'))

                    # iosxe: template peer-session <peer_session> \
                    # ebgp-multihop 255
                    if attributes.value('ps_ebgp_multihop_max_hop'):
                        configurations.append_line(
                            attributes.format('ebgp-multihop '
                                '{ps_ebgp_multihop_max_hop}'))
                    elif attributes.value('ps_ebgp_multihop'):
                        configurations.append_line(
                            attributes.format('ebgp-multihop 255'))

                    # iosxe: template peer-session <peer_session> \
                    # transport connection-mode <ps_transport_connection_mode>
                    if attributes.value('ps_transport_connection_mode'):
                        configurations.append_line(
                            attributes.format('transport connection-mode '
                                '{ps_transport_connection_mode.value}'))

                    # iosxe: template peer-session <peer_session> \
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

                # self.bgp_id condition is for the partial_configuration
                # scenarios
                if attributes.format('{bgp_id}') or self.bgp_id:
                    if not self.vrf:
                        self.vrf_name == 'default'
                    else:
                        self.vrf_name == self.vrf.name

                    # iosxe: router bgp 100 / [instance someword] /
                    # [vrf someword] /[bgpalways-compare-med] |
                    # [bgp bestpath {med missing-as-worst |
                    # compare-routerid | cost-community ignore} ]
                    if attributes.value('always_compare_med'):
                        configurations.append_line(attributes.format(
                            'bgp always-compare-med'))
                    if attributes.value('bestpath_compare_routerid'):
                        configurations.append_line(attributes.format(
                            'bgp bestpath compare-routerid'))
                    if attributes.value('bestpath_cost_community_ignore'):
                        configurations.append_line(attributes.format(
                            'bgp bestpath cost-community ignore'))
                    if attributes.value('bestpath_med_missing_at_worst'):
                        configurations.append_line(attributes.format(
                            'bgp bestpath med missing-as-worst'))

                    # iosxe: router bgp 100 / [instance someword] /
                    # [vrf someword] / bgp cluster-id <cluster_id>
                    if attributes.value('cluster_id'):
                        configurations.append_line(attributes.format(
                            'bgp cluster-id {cluster_id}'))

                    # iosxe: router bgp 100 / [instance someword] /
                    # [vrf someword] / bgp confederation identifier 
                    # <confederation_identifier>
                    if attributes.value('confederation_identifier'):
                        configurations.append_line(
                            attributes.format(
                                'bgp confederation identifier '
                                '{confederation_identifier}'))

                    # iosxe: router bgp 100 / [instance someword] /
                    # [vrf someword] / bgp confederation peers 
                    # <confederation_peers_as>
                    if attributes.value('confederation_peers_as'):
                        configurations.append_line(
                            attributes.format('bgp confederation peers '
                                '{confederation_peers_as}'))

                    # iosxe: router bgp 100 / [vrf someword] / bgp
                    # graceful-restart
                    if attributes.value('graceful_restart'):
                        configurations.append_line(
                            attributes.format('bgp graceful-restart'))

                    # iosxe: router bgp 100 / [vrf someword] /
                    # bgp graceful-restart restart-time 240
                    if attributes.value('graceful_restart_restart_time'):
                        configurations.append_line(
                            attributes.format('bgp graceful-restart '
                                'restart-time '
                                '{graceful_restart_restart_time}'))

                    # iosxe: router bgp 100 / [vrf someword] /
                    # bgp graceful-restart stalepath-time 600
                    if attributes.value('graceful_restart_stalepath_time'):
                        configurations.append_line(
                            attributes.format('bgp graceful-restart '
                                'stalepath-time '
                                '{graceful_restart_stalepath_time}'))

                    # iosxe: router bgp 100 / [vrf someword] /
                    # bgp log-neighbor-changes
                    if attributes.value('log_neighbor_changes'):
                        configurations.append_line(
                            attributes.format('bgp log-neighbor-changes'))

                    # iosxe: router bgp 100 / [vrf someword] /
                    # bgp router-id 1.2.3.4
                    if attributes.value('router_id'):
                        configurations.append_line(attributes.format(
                            'bgp router-id {router_id}'))

                    # iosxe: router bgp 100 / [vrf someword] /
                    # timers bgp <keepalive-interval> <holdtime>
                    if attributes.value('keepalive_interval') and \
                        attributes.value('holdtime'):
                        configurations.append_line(
                            attributes.format('timers bgp '
                                '{keepalive_interval} {holdtime}'))

                    # iosxe: router bgp 100 / [vrf someword] /
                    # bgp fast-external-fallover
                    if attributes.value('enforce-first-as'):
                        configurations.append_line(
                            attributes.format('bgp enforce-first-as'))

                    # iosxe: router bgp 100 / [vrf someword] / 
                    # no fast-external-fallover
                    if attributes.value('fast_external_fallover'):
                        configurations.append_line(
                            attributes.format(
                                'bgp fast-external-fallover'))

                   # iosxe: router bgp 100 / [vrf someword] /
                   # no bgp default ipv4-unicast
                    if attributes.value('default_choice_ipv4_unicast'):
                        configurations.append_line(
                            attributes.format(
                                'no bgp default ipv4-unicast'),
                                unconfig_cmd=attributes.format(
                                'bgp default ipv4-unicast'))

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
                else:
                    for neighbor_sub, neighbor_attributes in \
                        attributes.mapping_values('neighbor_attr',
                                                  keys=self.neighbors):
                        configurations.append_block(
                            neighbor_sub.build_config(apply=False,
                                attributes=neighbor_attributes,
                                unconfig=unconfig))

                        for address_family_sub, address_family_attributes in \
                            neighbor_attributes.mapping_values(
                                'address_family_attr', sort=True):
                            if self.vrf_name != 'default':
                                context_cli = \
                                    address_family_attributes.format(
                                        'address-family {address_family.value}'
                                        ' vrf %s' % self.vrf_name, force=True)
                            else:
                                context_cli = \
                                    address_family_attributes.format(
                                    'address-family {address_family.value}',
                                    force=True)

                            with configurations.submode_context(context_cli):

                                if address_family_attributes.value('activate'):
                                    configurations.append_line(
                                        address_family_attributes.format(
                                            'neighbor {neighbor.ip} activate',
                                            force_neighbor=True))

                                if address_family_attributes.value(
                                    'nexthop_self'):
                                    configurations.append_line(
                                        address_family_attributes.format(
                                            'neighbor {neighbor.ip} '
                                            'next-hop-self',
                                            force_neighbor=True))

                                if address_family_attributes.value(
                                    'route_reflector_client'):
                                    configurations.append_line(
                                        address_family_attributes.format(
                                            'neighbor {neighbor.ip} '
                                            'route-reflector-client',
                                            force_neighbor=True))

                                configurations.append_line(
                                    address_family_attributes.format(
                                        'neighbor {neighbor.ip} '
                                        'send-community {send_community}',
                                        force_neighbor=True))

                    for address_family_sub, address_family_attributes in \
                        attributes.mapping_values('address_family_attr',
                            keys = self.address_families):
                        configurations.append_block(
                            address_family_sub.build_config(apply=False,
                                attributes=address_family_attributes,
                                unconfig=unconfig, vrf_name = self.vrf_name))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                    unconfig=True, **kwargs)

            class AddressFamilyAttributes(ABC):

                def build_config(self, apply=True, attributes=None,
                    unconfig=False, **kwargs):
                    assert not apply
                    vrf_name = self.parent._vrf_name
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    with configurations.submode_context(
                        attributes.format(
                            'address-family {address_family.value} '
                            'vrf {vrf_name}',
                            force=True) if self.vrf_name != 'default' else \
                        attributes.format(
                            'address-family {address_family.value}',
                            force=True)):

                        if unconfig and attributes.iswildcard:
                            if attributes.value('address_family') is not None:
                                af_name = ''
                                if attributes.value('address_family').value ==\
                                    'ipv4 unicast':
                                    af_name = 'bgp-vpnv4'
                                if attributes.value('address_family').value ==\
                                    'ipv6 unicast':
                                    af_name = 'bgp-vpnv6'
                            if attributes.value('af_label_allocation_mode') \
                                and af_name:
                                if 'vrf' not in \
                                    self.parent.parent.mpls_label_dict:
                                    self.parent.parent.mpls_label_dict['vrf'] \
                                        = {}
                                if vrf_name not in \
                                    self.parent.parent.mpls_label_dict['vrf']:
                                    self.parent.parent.mpls_label_dict['vrf']\
                                    [vrf_name] = {}
                                if 'add_family' not in \
                                    self.parent.parent.mpls_label_dict['vrf']\
                                    [vrf_name]:
                                    self.parent.parent.mpls_label_dict['vrf']\
                                    [vrf_name]['add_family'] = {}
                                if af_name not in \
                                    self.parent.parent.mpls_label_dict['vrf']\
                                    [vrf_name]['add_family']:
                                    self.parent.parent.mpls_label_dict['vrf']\
                                    [vrf_name]['add_family'][af_name] = {}

                                self.parent.parent.mpls_label_dict['vrf']\
                                    [vrf_name]['add_family'][af_name]\
                                    ['af_label_allocation_mode'] = \
                                    attributes.value(
                                        'af_label_allocation_mode').value

                            configurations.submode_unconfig()

                        # iosxe: address-family ipv4 unicast/
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

                        # redistribute <protocol> metric <metric>
                        isis_metric_name = ''
                        ospf_metric_name = ''
                        rip_metric_name = ''
                        if attributes.value('af_redist_isis_metric'):
                            isis_metric_name = attributes.format(
                                'af_redist_isis_metric')
                        elif attributes.value('af_redist_ospf_metric'):
                            ospf_metric_name = attributes.format(
                                'af_redist_ospf_metric')
                        elif attributes.value('af_redist_rip_metric'):
                            rip_metric_name = attributes.format(
                                'af_redist_rip_metric')

                        # redistribute <protocol> <protocol.pid> metric
                        # <metric> route-map <route_policy>
                        for redistribute, redistribute_attributes in \
                            attributes.sequence_values('redistributes'):
                            assert redistribute_attributes.iswildcard
                            cfg = 'redistribute'
                            if isinstance(redistribute.protocol, Ospf):
                                cfg += redistribute_attributes.format(
                                    ' ospf {protocol.pid}')
                                if ospf_metric_name:
                                    cfg += 'metric {ospf_metric_name}'
                                if ospf_route_policy_name:
                                    cfg += 'route-map {ospf_route_policy_name}'
                            elif isinstance(redistribute.protocol, Isis):
                                cfg += redistribute_attributes.format(
                                    ' isis {protocol.pid}')
                                if isis_metric_name:
                                    cfg += 'metric {isis_metric_name}'
                                if isis_route_policy_name:
                                    cfg += 'route-map {isis_route_policy_name}'
                            elif isinstance(redistribute.protocol, Rip):
                                cfg += redistribute_attributes.format(' rip '
                                    '{protocol.pid}')
                                if rip_metric_name:
                                    cfg += 'metric {rip_metric_name}'
                                if rip_route_policy_name:
                                    cfg += 'route-map {rip_route_policy_name}'
                            else:
                                raise ValueError(redistribute.protocol)

                            configurations.append_line(
                                attributes.format(cfg))

                        # iosxe: address-family ipv4 unicast/
                        # redistribute static
                        cfg = ''
                        if attributes.value('af_redist_static'):
                            cfg = 'redistribute static'
                            # iosxe: address-family ipv4 unicast/
                            # redistribute static metric <metric>
                            if attributes.value('af_redist_static_metric'):
                                cfg += ' metric {af_redist_static_metric}'
                            # iosxe: address-family ipv4 unicast/
                            # redistribute static route-map <route_policy>
                            if attributes.value(
                                'af_redist_static_route_policy'):
                                cfg += ' route-map '\
                                       '{af_redist_static_route_policy}'
                        
                        if cfg:
                            configurations.append_line(
                                attributes.format(cfg))

                        # iosxe: address-family ipv4 unicast/
                        # redistribute connected
                        cfg = ''
                        if attributes.value('af_redist_connected'):
                            cfg = 'redistribute connected'
                            # iosxe: address-family ipv4 unicast/
                            # redistribute connected metric <metric>
                            if attributes.value('af_redist_connected_metric'):
                                cfg += ' metric {af_redist_connected_metric}'
                            # iosxe: address-family ipv4 unicast/
                            # redistribute connected route-map <route_policy>
                            if attributes.value(
                                'af_redist_connected_route_policy'):
                                cfg += ' route-map '\
                                       '{af_redist_connected_route_policy}'
                        
                        if cfg:
                            configurations.append_line(
                                attributes.format(cfg))

                        # iosxe: address-family ipv4 unicast/
                        # dampening 25 1000 1500 255
                        if attributes.value('af_dampening'):
                            cfg = 'bgp dampening'
                            if attributes.value('af_dampening_route_map'):
                                cfg += ' route-map {af_dampening_route_map}'
                            if attributes.value('af_dampening_half_life_time'):
                                cfg += ' {af_dampening_half_life_time}'
                                if attributes.value(
                                    'af_dampening_reuse_time') and \
                                    attributes.value(
                                        'af_dampening_suppress_time') and\
                                    attributes.value(
                                        'af_dampening_max_suppress_time'):
                                    cfg += ' {af_dampening_reuse_time} '\
                                           '{af_dampening_suppress_time} '\
                                           '{af_dampening_max_suppress_time}'

                            configurations.append_line(
                                attributes.format(cfg))

                        # iosxe: address-family ipv4 unicast/
                        # nexthop route-map <af_nexthop_route_map>
                        if attributes.value('af_nexthop_route_map'):
                            configurations.append_line(
                                attributes.format(
                                    'bgp nexthop route-map '
                                    '{af_nexthop_route_map}'))

                        # iosxe: address-family ipv4 unicast/
                        # bgp nexthop trigger delay critical
                        # <af_nexthop_trigger_delay_critical>
                        if attributes.value('af_nexthop_trigger_enable'):
                            if attributes.value(
                                'af_nexthop_trigger_delay_critical'):
                                configurations.append_line(attributes.format(
                                    'bgp nexthop trigger delay '
                                    '{af_nexthop_trigger_delay_critical}'))

                        # iosxe: address-family ipv4 unicast/
                        # bgp client-to-client reflection
                        if attributes.value('af_client_to_client_reflection'):
                            configurations.append_line(
                                attributes.format(
                                    'bgp client-to-client reflection'))

                        # iosxe: address-family ipv4 unicast/
                        # distance bgp <af_distance_extern_as> 
                        # <af_distance_internal_as> <af_distance_local>
                        if attributes.value('af_distance_extern_as'):
                            if attributes.value('af_distance_internal_as') and\
                                 attributes.value('af_distance_local') :
                                configurations.append_line(
                                    attributes.format(
                                        'distance bgp {af_distance_extern_as} '
                                        '{af_distance_internal_as} '
                                        '{af_distance_local}'))

                        # iosxe: address-family ipv4 unicast/ 
                        # maximum-paths <af_maximum_paths_ebgp>
                        if attributes.value('af_maximum_paths_ebgp'):
                            configurations.append_line(
                                attributes.format('maximum-paths '
                                    '{af_maximum_paths_ebgp}'))

                        # iosxe: address-family ipv4 unicast/
                        # maximum-paths ibgp <af_maximum_paths_ibgp>
                        if attributes.value('af_maximum_paths_ibgp'):
                            configurations.append_line(
                                attributes.format('maximum-paths ibgp '
                                    '{af_maximum_paths_ibgp}'))

                        # iosxe: address-family ipv4 unicast/
                        # maximum-paths eigp <af_maximum_paths_eibgp>
                        if attributes.value('af_maximum_paths_eibgp'):
                            configurations.append_line(
                                attributes.format('maximum-paths eibgp '
                                    '{af_maximum_paths_eibgp}'))

                        # iosxe: address-family ipv4 unicast/
                        # aggregate-address <af_aggregate_address_ipv4_address>
                        # <af_aggregate_address_ipv4_mask>
                        # [ as-set | summary-only ]
                        v = attributes.value(
                            'af_aggregate_address_ipv4_address')
                        k = attributes.value('af_aggregate_address_ipv4_mask')
                        if v and k:
                            base_s = 'aggregate-address '\
                                     '{af_aggregate_address_ipv4_address} '\
                                     '{af_aggregate_address_ipv4_mask}'
                            if attributes.value(
                                'af_aggregate_address_as_set'):
                                base_s += ' as-set'
                            if attributes.value(
                                'af_aggregate_address_summary_only'):
                                base_s += ' summary-only'

                            configurations.append_line(
                                attributes.format(base_s))

                        # iosxe: address-family ipv4 unicast/
                        # network <af_network_number> [mask <af_network_mask>]
                        # [route-map  <af_network_route_map>]
                        if attributes.value('af_network_number'):
                            base_s = 'network {af_network_number}'
                            if attributes.value('af_network_mask'):
                                base_s += 'mask {af_network_mask}'
                            if attributes.value('af_network_route_map'):
                                base_s += 'route-map {af_network_route_map}'

                            configurations.append_line(
                                attributes.format(base_s))

                        # iosxe: address-family ipv4 unicast/ aggregate-address 
                        # <af_v6_aggregate_address_ipv6_address>
                        # [as-set] [summary-only]
                        cfg = ''
                        if attributes.value(
                            'af_v6_aggregate_address_ipv6_address'):
                            cfg = 'aggregate-address '\
                                  '{af_v6_aggregate_address_ipv6_address}'
                            if attributes.value(
                                'af_v6_aggregate_address_as_set'):
                                cfg += 'as-set'
                            if attributes.value(
                                'af_v6_aggregate_address_summary_only'):
                                cfg += 'summary-only'

                            configurations.append_line(
                                attributes.format(cfg))

                        # iosxe: address-family ipv4 unicast/
                        # network <af_v6_network_number>  [route-map 
                        # <af_v6_network_route_map> ]
                        cfg = ''
                        if attributes.value(
                            'af_v6_network_number'):
                            cfg = 'network {af_v6_network_number}'
                            if attributes.value(
                                'af_v6_network_route_map'):
                                cfg += 'route-map {af_v6_network_route_map}'

                            configurations.append_line(
                                attributes.format(cfg))

                        # Only handle 'vpn4 unicast' & 'vpn6 unicast'
                        if attributes.value('address_family') is not None:
                            af_name = ''
                            if attributes.value('address_family').value ==\
                                'ipv4 unicast':
                                af_name = 'bgp-vpnv4'
                            if attributes.value('address_family').value ==\
                                'ipv6 unicast':
                                af_name = 'bgp-vpnv6'

                        # iosxe: address-family ipv4 unicast/
                        # mpls label mode { vrf <vrf> | all-vrfs } protocol
                        # { all-afs | bgp-vpnv4 | bgp-vpnv6 }
                        # <af_label_allocation_mode>
                        if attributes.value('af_label_allocation_mode') and\
                            af_name:

                            if 'vrf' not in self.parent.parent.mpls_label_dict:
                                self.parent.parent.mpls_label_dict['vrf'] = {}
                            if vrf_name not in \
                                self.parent.parent.mpls_label_dict['vrf']:
                                self.parent.parent.mpls_label_dict['vrf']\
                                [vrf_name] = {}
                            if 'add_family' not in \
                                self.parent.parent.mpls_label_dict['vrf']\
                                [vrf_name]:
                                self.parent.parent.mpls_label_dict['vrf']\
                                [vrf_name]['add_family'] = {}
                            if af_name not in \
                                self.parent.parent.mpls_label_dict['vrf']\
                                [vrf_name]['add_family']:
                                self.parent.parent.mpls_label_dict['vrf']\
                                [vrf_name]['add_family'][af_name] = {}

                            self.parent.parent.mpls_label_dict['vrf']\
                                [vrf_name]['add_family'][af_name]\
                                ['af_label_allocation_mode'] = \
                                attributes.value(
                                    'af_label_allocation_mode').value

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None,
                    **kwargs):
                    return self.build_config(apply=apply,
                        attributes=attributes, unconfig=True, **kwargs)

            class NeighborAttributes(ABC):

                def build_config(self, apply=True, attributes=None,
                    unconfig=False, **kwargs):
                    assert not apply
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)
                    # Flag to track the neighbors attributes

                    # A method to avoid code duplication.
                    # Bulding neighbor attributes, whether under address-family
                    # or not.
                    def vrf_cases(configurations):
                        # iosxe: neighbor <neighbor_id> fall-over bfd
                        if attributes.value('nbr_fall_over_bfd') or \
                            attributes.value('bfd_fast_detect'):
                            configurations.append_line(
                                attributes.format('neighbor {neighbor} '
                                                  'fall-over bfd',
                                                  force=True))

                        # iosxe: neighbor <neighbor_id>
                        # dont-capability-negotiate four-octets-as
                        if attributes.value(
                            'nbr_suppress_four_byte_as_capability'):
                            configurations.append_line(
                                attributes.format('neighbor {neighbor} '
                                    'dont-capability-negotiate '
                                    'four-octets-as', force=True))

                        # iosxe: neighbor <neighbor_id>
                        # description <nbr_description>
                        if attributes.value(
                            'nbr_description'):
                            configurations.append_line(
                                attributes.format('neighbor {neighbor} '
                                    'description {nbr_description}',
                                    force=True))

                        # iosxe: neighbor <neighbor_id>
                        # disable-connected-check
                        if attributes.value(
                            'nbr_disable_connected_check'):
                            configurations.append_line(
                                attributes.format('neighbor {neighbor} '
                                    'disable-connected-check', force=True))

                        # iosxe: neighbor <neighbor_id>
                        # ebgp-multihop <nbr_ebgp_multihop_max_hop>
                        if attributes.value('nbr_ebgp_multihop'):
                            if attributes.value(
                                'nbr_ebgp_multihop_max_hop'):
                                configurations.append_line(
                                    attributes.format('neighbor {neighbor}'
                                        ' ebgp-multihop '
                                        '{nbr_ebgp_multihop_max_hop}',
                                        force=True))

                        # iosxe: neighbor <neighbor_id> inherit
                        # peer-session <nbr_inherit_peer_session>
                        if attributes.value(
                            'nbr_inherit_peer_session'):
                            configurations.append_line(
                                attributes.format('neighbor {neighbor} '
                                    'inherit peer-session '
                                    '{nbr_inherit_peer_session}',
                                    force=True))

                        # iosxe: neighbor <neighbor_id> local-as
                        # <nbr_local_as_as_no> [[dual-as] |
                        # [no-prepend [replace-as]]]
                        if attributes.value('nbr_local_as_as_no'):
                            cfg = 'neighbor {neighbor} local-as '\
                                  '{nbr_local_as_as_no}'
                            if attributes.value('nbr_local_as_dual_as'):
                                cfg += ' dual-as'
                            if attributes.value('nbr_local_as_no_prepend'):
                                cfg += ' no-prepend'
                                if attributes.value(
                                    'nbr_local_as_replace_as'):
                                    cfg += ' replace-as'

                            configurations.append_line(
                                attributes.format(cfg, force=True))

                        # iosxe: neighbor <neighbor_id> remote-as
                        # <nbr_remote_as>
                        if attributes.value('nbr_remote_as'):
                            configurations.append_line(
                                attributes.format('neighbor {neighbor} '
                                    'remote-as {nbr_remote_as}'))

                        # iosxe: neighbor <neighbor_id> address-family
                        # <nbr_remove_private_as_af_name>
                        if attributes.value(
                            'nbr_remove_private_as_af_name'):
                            with configurations.submode_context(
                                attributes.format('address-family '
                                    '{nbr_remove_private_as_af_name.value}',
                                                  force=True)):
                                if unconfig and attributes.iswildcard:
                                    # Never reached!
                                    configurations.submode_unconfig()

                                # iosxe: neighbor <neighbor_id>
                                # remove-private-as
                                if attributes.value(
                                    'nbr_remove_private_as'):
                                    configurations.append_line(
                                        attributes.format('neighbor '
                                            '{neighbor}'
                                            ' remove-private-as',
                                            force=True))

                        # iosxe: neighbor <neighbor_id> shutdown
                        if attributes.value('nbr_shutdown'):
                            configurations.append_line(
                                attributes.format('neighbor {neighbor} '
                                                  'shutdown', force=True))

                        # iosxe: neighbor <neighbor_id> timers
                        # <nbr_keepalive_interval>  <nbr_holdtime>
                        if attributes.value('nbr_keepalive_interval') and \
                            attributes.value('nbr_holdtime'):
                            configurations.append_line(
                                attributes.format('neighbor {neighbor} '
                                    'timers {nbr_keepalive_interval} '
                                    '{nbr_holdtime}', force=True))

                        # iosxe: neighbor <neighbor_id> update-source
                        # <nbr_update_source>
                        if attributes.value('update_source') or \
                           attributes.value('nbr_update_source'):
                            cfg = 'neighbor {neighbor}'
                            if hasattr(attributes.value(
                                'update_source'), 'name'):
                                val = attributes.value(
                                    'update_source').name
                            else:
                                val = self.nbr_update_source
                            cfg += ' update-source {val}'.format(val=val)
                            configurations.append_line(
                                attributes.format(cfg, force=True))

                        # iosxe: neighbor <neighbor_id> password
                        # <nbr_password_text>
                        if attributes.value('nbr_password_text'):
                            configurations.append_line(attributes.format(
                                'neighbor {neighbor} '
                                'password {nbr_password_text}',
                                force=True))

                        # iosxe: neighbor <neighbor_id>
                        # transport connection-mode
                        # {nbr_transport_connection_mode}
                        if attributes.value(
                            'nbr_transport_connection_mode'):
                            configurations.append_line(attributes.format(
                                'neighbor {neighbor} '
                                'transport connection-mode '
                                '{nbr_transport_connection_mode.value}',
                                force=True))

                        for address_family_sub, address_family_attributes \
                            in attributes.mapping_values(
                                'address_family_attr', sort=True):
                            configurations.append_block(
                                address_family_sub.build_config(
                                    apply=False,
                                    attributes=address_family_attributes,
                                    unconfig=unconfig))

                        return configurations

                    # self.bgp_id condition is for the partial
                    # configuration scenarios
                    if attributes.format('{bgp_id}') or self.bgp_id:

                        if unconfig and attributes.iswildcard:
                            configurations.append_line(
                                attributes.format('neighbor {neighbor}'))
                        # Case of no vrf
                        if not self.vrf:
                            # Call the function to build configurations
                            # directly under 'router bgp <bgp_id>'
                            vrf_cases(configurations)
                        # Case of vrf, we need to build our nbr_attributes
                        # under address_family
                        else:
                            # Case of having vrf value, neighbor attributes
                            # defined but no address-Family provided.
                            # We need to default the address_family as below.
                            if not attributes.obj.address_family_attr:
                                for neighbor in \
                                    attributes.obj.neighbor_attr.keys():
                                    neighbor_key = neighbor

                                if neighbor_key.ip._version == 4:
                                    add_family_value = 'ipv4 unicast'
                                else:
                                    add_family_value = 'ipv6 unicast'

                                cfg = 'address-family '
                                cfg += attributes.format(add_family_value)
                                with configurations.submode_context(
                                    attributes.format(cfg+' vrf {vrf_name}',
                                        force=True)):
                                    if unconfig and attributes.iswildcard:
                                        configurations.submode_unconfig()

                                    # Call the function to build configurations
                                    # under the 'address-family' section
                                    vrf_cases(configurations)
                            else:
                                for address_family_sub, \
                                    address_family_attributes \
                                    in attributes.mapping_values(
                                        'address_family_attr', sort=True):
                                    configurations.append_block(
                                        address_family_sub.build_config(
                                            apply=False,
                                            attributes=\
                                                address_family_attributes,
                                            unconfig=unconfig))
                    else:
                        # iosxe: router bgp 100 / neighbor <ipv4|ipv6>
                        # remote-as 65536
                        configurations.append_line(attributes.format('neighbor'
                            ' {neighbor.ip} remote-as {asn}'))

                        # iosxe: router bgp 100 / neighbor <ipv4|ipv6>
                        # update-source Loopback0
                        configurations.append_line(attributes.format('neighbor'
                            ' {neighbor.ip} update-source '
                            '{update_source.name}'))

                        # iosxe: router bgp 100 / neighbor <ipv4|ipv6>
                        # ha-mode sso
                        configurations.append_line(attributes.format(
                            'neighbor {neighbor.ip} ha-mode {ha_mode}'))
                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None,
                    **kwargs):
                    return self.build_config(apply=apply,
                        attributes=attributes, unconfig=True, **kwargs)

                class AddressFamilyAttributes(ABC):

                    def build_config(self, apply=True, attributes=None,
                        unconfig=False, **kwargs):
                        assert not apply
                        assert not kwargs, kwargs
                        vrf_name = self.parent.parent._vrf_name
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        with configurations.submode_context(
                            attributes.format(
                                'address-family {address_family.value} '
                                'vrf {vrf_name}',
                                force=True) if self.vrf_name != 'default' else\
                            attributes.format(
                                'address-family {address_family.value}',
                                force=True)):

                            if unconfig and attributes.iswildcard:
                                configurations.submode_unconfig()

                            # iosxe: address-family <nbr_af_name> \ neighbor
                            # <neighbor> activate
                            configurations.append_line(
                                attributes.format('neighbor {neighbor} '
                                    'activate', force=True))

                            # iosxe: address-family <nbr_af_name> \ neighbor
                            # <neighbor> allowas-in [ <allowas-in-cnt> ]
                            if attributes.value('nbr_af_allowas_in'):
                                if attributes.value(
                                    'nbr_af_allowas_in_as_number'):
                                    configurations.append_line(
                                        attributes.format('neighbor {neighbor}'
                                            ' allowas-in '
                                            '{nbr_af_allowas_in_as_number}',
                                            force=True))
                                else:
                                    configurations.append_line(
                                        attributes.format('neighbor {neighbor}'
                                            ' allowas-in', force=True))

                            # iosxe: address-family <nbr_af_name> \ neighbor
                            # <neighbor> peer-policy
                            # <nbr_af_inherit_peer_policy>
                            if attributes.value('nbr_af_inherit_peer_policy'):
                                configurations.append_line(
                                    attributes.format('neighbor {neighbor} '
                                        'peer-policy '
                                        '{nbr_af_inherit_peer_policy}',
                                        force=True))

                            # iosxe: address-family <nbr_af_name> \ neighbor
                            # <neighbor> maximum-prefix
                            # <nbr_af_maximum_prefix_max_prefix_no>
                            # [<nbr_af_maximum_prefix_threshold>] restart
                            # [restart <nbr_af_maximum_prefix_restart> |
                            # warning-only ]
                            if attributes.value(
                                'nbr_af_maximum_prefix_max_prefix_no'):
                                cfg = 'neighbor {neighbor} '\
                                      'maximum-prefix '\
                                      '{nbr_af_maximum_prefix_max_prefix_no}'
                                if attributes.value(
                                    'nbr_af_maximum_prefix_threshold'):
                                    cfg += ' {nbr_af_maximum_prefix_threshold}'
                                if attributes.value(
                                    'nbr_af_maximum_prefix_restart'):
                                    cfg += ' restart '\
                                           '{nbr_af_maximum_prefix_restart}'
                                elif attributes.value(
                                    'nbr_af_maximum_prefix_warning_only'):
                                    cfg += ' warning-only'

                                configurations.append_line(
                                    attributes.format(cfg, force=True))

                            # iosxe: address-family <nbr_af_name> \ neighbor
                            # <neighbor> route-map <nbr_af_route_map_name_in>
                            # in
                            if attributes.value('nbr_af_route_map_name_in'):
                                configurations.append_line(
                                    attributes.format('neighbor {neighbor} '
                                        'route-map '
                                        '{nbr_af_route_map_name_in} in',
                                        force=True))

                            # iosxe: address-family <nbr_af_name> \ neighbor
                            # <neighbor> route-map <nbr_af_route_map_name_out>
                            # out
                            if attributes.value('nbr_af_route_map_name_out'):
                                configurations.append_line(
                                    attributes.format('neighbor {neighbor} '
                                        'route-map '
                                        '{nbr_af_route_map_name_out} out',
                                        force=True))

                            # iosxe: address-family <nbr_af_name> \ neighbor
                            # <neighbor> route-reflector-client
                            if attributes.value(
                                'nbr_af_route_reflector_client'):
                                    configurations.append_line(
                                        attributes.format('neighbor {neighbor}'
                                            ' route-reflector-client',
                                            force=True))

                            # iosxe: address-family <nbr_af_name> \ neighbor
                            # <neighbor> send-community
                            if attributes.value('nbr_af_send_community'):
                                configurations.append_line(attributes.format(
                                    'neighbor {neighbor} '
                                    'send-community '
                                    '{nbr_af_send_community.value}',
                                    force=True))

                            # iosxe: address-family <nbr_af_name> \ neighbor
                            # <neighbor> soft-reconfiguration inbound
                            if attributes.value('nbr_af_soft_reconfiguration'):
                                configurations.append_line(
                                    attributes.format('neighbor {neighbor} '
                                        'soft-reconfiguration '
                                        'inbound', force=True))

                            # iosxe: address-family <nbr_af_name> \neighbor
                            # <neighbor_id> next-hop-self
                            if attributes.value('nbr_af_next_hop_self'):
                                configurations.append_line(
                                    attributes.format('neighbor {neighbor} '
                                        'next-hop-self', force=True))

                            # iosxe: address-family <nbr_af_name> \ neighbor
                            # <neighbor_id> as-override
                            if attributes.value('nbr_af_as_override'):
                                configurations.append_line(
                                    attributes.format('neighbor {neighbor} '
                                        'as-override', force=True))

                            # iosxe: address-family <nbr_af_name> \ neighbor
                            # <neighbor> default-originate
                            # iosxe: address-family <nbr_af_name> \ neighbor
                            # <neighbor> default-originate route-map test
                            if attributes.value('nbr_af_default_originate'):
                                if attributes.value(
                                    'nbr_af_default_originate_route_map'):
                                    configurations.append_line(
                                        attributes.format('neighbor {neighbor}'
                                    ' default-originate '
                                    'route-map '
                                    '{nbr_af_default_originate_route_map}',
                                    force=True))
                                else:
                                    configurations.append_line(
                                        attributes.format('neighbor {neighbor}'
                                            ' default-originate', force=True))

                            # iosxe: address-family <nbr_af_name> \ neighbor
                            # <neighbor_id> soo 100:100
                            if attributes.value('nbr_af_soo'):
                                configurations.append_line(
                                    attributes.format('neighbor {neighbor} '
                                        'soo {nbr_af_soo}', force=True))

                            # iosxe: address-family <nbr_af_name> \
                            # neighbor <neighbor_id> suppress-signaling-protocol
                            if attributes.value('nbr_af_suppress_signaling_protocol_ldp'):
                                configurations.append_line(
                                    attributes.format('neighbor {neighbor} suppress-signaling-protocol ldp'))

                            if self.vrf_name != 'default':
                                # iosxe: neighbor <neighbor_id> fall-over bfd
                                if attributes.value('nbr_fall_over_bfd') or \
                                    attributes.value('bfd_fast_detect'):
                                    configurations.append_line(
                                        attributes.format('neighbor {neighbor}'
                                                          ' fall-over bfd',
                                                          force=True))

                                # iosxe: neighbor <neighbor_id>
                                # dont-capability-negotiate four-octets-as
                                if attributes.value(
                                    'nbr_suppress_four_byte_as_capability'):
                                    configurations.append_line(
                                        attributes.format('neighbor {neighbor}'
                                            ' dont-capability-negotiate '
                                            'four-octets-as', force=True))

                                # iosxe: neighbor <neighbor_id>
                                # description <nbr_description>
                                if attributes.value(
                                    'nbr_description'):
                                    configurations.append_line(
                                        attributes.format('neighbor {neighbor}'
                                            ' description {nbr_description}',
                                            force=True))

                                # iosxe: neighbor <neighbor_id>
                                # disable-connected-check
                                if attributes.value(
                                    'nbr_disable_connected_check'):
                                    configurations.append_line(
                                        attributes.format('neighbor {neighbor}'
                                            ' disable-connected-check',
                                            force=True))

                                # iosxe: neighbor <neighbor_id>
                                # ebgp-multihop <nbr_ebgp_multihop_max_hop>
                                if attributes.value('nbr_ebgp_multihop'):
                                    if attributes.value(
                                        'nbr_ebgp_multihop_max_hop'):
                                        configurations.append_line(
                                            attributes.format('neighbor '
                                                '{neighbor} ebgp-multihop '
                                                '{nbr_ebgp_multihop_max_hop}',
                                                force=True))

                                # iosxe: neighbor <neighbor_id> inherit
                                # peer-session <nbr_inherit_peer_session>
                                if attributes.value(
                                    'nbr_inherit_peer_session'):
                                    configurations.append_line(
                                        attributes.format('neighbor {neighbor}'
                                            ' inherit peer-session '
                                            '{nbr_inherit_peer_session}',
                                            force=True))

                                # iosxe: neighbor <neighbor_id> local-as
                                # <nbr_local_as_as_no> [[dual-as] |
                                # [no-prepend [replace-as]]]
                                if attributes.value('nbr_local_as_as_no'):
                                    cfg = 'neighbor {neighbor} local-as '\
                                          '{nbr_local_as_as_no}'
                                    if attributes.value(
                                        'nbr_local_as_dual_as'):
                                        cfg += ' dual-as'
                                    if attributes.value(
                                        'nbr_local_as_no_prepend'):
                                        cfg += ' no-prepend'
                                        if attributes.value(
                                            'nbr_local_as_replace_as'):
                                            cfg += ' replace-as'

                                    configurations.append_line(
                                        attributes.format(cfg, force=True))

                                # iosxe: neighbor <neighbor_id> remote-as
                                # <nbr_remote_as>
                                if attributes.value('nbr_remote_as'):
                                    configurations.append_line(
                                        attributes.format('neighbor {neighbor} '
                                            'remote-as {nbr_remote_as}'))

                                # iosxe: neighbor <neighbor_id> address-family
                                # <nbr_remove_private_as_af_name>
                                if attributes.value(
                                    'nbr_remove_private_as_af_name'):
                                    with configurations.submode_context(
                                        attributes.format('address-family '
                                            '{nbr_remove_private_as_af_name.value}',
                                                          force=True)):
                                        if unconfig and attributes.iswildcard:
                                            # Never reached!
                                            configurations.submode_unconfig()

                                        # iosxe: neighbor <neighbor_id>
                                        # remove-private-as
                                        if attributes.value(
                                            'nbr_remove_private_as'):
                                            configurations.append_line(
                                                attributes.format('neighbor '
                                                    '{neighbor}'
                                                    ' remove-private-as',
                                                    force=True))

                                # iosxe: neighbor <neighbor_id> shutdown
                                if attributes.value('nbr_shutdown'):
                                    configurations.append_line(
                                        attributes.format('neighbor {neighbor}'
                                                          ' shutdown',
                                                          force=True))

                                # iosxe: neighbor <neighbor_id> timers
                                # <nbr_keepalive_interval>  <nbr_holdtime>
                                if attributes.value('nbr_keepalive_interval') \
                                    and attributes.value('nbr_holdtime'):
                                    configurations.append_line(
                                        attributes.format('neighbor {neighbor}'
                                            ' timers {nbr_keepalive_interval} '
                                            '{nbr_holdtime}', force=True))

                                # iosxe: neighbor <neighbor_id> update-source
                                # <nbr_update_source>
                                if attributes.value('update_source') or \
                                   attributes.value('nbr_update_source'):
                                    cfg = 'neighbor {neighbor}'
                                    if hasattr(attributes.value(
                                        'update_source'), 'name'):
                                        val = attributes.value(
                                            'update_source').name
                                    else:
                                        val = self.nbr_update_source
                                    cfg += ' update-source {val}'.format(
                                        val=val)
                                    configurations.append_line(
                                        attributes.format(cfg, force=True))

                                # iosxe: neighbor <neighbor_id> password
                                # <nbr_password_text>
                                if attributes.value('nbr_password_text'):
                                    configurations.append_line(
                                        attributes.format('neighbor {neighbor}'
                                        ' password {nbr_password_text}',
                                        force=True))

                                # iosxe: neighbor <neighbor_id>
                                # transport connection-mode
                                # {nbr_transport_connection_mode}
                                if attributes.value(
                                    'nbr_transport_connection_mode'):
                                    configurations.append_line(
                                        attributes.format('neighbor {neighbor}'
                                        ' transport connection-mode '
                                        '{nbr_transport_connection_mode.value}',
                                        force=True))


                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None,
                        **kwargs):
                        return self.build_config(apply=apply,
                            attributes=attributes, unconfig=True, **kwargs)

