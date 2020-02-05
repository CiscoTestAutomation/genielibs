#!/usr/bin/env python

# Python
import unittest
from unittest.mock import Mock

# Genie
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device

# Fdb
from genie.libs.conf.fdb import Fdb


class test_fdb(TestCase):

    def setUp(self):
        
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed
        
        # Device
        self.dev1 = Device(name='PE1', testbed=testbed, os='iosxe')

    def test_fdb_config(self):

        # For failures
        self.maxDiff = None
        
        # Fdb object
        fdb = Fdb()
        self.dev1.add_feature(fdb)

        # bridge_assurance command rejected by router
        fdb.device_attr[self.dev1].mac_aging_time = 0
        fdb.device_attr[self.dev1].vlan_attr['10'].vlan_mac_learning = True
        fdb.device_attr[self.dev1].vlan_attr['105'].vlan_mac_learning = True
        fdb.device_attr[self.dev1].vlan_attr['10'].vlan_mac_aging_time = 10
        fdb.device_attr[self.dev1].vlan_attr['10'].mac_address_attr['aaaa.bbbb.cccc'].\
            interface = ['GigabitEthernet1/0/8', 'GigabitEthernet1/0/9']
        fdb.device_attr[self.dev1].vlan_attr['20'].mac_address_attr['aaaa.bbbb.cccc'].\
            drop = True
        fdb.device_attr[self.dev1].vlan_attr['30'].mac_address_attr['aaaa.bbbb.cccc'].\
            drop = True

        cfgs = fdb.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.\
            join([
                'mac address-table aging-time 0',
                'mac address-table learning vlan 10',
                'mac address-table aging-time 10 vlan 10',
                'mac address-table static aaaa.bbbb.cccc vlan 10 interface GigabitEthernet1/0/8 GigabitEthernet1/0/9',
                'mac address-table learning vlan 105',
                'mac address-table static aaaa.bbbb.cccc vlan 20 drop',
                'mac address-table static aaaa.bbbb.cccc vlan 30 drop',
            ]))

        cfgs = fdb.build_unconfig(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.\
            join([
                'no mac address-table aging-time 0',
                'no mac address-table learning vlan 10',
                'no mac address-table aging-time 10 vlan 10',
                'no mac address-table static aaaa.bbbb.cccc vlan 10 interface GigabitEthernet1/0/8 GigabitEthernet1/0/9',
                'no mac address-table learning vlan 105',
                'no mac address-table static aaaa.bbbb.cccc vlan 20 drop',
                'no mac address-table static aaaa.bbbb.cccc vlan 30 drop',
            ]))

        # uncfg with attributes
        cfgs = fdb.build_unconfig(apply=False,
                                  attributes={
                                    'device_attr': {
                                        self.dev1: {
                                            'mac_aging_time': None,
                                            'vlan_attr': {
                                                '10': {
                                                    'vlan_mac_learning': None,
                                                    'mac_address_attr': {
                                                        'aaaa.bbbb.cccc': {
                                                            'interface': None
                                                        }
                                                    }
                                                }
                                            }
        }}})
        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.\
            join([
                'no mac address-table aging-time 0',
                'no mac address-table learning vlan 10',
                'no mac address-table aging-time 10 vlan 10',
                'no mac address-table static aaaa.bbbb.cccc vlan 10 interface GigabitEthernet1/0/8 GigabitEthernet1/0/9',
            ]))

if __name__ == '__main__':
    unittest.main()
