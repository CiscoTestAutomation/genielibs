# import python
import operator
import unittest
import unittest.mock
from unittest.mock import Mock

# import genie
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Interface
from genie.libs.conf.route_policy import RoutePolicy


class test_route_policy(TestCase):

    def test_init(self):

        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/0/1',
            ipv4='10.1.0.1/24')
        intf2 = Interface(device=dev1, name='GigabitEthernet0/0/0/2',
            ipv4='10.2.0.1/24')
        intf3 = Interface(device=dev1, name='GigabitEthernet0/0/0/3',
            ipv4='10.3.0.1/24')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxr')
        intf4 = Interface(device=dev2, name='GigabitEthernet0/0/0/3',
            ipv4='10.1.0.2/24')
        intf5 = Interface(device=dev2, name='GigabitEthernet0/0/0/4',
            ipv4='10.2.0.2/24')

        with self.assertNoWarnings():

            rpl1 = RoutePolicy(name='rpl1')
            dev1.add_feature(rpl1)

            rpl1.pass_on = True

            cfgs = rpl1.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev1.name])
            self.assertMultiLineDictEqual(cfgs, {
                dev1.name: '\n'.join([
                    'route-policy rpl1',
                    ' pass',
                    ' end-policy',
                ]),
            })

            rpl1 = RoutePolicy(name='rpl1')
            dev1.add_feature(rpl1)

            rpl1.conditions = []
            cond = RoutePolicy.Condition(
                RoutePolicy.Condition.op_contains,
                (intf1.ipv4.ip, intf2.ipv4.network),
                'destination')
            cond.if_attr.set_nexthop = intf3.ipv4.ip
            cond.else_attr.drop_on = True
            rpl1.conditions.append(cond)

            cfgs = rpl1.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev1.name])
            self.assertMultiLineDictEqual(cfgs, {
                dev1.name: '\n'.join([
                    'route-policy rpl1',
                    ' if destination in (10.1.0.1, 10.2.0.0/24) then',
                    '  set next-hop 10.3.0.1',
                    ' else',
                    '  drop',
                    ' endif',
                    ' end-policy',
                ]),
            })

            class A(object):
                def __repr__(self):
                    return '<a>'
                def __init__(self):
                    self.rpl_set = Mock(side_effect=setattr)
                    self.rpl_get = Mock(side_effect=getattr)

            a = A()
            a.destination = intf5.ipv4.ip
            pass_on = rpl1.rpl_apply_attributes(a, setattr=a.rpl_set,
                getattr=a.rpl_get)
            self.assertEqual(a.rpl_get.call_args_list, [
                unittest.mock.call(a, 'destination'),
            ])
            self.assertEqual(a.rpl_set.call_args_list, [
                unittest.mock.call(a, 'nexthop', intf3.ipv4.ip),
            ])
            self.assertIs(pass_on, True)

            a = A()
            a.destination = intf4.ipv4.ip
            pass_on = rpl1.rpl_apply_attributes(a, setattr=a.rpl_set,
                getattr=a.rpl_get)
            self.assertEqual(a.rpl_get.call_args_list, [
                unittest.mock.call(a, 'destination'),
            ])
            self.assertEqual(a.rpl_set.call_args_list, [
                unittest.mock.call(a, 'drop', True),
            ])
            self.assertIs(pass_on, False)

            del cond.else_attr.drop_on
            cfgs = rpl1.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev1.name])
            self.assertMultiLineDictEqual(cfgs, {
                dev1.name: '\n'.join([
                    'route-policy rpl1',
                    ' if destination in (10.1.0.1, 10.2.0.0/24) then',
                    '  set next-hop 10.3.0.1',
                    ' endif',
                    ' end-policy',
                ]),
            })

            a = A()
            a.destination = intf4.ipv4.ip
            pass_on = rpl1.rpl_apply_attributes(a, setattr=a.rpl_set,
                getattr=a.rpl_get)
            self.assertEqual(a.rpl_get.call_args_list, [
                unittest.mock.call(a, 'destination'),
            ])
            self.assertEqual(a.rpl_set.call_args_list, [
            ])
            self.assertIs(pass_on, False)

    def test_basic_uncfg_with_name(self):
        '''
            Testing in case of having 'name' as the route-policy name.
        '''

        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')

        rpl1 = RoutePolicy(name='rpl1')
        dev1.add_feature(rpl1)

        rpl1.device_attr[dev1].statement_attr['10']
        rpl1.device_attr[dev1].statement_attr['10'].match_med_eq = 5
        rpl1.device_attr[dev1].statement_attr['10'].match_nexthop_in = 'hop'
        rpl1.device_attr[dev1].statement_attr['10'].actions = 'pass'

        # Unconfig testing
        # Set a mock
        dev1.configure = Mock()
        dev1.add_feature(rpl1)
        # Mock config

        uncfg1 = rpl1.build_unconfig(apply=False)
        self.assertCountEqual(uncfg1.keys(), ['PE1'])
        self.assertMultiLineEqual(str(uncfg1['PE1']), '\n'.join(
            ['no route-policy rpl1'
            ]))

    def test_basic_cfg(self):

        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxr')

        rpl1 = RoutePolicy(policy_definition='rpl1')
        dev1.add_feature(rpl1)

        rpl1.device_attr[dev1].statement_attr[10]
        rpl1.device_attr[dev1].statement_attr[10].match_med_eq = 5
        rpl1.device_attr[dev1].statement_attr[10].match_nexthop_in = 'hop'
        rpl1.device_attr[dev1].statement_attr[10].actions = 'pass'

        rpl1.device_attr[dev1].statement_attr[20]
        rpl1.device_attr[dev1].statement_attr[20].match_med_eq = 10
        rpl1.device_attr[dev1].statement_attr[20].match_nexthop_in = 'hop2'
        rpl1.device_attr[dev1].statement_attr[20].match_local_pref_eq = 16
        rpl1.device_attr[dev1].statement_attr[20].actions = 'drop'

        rpl1.device_attr[dev1].statement_attr[30]
        rpl1.device_attr[dev1].statement_attr[30].match_med_eq = 20
        rpl1.device_attr[dev1].statement_attr[30].match_nexthop_in = 'hop3'
        rpl1.device_attr[dev1].statement_attr[30].actions = 'done'
        rpl1.device_attr[dev1].statement_attr[30].set_med = 32

        cfgs = rpl1.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['route-policy rpl1',
             ' if med eq 5 and next-hop in hop then',
             '  # 10',
             '  pass',
             ' elseif local-preference eq 16 and med eq 10 and next-hop in hop2 then',
             '  # 20',
             '  drop',
             ' elseif med eq 20 and next-hop in hop3 then',
             '  # 30',
             '  set med 32',
             '  done',
             ' endif',
             ' end-policy',
             ' exit'
            ]))

        # Testing the configuration without if/else statements
        # ----------------------------------------------------
        rpl2 = RoutePolicy(policy_definition='rpl2')
        dev2.add_feature(rpl2)

        rpl2.device_attr[dev2].statement_attr['10']
        rpl2.device_attr[dev2].statement_attr['10'].actions = 'pass'
        rpl2.device_attr[dev2].statement_attr['10'].set_med = 32


        cfgs2 = rpl2.build_config(apply=False)
        self.assertCountEqual(cfgs2.keys(), [dev2.name])
        self.assertMultiLineEqual(str(cfgs2[dev2.name]), '\n'.join(
            ['route-policy rpl2',
             ' # 10',
             ' set med 32',
             ' pass',
             ' end-policy',
             ' exit'
            ]))

    def test_basic_uncfg(self):

        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')

        rpl1 = RoutePolicy(policy_definition='rpl1')
        dev1.add_feature(rpl1)

        rpl1.device_attr[dev1].statement_attr['10']
        rpl1.device_attr[dev1].statement_attr['10'].match_med_eq = 5
        rpl1.device_attr[dev1].statement_attr['10'].match_nexthop_in = 'hop'
        rpl1.device_attr[dev1].statement_attr['10'].actions = 'pass'

        # Unconfig testing
        # Set a mock
        dev1.configure = Mock()
        dev1.add_feature(rpl1)
        # Mock config

        uncfg1 = rpl1.build_unconfig(apply=False)
        self.assertCountEqual(uncfg1.keys(), ['PE1'])
        self.assertMultiLineEqual(str(uncfg1['PE1']), '\n'.join(
            ['no route-policy rpl1'
            ]))

if __name__ == '__main__':
    unittest.main()

