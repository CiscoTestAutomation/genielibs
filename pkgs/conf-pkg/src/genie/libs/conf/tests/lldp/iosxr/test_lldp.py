#!/usr/bin/env python

# Python
import unittest
from unittest.mock import Mock

# Genie
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device

# Stp
from genie.libs.conf.lldp import Lldp


class test_lldp(TestCase):

    def setUp(self):
        
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed
        
        # Device
        self.dev1 = Device(name='PE1', testbed=testbed, os='iosxr')

    def test_lldp_full_config(self):

        # For failures
        self.maxDiff = None
        
        # Pim object
        lldp = Lldp()
        self.dev1.add_feature(lldp)

        lldp.device_attr[self.dev1].enabled = True

        cfgs = lldp.build_config(apply=False)
        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.\
            join([
                'lldp',
            ]))

        cfgs = lldp.build_unconfig(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.\
            join([
                'no lldp',
            ]))
    

if __name__ == '__main__':
    unittest.main()