#!/usr/bin/env python

# Python
import unittest
from unittest.mock import Mock
from genie.libs.conf.ospfv3.summaryaddress import SummaryAddress

# Genie package
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

# Genie Conf
from genie.libs.conf.vrf import Vrf
from genie.libs.conf.interface import Interface
from genie.libs.conf.ospfv3 import Ospfv3
from genie.libs.conf.ospfv3.gracefulrestart import GracefulRestart
from genie.libs.conf.ospfv3.summaryaddress import SummaryAddress
from genie.libs.conf.ospfv3.arearange import AreaRange
from genie.libs.conf.ospfv3.areadefaultcost import AreaDefaultCost
from genie.libs.conf.ospfv3.arearoutemap import AreaRouteMap


class test_ospfv3(TestCase):

    def test_ospfv3_config(self):

        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        # Create VRF objects
        vrf0 = Vrf('default')
        vrf1 = Vrf('VRF1')

        # Create Interface object
        intf1 = Interface(name='Ethernet1/1', device=dev1)

        # Create OSPF object
        ospfv3_1 = Ospfv3()
        ospfv3_1.device_attr[dev1].enabled = True

        # Add OSPF configuration to vrf default
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].instance = '30'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].inst_shutdown = False
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].router_id = '3.3.3.3'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].passive_interface = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].log_adjacency_changes = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].log_adjacency_changes_detail = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].lsa_arrival = 30
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].lsa_group_pacing = 40
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].lsa_start_time = 50
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].lsa_hold_time = 60
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].lsa_max_time = 70
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].bfd_enable = True

        # Add graceful restart configuration to vrf default
        gr1 = GracefulRestart(device=dev1)
        gr1.gr_enable = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].add_gr_key(gr1)
        # Add graceful restart configuration to vrf default
        gr2 = GracefulRestart(device=dev1)
        gr2.gr_enable = True
        gr2.gr_restart_interval = 100
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].add_gr_key(gr2)
        # # Add graceful restart configuration to vrf default
        gr3 = GracefulRestart(device=dev1)
        gr3.gr_enable = True
        gr3.gr_helper_enable = False
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].add_gr_key(gr3)
        # # Add graceful restart configuration to vrf default
        gr4 = GracefulRestart(device=dev1)
        gr4.gr_enable = True
        gr4.gr_planned_only = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].add_gr_key(gr4)

        # Add area configuration to vrf default
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['1'].area_type = 'stub'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['1'].nosummary = False
        # Add area configuration to vrf default
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['2'].area_type = 'nssa'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['2'].nosummary = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['2'].nssa_default_info_originate = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['2'].nssa_route_map = 'test_route_map'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['2'].nssa_translate_always = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['2'].nssa_translate_supressfa = True

        # address_family attributes
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].default_metric = 100

        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].redist_bgp_id = 100
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].redist_bgp_route_map = 'test'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].redist_rip_id = 'rip-nxos'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].redist_rip_route_map = 'test'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].redist_direct = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr[
            'ipv6 unicast'].redist_direct_route_map = 'test'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].redist_static = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].redist_static_route_map = 'test'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].redist_isis_id = 'ABC'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].redist_isis_route_map = 'test'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].default_originate = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].default_originate_routemap = 'test'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].redist_max_prefix = 12
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].redist_max_prefix_thld = 10

        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].redist_max_prefix_retries = 5
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].redist_max_prefix_withdraw = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr[
            'ipv6 unicast'].redist_max_prefix_retries_timeout = 10
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].spf_start_time = 100
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].spf_hold_time = 200
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].spf_max_time = 300
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].table_map = 'test'

        # Add area default cost configuration to vrf default
        ad1 = AreaDefaultCost(device=dev1)
        ad1.af_area_id = '2'
        ad1.area_def_cost = 10
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].add_areacost_key(
            ad1)

        # # Add area routemap direction to vrf default
        arm1 = AreaRouteMap(device=dev1)
        arm1.routemap_area_id = '2'
        arm1.ar_route_map_in = 'test_in'
        arm1.ar_route_map_out = 'test_out'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].add_arearoutemap_key(
            arm1)

        # Add summary address configuration to vrf default
        sa1 = SummaryAddress(device=dev1)
        sa1.summary_address_prefix = '2001:db1:1::1/64'
        sa1.summary_address_not_advertise = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].add_sumadd_key(
            sa1)

        # Add summary address configuration to vrf default
        sa2 = SummaryAddress(device=dev1)
        sa2.summary_address_prefix = '2001:db2:2::2/64'
        sa2.summary_address_tag = 10
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].add_sumadd_key(
            sa2)

        # Add area range configuration to vrf default
        ar1 = AreaRange(device=dev1)
        ar1.range_area_id = '2'
        ar1.area_range_prefix = '2001:bd12:2::2/64'
        ar1.area_range_not_advertise = True
        ar1.area_range_cost = 10
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].address_family_attr['ipv6 unicast'].add_arearange_key(
            ar1)

        # virtual link attributes
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['7'].virtual_link_attr['ospfv3_vl1'].vl_router_id = '7.7.7.7'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['7'].virtual_link_attr['ospfv3_vl1'].vl_hello_interval = 55
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['7'].virtual_link_attr['ospfv3_vl1'].vl_dead_interval = 65
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['7'].virtual_link_attr['ospfv3_vl1'].vl_retransmit_interval = 75
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['7'].virtual_link_attr['ospfv3_vl1'].vl_transmit_delay = 85

        # Add interface configuration to VRF default
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_admin_control = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_secondaries = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_cost = 10
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_type = 'point-to-point'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_bfd_enable = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_passive = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_priority = 110
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_hello_interval = 50
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_dead_interval = 60
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_retransmit_interval = 70
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_transmit_delay = 70
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_mtu_ignore = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_instance = 60
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_protocol_shutdown = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_multi_area = 10

        dev1.add_feature(ospfv3_1)

        # Build config
        cfgs = ospfv3_1.build_config(apply=False)

        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'feature ospfv3',
                'router ospfv3 30',
                ' router-id 3.3.3.3',
                ' passive-interface default',
                ' log-adjacency-changes detail',
                ' bfd',
                ' timers lsa-arrival 30',
                ' timers lsa-group-pacing 40',
                ' timers throttle lsa 50 60 70',
                ' graceful-restart',
                ' graceful-restart grace-period 100',
                ' graceful-restart helper-disable',
                ' graceful-restart planned-only',
                ' address-family ipv6 unicast',
                '  default-information originate True route-map test',
                '  default-metric 100',
                '  redistribute bgp 100 route-map test',
                '  redistribute direct route-map test',
                '  redistribute static route-map test',
                '  redistribute isis ABC route-map test',
                '  redistribute rip rip-nxos route-map test',
                '  redistribute maximum-prefix 12 10 withdraw 5 10',
                '  table-map test',
                '  timers throttle lsa 100 200 300',
                '  area 2 default-cost 10',
                '  area 2 filter-list route-map test_in in',
                '  area 2 filter-list route-map test_out out',
                '  summary-address 2001:db1:1::1/64 not-advertise',
                '  summary-address 2001:db2:2::2/64 tag 10',
                '  area 2 range 2001:bd12:2::2/64 not-advertise cost 10',
                '  exit',
                ' area 1 stub',
                ' area 2 nssa no-summary default-information-originate route-map test_route_map',
                ' area 2 nssa translate type7 always suppress-fa',
                ' area 7 virtual-link 7.7.7.7',
                '  hello-interval 55',
                '  dead-interval 65',
                '  retransmit-interval 75',
                '  transmit-delay 85',
                '  exit',
                ' exit',
                'interface Ethernet1/1',
                ' ipv6 router ospfv3 30 area 0',
                ' ospfv3 cost 10',
                ' ospfv3 network point-to-point',
                ' ospfv3 bfd',
                ' ospfv3 passive-interface',
                ' ospfv3 priority 110',
                ' ospfv3 hello-interval 50',
                ' ospfv3 dead-interval 60',
                ' ospfv3 retransmit-interval 70',
                ' ospfv3 mtu-ignore',
                ' ospfv3 instance 60',
                ' ospfv3 shutdown',
                ' ospfv3 transmit-delay 70',
                ' ipv6 router ospfv3 30 multi-area 10',
                ' exit'
            ]))

        # Unconfig
        ospfv3_uncfg = ospfv3_1.build_unconfig(apply=False)

        # Check unconfig strings built correctly
        self.assertMultiLineEqual(
            str(ospfv3_uncfg[dev1.name]),
            '\n'.join([
                'no feature ospfv3',
            ]))

    def test_ospfv3_non_default_vrf_config(self):

        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        # Create VRF objects
        vrf1 = Vrf('VRF1')

        # Create Interface object
        intf1 = Interface(name='Ethernet1/1', device=dev1)

        # Create OSPF object
        ospfv3_1 = Ospfv3()
        ospfv3_1.device_attr[dev1].enabled = True

        # Add OSPF configuration to vrf VRF1
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].instance = '30'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].inst_shutdown = False
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].router_id = '3.3.3.3'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].passive_interface = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].log_adjacency_changes = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].log_adjacency_changes_detail = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].lsa_arrival = 30
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].lsa_group_pacing = 40
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].lsa_start_time = 50
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].lsa_hold_time = 60
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].lsa_max_time = 70

        # Add graceful restart configuration to vrf default
        gr1 = GracefulRestart(device=dev1)
        gr1.gr_enable = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].add_gr_key(gr1)
        # Add graceful restart configuration to vrf default
        gr2 = GracefulRestart(device=dev1)
        gr2.gr_enable = True
        gr2.gr_restart_interval = 100
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].add_gr_key(gr2)
        # # Add graceful restart configuration to vrf default
        gr3 = GracefulRestart(device=dev1)
        gr3.gr_enable = True
        gr3.gr_helper_enable = False
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].add_gr_key(gr3)
        # # Add graceful restart configuration to vrf default
        gr4 = GracefulRestart(device=dev1)
        gr4.gr_enable = True
        gr4.gr_planned_only = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].add_gr_key(gr4)

        # Add area configuration to vrf default
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].area_type = 'stub'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].nosummary = False
        # Add area configuration to vrf default
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['2'].area_type = 'nssa'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['2'].nosummary = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['2'].nssa_default_info_originate = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['2'].nssa_route_map = 'test_route_map'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['2'].nssa_translate_always = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['2'].nssa_translate_supressfa = True

        # address_family attributes
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].default_metric = 100

        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].redist_bgp_id = 100
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].redist_bgp_route_map = 'test'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].redist_rip_id = 'rip-nxos'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].redist_rip_route_map = 'test'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].redist_direct = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr[
            'ipv6 unicast'].redist_direct_route_map = 'test'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].redist_static = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].redist_static_route_map = 'test'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].redist_isis_id = 'ABC'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].redist_isis_route_map = 'test'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].default_originate = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].default_originate_routemap = 'test'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].redist_max_prefix = 12
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].redist_max_prefix_thld = 10
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].redist_max_prefix_warn_only = True

        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].spf_start_time = 100
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].spf_hold_time = 200
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].spf_max_time = 300
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].table_map = 'test'

        # Add area default cost configuration to vrf default
        ad1 = AreaDefaultCost(device=dev1)
        ad1.af_area_id = '2'
        ad1.area_def_cost = 10
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].add_areacost_key(
            ad1)

        # # Add area routemap direction to vrf default
        arm1 = AreaRouteMap(device=dev1)
        arm1.routemap_area_id = '2'
        arm1.ar_route_map_in = 'test_in'
        arm1.ar_route_map_out = 'test_out'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].add_arearoutemap_key(
            arm1)

        # Add summary address configuration to vrf default
        sa1 = SummaryAddress(device=dev1)
        sa1.summary_address_prefix = '2001:db1:1::1/64'
        sa1.summary_address_not_advertise = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].add_sumadd_key(
            sa1)

        # Add summary address configuration to vrf default
        sa2 = SummaryAddress(device=dev1)
        sa2.summary_address_prefix = '2001:db2:2::2/64'
        sa2.summary_address_tag = 10
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].add_sumadd_key(
            sa2)

        # Add area range configuration to vrf default
        ar1 = AreaRange(device=dev1)
        ar1.range_area_id = '2'
        ar1.area_range_prefix = '2001:bd12:2::2/64'
        ar1.area_range_not_advertise = True
        ar1.area_range_cost = 10
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].add_arearange_key(
            ar1)

        # virtual link attributes
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['7'].virtual_link_attr['ospfv3_vl1'].vl_router_id = '7.7.7.7'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['7'].virtual_link_attr['ospfv3_vl1'].vl_hello_interval = 55
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['7'].virtual_link_attr['ospfv3_vl1'].vl_dead_interval = 65
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['7'].virtual_link_attr['ospfv3_vl1'].vl_retransmit_interval = 75
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['7'].virtual_link_attr['ospfv3_vl1'].vl_transmit_delay = 85

        # Add interface configuration to VRF default
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['0'].interface_attr[intf1].if_admin_control = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['0'].interface_attr[intf1].if_secondaries = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['0'].interface_attr[intf1].if_cost = 10
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['0'].interface_attr[intf1].if_type = 'point-to-point'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['0'].interface_attr[intf1].if_passive = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['0'].interface_attr[intf1].if_priority = 110
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['0'].interface_attr[intf1].if_hello_interval = 50
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['0'].interface_attr[intf1].if_dead_interval = 60
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['0'].interface_attr[intf1].if_retransmit_interval = 70
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['0'].interface_attr[intf1].if_transmit_delay = 70
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['0'].interface_attr[intf1].if_mtu_ignore = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['0'].interface_attr[intf1].if_instance = 60
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['0'].interface_attr[intf1].if_protocol_shutdown = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['0'].interface_attr[intf1].if_multi_area = 10

        dev1.add_feature(ospfv3_1)

        # Build config
        cfgs = ospfv3_1.build_config(apply=False)

        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'feature ospfv3',
                'router ospfv3 30',
                ' vrf VRF1',
                '  router-id 3.3.3.3',
                '  passive-interface default',
                '  log-adjacency-changes detail',
                '  timers lsa-arrival 30',
                '  timers lsa-group-pacing 40',
                '  timers throttle lsa 50 60 70',
                '  graceful-restart',
                '  graceful-restart grace-period 100',
                '  graceful-restart helper-disable',
                '  graceful-restart planned-only',
                '  address-family ipv6 unicast',
                '   default-information originate True route-map test',
                '   default-metric 100',
                '   redistribute bgp 100 route-map test',
                '   redistribute direct route-map test',
                '   redistribute static route-map test',
                '   redistribute isis ABC route-map test',
                '   redistribute rip rip-nxos route-map test',
                '   redistribute maximum-prefix 12 10 warning-only',
                '   table-map test',
                '   timers throttle lsa 100 200 300',
                '   area 2 default-cost 10',
                '   area 2 filter-list route-map test_in in',
                '   area 2 filter-list route-map test_out out',
                '   summary-address 2001:db1:1::1/64 not-advertise',
                '   summary-address 2001:db2:2::2/64 tag 10',
                '   area 2 range 2001:bd12:2::2/64 not-advertise cost 10',
                '   exit',
                '  area 1 stub',
                '  area 2 nssa no-summary default-information-originate route-map test_route_map',
                '  area 2 nssa translate type7 always suppress-fa',
                '  area 7 virtual-link 7.7.7.7',
                '   hello-interval 55',
                '   dead-interval 65',
                '   retransmit-interval 75',
                '   transmit-delay 85',
                '   exit',
                '  exit',
                ' exit',
                'interface Ethernet1/1',
                ' ipv6 router ospfv3 30 area 0',
                ' ospfv3 cost 10',
                ' ospfv3 network point-to-point',
                ' ospfv3 passive-interface',
                ' ospfv3 priority 110',
                ' ospfv3 hello-interval 50',
                ' ospfv3 dead-interval 60',
                ' ospfv3 retransmit-interval 70',
                ' ospfv3 mtu-ignore',
                ' ospfv3 instance 60',
                ' ospfv3 shutdown',
                ' ospfv3 transmit-delay 70',
                ' ipv6 router ospfv3 30 multi-area 10',
                ' exit'
            ]))

        # Unconfig
        ospfv3_uncfg = ospfv3_1.build_unconfig(apply=False)

        # Check unconfig strings built correctly
        self.assertMultiLineEqual(
            str(ospfv3_uncfg[dev1.name]),
            '\n'.join([
                'no feature ospfv3',
            ]))

    def test_ospfv3_partial_config_unconfig(self):

        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        # Create VRF objects
        vrf1 = Vrf('VRF1')

        # Create Interface object
        intf1 = Interface(name='Ethernet1/1', device=dev1)

        # Create OSPF object
        ospfv3_1 = Ospfv3()
        ospfv3_1.device_attr[dev1].enabled = True

        # Add OSPF configuration to vrf default
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].instance = '30'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].inst_shutdown = False
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].router_id = '3.3.3.3'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].passive_interface = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].log_adjacency_changes = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].log_adjacency_changes_detail = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].lsa_arrival = 30
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].lsa_group_pacing = 40
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].lsa_start_time = 50
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].lsa_hold_time = 60
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].lsa_max_time = 70

        # Add graceful restart configuration to vrf vrf1
        gr1 = GracefulRestart(device=dev1)
        gr1.gr_enable = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].add_gr_key(gr1)
        # Add graceful restart configuration to vrf vrf1
        gr2 = GracefulRestart(device=dev1)
        gr2.gr_enable = True
        gr2.gr_restart_interval = 100
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].add_gr_key(gr2)
        # # Add graceful restart configuration to vrf vrf1
        gr3 = GracefulRestart(device=dev1)
        gr3.gr_enable = True
        gr3.gr_helper_enable = False
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].add_gr_key(gr3)
        # # Add graceful restart configuration to vrf vrf1
        gr4 = GracefulRestart(device=dev1)
        gr4.gr_enable = True
        gr4.gr_planned_only = True
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].add_gr_key(gr4)

        # Add area configuration to vrf vrf1
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].area_type = 'stub'
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].area_attr['1'].nosummary = True

        # Add summary address configuration to vrf vrf1
        sa2 = SummaryAddress(device=dev1)
        sa2.summary_address_prefix = '2001:db2:2::2/64'
        sa2.summary_address_tag = 10
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].address_family_attr['ipv6 unicast'].add_sumadd_key(
            sa2)

        dev1.add_feature(ospfv3_1)

        # Build config
        cfgs = ospfv3_1.build_config(apply=False)

        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'feature ospfv3',
                'router ospfv3 30',
                ' vrf VRF1',
                '  router-id 3.3.3.3',
                '  passive-interface default',
                '  log-adjacency-changes detail',
                '  timers lsa-arrival 30',
                '  timers lsa-group-pacing 40',
                '  timers throttle lsa 50 60 70',
                '  graceful-restart',
                '  graceful-restart grace-period 100',
                '  graceful-restart helper-disable',
                '  graceful-restart planned-only',
                '  address-family ipv6 unicast',
                '   summary-address 2001:db2:2::2/64 tag 10',
                '   exit',
                '  area 1 stub no-summary',
                '  exit',
                ' exit'
            ]))
        # change partial config - router_id
        ospfv3_1.device_attr[dev1].vrf_attr[vrf1].router_id = '7.7.7.7'
        partial_cfg1 = ospfv3_1.build_config(
            apply=False,
            attributes={'device_attr':
                        {'*': {'vrf_attr':
                               {'*': "router_id"}}}})
        self.assertCountEqual(partial_cfg1.keys(), [dev1.name])
        self.assertMultiLineEqual(str(partial_cfg1[dev1.name]), '\n'.
                                  join([
                                      'router ospfv3 30',
                                      ' vrf VRF1',
                                      '  router-id 7.7.7.7',
                                      '  exit',
                                      ' exit',
                                  ]))

        # remove cfg - area 1 stub
        partial_uncfg1 = ospfv3_1.build_unconfig(
            apply=False,
            attributes={'device_attr':
                        {'*': {'vrf_attr':
                               {'*': "lsa_arrival"}}}})

        self.assertMultiLineEqual(str(partial_uncfg1[dev1.name]), '\n'.
                                  join([
                                      'router ospfv3 30',
                                      ' vrf VRF1',
                                      '  no timers lsa-arrival 30',
                                      '  exit',
                                      ' exit',
                                  ]))

        # # remove a single attribute from a specific gr key
        partial_uncfg2 = ospfv3_1.build_unconfig(
            apply=False, attributes={'device_attr': {'*': {'vrf_attr': {'*': {'gr_keys': {gr4: {'gr_enable': None}}}}}}})

        self.assertMultiLineEqual(str(partial_uncfg2[dev1.name]), '\n'.
                                  join([
                                      'router ospfv3 30',
                                      ' vrf VRF1',
                                      '  no graceful-restart',
                                      '  exit',
                                      ' exit',
                                  ]))

        # remove all grace full restart multiline configs
        partial_uncfg3 = ospfv3_1.build_unconfig(
            apply=False, attributes={'device_attr': {'*': {'vrf_attr': {'*': 'gr_keys'}}}})

        self.assertMultiLineEqual(str(partial_uncfg3[dev1.name]), '\n'.
                                  join([
                                      'router ospfv3 30',
                                      ' vrf VRF1',
                                      '  no graceful-restart',
                                      '  no graceful-restart grace-period 100',
                                      '  no graceful-restart helper-disable',
                                      '  no graceful-restart planned-only',
                                      '  exit',
                                      ' exit',
                                  ]))


if __name__ == '__main__':
    unittest.main()
