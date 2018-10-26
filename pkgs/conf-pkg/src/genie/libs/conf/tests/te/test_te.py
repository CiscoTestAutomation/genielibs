#!/usr/bin/env python

import unittest,re
from unittest.mock import Mock

from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

from genie.libs.conf.te import Te, Srlg

if 0:
    print("\n PE1 CONFIG\n" + str(out['PE1']))
    print("\n PE2 CONFIG\n" + str(out['PE2']))

class test_te(unittest.TestCase):

    def setUp(self):
        self.tb = Genie.testbed = Testbed()
        self.dev1 = Device(testbed=self.tb, name='PE1', os='iosxr')
        self.dev2 = Device(testbed=self.tb, name='PE2', os='iosxr')
        self.i1 = Interface(name='GigabitEthernet0/0/0/1',device=self.dev1)
        self.i2 = Interface(name='GigabitEthernet0/0/0/2',device=self.dev2)
        self.i3 = Interface(name='GigabitEthernet0/0/0/3',device=self.dev1)
        self.i4 = Interface(name='GigabitEthernet0/0/0/4',device=self.dev2)
        self.i5 = Interface(name='GigabitEthernet0/0/0/5',device=self.dev1)
        self.i6 = Interface(name='GigabitEthernet0/0/0/6',device=self.dev2)
        self.i7 = Interface(name='GigabitEthernet0/0/0/7',device=self.dev1)
        self.i8 = Interface(name='GigabitEthernet0/0/0/8',device=self.dev2)
        self.link = Link(name='1_2_1',testbed=self.tb)
        self.link.connect_interface(interface=self.i1)
        self.link.connect_interface(interface=self.i2)
        self.link2 = Link(name='1_2_2',testbed=self.tb)
        self.link2.connect_interface(interface=self.i3)
        self.link2.connect_interface(interface=self.i4)
        self.link3 = Link(name='1_2_3',testbed=self.tb)
        self.link3.connect_interface(interface=self.i5)
        self.link3.connect_interface(interface=self.i6)
        self.link4 = Link(name='1_2_4',testbed=self.tb)
        self.link4.connect_interface(interface=self.i7)
        self.link4.connect_interface(interface=self.i8)
        self.assertSetEqual(
            set(self.link.find_interfaces()),
            set([self.i1, self.i2]))
        self.assertSetEqual(
            set(self.dev1.find_interfaces()),
            set([self.i1, self.i3, self.i5, self.i7]))
        self.assertSetEqual(
            set(self.dev2.find_interfaces()),
            set([self.i2, self.i4, self.i6, self.i8]))
    

    def test_MplsTe(self):

        te = Te()
        self.assertSetEqual(set(te.devices), set([]))
        self.assertSetEqual(set(te.links), set([]))

        if 0:
            print("before")
            print(te.devices)
            print(te.links)
            print(te.interfaces)

        self.link.add_feature(te)
        self.link2.add_feature(te)
        self.link3.add_feature(te)
        self.link4.add_feature(te)
        self.assertCountEqual(te.devices, [self.dev1, self.dev2])
        self.assertSetEqual(set(te.links), set([self.link, self.link2, self.link3, self.link4]))
        self.assertSetEqual(set(te.interfaces), set([self.i1, self.i2, self.i3, self.i4, self.i5, self.i6, self.i7, self.i8]))

        if 0:
            print("after")
            print(te.links)
            print(te.devices)
            print(te.interfaces)

        
        te.log_events_preemption = True
        te.log_events_frr_protection = True
        te.device_attr['PE1'].log_events_frr_protection_type = 'backup-tunnel'
        te.device_attr['PE2'].log_events_frr_protection_type = 'primary-lsp'
        te.device_attr['PE2'].log_events_frr_protection_primary_lsp_type = 'active-state'
        te.srlg_admin_weight = 20000
        te.backup_auto_tun_tunid_min = 210
        te.backup_auto_tun_tunid_max = 600
        te.auto_tun_backup_affinity_ignore = True
        te.affinity_map_val_dict['RED'] = "0x1"
        te.soft_preempt_timeout = 5
        te.reoptimize_delay_cleanup = 10
        te.reoptimize_delay_install = 1
        te.flooding_threshold_up = 1
        te.flooding_threshold_down = 1

        te.p2mp_auto_tun_tunid_min = 100
        te.p2mp_auto_tun_tunid_max = 200
        te.device_attr['PE1'].p2mp_auto_tun_tunid_min = 200
        te.device_attr['PE1'].p2mp_auto_tun_tunid_max = 300
        te.auto_tun_backup_affinity_ignore = True
        te.auto_tun_backup_timers_rem_unused = 100
        te.auto_tun_backup_attr_set = "backup"

        
        te.device_attr['PE1'].interface_attr[self.i1].auto_tun_backup_exclude_srlg = True
        te.device_attr['PE1'].interface_attr[self.i3].auto_tun_backup_exclude_srlg = True
        te.device_attr['PE1'].interface_attr[self.i3].auto_tun_backup_exclude_srlg_type = 'preferred'
        te.device_attr['PE1'].interface_attr[self.i5].auto_tun_backup_exclude_srlg = True
        te.device_attr['PE1'].interface_attr[self.i5].auto_tun_backup_exclude_srlg_type = 'weighted'
        te.device_attr['PE1'].affinity_map_val_dict = {}
        te.device_attr['PE1'].affinity_map_val_dict['RED'] = "0x2"

        te.device_attr['PE2'].affinity_map_bitpos_dict = {}
        te.device_attr['PE2'].affinity_map_bitpos_dict['BLUE'] = 94
        te.device_attr['PE2'].affinity_map_bitpos_dict['EDGE'] = 27
        te.device_attr['PE2'].affinity_map_bitpos_dict['PINK'] = 95
        te.device_attr['PE2'].affinity_map_bitpos_dict['GREEN'] = 91
        te.device_attr['PE2'].affinity_map_bitpos_dict['METRO'] = 29
        
        out = te.build_config(apply=False)
        self.maxDiff = None
        self.assertCountEqual(out.keys(), ['PE1', 'PE2'])
        self.assertMultiLineEqual(str(out['PE1']), '\n'.join([
            'mpls traffic-eng',
            ' auto-tunnel backup affinity ignore',
            ' auto-tunnel backup timers removal unused 100',
            ' auto-tunnel backup tunnel-id min 210 max 600',
            ' auto-tunnel p2mp tunnel-id min 200 max 300',
            ' logging events preemption',
            ' logging events frr-protection backup-tunnel',
            ' reoptimize timers delay cleanup 10',
            ' reoptimize timers delay installation 1',
            ' flooding threshold up 1 down 1',
            ' affinity-map RED 0x2',
            ' srlg admin-weight 20000',
            ' soft-preemption timeout 5',
            ' interface GigabitEthernet0/0/0/1',
            '  auto-tunnel backup attribute-set backup',
            '  auto-tunnel backup exclude srlg',
            '  exit',
            ' interface GigabitEthernet0/0/0/3',
            '  auto-tunnel backup attribute-set backup',
            '  auto-tunnel backup exclude srlg preferred',
            '  exit',
            ' interface GigabitEthernet0/0/0/5',
            '  auto-tunnel backup attribute-set backup',
            '  auto-tunnel backup exclude srlg weighted',
            '  exit',
            ' interface GigabitEthernet0/0/0/7',
            '  auto-tunnel backup attribute-set backup',
            '  exit',
            ' exit',
        ]))
        
        if 1:
            self.assertMultiLineEqual(str(out['PE2']), '\n'.join([
                'mpls traffic-eng',
                ' auto-tunnel backup affinity ignore',
                ' auto-tunnel backup timers removal unused 100',
                ' auto-tunnel backup tunnel-id min 210 max 600',
                ' auto-tunnel p2mp tunnel-id min 100 max 200',
                ' logging events preemption',
                ' logging events frr-protection primary-lsp active-state',
                ' reoptimize timers delay cleanup 10',
                ' reoptimize timers delay installation 1',
                ' flooding threshold up 1 down 1',
                ' affinity-map BLUE bit-position 94',
                ' affinity-map EDGE bit-position 27',
                ' affinity-map GREEN bit-position 91',
                ' affinity-map METRO bit-position 29',
                ' affinity-map PINK bit-position 95',
                ' affinity-map RED 0x1',
                ' srlg admin-weight 20000',
                ' soft-preemption timeout 5',
                ' interface GigabitEthernet0/0/0/2',
                '  auto-tunnel backup attribute-set backup',
                '  exit',
                ' interface GigabitEthernet0/0/0/4',
                '  auto-tunnel backup attribute-set backup',
                '  exit',
                ' interface GigabitEthernet0/0/0/6',
                '  auto-tunnel backup attribute-set backup',
                '  exit',
                ' interface GigabitEthernet0/0/0/8',
                '  auto-tunnel backup attribute-set backup',
                '  exit',
                ' exit',
                ]))

    def test_UnnumInterfaces(self):
        # Test unnum interface output
        te = Te()
        self.link.add_feature(te)

        te.ipv4_unnum_interfaces = {self.i1, self.i2, self.i3, self.i4}

        out = te.build_config(apply=False)
        self.assertRegex(str(out['PE1']), 'ipv4 unnumbered mpls traffic-eng GigabitEthernet0/0/0/1')
        self.assertRegex(str(out['PE1']), 'ipv4 unnumbered mpls traffic-eng GigabitEthernet0/0/0/3')
        
        self.assertRegex(str(out['PE2']), 'ipv4 unnumbered mpls traffic-eng GigabitEthernet0/0/0/2')
        self.assertRegex(str(out['PE2']), 'ipv4 unnumbered mpls traffic-eng GigabitEthernet0/0/0/4')
             
           
    def test_Srlg(self):
        srlg = Srlg()
        self.dev1.add_feature(srlg)
        self.dev2.add_feature(srlg)
        srlg.name_value_dict['R13'] = 10
        srlg.name_value_dict['R11'] = 20
        srlg.name_value_dict['R23'] = 30
        srlg.name_value_dict['R25'] = 40
        srlg.name_value_dict['R34'] = 50
        
        # if per-device dict is not initialized, base class dict will be over-written
        srlg.device_attr['PE1'].name_value_dict = {}
        srlg.device_attr['PE1'].name_value_dict['R13'] = 10
        srlg.device_attr['PE1'].name_value_dict['R11'] = 20
        srlg.device_attr['PE1'].name_value_dict['R23'] = 30
        srlg.device_attr['PE1'].name_value_dict['R25'] = 40
        srlg.device_attr['PE1'].name_value_dict['R34'] = 50
        srlg.device_attr['PE1'].name_value_dict['R35'] = 60
        srlg.device_attr['PE1'].name_value_dict['R45'] = 70
        
        srlg.device_attr['PE1'].interface_attr[self.i1].intf_name = 'R13'
        srlg.device_attr['PE1'].interface_attr[self.i3].intf_name = 'R11'
        srlg.device_attr['PE1'].interface_attr[self.i5].intf_name = 'R23'
        
        out = srlg.build_config(apply=False)
        self.assertCountEqual(out.keys(), ['PE1', 'PE2'])
        self.assertMultiLineEqual(str(out['PE1']), '\n'.join([
            'srlg',
            ' name R11 value 20',
            ' name R13 value 10',
            ' name R23 value 30',
            ' name R25 value 40',
            ' name R34 value 50',
            ' name R35 value 60',
            ' name R45 value 70',
            ' interface GigabitEthernet0/0/0/1',
            '  name R13',
            '  exit',
            ' interface GigabitEthernet0/0/0/3',
            '  name R11',
            '  exit',
            ' interface GigabitEthernet0/0/0/5',
            '  name R23',
            '  exit',
            ' exit',
        ]))
        self.assertMultiLineEqual(str(out['PE2']), '\n'.join([
            'srlg',
            ' name R11 value 20',
            ' name R13 value 10',
            ' name R23 value 30',
            ' name R25 value 40',
            ' name R34 value 50',
            ' exit',
        ]))
        


if __name__ == '__main__':
    unittest.main() 
        
