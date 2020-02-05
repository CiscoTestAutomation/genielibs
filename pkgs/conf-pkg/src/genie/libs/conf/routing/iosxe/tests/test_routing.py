#!/usr/bin/env python

# Python
import unittest
from unittest.mock import Mock

# Genie package
from genie.conf import Genie
from genie.tests.conf import TestCase
from genie.conf.base import Testbed, Device

# Genie Conf
from genie.libs.conf.routing import Routing


class test_routing(TestCase):

    def test_full(self):

        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')

        # Create Routing object
        routing = Routing()
        dev1.add_feature(routing)
        routing.device_attr[dev1].enabled = True

        # Build config
        cfgs = routing.build_config(apply=False)

        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'ip routing',
                'ipv6 unicast routing',
            ]))

        # Unconfigure
        uncfgs = routing.build_unconfig(apply=False)

        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(uncfgs[dev1.name]),
            '\n'.join([
                'no ip routing',
                'no ipv6 unicast routing',
            ]))

    def test_ipv4(self):

        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')

        # Create Routing object
        routing = Routing()
        dev1.add_feature(routing)
        routing.device_attr[dev1].enabled_ip_routing = True

        # Build config
        cfgs = routing.build_config(apply=False)

        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'ip routing',
            ]))

        # Unconfigure
        uncfgs = routing.build_unconfig(apply=False)

        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(uncfgs[dev1.name]),
            '\n'.join([
                'no ip routing',
            ]))

    def test_ipv6(self):

        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxe')

        # Create Routing object
        routing = Routing()
        dev1.add_feature(routing)
        routing.device_attr[dev1].enabled_ipv6_unicast_routing = True

        # Build config
        cfgs = routing.build_config(apply=False)

        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            '\n'.join([
                'ipv6 unicast routing',
            ]))

        # Unconfigure
        uncfgs = routing.build_unconfig(apply=False)

        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(uncfgs[dev1.name]),
            '\n'.join([
                'no ipv6 unicast routing',
            ]))

if __name__ == '__main__':
    unittest.main()
