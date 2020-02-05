#!/usr/bin/env python

# Python
import unittest
from unittest.mock import Mock

# Genie package
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

# Genie Conf
from genie.libs.conf.vrf import Vrf
from genie.libs.conf.interface import Interface
from genie.libs.conf.ospf import Ospf
from genie.libs.conf.ospf.gracefulrestart import GracefulRestart
from genie.libs.conf.ospf.stubrouter import StubRouter
from genie.libs.conf.ospf.arearange import AreaRange
from genie.libs.conf.ospf.interfacestaticneighbor import InterfaceStaticNeighbor


class test_ospf(TestCase):

    def test_ospf_config(self):

        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')

        # Create VRF objects
        vrf0 = Vrf('default')
        vrf1 = Vrf('VRF1')
        vrf2 = Vrf('VRF2')

        # Create Interface object
        intf1 = Interface(name='GigabitEthernet0/0/0/2',device=dev1)

        # Create OSPF object
        ospf1 = Ospf()

        # ---------------------------------------
        # Configure OSPF instance 1 VRF 'default'
        # ---------------------------------------
        ospf1.device_attr[dev1].vrf_attr[vrf0].instance = '1'
        ospf1.device_attr[dev1].vrf_attr[vrf0].router_id = '1.1.1.1'
        ospf1.device_attr[dev1].vrf_attr[vrf0].pref_all = 110
        ospf1.device_attr[dev1].vrf_attr[vrf0].nsr_enable = True

        # Add graceful restart configuration to vrf 'default'
        gr1 = GracefulRestart(device=dev1)
        gr1.gr_enable = True
        gr1.gr_type = 'ietf'
        gr1.gr_helper_enable = False
        ospf1.device_attr[dev1].vrf_attr[vrf0].add_gr_key(gr1)
        gr2 = GracefulRestart(device=dev1)
        gr2.gr_enable = True
        gr2.gr_type = 'cisco'
        ospf1.device_attr[dev1].vrf_attr[vrf0].add_gr_key(gr2)
        gr3 = GracefulRestart(device=dev1)
        gr3.gr_enable = True
        gr3.gr_restart_interval = 150
        ospf1.device_attr[dev1].vrf_attr[vrf0].add_gr_key(gr3)

        ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_autoconfig = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_igp_sync = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_bgp_id = 100
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_bgp_metric = 10
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_bgp_metric_type = '2'
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_bgp_nssa_only = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_bgp_preserve_med = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_bgp_tag = 24
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_bgp_route_map = 'BGP_TO_OSPF'
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_connected = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_connected_metric = 10
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_connected_route_policy = 'BGP_TO_OSPF'
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_static = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_static_metric = 10
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_static_route_policy = 'BGP_TO_OSPF'
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_isis = 'ABC'
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_isis_metric = 10
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_isis_route_policy = 'BGP_TO_OSPF'
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_max_prefix = 12
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_max_prefix_thld = 10
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_max_prefix_warn_only = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].bfd_enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].bfd_strict_mode = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].te_router_id = 'Loopback0'
        ospf1.device_attr[dev1].vrf_attr[vrf0].log_adjacency_changes = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].log_adjacency_changes_detail = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].adjacency_stagger_initial_number = 563
        ospf1.device_attr[dev1].vrf_attr[vrf0].adjacency_stagger_maximum_number = 1263
        ospf1.device_attr[dev1].vrf_attr[vrf0].auto_cost_enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].auto_cost_reference_bandwidth = 60000
        ospf1.device_attr[dev1].vrf_attr[vrf0].maximum_interfaces = 123
        ospf1.device_attr[dev1].vrf_attr[vrf0].spf_paths = 15
        ospf1.device_attr[dev1].vrf_attr[vrf0].spf_start = 600
        ospf1.device_attr[dev1].vrf_attr[vrf0].spf_hold = 700
        ospf1.device_attr[dev1].vrf_attr[vrf0].spf_maximum = 800
        ospf1.device_attr[dev1].vrf_attr[vrf0].spf_lsa_start = 600
        ospf1.device_attr[dev1].vrf_attr[vrf0].spf_lsa_hold = 700
        ospf1.device_attr[dev1].vrf_attr[vrf0].spf_lsa_maximum = 800
        ospf1.device_attr[dev1].vrf_attr[vrf0].db_ctrl_max_lsa = 123
        ospf1.device_attr[dev1].vrf_attr[vrf0].default_originate = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].default_originate_always = True
        
        # Add stub router configuration to vrf 'default'
        sr1 = StubRouter(device=dev1)
        sr1.stub_router_always = True
        sr1.stub_router_external_lsa = True
        sr1.stub_router_include_stub = True
        sr1.stub_router_summary_lsa = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].add_sr_key(sr1)
        sr2 = StubRouter(device=dev1)
        sr2.stub_router_on_startup = 60
        sr2.stub_router_external_lsa = True
        sr2.stub_router_include_stub = True
        sr2.stub_router_summary_lsa = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].add_sr_key(sr2)
        sr3 = StubRouter(device=dev1)
        sr3.stub_router_on_switchover = 70
        sr3.stub_router_external_lsa = True
        sr3.stub_router_include_stub = True
        sr3.stub_router_summary_lsa = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].add_sr_key(sr3)

        # Add area configuration to VRF 'default'
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].area_id = '0.0.0.0'
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].area_te_enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].area_bfd_enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].area_bfd_min_interval = 300
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].area_bfd_multiplier = 7
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].area_passive = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].area_mtu_ignore = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].area_demand_cirtuit = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].area_external_out = False
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].area_flood_reduction = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].area_link_down_fast_detect = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].area_ldp_auto_config = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].area_ldp_sync = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].area_ldp_sync_igp_shortcuts = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].area_type = 'stub'
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].summary = False
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].default_cost = 50

        # Add arearange configuration to vrf 'default'
        ar1 = AreaRange(device=dev1)
        ar1.area_range_prefix = '1.1.1.0/24'
        ar1.area_range_advertise = False
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].add_arearange_key(ar1)
        ar2 = AreaRange(device=dev1)
        ar2.area_range_prefix = '2.2.2.2 255.255.255.255'
        ar2.area_range_advertise = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].add_arearange_key(ar2)

        # Add interface configuration to VRF 'default'
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].interface_attr[intf1].if_cost = 10

        # Add interface staticneighbor configuration to VRF 'default'
        static_nbr1 = InterfaceStaticNeighbor(device=dev1)
        static_nbr1.if_static_neighbor = '10.10.10.10'
        static_nbr1.if_static_cost = 20
        static_nbr1.if_static_poll_interval = 60
        static_nbr1.if_static_priority = 110
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].interface_attr[intf1].add_staticnbr_key(static_nbr1)
        static_nbr2 = InterfaceStaticNeighbor(device=dev1)
        static_nbr2.if_static_neighbor = '20.20.20.20'
        static_nbr2.if_static_cost = 30
        static_nbr2.if_static_poll_interval = 120
        static_nbr2.if_static_priority = 113
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].interface_attr[intf1].add_staticnbr_key(static_nbr2)
        static_nbr3 = InterfaceStaticNeighbor(device=dev1)
        static_nbr3.if_static_neighbor = '30.30.30.30'
        static_nbr3.if_static_cost = 40
        static_nbr3.if_static_poll_interval = 150
        static_nbr3.if_static_priority = 115
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].interface_attr[intf1].add_staticnbr_key(static_nbr3)

        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].interface_attr[intf1].if_type = 'point-to-point'
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].interface_attr[intf1].if_passive = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].interface_attr[intf1].if_demand_circuit = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].interface_attr[intf1].if_priority = 110
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].interface_attr[intf1].if_bfd_enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].interface_attr[intf1].if_bfd_interval = 999
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].interface_attr[intf1].if_bfd_min_interval = 999
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].interface_attr[intf1].if_bfd_multiplier = 7
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].interface_attr[intf1].if_hello_interval = 50
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].interface_attr[intf1].if_dead_interval = 60
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].interface_attr[intf1].if_retransmit_interval = 70
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].interface_attr[intf1].if_ttl_sec_enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].interface_attr[intf1].if_ttl_sec_hops = 25
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].interface_attr[intf1].if_auth_trailer_key_chain = 'montreal'
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].interface_attr[intf1].if_auth_trailer_key_crypto_algorithm = 'md5'
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].interface_attr[intf1].if_auth_trailer_key = 'quebec'
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].interface_attr[intf1].if_mtu_ignore = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0.0.0.0'].interface_attr[intf1].if_prefix_suppression = True

        # ------------------------------------
        # Configure OSPF instance 2 VRF 'VRF1'
        # ------------------------------------
        ospf1.device_attr[dev1].vrf_attr[vrf1].instance = '2'
        ospf1.device_attr[dev1].vrf_attr[vrf1].router_id = '2.2.2.2'
        ospf1.device_attr[dev1].vrf_attr[vrf1].pref_intra_area = 100
        ospf1.device_attr[dev1].vrf_attr[vrf1].pref_inter_area = 150
        ospf1.device_attr[dev1].vrf_attr[vrf1].pref_external = 200
        ospf1.device_attr[dev1].vrf_attr[vrf1].auto_cost_enable = False

        # Add area configuration to VRF 'VRF1'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['0.0.0.1'].area_id = '0.0.0.1'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['0.0.0.1'].area_type = 'nssa'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['0.0.0.1'].summary = False
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['0.0.0.1'].default_cost = 1111
        
        # Add virtual-link configuration to vrf 'VRF1'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['0.0.0.1'].virtual_link_attr['OSPF_VL0'].vl_router_id = '7.7.7.7'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['0.0.0.1'].virtual_link_attr['OSPF_VL0'].vl_hello_interval = 55
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['0.0.0.1'].virtual_link_attr['OSPF_VL0'].vl_dead_interval = 65
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['0.0.0.1'].virtual_link_attr['OSPF_VL0'].vl_retransmit_interval = 75
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['0.0.0.1'].virtual_link_attr['OSPF_VL0'].vl_transmit_delay = 85
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['0.0.0.1'].virtual_link_attr['OSPF_VL0'].vl_auth_trailer_key_chain = 'ottawa'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['0.0.0.1'].virtual_link_attr['OSPF_VL0'].vl_auth_trailer_key_crypto_algorithm = 'simple'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['0.0.0.1'].virtual_link_attr['OSPF_VL0'].vl_auth_trailer_key = 'asgrocks'
        
        # ------------------------------------
        # Configure OSPF instance 3 VRF 'VRF2'
        # ------------------------------------
        ospf1.device_attr[dev1].vrf_attr[vrf2].instance = '3'
        ospf1.device_attr[dev1].vrf_attr[vrf2].router_id = '3.3.3.3'
        
        # Add area configuration to vrf 'VRF2'
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['0.0.0.2'].area_id = '0.0.0.2'
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['0.0.0.2'].area_type = 'nssa'
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['0.0.0.2'].summary = True
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['0.0.0.2'].default_cost = 123
        # Add sham-link configuration to vrf VRF1
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['0.0.0.2'].sham_link_attr['OSPF_SL0'].sl_local_id = '11.11.11.11'
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['0.0.0.2'].sham_link_attr['OSPF_SL0'].sl_remote_id = '12.12.12.12'
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['0.0.0.2'].sham_link_attr['OSPF_SL0'].sl_hello_interval = 55
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['0.0.0.2'].sham_link_attr['OSPF_SL0'].sl_dead_interval = 65
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['0.0.0.2'].sham_link_attr['OSPF_SL0'].sl_retransmit_interval = 75
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['0.0.0.2'].sham_link_attr['OSPF_SL0'].sl_transmit_delay = 85
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['0.0.0.2'].sham_link_attr['OSPF_SL0'].sl_auth_trailer_key_chain = 'toronto'
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['0.0.0.2'].sham_link_attr['OSPF_SL0'].sl_auth_trailer_key_crypto_algorithm = 'md5'
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['0.0.0.2'].sham_link_attr['OSPF_SL0'].sl_auth_trailer_key = 'genierocks'
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['0.0.0.2'].sham_link_attr['OSPF_SL0'].sl_cost = 50
        
        # Add OSPF to the device
        dev1.add_feature(ospf1)
        
        # Build config
        cfgs = ospf1.build_config(apply=False)

        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'router ospf 1',
                ' router-id 1.1.1.1',
                ' distance 110',
                ' nsr',
                ' nsf cisco',
                ' nsf ietf helper disable',
                ' nsf ietf',
                ' mpls ldp auto-config',
                ' mpls ldp sync',
                ' redistribute bgp 100 metric 10 metric-type 2 nssa-only preserve-med tag 24 route-policy BGP_TO_OSPF',
                ' redistribute connected metric 10 route-policy BGP_TO_OSPF',
                ' redistribute static metric 10 route-policy BGP_TO_OSPF',
                ' redistribute isis ABC metric 10 route-policy BGP_TO_OSPF',
                ' maximum redistributed-prefixes 12 10 warning-only',
                ' bfd fast-detect strict-mode',
                ' mpls traffic-eng router-id Loopback0',
                ' log adjacency changes detail',
                ' adjacency stagger 563 1263',
                ' auto-cost reference-bandwidth 60000',
                ' maximum paths 15',
                ' maximum interfaces 123',
                ' timers throttle spf 600 700 800',
                ' timers throttle lsa all 600 700 800',
                ' max-lsa 123',
                ' max-metric router-lsa on-startup 60 include-stub summary-lsa external-lsa',
                ' max-metric router-lsa on-switchover 70 include-stub summary-lsa external-lsa',
                ' max-metric router-lsa include-stub summary-lsa external-lsa',
                ' default-information originate always',
                ' area 0.0.0.0',
                '  mpls traffic-eng',
                '  bfd fast-detect',
                '  bfd minimum-interval 300',
                '  bfd multiplier 7',
                '  passive enable',
                '  mtu-ignore enable',
                '  demand-circuit enable',
                '  external-out disable',
                '  flood-reduction enable',
                '  link-down fast-detect',
                '  mpls ldp sync',
                '   stub no-summary',
                '  default-cost 50',
                '   range 1.1.1.0 255.255.255.0 not-advertise',
                '   range 2.2.2.2 255.255.255.255 advertise',
                '  interface GigabitEthernet0/0/0/2',
                '   cost 10',
                '   neighbor 10.10.10.10 cost 20 poll-interval 60 priority 110',
                '   neighbor 20.20.20.20 cost 30 poll-interval 120 priority 113',
                '   neighbor 30.30.30.30 cost 40 poll-interval 150 priority 115',
                '   network point-to-point',
                '   passive',
                '   demand-circuit',
                '   priority 110',
                '   bfd fast-detect',
                '   bfd minimum-interval 999',
                '   bfd multiplier 7',
                '   hello-interval 50',
                '   dead-interval 60',
                '   retransmit-interval 70',
                '   security ttl hops 25',
                '   authentication message-digest keychain montreal',
                '   authentication message-digest',
                '   message-digest-key 1 md5 quebec',
                '   mtu-ignore',
                '   prefix-suppression',
                '   exit',
                '  exit',
                ' exit',
                'router ospf 2 vrf VRF1',
                ' router-id 2.2.2.2',
                ' distance ospf intra-area 100 inter-area 150 external 200',
                ' auto-cost disable',
                ' area 0.0.0.1',
                '   nssa no-summary',
                '  default-cost 1111',
                '  virtual-link 7.7.7.7',
                '   hello-interval 55',
                '   dead-interval 65',
                '   retransmit-interval 75',
                '   transmit-delay 85',
                '   authentication message-digest keychain ottawa',
                '   authentication',
                '   authentication-key asgrocks',
                '   exit',
                '  exit',
                ' exit',
                'router ospf 3 vrf VRF2',
                ' router-id 3.3.3.3',
                ' area 0.0.0.2',
                '   nssa',
                '  default-cost 123',
                '  sham-link 11.11.11.11 12.12.12.12',
                '   hello-interval 55',
                '   dead-interval 65',
                '   retransmit-interval 75',
                '   transmit-delay 85',
                '   authentication message-digest keychain toronto',
                '   authentication message-digest',
                '   message-digest-key 1 md5 genierocks',
                '   cost 50',
                '   exit',
                '  exit',
                ' exit',
            ]))

        # Unconfig
        ospf_uncfg = ospf1.build_unconfig(apply=False)

        # Check unconfig strings built correctly
        self.assertMultiLineEqual(
            str(ospf_uncfg[dev1.name]),
            '\n'.join([
                'no router ospf 1',
                'no router ospf 2 vrf VRF1',
                'no router ospf 3 vrf VRF2'
            ]))


    def test_ospf_config2(self):

        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')

        # Create VRF objects
        vrf0 = Vrf('default')
        # Create OSPF object
        ospf1 = Ospf()

        # Add OSPF configurations to vrf 'default'
        ospf1.device_attr[dev1].vrf_attr[vrf0].instance = '1'
        ospf1.device_attr[dev1].vrf_attr[vrf0].router_id = '1.1.1.1'

        # Add OSPF to the device
        dev1.add_feature(ospf1)
        
        # Build config
        cfgs = ospf1.build_config(apply=False)

        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'router ospf 1',
                ' router-id 1.1.1.1',
                ' exit',
            ]))

        # Unconfigure router-id
        ospf_uncfg = ospf1.build_unconfig(apply=False, attributes={
            'device_attr': {
                dev1.name: 'vrf_attr__default__router_id',
            }})

        # Check unconfig strings built correctly
        self.assertMultiLineEqual(
            str(ospf_uncfg[dev1.name]),
            '\n'.join([
                'router ospf 1',
                ' no router-id 1.1.1.1',
                ' exit',
            ]))


if __name__ == '__main__':
    unittest.main()
