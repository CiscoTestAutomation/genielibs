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
from genie.libs.conf.ospf.areanetwork import AreaNetwork
from genie.libs.conf.ospf.arearange import AreaRange
from genie.libs.conf.ospf.interfacestaticneighbor import InterfaceStaticNeighbor


class test_ospf(TestCase):

    # For failures
    maxDiff = None

    def test_ospf_config1(self):

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')

        # Create VRF objects
        vrf0 = Vrf('default')
        vrf1 = Vrf('VRF1')
        vrf2 = Vrf('VRF2')

        # Create Interface object
        intf1 = Interface(name='GigabitEthernet1',device=dev1)

        # Create OSPF object
        ospf1 = Ospf()

        # Add OSPF configurations to vrf default
        ospf1.device_attr[dev1].vrf_attr[vrf0].instance = '30'
        ospf1.device_attr[dev1].vrf_attr[vrf0].enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].router_id = '3.3.3.3'
        ospf1.device_attr[dev1].vrf_attr[vrf0].pref_all = 115
        ospf1.device_attr[dev1].vrf_attr[vrf0].nsr_enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_autoconfig = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_auto_config_area_id = '0.0.0.0'
        ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_igp_sync = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_bgp_id = 100
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_bgp_metric = 555
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_bgp_metric_type = '1'
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_bgp_nssa_only = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_bgp_route_map = 'test'
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_bgp_subnets = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_bgp_tag = 12
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_connected = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_connected_metric = 12
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_connected_route_policy = 'test'
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_static = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_static_metric = 12
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_static_route_policy = 'test'
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_isis = 'ABC'
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_isis_metric = 12
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_isis_route_policy = 'test'
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_max_prefix = 12
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_max_prefix_thld = 10
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_max_prefix_warn_only = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].bfd_enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].bfd_strict_mode = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].log_adjacency_changes = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].log_adjacency_changes_detail = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].adjacency_stagger_initial_number = 10
        ospf1.device_attr[dev1].vrf_attr[vrf0].adjacency_stagger_maximum_number = 100
        ospf1.device_attr[dev1].vrf_attr[vrf0].auto_cost_enable = True
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
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].area_te_enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_admin_control = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_cost = 10
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_type = 'point-to-point'
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_passive = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_demand_circuit = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_priority = 110
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_bfd_enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_bfd_interval = 999
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_bfd_min_interval = 999
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_bfd_multiplier = 7
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_hello_interval = 50
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_dead_interval = 60
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_retransmit_interval = 70
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_lls = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_ttl_sec_enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_ttl_sec_hops = 25
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_auth_trailer_key_chain = 'montreal'
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_auth_trailer_key_crypto_algorithm = 'md5'
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_auth_trailer_key = 'quebec'
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_mtu_ignore = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_prefix_suppression = True
        # Add interface static neighbor configuration to OSPF
        static_nbr1 = InterfaceStaticNeighbor(device=dev1)
        static_nbr1.if_static_neighbor = '10.10.10.10'
        static_nbr1.if_static_cost = 20
        static_nbr1.if_static_poll_interval = 60
        static_nbr1.if_static_priority = 110
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].add_staticnbr_key(static_nbr1)
        static_nbr2 = InterfaceStaticNeighbor(device=dev1)
        static_nbr2.if_static_neighbor = '20.20.20.20'
        static_nbr2.if_static_cost = 30
        static_nbr2.if_static_poll_interval = 120
        static_nbr2.if_static_priority = 113
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].add_staticnbr_key(static_nbr2)
        static_nbr3 = InterfaceStaticNeighbor(device=dev1)
        static_nbr3.if_static_neighbor = '30.30.30.30'
        static_nbr3.if_static_cost = 40
        static_nbr3.if_static_poll_interval = 150
        static_nbr3.if_static_priority = 115
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].add_staticnbr_key(static_nbr3)

        # Add OSPF configurations to vrf VRF1
        ospf1.device_attr[dev1].vrf_attr[vrf1].instance = '10'
        ospf1.device_attr[dev1].vrf_attr[vrf1].enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf1].router_id = '1.1.1.1'
        ospf1.device_attr[dev1].vrf_attr[vrf1].pref_intra_area = 112
        ospf1.device_attr[dev1].vrf_attr[vrf1].pref_inter_area = 113
        ospf1.device_attr[dev1].vrf_attr[vrf1].pref_external = 114
        ospf1.device_attr[dev1].vrf_attr[vrf1].auto_cost_enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf1].auto_cost_reference_bandwidth = 60
        ospf1.device_attr[dev1].vrf_attr[vrf1].auto_cost_bandwidth_unit = 'gbps'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].area_te_enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].area_type = 'stub'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].default_cost = 1111
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].virtual_link_attr['OSPF_VL0'].vl_router_id = '7.7.7.7'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].virtual_link_attr['OSPF_VL0'].vl_hello_interval = 55
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].virtual_link_attr['OSPF_VL0'].vl_dead_interval = 65
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].virtual_link_attr['OSPF_VL0'].vl_retransmit_interval = 75
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].virtual_link_attr['OSPF_VL0'].vl_transmit_delay = 85
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].virtual_link_attr['OSPF_VL0'].vl_ttl_sec_hops = 167
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].virtual_link_attr['OSPF_VL0'].vl_auth_trailer_key_chain = 'ottawa'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].virtual_link_attr['OSPF_VL0'].vl_auth_trailer_key_crypto_algorithm = 'simple'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].virtual_link_attr['OSPF_VL0'].vl_auth_trailer_key = 'anything'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].sham_link_attr['OSPF_SL0'].sl_local_id = '11.11.11.11'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].sham_link_attr['OSPF_SL0'].sl_remote_id = '12.12.12.12'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].sham_link_attr['OSPF_SL0'].sl_ttl_sec_hops = 10
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].sham_link_attr['OSPF_SL1'].sl_local_id = '15.15.15.15'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].sham_link_attr['OSPF_SL1'].sl_remote_id = '16.16.16.16'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].sham_link_attr['OSPF_SL1'].sl_cost = 50
        
        # Add OSPF configurations to vrf VRF2
        ospf1.device_attr[dev1].vrf_attr[vrf2].instance = '20'
        ospf1.device_attr[dev1].vrf_attr[vrf2].enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf2].router_id = '2.2.2.2'
        ospf1.device_attr[dev1].vrf_attr[vrf2].auto_cost_enable = False
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['2'].area_te_enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['2'].area_type = 'nssa'
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['2'].summary = False
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['2'].default_cost = 1111
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['2'].virtual_link_attr['OSPF_VL1'].vl_router_id = '8.8.8.8'
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['2'].virtual_link_attr['OSPF_VL1'].vl_hello_interval = 56
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['2'].virtual_link_attr['OSPF_VL1'].vl_dead_interval = 66
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['2'].virtual_link_attr['OSPF_VL1'].vl_retransmit_interval = 76
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['2'].virtual_link_attr['OSPF_VL1'].vl_transmit_delay = 86
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['2'].virtual_link_attr['OSPF_VL1'].vl_ttl_sec_hops = 168
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['2'].virtual_link_attr['OSPF_VL1'].vl_auth_trailer_key_chain = 'toronto'
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['2'].virtual_link_attr['OSPF_VL1'].vl_auth_trailer_key_crypto_algorithm = 'md5'
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['2'].virtual_link_attr['OSPF_VL1'].vl_auth_trailer_key = 'anything'
        # Add graceful restart configuration to OSPF
        gr1 = GracefulRestart(device=dev1)
        gr1.gr_enable = True
        gr1.gr_type = 'cisco'
        gr1.gr_helper_enable = False
        ospf1.device_attr[dev1].vrf_attr[vrf2].add_gr_key(gr1)
        gr2 = GracefulRestart(device=dev1)
        gr2.gr_enable = True
        gr2.gr_type = 'ietf'
        gr2.gr_helper_strict_lsa_checking = True
        ospf1.device_attr[dev1].vrf_attr[vrf2].add_gr_key(gr2)
        gr3 = GracefulRestart(device=dev1)
        gr3.gr_enable = True
        gr3.gr_type = 'ietf'
        gr3.gr_restart_interval = 50
        ospf1.device_attr[dev1].vrf_attr[vrf2].add_gr_key(gr3)
        # Add stub router configuration to OSPF
        sr1 = StubRouter(device=dev1)
        sr1.stub_router_always = True
        sr1.stub_router_include_stub = True
        sr1.stub_router_summary_lsa = True
        sr1.stub_router_external_lsa = True
        ospf1.device_attr[dev1].vrf_attr[vrf2].add_sr_key(sr1)
        sr2 = StubRouter(device=dev1)
        sr2.stub_router_on_startup = 50
        sr2.stub_router_include_stub = True
        sr2.stub_router_summary_lsa = True
        sr2.stub_router_external_lsa = True
        ospf1.device_attr[dev1].vrf_attr[vrf2].add_sr_key(sr2)
        # Add area network configuration to OSPF
        an1 = AreaNetwork(device=dev1)
        an1.area_network = '192.168.1.0'
        an1.area_network_wildcard = '0.0.0.0'
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['2'].add_areanetwork_key(an1)
        an2 = AreaNetwork(device=dev1)
        an2.area_network = '192.168.1.1'
        an2.area_network_wildcard = '0.0.0.255'
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['2'].add_areanetwork_key(an2)
        # Add area range configuration to OSPF
        ar1 = AreaRange(device=dev1)
        ar1.area_range_prefix = '1.1.1.1/24'
        ar1.area_range_advertise = False
        ar1.area_range_cost = 10
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['2'].add_arearange_key(ar1)
        ar2 = AreaRange(device=dev1)
        ar2.area_range_prefix = '2.2.2.2 255.255.255.255'
        ar2.area_range_advertise = True
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['2'].add_arearange_key(ar2)

        # Add OSPF to the device
        dev1.add_feature(ospf1)
        
        # Build config
        cfgs = ospf1.build_config(apply=False)

        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'router ospf 30',
                ' no shutdown',
                ' router-id 3.3.3.3',
                ' distance 115',
                ' nsr',
                ' mpls ldp autoconfig area 0.0.0.0',
                ' mpls ldp sync',
                ' redistribute bgp 100 metric 555 metric-type 1 subnets nssa-only tag 12 route-map test',
                ' redistribute connected metric 12 route-map test',
                ' redistribute static metric 12 route-map test',
                ' redistribute isis ABC metric 12 route-map test',
                ' redistribute maximum-prefix 12 10 warning-only',
                ' bfd all-interfaces strict-mode',
                ' log-adjacency-changes detail',
                ' adjacency stagger 10 100',
                ' auto-cost',
                ' maximum-paths 15',
                ' timers throttle spf 600 700 800',
                ' timers throttle lsa 600 700 800',
                ' max-lsa 123',
                ' default-information originate always',
                ' mpls traffic-eng area 0',
                ' passive-interface GigabitEthernet1',
                ' neighbor 10.10.10.10 cost 20 poll-interval 60 priority 110',
                ' neighbor 20.20.20.20 cost 30 poll-interval 120 priority 113',
                ' neighbor 30.30.30.30 cost 40 poll-interval 150 priority 115',
                ' exit',
                'router ospf 10 vrf VRF1',
                ' no shutdown',
                ' router-id 1.1.1.1',
                ' distance ospf intra-area 112 inter-area 113 external 114',
                ' auto-cost reference-bandwidth 60000',
                ' mpls traffic-eng area 1',
                ' area 1 stub',
                ' area 1 default-cost 1111',
                ' area 1 virtual-link 7.7.7.7',
                ' area 1 virtual-link 7.7.7.7 hello-interval 55',
                ' area 1 virtual-link 7.7.7.7 dead-interval 65',
                ' area 1 virtual-link 7.7.7.7 retransmit-interval 75',
                ' area 1 virtual-link 7.7.7.7 transmit-delay 85',
                ' area 1 virtual-link 7.7.7.7 ttl-security hops 167',
                ' area 1 virtual-link 7.7.7.7 authentication key-chain ottawa',
                ' area 1 virtual-link 7.7.7.7 authentication',
                ' area 1 virtual-link 7.7.7.7 authentication-key anything',
                ' area 1 sham-link 11.11.11.11 12.12.12.12',
                ' area 1 sham-link 11.11.11.11 12.12.12.12 ttl-security hops 10',
                ' area 1 sham-link 15.15.15.15 16.16.16.16',
                ' area 1 sham-link 15.15.15.15 16.16.16.16 cost 50',
                ' exit',
                'router ospf 20 vrf VRF2',
                ' no shutdown',
                ' router-id 2.2.2.2',
                ' nsf cisco helper disable',
                ' nsf ietf restart-interval 50',
                ' nsf ietf helper strict-lsa-checking',
                ' no auto-cost',
                ' max-metric router-lsa external-lsa include-stub summary-lsa on-startup 50',
                ' max-metric router-lsa external-lsa include-stub summary-lsa',
                ' network 192.168.1.0 0.0.0.0 area 2',
                ' network 192.168.1.1 0.0.0.255 area 2',
                ' mpls traffic-eng area 2',
                ' area 2 nssa no-summary',
                ' area 2 default-cost 1111',
                ' area 2 range 1.1.1.1 255.255.255.0 not-advertise cost 10',
                ' area 2 range 2.2.2.2 255.255.255.255 advertise',
                ' area 2 virtual-link 8.8.8.8',
                ' area 2 virtual-link 8.8.8.8 hello-interval 56',
                ' area 2 virtual-link 8.8.8.8 dead-interval 66',
                ' area 2 virtual-link 8.8.8.8 retransmit-interval 76',
                ' area 2 virtual-link 8.8.8.8 transmit-delay 86',
                ' area 2 virtual-link 8.8.8.8 ttl-security hops 168',
                ' area 2 virtual-link 8.8.8.8 authentication key-chain toronto',
                ' area 2 virtual-link 8.8.8.8 authentication message-digest',
                ' area 2 virtual-link 8.8.8.8 message-digest-key 1 md5 anything',
                ' exit',
                'interface GigabitEthernet1',
                ' ip ospf 30 area 0',
                ' ip ospf cost 10',
                ' ip ospf network point-to-point',
                ' ip ospf demand-circuit',
                ' ip ospf priority 110',
                ' ip ospf bfd',
                ' bfd interval 999 min_rx 999 multiplier 7',
                ' ip ospf hello-interval 50',
                ' ip ospf dead-interval 60',
                ' ip ospf retransmit-interval 70',
                ' ip ospf lls',
                ' ip ospf ttl-security hops 25',
                ' ip ospf authentication key-chain montreal',
                ' ip ospf authentication message-digest',
                ' ip ospf message-digest-key 1 md5 quebec',
                ' ip ospf mtu-ignore',
                ' ip ospf prefix-suppression',
                ' exit',
            ]))

        # Unconfig
        ospf_uncfg = ospf1.build_unconfig(apply=False)

        # Check unconfig strings built correctly
        self.assertMultiLineEqual(
            str(ospf_uncfg[dev1.name]),
            '\n'.join([
                'no router ospf 30',
                'no router ospf 10 vrf VRF1',
                'no router ospf 20 vrf VRF2',
            ]))


    def test_ospf_config2(self):

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')

        # Create VRF objects
        vrf0 = Vrf('default')
        # Create OSPF object
        ospf1 = Ospf()

        # Add OSPF configurations to vrf default
        ospf1.device_attr[dev1].vrf_attr[vrf0].instance = '1'
        ospf1.device_attr[dev1].vrf_attr[vrf0].enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].router_id = '1.1.1.1'
        ospf1.device_attr[dev1].vrf_attr[vrf0].pref_all = 115

        # Add OSPF to the device
        dev1.add_feature(ospf1)
        
        # Build config
        cfgs = ospf1.build_config(apply=False)

        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'router ospf 1',
                ' no shutdown',
                ' router-id 1.1.1.1',
                ' distance 115',
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

    def test_ospf_device_build_config(self):

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')

        # Create VRF objects
        vrf0 = Vrf('default')
        # Create OSPF object
        ospf1 = Ospf()

        # Add OSPF configurations to vrf default
        ospf1.device_attr[dev1].vrf_attr[vrf0].instance = '30'
        ospf1.device_attr[dev1].vrf_attr[vrf0].pref_all = 115
        ospf1.device_attr[dev1].vrf_attr[vrf0].nsr_enable = True

        # Add OSPF to the device
        dev1.add_feature(ospf1)

        # Build config
        cfgs = dev1.build_config(apply=False)

        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'router ospf 30',
                ' distance 115',
                ' nsr',
                ' exit',
            ]))

        # Unconfigure nsr
        ospf_uncfg = dev1.build_unconfig(apply=False, attributes={
            'ospf': {
                'device_attr': {
                    dev1.name: 'vrf_attr__default__nsr_enable',
                }
            }
        })

        # Check unconfig strings built correctly
        self.assertMultiLineEqual(
            str(ospf_uncfg),
            '\n'.join([
                'router ospf 30',
                ' no nsr',
                ' exit',
            ]))

    def test_ospf_testbed_build_config(self):

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxe')

        # Create VRF objects
        vrf0 = Vrf('default')
        # Create OSPF object
        ospf1 = Ospf()

        # Add OSPF configurations to vrf default
        ospf1.device_attr[dev1].vrf_attr[vrf0].instance = '30'
        ospf1.device_attr[dev1].vrf_attr[vrf0].pref_all = 115
        ospf1.device_attr[dev1].vrf_attr[vrf0].nsr_enable = True
        ospf1.device_attr[dev2].vrf_attr[vrf0].instance = '30'
        ospf1.device_attr[dev2].vrf_attr[vrf0].pref_all = 115
        ospf1.device_attr[dev2].vrf_attr[vrf0].nsr_enable = True

        # Add OSPF to the device
        dev1.add_feature(ospf1)
        dev2.add_feature(ospf1)

        # Build config
        cfgs = testbed.build_config(apply=False)

        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'router ospf 30',
                ' distance 115',
                ' nsr',
                ' exit',
            ]))
        self.assertMultiLineEqual(
            str(cfgs[dev2.name]),
            '\n'.join([
                'router ospf 30',
                ' distance 115',
                ' nsr',
                ' exit',
            ]))

        # Unconfigure nsr
        ospf_uncfg = testbed.build_unconfig(apply=False, attributes={
            'ospf': {
                'device_attr': {
                    dev1.name: 'vrf_attr__default__nsr_enable',
                }
            }
        })

        # Check unconfig strings built correctly
        self.assertMultiLineEqual(
            str(ospf_uncfg[dev1.name]),
            '\n'.join([
                'router ospf 30',
                ' no nsr',
                ' exit',
            ]))
        # no config for dev2 is expected
        self.assertMultiLineEqual(
            str(ospf_uncfg[dev2.name]), '')

if __name__ == '__main__':
    unittest.main()
