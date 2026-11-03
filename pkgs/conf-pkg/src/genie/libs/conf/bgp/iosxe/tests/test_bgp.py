#!/usr/bin/env python

# import python
import unittest

# import genie
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Interface

# import genie.libs
from genie.libs.conf.bgp import Bgp
from genie.libs.conf.vrf import Vrf


class test_bgp(TestCase):

    # Old code test
    def test_init(self):

        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/1',
            ipv4='10.1.0.1/24')
        intf2 = Interface(device=dev1, name='GigabitEthernet0/0/2',
            ipv4='10.2.0.1/24')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxe')
        intf3 = Interface(device=dev2, name='GigabitEthernet0/0/3',
            ipv4='10.1.0.2/24')
        intf4 = Interface(device=dev2, name='GigabitEthernet0/0/4',
            ipv4='10.2.0.2/24')
        vrf1 = Vrf(name='vrf1')
        vrf2 = Vrf(name='a')

        with self.assertNoWarnings():

            bgp = Bgp(asn=100)
            self.assertIs(bgp.testbed, testbed)
            Genie.testbed = testbed
            bgp = Bgp(asn=100)
            self.assertIs(bgp.testbed, Genie.testbed)
            self.assertIs(bgp.testbed, testbed)

            dev1.add_feature(bgp)

            cfgs = bgp.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                'router bgp 100',
                ' address-family ipv4 unicast',
                '  exit',
                ' exit',
                    ]))

            dev2.add_feature(bgp)

            cfgs = bgp.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev1.name, dev2.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                'router bgp 100',
                ' address-family ipv4 unicast',
                '  exit',
                ' exit',
                    ]))
            self.assertMultiLineEqual(str(cfgs[dev2.name]), '\n'.join([
                'router bgp 100',
                ' address-family ipv4 unicast',
                '  exit',
                ' exit',
                    ]))

            bgp.device_attr[dev1].add_neighbor(intf3.ipv4)
            bgp.device_attr[dev1].add_vrf(vrf1)
            bgp.device_attr[dev1].vrf_attr[vrf1].add_neighbor(intf4.ipv4)
            bgp.device_attr[dev1].vrf_attr[vrf1].neighbor_attr[intf4.ipv4].\
                address_family_attr['ipv4 unicast'].activate = True
            bgp.device_attr[dev1].add_vrf(vrf2)

            cfgs = bgp.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev1.name, dev2.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                'router bgp 100',
                ' neighbor 10.1.0.2 remote-as 100',
                ' address-family ipv4 unicast',
                '  exit',
                ' address-family ipv4 unicast vrf a',
                '  exit',
                ' neighbor 10.2.0.2 remote-as 100',
                ' address-family ipv4 unicast vrf vrf1',
                '  neighbor 10.2.0.2 activate',
                '  exit',
                ' address-family ipv4 unicast vrf vrf1',
                '  exit',
                ' exit',
                    ]))
            self.assertMultiLineEqual(str(cfgs[dev2.name]), '\n'.join([
                'router bgp 100',
                ' address-family ipv4 unicast',
                '  exit',
                ' exit',
                    ]))

            cfgs = bgp.build_config(apply=False,
                attributes='device_attr__PE1__vrf_attr__default')
            self.assertCountEqual(cfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                'router bgp 100',
                ' neighbor 10.1.0.2 remote-as 100',
                ' address-family ipv4 unicast',
                '  exit',
                ' exit',
                    ]))

            cfgs = bgp.build_config(apply=False, attributes={
                'device_attr': {
                    '*': (),
                    },
                })
            self.assertCountEqual(cfgs.keys(), [dev1.name, dev2.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                    'router bgp 100',
                    ' exit',
                    ]))
            self.assertMultiLineEqual(str(cfgs[dev2.name]), '\n'.join([
                    'router bgp 100',
                    ' exit',
                    ]))

            cfgs = bgp.build_config(apply=False, attributes={
                'device_attr': {
                    'PE1': 'vrf_attr__default',
                    },
                })
            self.assertCountEqual(cfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                'router bgp 100',
                ' neighbor 10.1.0.2 remote-as 100',
                ' address-family ipv4 unicast',
                '  exit',
                ' exit',
                    ]))

            cfgs = bgp.build_config(apply=False, attributes={
                'device_attr': {
                    'PE1': 'vrf_attr__default__neighbor_attr__10.1.0.2',
                    },
                })
            self.assertCountEqual(cfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                'router bgp 100',
                ' neighbor 10.1.0.2 remote-as 100',
                ' exit',
                    ]))

    def test_cfg(self):

        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        intf1 = Interface(device=dev1, name='Ethernet0/0/1',
                          ipv4='10.1.0.1/24')
        intf2 = Interface(device=dev1, name='Ethernet0/0/2',
                          ipv4='10.2.0.1/24')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxe')
        intf3 = Interface(device=dev2, name='Ethernet0/0/3',
                          ipv4='10.1.0.2/24', ipv6='2001:111:222::/64')
        intf4 = Interface(device=dev2, name='Ethernet0/0/4',
                          ipv4='10.2.0.2/24')

        with self.assertNoWarnings():

            bgp = Bgp(bgp_id=100)
            self.assertIs(bgp.testbed, testbed)
            Genie.testbed = testbed
            bgp = Bgp(bgp_id=100)
            self.assertIs(bgp.testbed, Genie.testbed)
            self.assertIs(bgp.testbed, testbed)

            # Defining attributes
            af_name = 'ipv4 unicast'
            af_name2 = 'link-state'
            bgp.device_attr[dev1]
            bgp.device_attr[dev1].vrf_attr[None].always_compare_med = True
            bgp.device_attr[dev1].vrf_attr[None].address_family_attr[af_name]
            bgp.device_attr[dev1].vrf_attr[None].address_family_attr[af_name2]
            bgp.device_attr[dev1].vrf_attr[None].address_family_attr[af_name].\
                af_label_allocation_mode = 'per-vrf'
            bgp.device_attr[dev1].vrf_attr[None].address_family_attr[af_name].\
                af_dampening = True
            neighbor_id = intf4.ipv4
            bgp.device_attr[dev1].vrf_attr[None].add_neighbor(neighbor_id)
            bgp.device_attr[dev1].vrf_attr[None].neighbor_attr[neighbor_id]
            bgp.device_attr[dev1].vrf_attr[None].neighbor_attr[neighbor_id].\
                nbr_remote_as = 200
            bgp.device_attr[dev1].vrf_attr[None].neighbor_attr[neighbor_id].\
                nbr_fall_over_bfd = True
            bgp.device_attr[dev1].vrf_attr[None].neighbor_attr[neighbor_id].\
                nbr_shutdown = True
            bgp.device_attr[dev1].vrf_attr[None].neighbor_attr[neighbor_id].\
                nbr_update_source = 'loopback0'
            bgp.device_attr[dev1].vrf_attr[None].neighbor_attr[neighbor_id].\
                nbr_remove_private_as = True
            bgp.device_attr[dev1].vrf_attr[None].neighbor_attr[neighbor_id].\
                nbr_remove_private_as_af_name = 'ipv4 unicast'
            nbr_af_name = 'ipv4 multicast'
            bgp.device_attr[dev1].vrf_attr[None].neighbor_attr[neighbor_id].\
                address_family_attr[nbr_af_name]
            bgp.device_attr[dev1].vrf_attr[None].neighbor_attr[neighbor_id].\
                address_family_attr[nbr_af_name].nbr_af_allowas_in = True

            dev1.add_feature(bgp)

            cfgs = bgp.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
                ['router bgp 100',
                 ' bgp always-compare-med',
                 ' neighbor 10.2.0.2 fall-over bfd',
                 ' neighbor 10.2.0.2 remote-as 200',
                 ' address-family ipv4 unicast',
                 '  neighbor 10.2.0.2 remove-private-as',
                 '  exit',
                 ' neighbor 10.2.0.2 shutdown',
                 ' neighbor 10.2.0.2 update-source loopback0',
                 ' address-family ipv4 multicast',
                 '  neighbor 10.2.0.2 activate',
                 '  neighbor 10.2.0.2 allowas-in',
                 '  exit',
                 ' address-family ipv4 unicast',
                 '  bgp dampening',
                 '  exit',
                 ' address-family link-state',
                 '  exit',
                 ' exit',
                 'mpls label mode vrf default protocol bgp-vpnv4 per-vrf',
                ]))

    def test_partial_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')

        with self.assertNoWarnings():

            Genie.testbed = testbed
            bgp = Bgp(bgp_id=100)
            self.assertIs(bgp.testbed, testbed)
            Genie.testbed = testbed
            bgp = Bgp(bgp_id=100)
            self.assertIs(bgp.testbed, Genie.testbed)
            self.assertIs(bgp.testbed, testbed)

            # Defining attributes
            bgp.device_attr[dev1]
            dev1.add_feature(bgp)
            ps_name = 'PEER-SESSION'
            bgp.device_attr[dev1].peer_session_attr[ps_name].ps_fall_over_bfd=\
                True
            partial_cfg1 = bgp.build_config(
                                apply=False,
                                attributes={'device_attr':\
                                           {'*':{'peer_session_attr':\
                                           {'*':"ps_fall_over_bfd"}}}})

            self.assertCountEqual(partial_cfg1.keys(), [dev1.name])
            self.assertMultiLineEqual(str(partial_cfg1[dev1.name]), '\n'.\
                join([
                'router bgp 100',
                ' template peer-session PEER-SESSION',
                '  fall-over bfd',
                '  exit',
                ' exit',
                    ]))

    def test_cfg2(self):

        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        intf1 = Interface(device=dev1, name='Ethernet0/0/1',
                          ipv4='10.1.0.1/24')
        intf2 = Interface(device=dev1, name='Ethernet0/0/2',
                          ipv4='10.2.0.1/24',
                          ipv6='2001::1')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxe')
        intf3 = Interface(device=dev2, name='Ethernet0/0/3',
                          ipv4='10.1.0.2/24', ipv6='2001:111:222::/64')
        intf4 = Interface(device=dev2, name='Ethernet0/0/4',
                          ipv4='10.2.0.2/24')

        with self.assertNoWarnings():

            Genie.testbed = testbed
            bgp = Bgp(bgp_id=100)
            self.assertIs(bgp.testbed, testbed)
            Genie.testbed = testbed
            bgp = Bgp(bgp_id=100)
            self.assertIs(bgp.testbed, Genie.testbed)
            self.assertIs(bgp.testbed, testbed)

            # Defining attributes
            vrf_id = 'vrf1'
            vrf1 = Vrf(vrf_id)
            pp_name = 'PEER-POLICY'
            ps_name = 'PEER-SESSION'
            bgp.device_attr[dev2].peer_policy_attr[pp_name].pp_allowas_in =\
                True
            bgp.device_attr[dev2].peer_session_attr[ps_name].ps_fall_over_bfd=\
                True
            bgp.device_attr[dev2].vrf_attr[None].cluster_id = '150'
            af_name = 'ipv6 unicast'
            bgp.device_attr[dev2].vrf_attr[None].address_family_attr[af_name]
            bgp.device_attr[dev2].vrf_attr[None].address_family_attr[af_name].\
                af_nexthop_route_map = 'test'
            bgp.device_attr[dev2].vrf_attr[None].address_family_attr[af_name].\
                af_dampening = True
            bgp.device_attr[dev2].vrf_attr[None].address_family_attr[af_name].\
                af_dampening_half_life_time = 1
            bgp.device_attr[dev2].vrf_attr[None].address_family_attr[af_name].\
                af_dampening_reuse_time = 10
            bgp.device_attr[dev2].vrf_attr[None].address_family_attr[af_name].\
                af_dampening_suppress_time = 30
            bgp.device_attr[dev2].vrf_attr[None].address_family_attr[af_name].\
                af_dampening_max_suppress_time = 2
            neighbor_id = intf2.ipv4
            bgp.device_attr[dev2].vrf_attr[vrf1].add_neighbor(neighbor_id)
            bgp.device_attr[dev2].vrf_attr[vrf1].neighbor_attr[neighbor_id].\
                nbr_suppress_four_byte_as_capability = True

            dev2.add_feature(bgp)
            cfgs = bgp.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev2.name])
            self.maxDiff = None
            self.assertEqual(str(cfgs[dev2.name]), '\n'.join(
                ['router bgp 100',
                 ' bgp cluster-id 150',
                 ' address-family ipv6 unicast',
                 '  bgp dampening 1 10 30 2',
                 '  bgp nexthop route-map test',
                 '  exit',
                 ' address-family ipv4 unicast vrf vrf1',
                 '  neighbor 10.2.0.1 dont-capability-negotiate four-octets-as',
                 '  exit',
                 ' template peer-session PEER-SESSION',
                 '  fall-over bfd',
                 '  exit',
                 ' template peer-policy PEER-POLICY',
                 '  allowas-in',
                 '  exit',
                 ' exit',
                ]))

    def test_cfg3(self):

        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        intf1 = Interface(device=dev1, name='Ethernet0/0/1',
                          ipv4='10.1.0.1/24')
        intf2 = Interface(device=dev1, name='Ethernet0/0/2',
                          ipv4='10.2.0.1/24',
                          ipv6='2001::1')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxe')
        intf3 = Interface(device=dev2, name='Ethernet0/0/3',
                          ipv4='10.1.0.2/24', ipv6='2001:111:222::/64')
        intf4 = Interface(device=dev2, name='Ethernet0/0/4',
                          ipv4='10.2.0.2/24')

        with self.assertNoWarnings():

            Genie.testbed = testbed
            bgp = Bgp(bgp_id=100)
            self.assertIs(bgp.testbed, testbed)
            Genie.testbed = testbed
            bgp = Bgp(bgp_id=100)
            self.assertIs(bgp.testbed, Genie.testbed)
            self.assertIs(bgp.testbed, testbed)

            # Defining attributes
            vrf_id = 'vrf1'
            vrf1 = Vrf(vrf_id)
            pp_name = 'PEER-POLICY'
            ps_name = 'PEER-SESSION'
            bgp.device_attr[dev2].peer_policy_attr[pp_name].pp_as_override =\
                True
            bgp.device_attr[dev2].peer_session_attr[ps_name].ps_remote_as=\
                12
            bgp.device_attr[dev2].vrf_attr[None].cluster_id = '150'
            af_name = 'ipv6 unicast'
            bgp.device_attr[dev2].vrf_attr[None].address_family_attr[af_name]
            bgp.device_attr[dev2].vrf_attr[None].address_family_attr[af_name].\
                af_client_to_client_reflection = True
            nbr_af_name = 'ipv6 unicast'
            neighbor_id2 = intf2.ipv6
            bgp.device_attr[dev2].vrf_attr[vrf1].neighbor_attr[neighbor_id2].\
                address_family_attr[nbr_af_name]
            bgp.device_attr[dev2].vrf_attr[vrf1].neighbor_attr[neighbor_id2].\
                address_family_attr[nbr_af_name].\
                nbr_af_maximum_prefix_max_prefix_no = 300000

            dev2.add_feature(bgp)
            cfgs = bgp.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev2.name])
            self.maxDiff = None
            self.assertEqual(str(cfgs[dev2.name]), '\n'.join(
                ['router bgp 100',
                 ' bgp cluster-id 150',
                 ' address-family ipv6 unicast',
                 '  bgp client-to-client reflection',
                 '  exit',
                 ' address-family ipv6 unicast vrf vrf1',
                 '  neighbor 2001::1 activate',
                 '  neighbor 2001::1 maximum-prefix 300000',
                 '  exit',
                 ' template peer-session PEER-SESSION',
                 '  remote-as 12',
                 '  exit',
                 ' template peer-policy PEER-POLICY',
                 '  as-override',
                 '  exit',
                 ' exit',
                ]))


    def test_cfg_as(self):
        ''' Test 4-byte AS support'''
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        intf1 = Interface(device=dev1, name='Ethernet0/0/1',
                          ipv4='10.1.0.1/24')
        intf2 = Interface(device=dev1, name='Ethernet0/0/2',
                          ipv4='10.2.0.1/24',
                          ipv6='2001::1')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxe')
        intf3 = Interface(device=dev2, name='Ethernet0/0/3',
                          ipv4='10.1.0.2/24', ipv6='2001:111:222::/64')
        intf4 = Interface(device=dev2, name='Ethernet0/0/4',
                          ipv4='10.2.0.2/24')

        with self.assertNoWarnings():

            Genie.testbed = testbed
            bgp = Bgp(bgp_id='304.304')
            self.assertIs(bgp.testbed, testbed)
            Genie.testbed = testbed
            bgp = Bgp(bgp_id='304.304')
            self.assertIs(bgp.testbed, Genie.testbed)
            self.assertIs(bgp.testbed, testbed)

        dev1.add_feature(bgp)
        cfgs = bgp.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(cfgs[dev1.name]), '\n'.join(
            ['router bgp 304.304',
             ' exit',
            ]))


    def test_uncfg(self):

        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        intf1 = Interface(device=dev1, name='Ethernet0/0/1',
                          ipv4='10.1.0.1/24')
        intf2 = Interface(device=dev1, name='Ethernet0/0/2',
                          ipv4='10.2.0.1/24')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxe')
        intf3 = Interface(device=dev2, name='Ethernet0/0/3',
                          ipv4='10.1.0.2/24', ipv6='2001:111:222::/64')
        intf4 = Interface(device=dev2, name='Ethernet0/0/4',
                          ipv4='10.2.0.2/24')

        with self.assertNoWarnings():

            Genie.testbed = testbed
            bgp = Bgp(bgp_id=100)
            self.assertIs(bgp.testbed, testbed)
            Genie.testbed = testbed
            bgp = Bgp(bgp_id=100)
            self.assertIs(bgp.testbed, Genie.testbed)
            self.assertIs(bgp.testbed, testbed)

            dev1.add_feature(bgp)

            uncfgs = bgp.build_unconfig(apply=False)
            self.assertCountEqual(uncfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(uncfgs[dev1.name]), '\n'.join([
                'no router bgp 100',
                    ]))

            # Defining attributes
            af_name = 'vpnv4 unicast'
            af_name2 = 'link-state'
            vrf_id = 'vrf1'
            vrf1 = Vrf(vrf_id)
            bgp.device_attr[dev1]
            bgp.device_attr[dev1].vrf_attr[None].always_compare_med = True
            bgp.device_attr[dev1].vrf_attr[None].address_family_attr[af_name]
            bgp.device_attr[dev1].vrf_attr[None].address_family_attr[af_name2]
            bgp.device_attr[dev1].vrf_attr[None].address_family_attr[af_name].\
                af_dampening = True
            bgp.device_attr[dev1].vrf_attr[None].address_family_attr[af_name].\
                af_dampening_half_life_time = 1
            bgp.device_attr[dev1].vrf_attr[None].address_family_attr[af_name].\
                af_dampening_reuse_time = 10
            bgp.device_attr[dev1].vrf_attr[None].address_family_attr[af_name].\
                af_dampening_suppress_time = 30
            bgp.device_attr[dev1].vrf_attr[None].address_family_attr[af_name].\
                af_dampening_max_suppress_time = 2
            neighbor_id = intf4.ipv4
            bgp.device_attr[dev1].vrf_attr[vrf1].add_neighbor(neighbor_id)
            bgp.device_attr[dev1].vrf_attr[vrf1].neighbor_attr[neighbor_id]
            bgp.device_attr[dev1].vrf_attr[vrf1].neighbor_attr[neighbor_id].\
                nbr_fall_over_bfd = True


            partial_uncfg1 = bgp.build_unconfig(
                                apply=False,
                                attributes={'device_attr':\
                                           {'*':{'vrf_attr':\
                                           {'*':"always_compare_med"}}}})
            self.assertCountEqual(partial_uncfg1.keys(), [dev1.name])
            self.assertMultiLineEqual(str(partial_uncfg1[dev1.name]), '\n'.\
                join([
                'router bgp 100',
                ' no bgp always-compare-med',
                ' exit',
                    ]))

            partial_uncfg2 = bgp.build_unconfig(\
                                apply=False,
                                attributes={'device_attr':\
                                           {'*':{'vrf_attr':'*'}}})
            self.assertCountEqual(partial_uncfg2.keys(), [dev1.name])
            self.assertMultiLineEqual(str(partial_uncfg2[dev1.name]), '\n'.\
                join([
                'router bgp 100',
                ' no bgp always-compare-med',
                ' no address-family link-state',
                ' no address-family vpnv4 unicast',
                ' no neighbor 10.2.0.2',
                ' no address-family ipv4 unicast vrf vrf1',
                ' exit',
                    ]))

            partial_uncfg3 = bgp.build_unconfig(
                                apply=False,
                                attributes={'device_attr':\
                                           {'*': {'vrf_attr':\
                                           {'*': {'neighbor_attr':\
                                           {'*':"nbr_fall_over_bfd"}}}}}})
            self.assertCountEqual(partial_uncfg3.keys(), [dev1.name])
            self.assertMultiLineEqual(str(partial_uncfg3[dev1.name]), '\n'.\
                join([
                'router bgp 100',
                ' address-family ipv4 unicast vrf vrf1',
                '  no neighbor 10.2.0.2 fall-over bfd',
                '  exit',
                ' exit',
                    ]))

            # Defining neighbor address family
            nbr_af_name = 'ipv4 unicast'
            bgp.device_attr[dev1].vrf_attr[vrf1].neighbor_attr[neighbor_id].\
                address_family_attr[nbr_af_name]
            bgp.device_attr[dev1].vrf_attr[vrf1].neighbor_attr[neighbor_id].\
                address_family_attr[nbr_af_name].nbr_af_allowas_in = True

            partial_uncfg4 = bgp.build_unconfig(
                                apply=False,
                                attributes={'device_attr': {'*': {'vrf_attr':
                                    {'*': {'neighbor_attr':\
                                    {'*': {'address_family_attr':\
                                    {'*':"nbr_af_allowas_in"}}}}}}}})
            self.assertCountEqual(partial_uncfg4.keys(), [dev1.name])
            self.assertMultiLineEqual(str(partial_uncfg4[dev1.name]), '\n'.\
                join([
                'router bgp 100',
                ' address-family ipv4 unicast vrf vrf1',
                '  no neighbor 10.2.0.2 activate',
                '  no neighbor 10.2.0.2 allowas-in',
                '  exit',
                ' exit',
                    ]))

            partial_uncfg5 = bgp.build_unconfig(
                                apply=False,
                                attributes={'device_attr':\
                                           {'*':{'vrf_attr':\
                                           {'*':{'address_family_attr':\
                                           {'*':"af_dampening"}}}}}})
            self.assertCountEqual(partial_uncfg5.keys(), [dev1.name])
            self.assertMultiLineEqual(str(partial_uncfg5[dev1.name]), '\n'.\
                join([
                'router bgp 100',
                ' address-family vpnv4 unicast',
                '  no bgp dampening',
                '  exit',
                ' exit',
                    ]))

    def test_uncfg2(self):

        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')

        with self.assertNoWarnings():

            Genie.testbed = testbed
            bgp = Bgp(bgp_id=100)
            self.assertIs(bgp.testbed, testbed)
            Genie.testbed = testbed
            bgp = Bgp(bgp_id=100)
            self.assertIs(bgp.testbed, Genie.testbed)
            self.assertIs(bgp.testbed, testbed)

            dev1.add_feature(bgp)

            # Defining attributes
            af_name = 'ipv4 unicast'
            bgp.device_attr[dev1]
            bgp.device_attr[dev1].vrf_attr[None].always_compare_med = True
            bgp.device_attr[dev1].vrf_attr[None].address_family_attr[af_name]
            bgp.device_attr[dev1].vrf_attr[None].address_family_attr[af_name].\
                af_label_allocation_mode = 'per-vrf'

            uncfg = bgp.build_unconfig(apply=False)
            self.assertCountEqual(uncfg.keys(), [dev1.name])
            self.assertMultiLineEqual(str(uncfg[dev1.name]), '\n'.\
                join([
                'no router bgp 100',
                'no mpls label mode vrf default protocol bgp-vpnv4 per-vrf',
                    ]))

    def test_uncfg3(self):

        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxe')
        intf4 = Interface(device=dev2, name='Ethernet0/0/4',
                          ipv4='10.2.0.2/24')


        with self.assertNoWarnings():
            Genie.testbed = testbed
            bgp = Bgp(bgp_id=100)
            self.assertIs(bgp.testbed, Genie.testbed)
            self.assertIs(bgp.testbed, testbed)

            dev1.add_feature(bgp)

            # Defining attributes
            bgp.device_attr[dev1]
            neighbor_id = intf4.ipv4
            bgp.device_attr[dev1].vrf_attr[None].add_neighbor(neighbor_id)
            bgp.device_attr[dev1].vrf_attr[None].neighbor_attr[neighbor_id]

            partial_uncfg = bgp.build_unconfig(
                                apply=False,
                                attributes={'device_attr':\
                                           {'*':{'vrf_attr':\
                                           {'*':{'neighbor_attr':'*'}}}}})

            self.assertCountEqual(partial_uncfg.keys(), [dev1.name])
            self.assertMultiLineEqual(str(partial_uncfg[dev1.name]), '\n'.\
                join([
                'router bgp 100',
                ' no neighbor 10.2.0.2',
                ' exit',
                    ]))

    def test_cfg_l2vpn_vpls(self):

        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        bgp = Bgp(bgp_id=100)

        # Defining attributes
        nbr_af_name = 'l2vpn vpls'
        neighbor_id = '10.2.0.2'

        bgp.device_attr[dev1].vrf_attr[None].neighbor_attr[neighbor_id].\
            address_family_attr[nbr_af_name].nbr_af_suppress_signaling_protocol_ldp = True

        bgp.device_attr[dev1]

        self.assertIs(bgp.testbed, testbed)
        dev1.add_feature(bgp)

        cfgs = bgp.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['router bgp 100',
            ' address-family l2vpn vpls',
            '  neighbor 10.2.0.2 activate',
            '  neighbor 10.2.0.2 suppress-signaling-protocol ldp',
            '  exit',
            ' exit',
            ]))

        uncfgs = bgp.build_unconfig(
            apply=False,
            attributes={'device_attr': {'*': {'vrf_attr':
                                                  {'*': {'neighbor_attr': \
                                                             {'*': {'address_family_attr': \
                                                                        {'*': "nbr_af_suppress_signaling_protocol_ldp"}}}}}}}})

        self.assertCountEqual(uncfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(uncfgs[dev1.name]), '\n'.join(
            ['router bgp 100',
             ' address-family l2vpn vpls',
             '  no neighbor 10.2.0.2 activate',
             '  exit',
             ' exit',
         ]))

    def test_uncfg_as(self):

        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        intf1 = Interface(device=dev1, name='Ethernet0/0/1',
                          ipv4='10.1.0.1/24')
        intf2 = Interface(device=dev1, name='Ethernet0/0/2',
                          ipv4='10.2.0.1/24')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxe')
        intf3 = Interface(device=dev2, name='Ethernet0/0/3',
                          ipv4='10.1.0.2/24', ipv6='2001:111:222::/64')
        intf4 = Interface(device=dev2, name='Ethernet0/0/4',
                          ipv4='10.2.0.2/24')

        with self.assertNoWarnings():

            Genie.testbed = testbed
            bgp = Bgp(bgp_id='304.304')
            self.assertIs(bgp.testbed, testbed)
            Genie.testbed = testbed
            bgp = Bgp(bgp_id='304.304')
            self.assertIs(bgp.testbed, Genie.testbed)
            self.assertIs(bgp.testbed, testbed)

            dev1.add_feature(bgp)

            uncfgs = bgp.build_unconfig(apply=False)
            self.assertCountEqual(uncfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(uncfgs[dev1.name]), '\n'.join([
                'no router bgp 304.304',
                    ]))

    def test_af_network_and_v6_aggregate_spacing(self):
        '''Test whitespace in address-family network and IPv6 aggregate-address CLI generation'''
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')

        with self.assertNoWarnings():
            bgp = Bgp(bgp_id=100)
            dev1.add_feature(bgp)

            af_v4 = bgp.device_attr[dev1].vrf_attr[None].address_family_attr['ipv4 unicast']
            af_v4.af_network_number = '10.4.0.0'
            af_v4.af_network_mask = 24
            af_v4.af_network_route_map = 'RM_IPV4'

            af_v6 = bgp.device_attr[dev1].vrf_attr[None].address_family_attr['ipv6 unicast']
            af_v6.af_v6_aggregate_address_ipv6_address = '2001:db8::/32'
            af_v6.af_v6_aggregate_address_as_set = True
            af_v6.af_v6_aggregate_address_summary_only = True
            af_v6.af_v6_network_number = '2001:db8:1::/48'
            af_v6.af_v6_network_route_map = 'RM_IPV6'

            cfgs = bgp.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                'router bgp 100',
                ' address-family ipv4 unicast',
                '  network 10.4.0.0 mask 24 route-map RM_IPV4',
                '  exit',
                ' address-family ipv6 unicast',
                '  aggregate-address 2001:db8::/32 as-set summary-only',
                '  network 2001:db8:1::/48 route-map RM_IPV6',
                '  exit',
                ' exit',
            ]))

    def test_vrf_name_initialization_and_string_vrf(self):
        '''Test vrf_name resolution when VRF is indexed by string name or when _vrf_name is unset'''
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')

        with self.assertNoWarnings():
            bgp = Bgp(bgp_id=100)
            dev1.add_feature(bgp)

            # Indexing vrf_attr by string name without a Vrf instance registered in testbed
            bgp.device_attr[dev1].vrf_attr['Mgmt-vrf'].cluster_id = '150'
            bgp.device_attr[dev1].vrf_attr['Mgmt-vrf'].address_family_attr['ipv4 unicast'].\
                af_client_to_client_reflection = True

            cfgs = bgp.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                'router bgp 100',
                ' bgp cluster-id 150',
                ' address-family ipv4 unicast vrf Mgmt-vrf',
                '  bgp client-to-client reflection',
                '  exit',
                ' exit',
            ]))

            # Fallback initialization when _vrf_name is absent on VrfAttributes instance
            vrf_sub = bgp.device_attr[dev1].vrf_attr[None]
            del vrf_sub.__dict__['_vrf_name']
            cfg_str = vrf_sub.build_config(apply=False)
            self.assertEqual(vrf_sub.vrf_name, 'default')
            self.assertEqual(cfg_str, '')


if __name__ == '__main__':
    unittest.main()

