# import python
import unittest
import unittest.mock
from unittest.mock import Mock

# import genie
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Interface
from genie.libs.conf.route_policy import RoutePolicy


class test_route_policy(TestCase):

    def test_basic_cfg(self):

        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxe')

        rpl1 = RoutePolicy(policy_definition='rpl1',
                           route_disposition='permit')
        dev1.add_feature(rpl1)

        rpl1.device_attr[dev1].statement_attr['10']
        rpl1.device_attr[dev1].statement_attr['10'].match_med_eq = 5
        rpl1.device_attr[dev1].statement_attr['10'].description = 'test'
        rpl1.device_attr[dev1].statement_attr['10'].match_nexthop_in = '10'
        rpl1.device_attr[dev1].statement_attr['10'].match_nexthop_in_v6 = '30'
        rpl1.device_attr[dev1].statement_attr['10'].match_local_pref_eq = 40
        rpl1.device_attr[dev1].statement_attr['10'].match_route_type = 'internal'
        rpl1.device_attr[dev1].statement_attr['10'].match_community_list = \
            'community-list1'
        rpl1.device_attr[dev1].statement_attr['10'].match_ext_community_list = \
            'community-list2'
        rpl1.device_attr[dev1].statement_attr['10'].match_as_path_list = \
            '100'
        rpl1.device_attr[dev1].statement_attr['10'].match_level_eq = \
            'level-1-2'
        rpl1.device_attr[dev1].statement_attr['10'].match_interface = \
            'GigabitEthernet3/0/1'
        rpl1.device_attr[dev1].statement_attr['10'].match_prefix_list = \
            'prefixlist1'
        rpl1.device_attr[dev1].statement_attr['10'].match_prefix_list_v6 = \
            'prefixlist1v6'
        rpl1.device_attr[dev1].statement_attr['10'].match_tag_list = \
            'match_tag_list'
        rpl1.device_attr[dev1].statement_attr['10'].set_route_origin = \
            'igp'
        rpl1.device_attr[dev1].statement_attr['10'].set_local_pref = \
            100
        rpl1.device_attr[dev1].statement_attr['10'].set_next_hop = \
            '1.1.1.1'
        rpl1.device_attr[dev1].statement_attr['10'].set_next_hop_v6 = \
            '2001:db8:1::1'
        rpl1.device_attr[dev1].statement_attr['10'].set_next_hop_self = \
            True
        rpl1.device_attr[dev1].statement_attr['10'].set_med = \
            '100'
        rpl1.device_attr[dev1].statement_attr['10'].set_as_path_prepend = \
            '100'
        rpl1.device_attr[dev1].statement_attr['10'].set_as_path_prepend_n = \
            3
        rpl1.device_attr[dev1].statement_attr['10'].set_community = \
            ['100:100', '200:200']
        rpl1.device_attr[dev1].statement_attr['10'].set_community_no_export = \
            True
        rpl1.device_attr[dev1].statement_attr['10'].set_community_no_advertise = \
            True
        rpl1.device_attr[dev1].statement_attr['10'].set_community_additive = \
            True
        rpl1.device_attr[dev1].statement_attr['10'].set_community_delete = \
            'communit_list'
        rpl1.device_attr[dev1].statement_attr['10'].set_ext_community_rt = \
            ['100:10']
        rpl1.device_attr[dev1].statement_attr['10'].set_ext_community_rt_additive = \
            True
        rpl1.device_attr[dev1].statement_attr['10'].set_ext_community_soo = \
            '100:10'
        rpl1.device_attr[dev1].statement_attr['10'].set_ext_community_vpn = \
            '100:10'
        rpl1.device_attr[dev1].statement_attr['10'].set_ext_community_delete = \
            'community_list'
        rpl1.device_attr[dev1].statement_attr['10'].set_level = \
            'level-1'
        rpl1.device_attr[dev1].statement_attr['10'].set_metric_type = \
            'internal'
        rpl1.device_attr[dev1].statement_attr['10'].set_metric = \
            30
        rpl1.device_attr[dev1].statement_attr['10'].set_ospf_metric_type = \
            'type-1'
        rpl1.device_attr[dev1].statement_attr['10'].set_ospf_metric = \
            200
        rpl1.device_attr[dev1].statement_attr['10'].set_tag = \
            111
        rpl1.device_attr[dev1].statement_attr['10'].set_weight = \
            100

        self.maxDiff = None
        cfgs = rpl1.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['route-map rpl1 permit 10',
             ' description test',
             ' match metric 5',
             ' match ip next-hop prefix-list 10',
             ' match ipv6 next-hop prefix-list 30',
             ' match local-preference 40',
             ' match route-type internal',
             ' match community community-list1',
             ' match extcommunity community-list2',
             ' match as-path 100',
             ' match route-type level-1',
             ' match route-type level-2',
             ' match interface GigabitEthernet3/0/1',
             ' match ip address prefix-list prefixlist1',
             ' match ipv6 address prefix-list prefixlist1v6',
             ' match tag list match_tag_list',
             ' set origin igp',
             ' set local-preference 100',
             ' set ip next-hop 1.1.1.1',
             ' set ipv6 next-hop 2001:db8:1::1',
             ' set ip next-hop self',
             ' set metric 100',
             " set community 100:100 200:200 no-export no-advertise additive",
             ' set comm-list communit_list delete',
             " set extcommunity rt 100:10 additive",
             ' set extcommunity soo 100:10',
             ' set extcommunity vpn-distinguisher 100:10',
             ' set extcomm-list community_list delete',
             ' set level level-1',
             ' set metric-type internal',
             ' set metric 30',
             ' set metric-type type-1',
             ' set metric 200',
             ' set tag 111',
             ' set weight 100',
             ' exit'
            ]))

        rpl2 = RoutePolicy(policy_definition='rpl2',
                           route_disposition='deny')
        dev2.add_feature(rpl2)

        rpl2.device_attr[dev2].statement_attr['20']
        rpl2.device_attr[dev2].statement_attr['20'].set_metric_type = \
            'internal'

        cfgs = rpl2.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev2.name])
        self.assertMultiLineEqual(str(cfgs[dev2.name]), '\n'.join(
            ['route-map rpl2 deny 20',
             ' set metric-type internal',
             ' exit'
            ]))

        uncfg1 = rpl1.build_unconfig(apply=False)
        self.assertCountEqual(uncfg1.keys(), [dev1.name])
        self.assertMultiLineEqual(
            str(uncfg1[dev1.name]),
            '\n'.join([
                'no route-map rpl1 permit 10'
            ]))

        partial_uncfg1 = rpl1.build_unconfig(
                            apply=False,
                            attributes={'device_attr':{'*':{'statement_attr':\
                                       {'*':"match_med_eq"}}}})

        self.assertCountEqual(partial_uncfg1.keys(), [dev1.name])
        self.assertMultiLineEqual(
            str(partial_uncfg1[dev1.name]),
            '\n'.join([
                'route-map rpl1 permit 10',
                ' no match metric 5',
                ' exit'
            ]))


if __name__ == '__main__':
    unittest.main()

