#!/usr/bin/env python

# import python
import unittest
from unittest.mock import Mock

# import genie
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Interface

# import genie.libs
from genie.libs.conf.bgp import Bgp
from genie.libs.conf.vrf import Vrf


class test_bgp_config1(TestCase):

    def test_cfg_vxlan(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')
        bgp = Bgp(bgp_id=100)

        # Defining attributes
        af_name = 'l2vpn evpn'
        vrf = Vrf('default')
        bgp.device_attr[dev1].vrf_attr[vrf].address_family_attr[af_name].af_advertise_pip = True

        bgp.device_attr[dev1]

        self.assertIs(bgp.testbed, testbed)
        dev1.add_feature(bgp)

        cfgs = bgp.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['router bgp 100',
             ' address-family l2vpn evpn',
             '  advertise-pip',
             '  exit',
             ' exit',
             ]))

        uncfgs = bgp.build_unconfig(
            apply=False,
            attributes={'device_attr': {'*': {'vrf_attr':
                                            {'*': {'address_family_attr': \
                                                {'*': "af_advertise_pip"}}}}}})

        self.assertCountEqual(uncfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(uncfgs[dev1.name]), '\n'.join(
            ['router bgp 100',
             ' address-family l2vpn evpn',
             '  no advertise-pip',
             '  exit',
             ' exit',
             ]))

        bgp2 = Bgp(bgp_id=100)
        neighbor_id = '10.0.0.1'
        bgp2.device_attr[dev1].vrf_attr[vrf].neighbor_attr[neighbor_id].\
                    nbr_peer_type = Bgp.NBR_PEER_TYPE.fabric_border_leaf
        bgp2.device_attr[dev1].vrf_attr[vrf].neighbor_attr[neighbor_id].address_family_attr[af_name]. \
            nbr_af_rewrite_evpn_rt_asn = True
        bgp2.device_attr[dev1].vrf_attr[vrf].neighbor_attr[neighbor_id].address_family_attr[af_name].\
            nbr_af_disable_peer_as_check = True

        bgp2.device_attr[dev1]

        self.assertIs(bgp2.testbed, testbed)
        dev1.add_feature(bgp2)

        cfgs = bgp2.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['router bgp 100',
             ' neighbor 10.0.0.1',
             '  peer-type fabric-border-leaf',
             '  address-family l2vpn evpn',
             '   disable-peer-as-check',
             '   rewrite-evpn-rt-asn',
             '   exit',
             '  exit',
             ' exit',
             ]))

        uncfgs2 = bgp2.build_unconfig(
            apply=False,
            attributes={'device_attr': {'*': {'vrf_attr':
                                                  {'*': {'neighbor_attr': \
                                                     {'*': {"nbr_peer_type":None,
                                                            'address_family_attr': \
                                                                   {'*': "nbr_af_rewrite_evpn_rt_asn"},
                                                            }}}}}}})

        self.assertCountEqual(uncfgs2.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(uncfgs2[dev1.name]), '\n'.join(
            ['router bgp 100',
             ' neighbor 10.0.0.1',
             '  no peer-type fabric-border-leaf',
             '  address-family l2vpn evpn',
             '   no rewrite-evpn-rt-asn',
             '   exit',
             '  exit',
             ' exit',
             ]))

    def test_cfg_vxlan_rewrite_mvpn(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')
        bgp = Bgp(bgp_id=100)

        # Defining attributes
        af_name = 'ipv4 mvpn'
        vrf = Vrf('default')

        self.assertIs(bgp.testbed, testbed)
        dev1.add_feature(bgp)

        neighbor_id = '10.0.0.1'
        bgp.device_attr[dev1].vrf_attr[vrf].neighbor_attr[neighbor_id].\
                    nbr_peer_type = Bgp.NBR_PEER_TYPE.fabric_border_leaf
        bgp.device_attr[dev1].vrf_attr[vrf].neighbor_attr[neighbor_id].address_family_attr[af_name]. \
            nbr_af_rewrite_mvpn_rt_asn = True

        bgp.device_attr[dev1]

        self.assertIs(bgp.testbed, testbed)
        dev1.add_feature(bgp)

        cfgs = bgp.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['router bgp 100',
             ' neighbor 10.0.0.1',
             '  peer-type fabric-border-leaf',
             '  address-family ipv4 mvpn',
             '   rewrite-rt-asn',
             '   exit',
             '  exit',
             ' exit',
             ]))

        uncfgs2 = bgp.build_unconfig(
            apply=False,
            attributes={'device_attr': {'*': {'vrf_attr':
                                                  {'*': {'neighbor_attr': \
                                                     {'*': {"nbr_peer_type":None,
                                                            'address_family_attr': \
                                                                   {'*': "nbr_af_rewrite_mvpn_rt_asn"},
                                                            }}}}}}})

        self.assertCountEqual(uncfgs2.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(uncfgs2[dev1.name]), '\n'.join(
            ['router bgp 100',
             ' neighbor 10.0.0.1',
             '  no peer-type fabric-border-leaf',
             '  address-family ipv4 mvpn',
             '   no rewrite-rt-asn',
             '   exit',
             '  exit',
             ' exit',
             ]))

    def test_cfg_l2vpn_vpls(self):

        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')
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
            ' neighbor 10.2.0.2',
            '  address-family l2vpn vpls',
            '   suppress-signling-protocol ldp',
            '   exit',
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
             ' neighbor 10.2.0.2',
             '  address-family l2vpn vpls',
             '   no suppress-signling-protocol ldp',
             '   exit',
             '  exit',
             ' exit',
         ]))

    def test_cfg(self):
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

        with self.assertNoWarnings():
            Genie.testbed = testbed
            bgp = Bgp(asn=100, bgp_id=100)
            self.assertIs(bgp.testbed, testbed)
            Genie.testbed = testbed
            bgp = Bgp(asn=100, bgp_id=100)
            self.assertIs(bgp.testbed, Genie.testbed)
            self.assertIs(bgp.testbed, testbed)

            # Defining attributes
            af_name = 'vpnv4 unicast'
            af_name2 = 'link-state'
            bgp.device_attr[dev1]
            bgp.device_attr[dev1].enabled = True
            bgp.device_attr[dev1].vrf_attr[None].always_compare_med = True
            bgp.device_attr[dev1].vrf_attr[None].maxas_limit = 10
            bgp.device_attr[dev1].vrf_attr[None].prefix_peer_timeout = 10
            bgp.device_attr[dev1].vrf_attr[None].address_family_attr[af_name]
            bgp.device_attr[dev1].vrf_attr[None].address_family_attr[af_name2]
            bgp.device_attr[dev1].vrf_attr[None].address_family_attr[af_name]. \
                af_retain_rt_all = True
            bgp.device_attr[dev1].vrf_attr[None].address_family_attr[af_name]. \
                af_dampening = True
            bgp.device_attr[dev1].vrf_attr[None].address_family_attr[af_name]\
                .af_default_metric = True
            bgp.device_attr[dev1].vrf_attr[None].address_family_attr[af_name]\
                .af_default_metric_value = 0
            bgp.device_attr[dev1].vrf_attr[None].address_family_attr[af_name]\
                .af_advertise_l2_evpn = True
            bgp.device_attr[dev1].vrf_attr[None].address_family_attr[af_name] \
                .af_default_information_originate = True
            neighbor_id = intf4.ipv4
            bgp.device_attr[dev1].vrf_attr[None].add_neighbor(neighbor_id)
            bgp.device_attr[dev1].vrf_attr[None].neighbor_attr[neighbor_id]
            bgp.device_attr[dev1].vrf_attr[None].neighbor_attr[neighbor_id]. \
                nbr_fall_over_bfd = True
            bgp.device_attr[dev1].vrf_attr[None].neighbor_attr[neighbor_id]. \
                nbr_shutdown = True
            nbr_af_name = 'ipv4 unicast'
            bgp.device_attr[dev1].vrf_attr[None].neighbor_attr[neighbor_id]. \
                address_family_attr[nbr_af_name]
            bgp.device_attr[dev1].vrf_attr[None].neighbor_attr[neighbor_id]. \
                address_family_attr[nbr_af_name].nbr_af_allowas_in = True
            bgp.device_attr[dev1].vrf_attr[None].neighbor_attr[neighbor_id]. \
                address_family_attr[nbr_af_name].nbr_af_suppress_inactive = True
            dev1.add_feature(bgp)

            cfgs = bgp.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
                ['feature bgp',
                 'router bgp 100',
                 ' bestpath always-compare-med',
                 ' maxas-limit 10',
                 ' timers prefix-peer-timeout 10',
                 ' neighbor 10.2.0.2',
                 '  bfd',
                 '  shutdown',
                 '  address-family ipv4 unicast',
                 '   allowas-in',
                 '   suppress-inactive',
                 '   exit',
                 '  exit',
                 ' address-family link-state',
                 '  exit',
                 ' address-family vpnv4 unicast',
                 '  default-metric 0',
                 '  default-information originate',
                 '  dampening',
                 '  retain route-target all',
                 '  advertise l2vpn evpn',
                 '  exit',
                 ' exit',
                 ]))

            bgp.device_attr[dev1].protocol_shutdown = True
            partial_cfg1 = bgp.build_config(
                apply=False,
                attributes={'device_attr': \
                                {'*': "enabled", '*': "protocol_shutdown"}})
            self.assertCountEqual(partial_cfg1.keys(), [dev1.name])
            self.assertMultiLineEqual(str(partial_cfg1[dev1.name]), '\n'. \
                                      join([
                'router bgp 100',
                ' shutdown',
                ' exit',
            ]))
    def test_cfg2(self):

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

        with self.assertNoWarnings():

            Genie.testbed = testbed
            bgp = Bgp(asn=100,bgp_id=100)
            self.assertIs(bgp.testbed, testbed)
            Genie.testbed = testbed
            bgp = Bgp(asn=100,bgp_id=100)
            self.assertIs(bgp.testbed, Genie.testbed)
            self.assertIs(bgp.testbed, testbed)

            # Defining attributes
            vrf_id = 'vrf1'
            vrf1 = Vrf(vrf_id)
            pp_name = 'PEER-POLICY'
            ps_name = 'PEER-SESSION'
            bgp.device_attr[dev2].enabled = True
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
            nbr_af_name = 'vpnv6 unicast'
            bgp.device_attr[dev2].vrf_attr[vrf1].neighbor_attr[neighbor_id].\
                address_family_attr[nbr_af_name]
            bgp.device_attr[dev2].vrf_attr[vrf1].neighbor_attr[neighbor_id].\
                address_family_attr[nbr_af_name].\
                nbr_af_maximum_prefix_max_prefix_no = 300000
            bgp.device_attr[dev2].vrf_attr[vrf1].neighbor_attr[neighbor_id].\
                address_family_attr[nbr_af_name].nbr_af_default_originate = True

            dev2.add_feature(bgp)
            cfgs = bgp.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev2.name])
            self.maxDiff = None
            self.assertEqual(str(cfgs[dev2.name]), '\n'.join(
                ['feature bgp',
                'router bgp 100',
                ' cluster-id 150',
                ' address-family ipv6 unicast',
                '  dampening 1 10 30 2',
                '  nexthop route-map test',
                '  exit',
                ' vrf vrf1',
                '  neighbor 10.2.0.1',
                '   capability suppress 4-byte-as',
                '   address-family vpnv6 unicast',
                '    maximum-prefix 300000',
                '    default-originate',
                '    exit',
                '   exit',
                '  exit',
                ' template peer-session PEER-SESSION',
                '  bfd',
                '  exit',
                ' template peer-policy PEER-POLICY',
                '  allowas-in',
                '  exit',
                ' exit',
                ]))

            partial_uncfg1 = bgp.build_unconfig(apply=False, attributes={\
                                'device_attr':\
                                    {dev2.name:\
                                        {'vrf_attr':\
                                            {'vrf1':\
                                                {'neighbor_attr':\
                                                    {'10.2.0.1':\
                                                        {'address_family_attr':\
                                                            {'vpnv6 unicast':\
                                                                {'nbr_af_default_originate': None}}}}}}}}})
            self.assertCountEqual(partial_uncfg1.keys(), [dev2.name])
            self.assertMultiLineEqual(str(partial_uncfg1[dev2.name]), '\n'.\
                join([
                'router bgp 100',
                ' vrf vrf1',
                '  neighbor 10.2.0.1',
                '   address-family vpnv6 unicast',
                '    no default-originate',
                '    exit',
                '   exit',
                '  exit',
                ' exit',
                ]))


    def test_uncfg(self):

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

        with self.assertNoWarnings():
            bgp = Bgp(asn=100,bgp_id=100)
            self.assertIs(bgp.testbed, testbed)
            Genie.testbed = testbed
            bgp = Bgp(asn=100,bgp_id=100)
            self.assertIs(bgp.testbed, Genie.testbed)
            self.assertIs(bgp.testbed, testbed)

            dev1.add_feature(bgp)

            bgp.device_attr[dev1].enabled = True
            uncfgs = bgp.build_unconfig(apply=False)
            self.assertCountEqual(uncfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(uncfgs[dev1.name]), '\n'.join([
                'no feature bgp',
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
                af_retain_rt_all = True
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
            nbr_af_name = 'ipv4 unicast'
            bgp.device_attr[dev1].vrf_attr[vrf1].neighbor_attr[neighbor_id].\
                address_family_attr[nbr_af_name]
            bgp.device_attr[dev1].vrf_attr[vrf1].neighbor_attr[neighbor_id].\
                address_family_attr[nbr_af_name].nbr_af_allowas_in = True


            partial_uncfg1 = bgp.build_unconfig(
                                apply=False,
                                attributes={'device_attr':\
                                           {'*':{'vrf_attr':\
                                           {'*':"always_compare_med"}}}})
            self.assertCountEqual(partial_uncfg1.keys(), [dev1.name])
            self.assertMultiLineEqual(str(partial_uncfg1[dev1.name]), '\n'.\
                join([
                'router bgp 100',
                ' no bestpath always-compare-med',
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
                ' no bestpath always-compare-med',
                ' no address-family link-state',
                ' no address-family vpnv4 unicast',
                ' no vrf vrf1',
                ' exit',
                    ]))

            partial_uncfg3 = bgp.build_unconfig(
                                apply=False,
                                attributes={'device_attr': {'*': {'vrf_attr':
                                    {'*': {'neighbor_attr':\
                                    {'*': {'address_family_attr':\
                                    {'*':"nbr_af_allowas_in"}}}}}}}})
            self.assertCountEqual(partial_uncfg3.keys(), [dev1.name])
            self.assertMultiLineEqual(str(partial_uncfg3[dev1.name]), '\n'.\
                join([
                'router bgp 100',
                ' vrf vrf1',
                '  neighbor 10.2.0.2',
                '   address-family ipv4 unicast',
                '    no allowas-in',
                '    exit',
                '   exit',
                '  exit',
                ' exit',
                    ]))

            bgp.device_attr[dev1].protocol_shutdown = True
            partial_uncfg4 = bgp.build_unconfig(
                                apply=False,
                                attributes={'device_attr':\
                                           {'*':"protocol_shutdown"}})
            self.assertCountEqual(partial_uncfg4.keys(), [dev1.name])
            self.assertMultiLineEqual(str(partial_uncfg4[dev1.name]), '\n'.\
                join([
                'router bgp 100',
                ' no shutdown',
                ' exit',
                    ]))

            partial_uncfg5 = bgp.build_unconfig(\
                                apply=False,
                                attributes={'device_attr':\
                                            {'*':\
                                                {'vrf_attr':\
                                                    {'*':\
                                                        {'address_family_attr':\
                                                            {'*':\
                                                            "af_dampening"}}}}}})
            self.assertCountEqual(partial_uncfg5.keys(), [dev1.name])
            self.assertMultiLineEqual(str(partial_uncfg5[dev1.name]), '\n'.\
                join([
                'router bgp 100',
                ' address-family vpnv4 unicast',
                '  no dampening',
                '  exit',
                ' exit',
                    ]))

            bgp.device_attr[dev1].enabled = False
            uncfgs = bgp.build_unconfig(apply=False)
            self.assertCountEqual(uncfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(uncfgs[dev1.name]), '\n'.join([
                'no router bgp 100',
                    ]))

            bgp.device_attr[dev1].enabled = True
            uncfgs = bgp.build_unconfig(apply=False)
            self.assertCountEqual(uncfgs.keys(), [dev1.name])
            self.assertMultiLineEqual(str(uncfgs[dev1.name]), '\n'.join([
                'no feature bgp',
                    ]))

    def test_learn_config(self):

        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')
        dev1.custom = {'abstraction':{'order':['os'], 'context':'cli'}}
        dev2 = Device(testbed=testbed, name='PE2', os='nxos')

        golden_output = {'return_value': '''
            pinxdt-n9kv-3# show run bgp

            !Command: show running-config bgp
            !Time: Wed Jun 28 06:23:27 2017

            version 7.0(3)I7(1)
            feature bgp

            router bgp 333
              dynamic-med-interval 70
              shutdown
              cluster-id 3
              no graceful-restart
              flush-routes
              isolate
              disable-policy-batching ipv4 prefix-list s
              no enforce-first-as
              event-history objstore size large
              address-family ipv4 multicast
                dampening 1 10 30 2
                redistribute static route-map PERMIT_ALL_RM
              address-family ipv6 multicast
                dampening 1 10 30 2
                redistribute static route-map PERMIT_ALL_RM
              address-family ipv6 unicast
                dampening 1 10 30 2
                redistribute static route-map PERMIT_ALL_RM
                inject-map ORIGINATE_IPV6 exist-map INJECTED_IPV6 copy-attributes
                nexthop route-map test
              address-family vpnv4 unicast
                dampening route-map PASS-ALL
                nexthop trigger-delay critical 4 non-critical 5
              address-family vpnv6 unicast
                dampening 1 10 30 2
              address-family ipv4 labeled-unicast
              template peer-session PEER-SESSION
                ebgp-multihop 3
              neighbor fec1::1002
                remote-as 333
                address-family ipv4 unicast
                  send-community
                  send-community extended
                  route-reflector-client
                  soft-reconfiguration inbound always
              neighbor fec1::2002
                remote-as 888
                address-family ipv4 unicast
                  send-community
                  send-community extended
                  soft-reconfiguration inbound always
                address-family ipv6 multicast
                  send-community
                  send-community extended
                  soft-reconfiguration inbound always
                address-family ipv6 unicast
                  send-community
                  send-community extended
                  soft-reconfiguration inbound always
              neighbor 4.4.4.4
                capability suppress 4-byte-as
                address-family vpnv6 unicast
                  send-community
                  send-community extended
                  soft-reconfiguration inbound always
                  maximum-prefix 300000
              neighbor 21.0.101.1
                remote-as 333
                address-family ipv4 multicast
                  send-community
                  send-community extended
                  route-reflector-client
                  soft-reconfiguration inbound always
                address-family ipv4 unicast
                  send-community
                  send-community extended
                  route-reflector-client
                  soft-reconfiguration inbound always
                address-family ipv6 multicast
                  send-community
                  send-community extended
                  route-reflector-client
                  soft-reconfiguration inbound always
                address-family ipv6 unicast
                  send-community
                  send-community extended
                  route-reflector-client
                  soft-reconfiguration inbound always
                address-family vpnv4 unicast
                  send-community
                  send-community extended
                  route-reflector-client
                address-family vpnv6 unicast
                  send-community
                  send-community extended
                  route-reflector-client
              neighbor 21.0.102.1
                remote-as 333
                update-source loopback0
                address-family ipv4 multicast
                  send-community
                  send-community extended
                  route-reflector-client
                  soft-reconfiguration inbound always
                address-family ipv4 unicast
                  send-community
                  send-community extended
                  route-reflector-client
                  soft-reconfiguration inbound always
                address-family ipv6 multicast
                  send-community
                  send-community extended
                  route-reflector-client
                  soft-reconfiguration inbound always
                address-family ipv6 unicast
                  send-community
                  send-community extended
                  route-reflector-client
                  soft-reconfiguration inbound always
                address-family vpnv4 unicast
                  send-community
                  send-community extended
                address-family vpnv6 unicast
                  send-community
                  send-community extended
                  route-reflector-client
              neighbor 21.0.201.1
                remote-as 888
                address-family ipv4 multicast
                  send-community
                  send-community extended
                  soft-reconfiguration inbound always
                address-family ipv4 unicast
                  send-community
                  send-community extended
                  soft-reconfiguration inbound always
                address-family ipv6 multicast
                  send-community
                  send-community extended
                  soft-reconfiguration inbound always
                address-family ipv6 unicast
                  send-community
                  send-community extended
                  soft-reconfiguration inbound always
                address-family vpnv4 unicast
                  send-community
                  send-community extended
                address-family vpnv6 unicast
                  send-community
                  send-community extended
              vrf ac
                bestpath always-compare-med
                address-family ipv4 unicast
                neighbor 2.2.2.2
                  bfd
                  local-as 222
                  description ja
                  remove-private-as
                  disable-connected-check
                  capability suppress 4-byte-as
                  address-family ipv4 unicast
                    allowas-in 3
                    send-community
                    send-community extended
                    maximum-prefix 2
              vrf management
                neighbor 5.5.5.5
                  password 3 386c0565965f89de
              vrf vpn1
                address-family ipv4 multicast
                  redistribute static route-map PERMIT_ALL_RM
                address-family ipv4 unicast
                  dampening 1 10 30 2
                  redistribute static route-map PERMIT_ALL_RM
                address-family ipv6 multicast
                  dampening 1 10 30 2
                  redistribute static route-map PERMIT_ALL_RM
                address-family ipv6 unicast
                  dampening 1 10 30 2
                  redistribute static route-map PERMIT_ALL_RM
            vrf context vpn1
              rd 1:100
              address-family ipv4 unicast
                route-target import 100:1
                route-target export 100:1
                route-target export 400:400
                export map PERMIT_ALL_RM
                import map PERMIT_ALL_RM
                import vrf default map PERMIT_ALL_RM
                export vrf default map PERMIT_ALL_RM
              address-family ipv6 unicast
                route-target import 1:100
                route-target export 1:100
                route-target export 600:600
                export map PERMIT_ALL_RM
                import map PERMIT_ALL_RM
                import vrf default map PERMIT_ALL_RM
                export vrf default map PERMIT_ALL_RM
            vrf context vpn2
              rd 2:100
              address-family ipv4 unicast
                route-target import 400:400
              address-family ipv6 unicast
                route-target import 600:600
        '''}

        bgp = Bgp(asn=333, bgp_id=333)

        dev1.execute = Mock(**golden_output)

        bgp.device_attr[dev1]
        bgp.device_attr[dev1].enabled = True
        bgp.device_attr[dev1].vrf_attr[None].cluster_id = '3'

        af_name = 'ipv6 unicast'
        bgp.device_attr[dev1].vrf_attr[None].address_family_attr[af_name]
        bgp.device_attr[dev1].vrf_attr[None].address_family_attr[af_name].\
            af_nexthop_route_map = 'test'
        neighbor_id = '4.4.4.4'
        bgp.device_attr[dev1].vrf_attr[None].add_neighbor(neighbor_id)
        bgp.device_attr[dev1].vrf_attr[None].neighbor_attr[neighbor_id].\
            nbr_suppress_four_byte_as_capability = True
        nbr_af_name = 'vpnv6 unicast'
        bgp.device_attr[dev1].vrf_attr[None].neighbor_attr[neighbor_id].\
            address_family_attr[nbr_af_name]
        bgp.device_attr[dev1].vrf_attr[None].neighbor_attr[neighbor_id].\
            address_family_attr[nbr_af_name].\
            nbr_af_maximum_prefix_max_prefix_no = 300000

        cfgs = bgp.build_config(apply=False)

        # List of BGP conf objects representing the different instances
        # For NXOS, it is only one.
        learn = Bgp.learn_config(device=dev1)

        # Testing cluster_id
        self.assertEqual(learn[0].device_attr[dev1].vrf_attr['default'].\
            cluster_id,bgp.device_attr[dev1].vrf_attr['default'].cluster_id)

        # Testing af_nexthop_route_map
        self.assertEqual(learn[0].device_attr[dev1].vrf_attr['default'].\
            address_family_attr['ipv6 unicast'].af_nexthop_route_map,
            bgp.device_attr[dev1].vrf_attr['default'].address_family_attr\
            ['ipv6 unicast'].af_nexthop_route_map)

        # Testing nbr_suppress_four_byte_as_capability
        self.assertEqual(learn[0].device_attr[dev1].vrf_attr['default'].\
            neighbor_attr['4.4.4.4'].nbr_suppress_four_byte_as_capability,
            bgp.device_attr[dev1].vrf_attr['default'].neighbor_attr['4.4.4.4']\
            .nbr_suppress_four_byte_as_capability)

        # Testing nbr_af_maximum_prefix_max_prefix_no
        self.assertEqual(learn[0].device_attr[dev1].vrf_attr['default'].\
            neighbor_attr['4.4.4.4'].address_family_attr[nbr_af_name].\
            nbr_af_maximum_prefix_max_prefix_no, bgp.device_attr[dev1].\
            vrf_attr['default'].neighbor_attr['4.4.4.4'].address_family_attr\
            [nbr_af_name].nbr_af_maximum_prefix_max_prefix_no)

    def test_feature_bgp_config(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')
        bgp = Bgp()
        bgp.device_attr[dev1].enabled = True
        dev1.add_feature(bgp)
        cfgs = bgp.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.assertEqual(str(cfgs[dev1.name]), "feature bgp")


if __name__ == '__main__':
    unittest.main()

