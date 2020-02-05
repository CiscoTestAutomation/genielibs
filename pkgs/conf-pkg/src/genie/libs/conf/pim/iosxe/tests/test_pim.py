#!/usr/bin/env python

# Python
import unittest
from unittest.mock import Mock

# Genie
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface
from genie.conf.base.attributes import UnsupportedAttributeWarning

# PIM
from genie.libs.conf.vrf import Vrf
from genie.libs.conf.pim import Pim
from genie.libs.conf.pim.rp_address import RPAddressGroup


class test_pim(TestCase):

    def setUp(self):
        
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed
        
        # Device
        self.dev1 = Device(name='PE1', testbed=testbed, os='iosxe')

    def test_pim_full_config(self):

        # For failures
        self.maxDiff = None

        # shorten the line
        dev1 = self.dev1
        
        # Pim object
        pim = Pim()
        dev1.add_feature(pim)

        # Apply configuration

        # VRF configuration
        vrf1 = Vrf('default')
        pim.device_attr[self.dev1].vrf_attr[vrf1]
        vrf2 = Vrf('red')
        pim.device_attr[self.dev1].vrf_attr[vrf2]
        pim.device_attr[dev1].enabled_bidir = True

        for vrf, intf in {vrf1: 'GigabitEthernet0/0/1', vrf2: 'GigabitEthernet0/0/2'}.items():
            # == auto-rp ===
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                send_rp_announce_rp_group = '1.1.1.1'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                send_rp_announce_scope = 20
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                send_rp_announce_group_list = 'test_list'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                send_rp_announce_interval = 60
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                send_rp_announce_bidir = True

            # == auto-rp discovery===
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                send_rp_discovery_intf = intf
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                send_rp_discovery_scope = 20
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                send_rp_discovery_interval = 1000

            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                autorp_listener = True

            # == bsr candidate ===
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                bsr_candidate_interface = intf
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                bsr_candidate_hash_mask_length = 20
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                bsr_candidate_priority = 50
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                bsr_candidate_accept_rp_acl = 190

            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                bsr_candidate_address = '2001:DB8:1:1::1'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                bsr_candidate_hash_mask_length = 126
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                bsr_candidate_priority = 20
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                bsr_candidate_accept_rp_acl = 190
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                scope = True

            # == bsr rp-candidate ===
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                bsr_rp_candidate_interface = 'Loopback0'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                bsr_rp_candidate_group_list = '11'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                bsr_rp_candidate_priority = 10
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                bsr_rp_candidate_interval = 60
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                bsr_rp_candidate_bidir = True

            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                bsr_rp_candidate_address = '2001:DB8:2:2::2'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                bsr_rp_candidate_group_list = 'ff1e:abcd:def1::0/64'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                bsr_rp_candidate_priority = 10
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                bsr_rp_candidate_interval = 60

            # == static RP ===
            rp1 = RPAddressGroup(device=self.dev1)
            rp1.static_rp_address = '1.1.1.1'
            rp1.static_rp_group_list = '10'
            rp1.static_rp_override = True
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].add_static_rp(rp1)


            rp2 = RPAddressGroup(device=self.dev1)
            rp2.static_rp_address = '2001:db8:1:1::1'
            rp2.static_rp_group_list = 'ff1e:abcd:def1::0/64'
            rp2.static_rp_bidir = True
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].add_static_rp(rp2)

            # == static rp register ===
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                accept_register = 'regist_name'

            # ipv6
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                accept_register = 'regist_map_v6'

            # log-neighbor-changes
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                log_neighbor_changes = True
            # ipv6 is not supported

            # register_source
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                register_source = intf
            # not ipv6 supported
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                register_source = 'Loopback0'

            # == sg-expiry-timer ==
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                sg_expiry_timer = 182
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                sg_expiry_timer_sg_list = 'sg_name'

            # == spt-threshold ==
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                spt_switch_infinity = 0
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                spt_switch_policy = 'abcde'

            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                spt_switch_infinity = 'infinity'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                spt_switch_policy = 'abcdef'


            # == interface ==
            intf = 'Loopback0'
            # ----   mode  ----------
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                interface_attr[intf].mode = 'dense-mode'

            # ----   jp-policy  ----------
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                interface_attr[intf].boundary = 'test'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                interface_attr[intf].boundary_filter_autorp = True
            
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                interface_attr[intf].boundary = 'test'

            # ----   border  ----------
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                interface_attr[intf].bsr_border = True
            
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                interface_attr[intf].bsr_border = True

            # ----   hello-interval  ----------
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                interface_attr[intf].hello_interval_msec = 30000
            
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                interface_attr[intf].hello_interval = 3000

            # ----   dr-priority  ----------
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                interface_attr[intf].dr_priority = 777
            
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                interface_attr[intf].dr_priority = 777

            # ----   neighbor-policy  ----------
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                interface_attr[intf].neighbor_filter = 'pim_neighbor_policy'
            
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                interface_attr[intf].neighbor_filter = 'pim_neighbor_policy'
        
        # Build config
        cfgs = pim.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'ip pim bidir-enable',
                'ip pim send-rp-announce 1.1.1.1 scope 20 group-list test_list interval 60 bidir',
                'ip pim send-rp-discovery GigabitEthernet0/0/1 scope 20 interval 1000',
                'ip pim autorp listener',
                'ip pim bsr-candidate GigabitEthernet0/0/1 20 50 accept-rp-candidate 190',
                'ip pim rp-candidate Loopback0 group-list 11 interval 60 priority 10 bidir',
                'ip pim accept-register list regist_name',
                'ip pim log-neighbor-changes',
                'ip pim register-source GigabitEthernet0/0/1',
                'ip pim sparse sg-expiry-timer 182 sg-list sg_name',
                'ip pim spt-threshold 0 group-list abcde',
                'ip pim rp-address 1.1.1.1 10 override',
                'interface Loopback0',
                ' ip pim dense-mode',
                ' ip multicast boundary test filter-autorp',
                ' ip pim bsr-border',
                ' ip pim dr-priority 777',
                ' ip pim query-interval 30000 msec',
                ' ip pim neighbor-filter pim_neighbor_policy',
                ' exit',
                'ipv6 pim bsr candidate rp 2001:DB8:2:2::2 group-list ff1e:abcd:def1::0/64 interval 60 priority 10',
                'ipv6 pim accept-register list regist_map_v6',
                'ipv6 pim register-source Loopback0',
                'ipv6 pim spt-threshold infinity group-list abcdef',
                'ipv6 pim rp-address 2001:db8:1:1::1 ff1e:abcd:def1::0/64 bidir',
                'interface Loopback0',
                ' ipv6 multicast boundary block source',
                ' ipv6 pim bsr border',
                ' ipv6 pim dr-priority 777',
                ' ipv6 pim hello-interval 3000',
                ' exit',
                'ipv6 pim neighbor-filter list pim_neighbor_policy',
                'ip pim vrf red send-rp-announce 1.1.1.1 scope 20 group-list test_list interval 60 bidir',
                'ip pim vrf red send-rp-discovery GigabitEthernet0/0/2 scope 20 interval 1000',
                'ip pim autorp listener',
                'ip pim vrf red bsr-candidate GigabitEthernet0/0/2 20 50 accept-rp-candidate 190',
                'ip pim vrf red rp-candidate Loopback0 group-list 11 interval 60 priority 10 bidir',
                'ip pim accept-register list regist_name',
                'ip pim log-neighbor-changes',
                'ip pim vrf red register-source GigabitEthernet0/0/2',
                'ip pim vrf red sparse sg-expiry-timer 182 sg-list sg_name',
                'ip pim vrf red spt-threshold 0 group-list abcde',
                'ip pim vrf red rp-address 1.1.1.1 10 override',
                'interface Loopback0',
                ' ip pim dense-mode',
                ' ip multicast boundary test filter-autorp',
                ' ip pim bsr-border',
                ' ip pim dr-priority 777',
                ' ip pim query-interval 30000 msec',
                ' ip pim neighbor-filter pim_neighbor_policy',
                ' exit',
                'ipv6 pim vrf red bsr candidate rp 2001:DB8:2:2::2 group-list ff1e:abcd:def1::0/64 interval 60 priority 10',
                'ipv6 pim vrf red accept-register list regist_map_v6',
                'ipv6 pim vrf red register-source Loopback0',
                'ipv6 pim vrf red spt-threshold infinity group-list abcdef',
                'ipv6 pim vrf red rp-address 2001:db8:1:1::1 ff1e:abcd:def1::0/64 bidir',
                'interface Loopback0',
                ' ipv6 multicast boundary block source',
                ' ipv6 pim bsr border',
                ' ipv6 pim dr-priority 777',
                ' ipv6 pim hello-interval 3000',
                ' exit',
                'ipv6 pim vrf red neighbor-filter list pim_neighbor_policy',
            ]))

        cfgs = pim.build_unconfig(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'no ip pim bidir-enable',
                'no ip pim send-rp-discovery GigabitEthernet0/0/1 scope 20 interval 1000',
                'no ip pim autorp listener',
                'no ip pim bsr-candidate GigabitEthernet0/0/1 20 50 accept-rp-candidate 190',
                'no ip pim accept-register list regist_name',
                'no ip pim log-neighbor-changes',
                'no ip pim register-source GigabitEthernet0/0/1',
                'no ip pim sparse sg-expiry-timer 182 sg-list sg_name',
                'no ip pim spt-threshold 0 group-list abcde',
                'no ip pim rp-address 1.1.1.1 10 override',
                'interface Loopback0',
                ' no ip pim dense-mode',
                ' no ip multicast boundary test filter-autorp',
                ' no ip pim bsr-border',
                ' no ip pim dr-priority 777',
                ' no ip pim query-interval 30000 msec',
                ' no ip pim neighbor-filter pim_neighbor_policy',
                ' exit',
                'no ipv6 pim bsr candidate rp 2001:DB8:2:2::2 group-list ff1e:abcd:def1::0/64 interval 60 priority 10',
                'no ipv6 pim accept-register list regist_map_v6',
                'no ipv6 pim register-source Loopback0',
                'no ipv6 pim spt-threshold infinity group-list abcdef',
                'no ipv6 pim rp-address 2001:db8:1:1::1 ff1e:abcd:def1::0/64 bidir',
                'interface Loopback0',
                ' no ipv6 multicast boundary block source',
                ' no ipv6 pim bsr border',
                ' no ipv6 pim dr-priority 777',
                ' no ipv6 pim hello-interval 3000',
                ' exit',
                'no ipv6 pim neighbor-filter list pim_neighbor_policy',
                'no ip pim vrf red send-rp-discovery GigabitEthernet0/0/2 scope 20 interval 1000',
                'no ip pim autorp listener',
                'no ip pim vrf red bsr-candidate GigabitEthernet0/0/2 20 50 accept-rp-candidate 190',
                'no ip pim accept-register list regist_name',
                'no ip pim log-neighbor-changes',
                'no ip pim vrf red register-source GigabitEthernet0/0/2',
                'no ip pim vrf red sparse sg-expiry-timer 182 sg-list sg_name',
                'no ip pim vrf red spt-threshold 0 group-list abcde',
                'no ip pim vrf red rp-address 1.1.1.1 10 override',
                'interface Loopback0',
                ' no ip pim dense-mode',
                ' no ip multicast boundary test filter-autorp',
                ' no ip pim bsr-border',
                ' no ip pim dr-priority 777',
                ' no ip pim query-interval 30000 msec',
                ' no ip pim neighbor-filter pim_neighbor_policy',
                ' exit',
                'no ipv6 pim vrf red bsr candidate rp 2001:DB8:2:2::2 group-list ff1e:abcd:def1::0/64 interval 60 priority 10',
                'no ipv6 pim vrf red accept-register list regist_map_v6',
                'no ipv6 pim vrf red register-source Loopback0',
                'no ipv6 pim vrf red spt-threshold infinity group-list abcdef',
                'no ipv6 pim vrf red rp-address 2001:db8:1:1::1 ff1e:abcd:def1::0/64 bidir',
                'interface Loopback0',
                ' no ipv6 multicast boundary block source',
                ' no ipv6 pim bsr border',
                ' no ipv6 pim dr-priority 777',
                ' no ipv6 pim hello-interval 3000',
                ' exit',
                'no ipv6 pim vrf red neighbor-filter list pim_neighbor_policy',
            ]))

        # uncfg with attributes
            # pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            #     interface_attr[intf].mode = 'dense-mode'
        cfgs = pim.build_unconfig(apply=False,
                                  attributes={'device_attr': {
                                                self.dev1: {
                                                    'vrf_attr': {
                                                        'default': {
                                                            'address_family_attr': {
                                                                'ipv6': {
                                                                    'register_source': None
                                                                }
                                                            }
                                                        },
                                                        'red': {
                                                            'address_family_attr': {
                                                                'ipv4': {
                                                                    'interface_attr': {
                                                                        intf: {
                                                                            'mode': None
                                                                        }
                                                                    }
                                                                }
                                                            }                                                            
                                                        }
                                                    }
        }}})

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'no ipv6 pim register-source Loopback0',
                'interface Loopback0',
                ' no ip pim dense-mode',
                ' exit',
            ]))

    
    def test_multiple_pim_static_rp_config(self):

        # For failures
        self.maxDiff = None

        # shorten the line
        dev1 = self.dev1

        # VRF configuration
        vrf = Vrf('default')

        # == bsr static rp ===
        # -- bsr static rp intf --
        # Pim object
        pim = Pim()
        dev1.add_feature(pim)

        rp1 = RPAddressGroup(device=self.dev1)
        rp1.static_rp_address = '2.2.2.2'
        rp2 = RPAddressGroup(device=self.dev1)
        rp2.static_rp_address = '3.3.3.3'
        rp2.static_rp_group_list = 'rp_group_list'
        rp3 = RPAddressGroup(device=self.dev1)
        rp3.static_rp_address = '4.4.4.4'
        rp3.static_rp_group_list = 'rp_group_list'
        rp3.static_rp_override = True
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].add_static_rp(rp1)
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].add_static_rp(rp2)
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].add_static_rp(rp3)

        # Build config
        cfgs = pim.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'ip pim rp-address 2.2.2.2',
                'ip pim rp-address 3.3.3.3 rp_group_list',
                'ip pim rp-address 4.4.4.4 rp_group_list override',
                ]))

    

if __name__ == '__main__':
    unittest.main()
