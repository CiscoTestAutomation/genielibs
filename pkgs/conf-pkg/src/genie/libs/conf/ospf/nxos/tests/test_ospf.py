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


class test_ospf(TestCase):

    def test_ospf_config(self):

        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        # Create VRF objects
        vrf0 = Vrf('default')
        vrf1 = Vrf('VRF1')
        vrf2 = Vrf('VRF2')

        # Create Interface object
        intf1 = Interface(name='Ethernet1/2',device=dev1)

        # Create OSPF object
        ospf1 = Ospf()
        ospf1.device_attr[dev1].enabled = True

        # Add OSPF configuration to vrf default
        ospf1.device_attr[dev1].vrf_attr[vrf0].instance = '30'
        ospf1.device_attr[dev1].vrf_attr[vrf0].enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].router_id = '3.3.3.3'
        ospf1.device_attr[dev1].vrf_attr[vrf0].pref_all = 115
        ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_autoconfig = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_auto_config_area_id = '0.0.0.0'
        ospf1.device_attr[dev1].vrf_attr[vrf0].ldp_igp_sync = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_bgp_id = 100
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_bgp_route_map = 'test'
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_connected = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_connected_route_policy = 'test'
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_static = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_static_route_policy = 'test'
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_isis = 'ABC'
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_isis_route_policy = 'test'
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_max_prefix = 12
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_max_prefix_thld = 10
        ospf1.device_attr[dev1].vrf_attr[vrf0].redist_max_prefix_warn_only = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].bfd_enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].log_adjacency_changes = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].log_adjacency_changes_detail = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].auto_cost_enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].auto_cost_reference_bandwidth = 60000
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
        # Add area configuration to VRF default
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].area_te_enable = True
        # Add interface configuration to VRF default
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_admin_control = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_cost = 10
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_type = 'point-to-point'
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_passive = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_priority = 110
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_bfd_enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_bfd_interval = 999
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_bfd_min_interval = 999
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_bfd_multiplier = 7
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_hello_interval = 50
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_dead_interval = 60
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_retransmit_interval = 70
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_auth_trailer_key_chain = 'montreal'
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_auth_trailer_key_crypto_algorithm = 'md5'
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_auth_trailer_key = 'quebec'
        ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_mtu_ignore = True

        # Add OSPF configuration to vrf VRF1
        ospf1.device_attr[dev1].vrf_attr[vrf1].instance = '10'
        ospf1.device_attr[dev1].vrf_attr[vrf1].enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf1].router_id = '1.1.1.1'
        ospf1.device_attr[dev1].vrf_attr[vrf1].auto_cost_enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf1].auto_cost_reference_bandwidth = 600
        ospf1.device_attr[dev1].vrf_attr[vrf1].auto_cost_bandwidth_unit = 'gbps'
        # Add area configuration to vrf VRF1
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].area_type = 'stub'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].summary = False
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].default_cost = 1111
        # Add virtual-link configuration to vrf VRF1
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].virtual_link_attr['OSPF_VL0'].vl_router_id = '7.7.7.7'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].virtual_link_attr['OSPF_VL0'].vl_hello_interval = 55
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].virtual_link_attr['OSPF_VL0'].vl_dead_interval = 65
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].virtual_link_attr['OSPF_VL0'].vl_retransmit_interval = 75
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].virtual_link_attr['OSPF_VL0'].vl_transmit_delay = 85
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].virtual_link_attr['OSPF_VL0'].vl_auth_trailer_key_chain = 'ottawa'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].virtual_link_attr['OSPF_VL0'].vl_auth_trailer_key_crypto_algorithm = 'simple'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].virtual_link_attr['OSPF_VL0'].vl_auth_trailer_key = 'anything'
        # Add sham-link configuration to vrf VRF1
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].sham_link_attr['OSPF_SL0'].sl_local_id = '11.11.11.11'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].sham_link_attr['OSPF_SL0'].sl_remote_id = '12.12.12.12'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].sham_link_attr['OSPF_SL0'].sl_hello_interval = 55
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].sham_link_attr['OSPF_SL0'].sl_dead_interval = 65
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].sham_link_attr['OSPF_SL0'].sl_retransmit_interval = 75
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].sham_link_attr['OSPF_SL0'].sl_transmit_delay = 85
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].sham_link_attr['OSPF_SL0'].sl_auth_trailer_key_chain = 'toronto'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].sham_link_attr['OSPF_SL0'].sl_auth_trailer_key_crypto_algorithm = 'md5'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].sham_link_attr['OSPF_SL0'].sl_auth_trailer_key = 'anything'
        ospf1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].sham_link_attr['OSPF_SL0'].sl_cost = 50
        # Add stub router configuration to vrf VRF1
        sr1 = StubRouter(device=dev1)
        sr1.stub_router_always = True
        sr1.stub_router_external_lsa = True
        sr1.stub_router_include_stub = True
        sr1.stub_router_summary_lsa = True
        ospf1.device_attr[dev1].vrf_attr[vrf1].add_sr_key(sr1)
        
        # Add OSPF configuration to vrf VRF2
        ospf1.device_attr[dev1].vrf_attr[vrf2].instance = '20'
        ospf1.device_attr[dev1].vrf_attr[vrf2].enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf2].router_id = '2.2.2.2'
        ospf1.device_attr[dev1].vrf_attr[vrf2].auto_cost_enable = False
        # Add graceful restart configuration to vrf VRF2
        gr1 = GracefulRestart(device=dev1)
        gr1.gr_enable = True
        gr1.gr_helper_enable = False
        ospf1.device_attr[dev1].vrf_attr[vrf2].add_gr_key(gr1)
        gr2 = GracefulRestart(device=dev1)
        gr2.gr_enable = True
        gr2.gr_restart_interval = 50
        ospf1.device_attr[dev1].vrf_attr[vrf2].add_gr_key(gr2)
        # Add stub router configuration to vrf VRF2
        sr2 = StubRouter(device=dev1)
        sr2.stub_router_on_startup = 50
        sr2.stub_router_external_lsa = True
        sr2.stub_router_include_stub = True
        sr2.stub_router_summary_lsa = True
        ospf1.device_attr[dev1].vrf_attr[vrf2].add_sr_key(sr2)
        # Add area configuration to vrf VRF2
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['2'].area_type = 'nssa'
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['2'].summary = False
        ospf1.device_attr[dev1].vrf_attr[vrf2].area_attr['2'].default_cost = 1111
        # Add area range configuration to vrf VRF2
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
                'feature ospf',
                'router ospf 30',
                ' no shutdown',
                ' router-id 3.3.3.3',
                ' distance 115',
                ' mpls ldp autoconfig area 0.0.0.0',
                ' mpls ldp sync',
                ' redistribute bgp 100 route-map test',
                ' redistribute direct route-map test',
                ' redistribute static route-map test',
                ' redistribute isis ABC route-map test',
                ' redistribute maximum-prefix 12 10 warning-only',
                ' bfd',
                ' log-adjacency-changes detail',
                ' auto-cost reference-bandwidth 60000',
                ' maximum-paths 15',
                ' timers throttle spf 600 700 800',
                ' timers throttle lsa 600 700 800',
                ' max-lsa 123',
                ' default-information originate always',
                ' mpls traffic-eng area 0',
                ' exit',
                'router ospf 10',
                ' vrf VRF1',
                '  no shutdown',
                '  router-id 1.1.1.1',
                '  auto-cost reference-bandwidth 600 gbps',
                '  max-metric router-lsa external-lsa include-stub summary-lsa',
                '  area 1 stub no-summary',
                '  area 1 default-cost 1111',
                '  area 1 virtual-link 7.7.7.7',
                '   hello-interval 55',
                '   dead-interval 65',
                '   retransmit-interval 75',
                '   transmit-delay 85',
                '   authentication key-chain ottawa',
                '   authentication',
                '   authentication-key anything',
                '   exit',
                '  area 1 sham-link 11.11.11.11 12.12.12.12',
                '   hello-interval 55',
                '   dead-interval 65',
                '   retransmit-interval 75',
                '   transmit-delay 85',
                '   authentication key-chain toronto',
                '   authentication message-digest',
                '   message-digest-key 1 md5 anything',
                '   cost 50',
                '   exit',
                '  exit',
                ' exit',
                'router ospf 20',
                ' vrf VRF2',
                '  no shutdown',
                '  router-id 2.2.2.2',
                '  graceful-restart helper-disable',
                '  graceful-restart grace-period 50',
                '  no auto-cost reference-bandwidth',
                '  max-metric router-lsa external-lsa include-stub on-startup 50 summary-lsa',
                '  area 2 nssa no-summary',
                '  area 2 default-cost 1111',
                '  area 2 range 1.1.1.1 255.255.255.0 not-advertise cost 10',
                '  area 2 range 2.2.2.2 255.255.255.255 advertise',
                '  exit',
                ' exit',
                'interface Ethernet1/2',
                ' ip router ospf 30 area 0',
                ' ip ospf cost 10',
                ' ip ospf network point-to-point',
                ' ip ospf passive-interface',
                ' ip ospf priority 110',
                ' ip ospf bfd',
                ' bfd interval 999 min_rx 999 multiplier 7',
                ' ip ospf hello-interval 50',
                ' ip ospf dead-interval 60',
                ' ip ospf retransmit-interval 70',
                ' ip ospf authentication key-chain montreal',
                ' ip ospf authentication message-digest',
                ' ip ospf message-digest-key 1 md5 quebec',
                ' ip ospf mtu-ignore',
                ' exit',
            ]))

        # Unconfig
        ospf_uncfg = ospf1.build_unconfig(apply=False)

        # Check unconfig strings built correctly
        self.assertMultiLineEqual(
            str(ospf_uncfg[dev1.name]),
            '\n'.join([
                'no feature ospf',
            ]))


    def test_ospf_config2(self):

        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        # Create VRF objects
        vrf0 = Vrf('default')
        # Create OSPF object
        ospf1 = Ospf()
        ospf1.device_attr[dev1].enabled = True

        # Add OSPF configurations to vrf default
        ospf1.device_attr[dev1].vrf_attr[vrf0].instance = '1'
        ospf1.device_attr[dev1].vrf_attr[vrf0].enable = True
        ospf1.device_attr[dev1].vrf_attr[vrf0].router_id = '1.1.1.1'

        # Add OSPF to the device
        dev1.add_feature(ospf1)
        
        # Build config
        cfgs = ospf1.build_config(apply=False)

        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'feature ospf',
                'router ospf 1',
                ' no shutdown',
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
