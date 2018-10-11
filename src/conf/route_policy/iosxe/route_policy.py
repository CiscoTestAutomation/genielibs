# import python
from abc import ABC

# import genie
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

# Structure Hierarchy:
# +--Class RoutePolicy:
#         +--Class DeviceAttributes
#                +--Class StatementAttributes


class RoutePolicy(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            for sub, attributes2 in attributes.mapping_values(
                'statement_attr', keys=self.statement_attr):
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

        class StatementAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context(
                    attributes.format('route-map {policy_definition}'
                        ' {route_disposition.value} {statement_name}',
                        force=True)):
                    if unconfig and attributes.iswildcard:
                        # Never reached!
                        configurations.submode_unconfig()

                    # iosxe: description <description>
                    if attributes.value('description'):
                        configurations.append_line(
                            attributes.format('description {description}'))

                    # iosxe: match metric <match_med_eq>
                    if attributes.value('match_med_eq'):
                        configurations.append_line(
                            attributes.format('match metric {match_med_eq}'))

                    # iosxe: match ip next-hop prefix-list <match_nexthop_in>
                    if attributes.value('match_nexthop_in'):
                        configurations.append_line(
                            attributes.format('match ip next-hop prefix-list '
                                '{match_nexthop_in}'))

                    # iosxe: match ipv6 next-hop prefix-list
                    # <match_nexthop_in_v6>
                    if attributes.value('match_nexthop_in_v6'):
                        configurations.append_line(
                            attributes.format('match ipv6 next-hop '
                                'prefix-list {match_nexthop_in_v6}'))

                    # iosxe: match local-preference <match_local_pref_eq>
                    if attributes.value('match_local_pref_eq'):
                        configurations.append_line(
                            attributes.format('match local-preference '
                                '{match_local_pref_eq}'))

                    # iosxe: match route-type <match_route_type>
                    if attributes.value('match_route_type'):
                        configurations.append_line(
                            attributes.format('match route-type '
                                '{match_route_type.value}'))

                    # iosxe: match community <match_community_list>
                    if attributes.value('match_community_list'):
                        configurations.append_line(
                            attributes.format('match community '
                                '{match_community_list}'))

                    # iosxe: match extcommunity <match_ext_community_list>
                    if attributes.value('match_ext_community_list'):
                        configurations.append_line(
                            attributes.format('match extcommunity '
                                '{match_ext_community_list}'))

                    # iosxe: match as-path <match_as_path_list>
                    if attributes.value('match_as_path_list'):
                        configurations.append_line(
                            attributes.format('match as-path '
                                '{match_as_path_list}'))

                    # iosxe: match route-type <match_level_eq>
                    if attributes.value('match_level_eq'):
                        if attributes.value('match_level_eq')._value_ ==\
                            'level-1-2':
                            configurations.append_line(
                                attributes.format('match route-type '
                                    'level-1'))
                            configurations.append_line(
                                attributes.format('match route-type '
                                    'level-2'))
                        else:
                            configurations.append_line(
                                attributes.format('match route-type '
                                    '{match_level_eq.value}'))

                    # iosxe: match interface <match_interface>
                    if attributes.value('match_interface'):
                        configurations.append_line(
                            attributes.format('match interface '
                                '{match_interface}'))

                    # iosxe: match ip address prefix-list <match_prefix_list>
                    if attributes.value('match_prefix_list'):
                        configurations.append_line(
                            attributes.format('match ip address prefix-list '
                                '{match_prefix_list}'))

                    # iosxe: match ipv6 address prefix-list
                    # <match_prefix_list_v6>
                    if attributes.value('match_prefix_list_v6'):
                        configurations.append_line(
                            attributes.format('match ipv6 address prefix-list '
                                '{match_prefix_list_v6}'))

                    # iosxe: match tag list <match_tag_list>
                    if attributes.value('match_tag_list'):
                        configurations.append_line(
                            attributes.format('match tag list '
                                '{match_tag_list}'))

                    # iosxe: set origin <set_route_origin>
                    if attributes.value('set_route_origin'):
                        configurations.append_line(
                            attributes.format('set origin '
                                '{set_route_origin.value}'))

                    # iosxe: set local-preference <set_local_pref>
                    if attributes.value('set_local_pref'):
                        configurations.append_line(
                            attributes.format('set local-preference '
                                '{set_local_pref}'))

                    # iosxe: set ip next-hop <set_next_hop>
                    if attributes.value('set_next_hop') or \
                        attributes.value('set_nexthop'):
                        configurations.append_line(
                            attributes.format('set ip next-hop '
                                '{set_next_hop}'))

                    # iosxe: set ipv6 next-hop <set_next_hop_v6>
                    if attributes.value('set_next_hop_v6'):
                        configurations.append_line(
                            attributes.format('set ipv6 next-hop '
                                '{set_next_hop_v6}'))

                    # iosxe: set ip next-hop self
                    if attributes.value('set_next_hop_self'):
                        configurations.append_line(
                            attributes.format('set ip next-hop self'))

                    # iosxe: set metric <set_med>
                    if attributes.value('set_med'):
                        configurations.append_line(
                            attributes.format('set metric '
                                '{set_med}'))

                    # iosxe: set as-path prepend <set_as_path_prepend>
                    # iosxe: set as-path prepend <set_as_path_prepend>*
                    # {set_as_path_prepend_repeat_n}
                    if attributes.value('set_as_path_prepend'):
                        if attributes.value('set_as_path_prepend_n'):
                            configurations.append_line(
                                attributes.format('set as-path prepend '
                                    '{set_as_path_prepend}* '
                                    '{set_as_path_prepend_repeat_n}'))
                        else:
                            configurations.append_line(
                                attributes.format('set as-path prepend '
                                    '{set_as_path_prepend}'))

                    # iosxe: set community <set_community> [no-export]
                    # [no-advertise] [additive]
                    if attributes.value('set_community'):
                        cfg = 'set community'
                        for attribute in attributes.value('set_community'):
                            cfg += ' ' + attribute
                        v1 = attributes.value('set_community_no_export')
                        if v1 is not None:
                            cfg += ' no-export'
                        v2 = attributes.value('set_community_no_advertise')
                        if v2 is not None:
                            cfg += ' no-advertise'
                        v3 = attributes.value('set_community_additive')
                        if v3 is not None:
                            cfg += ' additive'

                        configurations.append_line(cfg)

                    # iosxe: set comm-list <set_community_delete> delete
                    if attributes.value('set_community_delete'):
                        configurations.append_line(
                            attributes.format('set comm-list '
                                '{set_community_delete} delete'))

                    # iosxe: set extcommunity rt <set_ext_community_rt>
                    # [additive]
                    if attributes.value('set_ext_community_rt'):
                        cfg = 'set extcommunity rt'
                        for attribute in attributes.value('set_ext_community_rt'):
                            cfg += ' ' + attribute
                        if attributes.value(
                            'set_ext_community_rt_additive') == True:
                            cfg += ' additive'

                        configurations.append_line(attributes.format(cfg))

                    # iosxe: set extcommunity soo <set_ext_community_soo>
                    if attributes.value('set_ext_community_soo'):
                        configurations.append_line(
                            attributes.format('set extcommunity soo '
                                '{set_ext_community_soo}'))

                    # iosxe: set extcommunity vpn-distinguisher
                    # <set_ext_community_vpn>
                    if attributes.value('set_ext_community_vpn'):
                        configurations.append_line(
                            attributes.format('set extcommunity '
                                'vpn-distinguisher {set_ext_community_vpn}'))

                    # iosxe: set extcomm-list <set_ext_community_delete> delete
                    if attributes.value('set_ext_community_delete'):
                        configurations.append_line(
                            attributes.format('set extcomm-list '
                                '{set_ext_community_delete} delete'))

                    # iosxe: set level <set_level>
                    if attributes.value('set_level'):
                        configurations.append_line(
                            attributes.format('set level {set_level.value}'))

                    # iosxe: set metric-type <set_metric_type>
                    if attributes.value('set_metric_type'):
                        configurations.append_line(
                            attributes.format('set metric-type '
                                '{set_metric_type.value}'))

                    # iosxe: set metric <set_metric>
                    if attributes.value('set_metric'):
                        configurations.append_line(
                            attributes.format('set metric '
                                '{set_metric}'))

                    # iosxe: set metric-type <set_ospf_metric_type>
                    if attributes.value('set_ospf_metric_type'):
                        configurations.append_line(
                            attributes.format('set metric-type '
                                '{set_ospf_metric_type.value}'))

                    # iosxe: set metric <set_ospf_metric>
                    if attributes.value('set_ospf_metric'):
                        configurations.append_line(
                            attributes.format('set metric '
                                '{set_ospf_metric}'))

                    # iosxe: set tag <set_tag>
                    if attributes.value('set_tag'):
                        configurations.append_line(
                            attributes.format('set tag '
                                '{set_tag}'))

                    # iosxe: set weight <set_weight>
                    if attributes.value('set_weight'):
                        configurations.append_line(
                            attributes.format('set weight '
                                '{set_weight}'))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

