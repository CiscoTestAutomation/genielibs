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


outputs = {}

def mapper(key, **kwargs):
    return outputs[key]


class test_pim(TestCase):

    def setUp(self):
        
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed
        
        # Device
        self.dev1 = Device(name='PE1', testbed=testbed, os='nxos')

    def test_pim_full_config(self):

        # For failures
        self.maxDiff = None

        # shorten the line
        dev1 = self.dev1
        
        # Pim object
        pim = Pim()
        dev1.add_feature(pim)

        # Apply configuration
        pim.device_attr[dev1].enabled = True

        # VRF configuration
        vrf1 = Vrf('default')
        pim.device_attr[self.dev1].vrf_attr[vrf1]
        vrf2 = Vrf('red')
        pim.device_attr[self.dev1].vrf_attr[vrf2]

        for vrf, intf in {vrf1: 'Ethernet1/1', vrf2: 'Ethernet2/1'}.items():
            # == auto-rp ===
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                auto_rp = True
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                send_rp_announce_rp_group = '1.1.1.1'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                send_rp_announce_route_map = 'test'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                send_rp_announce_scope = 20
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                send_rp_announce_interval = 60
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                send_rp_announce_bidir = True

            # == auto-rp discovery===
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                auto_rp_discovery = True
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                send_rp_discovery_intf = intf
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                send_rp_discovery_scope = 20
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                autorp_listener = True

            # == bsr candidate ===
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                bsr_candidate_interface = intf
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                bsr_candidate_hash_mask_length = 20
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                bsr_candidate_priority = 20

            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                bsr_candidate_interface = intf
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                bsr_candidate_hash_mask_length = 20
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                bsr_candidate_priority = 20

            # == bsr rp-candidate ===
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                bsr_rp_candidate_interface = intf
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                bsr_rp_candidate_group_list = '239.0.0.0/24'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                bsr_rp_candidate_route_map = 'test'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                bsr_rp_candidate_prefix_list = 'LLAL'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                bsr_rp_candidate_priority = 10
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                bsr_rp_candidate_interval = 60
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                bsr_rp_candidate_bidir = True
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                bsr_rp_candidate_priority = 10

            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                bsr_rp_candidate_interface = intf
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                bsr_rp_candidate_group_list = 'ff1e:abcd:def1::0/64'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                bsr_rp_candidate_route_map = 'test'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                bsr_rp_candidate_prefix_list = 'LLAL'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                bsr_rp_candidate_priority = 10
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                bsr_rp_candidate_interval = 60

            # == static RP ===
            rp1 = RPAddressGroup(device=self.dev1)
            rp1.static_rp_address = '1.1.1.1'
            rp1.static_rp_group_list = '239.0.0.0/24'
            rp1.static_rp_route_map = 'test'
            rp1.static_rp_prefix_list = 'LLAL'
            rp1.static_rp_bidir = True
            rp1.static_rp_override = True
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].add_static_rp(rp1)


            rp2 = RPAddressGroup(device=self.dev1)
            rp2.static_rp_address = '2001:db8:1:1::1'
            rp2.static_rp_group_list = 'ff1e:abcd:def1::0/64'
            rp2.static_rp_route_map = 'test'
            rp2.static_rp_prefix_list = 'LLAL'
            rp2.static_rp_override = True
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].add_static_rp(rp2)

            # == static rp register ===
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                accept_register = 'regist_name'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                accept_register_prefix_list = 'test'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                accept_register = 'regist_name'
            # not ipv6 supported
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                accept_register_prefix_list = 'test'

            # log-neighbor-changes
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                log_neighbor_changes = True
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                log_neighbor_changes = True

            # register_source
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                register_source = intf
            # not ipv6 supported
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                register_source = intf

            # == sg-expiry-timer ==
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                sg_expiry_timer = 182
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                sg_expiry_timer_infinity = True
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                sg_expiry_timer_sg_list = 'sg_name'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                sg_expiry_timer_prefix_list = 'prefix_name'

            # == spt-threshold ==
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                spt_switch_infinity = 'infinity'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                spt_switch_policy = 'abcde'

            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                spt_switch_infinity = 'infinity'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                spt_switch_policy = 'abcde'


            # == interface ==
            # ----   mode  ----------
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                interface_attr[intf].mode = 'sparse-mode'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                interface_attr[intf].boundary = 'abc'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                interface_attr[intf].boundary_in = True
            
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                interface_attr[intf].mode = 'sparse-mode'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                interface_attr[intf].boundary = 'abc'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                interface_attr[intf].boundary_in = True

            # ----   jp-policy  ----------
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                interface_attr[intf].boundary = 'test'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                interface_attr[intf].boundary_in = True
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                interface_attr[intf].boundary_out = True
            
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                interface_attr[intf].boundary = 'test'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                interface_attr[intf].boundary_in = True
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                interface_attr[intf].boundary_out = True

            # ----   border  ----------
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                interface_attr[intf].bsr_border = True
            
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                interface_attr[intf].bsr_border = True

            # ----   hello-interval  ----------
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                interface_attr[intf].hello_interval = 30000
            
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                interface_attr[intf].hello_interval = 30000

            # ----   dr-priority  ----------
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                interface_attr[intf].dr_priority = 777
            
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                interface_attr[intf].dr_priority = 777

            # ----   neighbor-policy  ----------
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                interface_attr[intf].neighbor_filter = 'pim_neighbor_policy'
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
                interface_attr[intf].neighbor_filter_prefix_list = 'test'
            
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                interface_attr[intf].neighbor_filter = 'pim_neighbor_policy'
            # not supported
            pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
                interface_attr[intf].neighbor_filter_prefix_list = 'test'
        
        # Build config
        cfgs = pim.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'feature pim',
                'feature pim6',
                'ip pim auto-rp rp-candidate 1.1.1.1 route-map test interval 60 scope 20 bidir',
                'ip pim auto-rp mapping-agent Ethernet1/1 scope 20',
                'ip pim auto-rp forward listen',
                'ip pim bsr forward listen',
                'ip pim bsr-candidate Ethernet1/1 hash-len 20 priority 20',
                'ip pim bsr forward listen',
                'ip pim rp-candidate Ethernet1/1 group-list 239.0.0.0/24 priority 10 interval 60 bidir',
                'ip pim register-policy regist_name',
                'ip pim register-policy prefix-list test',
                'ip pim log-neighbor-changes',
                'ip pim register-source Ethernet1/1',
                'ip pim sg-expiry-timer 182 prefix-list prefix_name',
                'ip pim sg-expiry-timer 182 sg-list sg_name',
                'ip pim sg-expiry-timer infinity prefix-list prefix_name',
                'ip pim sg-expiry-timer infinity sg-list sg_name',
                'ip pim spt-threshold infinity group-list abcde',
                'ip pim rp-address 1.1.1.1 group-list 239.0.0.0/24 bidir',
                'interface Ethernet1/1',
                ' ip pim sparse-mode',
                ' ip pim jp-policy test in',
                ' ip pim jp-policy test out',
                ' ip pim border',
                ' ip pim hello-interval 30000',
                ' ip pim dr-priority 777',
                ' ip pim neighbor-policy pim_neighbor_policy',
                ' ip pim neighbor-policy prefix-list test',
                ' exit',
                'ipv6 pim bsr forward listen',
                'ipv6 pim bsr-candidate Ethernet1/1 hash-len 20 priority 20',
                'ipv6 pim bsr forward listen',
                'ipv6 pim rp-candidate Ethernet1/1 group-list ff1e:abcd:def1::0/64 priority 10 interval 60',
                'ipv6 pim register-policy regist_name',
                'ipv6 pim log-neighbor-changes',
                'ipv6 pim spt-threshold infinity group-list abcde',
                'ipv6 pim rp-address 2001:db8:1:1::1 group-list ff1e:abcd:def1::0/64 override',
                'interface Ethernet1/1',
                ' ipv6 pim sparse-mode',
                ' ipv6 pim jp-policy test in',
                ' ipv6 pim jp-policy test out',
                ' ipv6 pim border',
                ' ipv6 pim hello-interval 30000',
                ' ipv6 pim dr-priority 777',
                ' ipv6 pim neighbor-policy pim_neighbor_policy',
                ' exit',
                'vrf context red',
                ' ip pim auto-rp rp-candidate 1.1.1.1 route-map test interval 60 scope 20 bidir',
                ' ip pim auto-rp mapping-agent Ethernet2/1 scope 20',
                ' ip pim auto-rp forward listen',
                ' ip pim bsr forward listen',
                ' ip pim bsr-candidate Ethernet2/1 hash-len 20 priority 20',
                ' ip pim bsr forward listen',
                ' ip pim rp-candidate Ethernet2/1 group-list 239.0.0.0/24 priority 10 interval 60 bidir',
                ' ip pim register-policy regist_name',
                ' ip pim register-policy prefix-list test',
                ' ip pim log-neighbor-changes',
                ' ip pim register-source Ethernet2/1',
                ' ip pim sg-expiry-timer 182 prefix-list prefix_name',
                ' ip pim sg-expiry-timer 182 sg-list sg_name',
                ' ip pim sg-expiry-timer infinity prefix-list prefix_name',
                ' ip pim sg-expiry-timer infinity sg-list sg_name',
                ' ip pim spt-threshold infinity group-list abcde',
                ' ip pim rp-address 1.1.1.1 group-list 239.0.0.0/24 bidir',
                ' exit',
                'interface Ethernet2/1',
                ' ip pim sparse-mode',
                ' ip pim jp-policy test in',
                ' ip pim jp-policy test out',
                ' ip pim border',
                ' ip pim hello-interval 30000',
                ' ip pim dr-priority 777',
                ' ip pim neighbor-policy pim_neighbor_policy',
                ' ip pim neighbor-policy prefix-list test',
                ' exit',
                'vrf context red',
                ' ipv6 pim bsr forward listen',
                ' ipv6 pim bsr-candidate Ethernet2/1 hash-len 20 priority 20',
                ' ipv6 pim bsr forward listen',
                ' ipv6 pim rp-candidate Ethernet2/1 group-list ff1e:abcd:def1::0/64 priority 10 interval 60',
                ' ipv6 pim register-policy regist_name',
                ' ipv6 pim log-neighbor-changes',
                ' ipv6 pim spt-threshold infinity group-list abcde',
                ' ipv6 pim rp-address 2001:db8:1:1::1 group-list ff1e:abcd:def1::0/64 override',
                ' exit',
                'interface Ethernet2/1',
                ' ipv6 pim sparse-mode',
                ' ipv6 pim jp-policy test in',
                ' ipv6 pim jp-policy test out',
                ' ipv6 pim border',
                ' ipv6 pim hello-interval 30000',
                ' ipv6 pim dr-priority 777',
                ' ipv6 pim neighbor-policy pim_neighbor_policy',
                ' exit',
            ]))

        cfgs = pim.build_unconfig(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'no feature pim',
                'no feature pim6',
            ]))

        
        cfgs = pim.build_unconfig(apply=False,
                                  attributes={'device_attr': {
                                                self.dev1: {
                                                    'vrf_attr': {
                                                        'default': {
                                                            'address_family_attr': {
                                                                'ipv4': {
                                                                    'register_source': None
                                                                }
                                                            }
                                                        },
                                                        'red': {
                                                            'address_family_attr': {
                                                                'ipv6': {
                                                                    'interface_attr': {
                                                                        'Ethernet2/1': {
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
                'no ip pim register-source Ethernet1/1',
                'interface Ethernet2/1',
                ' no ipv6 pim sparse-mode',
                ' exit',
            ]))

    def test_pim_auto_rp_config(self):

        # For failures
        self.maxDiff = None

        # shorten the line
        dev1 = self.dev1

        # VRF configuration
        vrf = Vrf('default')


        # == auto-rp lack of information ===
        # Pim object
        pim = Pim()
        dev1.add_feature(pim)

        pim.device_attr[dev1].enabled_pim = True
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            send_rp = True
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            send_rp_announce_rp_group = '1.1.1.1'

        # Build config
        cfgs = pim.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'feature pim',
                ]))

        # == auto-rp intf group-list ===
        # Pim object
        pim = Pim()
        dev1.add_feature(pim)

        # Apply configuration
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            send_rp = True
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            send_rp_announce_intf = 'Ethernet1/1'
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            send_rp_announce_group_list = '239.0.0.0/24'

        # Build config
        cfgs = pim.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'ip pim send-rp-announce Ethernet1/1 group-list 239.0.0.0/24',
                ]))

        # == auto-rp group route-map with interval ===
        # Pim object
        pim = Pim()
        dev1.add_feature(pim)

        # VRF configuration
        vrf = Vrf('red')

        # Apply configuration
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            send_rp = True
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            send_rp_announce_rp_group = '1.1.1.1'
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            send_rp_announce_route_map = 'test'
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            send_rp_announce_interval = 30

        # Build config
        cfgs = pim.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'vrf context red',
                ' ip pim send-rp-announce 1.1.1.1 route-map test interval 30',
                ' exit',
                ]))

        # == auto-rp intf prefix-list with interval bidir===
        # Pim object
        pim = Pim()
        dev1.add_feature(pim)

        # VRF configuration
        vrf = Vrf('red')

        # Apply configuration
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            auto_rp = True
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            send_rp_announce_intf = 'Ethernet1/1'
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            send_rp_announce_prefix_list = 'test'
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            send_rp_announce_scope = 10
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            send_rp_announce_bidir = True

        # Build config
        cfgs = pim.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'vrf context red',
                ' ip pim auto-rp rp-candidate Ethernet1/1 prefix-list test scope 10 bidir',
                ' exit',
                ]))


        # == auto-rp discovery===
        # Pim object
        pim = Pim()
        dev1.add_feature(pim)

        # VRF configuration
        vrf = Vrf('default')

        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            send_rp_discovery = True
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            send_rp_discovery_intf = 'Ethernet1/1'

        # Build config
        cfgs = pim.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'ip pim send-rp-discovery Ethernet1/1',
                ]))

    def test_pim_bsr_config(self):

        # For failures
        self.maxDiff = None

        # shorten the line
        dev1 = self.dev1

        # VRF configuration
        vrf = Vrf('default')

        # == bsr rp ===
        # Pim object
        pim = Pim()
        dev1.add_feature(pim)

        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            bsr_candidate_interface = 'Ethernet1/1'

        # Build config
        cfgs = pim.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'ip pim bsr forward listen',
                'ip pim bsr-candidate Ethernet1/1',
                ]))

        # Pim object
        pim = Pim()
        dev1.add_feature(pim)

        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            bsr_candidate_interface = 'Ethernet1/1'
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            bsr_candidate_hash_mask_length = 30

        # Build config
        cfgs = pim.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'ip pim bsr forward listen',
                'ip pim bsr-candidate Ethernet1/1 hash-len 30',
                ]))

        # Pim object
        pim = Pim()
        dev1.add_feature(pim)

        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
            bsr_candidate_interface = 'Ethernet1/1'
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
            bsr_candidate_priority = 200

        # Build config
        cfgs = pim.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'ipv6 pim bsr forward listen',
                'ipv6 pim bsr-candidate Ethernet1/1 priority 200',
                ]))

        # == bsr rp intf route-map ===
        # Pim object
        pim = Pim()
        dev1.add_feature(pim)

        # VRF configuration
        vrf = Vrf('red')

        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
            bsr_rp_candidate_interface = 'Ethernet1/1'
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].\
            bsr_rp_candidate_route_map = 'test'

        # Build config
        cfgs = pim.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'vrf context red',
                ' ipv6 pim bsr forward listen',
                ' ipv6 pim rp-candidate Ethernet1/1 route-map test',
                ' exit',
                ]))

        # == auto-rp intf prefix-list with interval bidir===
        # Pim object
        pim = Pim()
        dev1.add_feature(pim)

        # VRF configuration
        vrf = Vrf('red')

        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            bsr_rp_candidate_interface = 'Ethernet1/1'
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            bsr_rp_candidate_prefix_list = 'LALALLA'
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            bsr_rp_candidate_interval = 60
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            bsr_rp_candidate_bidir = True

        # Build config
        cfgs = pim.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'vrf context red',
                ' ip pim bsr forward listen',
                ' ip pim rp-candidate Ethernet1/1 prefix-list LALALLA interval 60 bidir',
                ' exit',
                ]))

    def test_pim_static_rp_config(self):

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
        rp1.static_rp_group_list = '224.0.0.0/4'
        rp2 = RPAddressGroup(device=self.dev1)
        rp2.static_rp_address = '3.3.3.3'
        rp2.static_rp_group_list = '224.0.0.0/4'
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].add_static_rp(rp1)
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].add_static_rp(rp2)

        # Build config
        cfgs = pim.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'ip pim rp-address 2.2.2.2 group-list 224.0.0.0/4',
                'ip pim rp-address 3.3.3.3 group-list 224.0.0.0/4',
                ]))

        # == bsr static rp intf route-map ===
        # Pim object
        pim = Pim()
        dev1.add_feature(pim)

        rp1 = RPAddressGroup(device=self.dev1)
        rp1.static_rp_address = '1.1.1.1'
        rp1.static_rp_route_map = 'test'
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].add_static_rp(rp1)

        # Build config
        cfgs = pim.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'ip pim rp-address 1.1.1.1 route-map test',
                ]))

        # == bsr static rp intf group-list ipv6 ===
        # Pim object
        pim = Pim()
        dev1.add_feature(pim)

        rp1 = RPAddressGroup(device=self.dev1)
        rp1.static_rp_address = '1:1::1:1'
        rp1.static_rp_group_list = 'ff00::/8'
        rp1.static_rp_override = True
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv6'].add_static_rp(rp1)

        # Build config
        cfgs = pim.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'ipv6 pim rp-address 1:1::1:1 group-list ff00::/8 override',
                ]))

    def test_pim_sg_expiry_timer_config(self):

        # For failures
        self.maxDiff = None

        # shorten the line
        dev1 = self.dev1

        # VRF configuration
        vrf = Vrf('default')

        # == sg_expiry_timer ===
        # Pim object
        pim = Pim()
        dev1.add_feature(pim)

        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            sg_expiry_timer = 181

        # Build config
        cfgs = pim.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'ip pim sg-expiry-timer 181',
                ]))

        # == sg_expiry_timer_infinity ===
        # Pim object
        pim = Pim()
        dev1.add_feature(pim)
        # VRF configuration
        vrf = Vrf('blue')

        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            sg_expiry_timer_infinity = True

        # Build config
        cfgs = pim.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'vrf context blue',
                ' ip pim sg-expiry-timer infinity',
                ' exit',
                ]))

        # == sg_expiry_timer  sg_expiry_timer_sg_list ===
        # Pim object
        pim = Pim()
        dev1.add_feature(pim)
        # VRF configuration
        vrf = Vrf('VRF1')

        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            sg_expiry_timer = 200
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            sg_expiry_timer_sg_list = 'test'

        # Build config
        cfgs = pim.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'vrf context VRF1',
                ' ip pim sg-expiry-timer 200 sg-list test',
                ' exit',
                ]))

        # == sg_expiry_timer_infinity sg_expiry_timer_prefix_list ===
        # Pim object
        pim = Pim()
        dev1.add_feature(pim)
        # VRF configuration
        vrf = Vrf('default')

        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            sg_expiry_timer_infinity = True
        pim.device_attr[dev1].vrf_attr[vrf].address_family_attr['ipv4'].\
            sg_expiry_timer_prefix_list = 'test'

        # Build config
        cfgs = pim.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.\
            join([
                'ip pim sg-expiry-timer infinity prefix-list test',
                ]))


    def test_learn_config(self):

        testbed = Testbed()
        dev = Device(testbed=testbed, name='PE2', os='nxos')
        dev.custom = {'abstraction':{'order':['os'], 'context':'cli'}}
        dev.mapping={}
        dev.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        dev.connectionmgr.connections['cli'] = dev

        golden_output = {'return_value': '''
            N95_2_R2# show run pim
            !Command: show running-config pim
!Time: Wed Aug 15 14:45:52 2018

version 7.0(3)I7(3)
feature pim

ip pim bsr bsr-candidate loopback0 priority 128
ip pim rp-address 6.6.6.6 group-list 234.0.0.0/8
ip pim rp-address 6.6.6.6 group-list 239.1.1.0/24 bidir
ip pim rp-address 26.26.26.26 group-list 237.0.0.0/8
ip pim rp-address 126.126.126.126 group-list 238.0.0.0/8
ip pim bsr rp-candidate loopback0 group-list 235.0.0.0/8 priority 128
ip pim send-rp-announce loopback0 group-list 236.0.0.0/8
ip pim send-rp-discovery loopback0
ip pim ssm range 232.0.0.0/8
ip pim anycast-rp 126.126.126.126 2.2.2.2
ip pim anycast-rp 126.126.126.126 6.6.6.6
ip pim bsr forward listen
ip pim register-source loopback0

vrf context VRF1
  ip pim bsr bsr-candidate loopback11 priority 128
  ip pim rp-address 6.6.6.6 group-list 234.0.0.0/8
  ip pim rp-address 6.6.6.6 group-list 239.1.1.0/24 bidir
  ip pim rp-address 26.26.26.26 group-list 237.0.0.0/8
  ip pim rp-address 126.126.126.126 group-list 238.0.0.0/8
  ip pim bsr rp-candidate loopback11 group-list 235.0.0.0/8 priority 128
  ip pim send-rp-announce loopback11 group-list 236.0.0.0/8
  ip pim send-rp-discovery loopback11
  ip pim ssm range 232.0.0.0/8
  ip pim anycast-rp 126.126.126.126 2.2.2.2
  ip pim anycast-rp 126.126.126.126 6.6.6.6
  ip pim bsr forward listen
  ip pim register-source loopback11

interface loopback0
  ip pim sparse-mode
        '''}

        golden_output_vrf = '''
            N95_2_R2# show run pim | inc vrf
vrf context VRF1
        '''
        golden_output_vrf6 = '''
            N95_2_R2# show run pim6 | inc vrf
vrf context VRF1
        '''
        golden_output_feature = '''
            N95_2_R2# show run pim | inc feature
feature pim
        '''
        golden_output_feature6 = '''
            N95_2_R2# show run pim6 | inc feature
feature pim6
        '''
        golden_output_auto_rp = '''
            N95_2_R2# show run pim | sec '^i' | inc send-rp-announce
ip pim send-rp-announce loopback0 group-list 236.0.0.0/8
        '''
        golden_output_auto_rp_vrf = '''
            N95_2_R2# show run pim | sec VRF1 | inc send-rp-announce
  ip pim send-rp-announce loopback11 group-list 236.0.0.0/8
        '''

        pim = Pim()
        outputs['show running-config pim | inc feature'] = golden_output_feature
        outputs['show running-config pim6 | inc feature'] = golden_output_feature6
        outputs['show running-config pim | inc vrf'] = golden_output_vrf
        outputs['show running-config pim6 | inc vrf'] = golden_output_vrf6
        outputs["show running-config pim | sec '^i' | inc send-rp-announce"] = golden_output_auto_rp
        outputs["show running-config pim | sec VRF1 | inc send-rp-announce"] = golden_output_auto_rp_vrf
        # Return outputs above as inputs to parser when called
        dev.execute = Mock()
        dev.execute.side_effect = mapper

        learn = Pim.learn_config(device=dev, attributes=['pim[vrf_attr][default][address_family_attr][ipv4][send_rp_announce_intf]'])

        self.assertEqual(learn[0].device_attr[dev].vrf_attr['default'].address_family_attr['ipv4'].send_rp_announce_intf, 'loopback0')
        self.assertEqual(learn[0].device_attr[dev].vrf_attr['default'].address_family_attr['ipv4'].send_rp_announce_group_list, None)

        learn = Pim.learn_config(device=dev)

        self.assertEqual(learn[0].device_attr[dev].vrf_attr['default'].address_family_attr['ipv4'].send_rp_announce_intf, 'loopback0')
        self.assertEqual(learn[0].device_attr[dev].vrf_attr['default'].address_family_attr['ipv4'].send_rp_announce_group_list, '236.0.0.0/8')
        self.assertEqual(learn[0].device_attr[dev].vrf_attr['VRF1'].address_family_attr['ipv4'].send_rp_announce_intf, 'loopback11')
        self.assertEqual(learn[0].device_attr[dev].vrf_attr['VRF1'].address_family_attr['ipv4'].send_rp_announce_group_list, '236.0.0.0/8')


if __name__ == '__main__':
    unittest.main()
