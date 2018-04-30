"""Implement IOS-XR (iosxr) Specific Configurations for RoutePolicy objects.
"""

# Structure Hierarchy:
# +--Class RoutePolicy:
#         +--Class DeviceAttributes
#                +--Class StatementAttributes

# import python
import operator
import warnings
from abc import ABC

# import genie
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig
from genie.libs.conf.community_set import CommunitySet

# import route_policy
from ..route_policy import RoutePolicyCondition


class UnsupportedSelectiveRoutePolicyConfig(UserWarning):
    '''Warning class for Unsupported Selective RoutePolicy Configuration.'''
    pass


def _build_condition_string(base, cond, attributes):

    if cond.op is RoutePolicyCondition.op_contains:
        a, b = cond.operands
        return '{} in ({})'.format(
            b,
            ', '.join('{}'.format(va) for va in a),
        )

    elif cond.op is RoutePolicyCondition.op_matches_any:
        a, b = cond.operands
        if isinstance(a, CommunitySet):
            return '{} matches-any {}'.format(
                b,
                a.name,
            )
        else:
            return '{} matches-any ({})'.format(
                b,
                ', '.join('{}'.format(va) for va in a),
            )

    else:
        raise NotImplementedError(cond.op)


def _build_condition_cli(base, cond, attributes):
    configurations = CliConfigBuilder()

    str = _build_condition_string(base, cond, attributes=attributes)
    assert str

    with configurations.submode_context('if {} then'.format(str), exit_cmd=None):
        if_attr, attributes2 = attributes.namespace('if_attr')
        configurations.append_block(_build_attributes_cli(base, if_attr, attributes=attributes2))
        if not configurations:
            configurations.append_line('done')

    with configurations.submode_context('else', cancel_empty=True, exit_cmd=None):
        else_attr, attributes2 = attributes.namespace('else_attr')
        configurations.append_block(_build_attributes_cli(base, else_attr, attributes=attributes2))

    configurations.append_line('endif')

    return configurations


def _build_attributes_cli(base, attrobj, attributes):
    configurations = CliConfigBuilder()

    for cond, attributes2 in attributes.sequence_values('conditions'):
        configurations.append_block(_build_condition_cli(base, cond, attributes=attributes2))

    configurations.append_block(
        attributes.format('{custom_config_cli}'))

    # iosxr: route-policy <rtepol> / set label-index ...
    configurations.append_line(attributes.format('set label-index {set_label_index}'))

    # iosxr: route-policy <rtepol> / set community ...
    v = attributes.value('set_community')
    if v is not None:
        if isinstance(v, CommunitySet):
            v = v.name
        configurations.append_line('set community {}'.format(v))

    # iosxr: route-policy <rtepol> / set next-hop ...
    configurations.append_line(attributes.format('set next-hop {set_nexthop}'))

    # iosxr: route-policy <rtepol> / pass
    if attributes.value('pass_on'):
        configurations.append_line('pass')

    # iosxr: route-policy <rtepol> / drop
    if attributes.value('drop_on'):
        configurations.append_line('drop')

    return configurations


class RoutePolicy(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
            **kwargs):
            '''IOS-XR RoutePolicy configuration.

            Note:
                Selective configuration is not supported on IOS-XR; The whole
                route-policy is always removed and re-configured.
            '''
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            if not attributes.iswildcard:
                warnings.warn(UnsupportedSelectiveRoutePolicyConfig,
                              'IOS-XR does not support selective route-policy'
                              ' configuration.')
                attributes = AttributesHelper(self)
            configurations = CliConfigBuilder()

            # First remove any existing to avoid CLI warnings
            if False:
                # Actually, a commit is needed to avoid the warning, so don't even bother!
                configurations.append_line(attributes.format(
                    'no route-policy {name}', force=True))

            # iosxr: route-policy <rtepol> (config-rpl)
            with configurations.submode_context(
                    attributes.format('route-policy {name}', force=True),
                    exit_cmd='end-policy'):

                configurations.append_block(_build_attributes_cli(self,
                                                                  self,
                                                                  attributes))

            # Initializing variables 
            need_end_if = False
            need_elseif = False

            for sub, attributes2 in attributes.mapping_values(
                'statement_attr', keys=self.statement_attr, sort=True):
                    if not unconfig:
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig,
                                             need_elseif=need_elseif,
                                             exit_cmd=None,
                                             **kwargs))

                        # Checking if 'if' or 'elseif' will be added to the
                        # config
                        if len(self.statement_attr) >1:
                            need_elseif = True

                        # Means configuartion contains if/else statmenets
                        if sub.conditional_keys:
                            need_end_if = True

                    # Case of unconfig is handled seperately as in XR we can't
                    # unconfig attributes. The whole route-policy need to be
                    # unconfigured.
                    else:
                        configurations.append_block(
                            sub.build_unconfig(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig,
                                             need_elseif=need_elseif,
                                             exit_cmd=None,
                                             **kwargs))

            if self.policy_definition and not unconfig:
                # Case of if/else statements
                if need_end_if:
                    configurations.append_line(attributes.format(' endif'))
                configurations.append_line(attributes.format(' end-policy'))
                configurations.append_line(attributes.format(' exit'))

            if apply:
                if configurations:
                    self.device.configure(configurations, fail_invalid=True)
            else:
                return CliConfig(device=self.device, unconfig=False,
                                 cli_config=configurations)

        def build_unconfig(self, apply=True, attributes=None, unconfig=True,
            **kwargs):
            '''IOS-XR RoutePolicy unconfiguration.

            Note:
                Selective unconfiguration is not supported on IOS-XR; The whole
                route-policy is always removed.
            '''

            try:
                self.name
                # Sebastien's block of code
                # -------------------------
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                if not attributes.iswildcard:
                    warnings.warn(UnsupportedSelectiveRoutePolicyConfig,
                                  'IOS-XR does not support selective'
                                  '  route-policy unconfiguration.')
                    attributes = AttributesHelper(self)
                configurations = CliConfigBuilder()

                configurations.append_line(attributes.format(
                    'no route-policy {name}', force=True))

                if apply:
                    if configurations:
                        self.device.configure(configurations,
                            fail_invalid=True)
                else:
                    return CliConfig(device=self.device, unconfig=True,
                                     cli_config=configurations,
                                     fail_invalid=True)
            except AttributeError:
                return self.build_config(apply=apply, attributes=attributes,
                                     unconfig=True, **kwargs)

        class StatementAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             need_elseif=False, exit_cmd=None, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                self.conditional_keys = {}

                def config_assembly(self, need_elseif=False,
                    unconfig=False, indent_count=0, **kwargs):

                        new_configurations = \
                            CliConfigBuilder(unconfig=unconfig)

                        # iosxr: if/elif med eq <match_med_eq>
                        if attributes.value('match_med_eq'):
                            self.conditional_keys['match_med_eq'] = \
                                attributes.format('med eq {match_med_eq}')

                        # iosxr: if/elif origin is <match_origin_eq>
                        if attributes.value('match_origin_eq'):
                            self.conditional_keys['match_origin_eq'] = \
                                attributes.format('origin is '
                                    '{match_origin_eq.value}')

                        # iosxr: if/elif nexthop in <match_nexthop_in>
                        if attributes.value('match_nexthop_in'):
                            self.conditional_keys['match_nexthop_in'] = \
                                attributes.format(
                                    'next-hop in {match_nexthop_in}')

                        # iosxr: if/elif nexthop in <match_nexthop_in_v6>
                        if attributes.value('match_nexthop_in_v6'):
                            self.conditional_keys['match_nexthop_in_v6'] = \
                                attributes.format('next-hop in '
                                    '{match_nexthop_in_v6}')

                        # iosxr: if/elif local-preference eq
                        # <match_local_pref_eq>
                        if attributes.value('match_local_pref_eq'):
                            self.conditional_keys['match_local_pref_eq'] = \
                                attributes.format('local-preference eq '
                                    '{match_local_pref_eq}')

                        # iosxr: if/elif community matches-any
                        # <match_community_list>
                        if attributes.value('match_community_list'):
                            self.conditional_keys['match_community_list'] = \
                                attributes.format('community matches-any '
                                    '{match_community_list}')

                        # iosxr: if/elif extcommunity
                        # <match_ext_community_list_type>
                        # matches-any <match_ext_community_list>
                        if attributes.value('match_ext_community_list') and \
                            attributes.value('match_ext_community_list_type'):
                            self.conditional_keys['match_ext_community_list'] = \
                                attributes.format('extcommunity '
                                    '{match_ext_community_list_type.value} '
                                    'matches-any {match_ext_community_list}')

                        # iosxr: if/elif as-path in <match_as_path_list>
                        if attributes.value('match_as_path_list'):
                            self.conditional_keys['match_as_path_list'] = \
                                attributes.format('as-path in '
                                    '{match_as_path_list}')

                        # iosxr: if/elif as-path length
                        # <match_as_path_length_oper> <match_as_path_length>
                        if attributes.value('match_as_path_length_oper') and \
                            attributes.value('match_as_path_length'):
                            self.conditional_keys['match_as_path_length'] = \
                                attributes.format('as-path length '
                                    '{match_as_path_length_oper.value} '
                                    '{match_as_path_length}')

                        # iosxr: if/elif route-type is <match_level_eq>
                        if attributes.value('match_level_eq'):
                            if 'level_1_2' in attributes.value(
                                'match_level_eq'):
                                self.conditional_keys['match_level_eq'] = \
                                    attributes.format(
                                        'route-type is interarea')
                            else:
                                self.conditional_keys['match_level_eq'] = \
                                    attributes.format('route-type is '
                                        '{match_level_eq.value}')

                        # iosxr: if/elif ospf-area is <area_eq>
                        if attributes.value('area_eq'):
                            self.conditional_keys['area_eq'] = \
                                attributes.format('ospf-area is '
                                    '{area_eq}')

                        # iosxr: if/elif destination in <match_prefix_list>
                        if attributes.value('match_prefix_list'):
                            self.conditional_keys['match_prefix_list'] = \
                                attributes.format('destination in '
                                    '{match_prefix_list}')

                        # iosxr: if/elif destination in <match_prefix_list_v6>
                        if attributes.value('match_prefix_list_v6'):
                            self.conditional_keys['match_prefix_list_v6'] = \
                                attributes.format('destination in '
                                    '{match_prefix_list_v6}')

                        # iosxr: if/elif tag in <match_tag_list>
                        if attributes.value('match_tag_list'):
                            self.conditional_keys['match_tag_list'] = \
                                attributes.format('tag in '
                                    '{match_tag_list}')

                        ## Here we construct the config line
                        if self.conditional_keys:
                            if need_elseif:
                                conditional_cfg = attributes.format(' elseif',
                                    force=True)
                            else:
                                conditional_cfg = attributes.format('if',
                                    force=True)
                            for index, key in enumerate(
                                sorted(self.conditional_keys.keys())):
                                conditional_cfg += ' {}'.format(
                                    self.conditional_keys[key])
                                if index < (len(self.conditional_keys)-1):
                                    conditional_cfg += ' and'
                                else:
                                    conditional_cfg += ' then'

                            new_configurations.append_line(conditional_cfg)
                        else:
                            # No spaces should preceed the configuration
                            # if there is no if/else statements
                            indent_count = 0

                        # Counting the spaces to preceed the configuration
                        # as per the if/else state.
                        spaces = ' ' * indent_count

                        # iosxr: # <statement_name>
                        if attributes.value('statement_name'):
                            new_configurations.append_line(
                                attributes.format(spaces+'# {statement_name}'))

                        # iosxr: # <description>
                        if attributes.value('description'):
                            new_configurations.append_line(
                                attributes.format(spaces+'# {description}'))

                        # iosxr: set origin <set_route_origin>
                        if attributes.value('set_route_origin'):
                            new_configurations.append_line(
                                attributes.format(spaces+'set origin '
                                    '{set_route_origin}'))

                        # iosxr: set local-preference <set_local_pref>
                        if attributes.value('set_local_pref'):
                            new_configurations.append_line(
                                attributes.format(
                                    spaces+'set local-preference '
                                    '{set_local_pref}'))

                        # iosxr: set next-hop <set_next_hop>
                        if attributes.value('set_next_hop') or \
                            attributes.value('set_nexthop'):
                            new_configurations.append_line(
                                attributes.format(spaces+'set next-hop '
                                    '{set_next_hop}'))

                        # iosxr: set next-hop <set_next_hop_v6>
                        if attributes.value('set_next_hop_v6'):
                            new_configurations.append_line(
                                attributes.format(spaces+'set next-hop '
                                    '{set_next_hop_v6}'))

                        # iosxr: set next-hop self
                        if attributes.value('set_next_hop_self'):
                            new_configurations.append_line(
                                attributes.format(spaces+'set next-hop self'))

                        # iosxr: set med <set_med>
                        if attributes.value('set_med'):
                            new_configurations.append_line(
                                attributes.format(spaces+'set med {set_med}'))

                        # iosxr: prepend as-path <set_as_path_prepend>
                        # <set_as_path_prepend_repeat_n>
                        if attributes.value('set_as_path_prepend') and \
                            attributes.value('set_as_path_prepend_repeat_n'):
                            new_configurations.append_line(
                                attributes.format(spaces+'prepend as-path '
                                    '{set_as_path_prepend} '
                                    '{set_as_path_prepend_repeat_n}'))

                        # iosxr: set community (<set_community>, no-export,
                        # no-advertise) additive
                        if attributes.value('set_community'):
                            cfg = attributes.format(spaces+'set community '
                                '({set_community}', force=True)
                            v1 = attributes.value('set_community_no_export')
                            if v1 is not None:
                                cfg += ' ,no-export'
                            v2 = attributes.value('set_community_no_advertise')
                            if v2 is not None:
                                cfg += ' ,no-advertise'
                            cfg += ')'
                            v3 = attributes.value('set_community_additive')
                            if v3 is not None:
                                cfg += ' additive'

                            new_configurations.append_line(cfg)

                        # iosxr: delete community in <set_community_delete>
                        if attributes.value('set_community_delete'):
                            new_configurations.append_line(
                                attributes.format(spaces+'delete community in '
                                    '{set_community_delete}'))

                        # iosxr: set extcommunity rt (<set_ext_community_rt>)
                        # [additive]
                        if attributes.value('set_ext_community_rt'):
                            if attributes.value(
                                'set_ext_community_rt_additive'):
                                new_configurations.append_line(
                                    attributes.format(
                                        spaces+'set extcommunity rt '
                                        '({set_ext_community_rt}) additive'))
                            else:
                                new_configurations.append_line(
                                    attributes.format(
                                        spaces+'set extcommunity rt '
                                        '({set_ext_community_rt})'))

                        # iosxr: set extcommunity soo (<set_ext_community_soo>)
                        # [additive]
                        if attributes.value('set_ext_community_soo'):
                            if attributes.value(
                                'set_ext_community_soo_additive'):
                                new_configurations.append_line(
                                    attributes.format(
                                        spaces+'set extcommunity soo '
                                        '({set_ext_community_soo}) additive'))
                            else:
                                new_configurations.append_line(
                                    attributes.format(
                                        spaces+'set extcommunity soo '
                                        '({set_ext_community_soo})'))

                        # iosxr: set extcommunity vpn (<set_ext_community_vpn>)
                        # [additive]
                        if attributes.value('set_ext_community_vpn'):
                            if attributes.value(
                                'set_ext_community_vpn_additive'):
                                new_configurations.append_line(
                                    attributes.format(
                                        spaces+'set extcommunity vpn '
                                        '({set_ext_community_vpn}) additive'))
                            else:
                                new_configurations.append_line(
                                    attributes.format(
                                        spaces+'set extcommunity vpn '
                                        '({set_ext_community_vpn})'))

                        # iosxr: delete extcommunity
                        # <set_ext_community_delete_type>
                        # <set_ext_community_delete>
                        if attributes.value('set_community_delete') and \
                            attributes.value('set_ext_community_delete_type'):
                            new_configurations.append_line(
                                attributes.format(spaces+'delete extcommunity '
                                    '{set_ext_community_delete_type.value} '
                                    '{set_community_delete}'))

                        # iosxr: set level <set_level>
                        if attributes.value('set_level'):
                            new_configurations.append_line(
                                attributes.format(spaces+'set level '
                                    '{set_level}'))

                        # iosxr: set metric-type <set_metric_type>
                        if attributes.value('set_metric_type'):
                            new_configurations.append_line(
                                attributes.format(spaces+'set metric-type '
                                    '{set_metric_type}'))

                        # iosxr: set isis-metric <set_metric>
                        if attributes.value('set_metric'):
                            new_configurations.append_line(
                                attributes.format(spaces+'set isis-metric '
                                    '{set_metric}'))

                        # iosxr: set metric-type <set_ospf_metric_type>
                        if attributes.value('set_ospf_metric_type'):
                            new_configurations.append_line(
                                attributes.format(spaces+'set metric-type '
                                    '{set_ospf_metric_type}'))

                        # iosxr: set ospf-metric <set_ospf_metric>
                        if attributes.value('set_ospf_metric'):
                            new_configurations.append_line(
                                attributes.format(spaces+'set ospf-metric '
                                    '{set_ospf_metric}'))

                        # iosxr: set tag <set_tag>
                        if attributes.value('set_tag'):
                            new_configurations.append_line(
                                attributes.format(spaces+'set tag '
                                    '{set_tag}'))

                        # iosxr: set weight <set_weight>
                        if attributes.value('set_weight'):
                            new_configurations.append_line(
                                attributes.format(spaces+'set weight '
                                    '{set_weight}'))

                        # iosxr: pass|done|drop
                        if attributes.value('actions'):
                            new_configurations.append_line(
                                attributes.format(spaces+'{actions.value}'))

                        return str(new_configurations)

                if need_elseif:
                    configurations.append_block(config_assembly(self,
                        need_elseif=need_elseif, unconfig=unconfig,
                        indent_count=2))
                else:
                    with configurations.submode_context(
                        attributes.format('route-policy {policy_definition}',
                            force=True), exit_cmd=None):
                            if unconfig and attributes.iswildcard:
                                # Never reached!
                                configurations.submode_unconfig()

                            configurations.append_block(config_assembly(self,
                                need_elseif=need_elseif, unconfig=unconfig,
                                indent_count=1))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):

                configurations = CliConfigBuilder()
                configurations.append_line(attributes.format(
                    'no route-policy {policy_definition}', force=True))

                return str(configurations)

