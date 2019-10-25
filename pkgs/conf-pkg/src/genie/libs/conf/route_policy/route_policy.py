
__all__ = (
    'RoutePolicy',
)

import operator
import fnmatch

from enum import Enum

from ipaddress import IPv4Address, IPv6Address

from genie.decorator import managedattribute
from genie.conf.base import DeviceFeature, Interface
from genie.conf.base.attributes import SubAttributes, SubAttributesDict,\
    AttributesInheriter, AttributesHelper, KeyedSubAttributes, \
    DeviceSubAttributes

from genie.libs.conf.base import ip_address, ip_network
from genie.libs.conf.community_set import CommunitySet


def _identity(value):
    return value


class RoutePolicyAttributes(object):

    custom_config_cli = managedattribute(
        name='custom_config_cli',
        finit=str,
        type=managedattribute.test_istype(str))

    conditions = managedattribute(
        name='conditions',
        finit=list,
        # Cyclic dependency -- set later
        #type=managedattribute.test_list_of((
        #    managedattribute.test_isinstance(RoutePolicyCondition),
        #)),
    )

    set_label_index = managedattribute(
        name='label_index',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='The "set label-index" option')

    set_community = managedattribute(
        name='set_community',
        default=None,
        type=(None, managedattribute.test_istype(CommunitySet),
              managedattribute.test_istype(list)),
        doc='The "set community" option')

    set_nexthop = managedattribute(
        name='nexthop',
        default=None,
        type=(None, ip_address),
        doc='The "set next-hop" option')

    pass_on = managedattribute(
        name='pass_on',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='The "pass" option: Pass this route for further processing')

    drop_on = managedattribute(
        name='drop_on',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='The "drop" option: Reject this route with no further processing')

    # ==== Statement section ===================
    policy_definition = managedattribute(
        name='policy_definition',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='The route-policy name')

    statement_name = managedattribute(
        name='statement_name',
        default=None,
        type=(None,
              managedattribute.test_istype(str),
              managedattribute.test_istype(int)),
        doc='The route-policy statement name')

    description = managedattribute(
        name='description',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    class ROUTE_DISPOSITION(Enum):
        permit = 'permit'
        deny = 'deny'

    route_disposition = managedattribute(
        name='route_disposition',
        default='permit',
        type=(None, ROUTE_DISPOSITION),
        doc='Route Disposition Enum value')

    match_med_eq = managedattribute(
        name='match_med_eq',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    match_nexthop_in = managedattribute(
        name='match_nexthop_in',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    match_nexthop_in_v6 = managedattribute(
        name='match_nexthop_in_v6',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    match_local_pref_eq = managedattribute(
        name='match_local_pref_eq',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    class MATCH_ROUTE_TYPE(Enum):
        internal = 'internal'
        external = 'external'

    match_route_type = managedattribute(
        name='match_route_type',
        default=None,
        type=(None, MATCH_ROUTE_TYPE))

    match_community_list = managedattribute(
        name='match_community_list',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    match_ext_community_list = managedattribute(
        name='match_ext_community_list',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # ==== XR Specific ===================

    class MATCH_ORIGIN_EQ(Enum):
        igp = 'igp'
        egp = 'egp'
        incomplete = 'incomplete'

    match_origin_eq = managedattribute(
        name='match_origin_eq',
        default=None,
        type=(None, MATCH_ORIGIN_EQ))

    class MATCH_EXT_COMMUNITY_LIST_TYPE(Enum):
        soo = 'soo'
        rt = 'rt'

    match_ext_community_list_type  = managedattribute(
        name='match_ext_community_list_type ',
        default=None,
        type=(None, MATCH_EXT_COMMUNITY_LIST_TYPE))

    match_as_path_length = managedattribute(
        name='match_as_path_length',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    class MATCH_AS_PATH_LENGTH_OPER(Enum):
        eq = 'eq'
        ge = 'ge'
        le = 'le'

    match_as_path_length_oper = managedattribute(
        name='match_as_path_length_oper',
        default=None,
        type=(None, MATCH_AS_PATH_LENGTH_OPER))

    area_eq = managedattribute(
        name='area_eq',
        default=None,
        type=(None, managedattribute.test_istype(int), IPv4Address))

    class SET_EXT_COMMUNITY_DELETE_TYPE(Enum):
        soo = 'soo'
        rt = 'rt'

    set_ext_community_delete_type  = managedattribute(
        name='set_ext_community_delete_type ',
        default=None,
        type=(None, SET_EXT_COMMUNITY_DELETE_TYPE))

    class ACTIONS(Enum):
        rppass = 'pass'
        done = 'done'
        drop = 'drop'

    actions  = managedattribute(
        name='actions',
        default=None,
        type=(None, ACTIONS))

    # =======================

    match_as_path_list = managedattribute(
        name='match_as_path_list',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    class MATCH_LEVEL_EQ(Enum):
        level_1 = 'level-1'
        level_2 = 'level-2'
        level_1_2 = 'level-1-2'

    match_level_eq = managedattribute(
        name='match_level_eq',
        default=None,
        type=(None, MATCH_LEVEL_EQ))

    match_interface = managedattribute(
        name='match_interface',
        default=None,
        type=(None, managedattribute.test_istype(str), Interface))

    match_prefix_list = managedattribute(
        name='match_prefix_list',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    match_prefix_list_v6 = managedattribute(
        name='match_prefix_list_v6',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    match_tag_list = managedattribute(
        name='match_tag_list',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    class SET_ROUTE_ORIGIN(Enum):
        igp = 'igp'
        egp = 'egp'
        incomplete = 'incomplete'

    set_route_origin = managedattribute(
        name='set_route_origin',
        default=None,
        type=(None, SET_ROUTE_ORIGIN))

    set_local_pref = managedattribute(
        name='set_local_pref',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    set_next_hop = managedattribute(
        name='set_next_hop',
        default=None,
        type=(None, managedattribute.test_istype(str), IPv4Address))

    set_next_hop_v6 = managedattribute(
        name='set_next_hop_v6',
        default=None,
        type=(None, managedattribute.test_istype(str), IPv6Address))

    set_next_hop_self = managedattribute(
        name='set_next_hop_self',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    set_med = managedattribute(
        name='set_med',
        default=None,
        type=(None,
              managedattribute.test_istype(int),
              managedattribute.test_istype(str)))

    set_as_path_prepend = managedattribute(
        name='set_as_path_prepend',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    set_as_path_prepend_n = managedattribute(
        name='set_as_path_prepend_n',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    set_community_no_export = managedattribute(
        name='set_community_no_export',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    set_community_no_advertise = managedattribute(
        name='set_community_no_advertise',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    set_community_additive = managedattribute(
        name='set_community_additive',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    set_community_delete = managedattribute(
        name='set_community_delete',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    set_ext_community_rt = managedattribute(
        name='set_ext_community_rt',
        default=None,
        type=(None, managedattribute.test_istype(list)))

    set_ext_community_rt_additive = managedattribute(
        name='set_ext_community_rt_additive',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    set_ext_community_soo = managedattribute(
        name='set_ext_community_soo',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    set_ext_community_soo_additive = managedattribute(
        name='set_ext_community_soo_additive',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    set_ext_community_vpn = managedattribute(
        name='set_ext_community_vpn',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    set_ext_community_vpn_additive = managedattribute(
        name='set_ext_community_vpn_additive',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    set_ext_community_delete = managedattribute(
        name='set_ext_community_delete',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    class SET_LEVEL(Enum):
        level_1 = 'level-1'
        level_2 = 'level-2'
        level_1_2 = 'level-1-2'

    set_level = managedattribute(
        name='set_level',
        default=None,
        type=(None, SET_LEVEL))

    class SET_METRIC_TYPE(Enum):
        internal = 'internal'
        external = 'external'

    set_metric_type = managedattribute(
        name='set_metric_type',
        default=None,
        type=(None, SET_METRIC_TYPE))

    set_metric = managedattribute(
        name='set_metric',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    class SET_OSPF_METRIC_TYPE(Enum):
        type_1 = 'type-1'
        type_2 = 'type-2'

    set_ospf_metric_type = managedattribute(
        name='set_ospf_metric_type',
        default=None,
        type=(None, SET_OSPF_METRIC_TYPE))

    set_ospf_metric = managedattribute(
        name='set_ospf_metric',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    set_tag = managedattribute(
        name='set_tag',
        default=None,
        type=(None, managedattribute.test_istype(int), IPv4Address))

    set_weight = managedattribute(
        name='set_weight',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    def rpl_apply_attributes(self, obj, *, setattr=setattr, getattr=getattr):
        '''Apply RoutePolicyAttributes rules to an object.

        It is best to apply device-specific rules from a RoutePolicy instead::

            rpl.device_attr[device].rpl_apply_attributes(obj, ...)

        Returns:
            True: pass -- explicit
            False: drop
            None: undetermined
        '''
        implicit_pass_on = None
        if self.custom_config_cli:
            setattr(obj, 'custom_config_cli', self.custom_config_cli)
            implicit_pass_on = True
        for cond in self.conditions:
            if cond.rpl_test_condition(obj, getattr=getattr):
                sub_pass_on = cond.if_attr.rpl_apply_attributes(obj,
                    setattr=setattr, getattr=getattr)
                if sub_pass_on is not None:
                    if sub_pass_on:
                        implicit_pass_on = True
                    else:
                        return False
            else:
                sub_pass_on = cond.else_attr.rpl_apply_attributes(obj,
                    setattr=setattr, getattr=getattr)
                if sub_pass_on is not None:
                    if sub_pass_on:
                        implicit_pass_on = True
                    else:
                        return False
        if self.set_nexthop is not None:
            setattr(obj, 'nexthop', self.set_nexthop)
            implicit_pass_on = True
        if self.set_label_index is not None:
            setattr(obj, 'label_index', self.set_label_index)
            implicit_pass_on = True
        if self.set_community is not None:
            setattr(obj, 'community', self.set_community)
            implicit_pass_on = True
        if self.pass_on:
            assert not self.drop_on
            setattr(obj, 'pass', True)
            return True
        elif self.drop_on:
            setattr(obj, 'drop', True)
            return False
        else:
            return implicit_pass_on


class RoutePolicyCondition(object):

    def op_contains(a, vb):
        try:
            vb = ip_address(vb)
        except ValueError:
            pass
        else:
            # b-ip in (a-ip|networks...)
            return any(vb in ip_network(va) for va in a)
        try:
            vb = ip_network(vb)
        except ValueError:
            pass
        else:
            # b-net in (a-ip|networks...)
            return any(vb == ip_network(va) for va in a)
        return vb in a

    def op_matches_any(a, vb):
        if isinstance(a, CommunitySet):
            a = a.communities
        sb = str(vb)
        return any(
            fnmatch.fnmatchcase(sb, a)
            if isinstance(a , str)
            else vb == a)

    op = managedattribute(
        name='op',
        type=managedattribute.test_in((
            op_contains,
            op_matches_any,
        )))

    operands = managedattribute(
        name='operands',
        type=managedattribute.test_tuple_of(_identity))

    if_attr = managedattribute(
        name='if_attr',
        finit=RoutePolicyAttributes,
        type=managedattribute.test_istype(RoutePolicyAttributes))

    else_attr = managedattribute(
        name='else_attr',
        finit=RoutePolicyAttributes,
        type=managedattribute.test_istype(RoutePolicyAttributes))

    def __init__(self, op, *operands):
        self.op = op
        self.operands = operands
        super().__init__()

    def rpl_test_condition(self, obj, *, getattr=getattr):
        if self.op in (
                RoutePolicyCondition.op_contains,
                RoutePolicyCondition.op_matches_any,
        ):
            a, b = self.operands
            return self.op(a, getattr(obj, b))
        else:
            assert NotImplementedError(self.op)

# Cyclic dependency -- set later
RoutePolicyAttributes.conditions = RoutePolicyAttributes.conditions.copy(
    type=managedattribute.test_list_of((
        managedattribute.test_isinstance(RoutePolicyCondition),
    )),
)

class RoutePolicyMixin(DeviceFeature):

    pass


class RoutePolicy(RoutePolicyAttributes, RoutePolicyMixin, DeviceFeature):

    Condition = RoutePolicyCondition

    name = managedattribute(
        name='name',
        type=managedattribute.test_istype(str))

    def rpl_apply_attributes(self, obj, **kwargs):
        '''Apply RoutePolicyAttributes rules to an object.

        It is best to apply device-specific rules using instead::

            rpl.device_attr[device].rpl_apply_attributes(obj, ...)

        Returns:
            True: pass -- implicit or explicit
            False: drop
        '''
        pass_on = super().rpl_apply_attributes(obj, **kwargs)
        return False if pass_on is None else pass_on

    custom_unconfig_cli = managedattribute(
        name='custom_unconfig_cli',
        finit=str,
        type=managedattribute.test_istype(str))

    class DeviceAttributes(DeviceSubAttributes):

        def rpl_apply_attributes(self, obj, **kwargs):
            '''Apply device-specific RoutePolicyAttributes rules to an object.

            Returns:
                True: pass -- implicit or explicit
                False: drop
            '''
            pass_on = RoutePolicyAttributes.rpl_apply_attributes(self, obj, **kwargs)
            return False if pass_on is None else pass_on

        class StatementAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.statement_name = key
                super().__init__(parent)

        statement_attr = managedattribute(
            name='statement_attr',
            read_only=True,
            doc=StatementAttributes.__doc__)

        @statement_attr.initter
        def statement_attr(self):
            return SubAttributesDict(self.StatementAttributes, parent=self)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    def __init__(self, name=None, policy_definition=None, *args, **kwargs):
        if name:
            self.name = name
        if policy_definition:
            self.policy_definition = policy_definition
        # Make sure at least one was populated:
        if not name and not policy_definition:
            raise TypeError("__init__() requires either 'name' or "
                            "'policy_definition' to be provided")
        if 'route_disposition' in kwargs:
            self.route_disposition = kwargs['route_disposition']
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

        cfgs = {key: value for key, value in cfgs.items() if value}
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

        cfgs = {key: value for key, value in cfgs.items() if value}
        if apply:
            self.testbed.config_on_devices(cfgs, fail_invalid=True)
        else:
            return cfgs

