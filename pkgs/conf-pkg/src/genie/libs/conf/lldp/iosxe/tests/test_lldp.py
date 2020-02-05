#!/usr/bin/env python

# Python
import unittest
from unittest.mock import Mock

# Genie
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface
from genie.conf.base.attributes import UnsupportedAttributeWarning

# Stp
from genie.libs.conf.lldp import Lldp


class test_lldp(TestCase):

    def setUp(self):
        
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed
        
        # Device
        self.dev1 = Device(name='PE1', testbed=testbed, os='iosxe')

    def test_lldp_full_config(self):

        # For failures
        self.maxDiff = None
        
        # Pim object
        lldp = Lldp()
        self.dev1.add_feature(lldp)

        lldp.device_attr[self.dev1].enabled = True
        lldp.device_attr[self.dev1].hello_timer = 20
        lldp.device_attr[self.dev1].hold_timer = 30
        lldp.device_attr[self.dev1].reinit_timer = 5

        lldp.device_attr[self.dev1].tlv_select_attr.suppress_tlv_port_description = True
        lldp.device_attr[self.dev1].tlv_select_attr.suppress_tlv_system_name = True
        lldp.device_attr[self.dev1].tlv_select_attr.suppress_tlv_system_description = True
        lldp.device_attr[self.dev1].tlv_select_attr.suppress_tlv_system_capabilities = False
        lldp.device_attr[self.dev1].tlv_select_attr.suppress_tlv_system_description = False

        lldp.device_attr[self.dev1].interface_attr['GigabitEthernet2/0/15'].if_enabled = True          

        cfgs = lldp.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.\
            join([
                'lldp run',
                'lldp timer 20',
                'lldp holdtime 30',
                'lldp reinit 5',
                'no lldp tlv-select port-description',
                'no lldp tlv-select system-name',
                'lldp tlv-select system-description',
                'lldp tlv-select system-capabilities',
                'interface GigabitEthernet2/0/15',
                ' lldp transmit',
                ' lldp receive',
                ' exit',
            ]))

        cfgs = lldp.build_unconfig(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.\
            join([
                'no lldp run',
                'no lldp timer 20',
                'no lldp holdtime 30',
                'no lldp reinit 5',
                'lldp tlv-select port-description',
                'lldp tlv-select system-name',
                'no lldp tlv-select system-description',
                'no lldp tlv-select system-capabilities',
                'interface GigabitEthernet2/0/15',
                ' no lldp transmit',
                ' no lldp receive',
                ' exit',
            ]))

        # uncfg with attributes
        cfgs = lldp.build_unconfig(apply=False,
                  attributes={'device_attr': {
                                self.dev1: {
                                    'enabled': None,
                                    'tlv_select_attr': {
                                        'suppress_tlv_port_description': None
                                    },
                                    'interface_attr': {
                                        'GigabitEthernet2/0/15': {
                                            'if_enabled': None
                                        }
                                    },}}})
        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.\
            join([
                'no lldp run',
                'lldp tlv-select port-description',
                'interface GigabitEthernet2/0/15',
                ' no lldp transmit',
                ' no lldp receive',
                ' exit',
            ]))
    

if __name__ == '__main__':
    unittest.main()
