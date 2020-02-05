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
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')
        intf1 = Interface(device=dev1, name='Ethernet0/0/1',
                          ipv4='10.1.0.1/24')
        intf2 = Interface(device=dev1, name='Ethernet0/0/2',
                          ipv4='10.2.0.1/24')
        dev2 = Device(testbed=testbed, name='PE2', os='nxos')
        intf3 = Interface(device=dev2, name='Ethernet0/0/3',
                          ipv4='10.1.0.2/24', ipv6='2001:111:222::/64')
        intf4 = Interface(device=dev2, name='Ethernet0/0/4',
                          ipv4='10.2.0.2/24')

        rpl1 = RoutePolicy(policy_definition='rpl1',
                           route_disposition='permit')
        dev1.add_feature(rpl1)

        rpl1.device_attr[dev1].statement_attr['10']
        rpl1.device_attr[dev1].statement_attr['10'].match_med_eq = 5

        cfgs = rpl1.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['route-map rpl1 permit 10',
             ' match metric 5',
             ' exit'
            ]))

        rpl2 = RoutePolicy(policy_definition='rpl2',
                           route_disposition='deny')
        dev2.add_feature(rpl2)

        rpl2.device_attr[dev2].statement_attr['20']
        rpl2.device_attr[dev2].statement_attr['20'].set_metric_type = \
            'internal'
        rpl2.device_attr[dev2].statement_attr['20'].set_ext_community_rt = \
            ['100:100','200:200']
        rpl2.device_attr[dev2].statement_attr['20'].\
            set_ext_community_rt_additive = True

        cfgs = rpl2.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev2.name])
        self.assertMultiLineEqual(str(cfgs[dev2.name]), '\n'.join(
            ["route-map rpl2 deny 20",
             " set extcommunity rt ['100:100', '200:200'] additive",
             " set metric-type internal",
             " exit"
            ]))

    def test_basic_uncfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')
        dev2 = Device(testbed=testbed, name='PE2', os='nxos')

        rpl1 = RoutePolicy(policy_definition='rpl1',
                           route_disposition='permit')
        dev1.add_feature(rpl1)

        rpl1.device_attr[dev1].statement_attr['10']
        rpl1.device_attr[dev1].statement_attr['10'].match_med_eq = 5

        # Unconfig testing
        # Set a mock
        dev1.configure = Mock()
        dev1.add_feature(rpl1)
        # Mock config

        uncfg1 = rpl1.build_unconfig(apply=False)
        self.assertCountEqual(uncfg1.keys(), ['PE1'])
        self.assertMultiLineEqual(
            str(uncfg1['PE1']),
            '\n'.join([
                'no route-map rpl1 permit 10'
            ]))

        partial_uncfg1 = rpl1.build_unconfig(
                            apply=False,
                            attributes={'device_attr':{'*':{'statement_attr':\
                                       {'*':"match_med_eq"}}}})

        self.assertCountEqual(partial_uncfg1.keys(), ['PE1'])
        self.assertMultiLineEqual(
            str(partial_uncfg1['PE1']),
            '\n'.join([
                'route-map rpl1 permit 10',
                ' no match metric 5',
                ' exit'
            ]))

if __name__ == '__main__':
    unittest.main()

