#!/usr/bin/env python

# python
import unittest
from unittest.mock import Mock

# Genie package
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Interface


class test_interface(TestCase):

    def test_ethernet(self):
        testbed = Testbed()
        Genie.testbed = Testbed()
        dev1 = Device(name='PE1', os='ios')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/1')

        # Defining attributes section
        intf1.description = 'test desc'
        intf1.enabled = True

        # Check config
        cfg = intf1.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'interface GigabitEthernet0/0/1',
            ' description test desc',
            ' no shutdown',
            ' exit',
        ]))

        # Check unconfig without attribtues
        uncfg = intf1.build_unconfig(apply=False)
        self.assertMultiLineEqual(str(uncfg), '\n'.join([
            'default interface GigabitEthernet0/0/1',
        ]))


if __name__ == '__main__':
    unittest.main()

