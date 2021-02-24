#!/usr/bin/env python

import unittest
from unittest.mock import Mock

from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface
from genie.conf.base.attributes import UnsupportedAttributeWarning

from genie.libs.conf.base import Redistribution
from genie.libs.conf.bgp import Bgp
from genie.libs.conf.isis import Isis
from genie.libs.conf.ospf import Ospf
from genie.libs.conf.route_policy import RoutePolicy
from genie.libs.conf.vrf import Vrf


class test_bgp(TestCase):

    def test_init(self):

        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/0/1',
            ipv4='10.1.0.1/24')
        intf2 = Interface(device=dev1, name='GigabitEthernet0/0/0/2',
            ipv4='10.2.0.1/24')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxr')
        intf3 = Interface(device=dev2, name='GigabitEthernet0/0/0/3',
            ipv4='10.1.0.2/24')
        intf4 = Interface(device=dev2, name='GigabitEthernet0/0/0/4',
            ipv4='10.2.0.2/24')
        vrf1 = Vrf(name='vrf1')
        vrf2 = Vrf(name='a')  # must be < 'default'

        with self.assertNoWarnings():

            Genie.testbed = testbed
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
                    ' exit',
                    ]))

            dev2.add_feature(bgp)

            cfgs = bgp.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev1.name, dev2.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                    'router bgp 100',
                    ' exit',
                    ]))
            self.assertMultiLineEqual(str(cfgs[dev2.name]), '\n'.join([
                    'router bgp 100',
                    ' exit',
                    ]))

            ospf1 = Ospf(pid=1)
            isis1 = Isis(pid=1)
            rtepol1 = RoutePolicy(name='rtepol1')
            bgp.redistributes = (
                'connected',
                Redistribution(ospf1, metric=20),
                Redistribution(isis1, route_policy=rtepol1),
            )
            bgp.device_attr[dev1].address_family_attr['ipv4 unicast']
            bgp.device_attr[dev2].address_family_attr['ipv4 unicast']

            cfgs = bgp.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev1.name, dev2.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                    'router bgp 100',
                    ' address-family ipv4 unicast',
                    '  redistribute connected',
                    '  redistribute ospf 1 metric 20',
                    '  redistribute isis 1 route-policy rtepol1',
                    '  exit',
                    ' exit',
                    ]))
            self.assertMultiLineEqual(str(cfgs[dev2.name]), '\n'.join([
                    'router bgp 100',
                    ' address-family ipv4 unicast',
                    '  redistribute connected',
                    '  redistribute ospf 1 metric 20',
                    '  redistribute isis 1 route-policy rtepol1',
                    '  exit',
                    ' exit',
                    ]))

            del bgp.redistributes

            bgp.device_attr[dev1].add_neighbor(intf3.ipv4)
            bgp.device_attr[dev1].neighbor_attr[intf3.ipv4].\
                address_family_attr['ipv4 unicast']
            bgp.device_attr[dev1].add_vrf(vrf1)
            bgp.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv4 unicast']
            bgp.device_attr[dev1].vrf_attr[vrf1].add_neighbor(intf4.ipv4)
            bgp.device_attr[dev1].vrf_attr[vrf1].neighbor_attr[intf4.ipv4].\
                address_family_attr['ipv4 unicast']
            bgp.device_attr[dev1].add_vrf(vrf2)
            bgp.device_attr[dev1].vrf_attr[vrf2].address_family_attr['ipv4 unicast']

            cfgs = bgp.build_config(apply=False)
            self.assertCountEqual(cfgs.keys(), [dev1.name, dev2.name])
            self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join([
                    'router bgp 100',
                    ' address-family ipv4 unicast',
                    '  exit',
                    ' neighbor 10.1.0.2',
                    '  remote-as 100',
                    '  address-family ipv4 unicast',
                    '   exit',
                    '  exit',
                    ' vrf a',
                    '  address-family ipv4 unicast',
                    '   exit',
                    '  exit',
                    ' vrf vrf1',
                    '  address-family ipv4 unicast',
                    '   exit',
                    '  neighbor 10.2.0.2',
                    '   remote-as 100',
                    '   address-family ipv4 unicast',
                    '    exit',
                    '   exit',
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
                    ' address-family ipv4 unicast',
                    '  exit',
                    ' neighbor 10.1.0.2',
                    '  remote-as 100',
                    '  address-family ipv4 unicast',
                    '   exit',
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
                    ' address-family ipv4 unicast',
                    '  exit',
                    ' neighbor 10.1.0.2',
                    '  remote-as 100',
                    '  address-family ipv4 unicast',
                    '   exit',
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
                    ' neighbor 10.1.0.2',
                    '  remote-as 100',
                    '  address-family ipv4 unicast',
                    '   exit',
                    '  exit',
                    ' exit',
                    ]))

    def setUp(self):

        Genie.testbed = testbed = Testbed()
        self.dev1 = Device(testbed=testbed, name='PE1', os='iosxr')
        self.intf1 = Interface(device=self.dev1,
            name='GigabitEthernet0/0/0/1', ipv4='10.1.0.1/24')
        self.intf2 = Interface(device=self.dev1,
            name='GigabitEthernet0/0/0/2', ipv4='10.2.0.1/24')
        self.dev2 = Device(testbed=testbed, name='PE2', os='iosxr')
        self.intf3 = Interface(device=self.dev2,
            name='GigabitEthernet0/0/0/3', ipv4='10.1.0.2/24')
        self.intf4 = Interface(device=self.dev2,
            name='GigabitEthernet0/0/0/4', ipv4='10.2.0.2/24')
        self.vrf1 = Vrf(name='vrf1')
        self.vrf2 = Vrf(name='default')

    def test_bgp_device_attr(self):
        # For failures
        self.maxDiff = None

        # shorten the line
        dev1 = self.dev1

        # ===== no instance =======        
        # Bgp object
        bgp = Bgp(bgp_id=100)
        dev1.add_feature(bgp)
        # Build config
        cfgs = bgp.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'router bgp 100',
                ' exit',
                ]))
        # ===== with instance =======        
        # Bgp object
        bgp = Bgp(bgp_id=100)
        dev1.add_feature(bgp)
        bgp.device_attr[dev1].instance_name = 'test'
        # Build config
        cfgs = bgp.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'router bgp 100 instance test',
                ' exit',
                ]))

        # ===== with different instances =======        
        # Bgp object
        bgp1 = Bgp(bgp_id=100, instance_name='test1')
        dev1.add_feature(bgp1)
        # Bgp object
        bgp2 = Bgp(bgp_id=100, instance_name='test2')
        dev1.add_feature(bgp2)
        # Bgp object
        bgp3 = Bgp(bgp_id=100, instance_name='test3')
        dev1.add_feature(bgp3)
        # Build config
        cfg1 = bgp1.build_config(apply=False)
        cfg2 = bgp2.build_config(apply=False)
        cfg3 = bgp3.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfg1[dev1.name]), '\n'.\
            join([
                'router bgp 100 instance test1',
                ' exit',
                ]))

        # Check config built correctly
        self.assertMultiLineEqual(str(cfg2[dev1.name]), '\n'.\
            join([
                'router bgp 100 instance test2',
                ' exit',
                ]))

        # Check config built correctly
        self.assertMultiLineEqual(str(cfg3[dev1.name]), '\n'.\
            join([
                'router bgp 100 instance test3',
                ' exit',
                ]))

        # Build unconfig
        cfg1 = bgp1.build_unconfig(apply=False)
        cfg2 = bgp2.build_unconfig(apply=False)
        cfg3 = bgp3.build_unconfig(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfg1[dev1.name]), '\n'.\
            join([
                'no router bgp 100 instance test1',
                ]))

        # Check config built correctly
        self.assertMultiLineEqual(str(cfg2[dev1.name]), '\n'.\
            join([
                'no router bgp 100 instance test2',
                ]))

        # Check config built correctly
        self.assertMultiLineEqual(str(cfg3[dev1.name]), '\n'.\
            join([
                'no router bgp 100 instance test3',
                ]))

    def test_cfg_l2vpn_vpls(self):

        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')
        bgp = Bgp(asn=100,bgp_id=100)

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
             '   signalling ldp disable',
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
             '   no signalling ldp disable',
             '   exit',
             '  exit',
             ' exit',
             ]))

    def test_bgp_peer_session_attr(self):
        # For failures
        self.maxDiff = None

        # shorten the line
        dev1 = self.dev1
    
        # Bgp object
        bgp = Bgp(bgp_id=100)
        dev1.add_feature(bgp)
        ps = 'PEERSESSION'
        bgp.device_attr[dev1].peer_session_attr[ps].ps_transport_connection_mode = 'passive'
        bgp.device_attr[dev1].peer_session_attr[ps].ps_suppress_four_byte_as_capability =True
        bgp.device_attr[dev1].peer_session_attr[ps].ps_description = 'some description'
        bgp.device_attr[dev1].peer_session_attr[ps].ps_disable_connected_check = True
        bgp.device_attr[dev1].peer_session_attr[ps].ps_shutdown = True
        bgp.device_attr[dev1].peer_session_attr[ps].ps_update_source = 'GigabitEthernet0/0/0/2'
        # Build config
        cfgs = bgp.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'router bgp 100',
                ' session-group PEERSESSION',
                '  capability suppress 4-byte-as',
                '  description some description',
                '  ignore-connected-check',
                '  shutdown',
                '  session-open-mode passive',
                '  update-source GigabitEthernet0/0/0/2',
                '  exit',
                ' exit',
                ]))

    def test_bgp_peer_policy_attr(self):
        # For failures
        self.maxDiff = None

        # shorten the line
        dev1 = self.dev1
    
        # Bgp object
        bgp = Bgp(bgp_id=100)
        dev1.add_feature(bgp)
        pp = 'PEERPOLICY'
        bgp.device_attr[dev1].peer_policy_attr[pp].pp_af_name = 'ipv4 unicast'
        bgp.device_attr[dev1].peer_policy_attr[pp].pp_allowas_in = True
        bgp.device_attr[dev1].peer_policy_attr[pp].pp_allowas_in_as_number = 5
        bgp.device_attr[dev1].peer_policy_attr[pp].pp_as_override = True
        bgp.device_attr[dev1].peer_policy_attr[pp].pp_default_originate = True
        bgp.device_attr[dev1].peer_policy_attr[pp].pp_default_originate_route_map = 'pp-map-test'
        bgp.device_attr[dev1].peer_policy_attr[pp].pp_route_map_name_in = 'allin'
        bgp.device_attr[dev1].peer_policy_attr[pp].pp_route_map_name_out = 'allout'
        bgp.device_attr[dev1].peer_policy_attr[pp].pp_maximum_prefix_max_prefix_no = 100
        bgp.device_attr[dev1].peer_policy_attr[pp].pp_maximum_prefix_threshold = 50
        bgp.device_attr[dev1].peer_policy_attr[pp].pp_maximum_prefix_restart = 99
        bgp.device_attr[dev1].peer_policy_attr[pp].pp_next_hop_self = True
        bgp.device_attr[dev1].peer_policy_attr[pp].pp_route_reflector_client = True
        bgp.device_attr[dev1].peer_policy_attr[pp].pp_send_community = 'standard'
        bgp.device_attr[dev1].peer_policy_attr[pp].pp_soft_reconfiguration = True
        # Build config
        cfgs = bgp.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'router bgp 100',
                ' af-group PEERPOLICY address-family ipv4 unicast',
                '  allowas-in 5',
                '  as-override',
                '  default-originate route-policy pp-map-test',
                '  route-policy allin in',
                '  route-policy allout out',
                '  maximum-prefix 100 50 restart 99',
                '  next-hop-self',
                '  route-reflector-client',
                '  send-community-ebgp',
                '  soft-reconfiguration inbound',
                '  exit',
                ' exit',
                ]))

    def test_bgp_vrf_attr(self):
        # For failures
        self.maxDiff = None

        # shorten the line
        dev1 = self.dev1

        # ===== none-default vrf =======        
        # Bgp object
        bgp = Bgp(bgp_id=100)
        dev1.add_feature(bgp)
        
        bgp.device_attr[dev1].add_vrf(self.vrf1)
        bgp.device_attr[dev1].vrf_attr[self.vrf1].rd = '100:1'
        bgp.device_attr[dev1].vrf_attr[self.vrf1].always_compare_med = True
        bgp.device_attr[dev1].vrf_attr[self.vrf1].graceful_restart = True
        bgp.device_attr[dev1].vrf_attr[self.vrf1].\
            graceful_restart_restart_time = 100
        bgp.device_attr[dev1].vrf_attr[self.vrf1].\
            graceful_restart_stalepath_time = 150
        bgp.device_attr[dev1].vrf_attr[self.vrf1].log_neighbor_changes = False
        bgp.device_attr[dev1].vrf_attr[self.vrf1].router_id = '1.1.1.1'
        bgp.device_attr[dev1].vrf_attr[self.vrf1].keepalive_interval = 10
        bgp.device_attr[dev1].vrf_attr[self.vrf1].holdtime = 100
        bgp.device_attr[dev1].vrf_attr[self.vrf1].enforce_first_as = False

        # Build config
        cfgs = bgp.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'router bgp 100',
                ' vrf vrf1',
                '  bgp bestpath med always',
                '  rd 100:1',
                '  bgp log neighbor changes disable',
                '  bgp router-id 1.1.1.1',
                '  timers bgp 10 100',
                '  bgp enforce-first-as disable',
                '  exit',
                ' exit',
                ]))

        # ===== default vrf =======        
        # Bgp object
        bgp = Bgp(bgp_id=100)
        dev1.add_feature(bgp)
        bgp.device_attr[dev1].add_vrf(self.vrf2)
        bgp.device_attr[dev1].vrf_attr[self.vrf2].always_compare_med = True
        bgp.device_attr[dev1].vrf_attr[self.vrf2].cluster_id = 10
        bgp.device_attr[dev1].vrf_attr[self.vrf2].confederation_identifier = 20
        bgp.device_attr[dev1].vrf_attr[self.vrf2].confederation_peers_as = '66'
        bgp.device_attr[dev1].vrf_attr[self.vrf2].graceful_restart = True
        bgp.device_attr[dev1].vrf_attr[self.vrf2].\
            graceful_restart_restart_time = 100
        bgp.device_attr[dev1].vrf_attr[self.vrf2].\
            graceful_restart_stalepath_time = 150
        bgp.device_attr[dev1].vrf_attr[self.vrf2].log_neighbor_changes = True
        bgp.device_attr[dev1].vrf_attr[self.vrf2].router_id = '1.1.1.1'
        bgp.device_attr[dev1].vrf_attr[self.vrf2].keepalive_interval = 10
        bgp.device_attr[dev1].vrf_attr[self.vrf2].holdtime = 100
        bgp.device_attr[dev1].vrf_attr[self.vrf2].fast_external_fallover = False

        # Build config
        cfgs = bgp.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'router bgp 100',
                ' bgp bestpath med always',
                ' bgp cluster-id 10',
                ' bgp confederation identifier 20',
                ' bgp confederation peers 66',
                ' bgp graceful-restart',
                ' bgp graceful-restart restart-time 100',
                ' bgp graceful-restart stalepath-time 150',
                ' bgp router-id 1.1.1.1',
                ' timers bgp 10 100',
                ' bgp fast-external-fallover disable',
                ' exit',
                ]))


    def test_bgp_vrf_family_attr(self):
        # For failures
        self.maxDiff = None

        # shorten the line
        dev1 = self.dev1

        # ===== none-default vrf =======        
        # Bgp object
        bgp = Bgp(bgp_id=100)
        dev1.add_feature(bgp)
        af = 'ipv4 unicast'
        af6 = 'ipv6 unicast'
        
        bgp.device_attr[dev1].add_vrf(self.vrf1)
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af]
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af].\
            af_dampening = True
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af].\
            af_dampening_route_map = 'route-test'
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af].\
            af_dampening_half_life_time = 30
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af].\
            af_client_to_client_reflection = True
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af].\
            af_distance_extern_as = 100
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af].\
            af_distance_internal_as = 110
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af].\
            af_distance_local = 120
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af].\
            af_maximum_paths_ebgp = 15
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af].\
            af_maximum_paths_ibgp = 20
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af].\
            af_maximum_paths_eibgp = 30
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af].\
            af_aggregate_address_ipv4_address = '2.2.2.2'
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af].\
            af_aggregate_address_ipv4_mask = 24
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af].\
            af_aggregate_address_summary_only = True
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af].\
            af_network_number = '3.3.3.3'
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af].\
            af_network_mask = 24
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af].\
            af_network_route_map = 'network-map-test'
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af].\
            af_redist_isis = '1'
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af].\
            af_redist_ospf = '1'
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af].\
            af_redist_ospf_metric = 10
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af].\
            af_redist_rip = True
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af].\
            af_redist_rip_route_policy = 'rip-route-test'
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af6].\
            af_v6_network_number = '3:3::/48'
        bgp.device_attr[dev1].vrf_attr[self.vrf1].address_family_attr[af6].\
            af_v6_aggregate_address_ipv6_address = '2:2::/64'

        # Build config
        cfgs = bgp.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'router bgp 100',
                ' vrf vrf1',
                '  address-family ipv4 unicast',
                '   bgp dampening 30',
                '   distance bgp 100 110 120',
                '   maximum-paths ebgp 15',
                '   maximum-paths ibgp 20',
                '   maximum-paths eibgp 30',
                '   aggregate-address 2.2.2.2/24 summary-only',
                '   network 3.3.3.3/24 route-policy network-map-test',
                '   redistribute ospf 1 metric 10',
                '   redistribute rip route-policy rip-route-test',
                '   exit',
                '  address-family ipv6 unicast',
                '   aggregate-address 2:2::/64',
                '   network 3:3::/48',
                '   exit',
                '  exit',
                ' exit',
                ]))

        # ===== default vrf =======        
        # Bgp object
        bgp = Bgp(bgp_id=100)
        dev1.add_feature(bgp)
        af = 'vpnv4 unicast'
        bgp.device_attr[dev1].add_vrf(self.vrf2)
        bgp.device_attr[dev1].vrf_attr[self.vrf2].always_compare_med = True
        bgp.device_attr[dev1].vrf_attr[self.vrf2].address_family_attr[af].\
        	af_retain_rt_all = True

        # Build config
        cfgs = bgp.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'router bgp 100',
                ' bgp bestpath med always',
                ' address-family vpnv4 unicast',
                '  retain route-target all',
                '  exit',
                ' exit',
                ]))

    def test_bgp_vrf_neighbor_attr(self):
        # For failures
        self.maxDiff = None

        # shorten the line
        dev1 = self.dev1

        # ===== none-default vrf =======        
        # Bgp object
        bgp = Bgp(bgp_id=100)
        dev1.add_feature(bgp)
        nei = '10.1.1.1'
        nei6 = '10:1::1:1'
        
        bgp.device_attr[dev1].add_vrf(self.vrf1)
        bgp.device_attr[dev1].vrf_attr[self.vrf1].add_neighbor(nei)
        bgp.device_attr[dev1].vrf_attr[self.vrf1].neighbor_attr[nei].\
            nbr_fall_over_bfd = True
        bgp.device_attr[dev1].vrf_attr[self.vrf1].neighbor_attr[nei].\
            nbr_ebgp_multihop = True
        bgp.device_attr[dev1].vrf_attr[self.vrf1].neighbor_attr[nei].\
            nbr_ebgp_multihop_max_hop = 30
        bgp.device_attr[dev1].vrf_attr[self.vrf1].neighbor_attr[nei].\
            nbr_inherit_peer_session = 'PEERSESSION'
        bgp.device_attr[dev1].vrf_attr[self.vrf1].neighbor_attr[nei].\
            nbr_local_as_as_no = 200
        bgp.device_attr[dev1].vrf_attr[self.vrf1].neighbor_attr[nei].\
            nbr_remote_as = 500
        bgp.device_attr[dev1].vrf_attr[self.vrf1].neighbor_attr[nei].\
            nbr_remove_private_as = True
        bgp.device_attr[dev1].vrf_attr[self.vrf1].neighbor_attr[nei].\
            nbr_remove_private_as_af_name = 'ipv4 unicast'
        bgp.device_attr[dev1].vrf_attr[self.vrf1].neighbor_attr[nei].\
            nbr_shutdown = True
        bgp.device_attr[dev1].vrf_attr[self.vrf1].neighbor_attr[nei].\
            nbr_keepalive_interval = 15
        bgp.device_attr[dev1].vrf_attr[self.vrf1].neighbor_attr[nei].\
            nbr_holdtime = 300
        bgp.device_attr[dev1].vrf_attr[self.vrf1].neighbor_attr[nei].\
            nbr_update_source = 'GigabitEthernet0/0/0/1'
        bgp.device_attr[dev1].vrf_attr[self.vrf1].neighbor_attr[nei].\
            nbr_password_text = 'somePassword'
        bgp.device_attr[dev1].vrf_attr[self.vrf1].neighbor_attr[nei].\
            nbr_transport_connection_mode = 'active'

        # Build config
        cfgs = bgp.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'router bgp 100',
                ' vrf vrf1',
                '  neighbor 10.1.1.1',
                '   bfd fast-detect',
                '   remote-as 500',
                '   update-source GigabitEthernet0/0/0/1',
                '   ebgp-multihop 30',
                '   use session-group PEERSESSION',
                '   local-as 200',
                '   address-family ipv4 unicast remove-private-AS',
                '   shutdown',
                '   timers 15 300',
                '   password somePassword',
                '   session-open-mode active',
                '   exit',
                '  exit',
                ' exit',
                ]))

    def test_bgp_vrf_neighbor_family_attr(self):
        # For failures
        self.maxDiff = None

        # shorten the line
        dev1 = self.dev1

        # ===== none-default vrf =======        
        # Bgp object
        bgp = Bgp(bgp_id=100)
        dev1.add_feature(bgp)
        nei = '10:1::1:1'
        af = 'ipv6 unicast'
        
        bgp.device_attr[dev1].add_vrf(self.vrf2)
        bgp.device_attr[dev1].vrf_attr[self.vrf2].address_family_attr[af]
        bgp.device_attr[dev1].vrf_attr[self.vrf2].add_neighbor(nei)
        bgp.device_attr[dev1].vrf_attr[self.vrf2].neighbor_attr[nei].\
            nbr_remote_as = 100
        bgp.device_attr[dev1].vrf_attr[self.vrf2].neighbor_attr[nei].\
            address_family_attr[af]
        bgp.device_attr[dev1].vrf_attr[self.vrf2].neighbor_attr[nei].\
            address_family_attr[af].nbr_af_allowas_in = True
        bgp.device_attr[dev1].vrf_attr[self.vrf2].neighbor_attr[nei].\
            address_family_attr[af].nbr_af_inherit_peer_policy = 'policy-test'
        bgp.device_attr[dev1].vrf_attr[self.vrf2].neighbor_attr[nei].\
            address_family_attr[af].nbr_af_maximum_prefix_max_prefix_no = 666
        bgp.device_attr[dev1].vrf_attr[self.vrf2].neighbor_attr[nei].\
            address_family_attr[af].nbr_af_maximum_prefix_warning_only = True
        bgp.device_attr[dev1].vrf_attr[self.vrf2].neighbor_attr[nei].\
            address_family_attr[af].nbr_af_route_map_name_in = 'nei-af-in'
        bgp.device_attr[dev1].vrf_attr[self.vrf2].neighbor_attr[nei].\
            address_family_attr[af].nbr_af_route_reflector_client = True
        bgp.device_attr[dev1].vrf_attr[self.vrf2].neighbor_attr[nei].\
            address_family_attr[af].nbr_af_next_hop_self = True
        bgp.device_attr[dev1].vrf_attr[self.vrf2].neighbor_attr[nei].\
            address_family_attr[af].nbr_af_default_originate = True

        # Build config
        cfgs = bgp.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'router bgp 100',
                ' address-family ipv6 unicast',
                '  exit',
                ' neighbor 10:1::1:1',
                '  remote-as 100',
                '  address-family ipv6 unicast',
                '   allowas-in',
                '   use af-group policy-test',
                '   maximum-prefix 666 warning-only',
                '   route-policy nei-af-in in',
                '   route-reflector-client',
                '   next-hop-self',
                '   default-originate',
                '   exit',
                '  exit',
                ' exit',
                ]))

    def test_bgp_with_attributes(self):
        # For failures
        self.maxDiff = None

        # shorten the line
        dev1 = self.dev1

        # ===== no instance =======        
        # Bgp object
        bgp = Bgp(bgp_id=100)
        dev1.add_feature(bgp)
        bgp.device_attr[dev1].vrf_attr[self.vrf1]
        attributes = {'device_attr': {dev1: {'vrf_attr': {self.vrf1: None}}}}
        # Build config
        cfgs = bgp.build_unconfig(apply=False, attributes=attributes)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'router bgp 100',
                ' no vrf vrf1',
                ' exit',
                ]))

        # ===== instance =======        
        # Bgp object
        bgp = Bgp(bgp_id=100, instance_name='test')
        dev1.add_feature(bgp)
        bgp.device_attr[dev1].vrf_attr[self.vrf1]
        bgp.device_attr[dev1].instance_name = 'test'
        attributes = {'device_attr': {dev1: {'vrf_attr': {self.vrf1: None}}}}
        # Build config
        cfgs = bgp.build_unconfig(apply=False, attributes=attributes)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'router bgp 100 instance test',
                ' no vrf vrf1',
                ' exit',
                ]))

        # ===== instance as attribute =======        
        # Bgp object
        bgp = Bgp(bgp_id=100)
        dev1.add_feature(bgp)
        bgp.device_attr[dev1].instance_name = 'test'
        attributes = {'device_attr': {dev1: {'instance_name': {'test': None}}}}
        # Build config
        cfgs = bgp.build_unconfig(apply=False, attributes=attributes)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'no router bgp 100 instance test',
                ]))

        # ===== instance as attribute =======        
        # Bgp object
        bgp = Bgp(bgp_id=100, instance='test')
        dev1.add_feature(bgp)
        bgp.device_attr[dev1].instance_name = 'test'
        attributes = {'device_attr': {dev1: {'instance_name': {'test': None}}}}
        # Build config
        cfgs = bgp.build_unconfig(apply=False, attributes=attributes)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'no router bgp 100 instance test',
                ]))


if __name__ == '__main__':
    unittest.main()

