#!/usr/bin/env python

# Python
import unittest
from unittest.mock import Mock
import pdb

# Genie
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface
from genie.conf.base.attributes import UnsupportedAttributeWarning

# Esi
from genie.libs.conf.evpn import Evpn


class test_evpn(TestCase):

    def setUp(self):

        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed

        # Device
        self.dev = Device(name='node01', testbed=testbed, os='nxos')
        self.intf1 = Interface(device=self.dev, name='Ethernet1/1')
        self.intf2 = Interface(device=self.dev, name='port-channel1')
        self.intf3 = Interface(device=self.dev, name='port-channel2')
        self.intf4 = Interface(device=self.dev, name='port-channel3')

        # Esi object
        self.evpn = Evpn()
        self.dev.add_feature(self.evpn)

    def test_evpn_config_modulo(self):

        self.evpn.device_attr[self.dev].multi_homing_enabled = True
        self.evpn.device_attr[self.dev].evpn_mutihoming_df_election = 'modulo'
        self.evpn.device_attr[self.dev].evpn_multihoming_es_delay_restore_time = 45
        self.evpn.device_attr[self.dev].evpn_multihoming_global_system_mac = 'aaaa.deaf.beef'
        intf1 = self.intf1.name
        self.evpn.device_attr[self.dev].interface_attr[intf1].evpn_multihoming_core_tracking = True
        intf2 = self.intf2.name
        self.evpn.device_attr[self.dev].interface_attr[intf2].ethernet_segment_intf = True
        self.evpn.device_attr[self.dev].interface_attr[intf2].system_mac = '000a:000b:000c'            
        self.evpn.device_attr[self.dev].interface_attr[intf2].local_discriminator = '101'
        intf3 = self.intf3.name
        self.evpn.device_attr[self.dev].interface_attr[intf3].ethernet_segment_intf = True         
        self.evpn.device_attr[self.dev].interface_attr[intf3].local_discriminator = '102'       
        intf4 = self.intf4.name
        self.evpn.device_attr[self.dev].interface_attr[intf4].ethernet_segment_intf = True
        self.evpn.device_attr[self.dev].interface_attr[intf4].esi_tag = '0000.0a00.0b00.0c00.0067'

        # Build Esi configuration
        cfgs = self.evpn.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev.name]),
            '\n'.join([
                    'evpn multihoming',
                    ' df-election mode modulo',
                    ' ethernet-segment delay-restore time 45',
                    ' system-mac aaaa.deaf.beef',
                    ' exit',
                    'interface Ethernet1/1',
                    ' evpn multihoming core-tracking',
                    ' exit',
                    'interface port-channel1',
                    ' switchport',
                    ' ethernet-segment',
                    '  esi system-mac 000a:000b:000c 101',
                    '  exit',
                    ' exit',
                    'interface port-channel2',
                    ' switchport',
                    ' ethernet-segment',
                    '  esi system-mac 102',
                    '  exit',
                    ' exit',
                    'interface port-channel3',
                    ' switchport',
                    ' ethernet-segment',
                    '  esi 0000.0a00.0b00.0c00.0067',
                    '  exit',
                    ' exit'
            ]))


if __name__ == '__main__':
    unittest.main()
